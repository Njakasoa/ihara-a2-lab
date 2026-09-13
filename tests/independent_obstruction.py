#!/usr/bin/env python3
"""Independent exact audit of the fixed-k343 all-degree nu=2 obstruction.

This checker uses only Python ``Fraction`` arithmetic.  It derives the global
degree and cost caps, checks the continuous lower bound on ``C``, and then
enumerates the seven surviving low-degree deficit cases together with all
admissible high-degree partitions.  It does not import ``src`` or the DP
implementation.  Degrees 12--47 are hypothetical relaxed stocks; their
enumeration is an arithmetic superset, not a place-existence claim.
"""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "results/all-degree-relaxation.json"

GENUS = 343
RATIONAL_PLACES = 192
BASELINE = Fraction(196608, 620201)
HISTORICAL_DM = Fraction(24576, 77527)
SPECIAL_REBATE = Fraction(37, 16)
LOW_STOCKS = {2: 0, 3: 0, 4: 0, 5: 2, 6: 16, 7: 0,
              8: 16, 9: 0, 10: 64, 11: 0}
LOW_DEGREES = (5, 6, 8)
MAX_DEGREE = 47
A_CAP_EXPECTED = 266
C_CAP_EXPECTED = 2280


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def t_minimum(a_value: int, baseline: Fraction = BASELINE) -> int:
    lower_cost = max(
        Fraction(0),
        Fraction(a_value, 1) - SPECIAL_REBATE - Fraction(a_value, 1024),
    )
    return floor_fraction(baseline * (GENUS - 1 + lower_cost)) + 1


def c_minimum(a_value: int) -> int:
    """Continuous greedy lower bound using the certified low stocks.

    A unit of A at degrees 5, 6, 8, and >=10 costs respectively 6, 7, 9,
    and at least 11 units of C.  The capacities in A are 10, 96, and 128.
    """
    if a_value <= 10:
        return 6 * a_value
    if a_value <= 106:
        return 7 * a_value - 10
    if a_value <= 234:
        return 9 * a_value - 222
    return 11 * a_value - 690


def c_maximum(a_value: int, t_value: int) -> int:
    """Largest integer C allowed by the GS square inequality."""
    d_value = 1 + a_value - t_value
    return (d_value * d_value - 4 * a_value) // 2


def derive_caps() -> dict:
    strict_cost_cap = (
        Fraction(RATIONAL_PLACES, 1) / BASELINE - (GENUS - 1)
    )
    # A - 37/16 - A/1024 < strict_cost_cap, so A is strictly below this
    # rational endpoint.  Taking the integer predecessor is exact.
    a_endpoint = (strict_cost_cap + SPECIAL_REBATE) * Fraction(1024, 1023)
    a_cap = (a_endpoint.numerator - 1) // a_endpoint.denominator
    require(a_cap == A_CAP_EXPECTED, "derived A cap changed")

    t_minimums = [t_minimum(a_value) for a_value in range(a_cap + 1)]
    valid = []
    survivors = []
    for a_value, t_value in enumerate(t_minimums):
        # GS implies t <= A in the theorem's admissible range.  This also
        # keeps D=1+A-t on its decreasing branch when t is increased.
        if not (1 <= t_value <= RATIONAL_PLACES and t_value <= a_value):
            continue
        c_limit = c_maximum(a_value, t_value)
        row = {
            "A": a_value,
            "t_min": t_value,
            "C_min": c_minimum(a_value),
            "C_max": c_limit,
        }
        valid.append(row)
        if row["C_min"] <= c_limit:
            survivors.append(row)
    require(len(survivors) == 1 and survivors[0] == {
        "A": 266, "t_min": 192, "C_min": 2236, "C_max": 2280,
    }, "continuous C lower bound has an unexpected survivor")
    global_c_cap = max(row["C_max"] for row in valid)
    require(global_c_cap == C_CAP_EXPECTED,
            "derived global C cap changed")
    cap_rows = [row for row in valid if row["C_max"] == global_c_cap]
    require(cap_rows == [{
        "A": 266, "t_min": 192, "C_min": 2236, "C_max": 2280,
    }], "global C cap is attained at an unexpected row")
    degree_cap = max(
        degree for degree in range(2, 100)
        if degree * (degree + 1) <= global_c_cap
    )
    require(degree_cap == MAX_DEGREE and 48 * 49 > global_c_cap,
            "derived degree cap changed")
    return {
        "strict_cost_cap": strict_cost_cap,
        "a_endpoint": a_endpoint,
        "a_cap": a_cap,
        "t_minimums": t_minimums,
        "valid_rows": valid,
        "continuous_survivors": survivors,
        "global_c_cap": global_c_cap,
        "degree_cap": degree_cap,
    }


def score(rows: list[tuple[int, int]], t_value: int = RATIONAL_PLACES) -> dict:
    a_value = sum(degree * multiplicity for degree, multiplicity in rows)
    c_value = sum(
        degree * (degree + 1) * multiplicity
        for degree, multiplicity in rows
    )
    rebate = sum(
        (Fraction(degree * multiplicity, 2**degree)
         for degree, multiplicity in rows),
        Fraction(0),
    )
    cost = Fraction(a_value, 1) - rebate
    denominator = Fraction(GENUS - 1, 1) + cost
    d_value = 1 + a_value - t_value
    margin = d_value * d_value - 2 * c_value - 4 * a_value
    return {
        "A": a_value,
        "C": c_value,
        "D": d_value,
        "GS_margin": margin,
        "rebate": rebate,
        "cost": cost,
        "denominator": denominator,
        "ratio": Fraction(t_value, 1) / denominator,
        "t": t_value,
    }


def high_stock(degree: int) -> int:
    require(degree == 10 or degree >= 12,
            "high stock requested outside the relaxed support")
    # Degree 10 uses the certified stock.  The A cap itself bounds it by 26
    # in every enumerated branch.  Degrees >=12 receive hypothetical stocks.
    return LOW_STOCKS[10] if degree == 10 else A_CAP_EXPECTED // degree


def enumerate_high_partitions(residual_a: int, c_budget: int) -> dict:
    """Enumerate residual A using degree 10 and arbitrary degrees 12..47."""
    degrees = (10,) + tuple(range(12, MAX_DEGREE + 1))
    partitions: list[tuple[int, ...]] = []
    nodes = 0
    pruned = 0

    def visit(index: int, remaining_a: int, used_c: int,
              witness: list[int]) -> None:
        nonlocal nodes, pruned
        nodes += 1
        if index == len(degrees):
            if remaining_a == 0:
                partitions.append(tuple(witness))
            else:
                pruned += 1
            return

        degree = degrees[index]
        c_term = degree * (degree + 1)
        maximum = min(
            high_stock(degree),
            remaining_a // degree,
            (c_budget - used_c) // c_term,
        )
        if maximum < 0:
            pruned += 1
            return
        if index + 1 < len(degrees):
            minimum_remaining_coefficient = degrees[index + 1] + 1
        else:
            minimum_remaining_coefficient = 0
        for multiplicity in range(maximum + 1):
            next_a = remaining_a - multiplicity * degree
            next_c = used_c + multiplicity * c_term
            if index + 1 == len(degrees):
                if next_a != 0:
                    pruned += 1
                    continue
            elif (next_c + minimum_remaining_coefficient * next_a
                  > c_budget):
                # Every remaining unit of A has degree at least the next
                # degree.  This is a lower bound, so the prune is sound.
                pruned += 1
                continue
            witness.append(multiplicity)
            visit(index + 1, next_a, next_c, witness)
            witness.pop()

    require(residual_a >= 0 and c_budget >= 0,
            "negative residual partition input")
    visit(0, residual_a, 0, [])
    return {
        "degrees": degrees,
        "partitions": partitions,
        "nodes": nodes,
        "pruned": pruned,
    }


def enumerate_survivors(caps: dict) -> dict:
    """Enumerate the A=266 cases left by the continuous test."""
    require(caps["continuous_survivors"] == [{
        "A": 266, "t_min": 192, "C_min": 2236, "C_max": 2280,
    }], "enumeration called before the unique continuous survivor")
    low_cases = []
    candidates = []
    low_total = 0
    low_pruned = 0
    partition_nodes = 0
    partition_pruned = 0
    for n5 in range(LOW_STOCKS[5] + 1):
        for n6 in range(LOW_STOCKS[6] + 1):
            for n8 in range(LOW_STOCKS[8] + 1):
                low_total += 1
                low_a = 5 * n5 + 6 * n6 + 8 * n8
                low_c = 30 * n5 + 42 * n6 + 72 * n8
                residual_a = A_CAP_EXPECTED - low_a
                c_budget = C_CAP_EXPECTED - low_c
                r5 = LOW_STOCKS[5] - n5
                r6 = LOW_STOCKS[6] - n6
                r8 = LOW_STOCKS[8] - n8
                deficit_weight = 25 * r5 + 24 * r6 + 16 * r8
                # The continuous high-degree lower bound is 11*residual_a.
                # Equivalently, total C is at least 2236 plus this deficit.
                if residual_a < 0 or c_budget < 0 or deficit_weight > 44:
                    low_pruned += 1
                    continue
                low_cases.append({
                    "n5": n5,
                    "n6": n6,
                    "n8": n8,
                    "r5": r5,
                    "r6": r6,
                    "r8": r8,
                    "deficit_weight": deficit_weight,
                    "residual_A": residual_a,
                    "C_budget": c_budget,
                })
                result = enumerate_high_partitions(residual_a, c_budget)
                partition_nodes += result["nodes"]
                partition_pruned += result["pruned"]
                for witness in result["partitions"]:
                    counts = {5: n5, 6: n6, 8: n8}
                    for degree, multiplicity in zip(result["degrees"], witness):
                        if multiplicity:
                            counts[degree] = multiplicity
                    rows = sorted(counts.items())
                    row_score = score(rows)
                    require(row_score["A"] == A_CAP_EXPECTED,
                            "partition changed the A cap row")
                    require(row_score["C"] <= C_CAP_EXPECTED,
                            "partition exceeded the global C cap")
                    require(row_score["GS_margin"] >= 0,
                            "partition passed C cap but failed GS")
                    candidates.append({
                        "rows": rows,
                        "score": row_score,
                        "low_case": low_cases[-1],
                        "high_witness": witness,
                    })

    require(low_total == 3 * 17 * 17, "low-degree enumeration changed")
    require(len(low_cases) == 7 and low_pruned == low_total - 7,
            "deficit lower bound did not leave seven cases")
    require(len(candidates) == 2,
            "unexpected number of admissible all-degree partitions")
    expected_rows = {
        ((5, 2), (6, 16), (8, 15), (10, 4)),
        ((5, 2), (6, 16), (8, 16), (10, 2), (12, 1)),
    }
    require({tuple(item["rows"]) for item in candidates} == expected_rows,
            "enumerated partition witnesses changed")
    ratios = [item["score"]["ratio"] for item in candidates]
    strict = [ratio for ratio in ratios if ratio > BASELINE]
    equals = [ratio for ratio in ratios if ratio == BASELINE]
    require(HISTORICAL_DM in ratios
            and len(strict) == 0 and len(equals) == 1,
            "relaxed enumeration found an unexpected improvement")
    maximum = max(ratios)
    require(maximum == BASELINE,
            "relaxed enumeration maximum is not the incumbent fraction")
    return {
        "low_cases": low_cases,
        "low_total": low_total,
        "low_pruned": low_pruned,
        "partition_nodes": partition_nodes,
        "partition_pruned": partition_pruned,
        "candidates": candidates,
        "candidate_count": len(candidates),
        "strict_improvement_count": len(strict),
        "equal_incumbent_count": len(equals),
        "maximum_ratio": maximum,
    }


def vector_from_rows(rows: list[tuple[int, int]]) -> dict[str, int]:
    values = {str(degree): 0 for degree in range(2, MAX_DEGREE + 1)}
    for degree, multiplicity in rows:
        values[str(degree)] = multiplicity
    return values


def rows_from_json(rows: object) -> list[tuple[int, int, int]]:
    require(isinstance(rows, list), "artifact rows are not a list")
    output = []
    for row in rows:
        require(isinstance(row, list) and len(row) == 3,
                "artifact row is malformed")
        output.append(tuple(int(value) for value in row))
    return output


def validate_best_record(best: dict, enum: dict) -> None:
    expected = next(
        item for item in enum["candidates"]
        if item["score"]["ratio"] == enum["maximum_ratio"]
    )
    row = expected["score"]
    require(best["status"] == "EXACT RATIONAL",
            "artifact winner is not exact rational")
    require(int(best["genus"]) == GENUS and int(best["p"]) == 2
            and int(best["q"]) == 2,
            "artifact winner field or genus changed")
    require(rows_from_json(best["rows"]) == [
        (degree, multiplicity, 2)
        for degree, multiplicity in expected["rows"]
    ], "artifact winner rows changed")
    require(best["multiplicity_vector"] == vector_from_rows(expected["rows"]),
            "artifact winner vector changed")
    require([int(value) for value in best["witness"]] == [
        vector_from_rows(expected["rows"])[str(degree)]
        for degree in range(2, MAX_DEGREE + 1)
    ], "artifact winner witness changed")
    for key in ("A", "C", "D", "GS", "GS_margin", "local_dimension",
                "twice_local_relation_cost", "generator_lower_bound"):
        expected_key = {
            "GS": "GS_margin",
            "GS_margin": "GS_margin",
            "local_dimension": "A",
            "twice_local_relation_cost": "C",
            "generator_lower_bound": "D",
        }.get(key, key)
        require(int(best[key]) == row[expected_key],
                f"artifact winner arithmetic field {key} changed")
    require(Fraction(best["average_conductor_degree_upper_bound"])
            == 2 * row["cost"], "artifact conductor average changed")
    require(Fraction(best["conductor_average"]) == 2 * row["cost"],
            "artifact conductor average alias changed")
    require(Fraction(best["conductor_cost"]) == row["cost"],
            "artifact conductor cost changed")
    require(Fraction(best["genus_denominator_upper_bound"])
            == row["denominator"], "artifact denominator changed")
    require(Fraction(best["ratio_lower_bound"]) == row["ratio"],
            "artifact ratio changed")
    require(int(best["rational_places"]) == RATIONAL_PLACES
            and int(best["t"]) == RATIONAL_PLACES
            and bool(best["t_le_A"])
            and bool(best["inequality_passes"])
            and bool(best["theorem_passes"])
            and not best["failure_reasons"],
            "artifact winner theorem status changed")
    require(int(best["constant_degree"]) == 1
            and int(best["relation_minus_generator_upper_bound"])
            == row["C"] // 2 + RATIONAL_PLACES - 1,
            "artifact winner relation bound changed")


def validate_artifact(payload: dict, caps: dict, enum: dict) -> None:
    require(payload["experiment"] ==
            "M2 relaxed all-degree exact compressed nu=2 search",
            "artifact experiment changed")
    require(payload["status"] ==
            "EXACT FINITE RELAXED DP; HYPOTHETICAL STOCKS; GEOMETRY OBLIGATIONS OPEN",
            "artifact status changed")
    input_data = payload["input"]
    require(input_data["base_field"] == "F_2"
            and int(input_data["q"]) == 2
            and int(input_data["genus"]) == GENUS
            and int(input_data["rational_place_count_N"]) == RATIONAL_PLACES
            and int(input_data["maximum_degree"]) == MAX_DEGREE,
            "artifact input changed")
    prefix = input_data["certified_prefix"]
    require(prefix["degrees"] == list(range(2, 12))
            and prefix["stocks"] == [LOW_STOCKS[d] for d in range(2, 12)],
            "artifact certified prefix changed")
    require(input_data["relaxed_degrees"] == list(range(12, 48))
            and input_data["relaxed_stock_rule"] == "floor(266/d), independent of actual curve inventory",
            "artifact relaxed degree support changed")
    relaxation = payload["relaxation"]
    require(relaxation["actual_inventory_not_called_for_degrees_12_to_47"]
            is True
            and relaxation["low_degree_rule"] == "use certified B_2..B_11 exactly"
            and relaxation["high_degree_rule"] ==
            "grant floor(266/d) hypothetical places for every d=12..47",
            "artifact relaxation scope changed")

    caps_data = payload["historical_and_caps"]
    require(Fraction(caps_data["baseline_ratio"]) == BASELINE
            and Fraction(caps_data["strict_cost_cap"])
            == caps["strict_cost_cap"]
            and Fraction(caps_data["special_rebate_bound"])
            == SPECIAL_REBATE
            and int(caps_data["a_cap"]) == caps["a_cap"]
            and Fraction(caps_data["a_strict_upper_endpoint"])
            == caps["a_endpoint"]
            and int(caps_data["global_c_cap"]) == caps["global_c_cap"],
            "artifact exact cap fields changed")
    require(caps_data["t_minimums"] == caps["t_minimums"],
            "artifact t minimum table changed")
    require(caps_data["global_c_cap_attaining_A"] == [{
        "A": 266, "C_limit": 2280, "D_at_t_min": 75, "t_min": 192,
    }], "artifact C-cap witness changed")
    require(caps_data["degree_cap_from_C"] ==
            "f(f+1)<=2280 implies f<=47",
            "artifact degree cap derivation changed")

    validate_best_record(payload["automatic_best"], enum)
    dp_best = payload["dp_best_state"]
    expected = next(item for item in enum["candidates"]
                    if item["score"]["ratio"] == enum["maximum_ratio"])
    row = expected["score"]
    expected_vector = vector_from_rows(expected["rows"])
    expected_witness = [expected_vector[str(d)]
                        for d in range(2, MAX_DEGREE + 1)]
    require(int(dp_best["A"]) == row["A"]
            and int(dp_best["C"]) == row["C"]
            and dp_best["multiplicity_vector"] == expected_vector
            and [int(value) for value in dp_best["witness"]]
            == expected_witness
            and int(dp_best["t"]) == RATIONAL_PLACES
            and int(dp_best["t_minimum"]) == RATIONAL_PLACES,
            "artifact DP winner state changed")
    require(Fraction(dp_best["cost"]) == row["cost"]
            and Fraction(dp_best["rebate"]) == row["rebate"]
            and Fraction(dp_best["ratio"]) == row["ratio"]
            and int(dp_best["rebate_scale"]) == 1 << MAX_DEGREE
            and int(dp_best["rebate_units"])
            == row["rebate"] * (1 << MAX_DEGREE),
            "artifact DP exact rebate state changed")
    conclusion = payload["conclusion"]
    require(conclusion["best_equals_incumbent"] is True
            and conclusion["strict_improvement_found_in_relaxed_box"] is False
            and int(conclusion["strict_improvements_count"]) == 0
            and Fraction(conclusion["best_ratio"]) == BASELINE,
            "artifact obstruction conclusion changed")
    dp_stats = payload["dp"]["stats"]
    require(int(dp_stats["strict_improvements_over_baseline"]) == 0,
            "artifact DP strict-improvement count changed")


def negative_certificate_checks(payload: dict, caps: dict, enum: dict) -> dict:
    """Ensure meaningful cap and result mutations are rejected."""
    def rejected(mutated: dict) -> bool:
        try:
            validate_artifact(mutated, caps, enum)
        except (AssertionError, KeyError, TypeError, ValueError):
            return True
        return False

    bad_a = copy.deepcopy(payload)
    bad_a["historical_and_caps"]["a_cap"] = 267
    bad_c = copy.deepcopy(payload)
    bad_c["historical_and_caps"]["global_c_cap"] = 2281
    bad_degree = copy.deepcopy(payload)
    bad_degree["input"]["maximum_degree"] = 46
    bad_ratio = copy.deepcopy(payload)
    bad_ratio["automatic_best"]["ratio_lower_bound"] = "1/1"
    bad_conclusion = copy.deepcopy(payload)
    bad_conclusion["conclusion"]["strict_improvement_found_in_relaxed_box"] = True
    bad_rule = copy.deepcopy(payload)
    bad_rule["input"]["relaxed_stock_rule"] = "certified places"
    statuses = {
        "changed_A_cap": rejected(bad_a),
        "changed_C_cap": rejected(bad_c),
        "changed_degree_cap": rejected(bad_degree),
        "changed_result_ratio": rejected(bad_ratio),
        "changed_conclusion": rejected(bad_conclusion),
        "changed_relaxation_rule": rejected(bad_rule),
    }
    require(all(statuses.values()), "an obstruction mutation was accepted")
    return {name: "REJECTED" for name in statuses}


def main() -> None:
    caps = derive_caps()
    enum = enumerate_survivors(caps)
    require(ARTIFACT.exists(), "results/all-degree-relaxation.json is missing")
    payload = json.loads(ARTIFACT.read_text())
    validate_artifact(payload, caps, enum)
    negatives = negative_certificate_checks(payload, caps, enum)
    candidate_rows = [
        {"rows": [[degree, multiplicity] for degree, multiplicity in item["rows"]],
         "ratio": str(item["score"]["ratio"]),
         "A": item["score"]["A"],
         "C": item["score"]["C"],
         "cost": str(item["score"]["cost"]),
         "GS_margin": item["score"]["GS_margin"]}
        for item in enum["candidates"]
    ]
    print("INDEPENDENT_OBSTRUCTION=PASS")
    print("CAPS=" + json.dumps({
        "strict_cost_cap": str(caps["strict_cost_cap"]),
        "A_endpoint": str(caps["a_endpoint"]),
        "A_cap": caps["a_cap"],
        "valid_A_rows": len(caps["valid_rows"]),
        "continuous_survivors": caps["continuous_survivors"],
        "C_cap": caps["global_c_cap"],
        "degree_cap": caps["degree_cap"],
    }, sort_keys=True))
    print("ENUMERATION=" + json.dumps({
        "low_cases": len(enum["low_cases"]),
        "low_total": enum["low_total"],
        "low_pruned": enum["low_pruned"],
        "partition_nodes": enum["partition_nodes"],
        "partition_pruned": enum["partition_pruned"],
        "candidate_count": enum["candidate_count"],
        "strict_improvement_count": enum["strict_improvement_count"],
        "equal_incumbent_count": enum["equal_incumbent_count"],
        "maximum_ratio": str(enum["maximum_ratio"]),
        "candidates": candidate_rows,
    }, sort_keys=True))
    print("CERTIFICATE_NEGATIVE_CASES="
          + json.dumps(negatives, sort_keys=True))
    print("CERTIFICATE=PASS")


if __name__ == "__main__":
    main()
