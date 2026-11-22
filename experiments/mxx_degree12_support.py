"""Pin two labelled supports allowed by Ma--Xing--Xing v2, Theorem 6.1.

The labels refer to the AS basis (1, x, x^2, x^3, y). A label g is the
smaller integer in its coset modulo the Frobenius translation of the
underlying H place. The Frobenius-stable coordinate chart is x-x(P).
"""

import argparse
import json
from pathlib import Path

from sage.env import SAGE_VERSION

from m3_ray_structure import field_from_bits, from_bits, orbit, to_bits
from mxx_genus334_sage import basis, coefficient, require


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "mxx-degree12-support.json"
SOURCE = "https://arxiv.org/html/2610.33649v2#S6.SS1"
# Residue field modulus, base x-polynomial, splitting/inert masks cited
# in the paper, and multiplicity in the support.
FIBRES = {
    8: (283, 7, 1, 2, 16),
    10: (1033, 37, 4, 8, 12),
    12: (4105, 73, 1, 2, 1),
}
MIXED_DEGREE_TEN = (
    (59, 2, 1, (15, 315), (0, 1, 2, 3, 16, 17, 18, 19)),
    (37, 8, 2, (314, 770), (0, 1, 2, 3)),
)


def polynomial(bits, x):
    return sum((x**i for i in range(bits.bit_length()) if (bits >> i) & 1),
               x.parent().zero())


def translate(point, mask):
    return point[:2] + tuple(w + ((mask >> i) & 1) for i, w in enumerate(point[2:]))


def regular_fibre(degree):
    """Return the finite field, a common geometric lift and its closed-place labels."""
    modulus, x_mask, split_mask, inert_mask, _ = FIBRES[degree]
    return construct_fibre(degree, modulus, x_mask, split_mask, inert_mask)


def construct_fibre(degree, modulus, x_mask, split_mask, inert_mask):
    """Construct the specified H-place and label all its lifts on the AS cover."""
    field = field_from_bits(modulus, degree, f"mxx{degree}")
    elements = [from_bits(field, i) for i in range(2**degree)]
    x = next(z for z in elements if polynomial(x_mask, z) == 0)
    a, b = x**3+x+1, x**2+x
    require(a != 0, "x must be an unramified chart parameter")
    least_root = {}
    for v in elements:
        least_root.setdefault(v*v+v, v)
    candidates = []
    for y in elements:
        if y*y+a*y != b:
            continue
        c = coefficient(x, y)
        require(c != 0, "unexpected ramified AS fibre")
        roots = tuple(least_root[b*h/c**2] for h in basis(x,y))
        shift = tuple(z**(2**(degree//2)) + z for z in roots)
        require(all(s in (0,1) for s in shift), "base Frobenius is not a translation")
        mask = sum(int(s) << i for i,s in enumerate(shift))
        if (mask & split_mask).bit_count() % 2 or (mask & inert_mask).bit_count() % 2 != 1:
            continue
        candidates.append(((x, y) + roots, mask))
    require(candidates, "no fibre has the specified splitting behaviour")
    point, frobenius = candidates[0]
    base_orbit, _ = orbit(point[:2])
    require(len(base_orbit) == degree//2, "wrong H residue degree")
    require(all(p[:2] in base_orbit for p, _ in candidates), "distinct eligible H places")
    labels = [g for g in range(32) if g < (g ^ frobenius)]
    orbit_ids = set()
    for g in labels:
        full_orbit, _ = orbit(translate(point, g))
        require(len(full_orbit) == degree, "wrong residue degree on k")
        orbit_ids.add(min(tuple(to_bits(v, degree) for v in row) for row in full_orbit))
    require(len(labels) == len(orbit_ids) == 16, "the fibre must have sixteen distinct places")
    return field, point, frobenius, labels


def ramified_branches():
    """Split character 11 identifies the two degree-six places above P3."""
    field = field_from_bits(11, 3, "ram3")
    x = from_bits(field, 2)
    y = x*x
    d = x**4+x**3+x*x+x
    require(x**3+x+1 == 0 and coefficient(x,y) == 0 and d != 0, "wrong P3")
    # pi=y+x^2 satisfies pi^2+a*pi=a*b, and c=d*pi+O(pi^2).
    # Thus the integral RHS b*a/c^2 of character 11 has residue 1/d^2.
    residue = 1/d**2
    roots = sorted(to_bits(v, 3) for v in field if v**2+v == residue)
    require(roots == [4,5], "unexpected residues for the split character")
    return {"H_point_bits": [to_bits(x,3), to_bits(y,3)], "H_modulus_bits": 11,
            "residue_degree_over_H": 2, "ramification_index_over_H": 8,
            "split_character_mask": 11, "AS_rhs_residue_bits": to_bits(residue,3),
            "character_residue_and_exponent": [[roots[0],2], [roots[1],3]]}


def compute():
    fibres = {}
    for degree, (modulus, x_mask, split, inert, count) in FIBRES.items():
        _, point, shift, labels = regular_fibre(degree)
        fibres[str(degree)] = {
            "field_modulus_bits": modulus, "x_polynomial_bits": x_mask,
            "split_character_mask": split, "inert_character_mask": inert,
            "base_lift_bits": [to_bits(v,degree) for v in point],
            "frobenius_mask": shift, "closed_place_labels": labels,
            "selected_labels": labels[:count], "exponent": 2,
        }
    mixed_fibres = []
    for x_mask, split, inert, base_point, selected in MIXED_DEGREE_TEN:
        _, point, shift, labels = construct_fibre(10, 1033, x_mask, split, inert)
        bits = [to_bits(v, 10) for v in point]
        require(tuple(bits[:2]) == base_point, "incorrect mixed-support base point")
        require(set(selected) <= set(labels) and len(set(selected)) == len(selected),
                "invalid choice of distinct degree-ten places")
        mixed_fibres.append({"x_polynomial_bits": x_mask, "base_lift_bits": bits,
                             "frobenius_mask": shift, "closed_place_labels": labels,
                             "selected_labels": list(selected)})
    require(sum(len(row["selected_labels"]) for row in mixed_fibres) == 12
            and MIXED_DEGREE_TEN[0][0] != MIXED_DEGREE_TEN[1][0],
            "mixed support must contain twelve distinct degree-ten places")
    return {"source": SOURCE, "sage_version": SAGE_VERSION,
            "AS_basis": ["1","x","x^2","x^3","y"], "rational_splitting_places": 192,
            "degree_six": ramified_branches(), "regular_fibres": fibres,
            "mixed_support_degree_ten_replacements": mixed_fibres}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    result = compute()
    if parser.parse_args().emit:
        print(json.dumps(result, indent=2))
    else:
        require(result == json.loads(RECEIPT.read_text()), "labelled support receipt mismatch")
        print("PASS: ramified branches, five regular fibres, and both degree-ten selections")
