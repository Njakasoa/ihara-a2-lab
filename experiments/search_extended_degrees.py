#!/usr/bin/env python3
"""Exact compressed search for the k343 binary ``nu=2`` degree<=30 box.

The degree<=12 search enumerates multiplicity vectors directly.  Doing that
through degree 30 would be needlessly enormous.  Here a state is ``(A,C)``;
for a fixed state only the largest exact rebate

    rebate = sum(m_d * d / 2**d)

matters, because the conductor cost is ``A-rebate``.  A witness multiplicity
vector is retained with that maximum rebate.  Future choices depend only on
``(A,C)`` and the remaining inventory, so this is an exact dynamic program for
the finite arithmetic objective.

The DP does not assert that the selected places have been exhibited.  It only
uses the certified place counts in ``curves/k343-place-counts-30.json``; the
usual S/T, constant-field, and p-primary ray-tower obligations remain open.
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

from theorem_search import (  # noqa: E402
    evaluate_binary,
    load_inventory,
    optimal_t,
)


BASELINE = Fraction(196608, 620201)
GENUS = 343
RATIONAL_PLACES = 192
MAX_DEGREE = 30
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


def _inventory_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def derive_a_cap(cost_cap: Fraction) -> tuple[int, Fraction]:
    """Derive the largest integer A allowed by the global rebate bound.

    For every degree<=30 vector,

      rebate <= 37/16 + A/1024,

    because the full d=5,6,8 stocks contribute at most 37/16 and every
    remaining degree is at least 10.  Thus strict improvement requires

      A - 37/16 - A/1024 < cost_cap.

    Solving this strict rational inequality gives the returned integer cap and
    the exact real upper endpoint (A must be strictly below it).
    """

    endpoint = (cost_cap + SPECIAL_REBATE) * Fraction(1024, 1023)
    # A < endpoint, with endpoint positive.  ceil(endpoint)-1 is exact using
    # the floor of (endpoint's numerator-1)/denominator.
    cap = (endpoint.numerator - 1) // endpoint.denominator
    return cap, endpoint


def derive_t_minimums(cost_baseline: Fraction, a_cap: int,
                      rational_places: int) -> tuple[int, ...]:
    """Return the necessary integer t lower bound for each A in [0,a_cap]."""

    values = []
    for a_value in range(a_cap + 1):
        lower_cost = max(
            Fraction(0),
            Fraction(a_value, 1) - SPECIAL_REBATE - Fraction(a_value, 1024),
        )
        values.append(
            _floor_fraction(
                cost_baseline * (GENUS - 1 + lower_cost)
            ) + 1
        )
    return tuple(values)


def derive_global_c_cap(t_minimums: tuple[int, ...], a_cap: int) -> tuple[int, list[dict]]:
    """Compute a global C cap from all A-dependent necessary conditions.

    If strict improvement is possible at A, then t>=t_min[A].  Consequently
    D<=1+A-t_min[A], and GS requires

      C <= floor(((1+A-t_min[A])**2 - 4*A)/2).

    Values with t_min>A or a negative right side cannot be feasible and are
    omitted from the maximum.  The maximum is a single global cap used while
    constructing *partial* DP states; no final-A-dependent rule is applied to
    a partial state.
    """

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
    """Run the compressed degree<=30 search and independently evaluate its winner."""

    inventory = load_inventory(inventory_path, max_degree=MAX_DEGREE)
    low_stocks = {entry.degree: entry.available for entry in inventory if entry.degree <= 11}
    if low_stocks != {5: 2, 6: 16, 8: 16, 10: 64}:
        raise ValueError("the fixed k343 rebate bound requires its certified low-degree prefix")
    stocks = tuple(entry.available for entry in inventory)
    degrees = tuple(entry.degree for entry in inventory)
    cost_cap = Fraction(RATIONAL_PLACES, 1) / BASELINE - (GENUS - 1)
    a_cap, a_endpoint = derive_a_cap(cost_cap)
    t_minimums = derive_t_minimums(BASELINE, a_cap, RATIONAL_PLACES)
    c_cap, c_cap_rows = derive_global_c_cap(t_minimums, a_cap)

    bounded_counts = tuple(min(stock, a_cap // degree)
                           for degree, stock in zip(degrees, stocks))
    raw_bounded_vectors = prod(count + 1 for count in bounded_counts)
    rebate_terms = tuple(
        degree * (1 << (MAX_DEGREE - degree)) for degree in degrees
    )
    c_terms = tuple(degree * (degree + 1) for degree in degrees)

    # A state value is (max rebate in units of 2**(-30), witness tuple).
    states: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {
        (0, 0): (0, ())
    }
    states_per_degree = [{"degree": None, "states": 1}]
    transition_attempts = 0
    cap_pruned_transitions = 0
    rebate_dominated_transitions = 0
    witness_tie_replacements = 0

    for index, (degree, count, rebate_term, c_term) in enumerate(
        zip(degrees, bounded_counts, rebate_terms, c_terms)
    ):
        next_states: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
        for (a_value, c_value), (rebate, witness) in states.items():
            max_by_a = (a_cap - a_value) // degree
            max_by_c = (c_cap - c_value) // c_term
            max_multiplicity = min(count, max_by_a, max_by_c)
            transition_attempts += max_multiplicity + 1
            if max_multiplicity < count:
                cap_pruned_transitions += count - max_multiplicity
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
            "bounded_stock": count,
            "states": len(states),
        })

    # The final A-dependent test is applied only after the globally capped DP.
    final_state_count = 0
    t_minimum_failures = 0
    gs_cap_failures = 0
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
        final_state_count += 1
        t_upper = optimal_t(a_value, c_value, RATIONAL_PLACES)
        if t_upper < t_min:
            gs_cap_failures += 1
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

    if best_state is not None:
        assert independent_evaluation is not None
        independent_evaluation["multiplicity_vector"] = best_state[
            "multiplicity_vector"
        ]
        independent_evaluation["witness"] = best_state["witness"]
        best_state["independent_engine_evaluation"] = independent_evaluation
    stats = {
        "raw_bounded_vectors_not_enumerated": raw_bounded_vectors,
        "bounded_counts": {
            str(degree): count
            for degree, count in zip(degrees, bounded_counts)
        },
        "dp_final_states": len(states),
        "final_states_passing_t_minimum": final_state_count,
        "t_minimum_failures": t_minimum_failures,
        "gs_or_t_upper_failures": gs_cap_failures,
        "exact_nonimprovements_after_caps": exact_nonimprovements,
        "strict_improvements_over_baseline": strict_improvements,
        "transition_attempts": transition_attempts,
        "globally_capped_transition_choices": cap_pruned_transitions,
        "rebate_dominated_transitions": rebate_dominated_transitions,
        "witness_tie_replacements": witness_tie_replacements,
        "states_per_degree": states_per_degree,
    }
    return {
        "experiment": "M2 extended exact compressed nu=2 degree<=30 search",
        "date": "2026-09-13",
        "status": "EXACT FINITE DP; GEOMETRY OBLIGATIONS OPEN",
        "input": {
            "base_field": "F_2",
            "q": 2,
            "genus": GENUS,
            "rational_place_count_N": RATIONAL_PLACES,
            "maximum_degree": MAX_DEGREE,
            "inventory": str(inventory_path.relative_to(REPOSITORY_ROOT)
                              if inventory_path.is_relative_to(REPOSITORY_ROOT)
                              else inventory_path),
            "inventory_sha256": _inventory_sha256(inventory_path),
            "degrees": [
                {"degree": degree, "available": stock}
                for degree, stock in zip(degrees, stocks)
            ],
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
        },
        "dp": {
            "state_key": "(A,C)",
            "retained_value": "maximal exact rebate=sum(m*d/2**d)",
            "rebate_scale": REBATE_SCALE,
            "partial_pruning": "only globally valid A<=a_cap and C<=global_c_cap",
            "states_per_degree": states_per_degree,
            "stats": stats,
        },
        "automatic_best": _candidate_json(independent_evaluation),
        "dp_best_state": _jsonable(best_state),
        "proof_obligations": [
            "the DP uses certified place counts only; each selected place still needs an explicit distinct representative",
            "T must be an explicit set of t rational places disjoint from S",
            "the constant field and p-primary T-ray tower hypotheses are not computed here",
            "this finite degree<=30 box says nothing about other curves, degrees beyond 30, other depths, or global optimality",
            "no ray-group rank or exact auxiliary ray degree is inferred",
        ],
        "scope_exclusions": [
            "all-nu search",
            "all-base-curve search",
            "ternary refinement",
            "global optimum claim",
        ],
        "reproducible_command": "python3 experiments/search_extended_degrees.py",
    }


def _markdown(report: Mapping[str, object]) -> str:
    caps = report["historical_and_caps"]
    assert isinstance(caps, Mapping)
    dp = report["dp"]
    assert isinstance(dp, Mapping)
    stats = dp["stats"]
    assert isinstance(stats, Mapping)
    best = report["automatic_best"]
    assert isinstance(best, Mapping)
    dp_best = report["dp_best_state"]
    assert isinstance(dp_best, Mapping)
    best_vector = best.get("multiplicity_vector", dp_best.get("multiplicity_vector"))
    best_rows = best.get("rows")
    if best_rows is None:
        best_rows = "see automatic_best in JSON"
    strict_count = stats.get("strict_improvements_over_baseline", 0)
    attaining = caps.get("global_c_cap_attaining_A", [])
    return f"""# Extended degree search — k343, binary `nu=2`

This bounded follow-up checks whether degrees 13 through 30 can improve the
automatically discovered degree-12-box ratio `196608/620201`. It uses the
certified `curves/k343-place-counts-30.json` inventory, with `g=343` and
`N=192`. It makes no claim outside this finite arithmetic box.

## Exact caps and compressed dynamic program

The incumbent is `b=196608/620201`. A strict improvement has conductor cost

`cost < 192/b - 342 = {caps['strict_cost_cap']}`.

Using the exact rebate bound
`rebate <= 37/16 + A/1024` gives

`A < {caps['a_strict_upper_endpoint']}`, hence the integer cap
`A <= {caps['a_cap']}`. For each integer A, the necessary numerator bound is

`t >= floor(b*(342+max(0,A-37/16-A/1024)))+1`.

Combining this with `I>=0` gives a computed global `C` cap of
`{caps['global_c_cap']}`; it is attained at
`{attaining}`. These A and C caps are global monotone bounds, so they are the
only arithmetic caps applied to partial DP states.

For each degree, multiplicities are bounded by both its certified stock and
`floor(266/d)`. The raw bounded product is
`{stats['raw_bounded_vectors_not_enumerated']}` and is not enumerated. A DP
state is `(A,C)` and retains the maximum exact rebate
`sum(m*d/2^d)`, scaled by `2^30`, together with one witness. At a fixed `(A,C)`
this rebate uniquely minimizes the conductor cost, so the dominance rule is
exact for the theorem objective.

The DP produced `{stats['dp_final_states']}` final states after
`{stats['transition_attempts']}` transition attempts. Globally capped choices:
`{stats['globally_capped_transition_choices']}`; dominated rebate transitions:
`{stats['rebate_dominated_transitions']}`. After the final necessary t and GS
checks, `{stats['strict_improvements_over_baseline']}` states strictly beat the
incumbent and `{stats['exact_nonimprovements_after_caps']}` do not.

## Result

The best DP witness has multiplicity vector `{best_vector}` and rows
`{best_rows}`. The JSON records its DP state and an independent evaluation by
`src/theorem_search.py`; the exact ratio is
`{best.get('ratio_lower_bound', 'see JSON')}`. The independent evaluator agrees
with the DP state and witness. No candidate vector was supplied to the DP.

This is an arithmetic search result. The selected degree-12 and higher-degree
places must be exhibited as distinct places, `T` must be explicitly chosen and
disjoint from `S`, and the constant-field and p-primary ray-tower hypotheses
remain proof obligations. No ray-group rank or exact ray degree is inferred.

## Reproduction and scope

```sh
python3 experiments/search_extended_degrees.py
```

The search covers only `k343`, degrees at most 30, and uniform depth `nu=2`.
It does not search all depths, other base curves, ternary refinement, or an
unrestricted global optimum.
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
        default=REPOSITORY_ROOT / "results" / "extended-degrees.json",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=REPOSITORY_ROOT / "results" / "EXTENDED_DEGREES.md",
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
        print("Extended degree best:", best.get("ratio_lower_bound"),
              "rows=", best.get("rows"), "t=", best.get("t"))
    print("JSON:", args.output_json)
    print("Markdown:", args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
