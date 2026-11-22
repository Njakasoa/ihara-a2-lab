"""Exclude the remaining degree-eight jet using the quartic quotient C_(2,8).

Sage recomputes the Riemann--Roch dimension on H, tests a necessary
logarithmic-derivative identity at an auxiliary point, and compares values
at both branches of the quadratic subfield C_2 over the degree-four place.
Run with --emit for the full receipt, or without arguments to check it.
"""

import argparse
import json
from pathlib import Path

from sage.all import GF, FunctionField, PolynomialRing, PowerSeriesRing
from sage.env import SAGE_VERSION

from m3_ray_structure import field_from_bits, from_bits, require, sha256_file, to_bits


ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "certificates" / "m2-tower.json"
RECEIPT = ROOT / "results" / "m3-degree8-quartic-norm.json"


def basis_values(x, y):
    d = x*(x**5+x**2+1)
    return [x**i/d for i in range(7)] + [x**i*y/d for i in range(4)]


def rr_space():
    """The bound on A is the zero divisor of x*c on the genus-two field."""
    K = FunctionField(GF(2), "x")
    x = K.gen()
    Y = PolynomialRing(K, "Y").gen()
    H = K.extension(Y**2 + (x**3+x+1)*Y + x**2+x, "y")
    x, y = H(x), H.gen()
    divisor = (x*(x**5+x**2+1)).divisor_of_zeros()
    require(sorted((int(P.degree()), int(divisor.valuation(P))) for P in divisor.support()) ==
            [(1,1),(1,1),(5,1),(5,1)], "unexpected pole allowance")
    require(H.genus() == 2 and divisor.degree() == 12, "Riemann--Roch degree changed")
    require(len(divisor.basis_function_space()) == 11, "unexpected dimension")
    functions = basis_values(x, y)
    for g in functions:
        require((g.divisor() + divisor).is_effective(), "basis element outside L(D)")
    # Multiplication by x*c gives 1,...,x^6 and y,...,x^3*y;
    # these are independent since H/F2(x) is quadratic.
    deriv = H.derivation()
    require(deriv(x) == 1 and (x**3+x+1)*deriv(y) == (x**2+1)*y+1,
            "expected the derivation with respect to x")
    f_x = (x**2+x)*x/(x**5+x**2+1)**2
    require((x+1)*deriv(f_x)+f_x == 0, "inhomogeneous term did not cancel")
    defects = sum_table([(x+1)*deriv(g)+g**2+g for g in functions])
    return len(functions), [i for i,v in enumerate(defects) if not v]


def sum_table(basis):
    values = [basis[0].parent().zero()]
    for v in basis:
        values += [s+v for s in values]
    return values


def compute():
    dimension, symbolic_kernel = rr_space()
    entries = json.loads(SUPPORT.read_text())["selected_allowed_ramification_places"]
    places = [e for e in entries if e["degree"] == 8]
    require(len(places) == 16 and {e["GF_modulus_bits"] for e in places} == {283},
            "unexpected degree-eight fibre")
    F = field_from_bits(283, 8, "quartic")
    # Auxiliary point: the two-term expansion in t=x-x0 evaluates each
    # rational basis function and its derivative without symbolic division.
    x0, y0 = [from_bits(F,v) for v in (2,197)]
    a0 = x0**3+x0+1
    require(a0 and x0*(x0**5+x0**2+1) and y0**2+a0*y0==x0**2+x0,
            "auxiliary point is not on the required chart")
    R = PowerSeriesRing(F, "t", default_prec=2)
    t = R.gen()
    xt = (R(x0)+t).add_bigoh(2)
    yt = (R(y0) + ((x0**2+1)*y0+1)/a0*t).add_bigoh(2)
    require(yt**2+(xt**3+xt+1)*yt == xt**2+xt, "invalid tangent direction")
    columns = []
    for g in basis_values(xt,yt):
        value, derivative = g[0], g[1]
        columns.append((x0+1)*derivative + value**2 + value)
    defects = sum_table(columns)
    survivors = [m for m, d in enumerate(defects) if d == 0]
    require(len(survivors) == 16 and len(defects) == 2**dimension, "unexpected kernel")
    require(survivors == symbolic_kernel, "symbolic and pointwise kernels differ")

    values_at_Q4 = set()
    branch_values = set()
    for place in places:
        X, Y, *w = [from_bits(F,v) for v in place["representative"]]
        require((to_bits(X,8),to_bits(Y,8)) == (188,12), "inconsistent base point")
        c = X**5+X**2+1
        f = (X**2+X)*X/c**2
        xi = w[1]  # character mask 2, i.e. the generator indexed by x
        require(xi**2+xi == f and xi**16 == xi, "C_2 must split at Q4")
        branch_values.update((to_bits(xi,8),to_bits(xi+1,8)))
        values = sum_table(basis_values(X,Y))
        values_at_Q4.update(to_bits(values[m],8) for m in survivors)
    require(branch_values == {92,93} and not values_at_Q4.intersection(branch_values),
            "the quartic test no longer excludes the nonzero jet")
    return {
        "sage_version": SAGE_VERSION, "support_sha256": sha256_file(SUPPORT),
        "quartic_character_masks": [2,8], "Frobenius_Q4_mask": 24,
        "RR_degree": 12, "RR_dimension": dimension, "A_candidates": len(defects),
        "A_basis": "1,x,...,x^6,y,xy,x^2y,x^3y divided by x*(x^5+x^2+1)",
        "auxiliary_field_modulus_bits": 283, "auxiliary_point": [2,197],
        "necessary_equation": "(x+1)*A' + A^2 + A = 0",
        "auxiliary_test_columns": [to_bits(z,8) for z in columns],
        "surviving_A_masks": survivors, "point_over_Q4": [188,12],
        "symbolic_kernel_equals_auxiliary_kernel": True,
        "possible_A_values_at_Q4": sorted(values_at_Q4),
        "required_branch_values_at_Q4": sorted(branch_values),
        "intersection": sorted(values_at_Q4.intersection(branch_values)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print deterministic JSON")
    if parser.parse_args().emit:
        print(json.dumps(compute(), indent=2))
    else:
        require(compute() == json.loads(RECEIPT.read_text()), "quartic receipt mismatch")
        print("PASS: 2048 Riemann--Roch candidates, 16 pass the auxiliary test,"
              " none attains either quartic-norm branch value")


if __name__ == "__main__":
    main()
