"""Check the quadratic norm constraints at the M2 places of degree eight.

Base-unit masks use the order (x, x+1, y, y+1, y+x). Character masks
use the five Artin--Schreier generators of the genus-343 field. The two
bases both have five elements and refer to different vector spaces.
"""

import argparse
import json
from pathlib import Path

from sage.env import SAGE_VERSION

from m3_degree6_norm_obstruction import SUPPORT, check_fibre, ramified_norm_test
from m3_ray_structure import (
    BASE_UNIT_NAMES,
    field_from_bits,
    from_bits,
    local_coordinates,
    require,
    sha256_file,
    to_bits,
    xor_rank,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "results" / "m3-degree8-norm-obstruction.json"


def linear_combination(values, mask):
    value = 0
    for i, coefficient in enumerate(values):
        if mask & (1 << i):
            value ^= coefficient
    return value


def binary_pairing(left, right):
    return (left & right).bit_count() % 2


def ramified_base_units(entry):
    field = field_from_bits(entry["GF_modulus_bits"], 5, entry["id"])
    x, y = [from_bits(field, v) for v in entry["representative"]]
    dy = ((x**2 + 1) * y + 1) / (x**3 + x + 1)
    jets = [1/x, 1/(x + 1), dy/y, dy/(y + 1), (dy + 1)/(y + x)]
    pole_bits = ramified_norm_test(entry)["reduced_poles"]
    poles = [from_bits(field, bits) for bits in pole_bits]
    syndromes = [
        sum(int((pole * jet).trace()) << i for i, pole in enumerate(poles))
        for jet in jets
    ]
    return {
        "point": entry["representative"],
        "jets": [to_bits(jet, 5) for jet in jets],
        "reduced_poles": pole_bits,
        "trace_syndromes": syndromes,
    }


def base_square_classes(jets, ramified):
    classes = []
    for mask in range(32):
        classes.append({
            "mask": mask,
            "jet_Q3": linear_combination(jets[6], mask),
            "jet_Q4": linear_combination(jets[8], mask),
            "jets_Q5": [linear_combination(q["jets"], mask) for q in ramified],
            "syndromes_Q5": [
                linear_combination(q["trace_syndromes"], mask) for q in ramified
            ],
        })
    return classes


def common_root_tests(candidates, classes, frobenius):
    """Test the same square root w of the total norm at both ramified places."""
    tests = []
    for candidate in candidates:
        allowed = []
        for root in classes:
            place_pairs = list(zip(root["syndromes_Q5"], candidate["syndromes_Q5"]))
            compatible = all(
                binary_pairing(h, root_mask)
                == binary_pairing(h, frobenius) * binary_pairing(h, candidate_mask)
                for root_mask, candidate_mask in place_pairs
                for h in range(1, 32)
            )
            if compatible:
                allowed.append(root["mask"])
        tests.append({
            "candidate_class": candidate["mask"],
            "target_jet": candidate["jet_Q4"],
            "syndromes_Q5": candidate["syndromes_Q5"],
            "common_root_classes": allowed,
        })
    return tests


def compute():
    entries = json.loads(SUPPORT.read_text())["selected_allowed_ramification_places"]
    rows = [(entry, local_coordinates(entry)) for entry in entries]
    fibres = {degree: check_fibre(rows, degree, shift) for degree, shift in [(6, 18), (8, 24)]}

    jets = {}
    for degree in fibres:
        values = {
            tuple(to_bits(data["coordinates"][name], degree) for name in BASE_UNIT_NAMES)
            for entry, data in rows if entry["degree"] == degree
        }
        require(len(values) == 1, "base charts disagree on a complete fibre")
        jets[degree], = values
    ramified = [ramified_base_units(entry) for entry in entries if entry["chart"] == "ramified"]
    require(len(ramified) == 2, "expected two degree-five places")
    require(all(xor_rank(q["trace_syndromes"]) == 5 for q in ramified),
            "the five base units must have independent norm syndromes")
    classes = base_square_classes(jets, ramified)
    kernel_q3 = [c for c in classes if c["jet_Q3"] == 0]
    common = [c["mask"] for c in kernel_q3 if not any(c["jets_Q5"])]
    require([c["mask"] for c in kernel_q3] == [0, 1, 2, 3] and common == [0],
            "unexpected base-unit kernel at Q3 and Q5")
    require(xor_rank(c["jet_Q4"] for c in kernel_q3) == 2,
            "the Q4 jet must be injective on the two-dimensional Q3 kernel")

    tests = common_root_tests(kernel_q3, classes, fibres[8]["shift_mask"])
    expected = [(0, 0, 0, [0]), (1, 189, 16, []), (2, 188, 24, [2]), (3, 1, 8, [])]
    for test, (mask, jet, syndrome, roots) in zip(tests, expected):
        require(test["candidate_class"] == mask and test["target_jet"] == jet
                and test["syndromes_Q5"] == [syndrome, syndrome]
                and test["common_root_classes"] == roots, "quadratic norm constraint changed")
    surviving_jets = [t["target_jet"] for t in tests if t["target_jet"] and t["common_root_classes"]]
    dimension = xor_rank(surviving_jets)
    require(dimension == 1, "quadratic constraints should leave one binary direction")

    zeta = ROOT / "certificates" / "k343-zeta.json"
    class_number = sum(json.loads(zeta.read_text())["base_H_zeta"])
    require(class_number == 19, "odd base class number required for descent")
    return {
        "sage_version": SAGE_VERSION,
        "support_sha256": sha256_file(SUPPORT),
        "zeta_sha256": sha256_file(zeta),
        "base_class_number": class_number,
        "units": list(BASE_UNIT_NAMES),
        "fibres": fibres,
        "ramified_base_units": ramified,
        "classes": classes,
        "kernel_Q3_and_Q5": common,
        "common_root_tests": tests,
        "surviving_nonzero_jets": surviving_jets,
        "isolated_jet_dimension_upper_bound": dimension,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the recomputed JSON")
    args = parser.parse_args()
    payload = json.dumps(compute(), indent=2)
    if args.emit:
        print(payload)
    else:
        require(json.loads(payload) == json.loads(RECEIPT.read_text()), "degree-eight receipt mismatch")
        print("PASS: 32 base square classes, 31 norm conditions, one possible nonzero degree-eight jet")
