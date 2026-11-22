"""Verify a degree-12 relation on the two-fibre degree-10 selection.

The quadratic witness is a principal element with even valuations outside
the splitting set, as required in the elementary ray quotient.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from sage.all import GF, FunctionField, PolynomialRing
from sage.env import SAGE_VERSION

from m3_ray_structure import field_from_bits, from_bits, to_bits
from mxx_degree12_support import compute as labelled_support, polynomial, translate
from mxx_genus334_sage import basis, characters_at_place, coefficient, require

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "mxx-degree12-quadratic-witness.json"


def witness_coefficients(x, y):
    """Return A,B in f=A+B*w_3, using little-endian binary polynomials."""
    A = (x*polynomial(245396, x)*y + polynomial(1305095, x))/polynomial(6809118, x)
    B = (polynomial(65, x)*y + polynomial(8085, x))/polynomial(8429, x)
    return A, B


def verify_function():
    base = FunctionField(GF(2), "x")
    x = base.gen()
    Y = PolynomialRing(base, "Y").gen()
    H = base.extension(Y**2 + (x**3+x+1)*Y + x**2+x, "y")
    x, y = H(x), H.gen()
    c = coefficient(x, y)
    rhs = [(x**2+x)*h/c**2 for h in basis(x,y)]
    A, B = witness_coefficients(x, y)
    deriv = H.derivation()
    # w_3^2+w_3=r and w_3'=r'. These two rational identities give f'=f^2.
    r = rhs[3]
    require(B and deriv(B) == B**2 and deriv(A) + A**2 == B*deriv(r) + B**2*r,
            "quadratic identity for the logarithmic differential failed")

    rational = H.places(1)
    zeros = sorted(c.zeros(), key=lambda place: place.degree())
    q4, = (x**2+x+1).zeros()
    require(len(rational) == 6 and [p.degree() for p in zeros] == [3,7]
            and q4.degree() == 4, "unexpected marked places on H")
    allowed = x.differential().divisor() - 2*q4.divisor()
    for p in rational:
        allowed += p
    ramified = zeros[0].divisor() + zeros[1].divisor()
    require((A.divisor() + allowed + 2*ramified).is_effective()
            and (B.divisor() + allowed + ramified).is_effective(),
            "pole containment or prescribed zeros on the degree-four fibre failed")
    local = []
    for place in zeros:
        ram, _ = characters_at_place(H, place, rhs)
        require(8 in ram, "the quadratic witness subfield must ramify at this place")
        quotient_order = 32
        unramified_characters = quotient_order - len(ram)
        e_k = quotient_order // unramified_characters
        # All ramified characters have conductor 2. The different exponent
        # at a completion of k/H is therefore 2(e_k-1).
        relative_index = e_k//2
        relative_different = 2*(e_k-1) - relative_index*2
        minimum_order = relative_different - relative_index  # pullback of a simple pole
        require(relative_index % 2 == 0 and minimum_order >= 2,
                "ramified pullback must have even valuation and vanishing jet")
        local.append({"base_place_degree": int(place.degree()), "relative_index": relative_index,
                      "relative_different": relative_different, "dlog_order_at_least": minimum_order})
    return local


def jets(degree, modulus, fibre):
    field = field_from_bits(modulus, degree, f"mixed{degree}")
    base_point = tuple(from_bits(field, n) for n in fibre["base_lift_bits"])
    values = []
    for label in fibre["selected_labels"]:
        x, y, *w = translate(base_point, label)
        A, B = witness_coefficients(x,y)
        z = w[3]
        require(z**2+z == (x**2+x)*x**3/coefficient(x,y)**2,
                "representative does not satisfy the selected AS equation")
        values.append(to_bits(A+B*z, degree))
    return {"degree": degree, "base_point_bits": fibre["base_lift_bits"][:2],
            "labels": fibre["selected_labels"], "jets": values}


def compute():
    local = verify_function()
    support = labelled_support()
    regular = support["regular_fibres"]
    rows = [jets(8, 283, regular["8"])]
    rows += [jets(10, 1033, f) for f in support["mixed_support_degree_ten_replacements"]]
    rows.append(jets(12, 4105, regular["12"]))
    require(len(rows[0]["jets"]) == 16 and len(rows[1]["jets"])+len(rows[2]["jets"]) == 12
            and not any(j for row in rows[:-1] for j in row["jets"])
            and rows[-1]["jets"] == [2467], "mixed-support witness is not isolated")
    require(support["degree_six"]["character_residue_and_exponent"] == [[4,2],[5,3]],
            "unexpected exponent-three branch")
    counts = {6:2, 8:16, 10:12, 12:1}
    mean = sum(2*f*n*(1-Fraction(1, 2**(f-int(f == 12)))) for f,n in counts.items())
    bound = Fraction(192)/(333+mean/2)
    require(bound == Fraction(32768,103115), "the one-direction conductor gain changed")
    return {"sage_version": SAGE_VERSION, "selected_support": "mixed_degree_ten",
            "quadratic_character_mask": 8, "witness": "f=A+B*w_3; dlog(f)=f*dx",
            "binary_polynomials": {"A": "(x*p245396*y+p1305095)/p6809118",
                                   "B": "(p65*y+p8085)/p8429"},
            "ramified_pullback": local, "degree_six_elementary_jets": [0,0],
            "regular_place_jets": rows, "degree_twelve_elementary_inertia_order_upper_bound": 2048,
            "mean_conductor_degree_upper_bound": str(mean), "tower_ratio_lower_bound": str(bound)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    result = compute()
    if parser.parse_args().emit:
        print(json.dumps(result, indent=2))
    else:
        require(result == json.loads(RECEIPT.read_text()), "quadratic witness receipt mismatch")
        print("PASS: mixed selection, isolated elementary degree-12 jet 2467, bound 32768/103115")
