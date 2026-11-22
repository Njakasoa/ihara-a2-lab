"""Check the finite inputs to the degree-six full-field norm obstruction in Sage."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from sage.all import GF, VectorSpace
from sage.env import SAGE_VERSION

from m3_ray_structure import (
    BASE_UNIT_NAMES, field_from_bits, from_bits, h_basis, local_coordinates,
    orbit, pack_blocks, require, to_bits, xor_rank,
)

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "certificates" / "m2-tower.json"
RECEIPT = ROOT / "results" / "m3-degree6-norm-obstruction.json"


def check_fibre(rows, degree, expected_shift):
    """Certify one complete orbit above an H-place of half the degree."""
    lifts, bases, shifts = set(), set(), set()
    for entry, data in rows:
        if entry["degree"] != degree:
            continue
        point = data["point"]
        conjugates, _ = orbit(point)
        key = min(tuple(to_bits(v, degree) for v in q) for q in conjugates)
        lifts.add(key)
        base_orbit, _ = orbit(point[:2])
        require(len(base_orbit) == degree // 2, "wrong base degree")
        bases.add(min(tuple(to_bits(v, degree) for v in q) for q in base_orbit))
        shift = [z**(2**(degree // 2)) + z for z in point[2:]]
        require(all(v == 0 or v == 1 for v in shift), "nonbinary shift")
        shifts.add(sum(int(v) << i for i, v in enumerate(shift)))
    require(len(lifts) == 16 and len(bases) == 1, "incomplete fibre")
    require(shifts == {expected_shift}, "unexpected Frobenius")
    return {"base_degree": degree // 2, "places": len(lifts), "shift_mask": expected_shift}


def ramified_norm_test(entry):
    """Differentiate the candidate in H and reduce all five Artin–Schreier poles."""
    field = field_from_bits(entry["GF_modulus_bits"], 5, entry["id"])
    x, y = [from_bits(field, v) for v in entry["representative"]]
    a, b = x**3 + x + 1, x**2 + x
    require(x**5 + x**2 + 1 == 0 and a != 0, "wrong ramified H-chart")
    dy = ((x**2 + 1)*y + 1)/a
    c_prime = x**4
    jet = 1/x + 1/(x + 1) + (dy + 1)/(y + x)
    poles = []
    traces = []
    for h, dh in zip(h_basis(x, y), [0, 1, 0, dy, 0]):
        double_pole = b*h / c_prime**2
        simple_pole = (h + b*dh) / c_prime**2
        reduced = simple_pole + double_pole.sqrt()
        poles.append(to_bits(reduced, 5))
        traces.append(int((reduced*jet).trace()))
    mask = sum(t << i for i, t in enumerate(traces))
    require(xor_rank(poles) == 5, "a quadratic character is unramified")
    require(mask == 10 and traces[3] == 1, "candidate local norm syndrome changed")
    return {"point": entry["representative"], "reduced_poles": poles,
            "candidate_jet": to_bits(jet, 5), "traces": traces, "trace_mask": mask}


def quadratic_quotients(fibres, ramified):
    """Genus, zero budget, and forced local norm signs for all 31 characters."""
    quadratic_different = 2  # A nonzero reduced simple pole has lower jump one.
    ramified_degrees = [5 for _ in ramified]
    degree_canonical = 2*(2*2 - 2) + quadratic_different*sum(ramified_degrees)
    rational_places = 2*6  # The six rational H-places split completely.
    require(degree_canonical == 24, "quadratic quotient genus changed")
    by_character = []
    for h in range(1, 32):
        splits = {}
        for key, fibre in fibres.items():
            residue_degree = 1 + ((h & fibre["shift_mask"]).bit_count() % 2)
            splits[key] = {"count": 2 // residue_degree,
                           "place_degree": fibre["base_degree"]*residue_degree}
        q4 = splits["8"]
        total_q4_degree = q4["count"]*q4["place_degree"]
        total_ramified_degree = sum(ramified_degrees)
        pole_budget = degree_canonical + rational_places
        required_zeros = 2*(total_q4_degree + total_ramified_degree)
        require(pole_budget == required_zeros == 36, "zero budget must saturate")
        epsilon = (h & fibres["6"]["shift_mask"]).bit_count() % 2
        local_pairing = (h & ramified[0]["trace_mask"]).bit_count() % 2
        by_character.append({"mask": h, "degree3_fibre": splits["6"], "degree4_fibre": q4,
                             "epsilon": epsilon, "required_trace_bit": epsilon*local_pairing})
    required = {r["mask"]: r["required_trace_bit"] for r in by_character}
    require(required[8] == required[16] == 0 and required[8 ^ 16] == 1,
            "local norm functional must violate additivity")
    return {"genus": 1 + degree_canonical//2, "rational_places": rational_places,
            "different_exponent_at_each_ramified_place": quadratic_different,
            "degree_of_q4_fibre": total_q4_degree, "degree_of_two_ramified_places": total_ramified_degree,
            "available_zero_degree": pole_budget, "required_zero_degree": required_zeros,
            "remaining_zero_degree": pole_budget - required_zeros, "characters": by_character,
            "nonadditivity_witness": {"masks": [8, 16, 24], "required_bits": [required[i] for i in (8, 16, 24)]}}


def compute():
    entries = json.loads(SUPPORT.read_text())["selected_allowed_ramification_places"]
    rows = [(entry, local_coordinates(entry)) for entry in entries]
    fibres = {str(d): check_fibre(rows, d, shift) for d, shift in [(6, 18), (8, 24)]}
    space = VectorSpace(GF(2), 5)
    frobenius = space([(18 >> i) & 1 for i in range(5)])
    fibres_by_size = Counter()
    for dimension in range(1, 6):
        for subgroup in space.subspaces(dimension):
            size = 2**dimension // (2 if frobenius in subgroup else 1)
            fibres_by_size[size] += 1
            if size == 1:
                require(dimension == 1 and frobenius in subgroup, "unexpected exception")
    require(sum(fibres_by_size.values()) == 373 and fibres_by_size[1] == 1,
            "failed intermediate-field enumeration")

    packed = [pack_blocks([(data["coordinates"][unit], entry["degree"])
                           for entry, data in rows]) for unit in BASE_UNIT_NAMES]
    require(xor_rank(packed) == 5, "base-unit square classes are dependent")
    jets = {}
    for degree in (6, 8):
        local_rows = {tuple(to_bits(data["coordinates"][name], degree) for name in BASE_UNIT_NAMES)
                      for entry, data in rows if entry["degree"] == degree}
        require(len(local_rows) == 1, "certificate changed the residue coordinates")
        jets[degree], = local_rows

    possible = []
    for mask in range(32):
        image = {6: 0, 8: 0}
        for i in range(5):
            if mask & (1 << i):
                for d in image:
                    image[d] ^= jets[d][i]
        if image[8] == 0 and image[6] != 0:
            possible.append({"mask": mask, "degree6_jet": image[6]})
    require(possible == [{"mask": 19, "degree6_jet": 15}], "norm candidate changed")
    require(frobenius[3] == 0, "the h=y quadratic field must lie in the fixed field")
    ramified = [ramified_norm_test(e) for e in entries if e["chart"] == "ramified"]
    require(len(ramified) == 2, "expected both degree-five ramification places")
    # Row i is indexed by the chosen norm character e_i. A sum of s (c*s)^t
    # is symmetric; the matrix required by an isolated jet is tau syndrome^t.
    syndrome = ramified[0]["traces"]
    tensor = [[int(frobenius[i])*syndrome[j] for j in range(5)] for i in range(5)]
    require(tensor[1][3] == 1 and tensor[3][1] == 0, "missing asymmetry")
    return {"sage_version": SAGE_VERSION, "support_sha256": hashlib.sha256(SUPPORT.read_bytes()).hexdigest(),
            "fibres": fibres, "proper_subfields_by_fibre_size": dict(sorted(fibres_by_size.items())),
            "units": list(BASE_UNIT_NAMES), "unit_rank": xor_rank(packed),
            "base_jets": jets, "norm_candidates": possible, "ramified_local_norm_tests": ramified,
            "required_tensor": tensor, "off_diagonal_witness": {"m_1_3": tensor[1][3], "m_3_1": tensor[3][1]},
            "quadratic_quotients": quadratic_quotients(fibres, ramified)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the deterministic JSON")
    args = parser.parse_args()
    payload = json.dumps(compute(), indent=2) + "\n"
    if args.emit:
        print(payload, end="")
    else:
        require(json.loads(payload) == json.loads(RECEIPT.read_text()), "receipt mismatch")
        print("PASS: degree-six full-field norm obstruction")


if __name__ == "__main__":
    main()
