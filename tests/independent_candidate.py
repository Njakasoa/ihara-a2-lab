#!/usr/bin/env python3
"""Independent Sage audit of concrete k343 place representatives.

The checker reconstructs each stored finite field from its modulus bits,
checks the normalized chart equations, and verifies exact Frobenius orbits.
It intentionally does not import ``src`` or the M1 checker.  Candidate-search
arithmetic is enabled when results/m2-search.json exists; absent search output
is reported as a bounded waiting state rather than guessed.
"""

from __future__ import annotations

import json
import copy
from fractions import Fraction
from pathlib import Path

try:
    from sage.all import GF, PolynomialRing
except ImportError as exc:  # pragma: no cover - only outside Sage.
    raise SystemExit(
        "independent_candidate.py must be run with scripts/sage-python"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def field_from_bits(bits, degree, name):
    """Build the exact Sage field represented by an inventory modulus."""
    bits = int(bits)
    degree = int(degree)
    require(0 <= bits < (1 << (degree + 1)),
            "field modulus bits exceed the declared degree")
    if degree == 1:
        # The legacy inventory records bits=2 for F2; there is no modulus
        # argument for Sage's prime field constructor.
        require(bits == 2, "unexpected degree-one modulus encoding")
        return GF(2)
    P = PolynomialRing(GF(2), "m")
    m = P.gen()
    modulus = P(sum(((bits >> i) & 1) * m**i
                    for i in range(degree + 1)))
    require(modulus.degree() == degree and modulus.is_irreducible(),
            f"declared modulus is not irreducible of degree {degree}")
    safe_name = "".join(char if char.isalnum() else "_" for char in str(name))
    if not safe_name or safe_name[0].isdigit():
        safe_name = "f_" + safe_name
    return GF(2**degree, safe_name, modulus=modulus)


def from_bits(F, value):
    value = int(value)
    require(0 <= value < F.cardinality(),
            "coordinate is outside its finite field")
    if F.cardinality() == 2:
        return F(value)
    return F.from_integer(value)


def to_bits(value):
    polynomial = value.polynomial()
    return sum(int(polynomial[i]) << i for i in range(value.parent().degree()))


def orbit(point):
    """Return the exact Frobenius orbit and its first return point."""
    seen = []
    current = tuple(point)
    while current not in seen:
        seen.append(current)
        current = tuple(value * value for value in current)
    return seen, current


def orbit_signature(points):
    encoded = [tuple(to_bits(value) for value in point) for point in points]
    return min(encoded)


def h_equation(xx, yy):
    aa = xx**3 + xx + 1
    bb = xx**2 + xx
    return yy**2 + aa * yy == bb


def k_basis(xx, yy):
    return [xx**0, xx, xx**2, yy, yy**2]


def validate_entry(entry, degree, field_name):
    require(isinstance(entry, dict), f"{field_name}: place is not an object")
    require(int(entry["degree"]) == degree,
            f"{field_name}: wrong declared degree")
    require(isinstance(entry.get("id"), str) and entry["id"],
            f"{field_name}: missing place id")
    bits = int(entry["GF_modulus_bits"])
    F = field_from_bits(bits, degree, f"{field_name}_{degree}")
    raw = entry["representative"]
    chart = entry["chart"]
    if chart == "infinity":
        require(degree == 1, f"{field_name}: infinity chart has degree != 1")
        require(len(raw) == 6, f"{field_name}: bad infinity representative")
        require(all(int(value) in (0, 1) for value in raw),
                f"{field_name}: infinity coordinates leave F2")
        point = tuple(from_bits(F, value) for value in raw)
    elif chart == "ramified":
        require(len(raw) == 2, f"{field_name}: bad ramified representative")
        point = tuple(from_bits(F, value) for value in raw)
        xx, yy = point
        aa = xx**3 + xx + 1
        cc = xx**5 + xx**2 + 1
        require(h_equation(xx, yy), f"{field_name}: ramified point fails H")
        require(cc == 0 and aa != 0,
                f"{field_name}: ramified point does not lie over c=0")
    elif chart == "regular":
        require(len(raw) == 7, f"{field_name}: bad regular representative")
        point = tuple(from_bits(F, value) for value in raw)
        xx, yy, *ws = point
        aa = xx**3 + xx + 1
        bb = xx**2 + xx
        cc = xx**5 + xx**2 + 1
        require(h_equation(xx, yy), f"{field_name}: regular point fails H")
        require(cc != 0, f"{field_name}: regular chart has c=0")
        for wi, hi in zip(ws, k_basis(xx, yy)):
            require(wi**2 + wi == bb * hi / (cc * cc),
                    f"{field_name}: AS coordinate equation failed")
    else:
        raise AssertionError(f"{field_name}: unknown chart {chart!r}")

    points, returned = orbit(point)
    require(returned == point, f"{field_name}: Frobenius orbit did not return")
    require(len(points) == degree,
            f"{field_name}: orbit length is not the declared degree")
    return F, point, points, orbit_signature(points)


def load_entries(path, label, expected_counts):
    data = json.loads(path.read_text())
    entries = []
    if isinstance(data, dict):
        for key, rows in data.items():
            degree = int(key)
            require(isinstance(rows, list), f"{label}: degree bucket is not a list")
            require(degree in expected_counts,
                    f"{label}: unexpected degree {degree}")
            for row in rows:
                entries.append((degree, row))
    else:
        require(isinstance(data, list), f"{label}: inventory is not a list")
        require(len(expected_counts) == 1,
                f"{label}: list inventory needs one expected degree")
        degree = next(iter(expected_counts))
        entries = [(degree, row) for row in data]

    actual_counts = {}
    ids = set()
    signatures = set()
    checked = []
    for index, (degree, row) in enumerate(entries, 1):
        name = f"{label}[{index}]"
        require(row["id"] not in ids, f"{name}: duplicate place id")
        ids.add(row["id"])
        _, point, points, signature = validate_entry(row, degree, name)
        key = (degree, row["chart"], signature)
        require(key not in signatures, f"{name}: duplicate Frobenius orbit")
        signatures.add(key)
        actual_counts[degree] = actual_counts.get(degree, 0) + 1
        checked.append((degree, row, point, points, signature))

    require(actual_counts == expected_counts,
            f"{label}: wrong place cardinalities {actual_counts}")
    # Canonical inventories are ordered by the encoded minimum Frobenius
    # representative within each degree and chart.  This is the order used
    # when a multiplicity row selects the first available places.
    for degree in expected_counts:
        for chart in {row["chart"] for d, row, *_ in checked
                      if d == degree}:
            rows = [(signature, row["id"])
                    for d, row, _, _, signature in checked
                    if d == degree and row["chart"] == chart]
            require(rows == sorted(rows),
                    f"{label}: rows are not canonical in degree {degree}")
    return checked, ids, signatures


def validate_main_inventory():
    expected = {1: 192, 5: 2, 6: 16, 8: 16, 10: 64}
    checked, ids, signatures = load_entries(
        ROOT / "curves/k343-places.json", "k343-places", expected)
    by_degree = {degree: [row for d, row, *_ in checked if d == degree]
                 for degree in expected}
    infinity = {tuple(int(value) for value in row["representative"])
                for row in by_degree[1] if row["chart"] == "infinity"}
    expected_infinity = {
        (branch, w0, w1, w2, w3, w4)
        for branch in (0, 1)
        for w0 in (0, 1)
        for w1 in (0, 1)
        for w2 in (0, 1)
        for w3 in (0, 1)
        for w4 in (0, 1)
    }
    require(infinity == expected_infinity,
            "k343-places: infinity normalized chart is incomplete or duplicated")
    require(sum(row["chart"] == "regular" for row in by_degree[1]) == 128,
            "k343-places: rational regular split count is not 128")
    require(all(row["chart"] == "ramified" for row in by_degree[5]),
            "k343-places: degree-five inventory is not ramified chart")
    require(all(row["chart"] == "regular"
                for degree in (6, 8, 10)
                for row in by_degree[degree]),
            "k343-places: non-ramified inventory has a wrong chart")
    T_ids = {row["id"] for row in by_degree[1]}
    require(len(T_ids) == 192, "k343-places: T is not the 192-place d=1 inventory")
    require(not (T_ids & (ids - T_ids)),
            "k343-places: a selected non-rational place overlaps T")
    return ({"counts": expected, "checked": len(checked),
             "T_size": len(T_ids), "infinity_size": len(infinity),
             "signature_count": len(signatures)}, checked)


def validate_degree12_inventory():
    expected = {12: 208}
    checked, ids, signatures = load_entries(
        ROOT / "curves/k343-degree12-places.json", "k343-degree12-places", expected)
    require(all(row["chart"] == "regular" for _, row, *_ in checked),
            "k343-degree12-places: a degree-12 row is not regular")
    return ({"counts": expected, "checked": len(checked),
             "signature_count": len(signatures), "ids": len(ids)}, checked)


def validate_degree12_lifting():
    cert = json.loads((ROOT / "certificates/degree12-lifting.json").read_text())
    require(cert["base"] == "H", "degree12 lifting has the wrong base")
    require(int(cert["field_modulus_bits"]) == 67,
            "degree12 lifting has the wrong F64 modulus")
    rows = cert["H_degree6_places"]
    require(len(rows) == 13, "degree12 lifting does not have 13 H places")
    F = field_from_bits(67, 6, "lifting_F64")
    signatures = set()
    for index, row in enumerate(rows, 1):
        name = f"degree12-lifting[{index}]"
        require(int(row["degree"]) == 6, f"{name}: wrong H degree")
        raw = row["representative"]
        require(len(raw) == 2, f"{name}: malformed H representative")
        point = tuple(from_bits(F, value) for value in raw)
        xx, yy = point
        require(h_equation(xx, yy), f"{name}: representative fails H")
        cc = xx**5 + xx**2 + 1
        require(cc != 0, f"{name}: ramified c=0 point used for lifting")
        vector = [int(value) for value in row["Frobenius_vector"]]
        require(len(vector) == 5 and all(value in (0, 1) for value in vector),
                f"{name}: malformed Frobenius vector")
        require(any(vector), f"{name}: Frobenius vector has order one")
        factor = (xx**2 + xx) / (cc * cc)
        computed = [int((factor * hi).trace()) for hi in k_basis(xx, yy)]
        require(computed == vector,
                f"{name}: stored five-bit Frobenius vector disagrees")
        require(int(row["residue_extension_degree_in_k"]) == 2,
                f"{name}: wrong residue extension degree")
        require(int(row["places_above"]) == 16,
                f"{name}: wrong number of places above")
        require(int(row["degree_above"]) == 12,
                f"{name}: wrong lifted degree")
        points, returned = orbit(point)
        require(returned == point and len(points) == 6,
                f"{name}: H representative has wrong Frobenius orbit")
        signature = orbit_signature(points)
        require(signature not in signatures,
                f"{name}: duplicate H degree-six orbit")
        signatures.add(signature)
    lower_bound = sum(int(row["places_above"]) for row in rows)
    require(lower_bound == 208, "degree12 lifting lower bound is not 208")
    require(int(cert["k_degree12_places_lower_bound"]) == lower_bound,
            "degree12 lifting stored lower bound disagrees")
    return {"H_degree6_orbits": len(signatures),
            "k_degree12_lower_bound": lower_bound,
            "vector_traces": "PASS"}


def exact_dm_row(places, t, genus=343):
    A = sum(int(multiplicity) * int(degree)
            for degree, multiplicity in places)
    C = sum(int(multiplicity) * int(degree) * (int(degree) + 1)
            for degree, multiplicity in places)
    D = 1 + A - int(t)
    margin = D**2 - 2 * C - 4 * A
    mean = 2 * sum(Fraction(int(multiplicity) * int(degree))
                   * (1 - Fraction(1, 2**int(degree)))
                   for degree, multiplicity in places)
    denominator = Fraction(int(genus) - 1) + mean / 2
    ratio = Fraction(int(t)) / denominator
    return {"A": A, "C": C, "D": D, "GS_margin": margin,
            "mean_conductor_upper_bound": mean,
            "denominator": denominator, "ratio": ratio}


def validate_gs(row):
    require(row["t"] > 0 and row["t"] <= row["A"],
            "candidate has unavailable or excessive splitting multiplicity")
    require(row["GS_margin"] >= 0, "candidate GS criterion fails")


def validate_candidate_selection(multiplicities, degrees, stocks,
                                 inventory_by_degree, t, t_size,
                                 selected_ids=None):
    """Validate stock bounds and an explicit first-canonical selection."""
    require(len(multiplicities) == len(degrees) == len(stocks),
            "candidate vectors have inconsistent lengths")
    require(int(t) <= int(t_size),
            "candidate requests unavailable rational splitting places")
    chosen = {}
    for multiplicity, degree, stock in zip(multiplicities, degrees, stocks):
        multiplicity = int(multiplicity)
        degree = int(degree)
        stock = int(stock)
        require(0 <= multiplicity <= stock,
                f"candidate multiplicity unavailable at degree {degree}")
        available = inventory_by_degree[degree]
        require(stock == len(available),
                f"candidate stock disagrees at degree {degree}")
        first = [row["id"] for row in available[:multiplicity]]
        chosen[degree] = first
        if selected_ids is not None:
            require(selected_ids.get(str(degree), selected_ids.get(degree))
                    == first,
                    f"candidate does not select first canonical degree-{degree} places")
    flattened = [place_id for ids in chosen.values() for place_id in ids]
    require(len(flattened) == len(set(flattened)),
            "candidate selects a duplicate place")
    require(int(t) > 0, "candidate has empty splitting set")
    return chosen


def validate_candidate_record(candidate, degrees, stocks, inventory_by_degree,
                              t_size):
    require(candidate["genus"] == 343, "candidate genus is wrong")
    multiplicities = [int(value) for value in candidate["multiplicities"]]
    chosen = validate_candidate_selection(
        multiplicities, degrees, stocks, inventory_by_degree,
        candidate["t"], t_size, candidate.get("selected_place_ids"))
    row = exact_dm_row(list(zip(degrees, multiplicities)), candidate["t"],
                       candidate["genus"])
    for key in ("A", "C", "D", "GS_margin"):
        require(int(candidate[key]) == row[key],
                f"candidate arithmetic field {key} disagrees")
    require(Fraction(candidate["denominator"]) == row["denominator"],
            "candidate denominator disagrees")
    require(Fraction(candidate["bound"]) == row["ratio"],
            "candidate bound disagrees")
    validate_gs({"A": row["A"], "t": int(candidate["t"]),
                 "GS_margin": row["GS_margin"]})
    return row, chosen


def validate_reference_candidate(path, checked, t_size):
    result = json.loads(path.read_text())
    require(result["kind"] == "independent reference enumeration",
            "reference search has an unexpected kind")
    degrees = [int(value) for value in result["degrees"]]
    stocks = [int(value) for value in result["stocks"]]
    require(degrees == [5, 6, 8, 10, 12],
            "reference search degree support changed")
    require(stocks == [2, 16, 16, 64, 208],
            "reference search stock support changed")
    require(Fraction(result["fixed_cost_cap_exclusive"]) == Fraction(33751, 128),
            "reference fixed cost cap disagrees with baseline")
    require(int(result["visited_leaves"]) >= int(result["feasible_leaves"]) >= 0,
            "reference search leaf counters are inconsistent")
    require(int(result["pruned_subtrees"]) >= 0,
            "reference search pruned subtree count is negative")
    require(len(result["maximizers"]) == 1,
            "reference search does not have one recorded maximizer")
    candidate = dict(result["maximizers"][0])
    candidate["genus"] = 343
    by_degree = {degree: [row for d, row, *_ in checked if d == degree]
                 for degree in degrees}
    row, chosen = validate_candidate_record(candidate, degrees, stocks,
                                            by_degree, t_size)
    require(result["best_bound"] == candidate["bound"],
            "reference best bound disagrees with its maximizer")
    baseline = Fraction(24576, 77527)
    require(row["ratio"] > baseline,
            "reference candidate is not strictly above the historical baseline")

    feasible_t = []
    for t in range(1, int(t_size) + 1):
        trial = exact_dm_row(list(zip(degrees, candidate["multiplicities"])), t,
                             candidate["genus"])
        if t <= trial["A"] and trial["GS_margin"] >= 0:
            feasible_t.append(t)
    require(feasible_t and max(feasible_t) == int(t_size),
            "fixed-S feasible t maximum is not 192")
    return {
        "degrees": degrees,
        "stocks": stocks,
        "multiplicities": [int(value) for value in candidate["multiplicities"]],
        "selected_counts": {str(degree): len(chosen[degree])
                             for degree in degrees},
        "t": int(candidate["t"]),
        "A": row["A"],
        "C": row["C"],
        "D": row["D"],
        "GS_margin": row["GS_margin"],
        "mean_conductor_upper_bound": str(row["mean_conductor_upper_bound"]),
        "denominator": str(row["denominator"]),
        "bound": str(row["ratio"]),
        "baseline": str(baseline),
        "improvement_over_baseline": str(row["ratio"] - baseline),
        "feasible_t_count": len(feasible_t),
        "max_feasible_t": max(feasible_t),
        "visited_leaves": int(result["visited_leaves"]),
        "feasible_leaves": int(result["feasible_leaves"]),
        "pruned_subtrees": int(result["pruned_subtrees"]),
    }


def validate_search_best(best, label, expected_rows, t_size):
    """Recompute the exact row reported by a bounded search artifact."""
    require(best["status"] == "EXACT RATIONAL",
            f"{label}: search winner is not marked exact rational")
    require(int(best["genus"]) == 343 and int(best["q"]) == 2
            and int(best["p"]) == 2,
            f"{label}: field or genus changed")
    require(int(best["rational_places"]) == t_size
            and int(best["t"]) == t_size and bool(best["t_le_A"]),
            f"{label}: rational-place or t row changed")
    rows = [[int(value) for value in row] for row in best["rows"]]
    require(rows == expected_rows, f"{label}: reported rows changed")
    places = [(row[0], row[1]) for row in rows]
    row = exact_dm_row(places, t_size, 343)
    exact_fields = {
        "A": row["A"],
        "C": row["C"],
        "D": row["D"],
        "GS": row["GS_margin"],
        "GS_margin": row["GS_margin"],
        "local_dimension": row["A"],
        "twice_local_relation_cost": row["C"],
        "generator_lower_bound": row["D"],
    }
    for key, expected in exact_fields.items():
        if key in best:
            require(int(best[key]) == expected,
                    f"{label}: arithmetic field {key} disagrees")
    require(Fraction(best["average_conductor_degree_upper_bound"])
            == row["mean_conductor_upper_bound"],
            f"{label}: conductor average disagrees")
    require(Fraction(best["genus_denominator_upper_bound"])
            == row["denominator"], f"{label}: denominator disagrees")
    require(Fraction(best["ratio_lower_bound"]) == row["ratio"],
            f"{label}: ratio disagrees")
    if "ratio_from_units" in best:
        require(Fraction(best["ratio_from_units"]) == row["ratio"],
                f"{label}: unit ratio disagrees")
    require(int(best["relation_minus_generator_upper_bound"])
            == row["C"] // 2 + t_size - 1,
            f"{label}: relation-minus-generator bound disagrees")
    require(bool(best["inequality_passes"]) and bool(best["theorem_passes"])
            and not best.get("failure_reasons"),
            f"{label}: theorem or GS status failed")
    require(row["ratio"] > Fraction(24576, 77527),
            f"{label}: winner does not beat the historical baseline")
    return row


def validate_generic_search(path, candidate_summary, t_size):
    """Audit the worker search's winner without trusting its arithmetic."""
    result = json.loads(path.read_text())
    require(result["status"] == "EXACT FINITE INTEGER/RATIONAL SEARCH; GEOMETRY OBLIGATIONS OPEN",
            "generic search has an unexpected status")
    search_input = result["input"]
    require(int(search_input["genus"]) == 343 and int(search_input["q"]) == 2
            and int(search_input["rational_place_count_N"]) == t_size,
            "generic search input changed")
    expected_inventory = [[5, 2], [6, 16], [8, 16], [10, 64], [12, 208]]
    inventory = [[int(row["degree"]), int(row["available"])]
                 for row in search_input["nonrational_degrees_with_positive_counts"]]
    require(inventory == expected_inventory,
            "generic search inventory support changed")
    expected_rows = [[5, 2, 2], [6, 16, 2], [8, 16, 2],
                     [10, 2, 2], [12, 1, 2]]
    neighborhood = result["nonuniform_even_neighborhood"]["best"]
    automatic = result["nu2_search"]["automatic_best"]
    neighborhood_row = validate_search_best(
        neighborhood, "nonuniform search", expected_rows, t_size)
    automatic_row = validate_search_best(
        automatic, "nu2 search", expected_rows, t_size)
    require(neighborhood_row == automatic_row,
            "generic search winners disagree")
    multiplicity_vector = {
        str(degree): multiplicity
        for degree, multiplicity, _depth in expected_rows
    }
    require(automatic["multiplicity_vector"] == multiplicity_vector,
            "generic search multiplicity vector disagrees")
    require(int(result["nu2_search"]["depth"]) == 2,
            "generic search depth changed")
    require(Fraction(automatic["ratio_lower_bound"])
            == Fraction(candidate_summary["bound"]),
            "generic search winner disagrees with reference candidate")
    return {
        "status": "PASS",
        "winner": [5, 2, 6, 16, 8, 16, 10, 2, 12, 1],
        "bound": str(automatic_row["ratio"]),
        "depth": int(result["nu2_search"]["depth"]),
        "accepted_configurations": int(result["nu2_search"]["stats"]["accepted_configurations"]),
        "evaluated_configurations": int(result["nu2_search"]["stats"]["evaluated_configurations"]),
        "local_variants": int(result["nonuniform_even_neighborhood"]["stats"]["evaluated_variants"]),
    }


def validate_m2_certificate_data(cert, checked, candidate_summary):
    """Check the bound certificate against the independently checked places."""
    require(cert["id"] == "M2-K343-NU2-001", "M2 certificate id changed")
    require(cert["base_field"] == "F2" and cert["base_function_field"] == "k343",
            "M2 certificate base changed")
    require(cert["genus"] == 343 and cert["rational_place_count"] == 192,
            "M2 certificate genus or rational count changed")
    require(cert["rational_place_inventory"] == "curves/k343-places.json",
            "M2 certificate points at the wrong inventory")

    inventory = {row["id"]: row for _, row, *_ in checked}
    T = cert["selected_splitting_places"]
    require(T == [row["id"] for degree, row, *_ in checked if degree == 1],
            "M2 certificate T is not the complete canonical d=1 inventory")
    require(len(T) == cert["rational_place_count"] and len(set(T)) == len(T),
            "M2 certificate T has a duplicate or wrong size")

    allowed = cert["selected_allowed_ramification_places"]
    require(len(allowed) == 37, "M2 certificate S has the wrong size")
    allowed_ids = [row["id"] for row in allowed]
    require(len(set(allowed_ids)) == len(allowed_ids),
            "M2 certificate S has duplicate places")
    require(not (set(T) & set(allowed_ids)), "M2 certificate S overlaps T")
    require(all(place_id in inventory and inventory[place_id] == row
                for place_id, row in zip(allowed_ids, allowed)),
            "M2 certificate S row is not the checked inventory representative")

    degrees = candidate_summary["degrees"]
    multiplicities = candidate_summary["multiplicities"]
    expected_ids = []
    for degree, multiplicity in zip(degrees, multiplicities):
        rows = [row for d, row, *_ in checked if d == degree]
        expected_ids.extend(row["id"] for row in rows[:multiplicity])
    require(allowed_ids == expected_ids,
            "M2 certificate S does not use first canonical representatives")
    require([int(row["degree"]) for row in allowed]
            == [degree for degree, multiplicity in zip(degrees, multiplicities)
                for _ in range(multiplicity)],
            "M2 certificate S degree sequence disagrees")

    modulus = cert["modulus"]
    require([row["place_id"] for row in modulus] == allowed_ids,
            "M2 modulus places disagree with S")
    require(all(int(row["exponent"]) == 2 for row in modulus),
            "M2 modulus has a non-2 exponent")

    ramification = cert["ramification_indices"]
    k_over_h = ramification["k_over_H"]
    require(k_over_h["both_degree5_places"] == 32
            and k_over_h["residue_degrees"] == 1,
            "k/H ramification certificate changed")
    k_over_h_expected = {
        row["id"]: 2**int(row["degree"]) for row in allowed
    }
    k_over_k = ramification["K_over_k"]
    require(k_over_k["exact"] is None,
            "M2 certificate unexpectedly claims an exact K/k ramification")
    require(k_over_k["upper_bounds"] == k_over_h_expected,
            "M2 local inertia upper bounds disagree with degrees")
    extension = cert["extension_degree"]
    require(extension["k_over_H"] == 32 and extension["K_over_k"] is None,
            "M2 certificate does not preserve unknown ray degree")
    require(extension["K_over_k_lower_bound"] <= extension["K_over_k_upper_bound"],
            "M2 ray-degree bounds are inconsistent")

    ray_data = cert["ray_class_group_data"]
    require(ray_data["exact_order"] is None and ray_data["invariant_factors"] is None,
            "M2 certificate claims an uncomputed ray-group structure")
    require(ray_data["p_rank_lower_bound"] == 75,
            "M2 ray p-rank lower bound changed")

    row = exact_dm_row(list(zip(degrees, multiplicities)), 192, 343)
    parameters = cert["Golod_Shafarevich_parameters"]
    require(parameters["generator_lower_bound"] == row["D"]
            and int(parameters["local_dimension"]) == row["A"]
            and int(parameters["twice_local_relation_cost"]) == row["C"],
            "M2 GS parameter certificate changed")
    require(int(parameters["relation_minus_generator_upper_bound"])
            == row["C"] // 2 + 192 - 1,
            "M2 relation-minus-generator bound changed")
    inequality = cert["tower_infinitude_inequality"]
    require(inequality["integer_margin"] == row["GS_margin"]
            and inequality["comparison"] == "41 >= 0",
            "M2 GS inequality certificate changed")

    require(Fraction(cert["average_conductor_degree_upper_bound"])
            == row["mean_conductor_upper_bound"],
            "M2 conductor average changed")
    require(Fraction(cert["genus_denominator_upper_bound"])
            == row["denominator"],
            "M2 denominator changed")
    require(cert["rational_place_numerator"] == 192,
            "M2 rational numerator changed")
    require(Fraction(cert["resulting_Ihara_ratio_lower_bound"])
            == row["ratio"],
            "M2 bound changed")
    coding = cert["coding_consequence"]
    require(Fraction(coding["elementary_R_plus_delta_lower_bound"])
            == 1 - 1 / row["ratio"] and coding["positive_guarantee"] is False,
            "M2 coding consequence changed")
    require(Fraction(cert["improvement_over_DM"])
            == row["ratio"] - Fraction(24576, 77527),
            "M2 baseline improvement changed")
    return {"T_size": len(T), "S_size": len(allowed),
            "S_degrees": [degree for degree, _ in zip(degrees, multiplicities)
                          for _ in range(_)],
            "modulus_exponent": 2,
            "K_over_k_exact": "UNKNOWN",
            "K_over_k_upper_bounds": "PASS",
            "denominator": str(row["denominator"]),
            "bound": str(row["ratio"]),
            "coding_fraction": str(1 - 1 / row["ratio"])}


def negative_case_checks(main_checked, candidate_summary, t_size):
    """Mutate validated data and ensure the same predicates reject it."""
    degrees = candidate_summary["degrees"]
    stocks = candidate_summary["stocks"]
    multiplicities = candidate_summary["multiplicities"]
    by_degree = {degree: [row for d, row, *_ in main_checked if d == degree]
                 for degree in degrees}
    candidate = {
        "genus": 343, "multiplicities": multiplicities, "t": t_size,
        "A": candidate_summary["A"], "C": candidate_summary["C"],
        "D": candidate_summary["D"], "GS_margin": candidate_summary["GS_margin"],
        "denominator": candidate_summary["denominator"],
        "bound": candidate_summary["bound"],
    }

    def rejected(call):
        try:
            call()
        except (AssertionError, KeyError, ValueError):
            return True
        return False

    selected = validate_candidate_selection(multiplicities, degrees, stocks,
                                            by_degree, t_size, t_size, None)
    duplicate_ids = {str(degree): list(ids) for degree, ids in selected.items()}
    duplicate_ids[str(degrees[0])][-1] = duplicate_ids[str(degrees[0])][0]
    duplicate_ok = rejected(lambda: validate_candidate_selection(
        multiplicities, degrees, stocks, by_degree, t_size, t_size,
        duplicate_ids))

    bad_degree = copy.deepcopy(main_checked[0][1])
    bad_degree["degree"] = int(bad_degree["degree"]) + 1
    wrong_degree_ok = rejected(lambda: validate_entry(
        bad_degree, int(main_checked[0][0]), "negative-wrong-degree"))

    regular = next(row for degree, row, *_ in main_checked
                   if degree == 6 and row["chart"] == "regular")
    bad_chart = copy.deepcopy(regular)
    bad_chart["chart"] = "ramified"
    wrong_chart_ok = rejected(lambda: validate_entry(
        bad_chart, 6, "negative-wrong-chart"))

    bad_equation = copy.deepcopy(regular)
    bad_equation["representative"][1] ^= 1
    wrong_equation_ok = rejected(lambda: validate_entry(
        bad_equation, 6, "negative-wrong-equation"))

    bad_arithmetic = dict(candidate)
    bad_arithmetic["A"] += 1
    wrong_arithmetic_ok = rejected(lambda: validate_candidate_record(
        bad_arithmetic, degrees, stocks, by_degree, t_size))

    bad_gs = {"A": candidate["A"], "t": candidate["A"] + 1,
              "GS_margin": candidate["GS_margin"]}
    failed_gs_ok = rejected(lambda: validate_gs(bad_gs))

    unavailable = list(multiplicities)
    unavailable[0] = stocks[0] + 1
    unavailable_ok = rejected(lambda: validate_candidate_selection(
        unavailable, degrees, stocks, by_degree, t_size, t_size, None))
    statuses = {
        "duplicate_place": duplicate_ok,
        "wrong_degree": wrong_degree_ok,
        "wrong_chart": wrong_chart_ok,
        "wrong_equation": wrong_equation_ok,
        "changed_arithmetic": wrong_arithmetic_ok,
        "failed_GS": failed_gs_ok,
        "unavailable_multiplicity": unavailable_ok,
    }
    require(all(statuses.values()), "at least one adversarial case was accepted")
    return {name: "REJECTED" for name in statuses}


def certificate_negative_checks(cert, checked, candidate_summary):
    """Mutate actual M2 certificate fields and run the same certificate checks."""
    degrees = candidate_summary["degrees"]
    stocks = candidate_summary["stocks"]
    by_degree = {degree: [row for d, row, *_ in checked if d == degree]
                 for degree in degrees}

    def rejected(call):
        try:
            call()
        except (AssertionError, KeyError, ValueError):
            return True
        return False

    duplicate = copy.deepcopy(cert)
    duplicate["selected_allowed_ramification_places"][1]["id"] = \
        duplicate["selected_allowed_ramification_places"][0]["id"]
    duplicate_ok = rejected(lambda: validate_m2_certificate_data(
        duplicate, checked, candidate_summary))

    bad_modulus = copy.deepcopy(cert)
    bad_modulus["modulus"][0]["exponent"] = 3
    modulus_ok = rejected(lambda: validate_m2_certificate_data(
        bad_modulus, checked, candidate_summary))

    bad_ray_degree = copy.deepcopy(cert)
    bad_ray_degree["extension_degree"]["K_over_k"] = 1
    ray_degree_ok = rejected(lambda: validate_m2_certificate_data(
        bad_ray_degree, checked, candidate_summary))

    bad_denominator = copy.deepcopy(cert)
    bad_denominator["genus_denominator_upper_bound"] = "1/1"
    denominator_ok = rejected(lambda: validate_m2_certificate_data(
        bad_denominator, checked, candidate_summary))
    statuses = {"certificate_duplicate_S": duplicate_ok,
                "certificate_modulus": modulus_ok,
                "certificate_ray_degree": ray_degree_ok,
                "certificate_denominator": denominator_ok}
    require(all(statuses.values()),
            "at least one M2 certificate adversarial case was accepted")
    return {name: "REJECTED" for name in statuses}


def main():
    main_inventory, main_checked = validate_main_inventory()
    d12_inventory, d12_checked = validate_degree12_inventory()
    all_checked = main_checked + d12_checked
    lifting = validate_degree12_lifting()
    print("INDEPENDENT_CANDIDATE_INITIAL=PASS")
    print("MAIN_INVENTORY=" + json.dumps(main_inventory, sort_keys=True))
    print("DEGREE12_INVENTORY=" + json.dumps(d12_inventory, sort_keys=True))
    print("DEGREE12_LIFTING=" + json.dumps(lifting, sort_keys=True))
    reference_path = ROOT / "results/reference-nu2-search.json"
    candidate = None
    if reference_path.exists():
        candidate = validate_reference_candidate(reference_path, all_checked, 192)
        negatives = negative_case_checks(all_checked, candidate, 192)
        print("REFERENCE_CANDIDATE=" + json.dumps(candidate, sort_keys=True))
        print("CANDIDATE_NEGATIVE_CASES=" + json.dumps(negatives, sort_keys=True))
        print("CANDIDATE_SEARCH=REFERENCE_PASS")
    else:
        print("REFERENCE_CANDIDATE=WAITING results/reference-nu2-search.json unavailable")

    certificate_path = ROOT / "certificates/m2-tower.json"
    if certificate_path.exists():
        require(candidate is not None,
                "M2 certificate requires the independently checked candidate row")
        certificate = json.loads(certificate_path.read_text())
        certificate_summary = validate_m2_certificate_data(
            certificate, all_checked, candidate)
        require(certificate_summary["bound"] == candidate["bound"],
                "M2 certificate bound differs from reference candidate")
        certificate_negatives = certificate_negative_checks(
            certificate, all_checked, candidate)
        print("M2_CERTIFICATE=" + json.dumps(certificate_summary, sort_keys=True))
        print("M2_CERTIFICATE_NEGATIVE_CASES="
              + json.dumps(certificate_negatives, sort_keys=True))
        print("M2_CERTIFICATE=PASS")
    else:
        print("M2_CERTIFICATE=WAITING certificates/m2-tower.json unavailable")

    generic_search = ROOT / "results/m2-search.json"
    if generic_search.exists():
        generic_summary = validate_generic_search(
            generic_search, candidate, 192)
        print("GENERIC_SEARCH=" + json.dumps(generic_summary, sort_keys=True))
    else:
        print("GENERIC_SEARCH=WAITING results/m2-search.json unavailable")


if __name__ == "__main__":
    main()
