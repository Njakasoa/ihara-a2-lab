"""Test degree-twelve isolation on one explicit support of Theorem 6.1.

Polynomial identities are evaluated on the basis y^e prod_{i in I}(c*w_i)
over F2[x]. Binary polynomial masks give exact coefficients at every degree.
Run with Sage's Python from the repository root.
"""

import argparse
import json
from fractions import Fraction
from pathlib import Path

from sage.all import GF, FunctionField, PolynomialRing, matrix
from sage.env import SAGE_VERSION

from m3_ray_structure import sha256_file
from mxx_degree12_support import compute as support_certificate, polynomial
from mxx_genus334_sage import basis, coefficient, require


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "mxx-degree12-grouped.json"
X, A, B, Q = 2, 11, 6, 7  # x, x^3+x+1, x^2+x, x^2+x+1
ONE = (1, 0)
ZERO = (0, 0)
C = (Q, 30)  # x^2+x+1 + (x^4+x^3+x^2+x)*y
H = [ONE, (X, 0), (4, 0), (8, 0), (0, 1)]


def pmul(p, q):
    result = 0
    while q:
        bit = q & -q
        result ^= p << (bit.bit_length() - 1)
        q ^= bit
    return result


def pder(p):
    return sum(1 << (i-1) for i in range(1, p.bit_length(), 2) if (p >> i) & 1)


def add(u, v):
    return u[0] ^ v[0], u[1] ^ v[1]


def mul(u, v):
    p, q = u
    r, s = v
    z = pmul(q, s)
    return pmul(p, r) ^ pmul(z, B), pmul(p, s) ^ pmul(q, r) ^ pmul(z, A)


def a_der(u):
    """a*d/dx on H, using a*y' = 1 + (x^2+1)*y."""
    p, q = u
    return pmul(A, pder(p)) ^ q, pmul(A, pder(q)) ^ pmul(5, q)


def coefficient_space():
    # At the infinity where y tends to zero, its t=1/x expansion satisfies
    # t^3*y^2 + (1+t^2+t^3)*y = t+t^2.
    series = []
    for n in range(36):
        value = int(n in (1, 2))
        if n >= 2:
            value ^= series[n-2]
        if n >= 3:
            value ^= series[n-3]
            if n % 2:
                value ^= series[(n-3)//2]
        series.append(value)
    columns = []
    for mask in range(32):
        m = 5 - mask.bit_count()
        for i in range(3*m+1):
            columns.append((mask, (1 << i, 0)))
        for i in range(7*m-2):
            # Cancel precisely the forbidden terms of x^i*y at this infinity.
            correction = sum(series[n] << (i-n) for n in range(i-3*m))
            columns.append((mask, (correction, 1 << i)))
    require(len(columns) == 770, "unexpected trace coefficient dimension")
    return columns


def kernel(columns):
    """Compute a relation basis among columns represented by binary integers."""
    pivots = {}
    relations = []
    for i, col in enumerate(columns):
        combination = 1 << i
        while col:
            pivot = col.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = col, combination
                break
            v, w = pivots[pivot]
            col ^= v
            combination ^= w
        if not col:
            relations.append(combination)
    return relations


def indexes(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def product_squares():
    """Coefficients of V_I^2, with V_i=c*w_i and V_i^2=c*V_i+b*h_i."""
    squares = [{0: ONE}]
    for i, h in enumerate(H):
        for item in squares[:]:
            out = {}
            for m, v in item.items():
                out[m] = mul(mul((B, 0), h), v)
                out[m | (1 << i)] = mul(C, v)
            squares.append(out)
    return squares


def symbolic_kernel(columns):
    # B_omega=N/D is the coefficient of dlog(u) on dx, D=a*b*c^5.
    denominator = (pmul(A, B), 0)
    for _ in range(5):
        denominator = mul(denominator, C)
    ac = mul((A, 0), C)
    j_denominator = mul(C, a_der(denominator))
    a_dc = a_der(C)
    a_dbh = [a_der(mul((B, 0), h)) for h in H]
    squares = product_squares()
    defects = []
    for mask, polynomial in columns:
        n = mul((pmul(Q, Q), 0), polynomial)
        # Multiply B_omega' + B_omega^2 by a*c*D^2.
        v = add(mul(denominator, mul(C, a_der(n))), mul(j_denominator, n))
        if mask.bit_count() % 2:
            v = add(v, mul(mul(denominator, n), a_dc))
        coefficients = {mask: v}
        for i in indexes(mask):
            coefficients[mask ^ (1 << i)] = mul(mul(denominator, n), a_dbh[i])
        common = mul(ac, mul(n, n))
        for j, square in squares[mask].items():
            coefficients[j] = add(coefficients.get(j, ZERO), mul(common, square))
        packed = 0
        for j, (p, q) in coefficients.items():
            require(max(p.bit_length(), q.bit_length()) <= 128, "overlapping polynomial blocks")
            packed |= (p | (q << 128)) << (256*j)
        defects.append(packed)
    return kernel(defects)


def evaluate_kernel(columns, subspace, degree, modulus, point, translations):
    ring = PolynomialRing(GF(2), "z")
    field = GF(2**degree, name="v", modulus=ring([(modulus >> i) & 1 for i in range(degree+1)]))
    x, y, *w = [field.from_integer(v) for v in point]
    a, b, q, c = x**3+x+1, x**2+x, x**2+x+1, coefficient(x,y)
    require(y**2+a*y == b and a*b*c, "invalid jet chart")
    require(all(z**2+z == b*h/c**2 for z, h in zip(w, basis(x,y))), "invalid AS point")
    base = [q**2*(polynomial(p,x)+y*polynomial(r,x))/(a*b*c**5)
            for _, (p,r) in columns]
    images = []
    for shift in translations:
        monomials = [field.one()]
        for i, z in enumerate(w):
            v = c*(z+((shift >> i) & 1))
            monomials += [m*v for m in monomials]
        values = [b0*monomials[m] for b0, (m, _) in zip(base, columns)]
        images.append([int(sum((values[i] for i in indexes(relation)), field.zero()).to_integer())
                       for relation in subspace])
    return [sum(row[i] << (degree*j) for j, row in enumerate(images)) for i in range(len(subspace))]


def grouped_ramification(terms):
    """Compute the norm of the survivor by a four-by-four determinant over H."""
    base = FunctionField(GF(2), "x")
    x = base.gen()
    Y = PolynomialRing(base, "Y").gen()
    field = base.extension(Y**2 + (x**3+x+1)*Y + x**2+x, "y")
    x, y = field(x), field.gen()
    a, b, q, c = x**3+x+1, x**2+x, x**2+x+1, coefficient(x,y)
    p3, p7 = sorted(c.zeros(), key=lambda p: p.degree())
    require((p3.degree(), p7.degree(), a.valuation(p3), c.valuation(p3), c.valuation(p7))
            == (3, 7, 2, 1, 1), "invalid polar divisor")
    require(sorted(c.valuation(p) for p in field.places_infinite()) == [-7,-3],
            "incorrect infinity bounds for the coefficient basis")
    require(len(q.zeros()) == 1 and q.zeros()[0].degree() == 4, "unexpected Q4")
    require(set(terms) == {0, 4, 16, 20}, "quartic survivor has unexpected generators")
    coordinates = [q**2*(polynomial(terms[m][0],x)+y*polynomial(terms[m][1],x))/(a*b*c**5)
                   for m in (0,4,16,20)]
    # Basis 1, V_2, V_4, V_2*V_4, with V_i^2=c*V_i+b*h_i.
    rows = []
    for unit_mask in range(4):
        row = [field.zero() for _ in range(4)]
        for m, value in enumerate(coordinates):
            expansion = {m ^ unit_mask: value}
            for i in indexes(m & unit_mask):
                expanded = {}
                for k, v in expansion.items():
                    expanded[k] = v*b*(x**2 if i == 0 else y)
                    expanded[k | (1 << i)] = v*c
                expansion = expanded
            for k, v in expansion.items():
                row[k] += v
        rows.append(row)
    norm = matrix(field, rows).determinant()
    require(norm and norm.valuation(p3) == -14, "valuation of the quartic norm at P3")
    geom = json.loads((ROOT / "certificates/mxx-theorem61.json").read_text())["geometry"]
    require(not {4, 16, 20}.intersection(geom["P3_unramified_nonzero_masks"]) and
            geom["ramification_index_and_residue_degree"] == {"3":[8,2], "7":[32,1]},
            "incorrect relative ramification in the quartic field")
    return {"quartic_character_masks": [4,16], "v_P3_norm_of_B": int(norm.valuation(p3)),
            "v_P7_norm_of_B": int(norm.valuation(p7)),
            "relative_e_and_different_k_over_quartic": {"P3":[2,2], "P7":[8,14]}}


def compute():
    support = support_certificate()
    support_path = ROOT / "results/mxx-degree12-support.json"
    require(support == json.loads(support_path.read_text()), "support receipt mismatch")
    degree8 = support["regular_fibres"]["8"]
    grouped = support["regular_fibres"]["10"]
    target = support["regular_fibres"]["12"]
    columns = coefficient_space()
    space = symbolic_kernel(columns)
    require(len(space) == 68, "unexpected symbolic kernel")
    images = evaluate_kernel(columns, space, 10, grouped["field_modulus_bits"],
                             grouped["base_lift_bits"], grouped["selected_labels"])
    relation, = kernel(images)
    survivor = 0
    for i in indexes(relation):
        survivor ^= space[i]
    terms = {}
    for i in indexes(survivor):
        m, p = columns[i]
        terms[m] = add(terms.get(m, ZERO), p)
    terms = {m:p for m,p in terms.items() if p != ZERO}
    local = grouped_ramification(terms)
    jets = evaluate_kernel(columns, [survivor], 12, target["field_modulus_bits"],
                           target["base_lift_bits"], target["selected_labels"])
    require(jets == [3400], "wrong degree-twelve jet")
    require(evaluate_kernel(columns, [survivor], 8, degree8["field_modulus_bits"],
                            degree8["base_lift_bits"], degree8["selected_labels"]) == [0],
            "the survivor must vanish at all sixteen degree-eight places")
    require(evaluate_kernel(columns, [survivor], 10, grouped["field_modulus_bits"],
                            grouped["base_lift_bits"], grouped["selected_labels"]) == [0],
            "the survivor must vanish at all twelve degree-ten places")
    labels = target["closed_place_labels"]
    packed, = evaluate_kernel(columns, [survivor], 12, target["field_modulus_bits"],
                              target["base_lift_bits"], labels)
    alternatives = {str(g):(packed >> (12*i)) & 4095 for i, g in enumerate(labels)}
    require(len(alternatives) == 16 and all(alternatives.values()),
            "every target above the cited degree-six base place must detect the same line")

    mixed, count = [0] * len(space), 0
    for row in support["mixed_support_degree_ten_replacements"]:
        new = evaluate_kernel(columns, space, 10, grouped["field_modulus_bits"],
                              row["base_lift_bits"], row["selected_labels"])
        mixed = [col | (other << (10*count)) for col, other in zip(mixed, new)]
        count += len(row["selected_labels"])
    require(count == 12 and len(kernel(mixed)) == 1, "mixed support rank changed")
    old = json.loads((ROOT / "certificates/mxx-theorem61.json").read_text())
    saving = Fraction(12, 2048) - Fraction(12, 4096)
    denominator = Fraction(old["genus_denominator_upper_bound"]) - saving
    new_bound = old["splitting_places"]/denominator
    require(new_bound == Fraction(32768,103115) and new_bound > Fraction(old["bound"]),
            "unexpected comparison to Theorem 6.1")
    return {"sage_version":SAGE_VERSION,
            "support_receipt_sha256":sha256_file(support_path),
            "theorem_6_1_baseline_sha256":sha256_file(ROOT / "certificates/mxx-theorem61.json"),
            "basis_size":len(columns), "rank_of_logarithmic_identity":len(columns)-len(space),
            "kernel_before_degree10":len(space), "kernel_after_grouped_degree10":1,
            "kernel_after_mixed_degree10":1, "grouped_degree10_labels":grouped["selected_labels"],
            "survivor_numerator_terms":{str(m):list(v) for m,v in sorted(terms.items())},
            "ramification":local, "grouped_degree12_jet":jets[0],
            "degree12_jets_for_alternative_labels_in_same_fibre":alternatives,
            "grouped_degree12_elementary_inertia_order":2048,
            "original_bound":old["bound"], "new_denominator_upper_bound":str(denominator),
            "new_mean_conductor_degree_upper_bound":str(2*(denominator-333)),
            "tower_ratio_lower_bound":str(new_bound)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    if parser.parse_args().emit:
        print(json.dumps(compute(), indent=2))
    else:
        require(compute() == json.loads(RECEIPT.read_text()), "grouped support receipt mismatch")
        print("PASS: symbolic Cartier calculation on the grouped genus-334 support")
