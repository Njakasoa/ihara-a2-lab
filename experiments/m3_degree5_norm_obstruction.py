"""Verify the 31 quadratic norm constraints at both degree-five places of k343.

Run with Sage Python. The default compares the recomputation with the archived
JSON; --emit writes the receipt to stdout.
"""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from sage.all import PolynomialRing, prod
from sage.env import SAGE_VERSION

from m3_degree6_norm_obstruction import SUPPORT, check_fibre, ramified_norm_test
from m3_ray_structure import field_from_bits, from_bits, local_coordinates, require, to_bits, xor_rank

RECEIPT = Path(__file__).resolve().parents[1] / "results" / "m3-degree5-norm-obstruction.json"


def reduced_poles_and_constants(entry, field):
    """Compute terms through z^0 after subtracting the AS double pole."""
    alpha, beta = (from_bits(field, v) for v in entry["representative"])
    R = PolynomialRing(field, "z")
    z = R.gen()
    X = alpha+z
    a, b, c = X**3+X+1, X**2+X, X**5+X**2+1
    require(c[0] == 0 and a[0] and c[1], "invalid degree-five chart")
    Y = R(beta)
    for j in (1, 2):
        Y += (Y**2+a*Y+b)[j] / a[0] * z**j
    require((Y**2+a*Y+b) % z**3 == 0, "base equation failed to order three")
    den = (c // z)**2
    coeffs = []
    for h in (R.one(), X, X**2, Y, Y**2):
        numerator = b*h
        A = numerator[0]/den[0]
        B = numerator[1]/den[0]
        C = (numerator[2] + A*den[2])/den[0]
        require((numerator - den*(A+B*z+C*z**2)) % z**3 == 0, "Laurent division failed")
        # Add wp(sqrt(A)/z); the constant C is unchanged.
        coeffs.append((B+A.sqrt(), C))
    poles, constants = zip(*coeffs)
    return poles, constants


def local_norms(entry):
    F = field_from_bits(entry["GF_modulus_bits"], 5, entry["id"])
    elements = [from_bits(F,j) for j in range(32)]
    R = PolynomialRing(F,"Z")
    Z = R.gen()
    poles, constants = reduced_poles_and_constants(entry, F)
    pole_bits = [to_bits(r,5) for r in poles]
    require(xor_rank(pole_bits) == 5, "reduced pole coefficients do not span F32")
    require(pole_bits == ramified_norm_test(entry)["reduced_poles"], "independent pole check failed")

    # Fix the unramified twist in Z^32+Z=1/z+twist. The true reduced AS
    # equations and S_ri(Z)^2+S_ri(Z) then differ by integral AS coboundaries.
    twists = [b for b in elements if all((C+r*b).trace() == 0 for r,C in zip(poles,constants))]
    require(len(twists) == 1, "expected a unique constant twist")
    twist, = twists
    shifts = []
    for r,C in zip(poles, constants):
        roots = [v for v in elements if v**2+v == C+r*twist]
        require(len(roots) == 2, "integral AS difference fails the residue solvability test")
        shifts.append(to_bits(roots[0],5))

    maps = []
    signatures = [0]*32
    kernel_intersection = set(range(32))
    for h in range(1,32):
        r = sum(poles[i] for i in range(5) if h & (1 << i))
        S = sum((r*Z)**(1 << j) for j in range(5))
        require(S**2+S == r*(Z**32+Z), "trace-polynomial AS equation failed")
        kernel = [j for j in range(32) if (r*elements[j]).trace() == 0]
        require(len(kernel) == 16, "wrong quadratic kernel order")
        P = prod(Z+elements[j] for j in kernel)
        require(P == S/r**16, "subspace product disagrees with the trace polynomial")
        for j, v in enumerate(elements):
            # Local uniformizers pi=1/Z and pi_h=1/P(Z) make the norm
            # of 1+v*pi exactly 1+P(v)*pi_h.
            require(P(Z+v) == P+P(v), "norm numerator is not P(Z)+P(v)")
            detected = bool(P(v))
            require(detected == bool((r*v).trace()), "wrong norm kernel")
            signatures[j] |= int(detected) << (h-1)
        kernel_intersection.intersection_update(kernel)
        maps.append({"character_mask": h, "trace_coefficient_bits": to_bits(r,5),
                     "nonzero_output_bits": to_bits(1/r**16,5), "kernel_inputs_bits": kernel})
    require(len({tuple(m["kernel_inputs_bits"]) for m in maps}) == 31, "repeated hyperplane")
    counts = Counter(bits.bit_count() for bits in signatures)
    require(kernel_intersection == {0} and counts == {0:1,16:31}, "joint detector failed")
    rank = xor_rank(signatures[1 << j] for j in range(5))
    require(rank == 5 and len(set(signatures)) == 32, "combined norm map is not injective")
    return {"place": entry["id"], "point_bits": entry["representative"],
            "residue_modulus_bits": entry["GF_modulus_bits"], "reduced_poles_bits": pole_bits,
            "regular_constants_bits": [to_bits(C,5) for C in constants],
            "twist_bits": to_bits(twist,5), "integral_correction_residue_roots_bits": shifts,
            "norm_maps": maps, "joint_binary_rank": rank,
            "common_kernel_inputs_bits": sorted(kernel_intersection),
            "detection_weight_histogram": dict(sorted(counts.items()))}


def compute():
    entries = json.loads(SUPPORT.read_text())["selected_allowed_ramification_places"]
    rows = [(e,local_coordinates(e)) for e in entries]
    fibres = {d:check_fibre(rows,d,shift) for d,shift in [(6,18),(8,24)]}
    ramified = [e for e in entries if e["chart"] == "ramified"]
    require(len(ramified) == 2 and all(e["degree"] == 5 for e in ramified),
            "the other ramified degree-five place must be available")
    norm_certificates = [local_norms(e) for e in ramified]
    # On each quadratic quotient the complete unramified fibres contribute
    # 6 and 8 to the divisor degree, and the other ramified place contributes 5.
    base_genus = 2
    canonical_degree = 2 * (2 * base_genus - 2) + 2 * sum(e["degree"] for e in ramified)
    max_zero_degree = canonical_degree + 2 * 6  # Split rational places of H.
    prescribed_zero_degree = 2 * (sum(2 * f["base_degree"] for f in fibres.values()) + 5)
    require(prescribed_zero_degree == 38 and max_zero_degree == 36, "the global zero obstruction failed")

    # Every isolated jet maps to zero under every norm by the zero count.
    # A trivial common kernel thus gives the full order of the local block.
    inertia_orders = {}
    mean_contribution = Fraction(0)
    for entry, certificate in zip(ramified, norm_certificates):
        require(certificate["common_kernel_inputs_bits"] == [0], "undetected local jet")
        order = 2 ** entry["degree"]
        inertia_orders[entry["id"]] = order
        mean_contribution += 2 * entry["degree"] * (1 - Fraction(1, order))
    return {"sage_version": SAGE_VERSION, "support_sha256": hashlib.sha256(SUPPORT.read_bytes()).hexdigest(),
            "fibres": fibres, "quotient_genus": 1 + canonical_degree // 2,
            "degree_of_prescribed_double_zeros": prescribed_zero_degree, "maximum_zero_degree": max_zero_degree,
            "full_2_primary_ray_inertia_orders": inertia_orders,
            "degree_five_mean_conductor_contribution": str(mean_contribution),
            "local_model": "Z^32+Z=1/z+twist; pi=1/Z, pi_h=1/P_h(Z), S_h=r_h^16 P_h",
            "encoding": "coefficient of the i-th basis generator has bit i; low bit is constant in F32",
            "ramified_places": norm_certificates}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="write the full JSON receipt to stdout")
    args = parser.parse_args()
    payload = json.dumps(compute(), indent=2)
    if args.emit:
        print(payload)
    else:
        require(json.loads(payload) == json.loads(RECEIPT.read_text()), "degree-five receipt mismatch")
        print("PASS: zero degree 38 > 36; all 31 norm maps jointly injective at both degree-five places")
