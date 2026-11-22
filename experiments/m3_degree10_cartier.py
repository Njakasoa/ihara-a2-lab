"""Test the necessary logarithmic-derivative identity after trace descent.

The proof bounds each coefficient of s = dlog(u) / dlog((x+1)c)
in the square-free Artin--Schreier monomial basis. On eight auxiliary
fibres we evaluate the differential equation on these 583 columns.
Its binary kernel bounds every possible s, regardless of whether a
particular vector in the kernel comes from a T-unit.
"""

import argparse
import json
from pathlib import Path

from sage.all import GF, PolynomialRing, matrix
from sage.env import SAGE_VERSION

from m3_degree6_norm_obstruction import SUPPORT, check_fibre
from m3_ray_structure import field_from_bits, from_bits, local_coordinates, require, sha256_file, xor_rank

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "m3-degree10-cartier.json"
AUXILIARY_POINTS = [(32, 2409), (32, 2304), (33, 1258), (33, 163),
                    (105, 3563), (105, 72), (163, 2336), (163, 32)]


def coefficient_basis():
    """x^n y^j times the AS monomial of mask I, divided by x*c^(4-|I|)."""
    columns = []
    for mask in range(31):
        pole_order = 4 - mask.bit_count()
        degree = 1 + 5*pole_order
        for y_power, max_degree in [(0, degree + 1), (1, degree - 2)]:
            for n in range(max_degree + 1):
                columns.append((mask, pole_order, y_power, n))
    require(len(columns) == 583, "unexpected coefficient-space dimension")
    return columns


def as_values(x, y):
    a, b, c = x**3 + x + 1, x**2 + x, x**5 + x**2 + 1
    require(a and c and y**2 + a*y == b, "point off the unramified x chart")
    dy = (1 + (x**2 + 1)*y)/a
    h = [1, x, x**2, y, y**2]
    derivatives = [0, 1, 0, dy, 0]
    return ([b*value/c**2 for value in h],
            [(value + b*dvalue)/c**2 for value, dvalue in zip(h, derivatives)])


def coefficient_values(columns, x, y):
    """Value and x-derivative of the base factor of each column."""
    a, c = x**3 + x + 1, x**5 + x**2 + 1
    dy = (1 + (x**2 + 1)*y)/a
    factors = []
    for mask, pole_order, y_power, n in columns:
        denominator = x*c**pole_order
        log_derivative = 1/x + (pole_order % 2)*x**4/c
        numerator = x**n
        derivative = x**(n-1) if n % 2 else x.parent().zero()
        if y_power:
            numerator, derivative = numerator*y, derivative*y + numerator*dy
        value = numerator/denominator
        factors.append((mask, value, derivative/denominator + value*log_derivative))
    return factors


def as_monomials(z, dz):
    """Values and x-derivatives of all 32 square-free monomials."""
    field = z[0].parent()
    monomials = [(field.one(), field.zero())]
    for root, derivative in zip(z, dz):
        monomials += [(v*root, dv*root + v*derivative) for v, dv in monomials]
    return monomials


def logarithmic_factor(x):
    c = x**5 + x**2 + 1
    return (x**4 + x**2 + 1)/((x + 1)*c)


def cartier_matrix(columns):
    field = field_from_bits(4105, 12, "cartier_aux")
    encoding = {from_bits(field, i): i for i in range(4096)}
    variable = PolynomialRing(field, "Z").gen()
    rows, ranks = [], []
    for x_bits, y_bits in AUXILIARY_POINTS:
        x, y = (from_bits(field, i) for i in (x_bits, y_bits))
        as_rhs, derivatives = as_values(x, y)
        roots = []
        for rhs in as_rhs:
            pair = (variable**2 + variable + rhs).roots(multiplicities=False)
            require(len(pair) == 2, "the auxiliary fibre must split geometrically")
            roots.append(min(pair, key=encoding.__getitem__))
        factors = coefficient_values(columns, x, y)
        gamma = logarithmic_factor(x)
        require(gamma, "auxiliary fibre is a zero of the reference differential")
        for translation in range(32):
            z = [root + ((translation >> i) & 1) for i, root in enumerate(roots)]
            monomials = as_monomials(z, derivatives)
            defects = []
            for mask, base, base_derivative in factors:
                v, dv = monomials[mask]
                s = base*v
                ds = base_derivative*v + base*dv
                defects.append(encoding[ds/gamma + s**2 + s])
            rows.extend([[(v >> i) & 1 for v in defects] for i in range(12)])
        conditions = matrix(GF(2), rows)
        ranks.append(int(conditions.rank()))
    return conditions, ranks


def target_values(columns, kernel, place, field):
    """Return the values of s on the kernel basis and the multiplier gamma/dx."""
    x, y, *z = [from_bits(field, i) for i in place["representative"]]
    as_rhs, derivatives = as_values(x, y)
    require(all(root**2 + root == rhs for root, rhs in zip(z, as_rhs)),
            "invalid target representative")
    gamma = logarithmic_factor(x)
    require(gamma, "the reference differential must be nonzero at this place")
    monomials = as_monomials(z, derivatives)
    values = [base*monomials[mask][0] for mask, base, _ in coefficient_values(columns, x, y)]
    quotient_values = [sum((values[i] for i in row.nonzero_positions()), field.zero())
                       for row in kernel]
    return quotient_values, gamma


def compute():
    entries = json.loads(SUPPORT.read_text())["selected_allowed_ramification_places"]
    data = [(entry, local_coordinates(entry)) for entry in entries]
    fibres = {str(d): check_fibre(data, d, mask) for d, mask in [(6, 18), (8, 24)]}
    places = [e for e in entries if e["degree"] == 10]
    require(len(places) == 2 and all(e["GF_modulus_bits"] == 1033 for e in places),
            "unexpected pair of degree-ten places")
    first, second = (e["representative"] for e in places)
    require(first[:-1] == second[:-1] and first[-1] ^ second[-1] == 1,
            "expected the representatives to differ by the fifth AS translation")

    columns = coefficient_basis()
    conditions, ranks = cartier_matrix(columns)
    kernel = conditions.right_kernel().basis_matrix()
    require(ranks == [166, 316, 423, 508, 544, 567, 573, 575] and kernel.nrows() == 8,
            "unexpected rank of the necessary conditions")
    active = {columns[i] for v in kernel for i in v.nonzero_positions()}
    require(all(mask < 8 and y_power == 0 for mask, _, y_power, _ in active),
            "the kernel uses a coefficient or generator outside the first three AS coordinates")

    field = field_from_bits(1033, 10, "cartier_target")
    encoding = {from_bits(field, i): i for i in range(1024)}
    values_by_place = []
    for place in places:
        quotients, gamma = target_values(columns, kernel, place, field)
        values_by_place.append([encoding[gamma*v] for v in quotients])
    require(values_by_place[0] == values_by_place[1], "degree-ten jets disagree")
    evaluation_rank = xor_rank(values_by_place[0])
    require(evaluation_rank == 7, "unexpected degree-ten evaluation rank on the upper space")
    # The final M2 place checks injectivity of the joint evaluation. This
    # necessary kernel need not consist of logarithms of actual T-units.
    remaining, = [e for e in entries if e["degree"] == 12]
    residue = field_from_bits(remaining["GF_modulus_bits"], 12, "cartier_last")
    encode_last = {from_bits(residue, i): i for i in range(4096)}
    quotients, gamma_last = target_values(columns, kernel, remaining, residue)
    evaluation = matrix(GF(2), [[(v >> i) & 1 for v in values_by_place[0]] for i in range(10)])
    line, = evaluation.right_kernel().basis()
    quotient_last = sum((quotients[i] for i in line.nonzero_positions()), residue.zero())
    last_jet = gamma_last*quotient_last
    combined_rank = xor_rank(v | (encode_last[gamma_last*w] << 10)
                             for v, w in zip(values_by_place[0], quotients))
    require((encode_last[quotient_last], encode_last[last_jet], combined_rank) == (1173, 1043, 8),
            "joint evaluation must be injective on the necessary kernel")
    return {
        "sage_version": SAGE_VERSION,
        "support_sha256": sha256_file(SUPPORT),
        "complete_fibres": fibres,
        "reference_differential": "dlog((x+1)*(x^5+x^2+1))",
        "coefficient_space_dimension": len(columns),
        "auxiliary_modulus_bits": 4105,
        "auxiliary_H_points": AUXILIARY_POINTS,
        "translations_per_point": 32,
        "binary_rows": int(conditions.nrows()),
        "cumulative_ranks": ranks,
        "necessary_kernel_dimension": int(kernel.nrows()),
        "AS_monomial_masks_in_kernel": sorted({c[0] for c in active}),
        "base_y_powers_in_kernel": sorted({c[2] for c in active}),
        "target_place_ids": [e["id"] for e in places],
        "target_fibre_translation_mask": 16,
        "degree_ten_jets_by_place_on_kernel_basis": values_by_place,
        "degree_ten_evaluation_rank_on_necessary_kernel": evaluation_rank,
        "remaining_place": remaining["id"],
        "degree_twelve_quotient_value_on_degree_ten_kernel_line": encode_last[quotient_last],
        "degree_twelve_jet_on_degree_ten_kernel_line": encode_last[last_jet],
        "degree_ten_and_twelve_joint_evaluation_rank": combined_rank,
        "isolated_jet_dimensions": [0, 0],
        "inertia_orders_full_2_primary_ray_group": [1024, 1024],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the recomputed JSON")
    args = parser.parse_args()
    payload = json.dumps(compute(), indent=2)
    if args.emit:
        print(payload)
    else:
        require(json.loads(payload) == json.loads(RECEIPT.read_text()), "degree-ten receipt mismatch")
        print("PASS: rank 575 on 583 columns; all eight kernel vectors give equal degree-ten jets")
