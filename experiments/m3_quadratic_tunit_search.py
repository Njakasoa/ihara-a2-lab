"""Search integral translates in the 31 quadratic subfields of k343/H.

Run with Sage Python to check the archived JSON receipt; --emit prints a fresh copy.
The finite search works on the M2 modulus, in the block order of m2-tower.json.
"""
import argparse
import json
from functools import lru_cache
from pathlib import Path

from sage.all import GF, PolynomialRing, matrix

from m3_ray_structure import (
    ALL_UNIT_NAMES, CERT_PATH, independent_rows, installed_sage_version,
    local_coordinates, require, sha256_file, to_bits, xor_rank,
)


R = PolynomialRing(GF(2), "x")
x = R.gen()
a, b, c = x**3+x+1, x*x+x, x**5+x*x+1


@lru_cache(maxsize=None)
def poly(bits):
    """Univariate polynomial, low bit = constant coefficient."""
    return R([(bits >> i) & 1 for i in range(bits.bit_length())])


@lru_cache(maxsize=31)
def subfield_rhs(mask):
    """Coefficients of h in the basis (1,y), using y²=a*y+b."""
    u = sum(((mask >> i) & 1) * x**i for i in range(3))
    return u + ((mask >> 4) & 1)*b, R((mask >> 3) & 1) + ((mask >> 4) & 1)*a


@lru_cache(maxsize=10000)
def split_exponents(norm):
    if not norm:
        return None
    i = int(norm.valuation())
    j = int(norm.degree()) - i
    return (i, j) if norm == x**i * (x+1)**j else None


def find_units(p_degree, q_degree):
    """Test g=A*c*w_h+P+Q*y by its iterated polynomial norm."""
    smooth = []
    for A_bits in (1, 2, 3, 6):
        A = poly(A_bits)
        for P_bits in range(1 << (p_degree+1)):
            P = poly(P_bits)
            for Q_bits in range(1 << (q_degree+1)):
                Q = poly(Q_bits)
                # N(g)=A² b h + A c (P+Qy) + (P+Qy)² in H.
                u0 = A*c*P + P*P + b*Q*Q
                u1 = A*c*Q + a*Q*Q
                for mask in range(1, 32):
                    h0, h1 = subfield_rhs(mask)
                    u, v = u0 + A*A*b*h0, u1 + A*A*b*h1
                    norm = u*u + a*u*v + b*v*v
                    exponents = split_exponents(norm)
                    if exponents is not None:
                        smooth.append((mask, A_bits, P_bits, Q_bits, *exponents))
    return smooth


def place_jet(entry, data, recipes):
    """Return dlog(g) for each certificate in the chosen uniformizer."""
    degree = int(entry["degree"])
    if entry["chart"] == "ramified":
        # e(k/H)=32, hence e(k/H(w_h))>=16. Pullback of every local
        # subfield unit has no linear term (the residue fields are finite).
        return [0] * len(recipes)
    F = data["field"]
    X, Y, *W = data["point"]
    aa, bb, cc = X**3+X+1, X*X+X, X**5+X*X+1
    dx, dy = ((F(1), ((X*X+1)*Y+1)/aa) if aa else (F(0), F(1)))
    db, dc = dx, X**4 * dx
    hs, dhs = (F(1), X, X*X, Y, Y*Y), (F(0), dx, F(0), dy, F(0))
    integral_generators = {}
    for mask in {unit[0] for unit in recipes}:
        indices = [i for i in range(5) if mask & (1 << i)]
        h = sum(hs[i] for i in indices)
        dh = sum(dhs[i] for i in indices)
        v = cc * sum(W[i] for i in indices)
        require(v*v+cc*v == bb*h, "quadratic equation failed")
        integral_generators[mask] = v, (db*h+bb*dh+dc*v)/cc
    evaluations = {}
    for bits in {k for recipe in recipes for k in recipe[1:4]}:
        f = poly(bits)
        evaluations[bits] = F(f(X)), F(f.derivative()(X))*dx
    block = []
    for mask, A_bits, P_bits, Q_bits, i, j in recipes:
        A, dA = evaluations[A_bits]
        P, dP = evaluations[P_bits]
        Q, dQ = evaluations[Q_bits]
        v, dv = integral_generators[mask]
        g = A*v + P + Q*Y
        require(g != 0, "norm-certified unit vanishes at a selected place")
        dg = dA*v + A*dv + dP + dQ*Y + Q*dy
        block.append(to_bits(dg/g, degree))
    return block


def check_basis_norms(recipes):
    """Independently take the determinant of multiplication on 1,y,v,yv."""
    F = R.fraction_field()
    I = matrix.identity(F, 2)
    Y = matrix(F, [[0,b],[1,a]])
    for mask, aa, pp, qq, i, j in recipes:
        h0, h1 = subfield_rhs(mask)
        A = poly(aa)
        B = poly(pp)*I + poly(qq)*Y
        H = h0*I + h1*Y
        left = B.stack(A*I)
        right = (A*b*H).stack(B + A*c*I)
        require(left.augment(right).det() == x**i*(x+1)**j, "basis norm determinant failed")


def check_degree_six_fiber(entries, packed, blocks):
    """Lift 16 orbits to deck group F2^5 and check affine functions on all 32 points."""
    six = [(e, start) for e, (_, start, d) in zip(entries, blocks) if d == 6]
    ref, _ = six[0]
    F = local_coordinates(ref)["field"]
    lift = lambda u: F.from_integer(int(u))
    def coordinates(w):
        require(all(z in (0,1) for z in w), "not a deck translation")
        return sum(int(z) << i for i,z in enumerate(w))
    W = [lift(k) for k in ref["representative"][2:]]
    frob = coordinates([z**8+z for z in W])
    require(frob != 0, "no residue degree two extension")
    locations = []
    for e, start in six:
        require(e["representative"][:2] == ref["representative"][:2] and
                e["GF_modulus_bits"] == ref["GF_modulus_bits"], "unaligned base point")
        g = coordinates([lift(k)+z for k,z in zip(e["representative"][2:], W)])
        locations.append((start,g))
    for row in packed:
        fiber = {}
        for start, g in locations:
            j = (row >> start) & 63
            fiber[g] = j
            fiber[g ^ frob] = to_bits(lift(j)**8, 6)
        require(len(fiber) == 32, "closed places do not partition the geometric fiber")
        for g in range(32):
            predicted = fiber[0]
            for i in range(5):
                if g & (1 << i):
                    predicted ^= fiber[1 << i] ^ fiber[0]
            require(predicted == fiber[g], "quadratic-unit fiber failed the affine test")
    return frob


def run(p_degree, q_degree):
    recipes = find_units(p_degree, q_degree)
    entries = json.loads(CERT_PATH.read_text())["selected_allowed_ramification_places"]
    known = {name: 0 for name in ALL_UNIT_NAMES}
    packed = [0] * len(recipes)
    blocks = []
    offset = 0
    for entry in entries:
        data = local_coordinates(entry)
        degree = int(entry["degree"])
        for name in known:
            known[name] |= to_bits(data["coordinates"][name], degree) << offset
        for i, jet in enumerate(place_jet(entry, data, recipes)):
            packed[i] |= jet << offset
        blocks.append((entry["id"], offset, degree))
        offset += degree
    rows, basis_labels = independent_rows(list(known.items()) + list(enumerate(packed)))
    rank = len(rows)
    require(xor_rank(known.values()) == 5 and len(entries) == 37 and offset == 266,
            "incompatible baseline or place inventory")
    fresh = [i for i in basis_labels if isinstance(i,int)]
    check_basis_norms([recipes[i] for i in fresh])
    frob = check_degree_six_fiber(entries, rows, blocks)
    sage_matrix = matrix(GF(2), [[(r >> i) & 1 for i in range(offset)]
                                 for r in list(known.values()) + packed])
    require(sage_matrix.rank() == rank, "Sage matrix rank differs from the XOR elimination")
    all_bits = (1 << offset)-1
    intersections = {}
    for label, start, degree in blocks:
        outside = all_bits ^ (((1 << degree)-1) << start)
        intersections[label] = rank - xor_rank(v & outside for v in rows)
    return {
        "sage_version": installed_sage_version(),
        "place_inventory_sha256": sha256_file(CERT_PATH),
        "field": "M2 genus 343, modulus 2 at the 37 selected places",
        "family": "g=A*c*w_h+P+Q*y; h=sum of mask bits times (1,x,x²,y,y²)",
        "polynomial_encoding": "bit i is coefficient of x^i over F2",
        "A_masks": [1,2,3,6], "max_degree_P": p_degree, "max_degree_Q": q_degree,
        "tested": 31*4*(1 << (p_degree+q_degree+2)),
        "unit_count": len(recipes), "known_rank": 5, "certified_rank": rank,
        "ambient_dimension": offset, "basis": basis_labels,
        "independent_checks": {"sage_binary_matrix_rank": rank,
                               "regular_representation_norms_on_new_basis": len(fresh),
                               "degree_six_geometric_affinity_checked_on_basis": rank,
                               "degree_six_frobenius_cubed_deck_mask": frob},
        "certificate_columns": ["mask_h","A_bits","P_bits","Q_bits",
                                "x_exponent_in_norm","x_plus_one_exponent_in_norm"],
        "certificates": [list(r) for r in recipes],
        "basis_new_rows_hex": {str(i): hex(packed[i]) for i in basis_labels if isinstance(i,int)},
        "block_intersection_dimensions": intersections,
        "scope": "Subspace of the global relation image. Each g is integral at finite places, with absolute norm x^i*(x+1)^j; zeros/poles lie only over 0,1,infinity.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    archived = CERT_PATH.parents[1]/"results"/"m3-quadratic-tunit-search.json"
    mode.add_argument("--check", nargs="?", type=Path, const=archived, metavar="RECEIPT",
                      help="verify the full receipt (default: the archived M3 result)")
    mode.add_argument("--emit", action="store_true", help="write the full JSON to stdout")
    parser.add_argument("--p-degree", type=int, default=4)
    parser.add_argument("--q-degree", type=int, default=2)
    args = parser.parse_args()
    if min(args.p_degree, args.q_degree) < 0:
        parser.error("degrees must be nonnegative")
    report = run(args.p_degree, args.q_degree)
    if args.emit:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        path = args.check or archived
        expected = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(expected, dict), "receipt is not a JSON object")
        differences = sorted(k for k in expected.keys() | report.keys()
                             if k not in expected or k not in report or expected[k] != report[k])
        require(not differences, f"receipt mismatch in {', '.join(differences)}")
        block_count = len(report["block_intersection_dimensions"])
        print(f"PASS: {report['tested']} recipes, {report['unit_count']} norm certificates, "
              f"binary rank {report['certified_rank']}, {block_count} block intersections checked.")
