"""Compute the degree-ten fibre, local norm constraints and a global T-unit."""

import argparse
import json
from pathlib import Path

from sage.env import SAGE_VERSION

from m3_degree6_norm_obstruction import SUPPORT, check_fibre
from m3_quadratic_tunit_search import check_basis_norms, place_jet
from m3_ray_structure import local_coordinates, orbit, require, sha256_file, to_bits, xor_rank


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "m3-degree10-norm-obstruction.json"


def translation_mask(differences):
    require(all(v in (0, 1) for v in differences), "not a deck translation")
    return sum(int(v) << i for i, v in enumerate(differences))


def degree_ten_geometry(rows):
    selected = [(entry, data) for entry, data in rows if entry["degree"] == 10]
    require(len(selected) == 2, "expected two selected places")
    (first, data), (second, _) = selected
    field = data["field"]
    require(first["GF_modulus_bits"] == second["GF_modulus_bits"] == 1033,
            "inconsistent degree-ten residue fields")
    point = data["point"]
    x, y, *w = point
    require(first["representative"][:2] == second["representative"][:2]
            and len(orbit((x, y))[0]) == 5, "the base chart must be one degree-five point")
    frobenius = translation_mask([z**32 + z for z in w])
    other_shift = translation_mask([z + field.from_integer(k) for z, k in
                                    zip(w, second["representative"][2:])])
    require(frobenius == 21 and other_shift == 16, "degree-ten fibre labels changed")

    # Pair the 32 geometric points by the fifth power of Frobenius.
    labels = [g for g in range(32) if g < (g ^ frobenius)]
    orbits = set()
    for g in labels:
        lifted = (x, y, *(z + ((g >> i) & 1) for i, z in enumerate(w)))
        points, _ = orbit(lifted)
        require(len(points) == 10, "unexpected geometric orbit length")
        orbits.add(min(tuple(to_bits(v, 10) for v in q) for q in points))
    require(len(orbits) == 16, "incomplete degree-ten fibre")
    return field, labels, {
        "base_point": first["representative"][:2],
        "field_modulus_bits": first["GF_modulus_bits"],
        "base_degree": 5,
        "frobenius": frobenius,
        "second_translation": other_shift,
        "total_closed_places": len(orbits),
        "selected_places": [first["id"], second["id"]],
        "unselected_places": len(orbits) - len(selected),
    }


def local_norm_tests(field, labels, geometry):
    """Test first-jet fibre sums with 14 unconstrained closed places.

    Over one geometric base point the 32 values satisfy J(g+t)=J(g)^32.
    The coset sums over all subgroups of codimension at most r vanish iff
    the moments against square-free monomials of degree <= r do: coset
    indicators are products of affine forms and each monomial itself is a
    coordinate-coset indicator. Addition, including after Frobenius, is
    binary linear. Only the two selected values are prescribed by M2.
    """
    t = geometry["frobenius"]
    s = min(geometry["second_translation"], geometry["second_translation"] ^ t)
    require(0 in labels and s in labels and s != 0, "selected lifts coincide")
    output = []
    for codimension in (1, 2):
        moments = [m for m in range(32) if m.bit_count() <= codimension]
        columns, selected_columns = [], []
        for g in labels:
            for bit in range(10):
                value = 1 << bit
                conjugate = to_bits(field.from_integer(value)**32, 10)
                local = []
                for m in moments:
                    left = value if (g & m) == m else 0
                    right = conjugate if ((g ^ t) & m) == m else 0
                    local.append(left ^ right)
                columns.append(sum(z << (10 * i) for i, z in enumerate(local)))
                # The canonical representative of the second closed place may
                # be its conjugate; evaluate at the chart in the certificate.
                selected_value = 0
                if g == 0:
                    selected_value = value
                if g == s:
                    at_second = value if g == geometry["second_translation"] else conjugate
                    selected_value = at_second << 10
                selected_columns.append(selected_value)
        rank = xor_rank(columns)
        offset = 10 * len(moments)
        joint_rank = xor_rank(a | (b << offset) for a, b in zip(columns, selected_columns))
        require(joint_rank - rank == 20, "two-jet projection failed to be surjective")
        expected = {1: 30, 2: 80}[codimension]
        require(rank == expected, "unexpected rank of the fibre moment conditions")
        output.append({
            "max_subfield_degree_over_H": 2**codimension,
            "vanishing_moment_count": len(moments),
            "binary_rank": rank,
            "binary_kernel_dimension": len(columns) - rank,
            "binary_projection_rank_on_two_selected_places": joint_rank - rank,
        })
    return output


def global_unit(rows):
    # For h=x+x^2=b, w^2+w=(b/c)^2 makes w=(w+b/c)^2.
    # Thus u=(x+1)c*w has dlog equal to dlog((x+1)c) and is a T-unit
    # because the absolute norm of c*w is x^4*(x+1)^4.
    recipe = (6, 1, 0, 0, 4, 4)
    check_basis_norms([recipe])
    nonzero = {}
    zero_degrees = []
    for entry, data in rows:
        degree = entry["degree"]
        jet = place_jet(entry, data, [recipe])[0] ^ to_bits(data["coordinates"]["x+1"], degree)
        if entry["chart"] == "regular" and degree != 6:
            x, _, *w = data["point"]
            c = x**5 + x**2 + 1
            b = x**2 + x
            xi = w[1] + w[2]
            require((xi + b/c)**2 == xi, "quadratic square-class identity failed")
            expected = 1/(x+1) + x**4/c
            require(jet == to_bits(expected, degree), "inconsistent differential chart")
        if jet:
            nonzero[entry["id"]] = jet
        else:
            zero_degrees.append(degree)
    require(sorted(zero_degrees) == [5]*2 + [6]*16 + [8]*16, "unexpected unit support")
    return {"unit": "(x+1)*c*w_6", "recipe_for_c_times_w_6": list(recipe),
            "zero_jet_count": len(zero_degrees), "nonzero_jets": nonzero}


def compute():
    entries = json.loads(SUPPORT.read_text())["selected_allowed_ramification_places"]
    rows = [(entry, local_coordinates(entry)) for entry in entries]
    complete = {str(d): check_fibre(rows, d, t) for d, t in [(6, 18), (8, 24)]}
    field, labels, geometry = degree_ten_geometry(rows)
    ramified = [e["degree"] for e, _ in rows if e["chart"] == "ramified"]
    require(ramified == [5, 5], "ramification degrees changed")
    zero_degree = 2 * (sum(ramified) + 2 * sum(f["base_degree"] for f in complete.values()))
    canonical_degree = 2 * (2*2 - 2) + 2 * sum(ramified)
    zero_budget = canonical_degree + 12
    require(zero_degree == 48 and zero_budget == 36, "quadratic zero budget changed")
    return {
        "sage_version": SAGE_VERSION,
        "support_sha256": sha256_file(SUPPORT),
        "complete_zero_fibres": complete,
        "degree_ten": geometry,
        "quadratic_minimum_zero_degree": zero_degree,
        "quadratic_available_zero_degree": zero_budget,
        "geometric_fibre_norm_tests": local_norm_tests(field, labels, geometry),
        "explicit_global_unit": global_unit(rows),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the recomputed JSON")
    args = parser.parse_args()
    result = compute()
    if args.emit:
        print(json.dumps(result, indent=2))
    else:
        require(result == json.loads(RECEIPT.read_text()), "degree-ten receipt mismatch")
        print("PASS: degree-ten fibre, joint local norm tests and global T-unit jets")
