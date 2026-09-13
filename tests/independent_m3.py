#!/usr/bin/env python3
"""Independent M3 arithmetic gate.

This checker intentionally has no import from ``src`` or ``experiments``.
It has three small, separate components:

* exact Fraction arithmetic for the refined and frozen obstruction gates;
* a compact binary-polynomial finite-field implementation for the 37 stored
  ray representatives and their raw relation matrix;
* direct truncated-unit multiplication for groups with at most 4096 elements.

The checker consumes certificates and receipts, but recomputes equations,
Frobenius orbits, local coordinates, ranks, conductor laws, caps and scores.
Receipt status flags are never used as evidence of a PASS.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
from math import isqrt
from pathlib import Path
import platform
import subprocess
import time


F = Fraction


ROOT = Path(__file__).resolve().parents[1]
B = Fraction(196608, 620201)
GENUS = 343
N1 = 192
BASE_UNITS = ("x", "x+1", "y", "y+1", "y+x")
ETA_UNITS = ("eta_1", "eta_x", "eta_x2", "eta_y", "eta_y2")
ALL_UNITS = BASE_UNITS + ETA_UNITS
SUPPORT_DEGREES = (5, 6, 8, 10, 12)
SUPPORT_MULTIPLICITIES = (2, 16, 16, 2, 1)
SUPPORT_NU = (2, 2, 2, 2, 2)
EXPECTED_SUPPORT = dict(zip(SUPPORT_DEGREES, SUPPORT_MULTIPLICITIES))

# These are the exact polynomial-basis encodings present in the certificates.
# Each is checked by the Rabin irreducibility criterion before use.
FIELD_MODULI = {
    1: 3,
    2: 7,
    3: 11,
    4: 19,
    5: 37,
    6: 67,
    8: 283,
    10: 1033,
    12: 4105,
}


class CheckFailure(AssertionError):
    """A certificate or independently recomputed value failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def ceil_log2(value: int) -> int:
    require(value >= 1, "logarithm input must be positive")
    return (value - 1).bit_length()


# ---------------------------------------------------------------------------
# A small independent binary finite field implementation.


def poly_mul(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def poly_mod(value: int, modulus: int) -> int:
    require(modulus > 0, "polynomial modulus must be positive")
    degree = modulus.bit_length() - 1
    while value and value.bit_length() - 1 >= degree:
        value ^= modulus << (value.bit_length() - 1 - degree)
    return value


def poly_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, poly_mod(left, right)
    return left


def poly_pow_mod(base: int, exponent: int, modulus: int) -> int:
    result = 1
    base = poly_mod(base, modulus)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_mul(result, base), modulus)
        base = poly_mod(poly_mul(base, base), modulus)
        exponent >>= 1
    return result


def prime_divisors(value: int) -> tuple[int, ...]:
    result = []
    candidate = 2
    remainder = value
    while candidate * candidate <= remainder:
        if remainder % candidate == 0:
            result.append(candidate)
            while remainder % candidate == 0:
                remainder //= candidate
        candidate += 1
    if remainder > 1:
        result.append(remainder)
    return tuple(result)


def irreducible_binary(modulus: int, degree: int) -> bool:
    if modulus.bit_length() - 1 != degree or not modulus & 1:
        return False
    x = poly_mod(2, modulus)
    if poly_pow_mod(x, 1 << degree, modulus) != x:
        return False
    for prime in prime_divisors(degree):
        test = poly_pow_mod(x, 1 << (degree // prime), modulus) ^ x
        if poly_gcd(test, modulus) != 1:
            return False
    return True


class BinaryField:
    """F_(2^degree), with elements represented by coefficient bit masks."""

    def __init__(self, degree: int, modulus: int):
        require(degree > 0, "field degree must be positive")
        require(irreducible_binary(modulus, degree),
                f"modulus {modulus} is not irreducible of degree {degree}")
        self.degree = degree
        self.modulus = modulus
        self.q = 1 << degree

    def check(self, value: int) -> int:
        require(isinstance(value, int) and 0 <= value < self.q,
                "field coordinate outside its field")
        return value

    def add(self, left: int, right: int) -> int:
        return self.check(left) ^ self.check(right)

    def mul(self, left: int, right: int) -> int:
        self.check(left)
        self.check(right)
        return poly_mod(poly_mul(left, right), self.modulus)

    def square(self, value: int) -> int:
        return self.mul(value, value)

    def power(self, value: int, exponent: int) -> int:
        self.check(value)
        require(exponent >= 0, "field exponent must be nonnegative")
        result = 1
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exponent >>= 1
        return result

    def inverse(self, value: int) -> int:
        self.check(value)
        require(value != 0, "division by zero in finite field")
        return self.power(value, self.q - 2)

    def divide(self, numerator: int, denominator: int) -> int:
        return self.mul(numerator, self.inverse(denominator))

    def trace(self, value: int) -> int:
        self.check(value)
        result = 0
        current = value
        for _ in range(self.degree):
            result ^= current
            current = self.square(current)
        require(result in (0, 1), "finite-field trace did not land in F2")
        return result


def field_for(degree: int, modulus: int | None = None) -> BinaryField:
    if modulus is None:
        modulus = FIELD_MODULI[degree]
    require(modulus == FIELD_MODULI.get(degree, modulus),
            "certificate field modulus differs from the reviewed encoding")
    return BinaryField(degree, modulus)


def frobenius_orbit(point: tuple[int, ...], field: BinaryField):
    seen: list[tuple[int, ...]] = []
    current = point
    while current not in seen:
        seen.append(current)
        current = tuple(field.square(value) for value in current)
    return seen, current


def h_data(x: int, y: int, field: BinaryField) -> tuple[int, int, int]:
    x2 = field.square(x)
    x3 = field.mul(x2, x)
    one = 1
    a = field.add(field.add(x3, x), one)
    b = field.add(x2, x)
    c = field.add(field.add(field.power(x, 5), x2), 1)
    return a, b, c


def h_basis(x: int, y: int, field: BinaryField) -> tuple[int, ...]:
    return (1, x, field.square(x), y, field.square(y))


def raw_representative(row: dict) -> tuple[int, ...]:
    values = row.get("representative")
    if values is None:
        values = row.get("representative_bits")
    require(isinstance(values, list), "place representative is not a list")
    return tuple(int(value) for value in values)


def local_coordinates(row: dict) -> tuple[dict[str, int], tuple[int, ...], int]:
    """Check equations and return independently derived U^1/U^2 coordinates."""
    degree = int(row["degree"])
    modulus = int(row["GF_modulus_bits"])
    field = field_for(degree, modulus)
    point = raw_representative(row)
    require(all(0 <= value < field.q for value in point),
            f"{row.get('id')}: representative leaves residue field")
    orbit, returned = frobenius_orbit(point, field)
    require(returned == point, f"{row.get('id')}: Frobenius did not return")
    require(len(orbit) == degree,
            f"{row.get('id')}: declared degree differs from orbit length")
    require(len(point) in (2, 7), f"{row.get('id')}: malformed point length")

    x, y = point[:2]
    a, b, c = h_data(x, y, field)
    equation = field.add(field.add(field.square(y), field.mul(a, y)), b)
    require(equation == 0, f"{row.get('id')}: H equation failed")

    if row["chart"] == "ramified":
        require(len(point) == 2 and a != 0 and c == 0,
                f"{row.get('id')}: wrong ramified locus")
        for value in (x, field.add(x, 1), y, field.add(y, 1),
                      field.add(y, x)):
            require(value != 0, f"{row.get('id')}: a listed T-unit vanishes")
        return {name: 0 for name in ALL_UNITS}, point, len(orbit)

    require(row["chart"] == "regular" and len(point) == 7,
            f"{row.get('id')}: malformed regular chart")
    z_values = point[2:]
    require(c != 0, f"{row.get('id')}: regular chart has c=0")
    c2 = field.square(c)
    basis = h_basis(x, y, field)
    f_values = []
    for index, (z_value, h_value) in enumerate(zip(z_values, basis)):
        f_value = field.divide(field.mul(b, h_value), c2)
        require(field.add(field.square(z_value), z_value) == f_value,
                f"{row.get('id')}: AS equation {index} failed")
        require(f_value != 0 and z_value != 0
                and field.add(z_value, 1) != 0,
                f"{row.get('id')}: eta_{index} is not a regular unit")
        # z/(z+1)=z^2/f is checked without using it to derive the matrix.
        require(field.divide(z_value, field.add(z_value, 1))
                == field.divide(field.square(z_value), f_value),
                f"{row.get('id')}: eta square-class identity failed")
        f_values.append(f_value)

    for value in (x, field.add(x, 1), y, field.add(y, 1),
                  field.add(y, x)):
        require(value != 0, f"{row.get('id')}: a listed T-unit vanishes")

    zero = 0
    if a != 0:
        x2 = field.square(x)
        numerator = field.add(field.mul(field.add(x2, 1), y), 1)
        y_prime = field.divide(numerator, a)
        require(field.mul(a, y_prime) == numerator,
                f"{row.get('id')}: y derivative equation failed")
        base = {
            "x": field.inverse(x),
            "x+1": field.inverse(field.add(x, 1)),
            "y": field.divide(y_prime, y),
            "y+1": field.divide(y_prime, field.add(y, 1)),
            "y+x": field.divide(field.add(y_prime, 1), field.add(y, x)),
        }
        h_derivatives = (zero, 1, zero, y_prime, zero)
        kind = "regular_x_uniformizer"
    else:
        x2 = field.square(x)
        f_x = field.add(field.mul(field.add(x2, 1), y), 1)
        require(f_x != 0, f"{row.get('id')}: y is not a local uniformizer")
        base = {
            "x": zero,
            "x+1": zero,
            "y": field.inverse(y),
            "y+1": field.inverse(field.add(y, 1)),
            "y+x": field.inverse(field.add(y, x)),
        }
        h_derivatives = (zero, zero, zero, 1, zero)
        kind = "regular_y_uniformizer"

    eta_names = ETA_UNITS
    eta = {}
    for name, h_value, h_derivative in zip(
        eta_names, basis, h_derivatives
    ):
        if kind == "regular_x_uniformizer":
            eta[name] = field.add(
                field.inverse(b), field.divide(h_derivative, h_value)
            )
        else:
            eta[name] = field.divide(h_derivative, h_value)

    coordinates = dict(base)
    coordinates.update(eta)

    # Reconstruct dlog(eta_h) from the AS equation as a second local check.
    for name, f_value, z_value, h_value, h_derivative in zip(
        eta_names, f_values, z_values, basis, h_derivatives
    ):
        if kind == "regular_x_uniformizer":
            f_prime = field.divide(
                field.add(h_value, field.mul(b, h_derivative)), c2
            )
        else:
            f_prime = field.divide(field.mul(b, h_derivative), c2)
        require(field.divide(f_prime, f_value) == coordinates[name],
                f"{row.get('id')}: dlog eta formula failed for {name}")
        eta_value = field.divide(z_value, field.add(z_value, 1))
        z_prime = f_prime
        eta_prime = field.divide(z_prime, field.square(field.add(z_value, 1)))
        require(field.divide(eta_prime, eta_value) == coordinates[name],
                f"{row.get('id')}: quotient derivative failed for {name}")
    return coordinates, point, len(orbit)


# ---------------------------------------------------------------------------
# F2 row operations and the raw ray relation matrix.


def rank_f2(rows) -> int:
    """Row-reduce with the lowest set bit as pivot."""
    pivots: dict[int, int] = {}
    for original in rows:
        reduced = int(original)
        while reduced:
            pivot = (reduced & -reduced).bit_length() - 1
            previous = pivots.get(pivot)
            if previous is None:
                pivots[pivot] = reduced
                break
            reduced ^= previous
    return len(pivots)


def independent_f2(items):
    pivots: dict[int, int] = {}
    rows = []
    labels = []
    for label, original in items:
        reduced = int(original)
        while reduced:
            pivot = (reduced & -reduced).bit_length() - 1
            previous = pivots.get(pivot)
            if previous is None:
                pivots[pivot] = reduced
                rows.append(int(original))
                labels.append(label)
                break
            reduced ^= previous
    return rows, labels


def validate_degree12_lifting(lifting: dict) -> dict:
    rows = lifting["H_degree6_places"]
    require(len(rows) == 13, "degree-12 lifting row count changed")
    field = field_for(6, int(lifting["field_modulus_bits"]))
    signatures = set()
    for index, row in enumerate(rows):
        require(int(row["degree"]) == 6, f"lifting row {index} degree changed")
        point = raw_representative(row)
        require(len(point) == 2, f"lifting row {index} malformed")
        x, y = point
        a, b, c = h_data(x, y, field)
        require(field.add(field.add(field.square(y), field.mul(a, y)), b) == 0,
                f"lifting row {index} H equation failed")
        require(c != 0, f"lifting row {index} lies on c=0")
        vector = [int(value) for value in row["Frobenius_vector"]]
        require(len(vector) == 5 and all(value in (0, 1) for value in vector)
                and any(vector), f"lifting row {index} vector malformed")
        factor = field.divide(b, field.square(c))
        computed = [field.trace(field.mul(factor, h))
                    for h in h_basis(x, y, field)]
        require(computed == vector,
                f"lifting row {index} Frobenius vector changed")
        require(int(row["residue_extension_degree_in_k"]) == 2,
                f"lifting row {index} residue extension changed")
        require(int(row["places_above"]) == 16,
                f"lifting row {index} places-above count changed")
        require(int(row["degree_above"]) == 12,
                f"lifting row {index} degree-above changed")
        orbit, returned = frobenius_orbit(point, field)
        require(returned == point and len(orbit) == 6,
                f"lifting row {index} Frobenius orbit changed")
        signature = min(orbit)
        require(signature not in signatures, "duplicate lifting orbit")
        signatures.add(signature)
    lower_bound = sum(int(row["places_above"]) for row in rows)
    require(lower_bound == 208
            and int(lifting["k_degree12_places_lower_bound"]) == lower_bound,
            "degree-12 lifting lower bound changed")
    return {"rows": len(rows), "orbits": len(signatures),
            "k_degree12_lower_bound": lower_bound}


def validate_ray_payload(ray: dict, tower: dict, zeta: dict) -> dict:
    selected = tower["selected_allowed_ramification_places"]
    local_rows = ray["local_places"]
    require(len(selected) == 37 and len(local_rows) == 37,
            "ray support row count changed")
    expected = EXPECTED_SUPPORT
    actual = {}
    by_id = {}
    for row in selected:
        degree = int(row["degree"])
        actual[degree] = actual.get(degree, 0) + 1
        require(row["id"] not in by_id, "duplicate selected place id")
        by_id[row["id"]] = row
    require(actual == expected, f"ray support multiplicities changed: {actual}")

    local_by_id = {row["id"]: row for row in local_rows}
    require(len(local_by_id) == 37, "duplicate local receipt id")
    coordinate_lists = ray["local_coordinate_bits_by_unit"]
    require(set(coordinate_lists) == set(ALL_UNITS),
            "raw relation matrix unit labels changed")
    for name in ALL_UNITS:
        require(len(coordinate_lists[name]) == 37,
                f"raw relation row length changed for {name}")

    offsets = []
    computed_rows = {name: [] for name in ALL_UNITS}
    block_order = []
    local_results = []
    offset = 0
    signatures = set()
    for index, selected_row in enumerate(selected):
        identifier = selected_row["id"]
        require(identifier in local_by_id, f"missing local row {identifier}")
        local = local_by_id[identifier]
        for key in ("degree", "chart", "GF_modulus_bits"):
            require(int(local[key]) == int(selected_row[key])
                    if key != "chart" else local[key] == selected_row[key],
                    f"changed place {identifier} {key}")
        # Reconstruct coordinates from the raw k representative.  The local
        # receipt's precomputed coordinate flags are only comparison targets.
        coords, point, orbit_length = local_coordinates(selected_row)
        require(raw_representative(local) == point,
                f"changed representative for {identifier}")
        # Canonicalize by the full Frobenius orbit.  A changed conjugate
        # representative must be treated as the same place, rather than
        # slipping through as a distinct raw tuple.
        field = field_for(int(selected_row["degree"]),
                          int(selected_row["GF_modulus_bits"]))
        orbit, _ = frobenius_orbit(point, field)
        signature = (int(selected_row["degree"]), selected_row["chart"],
                     min(orbit))
        require(signature not in signatures, f"duplicate Frobenius orbit {identifier}")
        signatures.add(signature)
        degree = int(selected_row["degree"])
        offsets.append(offset)
        offset += degree
        block_order.append(identifier)
        for name in ALL_UNITS:
            value = int(coords[name])
            require(value == int(coordinate_lists[name][index]),
                    f"raw local coordinate changed at {identifier}/{name}")
            computed_rows[name].append(value)
        require(int(local["orbit_length"]) == orbit_length,
                f"orbit length receipt changed at {identifier}")
        require(int(local["local_unit_quotient"]["dimension_over_F2"]) == degree
                and int(local["local_unit_quotient"]["order"]) == 1 << degree,
                f"local quotient metadata changed at {identifier}")
        local_results.append({"id": identifier, "degree": degree,
                              "orbit_length": orbit_length,
                              "chart": selected_row["chart"]})

    require(offset == 266, f"local direct-sum dimension changed: {offset}")
    require(offsets == [int(value) for value in ray["block_offsets_f2"]],
            "block offsets changed")
    require(block_order == ray["block_order"], "block order changed")

    packed = {}
    for name in ALL_UNITS:
        value = 0
        for index, coordinate in enumerate(computed_rows[name]):
            value |= coordinate << offsets[index]
        packed[name] = value
        expected_hex = ray["known_relation_rows_hex"][name]
        require(value == int(expected_hex, 16),
                f"packed relation row changed for {name}")

    items = [(name, packed[name]) for name in ALL_UNITS]
    independent, labels = independent_f2(items)
    rank = rank_f2(packed.values())
    require(rank == 5 and labels == list(BASE_UNITS),
            f"raw matrix rank/basis changed: rank={rank}, labels={labels}")
    for name in ETA_UNITS:
        require(rank_f2(independent + [packed[name]]) == rank,
                f"eta row {name} adds a relation direction")

    intersections = []
    projections = []
    for index, selected_row in enumerate(selected):
        degree = int(selected_row["degree"])
        mask = ((1 << degree) - 1) << offsets[index]
        outside = [row & ~mask for row in independent]
        inside = [(row & mask) >> offsets[index] for row in independent]
        intersection = rank - rank_f2(outside)
        projection = rank_f2(inside)
        require(intersection == 0,
                f"known relation intersects block {selected_row['id']}")
        intersections.append(intersection)
        projections.append(projection)
        local = local_by_id[selected_row["id"]]
        require(int(local["known_relation_single_block_intersection_dim"])
                == intersection
                and int(local["known_relation_projection_rank"]) == projection,
                f"block rank metadata changed at {selected_row['id']}")

    jacobian_order = int(zeta["k_jacobian_order"])
    require(jacobian_order == sum(int(value)
                                  for value in zeta["k_zeta_coefficients"]),
            "zeta Jacobian checksum changed")
    v2 = 0
    temp = jacobian_order
    while temp % 2 == 0:
        v2 += 1
        temp //= 2
    subspace = ray["known_relation_subspace"]
    require(int(subspace["ambient_local_dimension"]) == 266
            and int(subspace["unit_row_count"]) == 10
            and int(subspace["rank_over_F2"]) == rank
            and subspace["independent_units"] == list(BASE_UNITS)
            and int(subspace["known_relations_quotient_dimension"]) == 261,
            "known relation subspace metadata changed")
    require(ray["split_ray_class_component"]["conditional_v2_order_upper_bound"]
            == 312,
            "ray order upper-bound metadata changed")
    require(ray["class_group_component"]["v2_of_complete_Jacobian_order"] == v2 == 51,
            "Jacobian 2-adic valuation metadata changed")
    return {"places": len(selected), "local_dimension": offset, "rank": rank,
            "independent_units": labels, "single_block_intersections": intersections,
            "projection_ranks": projections, "jacobian_v2": v2}


# ---------------------------------------------------------------------------
# Direct local-unit arithmetic, separate from src/m3_local_units.py.


def unit_multiply(left: tuple[int, ...], right: tuple[int, ...],
                  field: BinaryField, nu: int) -> tuple[int, ...]:
    require(len(left) == len(right) == nu - 1,
            "truncated unit coefficient length changed")
    result = [field.add(a, b) for a, b in zip(left, right)]
    for j in range(2, nu):
        cross = 0
        for i in range(1, j):
            cross = field.add(
                cross, field.mul(left[i - 1], right[j - i - 1])
            )
        result[j - 1] = field.add(result[j - 1], cross)
    return tuple(result)


def subgroup_filtration(elements, r: int) -> set[tuple[int, ...]]:
    if r <= 1:
        return set(elements)
    return {element for element in elements
            if all(value == 0 for value in element[:r - 1])}


def log2_exact(value: int) -> int:
    require(value > 0 and value & (value - 1) == 0,
            f"expected power of two, got {value}")
    return value.bit_length() - 1


def direct_local_fixture(f: int, nu: int) -> dict:
    require(nu >= 1, "local cutoff must be positive")
    field = field_for(f)
    q = field.q
    order_expected = q ** (nu - 1)
    require(order_expected <= 4096,
            f"local direct enumeration exceeded cap at ({f},{nu})")
    elements = tuple(itertools.product(range(q), repeat=nu - 1))
    require(len(elements) == order_expected, "enumerator cardinality mismatch")
    identity = (0,) * (nu - 1)
    for left, right in ((elements[0], elements[-1]),
                        (elements[-1], elements[0])):
        require(unit_multiply(left, right, field, nu)
                == unit_multiply(right, left, field, nu),
                "truncated unit multiplication is not commutative")
    squares = {unit_multiply(element, element, field, nu)
               for element in elements}

    order_profile = {}
    killed_logs = []
    for element in elements:
        if element == identity:
            element_order = 1
        else:
            element_order = 1
            power = element
            while power != identity:
                power = unit_multiply(power, power, field, nu)
                element_order *= 2
                require(element_order <= (1 << ceil_log2(nu)),
                        "local element exponent exceeds formula")
        order_profile[element_order] = order_profile.get(element_order, 0) + 1

    exponent_index = ceil_log2(nu)
    for j in range(1, exponent_index + 1):
        killed = 0
        for element in elements:
            power = element
            for _ in range(j):
                power = unit_multiply(power, power, field, nu)
            killed += power == identity
        killed_logs.append(log2_exact(killed))

    valuation_sizes = []
    full_cumulative = []
    for r in range(nu + 1):
        if r == 0:
            full_cumulative.append(1)
        else:
            subgroup = subgroup_filtration(elements, r)
            valuation_sizes.append(len(subgroup))
            full_cumulative.append(order_expected // len(subgroup))
    # r=1 has the same p-primary character count as r=0; the direct subgroup
    # quotient also records this since U^1 is the whole group.
    require(full_cumulative[0] == full_cumulative[1] == 1,
            "conductor-one wild jump appeared")

    as_cumulative = []
    square_size = len(squares)
    for r in range(nu + 1):
        subgroup = subgroup_filtration(elements, r)
        # |G/(G^2 H_r)| = |G| |G^2 cap H_r|/(|G^2||H_r|).
        quotient = (order_expected * len(squares & subgroup)
                    // (square_size * len(subgroup)))
        as_cumulative.append(quotient)

    full_exact = tuple(full_cumulative[i] - (full_cumulative[i - 1]
                                              if i else 0)
                       for i in range(nu + 1))
    as_exact = tuple(as_cumulative[i] - (as_cumulative[i - 1] if i else 0)
                     for i in range(nu + 1))
    full_average = Fraction(sum(i * value for i, value in enumerate(full_exact)),
                            order_expected)
    as_order = order_expected // square_size
    as_average = Fraction(sum(i * value for i, value in enumerate(as_exact)),
                          as_order)

    # Closed formulae are derived independently here and checked against the
    # operation-by-operation enumeration above.
    killed_expected = tuple(
        f * (((nu + (1 << (j - 1)) - 1) >> (j - 1))
             - ((nu + (1 << j) - 1) >> j))
        for j in range(1, exponent_index + 1)
    )
    full_expected = tuple(
        1 if r <= 1 else q ** (r - 1) for r in range(nu + 1)
    )
    as_expected = tuple(q ** (r // 2) for r in range(nu + 1))
    killed_counts = tuple(
        killed_logs[0:1]
        + [killed_logs[index] - killed_logs[index - 1]
           for index in range(1, len(killed_logs))]
    )
    require(killed_counts == killed_expected,
            f"killed-layer profile changed at ({f},{nu})")
    require(tuple(full_cumulative) == full_expected,
            f"full conductor law changed at ({f},{nu})")
    require(tuple(as_cumulative) == as_expected,
            f"AS conductor law changed at ({f},{nu})")

    full_tail = Fraction(0) if nu == 1 else Fraction(nu, 1)
    if nu > 1:
        full_tail -= Fraction(2, q ** (nu - 1))
        for j in range(1, nu - 1):
            full_tail -= Fraction(1, q ** j)
    s = nu // 2
    as_tail = Fraction(2 * s, 1)
    for j in range(1, s + 1):
        as_tail -= Fraction(2, q ** j)
    require(full_average == full_tail and as_average == as_tail,
            f"local average formula changed at ({f},{nu})")
    local_rebate = Fraction(f * s, 1) - Fraction(f, 2) * as_average
    expected_rebate = (Fraction(f, q - 1) * (1 - Fraction(1, q ** s))
                       if s else Fraction(0))
    require(local_rebate == expected_rebate,
            f"elementary rebate changed at ({f},{nu})")
    expected_rank = f * (nu // 2)
    require(log2_exact(order_expected // square_size) == expected_rank,
            f"local 2-rank changed at ({f},{nu})")
    expected_exponent = 1 if nu == 1 else 1 << ceil_log2(nu)
    require(max(order_profile) == expected_exponent,
            f"local exponent changed at ({f},{nu})")
    relation_c = expected_rank * (expected_rank + 1)
    return {
        "f": f,
        "nu": nu,
        "order": order_expected,
        "p_rank": expected_rank,
        "exponent": expected_exponent,
        "cyclic_order_profile": {str(k): v for k, v in sorted(order_profile.items())},
        "killed_layers": list(killed_counts),
        "full_cumulative": list(full_cumulative),
        "full_average": str(full_average),
        "as_cumulative": list(as_cumulative),
        "as_average": str(as_average),
        "elementary_rebate": str(local_rebate),
        "refined_relation_C": relation_c,
    }


def direct_local_checks() -> dict:
    fixtures = (
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (4, 2), (6, 2), (12, 2),
    )
    reports = [direct_local_fixture(f, nu) for f, nu in fixtures]
    return {"method": "direct truncated polynomial multiplication over binary fields",
            "group_order_cap": 4096,
            "fixtures": [list(item) for item in fixtures],
            "reports": reports}


# ---------------------------------------------------------------------------
# Frozen and refined obstruction arithmetic.


def validate_frozen(frozen: dict) -> dict:
    require(frozen["bound"] == str(B), "frozen baseline fraction changed")
    require(int(frozen["genus"]) == GENUS
            and int(frozen["rational_places"]) == N1,
            "frozen genus or rational count changed")
    require([int(v) for v in frozen["degrees"]] == list(SUPPORT_DEGREES)
            and [int(v) for v in frozen["multiplicities"]]
            == list(SUPPORT_MULTIPLICITIES)
            and [int(v) for v in frozen["nu"]] == list(SUPPORT_NU),
            "frozen support degree, multiplicity, or nu changed")
    rows = list(zip(SUPPORT_DEGREES, SUPPORT_MULTIPLICITIES))
    a_value = sum(f * m for f, m in rows)
    c_value = sum(f * (f + 1) * m for f, m in rows)
    d_value = 1 + a_value - N1
    margin = d_value * d_value - 2 * c_value - 4 * a_value
    cost = sum(F(f * (1 - F(1, 2 ** f))) * m for f, m in rows)
    denominator = F(GENUS - 1) + cost
    ratio = F(N1) / denominator
    expected = {"A": a_value, "C": c_value, "D": d_value, "I": margin,
                "denominator": str(denominator), "ratio": str(ratio)}
    require(a_value == 266 and c_value == 2260 and d_value == 75
            and margin == 41 and expected["denominator"] == "620201/1024"
            and ratio == B, "frozen baseline arithmetic changed")
    for key, value in (("A", a_value), ("C", c_value), ("D", d_value),
                       ("I", margin)):
        require(int(frozen[key]) == value, f"frozen field {key} changed")
    require(frozen["denominator"] == str(denominator),
            "frozen denominator changed")
    return expected


def refined_beta() -> Fraction:
    return sum(
        m * f * (Fraction(1, 2 ** f - 1) - Fraction(1, 1023))
        for f, m in ((5, 2), (6, 16), (8, 16))
    )


def refined_pairs() -> dict:
    beta = refined_beta()
    counts = {"pairs_tested": 0, "splitting_rejected": 0,
              "relation_rejected": 0}
    caps = []
    survivors = []
    for n in range(N1):
        endpoint = (F(N1 - n) / B - (GENUS - 1) + n
                    + beta - F(n, 1023)) * F(1023, 1022)
        # The strict inequality is A < endpoint, so even an integral
        # endpoint contributes its integer predecessor.
        cap = (endpoint.numerator - 1) // endpoint.denominator
        caps.append({"n": n, "strict_A_endpoint": endpoint, "A_cap": cap})
        for a_value in range(n, cap + 1):
            counts["pairs_tested"] += 1
            lower_cost = max(F(0), F(a_value - n) - beta
                             - F(a_value - n, 1023))
            t_min = floor_fraction(B * (GENUS - 1 + lower_cost)) + 1
            if t_min > min(a_value, N1 - n):
                counts["splitting_rejected"] += 1
                continue
            c_min = max(0, 11 * a_value - 690 - 25 * n)
            c_max = ((1 + a_value - t_min) ** 2 - 4 * a_value) // 2
            if c_min > c_max:
                counts["relation_rejected"] += 1
                continue
            survivors.append({"n": n, "A": a_value, "t_min": t_min,
                              "t_max": min(a_value, N1 - n),
                              "C_min": c_min, "C_max": c_max})
    expected_survivors = [{"n": 0, "A": 266, "t_min": 192,
                           "t_max": 192, "C_min": 2236, "C_max": 2280}]
    require(counts == {"pairs_tested": 11384, "splitting_rejected": 7862,
                       "relation_rejected": 3521},
            f"refined finite counts changed: {counts}")
    require(survivors == expected_survivors,
            f"refined survivors changed: {survivors}")
    return {"beta": beta, "counts": counts, "caps": caps,
            "survivors": survivors}


def refined_assignment(rows: list[list[int]], inventory: dict[int, int]) -> dict:
    stocks: dict[int, int] = {}
    a_value = 0
    c_value = 0
    rational = 0
    cost = Fraction(0)
    for row in rows:
        require(isinstance(row, list) and len(row) == 3,
                "refined assignment row malformed")
        f, multiplicity, nu = (int(value) for value in row)
        require(f >= 1 and multiplicity >= 1 and nu >= 2,
                "invalid refined assignment row")
        stocks[f] = stocks.get(f, 0) + multiplicity
        rational += multiplicity if f == 1 else 0
        s = nu // 2
        local_a = f * s
        a_value += multiplicity * local_a
        c_value += multiplicity * local_a * (local_a + 1)
        rebate = Fraction(f, 2 ** f - 1) * (1 - Fraction(1, 2 ** local_a))
        cost += multiplicity * (local_a - rebate)
    require(all(multiplicity <= inventory.get(f, 0)
                for f, multiplicity in stocks.items()), "assignment stock exceeded")
    q_value = 2 * c_value + 4 * a_value
    root = isqrt(q_value)
    ceil_root = root + (root * root != q_value)
    t_value = max(0, min(N1 - rational, a_value, 1 + a_value - ceil_root))
    denominator = GENUS - 1 + cost
    margin = (1 + a_value - t_value) ** 2 - 2 * c_value - 4 * a_value
    return {"rows": rows, "T_size": t_value, "rational_support": rational,
            "A": a_value, "C_refined": c_value, "D": 1 + a_value - t_value,
            "GS_margin": margin, "conductor_average_bound": str(2 * cost),
            "genus_denominator": str(denominator),
            "exact_score": str(F(t_value) / denominator)}


def validate_refined_record(record: dict, inventory: dict[int, int],
                            old_record: dict | None = None) -> dict:
    data = record["data"]
    beta = refined_beta()
    require(data["baseline"] == str(B) and data["beta"] == str(beta),
            "refined baseline or beta changed")
    require(int(data["genus"]) == GENUS and int(data["N1"]) == N1,
            "refined base metadata changed")
    finite = refined_pairs()
    require(data["counts"] == finite["counts"], "refined pair counts changed")
    actual_caps = data["caps"]
    require(len(actual_caps) == len(finite["caps"]), "refined cap count changed")
    for actual, expected in zip(actual_caps, finite["caps"]):
        require(actual["n"] == expected["n"]
                and actual["A_cap"] == expected["A_cap"]
                and Fraction(actual["strict_A_endpoint"]) == expected["strict_A_endpoint"],
                f"refined cap changed at n={expected['n']}")
    require(data["survivors"] == finite["survivors"],
            "refined survivor certificate changed")
    # Derive the deep penalties and the two residual Cauchy cases from the
    # reviewed low-degree stocks.  The receipt is compared only afterwards.
    def deficit(degree: int, s_value: int) -> int:
        local_a = degree * s_value
        return local_a * (local_a - 10)

    derived_penalties = {
        "f5_s2": deficit(5, 2) - deficit(5, 1),
        "f5_s3": deficit(5, 3) - deficit(5, 1),
        "f6_s2": deficit(6, 2) - deficit(6, 1),
        "f8_s2": deficit(8, 2) - deficit(8, 1),
        "f10_s2": deficit(10, 2) - deficit(10, 1),
    }
    require(data["deep_penalties"] == derived_penalties,
            "refined deep penalty constants changed")
    survivor = finite["survivors"][0]
    derived_slack = survivor["C_max"] - survivor["C_min"]
    require(int(data["remaining_slack"]) == derived_slack,
            "refined remaining slack changed")
    stock5, stock6, stock8 = (inventory.get(5, 0), inventory.get(6, 0),
                              inventory.get(8, 0))
    require((stock5, stock6, stock8) == (2, 16, 16),
            "reviewed low-degree stocks changed")
    residuals = []
    for omitted8 in (0, 1):
        selected8 = stock8 - omitted8
        # One f=5 place is moved from depth two to depth four; all other
        # low places stay shallow.  This is the only deep pattern allowed by
        # the independently derived 44-unit penalty budget.
        low_mass = 10 + 5 * (stock5 - 1) + 6 * stock6 + 8 * selected8
        low_cost = 110 + 30 * (stock5 - 1) + 42 * stock6 + 72 * selected8
        high_mass = survivor["A"] - low_mass
        c_budget = survivor["C_max"] - low_cost
        number_cap = high_mass // 10
        cauchy = Fraction(high_mass * high_mass, number_cap) + high_mass
        residuals.append({
            "omitted_degree8": omitted8,
            "high_degree_rank_mass": high_mass,
            "C_budget": c_budget,
            "number_cap": number_cap,
            "Cauchy_lower_bound": str(cauchy),
            "rejected": cauchy > c_budget,
        })
    require(data["residual_high_degree_patterns"] == residuals,
            "refined residual obstruction changed")
    require(data["exact_optimum"] == str(B), "refined optimum changed")

    assignments = data["assignments"]
    require(isinstance(assignments, list) and assignments,
            "refined assignments missing")
    recomputed = []
    for actual in assignments:
        expected = refined_assignment(actual["rows"], inventory)
        for key, value in expected.items():
            require(actual[key] == value,
                    f"refined assignment field changed: {key}")
        recomputed.append(expected)
    require(recomputed[0]["exact_score"] == str(B)
            and all(F(item["exact_score"]) <= B for item in recomputed),
            "refined assignment optimum changed")
    if old_record is not None:
        require(data["terminal_dependency"]
                == "frozen independent M2 all-degree nu2 obstruction",
                "refined terminal dependency changed")
    return {"beta": str(beta), "counts": finite["counts"],
            "survivor": finite["survivors"][0],
            "assignment_count": len(assignments),
            "exact_optimum": str(B)}


def old_pair_crosscheck(old_record: dict) -> dict:
    finite = old_record["data"]["finite_certificate"]
    counts = {"pairs_tested": 0, "splitting_rejected": 0,
              "relation_rejected": 0}
    survivors = []
    old_special = Fraction(37, 16)
    for n in range(N1):
        endpoint = (Fraction(269993, 1024) + old_special
                    - n * (1 / B - Fraction(1, 2))) * Fraction(1024, 1023)
        cap = (endpoint.numerator - 1) // endpoint.denominator
        for a_value in range(n, cap + 1):
            counts["pairs_tested"] += 1
            lower_cost = max(F(0), F(a_value) - F(n, 2)
                             - old_special - F(a_value, 1024))
            t_min = floor_fraction(B * (GENUS - 1 + lower_cost)) + 1
            if t_min > min(a_value, N1 - n):
                counts["splitting_rejected"] += 1
                continue
            c_min = max(0, 11 * a_value - 690 - 10 * n)
            c_max = ((1 + a_value - t_min) ** 2 - 4 * a_value) // 2
            if c_min > c_max:
                counts["relation_rejected"] += 1
                continue
            survivors.append({"rational_support": n, "A": a_value,
                              "t_min": t_min, "t_max": min(a_value, N1 - n),
                              "C_min": c_min, "C_max": c_max})
    require(counts == finite["counts"], "old obstruction count changed")
    require(survivors == finite["survivors"], "old obstruction survivor changed")
    return {"counts": counts, "survivors": survivors}


# ---------------------------------------------------------------------------
# Mutation gate and receipt.


def rejected(label: str, value, validator) -> str:
    try:
        validator(value)
    except Exception:
        return "REJECTED"
    return "ACCEPTED"


def mutation_checks(frozen: dict, lifting: dict, ray: dict, tower: dict,
                    zeta: dict, refined: dict, inventory: dict[int, int]) -> dict:
    statuses = {}

    mutated = deepcopy(tower)
    mutated["selected_allowed_ramification_places"][0]["degree"] += 1
    statuses["changed_place_degree"] = rejected(
        "changed_place_degree", mutated,
        lambda value: validate_ray_payload(ray, value, zeta))

    mutated = deepcopy(lifting)
    mutated["H_degree6_places"][0]["Frobenius_vector"][0] ^= 1
    statuses["changed_frobenius_vector"] = rejected(
        "changed_frobenius_vector", mutated, validate_degree12_lifting)

    mutated = deepcopy(frozen)
    mutated["nu"][0] += 2
    statuses["changed_nu"] = rejected("changed_nu", mutated, validate_frozen)

    mutated = deepcopy(ray)
    mutated["known_relation_subspace"]["rank_over_F2"] += 1
    statuses["changed_group_rank"] = rejected(
        "changed_group_rank", mutated,
        lambda value: validate_ray_payload(value, tower, zeta))

    mutated = deepcopy(frozen)
    mutated["multiplicities"][0] += 1
    statuses["changed_support_multiplicity"] = rejected(
        "changed_support_multiplicity", mutated, validate_frozen)

    mutated = deepcopy(refined)
    mutated["data"]["assignments"][0]["GS_margin"] += 1
    statuses["changed_GS_margin"] = rejected(
        "changed_GS_margin", mutated,
        lambda value: validate_refined_record(value, inventory))

    mutated = deepcopy(refined)
    mutated["data"]["caps"][0]["A_cap"] += 1
    statuses["changed_proof_cap"] = rejected(
        "changed_proof_cap", mutated,
        lambda value: validate_refined_record(value, inventory))

    mutated = deepcopy(refined)
    mutated["data"]["beta"] = str(refined_beta() + 1)
    statuses["changed_proof_constant"] = rejected(
        "changed_proof_constant", mutated,
        lambda value: validate_refined_record(value, inventory))

    mutated = deepcopy(refined)
    mutated["data"]["survivors"] = []
    statuses["changed_survivors"] = rejected(
        "changed_survivors", mutated,
        lambda value: validate_refined_record(value, inventory))
    require(all(value == "REJECTED" for value in statuses.values()),
            f"a required mutation was accepted: {statuses}")
    return statuses


def run(output: Path) -> dict:
    started = time.perf_counter()
    frozen = json.loads((ROOT / "certificates/m2-frozen.json").read_text())
    tower = json.loads((ROOT / "certificates/m2-tower.json").read_text())
    zeta_data = json.loads((ROOT / "certificates/k343-zeta.json").read_text())
    lifting = json.loads((ROOT / "certificates/degree12-lifting.json").read_text())
    ray = json.loads((ROOT / "results/m3-ray-structure.json").read_text())
    old_record = json.loads((ROOT / "results/m3-obstruction.json").read_text())
    refined = json.loads((ROOT / "results/m3-refined-obstruction.json").read_text())
    inventory_data = json.loads((ROOT / "curves/k343-place-counts-30.json").read_text())
    require(inventory_data["place_counts"][:12]
            == [192, 0, 0, 0, 2, 16, 0, 16, 0, 64, 0, 208],
            "reviewed place inventory changed")
    inventory = dict(enumerate(inventory_data["place_counts"], 1))

    frozen_result = validate_frozen(frozen)
    lifting_result = validate_degree12_lifting(lifting)
    ray_result = validate_ray_payload(ray, tower, zeta_data)
    local_result = direct_local_checks()
    old_result = old_pair_crosscheck(old_record)
    refined_result = validate_refined_record(refined, inventory, old_record)
    mutations = mutation_checks(frozen, lifting, ray, tower,
                                zeta_data, refined, inventory)

    input_paths = [
        "M3_RESULT.md", "M2_BASELINE.md",
        "proofs/M3_NONUNIFORM_OBSTRUCTION.md",
        "proofs/EXCHANGE_LEMMAS_M3.md",
        "proofs/NONUNIFORM_CONDUCTOR_LOCAL_THEORY.md",
        "proofs/M3_REFINED_RAY_CRITERION.md",
        "proofs/M3_REFINED_OBSTRUCTION.md",
        "experiments/m3_obstruction.py", "experiments/m3_refined_obstruction.py",
        "experiments/m3_ray_structure.py", "experiments/m3_local_units.py",
        "src/m3_local_units.py",
        "certificates/m2-frozen.json", "certificates/m2-tower.json",
        "certificates/k343-zeta.json", "certificates/degree12-lifting.json",
        "curves/k343-place-counts-30.json", "results/m3-ray-structure.json",
        "results/m3-obstruction.json", "results/m3-refined-obstruction.json",
    ]
    input_hashes = {path: sha256_file(ROOT / path) for path in input_paths}
    payload = {
        "baseline": frozen_result,
        "degree12_lifting": lifting_result,
        "ray_matrix": ray_result,
        "local_units": local_result,
        "old_obstruction_crosscheck": old_result,
        "refined_obstruction": refined_result,
        "adversarial_mutations": mutations,
        "coverage": {
            "production_imports": [],
            "raw_ray_relation_matrix_recomputed": True,
            "finite_field_equations_and_frobenius_recomputed": True,
            "local_unit_operation_enumeration": True,
            "refined_all_depth_pair_caps": True,
            "unknowns": [
                "full split ray-class-group order, rank, and cyclic factors",
                "full T-unit relation space and exact local inertia orders",
                "exact global conductor means and actual tower ratios",
                "a new unconditional A(2) bound beyond the frozen theorem",
            ],
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    elapsed = time.perf_counter() - started
    utc = datetime.now(timezone.utc).isoformat()
    report = {
        "experiment_id": "M3-INDEPENDENT-VALIDATION-001",
        "UTC": utc,
        "timestamp_utc": utc,
        "commit": commit(),
        "agent": "/root/m3_independent_tester",
        "software_versions": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "runtime_seconds": round(elapsed, 6),
        "input_hashes_sha256": input_hashes,
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "payload_sha256": hashlib.sha256(canonical).hexdigest(),
        "verification_status": "PASS",
        "status": "PASS",
        "method": "independent standard-library arithmetic; no production imports",
        "data": payload,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("M3_INDEPENDENT_VALIDATION=PASS")
    print("REFINED_COUNTS=" + json.dumps(refined_result["counts"], sort_keys=True))
    print("REFINED_SURVIVOR=" + json.dumps(refined_result["survivor"], sort_keys=True))
    print("RAY_MATRIX=" + json.dumps(ray_result, sort_keys=True))
    print("LOCAL_FIXTURES=" + str(len(local_result["fixtures"])))
    print("MUTATIONS=" + json.dumps(mutations, sort_keys=True))
    print("RUNTIME_SECONDS=" + str(report["runtime_seconds"]))
    return report


if __name__ == "__main__":
    run(ROOT / "results/m3-independent.json")
