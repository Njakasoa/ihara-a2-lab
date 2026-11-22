"""Search for T-units in the degree-16 subfield fixed by degree-six Frobenius.

Run under Sage 10.9 with sage -python experiments/m3_degree6_descent.py.
Use --emit to print the deterministic receipt. The search is finite: even
a zero result does not compute the T-unit group of the subfield.
"""

import argparse
import itertools
import json
from pathlib import Path

from sage.all import GF, PolynomialRing
from sage.env import SAGE_VERSION

from m3_ray_structure import h_basis, local_coordinates, require, to_bits, xor_rank


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results/m3-degree6-descent.json"


def lin(mask, basis):
    return sum((v for i, v in enumerate(basis) if mask & (1 << i)), basis[0] * 0)


def low_degree_basis(x, y):
    return [x**0, x, x**2, x**3, x**4, y, x*y, x**2*y]


def fixed_field(local_data):
    """Identify one H-place of degree 3 and its 16 lifts from the actual points."""
    frobenius_masks = set()
    orbit_labels = []
    for entry, data in local_data:
        if entry["degree"] != 6:
            continue
        x, y, *w = data["point"]
        require(x**8 == x and x**2 != x and y**8 == y, "H-place must have degree 3")
        translations = [z**8 + z for z in w]
        require(all(t**2 == t for t in translations), "third Frobenius is not a translation")
        shift = sum(int(t) << i for i, t in enumerate(translations))
        frobenius_masks.add(shift)
        # Pick the same geometric H-point for every lift, and compare F64
        # bit coordinates rather than parents with different Sage names.
        coords = tuple(data["point"])
        conjugates = []
        for _ in range(6):
            conjugates.append(tuple(to_bits(v, 6) for v in coords))
            coords = tuple(v*v for v in coords)
        orbit_labels.append(min(conjugates))
    require(len(orbit_labels) == 16 and len(set(orbit_labels)) == 16, "lost a lift")
    require(len({row[:2] for row in orbit_labels}) == 1, "different underlying H-points")
    require(len(frobenius_masks) == 1, "Frobenius is not constant over the orbit")
    shift, = frobenius_masks
    require(shift != 0, "inert extension must have a nonzero translation")
    annihilator = [h for h in range(1, 32) if (h & shift).bit_count() % 2 == 0]
    basis = []
    for h in annihilator:
        if xor_rank(basis + [h]) > len(basis):
            basis.append(h)
    require(len(basis) == 4, "fixed field must have four independent AS characters")
    labels = []
    origin = orbit_labels[0][2:]
    for row in orbit_labels:
        delta = [a ^ b for a, b in zip(row[2:], origin)]
        require(set(delta) <= {0, 1}, "lift coordinates must differ by binary translations")
        mask = sum(v << i for i, v in enumerate(delta))
        labels.append(sum(((mask & h).bit_count() % 2) << i for i, h in enumerate(basis)))
    require(sorted(labels) == list(range(16)), "lifts are not a regular translation orbit")
    paired_rows = {((1 << x) | (1 << (x ^ t))) for t in range(1, 16) for x in range(16)}
    require(xor_rank(paired_rows) == 15, "proper-subfield functions should span the even code")
    return shift, basis, labels


def check_norm_by_multiplication(A, coefficients, characters, b, c, expected):
    """Multiply all 16 conjugates in the algebra with square-free monomials."""
    product = {0: A.parent().one()}
    for shift in range(16):
        translated_constant = A + c*lin(shift, coefficients)
        new = {}
        for mask, coefficient in product.items():
            new[mask] = new.get(mask, 0) + coefficient*translated_constant
            for i, l in enumerate(coefficients):
                bit = 1 << i
                term = coefficient*l
                if mask & bit:
                    new[mask] = new.get(mask, 0) + c*term
                    new[mask ^ bit] = new.get(mask ^ bit, 0) + b*characters[i]*term
                else:
                    new[mask | bit] = new.get(mask | bit, 0) + term
        product = {m: v for m, v in new.items() if v}
    require(product == {0: expected}, "product over the 16 conjugates disagrees with norm")


def norm_search(fixed_basis):
    """For z_h=c*w_h, Norm over translations tests u=A+sum l_i*z_hi.

    If the shift currently acts by adding delta, its two conjugates have
    product u²+delta*u. Each z_h²=c*z_h+b*h eliminates a square. Since
    A is fixed by every translation, its contribution is additive.
    """
    S = PolynomialRing(GF(2), "x")
    x0 = S.gen()
    a, b, c = x0**3 + x0 + 1, x0**2 + x0, x0**5 + x0**2 + 1
    SY = PolynomialRing(S, "Y")
    Y = SY.gen()
    R = SY.quotient(Y**2 + a*Y + b, "y")
    x, y = R(x0), R.gen()
    base_coeffs = [R.one(), x, x*x, y]
    A_basis = low_degree_basis(x, y)
    character_values = [lin(h, h_basis(x, y)) for h in range(32)]
    eligible = [h for h in range(1, 32) if xor_rank(fixed_basis + [h]) == 4]

    coeffs = list(base_coeffs)
    additive_images = list(A_basis)
    # Scalars independent of h. Accumulate the constant contribution of
    # each input b*h, allowing all ordered bases to share these operations.
    contributions = [[R.zero() for _ in range(32)] for _ in range(4)]
    for i in range(4):
        delta = coeffs[i]*c
        require(bool(delta), "candidate stabilizer is larger than the fixed involution")
        additive_images = [v*v + delta*v for v in additive_images]
        for j, coeff in enumerate(coeffs):
            sq = coeff*coeff
            contributions[j] = [v*v + delta*v + sq*b*h
                                for v, h in zip(contributions[j], character_values)]
        coeffs = [v*v*c + delta*v for v in coeffs]
    require(all(v == 0 for v in coeffs), "norm must descend to H")

    sample_A = 38
    sample = sum((row[h] for row,h in zip(contributions, fixed_basis)), R.zero())
    check_norm_by_multiplication(
        lin(sample_A, A_basis), base_coeffs, [character_values[h] for h in fixed_basis],
        b, c, sample + lin(sample_A, additive_images))

    # Q(e+fy)=e²+a*e*f+b*f² is a quadratic form over F2. Its polar
    # form is a*(e*v+f*u). Pack a polynomial as its coefficient bits, so
    # every addition of precomputed norms/polar terms is an exact XOR.
    def pack_polynomial(p):
        return sum(int(v) << i for i, v in enumerate(p.list()))

    def Q(u):
        e, f = u.lift()[0], u.lift()[1]
        return pack_polynomial(e*e + a*e*f + b*f*f)

    def polar(u,v):
        e, f = u.lift()[0], u.lift()[1]
        g, h = v.lift()[0], v.lift()[1]
        return pack_polynomial(a*(e*h + f*g))

    constants = [lin(mask, additive_images) for mask in range(1 << len(A_basis))]
    const_norms = [Q(v) for v in constants]
    individual = {(i,h): Q(row[h]) for i,row in enumerate(contributions) for h in eligible}
    pairs = {(i,h,j,k): polar(contributions[i][h], contributions[j][k])
             for i,j in itertools.combinations(range(4),2) for h in eligible for k in eligible}
    linear = {(i,h): [polar(contributions[i][h], u) for u in additive_images]
              for i in range(4) for h in eligible}
    # Products for the terms appearing in Q cover every possible degree;
    # higher terms cannot arise when these terms are added in characteristic 2.
    max_bits = max(n.bit_length() for n in
                   itertools.chain(const_norms, individual.values(), pairs.values(),
                                   itertools.chain.from_iterable(linear.values())))
    smooth = {pack_polynomial(x0**i*(x0+1)**(d-i)): (i,d-i)
              for d in range(max_bits) for i in range(d+1)}
    expected_sample = pack_polynomial((sample+constants[sample_A]).lift().resultant(Y**2+a*Y+b))
    require(Q(sample + constants[sample_A]) == expected_sample,
            "quadratic norm disagrees with the independent resultant")
    units = []
    count = 0
    for basis in itertools.permutations(eligible, 4):
        if xor_rank(basis) != 4:
            continue
        count += 1
        norm0 = 0
        cross_basis = [0]*len(A_basis)
        for i,h in enumerate(basis):
            norm0 ^= individual[i,h]
            for j in range(i):
                norm0 ^= pairs[j,basis[j],i,h]
            cross_basis = [x ^ y for x,y in zip(cross_basis, linear[i,h])]
        cross = [0]
        for v in cross_basis:
            cross += [w ^ v for w in cross]
        if basis == tuple(fixed_basis):
            require(norm0 ^ const_norms[sample_A] ^ cross[sample_A] == expected_sample,
                    "packed search disagrees with independent norm")
        for mask, (qv, cv) in enumerate(zip(const_norms,cross)):
            norm = norm0 ^ qv ^ cv
            require(bool(norm), "candidate vanished identically")
            if norm in smooth:
                i, j = smooth[norm]
                units.append({"characters": list(basis), "A_mask": mask,
                              "norm_x_valuation": i, "norm_x_plus_one_valuation": j})
    require(count == 15*14*12*8, "expected all ordered bases of the four-dimensional space")
    return count, len(constants), units


def local_unit_jets(entry, data, unit):
    """All Galois translates of one certified unit in the selected local chart."""
    f = entry["degree"]
    if entry["chart"] == "ramified":
        # k/K_fixed is ramified at P_5 (k/H is totally ramified).
        # A regular unit pulled back with e=2 has zero linear coefficient.
        return [0] * 16
    x, y, *w = data["point"]
    F = data["field"]
    a, b, c = x**3+x+1, x**2+x, x**5+x**2+1
    if a:
        dx, dy = F.one(), ((x*x+1)*y+1)/a
    else:
        dx, dy = F.zero(), F.one()
    basis = h_basis(x, y)
    basis_d = [F.zero(), dx, F.zero(), dy, F.zero()]
    A = lin(unit["A_mask"], low_degree_basis(x, y))
    dA = lin(unit["A_mask"], [F.zero(), dx, F.zero(), x*x*dx, F.zero(),
                              dy, x*dy+y*dx, x*x*dy])
    coefficients = [F.one(), x, x*x, y]
    derivatives = [F.zero(), dx, F.zero(), dy]
    result = []
    for trans in range(16):
        u, du = A, dA
        for i, h in enumerate(unit["characters"]):
            wh = lin(h, w) + ((trans >> i) & 1)
            z = c*wh
            dz = x**4*dx*wh + (dx*lin(h, basis)+b*lin(h, basis_d))/c
            u += coefficients[i]*z
            du += coefficients[i]*dz + derivatives[i]*z
        require(bool(u), "norm-certified unit vanished at a selected place")
        result.append(to_bits(du/u, f))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the deterministic receipt")
    args = parser.parse_args()
    cert = json.loads((ROOT / "certificates/m2-tower.json").read_text())
    entries = cert["selected_allowed_ramification_places"]
    local_data = [(entry, local_coordinates(entry)) for entry in entries]
    shift, basis, labels = fixed_field(local_data)
    n_bases, n_A, units = norm_search(basis)
    rows, offset = [], 0
    block_ranges = []
    for entry, data in local_data:
        f = entry["degree"]
        blocks = [to_bits(data["coordinates"][name], f) for name in ("x", "x+1", "y", "y+1", "y+x")]
        for unit in units:
            blocks.extend(local_unit_jets(entry, data, unit))
        if not rows:
            rows = [0] * len(blocks)
        for i, v in enumerate(blocks):
            rows[i] |= int(v) << offset
        block_ranges.append((entry, ((1 << f)-1) << offset))
        offset += f
    rank = xor_rank(rows)
    isolated = {entry["id"]: rank - xor_rank([v & ~block for v in rows])
                for entry, block in block_ranges if entry["degree"] == 6}
    receipt = {
        "sage_version": SAGE_VERSION,
        "fixed_field": {"degree_over_H": 16, "degree6_frobenius_mask": shift,
                        "annihilating_character_basis": basis, "degree6_orbit_labels": labels,
                        "pair_indicator_binary_rank": 15,
                        "proper_subfields": "Their dlog vectors on the 16 aligned lifts to the fixed field sum to zero in F8: translation by a nonzero involution pairs equal entries. This also holds for products from any of these proper subfields."},
        "search": {"shape": "A + sum l_i*c*w_{h_i}, l=(1,x,x^2,y)",
                   "A_basis": ["1","x","x^2","x^3","x^4","y","xy","x^2y"],
                   "ordered_character_bases": n_bases, "A_count": n_A,
                   "tested": n_bases*n_A, "certified_T_units": units,
                   "independent_control": "One full-degree candidate checked by multiplication of 16 conjugates, then by a polynomial resultant.",
                   "criterion": "Integral at all finite places; norm to F2(x) has support in x,x+1. Every point over 0,1,infinity is in T."},
        "local_jets": {"full_rank_including_five_base_units": rank,
                       "single_block_dimensions_degree6": isolated},
        "scope": "The degree-16 primitive search is bounded. Only the cancellation for proper subfields of this fixed field is universal."
    }
    if args.emit:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        require(json.loads(RECEIPT.read_text()) == receipt, "descent receipt mismatch")
        print(f"PASS: {n_bases*n_A} full-degree norm tests; {len(units)} T-units")


if __name__ == "__main__":
    main()
