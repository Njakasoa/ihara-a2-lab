"""Check the genus-334 degree-twelve computation by pointwise differentiation.

The column space and support use the proof's conventions. This checker tests
the differential equation at split auxiliary fibres without reducing any
polynomial identity in the 32-generator-monomial algebra.
"""

import json
from pathlib import Path

from sage.all import GF, PolynomialRing, matrix

from m3_ray_structure import field_from_bits, from_bits
from mxx_degree12_grouped import coefficient_space
from mxx_genus334_sage import require


ROOT = Path(__file__).resolve().parents[1]
POINTS = [(32, 2409), (32, 2304), (33, 1258), (33, 163),
          (105, 3563), (105, 72), (125, 3994)]


def contributions(columns, x, y, roots, shifts, differentiate):
    field = x.parent()
    p = PolynomialRing(field, "z", sparse=False)
    a, b = x**3+x+1, x**2+x
    d, q = x**4+x**3+x**2+x, b+1
    c = d*y+q
    require(a and b and c and y**2+a*y == b, "singular or invalid test chart")
    dy = ((x**2+1)*y+1)/a
    dc = (x**2+1)*y + d*dy + 1
    gamma = q**2/(a*b)
    dgamma = gamma*((x**2+1)/a+1/b)
    hs = [field.one(), x, x**2, x**3, y]
    dhs = [field.zero(), 1, 0, x**2, dy]
    rhs = [b*h/c**2 for h in hs]
    dw = [(h+b*dh)/c**2 for h, dh in zip(hs, dhs)]
    if roots is None:
        roots = []
        for f in rhs:
            solutions = (p.gen()**2+p.gen()+f).roots(multiplicities=False)
            require(len(solutions) == 2, "auxiliary point must split")
            roots.append(solutions[0])
    require(all(z*z+z == f for z, f in zip(roots, rhs)), "invalid AS coordinates")

    polys = {}
    for _, pair in columns:
        for code in pair:
            if code not in polys:
                poly = p([(code >> i) & 1 for i in range(code.bit_length())])
                polys[code] = poly(x), poly.derivative()(x)
    weights = []
    for mask, (p_code, q_code) in columns:
        exponent = 5-mask.bit_count()
        pp, dp = polys[p_code]
        qq, dq = polys[q_code]
        coeff = (pp+qq*y)/c**exponent
        dcoeff = (dp+dq*y+qq*dy)/c**exponent + (exponent % 2)*coeff*dc/c
        weights.append((mask, gamma*coeff, dgamma*coeff+gamma*dcoeff))

    rows = []
    for shift in shifts:
        mono = [(field.one(), field.zero())]
        for i, (w, zp) in enumerate(zip(roots, dw)):
            z = w+((shift >> i) & 1)
            mono += [(v*z, vp*z+v*zp) for v, vp in mono]
        values = []
        for mask, coeff, cp in weights:
            mon, mp = mono[mask]
            v = coeff*mon
            if differentiate:
                v = cp*mon+coeff*mp+v*v
            values.append(int(v.to_integer()))
        rows.extend([[(v >> j) & 1 for v in values] for j in range(field.degree())])
    return rows


def fibre_rows(columns, row, degree, modulus):
    field = field_from_bits(modulus, degree, f"check{degree}")
    x, y, *roots = [from_bits(field, v) for v in row["base_lift_bits"]]
    return contributions(columns, x, y, roots, row["selected_labels"], False)


def check():
    support = json.loads((ROOT/"results/mxx-degree12-support.json").read_text())
    regular = support["regular_fibres"]
    columns = coefficient_space()
    field = field_from_bits(4105, 12, "aux")
    rows, ranks = [], []
    for x, y in POINTS:
        rows.extend(contributions(columns, from_bits(field, x), from_bits(field, y),
                                  None, range(32), True))
        ranks.append(matrix(GF(2), rows).rank())
    require(ranks == [182, 343, 488, 584, 650, 686, 702], "auxiliary rank mismatch")
    kernel = matrix(GF(2), rows).right_kernel().basis_matrix()
    require(kernel.nrows() == 68, "a global solution must survive the auxiliary tests")
    target = matrix(GF(2), fibre_rows(columns, regular["12"], 12, 4105))
    grouped = fibre_rows(columns, regular["10"], 10, 1033)
    mixed = []
    for row in support["mixed_support_degree_ten_replacements"]:
        mixed.extend(fibre_rows(columns, row, 10, 1033))
    require(len(grouped) == len(mixed) == 120, "expected twelve degree-ten places")
    for selected, expected in [(grouped, 3400), (mixed, 2467)]:
        relative = (matrix(GF(2), selected)*kernel.transpose()).right_kernel().basis()
        require(len(relative) == 1, "expected a single possible jet direction")
        value = target*(relative[0]*kernel)
        require(sum(int(bit) << i for i, bit in enumerate(value)) == expected,
                "degree-twelve jet mismatch")
    print("PASS: pointwise Cartier ranks", list(map(int, ranks)),
          "and isolated jet candidates 3400 (grouped), 2467 (mixed)")


if __name__ == "__main__":
    check()
