"""Verify the degree-twelve logarithmic differential and the odd class number.

The accompanying proof turns this differential into that of a T-unit
using an odd-order affine class group. The program computes the identity,
the jets and the Jacobian order without constructing the correcting square.
"""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

from sage.all import GF, PolynomialRing
from sage.env import SAGE_VERSION

from m3_degree6_norm_obstruction import SUPPORT, ramified_norm_test
from m3_ray_structure import local_coordinates, require, sha256_file, to_bits, xor_rank

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "m3-degree12-unit.json"
CARTIER_RECEIPT = ROOT / "results" / "m3-degree10-cartier.json"
sys.path.insert(0, str(ROOT / "src"))
from exact_curves import zeta_numerator
from zeta_cover import points_from_zeta, poly_product


def candidate_coefficients(x):
    """s=A+L*U+M*V+U*V with U=xi_1+xi_(x^2) and V=xi_x."""
    c = x**5 + x**2 + 1
    q = x**2 + x + 1
    numerator = sum(x**i for i in range(13) if (7487 >> i) & 1)
    return numerator/(x*c**2), q/(x*c), x*q/c


def gamma_coefficient(x):
    return (x**4 + x**2 + 1)/((x+1)*(x**5+x**2+1))


def symbolic_identity():
    """Check (g*s)'=(g*s)^2 on 1,U,V,UV over F2(x)."""
    rational = PolynomialRing(GF(2), "x").fraction_field()
    x = rational.gen()
    a, left, right = candidate_coefficients(x)
    c = x**5+x**2+1
    b = x**2+x
    f_u, f_v = b*(1+x**2)/c**2, b*x/c**2
    g = gamma_coefficient(x)
    require(g == ((x+1)*c).derivative()/((x+1)*c) and g.derivative() == g**2,
            "invalid logarithmic reference")
    # U^2=U+f_u, V^2=V+f_v, so U'=f_u', V'=f_v'.
    du, dv = f_u.derivative(), f_v.derivative()
    d_s = [a.derivative() + left*du + right*dv, left.derivative()+dv,
           right.derivative()+du, rational.zero()]
    s_plus_square = [a + a**2 + left**2*f_u + right**2*f_v + f_u*f_v,
                     left + left**2 + f_v, right + right**2 + f_u, rational.zero()]
    require(all(d == g*v for d, v in zip(d_s, s_plus_square)),
            "the quartic logarithmic identity is not identically zero")


def point_counts(n):
    """Direct counts on the degree-eight cover and its seven quadratic quotients."""
    field = GF(2**n, name="z")
    full = 8   # all points over infinity split
    quadratic = [2]*7
    for x in field:
        c = x**5+x**2+1
        if c == 0:
            full += 1
            quadratic = [v+1 for v in quadratic]
            continue
        scale = (x**2+x)/c**2
        mask = sum(int((scale*v).trace()) << i
                   for i, v in enumerate([field.one(), x, x**2]))
        if mask == 0:
            full += 8
        for h in range(1, 8):
            if (mask & h).bit_count() % 2 == 0:
                quadratic[h-1] += 2
    return full, quadratic


def class_number():
    counts = [point_counts(n) for n in range(1, 11)]
    numerator = [1]
    factors = []
    for i in range(7):
        ns = [quadratic[i] for _, quadratic in counts]
        factor = zeta_numerator(ns[:8], genus=4)
        require(points_from_zeta(factor, 10) == ns, "quadratic held-out counts disagree")
        numerator = poly_product(numerator, factor)
        factors.append(factor)
    require(len(numerator) == 57 and points_from_zeta(numerator, 10) == [v for v, _ in counts],
            "direct degree-eight counts disagree with the seven-factor zeta")
    ring = PolynomialRing(GF(2), "t")
    t = ring.gen()
    require(ring(numerator) == (1+t+t**2+t**3+t**4)**7 and sum(numerator) % 2 == 1,
            "the arithmetic class number must be odd")
    return {"genus": 28, "quadratic_zeta_factors": factors,
            "full_zeta_numerator": numerator, "direct_point_counts_degrees_1_to_10": [v for v, _ in counts],
            "jacobian_order": sum(numerator), "mod_two_factor": "(1+t+t^2+t^3+t^4)^7"}


def exact_tower(inventory, isolated_jets):
    """Apply the depth-two conductor average to all proven inertia orders."""
    degrees = {row["id"]: row["degree"] for row in inventory["selected_allowed_ramification_places"]}
    modulus = inventory["modulus"]
    require(len(modulus) == len(degrees) == 37
            and all(p["exponent"] == 2 and degrees[p["place_id"]] == p["degree"] for p in modulus)
            and {p["place_id"] for p in modulus} == set(degrees), "unexpected fixed M2 modulus")
    counts = Counter(degrees.values())
    require(counts == {5: 2, 6: 16, 8: 16, 10: 2, 12: 1}, "unexpected support multiplicities")
    prior_receipts = ["m3-degree5-norm-obstruction", "m3-degree6-norm-obstruction",
                      "m3-degree8-norm-obstruction", "m3-degree8-quartic-norm", "m3-degree10-cartier"]
    # The proofs for degrees 5, 6, 8, 10 exclude an isolated jet at each
    # such place. Their finite inputs are bound below. In degree 12 the
    # necessary line in the Cartier receipt is attained by this witness.
    hashes = {name: sha256_file(ROOT / "results" / (name+".json")) for name in prior_receipts}
    orders = {p: 2**(d - int(p in isolated_jets)) for p, d in degrees.items()}
    contributions = {d: sum(2*d*(1-Fraction(1, orders[p])) for p in degrees if degrees[p] == d)
                     for d in sorted(counts)}
    mean = sum(contributions.values())
    split = len(inventory["selected_splitting_places"])
    denominator = inventory["genus"] - 1 + mean/2
    score = split/denominator
    dimension = sum(degrees.values())
    generators = dimension - split + 1
    twice_cost = sum(d*(d+1) for d in degrees.values())
    margin = generators**2 - 4*generators - 2*twice_cost - 4*(split-1)
    require((mean, score) == (Fraction(134995, 256), Fraction(98304, 310099)), "unexpected exact ratio")
    require(margin == inventory["tower_infinitude_inequality"]["integer_margin"] == 41,
            "the fixed M2 infinitude criterion must hold")
    return {"prior_receipt_sha256": hashes, "inertia_orders_by_place": orders,
            "mean_conductor_contributions_by_degree": {str(d): str(v) for d, v in contributions.items()},
            "exact_mean_conductor_degree": str(mean), "normalized_genus_denominator": str(denominator),
            "split_rational_places": split, "generator_lower_bound": generators,
            "twice_local_relation_cost": twice_cost, "tower_criterion_integer_margin": margin,
            "Ihara_ratio_lower_bound_from_this_tower": str(score)}


def compute():
    symbolic_identity()
    bound = json.loads(CARTIER_RECEIPT.read_text())
    require(bound["support_sha256"] == sha256_file(SUPPORT)
            and bound["necessary_kernel_dimension"] - bound["degree_ten_evaluation_rank_on_necessary_kernel"] == 1,
            "the independent Cartier certificate must bound the isolated line")
    inventory = json.loads(SUPPORT.read_text())
    entries = inventory["selected_allowed_ramification_places"]
    jets, ramified_poles = {}, []
    for entry in entries:
        degree = entry["degree"]
        data = local_coordinates(entry)
        if entry["chart"] == "ramified":
            # The quartic logarithmic form is at worst simply polar. Pullback
            # to the degree-eight field has order >=0 (e=2,different=2);
            # then pullback to k has order >=6 (e=4,different=6).
            poles = ramified_norm_test(entry)["reduced_poles"][:3]
            require(degree == 5 and xor_rank(poles) == 3, "wrong rank at the ramified prime")
            ramified_poles.append(poles)
            jet = 0
        else:
            x, y, *z = data["point"]
            a, left, right = candidate_coefficients(x)
            u, v = z[0]+z[2], z[1]
            s = a + left*u + right*v + u*v
            coefficient = s*gamma_coefficient(x)
            if degree == 6:
                # y-y(P) is the parameter, and dx/dy=a/((x^2+1)y+1).
                dx_dy = (x**3+x+1)/((x**2+1)*y+1)
                require(not dx_dy, "unexpected degree-six tangent")
                coefficient *= dx_dy
            jet = to_bits(coefficient, degree)
        jets[entry["id"]] = jet
    nonzero = {place: jet for place, jet in jets.items() if jet}
    require(len(jets) == 37 and nonzero == {"k343-d12-001": 1043},
            "the proposed differential must be supported on the single degree-twelve block")
    require(nonzero == {bound["remaining_place"]: bound["degree_twelve_jet_on_degree_ten_kernel_line"]},
            "the constructed jet must attain the necessary line")
    require(len(ramified_poles) == 2, "expected two degree-five places on k")
    return {
        "sage_version": SAGE_VERSION, "support_sha256": sha256_file(SUPPORT),
        "degree_ten_cartier_receipt_sha256": sha256_file(CARTIER_RECEIPT),
        "quartic_AS_character_masks": [5, 2],
        "A_numerator_binary_mask": 7487,
        "coefficients_of_B_prime_plus_B_squared_on_quartic_basis": [0, 0, 0, 0],
        "reduced_AS_poles_for_the_three_rational_generators": ramified_poles,
        "degree_eight_correction_field": class_number(),
        "jets_on_all_37_places": jets,
        "isolated_jet_dimension": 1,
        "inertia_order_full_2_primary_ray_group": 2048,
        "exact_full_ray_tower": exact_tower(inventory, nonzero),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the recomputed JSON")
    args = parser.parse_args()
    payload = compute()
    if args.emit:
        print(json.dumps(payload, indent=2))
    else:
        require(payload == json.loads(RECEIPT.read_text()), "degree-twelve receipt mismatch")
        print("PASS: quartic identity, odd class number, 36 zero jets and one jet of value 1043;"
              " all 37 inertia orders, mean 134995/256, tower margin 41, ratio 98304/310099")
