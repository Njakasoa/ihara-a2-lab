#!/usr/bin/env python3
"""Bounded exact local/ray-class component calculation for the M2 modulus.

This script deliberately avoids ``K.maximal_order()`` on the genus-343
five-step function-field tower.  A historical bounded Sage pilot reached that
call but did not return within 120 seconds.  Its exact source and external
timeout command are preserved in
``experiments/m3_sage_maximal_order_pilot.py``; this receipt command does not
rerun that pilot.  The calculation below is instead exact finite-field
arithmetic on the 37 representatives in ``m2-tower.json``.

It computes the principal-unit coordinates of a certified set of T-units in
U_P^(1)/U_P^(2), their F_2 relation rank, and the intersection of the known
relation space with each individual local block.  It does not claim that the
listed T-units exhaust the T-unit group, and it does not infer a full ray
class-group order or local inertia order from this subspace.

Run with::

    scripts/sage-python experiments/m3_ray_structure.py
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from sage.all import GF, PolynomialRing
except ImportError as exc:  # pragma: no cover - only outside Sage.
    raise SystemExit("m3_ray_structure.py must run with scripts/sage-python") from exc

try:
    import sage.version as sage_version_module
except ImportError:  # pragma: no cover - Sage provides this module.
    sage_version_module = None


ROOT = Path(__file__).resolve().parents[1]
CERT_PATH = ROOT / "certificates/m2-tower.json"
ZETA_PATH = ROOT / "certificates/k343-zeta.json"
OUTPUT_PATH = ROOT / "results/m3-ray-structure.json"

BASE_UNIT_NAMES = ("x", "x+1", "y", "y+1", "y+x")
ETA_NAMES = ("eta_1", "eta_x", "eta_x2", "eta_y", "eta_y2")
ALL_UNIT_NAMES = BASE_UNIT_NAMES + ETA_NAMES
H_BASIS_NAMES = ("1", "x", "x^2", "y", "y^2")
HISTORICAL_PILOT_SOURCE = "experiments/m3_sage_maximal_order_pilot.py"
HISTORICAL_PILOT_COMMAND = (
    "timeout 120s scripts/sage-python "
    "experiments/m3_sage_maximal_order_pilot.py"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def installed_sage_version() -> str:
    """Return Sage's runtime version without baking a release into the receipt."""
    if sage_version_module is None:
        return "unavailable"
    value = getattr(sage_version_module, "SAGE_VERSION", None)
    if value is None:
        value = getattr(sage_version_module, "version", None)
    if callable(value):
        value = value()
    return str(value) if value is not None else "unknown"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception as exc:  # pragma: no cover - repository normally exists.
        return f"unavailable:{type(exc).__name__}"


def field_from_bits(bits: int, degree: int, name: str):
    """Reconstruct the exact field encoded by the inventory certificate."""
    require(degree >= 1, "place degree must be positive")
    require(0 <= bits < (1 << (degree + 1)), "modulus bits exceed degree")
    if degree == 1:
        require(bits == 2, "degree-one inventory must use bits=2")
        return GF(2)
    ring = PolynomialRing(GF(2), "m")
    m = ring.gen()
    modulus = ring(sum(((bits >> i) & 1) * m**i for i in range(degree + 1)))
    require(modulus.degree() == degree, "modulus has the wrong degree")
    require(modulus.is_irreducible(), f"modulus is reducible: {modulus}")
    safe = "z" + re.sub(r"[^A-Za-z0-9]", "", name)
    return GF(2**degree, safe, modulus=modulus)


def from_bits(field, value: int):
    value = int(value)
    require(0 <= value < field.cardinality(), "coordinate outside residue field")
    if field.cardinality() == 2:
        return field(value)
    return field.from_integer(value)


def to_bits(value, degree: int) -> int:
    polynomial = value.polynomial()
    return sum(int(polynomial[i]) << i for i in range(degree))


def orbit(point):
    """Return a Frobenius orbit and the first repeated point."""
    initial = tuple(point)
    seen = []
    current = initial
    while current not in seen:
        seen.append(current)
        current = tuple(value * value for value in current)
    return seen, current


def xor_rank(values) -> int:
    """Rank of packed F_2 vectors, using exact integer Gaussian elimination."""
    pivots = {}
    for value in values:
        reduced = int(value)
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


def independent_rows(items):
    """Return independent packed rows and labels in deterministic input order."""
    pivots = {}
    rows = []
    labels = []
    for label, value in items:
        reduced = int(value)
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot][0]
            else:
                pivots[pivot] = (reduced, label)
                rows.append(int(value))
                labels.append(label)
                break
    return rows, labels


def pack_blocks(blocks) -> int:
    """Pack residue-field coordinates into one F_2 vector."""
    packed = 0
    offset = 0
    for value, degree in blocks:
        packed |= to_bits(value, degree) << offset
        offset += degree
    return packed


def valuation_two(value: int) -> int:
    require(value > 0, "2-adic valuation needs a positive integer")
    result = 0
    while value % 2 == 0:
        value //= 2
        result += 1
    return result


def h_basis(x, y):
    return [x**0, x, x**2, y, y**2]


def local_coordinates(entry):
    """Validate one representative and return its exact logarithmic rows.

    At an unramified regular place, if t is a local uniformizer and g is a
    unit, the p-primary coordinate in U^1/U^2 is g'(P)/g(P): raising g to
    2^f-1 removes its odd-order residue and leaves this coefficient.  For
    a!=0, t=x-x(P).  For the selected degree-six a=0 places, t=y-y(P),
    because F_x(P)!=0 and dx=0 in the cotangent space.
    """
    degree = int(entry["degree"])
    field = field_from_bits(
        int(entry["GF_modulus_bits"]), degree, str(entry["id"])
    )
    point = tuple(from_bits(field, value) for value in entry["representative"])
    points, returned = orbit(point)
    require(returned == point, f"{entry['id']}: Frobenius did not return")
    require(len(points) == degree, f"{entry['id']}: wrong Frobenius degree")

    if entry["chart"] == "ramified":
        require(len(point) == 2, f"{entry['id']}: malformed ramified chart")
        x, y = point
        a = x**3 + x + 1
        c = x**5 + x**2 + 1
        require(a != 0 and c == 0, f"{entry['id']}: wrong ramified locus")
        # The two degree-five H places are totally ramified in k/H with
        # e=32.  Every listed unit is a base unit or eta_h=1+O(tau^32), so
        # its U^1/U^2 coordinate at the k-place is exactly zero.
        for value in (x, x + 1, y, y + 1, y + x):
            require(value != 0, f"{entry['id']}: listed T-unit is not a unit")
        return {
            "field": field,
            "point": point,
            "kind": "ramified_k_over_H",
            "coordinates": {name: field(0) for name in ALL_UNIT_NAMES},
            "orbit_length": len(points),
        }

    require(entry["chart"] == "regular", f"{entry['id']}: unknown chart")
    require(len(point) == 7, f"{entry['id']}: malformed regular chart")
    x, y, *z_values = point
    a = x**3 + x + 1
    b = x**2 + x
    c = x**5 + x**2 + 1
    require(y**2 + a * y == b, f"{entry['id']}: H equation failed")
    require(c != 0, f"{entry['id']}: regular chart has c=0")
    basis = h_basis(x, y)
    require(len(z_values) == 5, f"{entry['id']}: wrong AS coordinate count")
    f_values = []
    for z_value, h_value in zip(z_values, basis):
        f_value = b * h_value / (c * c)
        require(z_value**2 + z_value == f_value,
                f"{entry['id']}: AS equation failed")
        require(f_value != 0 and z_value != 0 and z_value + 1 != 0,
                f"{entry['id']}: eta_h is not a regular unit")
        # eta_h=z_h/(z_h+1)=z_h^2/f_h, an identity used below.
        require(z_value / (z_value + 1) == z_value**2 / f_value,
                f"{entry['id']}: eta square-class identity failed")
        f_values.append(f_value)

    for value in (x, x + 1, y, y + 1, y + x):
        require(value != 0, f"{entry['id']}: listed T-unit is not a unit")

    if a != 0:
        # Differentiate y^2+a y=b in characteristic two with respect to x.
        y_prime = ((x**2 + 1) * y + 1) / a
        require(a * y_prime == (x**2 + 1) * y + 1,
                f"{entry['id']}: y derivative check failed")
        uniformizer = "x-x(P)"
        base = {
            "x": 1 / x,
            "x+1": 1 / (x + 1),
            "y": y_prime / y,
            "y+1": y_prime / (y + 1),
            "y+x": (y_prime + 1) / (y + x),
        }
        h_derivatives = [field(0), field(1), field(0), y_prime, field(0)]
        # b'=1 and (c^2)'=0 in characteristic two.
        eta = {
            name: 1 / b + h_derivative / h_value
            for name, h_derivative, h_value in zip(
                ETA_NAMES, h_derivatives, basis
            )
        }
        kind = "regular_x_uniformizer"
    else:
        # All selected a=0 regular places are the degree-six rows.  At a=0,
        # F_x=(x^2+1)y+1 is nonzero; t=y-y(P) is a local parameter and dx=0.
        f_x = (x**2 + 1) * y + 1
        require(f_x != 0, f"{entry['id']}: a=0 chart lacks y uniformizer")
        uniformizer = "y-y(P)"
        base = {
            "x": field(0),
            "x+1": field(0),
            "y": 1 / y,
            "y+1": 1 / (y + 1),
            "y+x": 1 / (y + x),
        }
        # Only h=y has nonzero derivative with respect to this parameter;
        # x, b and c have zero first differential.
        eta = {
            "eta_1": field(0),
            "eta_x": field(0),
            "eta_x2": field(0),
            "eta_y": 1 / y,
            "eta_y2": field(0),
        }
        kind = "regular_y_uniformizer"

    coordinates = dict(base)
    coordinates.update(eta)
    # Check the logarithmic identity dlog(eta_h)=dlog(bh/c^2) directly from
    # the derivative table.  This catches accidental use of the wrong chart.
    for name, f_value, z_value, h_value in zip(
        ETA_NAMES, f_values, z_values, basis
    ):
        eta_value = z_value / (z_value + 1)
        # The first-order coordinate itself is independent of z_value:
        # eta' / eta = f'/f.  Reconstruct eta' from z'=f' and compare.
        if kind == "regular_x_uniformizer":
            y_prime = ((x**2 + 1) * y + 1) / a
            h_derivative = {
                "eta_1": field(0),
                "eta_x": field(1),
                "eta_x2": field(0),
                "eta_y": y_prime,
                "eta_y2": field(0),
            }[name]
            f_prime = (h_value + b * h_derivative) / (c * c)
        else:
            h_derivative = {
                "eta_1": field(0),
                "eta_x": field(0),
                "eta_x2": field(0),
                "eta_y": field(1),
                "eta_y2": field(0),
            }[name]
            f_prime = b * h_derivative / (c * c)
        require(f_prime / f_value == coordinates[name],
                f"{entry['id']}: dlog eta formula failed for {name}")
        # eta itself has an odd-order residue at regular places; its
        # p-primary logarithmic coordinate is eta'/eta.
        z_prime = f_prime
        eta_prime = z_prime / (z_value + 1) ** 2
        require(eta_prime / eta_value == coordinates[name],
                f"{entry['id']}: quotient derivative failed for {name}")

    return {
        "field": field,
        "point": point,
        "kind": kind,
        "uniformizer": uniformizer,
        "coordinates": coordinates,
        "orbit_length": len(points),
    }


def build_receipt() -> dict:
    started = time.perf_counter()
    cert = json.loads(CERT_PATH.read_text())
    zeta = json.loads(ZETA_PATH.read_text())
    entries = cert["selected_allowed_ramification_places"]
    require(len(entries) == 37, "M2 support should have 37 selected places")
    expected_degrees = {5: 2, 6: 16, 8: 16, 10: 2, 12: 1}
    actual_degrees = {}
    for entry in entries:
        actual_degrees[int(entry["degree"])] = actual_degrees.get(
            int(entry["degree"]), 0
        ) + 1
    require(actual_degrees == expected_degrees,
            f"wrong M2 support degrees: {actual_degrees}")

    local_data = []
    coordinate_lists = {name: [] for name in ALL_UNIT_NAMES}
    block_order = []
    offsets = []
    offset = 0
    signatures = set()
    for entry in entries:
        data = local_coordinates(entry)
        signature = (int(entry["degree"]), entry["chart"],
                     tuple(to_bits(v, int(entry["degree"]))
                           for v in data["point"]))
        require(signature not in signatures,
                f"duplicate selected representative: {entry['id']}")
        signatures.add(signature)
        degree = int(entry["degree"])
        offsets.append(offset)
        offset += degree
        block_order.append(entry["id"])
        for name in ALL_UNIT_NAMES:
            coordinate_lists[name].append(
                to_bits(data["coordinates"][name], degree)
            )
        local_data.append({
            "id": entry["id"],
            "degree": degree,
            "chart": entry["chart"],
            "uniformizer": data.get("uniformizer", "ramified local parameter"),
            "local_unit_quotient": {
                "description": "U_P^(1)/U_P^(2) = additive residue field",
                "dimension_over_F2": degree,
                "order": 2**degree,
            },
            "GF_modulus_bits": int(entry["GF_modulus_bits"]),
            "representative_bits": [
                to_bits(value, degree) for value in data["point"]
            ],
            "orbit_length": data["orbit_length"],
        })

    packed_rows = {
        name: pack_blocks(
            (from_bits(
                field_from_bits(
                    int(entry["GF_modulus_bits"]), int(entry["degree"]),
                    str(entry["id"]),
                ),
                coordinate_lists[name][index],
            ), int(entry["degree"]))
            for index, entry in enumerate(entries)
        )
        for name in ALL_UNIT_NAMES
    }
    # The conversion above is intentionally reconstructed from bit encodings;
    # this second packing path verifies that field elements and packed rows
    # agree without relying on a Sage matrix coercion.
    packed_rows_direct = {}
    for name in ALL_UNIT_NAMES:
        packed = 0
        for index, entry in enumerate(entries):
            packed |= coordinate_lists[name][index] << offsets[index]
        packed_rows_direct[name] = packed
    require(packed_rows == packed_rows_direct,
            "reconstructed and direct relation rows disagree")

    relation_items = [(name, packed_rows[name]) for name in ALL_UNIT_NAMES]
    relation_rank = xor_rank(packed_rows.values())
    independent, independent_names = independent_rows(relation_items)
    require(relation_rank == len(independent) == 5,
            "certified T-unit relation rank is not five")
    require(independent_names == list(BASE_UNIT_NAMES),
            f"unexpected independent unit basis: {independent_names}")
    for eta_name in ETA_NAMES:
        require(xor_rank(independent + [packed_rows[eta_name]]) == relation_rank,
                f"{eta_name} added an unexpected relation direction")

    # For each place P, compute both the projection of the known relation
    # space and R_known intersecting the single local block V_P.
    block_rows = []
    for index, entry in enumerate(entries):
        degree = int(entry["degree"])
        mask = ((1 << degree) - 1) << offsets[index]
        outside_rows = [row & ~mask for row in independent]
        local_rows = [(row & mask) >> offsets[index] for row in independent]
        intersection = relation_rank - xor_rank(outside_rows)
        projection_rank = xor_rank(local_rows)
        require(intersection >= 0, "negative relation/block intersection")
        local_data[index]["known_relation_projection_rank"] = projection_rank
        local_data[index]["known_relation_single_block_intersection_dim"] = intersection
        block_rows.append({
            "id": entry["id"],
            "degree": degree,
            "known_relation_projection_rank": projection_rank,
            "known_relation_single_block_intersection_dim": intersection,
            "naive_local_inertia_order_upper_bound": f"2^{degree}",
            "naive_local_inertia_order_upper_bound_integer": 2**degree,
            "exact_local_inertia_order": None,
            "status": "UNKNOWN_FULL_RAY_GROUP",
        })

    # The complete Jacobian order is available from the zeta certificate, but
    # only its 2-adic valuation is used here.  The group structure and rank
    # are deliberately left unknown.
    jacobian_order = int(zeta["k_jacobian_order"])
    require(jacobian_order == sum(int(value) for value in zeta["k_zeta_coefficients"]),
            "zeta certificate Jacobian order mismatch")
    jacobian_v2 = valuation_two(jacobian_order)

    # Five relations remove five dimensions from the 266-dimensional local
    # principal-unit direct sum in the standard split ray exact sequence.
    # Further T-unit relations may remove more dimensions; this is an upper
    # bound on the actual split ray group, not an equality.
    local_dimension = sum(int(entry["degree"]) for entry in entries)
    require(local_dimension == 266, "M2 local dimension is not 266")
    known_quotient_dimension = local_dimension - relation_rank
    ray_order_upper_v2 = jacobian_v2 + known_quotient_dimension
    require(known_quotient_dimension == 261 and ray_order_upper_v2 == 312,
            "unexpected known ray dimension arithmetic")

    elapsed = time.perf_counter() - started
    input_hashes = {
        "certificates/m2-tower.json": sha256_file(CERT_PATH),
        "certificates/k343-zeta.json": sha256_file(ZETA_PATH),
    }
    # The script hash is computed after the source has been written and is
    # stable for reruns at a fixed commit.
    script_hash = sha256_file(Path(__file__).resolve())

    return {
        "experiment_id": "M3-RAY-STRUCTURE-001",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "agent": "m3_sage_ray",
        "git_commit": git_commit(),
        "software": {
            "sage": installed_sage_version(),
            "python": platform.python_version(),
            "finite_field_backend": "Sage GF(2^d), polynomial-basis from certificate bits",
        },
        "runtime_seconds": elapsed,
        "input_hashes_sha256": input_hashes,
        "script_sha256": script_hash,
        "output_path": str(OUTPUT_PATH.relative_to(ROOT)),
        "scope": {
            "base_field": "F2",
            "base_function_field": "k343",
            "genus": 343,
            "splitting_set_T_size": 192,
            "support_multiplicities_by_degree": {"5": 2, "6": 16, "8": 16, "10": 2, "12": 1},
            "modulus": "2 * sum(P for P in selected M2 support)",
            "local_principal_unit_quotient": "U_P^(1)/U_P^(2)",
        },
        "sage_capability_pilot": {
            "status": "HISTORICAL_ONLY_NOT_RERUN",
            "nested_AS_extension_build": "PASS; five successive degree-two extensions constructed (historical pilot)",
            "nested_AS_extension_build_bound_seconds": 1.0,
            "maximal_order_or_place_enumeration": "TIMEOUT_OBSERVED_HISTORICAL",
            "maximal_order_bound_seconds": 120,
            "pilot_source": HISTORICAL_PILOT_SOURCE,
            "pilot_command": HISTORICAL_PILOT_COMMAND,
            "external_timeout_seconds": 120,
            "rerun_by_this_command": False,
            "observed_stage": "K.maximal_order()",
            "interpretation": "historical capability evidence only; full K construction/class/ray API remains unavailable within bounded effort",
        },
        "certified_T_units": [
            {
                "name": "x",
                "expression": "x",
                "justification": "zeros above x=0 and poles above infinity; all six H rational places split in k",
            },
            {
                "name": "x+1",
                "expression": "x+1",
                "justification": "zeros above x=1 and poles above infinity; all six H rational places split in k",
            },
            {
                "name": "y",
                "expression": "y",
                "justification": "Norm_H/F2(x)(y)=b=x(x+1); zeros/poles lie above H rational places",
            },
            {
                "name": "y+1",
                "expression": "y+1",
                "justification": "Norm(y+1)=b+a+1=x^2(x+1); zeros/poles lie above H rational places",
            },
            {
                "name": "y+x",
                "expression": "y+x",
                "justification": "Norm(y+x)=b+ax+x^2=x^2(x+1)^2; zeros/poles lie above H rational places",
            },
            {
                "name": "eta_1",
                "expression": "z_1/(z_1+1), z_1^2+z_1=b/c^2",
                "justification": "eta_h=z_h^2/(b*h/c^2); its zeros/poles are over zeros of b, hence T",
            },
            {
                "name": "eta_x",
                "expression": "z_x/(z_x+1), z_x^2+z_x=bx/c^2",
                "justification": "eta_h=z_h^2/(b*h/c^2); zeros of bx are over H rational places",
            },
            {
                "name": "eta_x2",
                "expression": "z_x2/(z_x2+1), z_x2^2+z_x2=bx^2/c^2",
                "justification": "eta_h=z_h^2/(b*h/c^2); zeros of bx^2 are over H rational places",
            },
            {
                "name": "eta_y",
                "expression": "z_y/(z_y+1), z_y^2+z_y=by/c^2",
                "justification": "eta_h=z_h^2/(b*h/c^2); zeros of by are among H rational places",
            },
            {
                "name": "eta_y2",
                "expression": "z_y2/(z_y2+1), z_y2^2+z_y2=by^2/c^2",
                "justification": "eta_h=z_h^2/(b*h/c^2); zeros of by^2 are among H rational places",
            },
        ],
        "unit_square_class_identity": "eta_h = z_h^2/(b*h/c^2), hence [eta_h]=[b*h] in k*/k*^2",
        "local_places": local_data,
        "block_order": block_order,
        "block_offsets_f2": offsets,
        "local_coordinate_bits_by_unit": coordinate_lists,
        "known_relation_rows_hex": {
            name: hex(value) for name, value in packed_rows.items()
        },
        "known_relation_subspace": {
            "ambient_local_dimension": local_dimension,
            "unit_row_count": len(ALL_UNIT_NAMES),
            "rank_over_F2": relation_rank,
            "independent_units": independent_names,
            "known_relations_quotient_dimension": known_quotient_dimension,
            "eta_rows_add_no_rank": True,
            "interpretation": "exhibited T-unit relations only; additional T-unit relations are unknown",
        },
        "local_projection_and_inertia": block_rows,
        "class_group_component": {
            "complete_Jacobian_order_from_zeta": str(jacobian_order),
            "v2_of_complete_Jacobian_order": jacobian_v2,
            "complete_Jacobian_2_rank": None,
            "complete_Jacobian_2_cyclic_factors": None,
            "status": "ORDER_ONLY",
        },
        "split_ray_class_component": {
            "standard_exact_sequence_local_term_dimension": local_dimension,
            "known_T_unit_relation_rank": relation_rank,
            "known_local_term_quotient_dimension": known_quotient_dimension,
            "conditional_v2_order_upper_bound": ray_order_upper_v2,
            "conditional_order_upper_bound": f"2^{ray_order_upper_v2}",
            "full_order": None,
            "full_2_rank": None,
            "cyclic_factors": None,
            "proof_obligation": "Apply the standard split ray exact sequence and account for all (not only listed) T-units",
            "status": "UPPER_BOUND_FROM_EXHIBITED_RELATIONS_ONLY",
        },
        "conductor_consequence": {
            "exact_mean_conductor_degree": None,
            "M2_bound_unchanged": True,
            "reason": "known relation subspace has zero intersection with every single local block; hidden relations and full inertia remain unknown",
        },
        "verification": {
            "selected_representatives_equations_and_Frobenius": "PASS",
            "regular_local_derivative_formulas": "PASS",
            "ramified_local_coordinate_zero_argument": "PASS_GIVEN_e=32_CERTIFICATE",
            "known_relation_rank": "PASS rank=5",
            "single_block_intersection_all_zero": all(
                row["known_relation_single_block_intersection_dim"] == 0
                for row in block_rows
            ),
            "full_ray_group": "UNKNOWN",
            "full_inertia_orders": "UNKNOWN",
        },
    }


def main() -> None:
    receipt = build_receipt()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("M3_RAY_STRUCTURE_STATUS=PASS")
    print("EXPERIMENT=" + receipt["experiment_id"])
    print("SAGE=" + receipt["software"]["sage"])
    print("LOCAL_DIMENSION=" + str(receipt["known_relation_subspace"]["ambient_local_dimension"]))
    print("KNOWN_RELATION_RANK=" + str(receipt["known_relation_subspace"]["rank_over_F2"]))
    print("KNOWN_QUOTIENT_DIMENSION=" + str(receipt["known_relation_subspace"]["known_relations_quotient_dimension"]))
    print("RAY_V2_ORDER_UPPER_BOUND=" + str(receipt["split_ray_class_component"]["conditional_v2_order_upper_bound"]))
    print("SINGLE_BLOCK_INTERSECTIONS=" + str(all(
        row["known_relation_single_block_intersection_dim"] == 0
        for row in receipt["local_projection_and_inertia"]
    )))
    print("FULL_RAY_GROUP=UNKNOWN")
    print("FULL_INERTIA_ORDERS=UNKNOWN")
    print("RUNTIME_SECONDS=" + str(receipt["runtime_seconds"]))


if __name__ == "__main__":
    main()
