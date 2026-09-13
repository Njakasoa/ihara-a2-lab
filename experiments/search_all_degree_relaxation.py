#!/usr/bin/env python3
"""Relaxed all-degree binary ``nu=2`` obstruction for the fixed k343 data.

This experiment is deliberately separate from the certified degree<=30
search.  It uses the certified place counts only for degrees 2 through 11,
including their zero entries.  For every degree 12 through 47 it supplies the
hypothetical stock ``floor(266/d)``, whether or not the supplied curve
inventory contains that many places.  Thus the search is an arithmetic
relaxation that contains every actual configuration capable of beating the
incumbent; it is not an inventory of newly certified places.

The raw product of these hypothetical stocks is too large for vector DFS.  A
dynamic program stores states ``(A,C)`` and, for each state, the maximum exact
rebate ``sum(m*d/2**d)`` together with a witness.  At fixed ``(A,C)`` this is
the minimum possible conductor cost and is therefore the only witness that
can improve the rational theorem score.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from math import prod
from pathlib import Path
from typing import Mapping


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from theorem_search import evaluate_binary, optimal_t  # noqa: E402


BASELINE = Fraction(196608, 620201)
GENUS = 343
RATIONAL_PLACES = 192
MAX_DEGREE = 47
CERTIFIED_LOW_MAX = 11
REBATE_SCALE = 1 << MAX_DEGREE
SPECIAL_REBATE = Fraction(37, 16)


def _decimal(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 30
        return format(Decimal(value.numerator) / Decimal(value.denominator), ".20f")


def _jsonable(value: object) -> object:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _inventory_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _certified_low_stocks(path: Path) -> tuple[int, ...]:
    """Read B_2,...,B_11, preserving zeros from the certified inventory."""

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, Mapping) or "place_counts" not in payload:
        raise ValueError("certified inventory needs place_counts")
    counts = payload["place_counts"]
    if not isinstance(counts, list) or len(counts) < CERTIFIED_LOW_MAX:
        raise ValueError("certified inventory has no complete B_2..B_11 prefix")
    values = []
    for degree in range(2, CERTIFIED_LOW_MAX + 1):
        value = counts[degree - 1]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"invalid certified count B_{degree}")
        values.append(value)
    expected = (0, 0, 0, 2, 16, 0, 16, 0, 64, 0)
    if tuple(values) != expected:
        raise ValueError("the fixed k343 rebate bound requires its certified B2..B11 prefix")
    return tuple(values)


def derive_a_cap(cost_cap: Fraction) -> tuple[int, Fraction]:
    """Derive A<endpoint from the exact global rebate upper bound."""

    endpoint = (cost_cap + SPECIAL_REBATE) * Fraction(1024, 1023)
    cap = (endpoint.numerator - 1) // endpoint.denominator
    return cap, endpoint


def derive_t_minimums(a_cap: int) -> tuple[int, ...]:
    """Necessary t lower bounds for a strict improvement at each A."""

    values = []
    for a_value in range(a_cap + 1):
        lower_cost = max(
            Fraction(0),
            Fraction(a_value, 1) - SPECIAL_REBATE - Fraction(a_value, 1024),
        )
        values.append(
            _floor_fraction(BASELINE * (GENUS - 1 + lower_cost)) + 1
        )
    return tuple(values)


def derive_global_c_cap(t_minimums: tuple[int, ...], a_cap: int) -> tuple[int, list[dict]]:
    """Compute the single C cap valid for every possible final A."""

    rows = []
    for a_value in range(a_cap + 1):
        t_min = t_minimums[a_value]
        if t_min < 1 or t_min > RATIONAL_PLACES or t_min > a_value:
            continue
        d_upper = 1 + a_value - t_min
        c_limit = (d_upper * d_upper - 4 * a_value) // 2
        if c_limit < 0:
            continue
        rows.append({
            "A": a_value,
            "t_min": t_min,
            "D_at_t_min": d_upper,
            "C_limit": c_limit,
        })
    if not rows:
        return -1, rows
    return max(row["C_limit"] for row in rows), rows


def _candidate_json(candidate: Mapping[str, object] | None) -> object:
    if candidate is None:
        return None
    output = _jsonable(candidate)
    assert isinstance(output, dict)
    for key in (
        "conductor_average",
        "conductor_cost",
        "genus_denominator_upper_bound",
        "ratio_lower_bound",
    ):
        value = candidate.get(key)
        if isinstance(value, Fraction):
            output[f"{key}_decimal"] = _decimal(value)
    return output


def run_search(inventory_path: Path) -> dict:
    """Run the relaxed degree 2..47 DP and audit its best witness."""

    low_stocks = _certified_low_stocks(inventory_path)
    cost_cap = Fraction(RATIONAL_PLACES, 1) / BASELINE - (GENUS - 1)
    a_cap, a_endpoint = derive_a_cap(cost_cap)
    degrees = tuple(range(2, MAX_DEGREE + 1))
    stocks = tuple(
        low_stocks[degree - 2] if degree <= CERTIFIED_LOW_MAX else a_cap // degree
        for degree in degrees
    )
    bounded_counts = tuple(
        min(stock, a_cap // degree) for degree, stock in zip(degrees, stocks)
    )

    t_minimums = derive_t_minimums(a_cap)
    c_cap, c_cap_rows = derive_global_c_cap(t_minimums, a_cap)

    raw_bounded_vectors = prod(count + 1 for count in bounded_counts)
    rebate_terms = tuple(
        degree * (1 << (MAX_DEGREE - degree)) for degree in degrees
    )
    c_terms = tuple(degree * (degree + 1) for degree in degrees)

    # State value: (maximum rebate in 2**(-47) units, one witness tuple).
    states: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {
        (0, 0): (0, ())
    }
    states_per_degree = [{"degree": None, "states": 1}]
    transition_attempts = 0
    globally_capped_choices = 0
    rebate_dominated_transitions = 0
    witness_tie_replacements = 0

    for degree, count, rebate_term, c_term in zip(
        degrees, bounded_counts, rebate_terms, c_terms
    ):
        next_states: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
        for (a_value, c_value), (rebate, witness) in states.items():
            max_by_a = (a_cap - a_value) // degree
            max_by_c = (c_cap - c_value) // c_term
            max_multiplicity = min(count, max_by_a, max_by_c)
            transition_attempts += max_multiplicity + 1
            if max_multiplicity < count:
                globally_capped_choices += count - max_multiplicity
            for multiplicity in range(max_multiplicity + 1):
                key = (
                    a_value + multiplicity * degree,
                    c_value + multiplicity * c_term,
                )
                value = (
                    rebate + multiplicity * rebate_term,
                    witness + (multiplicity,),
                )
                old = next_states.get(key)
                if old is None or value[0] > old[0]:
                    next_states[key] = value
                    if old is not None:
                        rebate_dominated_transitions += 1
                elif old is not None and value[0] == old[0] and value[1] < old[1]:
                    next_states[key] = value
                    witness_tie_replacements += 1
                else:
                    rebate_dominated_transitions += 1
        states = next_states
        states_per_degree.append({
            "degree": degree,
            "stock": stocks[degree - 2],
            "bounded_stock": bounded_counts[degree - 2],
            "states": len(states),
        })

    final_states_passing_t_minimum = 0
    t_minimum_failures = 0
    gs_or_t_upper_failures = 0
    exact_nonimprovements = 0
    strict_improvements = 0
    best_state: dict | None = None
    best_ratio: Fraction | None = None
    best_key: tuple[int, int] | None = None
    for (a_value, c_value), (rebate, witness) in states.items():
        t_min = t_minimums[a_value]
        if t_min < 1 or t_min > RATIONAL_PLACES or t_min > a_value:
            t_minimum_failures += 1
            continue
        final_states_passing_t_minimum += 1
        t_upper = optimal_t(a_value, c_value, RATIONAL_PLACES)
        if t_upper < t_min:
            gs_or_t_upper_failures += 1
            continue
        cost = Fraction(a_value * REBATE_SCALE - rebate, REBATE_SCALE)
        ratio = Fraction(t_upper, 1) / (GENUS - 1 + cost)
        if ratio > BASELINE:
            strict_improvements += 1
        else:
            exact_nonimprovements += 1
        key = (a_value, c_value)
        if (
            best_ratio is None
            or ratio > best_ratio
            or (ratio == best_ratio and key < best_key)
        ):
            best_ratio = ratio
            best_key = key
            best_state = {
                "A": a_value,
                "C": c_value,
                "rebate_units": rebate,
                "rebate_scale": REBATE_SCALE,
                "rebate": Fraction(rebate, REBATE_SCALE),
                "cost": cost,
                "t": t_upper,
                "t_minimum": t_min,
                "multiplicity_vector": {
                    str(degree): multiplicity
                    for degree, multiplicity in zip(degrees, witness)
                },
                "witness": witness,
                "ratio": ratio,
            }

    independent_evaluation = None
    if best_state is not None:
        rows = tuple(
            (degree, multiplicity, 2)
            for degree, multiplicity in zip(degrees, best_state["witness"])
            if multiplicity
        )
        independent_evaluation = evaluate_binary(
            GENUS,
            optimal_t(best_state["A"], best_state["C"], RATIONAL_PLACES),
            rows,
            rational_places=RATIONAL_PLACES,
        )
        if independent_evaluation["ratio_lower_bound"] != best_state["ratio"]:
            raise AssertionError("DP winner disagrees with theorem evaluator")
        if independent_evaluation["A"] != best_state["A"] or independent_evaluation["C"] != best_state["C"]:
            raise AssertionError("DP witness disagrees with theorem evaluator")
        independent_evaluation["multiplicity_vector"] = best_state[
            "multiplicity_vector"
        ]
        independent_evaluation["witness"] = best_state["witness"]
    stats = {
        "raw_bounded_vectors_not_enumerated": raw_bounded_vectors,
        "bounded_counts": {
            str(degree): count
            for degree, count in zip(degrees, bounded_counts)
        },
        "dp_final_states": len(states),
        "final_states_passing_t_minimum": final_states_passing_t_minimum,
        "t_minimum_failures": t_minimum_failures,
        "gs_or_t_upper_failures": gs_or_t_upper_failures,
        "exact_nonimprovements_after_caps": exact_nonimprovements,
        "strict_improvements_over_baseline": strict_improvements,
        "transition_attempts": transition_attempts,
        "globally_capped_transition_choices": globally_capped_choices,
        "rebate_dominated_transitions": rebate_dominated_transitions,
        "witness_tie_replacements": witness_tie_replacements,
    }
    relative_inventory = (
        inventory_path.relative_to(REPOSITORY_ROOT)
        if inventory_path.is_relative_to(REPOSITORY_ROOT)
        else inventory_path
    )
    return {
        "experiment": "M2 relaxed all-degree exact compressed nu=2 search",
        "date": "2026-09-13",
        "status": "EXACT FINITE RELAXED DP; HYPOTHETICAL STOCKS; GEOMETRY OBLIGATIONS OPEN",
        "input": {
            "base_field": "F_2",
            "q": 2,
            "genus": GENUS,
            "rational_place_count_N": RATIONAL_PLACES,
            "maximum_degree": MAX_DEGREE,
            "inventory_source_for_certified_prefix": str(relative_inventory),
            "inventory_sha256": _inventory_sha256(inventory_path),
            "certified_prefix": {
                "degrees": list(range(2, CERTIFIED_LOW_MAX + 1)),
                "stocks": list(low_stocks),
                "meaning": "certified B_2..B_11, including zero counts",
            },
            "relaxed_degrees": list(range(CERTIFIED_LOW_MAX + 1, MAX_DEGREE + 1)),
            "relaxed_stock_rule": "floor(266/d), independent of actual curve inventory",
        },
        "relaxation": {
            "label": "HYPOTHETICAL STOCKS; NOT CERTIFIED PLACE COUNTS",
            "why_contains_actual_search": "any strict-improvement vector has A<=266, so each degree has multiplicity <=floor(266/d)",
            "low_degree_rule": "use certified B_2..B_11 exactly",
            "high_degree_rule": "grant floor(266/d) hypothetical places for every d=12..47",
            "actual_inventory_not_called_for_degrees_12_to_47": True,
        },
        "historical_and_caps": {
            "baseline_ratio": BASELINE,
            "baseline_ratio_decimal": _decimal(BASELINE),
            "strict_cost_cap": cost_cap,
            "strict_cost_cap_decimal": _decimal(cost_cap),
            "special_rebate_bound": SPECIAL_REBATE,
            "a_cap": a_cap,
            "a_strict_upper_endpoint": a_endpoint,
            "t_minimum_formula": "floor(b*(342+max(0,A-37/16-A/1024)))+1",
            "t_minimums": list(t_minimums),
            "global_c_cap": c_cap,
            "global_c_cap_attaining_A": [
                row for row in c_cap_rows if row["C_limit"] == c_cap
            ],
            "degree_cap_from_C": "f(f+1)<=2280 implies f<=47",
        },
        "dp": {
            "state_key": "(A,C)",
            "retained_value": "maximal exact rebate=sum(m*d/2**d)",
            "rebate_scale": REBATE_SCALE,
            "partial_pruning": "only globally valid A<=266 and C<=2280",
            "states_per_degree": states_per_degree,
            "stats": stats,
        },
        "automatic_best": _candidate_json(independent_evaluation),
        "dp_best_state": _jsonable(best_state),
        "conclusion": {
            "strict_improvement_found_in_relaxed_box": strict_improvements > 0,
            "strict_improvements_count": strict_improvements,
            "best_ratio": best_ratio,
            "best_equals_incumbent": best_ratio == BASELINE if best_ratio is not None else False,
            "arithmetic_obstruction": (
                "No hypothetical degree<=47 nu=2 configuration beats the incumbent; "
                "therefore no actual fixed-k configuration with arbitrary nonrational degree can beat it under this conservative score."
                if strict_improvements == 0 and best_ratio == BASELINE
                else "The relaxed obstruction did not rule out a strict improvement."
            ),
        },
        "proof_obligations": [
            "the relaxed high-degree stocks are hypothetical and confer no existence of places",
            "the actual winner still needs explicit distinct S places, disjoint explicit T, and the p-primary ray-tower hypotheses",
            "the obstruction covers fixed k343, nonrational S, nu=2, and the conservative binary conductor score only",
            "it says nothing about nu>2, rational S, another base curve, another theorem criterion, exact ray groups, or global A(2) optimality",
        ],
        "scope_exclusions": [
            "all-nu search",
            "all-base-curve search",
            "ternary refinement",
            "exact ray-group computation",
            "global optimum outside fixed-k conservative nu=2 score",
        ],
        "reproducible_command": "python3 experiments/search_all_degree_relaxation.py",
    }


def _markdown(report: Mapping[str, object]) -> str:
    caps = report["historical_and_caps"]
    assert isinstance(caps, Mapping)
    dp = report["dp"]
    assert isinstance(dp, Mapping)
    stats = dp["stats"]
    assert isinstance(stats, Mapping)
    conclusion = report["conclusion"]
    assert isinstance(conclusion, Mapping)
    best = report["automatic_best"]
    assert isinstance(best, Mapping)
    strict_count = stats.get("strict_improvements_over_baseline", 0)
    if strict_count:
        conclusion_text = (
            f"The relaxed box contains {strict_count} hypothetical strict improvement(s). "
            "The obstruction therefore fails in this relaxed arithmetic model; "
            "the witness has no place-existence claim."
        )
    else:
        conclusion_text = (
            "No hypothetical degree<=47 ν=2 configuration beats the incumbent. "
            "Consequently, after the separate geometric obligations are met for "
            "the winner, this certifies the conservative fixed-k ν=2 score optimum."
        )
    return f"""# Fixed-k ν=2 obstruction with relaxed all-degree stocks

This is a separate bounded arithmetic audit of the automatically discovered
ratio `196608/620201`. It uses certified `k343` counts for degrees 2 through
11, including zeros, and then grants **hypothetical** stocks
`floor(266/f)` for every degree 12 through 47. Those high-degree stocks are
not certified place counts and are used only to form a superset of every
actual configuration that could beat the incumbent.

## Why the relaxation is finite

Let `b=196608/620201`, `g=343`, `N=192`, and let `cost` be the ν=2
conductor-filtration cost. A strict improvement requires

`cost < N/b-(g-1) = {caps['strict_cost_cap']}`.

The certified stocks in degrees 5, 6 and 8 contribute at most `37/16` rebate;
every other nonzero degree in the certified prefix or relaxation is at least
10, so its rebate is at most `A/1024`. Therefore

`cost >= A-37/16-A/1024`,

which gives `A < {caps['a_strict_upper_endpoint']}` and hence `A<=266`.
This also bounds every hypothetical multiplicity by `floor(266/f)`. Combining
the necessary

`t >= floor(b*(342+max(0,A-37/16-A/1024)))+1`

with `I>=0` gives the computed global cap `C<=2280`. Since each selected
degree contributes `f(f+1)` to C, any selected degree satisfies `f<=47`.
Thus degrees 2 through 47 cover every possible strict improvement under this
fixed-k, ν=2 score, while degrees above 47 are ruled out arithmetically.

## Exact DP and result

The raw relaxed multiplicity product is
`{stats['raw_bounded_vectors_not_enumerated']}` and is not enumerated. The DP
state is `(A,C)` and retains the maximal exact rebate
`sum(m*d/2^d)`, scaled by `2^47`, with a witness. Equal `(A,C)` states with a
smaller rebate are dominated because they have the same optimal t and a larger
denominator. Partial states are pruned only by the global caps `A<=266` and
`C<=2280`.

The DP has `{stats['dp_final_states']}` final states after
`{stats['transition_attempts']}` transition attempts. It applied
`{stats['globally_capped_transition_choices']}` global cap choices and removed
`{stats['rebate_dominated_transitions']}` dominated transitions. After the
final t and GS checks, it found
`{conclusion['strict_improvements_count']}` strict improvements over the
incumbent. The best witness is
`{best.get('multiplicity_vector')}`, with rows `{best.get('rows')}` and exact
ratio `{best.get('ratio_lower_bound')}`. A witness cross-check using
`src/theorem_search.py` agrees with the DP state and witness. Independent
exhaustion is checked by `tests/independent_obstruction.py`; see
`results/INDEPENDENT_OBSTRUCTION.md` for its separate verification report.

The bounded conclusion is: {conclusion_text}
It does not certify place existence for the hypothetical high-degree stocks and
makes no claim about other depths, curves, criteria, exact ray groups, or
global `A(2)`.

## Reproduction

```sh
python3 experiments/search_all_degree_relaxation.py
```

The machine-readable artifact is `results/all-degree-relaxation.json`.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=REPOSITORY_ROOT / "curves" / "k343-place-counts-30.json",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=REPOSITORY_ROOT / "results" / "all-degree-relaxation.json",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=REPOSITORY_ROOT / "proofs" / "NU2_OBSTRUCTION.md",
    )
    args = parser.parse_args(argv)
    inventory_path = args.inventory
    if not inventory_path.is_absolute():
        inventory_path = Path.cwd() / inventory_path
    report = run_search(inventory_path)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(_jsonable(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.output_md.write_text(_markdown(_jsonable(report)), encoding="utf-8")
    best = report["automatic_best"]
    if isinstance(best, Mapping):
        print("All-degree relaxed best:", best.get("ratio_lower_bound"),
              "rows=", best.get("rows"), "t=", best.get("t"))
    print("JSON:", args.output_json)
    print("Proof:", args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
