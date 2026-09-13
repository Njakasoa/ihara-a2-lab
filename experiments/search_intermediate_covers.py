#!/usr/bin/env python3
"""Bounded nu=2 arithmetic search over every certified intermediate cover.

Each record in curves/intermediate-covers.json supplies a genus, rational-place
count, and exact-degree place inventory.  This script passes the nonrational
degrees 2 through 12 directly to theorem_search.search_nu2 with the already
observed M2 ratio as the strict-improvement incumbent.

The engine's cost cut is sound only for strict improvements over that
incumbent.  Consequently a per-cover result with no beating candidate reports
the best candidate in the evaluated (unpruned) region, never a global optimum.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import date
from fractions import Fraction
from pathlib import Path
from typing import Mapping


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from theorem_search import search_nu2  # noqa: E402


BENCHMARK = Fraction(196608, 620201)
MAX_DEGREE = 12
DEFAULT_DATABASE = REPOSITORY_ROOT / "curves" / "intermediate-covers.json"
DEFAULT_OUTPUT_JSON = REPOSITORY_ROOT / "results" / "intermediate-search.json"
DEFAULT_OUTPUT_MD = REPOSITORY_ROOT / "results" / "INTERMEDIATE_SEARCH.md"


def _jsonable(value: object) -> object:
    """Convert exact runtime values into stable JSON values."""

    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _inventory(record: Mapping[str, object], max_degree: int = MAX_DEGREE):
    counts = record["place_counts"]
    if not isinstance(counts, list):
        raise ValueError("intermediate-cover record needs a place_counts list")
    upper = min(max_degree, len(counts))
    return [
        (degree, int(counts[degree - 1]))
        for degree in range(2, upper + 1)
        if int(counts[degree - 1]) > 0
    ]


def _record_id(index: int, record: Mapping[str, object]) -> str:
    basis = "-".join(str(mask) for mask in record["basis_masks"])
    return f"cover-{index:03d}-r{record['rank']}-b{basis}"


def _per_cover_result(
    index: int,
    record: Mapping[str, object],
    engine_result: Mapping[str, object],
    elapsed_seconds: float,
    *,
    max_degree: int,
) -> dict:
    stats = engine_result["stats"]
    assert isinstance(stats, Mapping)
    beats = int(stats["beats_incumbent"])
    best = engine_result.get("best")
    if best is not None:
        best = _jsonable(best)
    if beats:
        best_claim = (
            "strict-improvement finite-box optimum for this completed box; "
            "all pruned branches are unable to beat the benchmark"
        )
    else:
        best_claim = (
            "best among evaluated candidates only; the cost cut proves no "
            "strict improvement over the benchmark, not global optimality"
        )
    return {
        "index": index,
        "id": _record_id(index, record),
        "rank": int(record["rank"]),
        "basis_masks": record["basis_masks"],
        "genus": int(record["genus"]),
        "rational_places": int(record["rational_places"]),
        "inventory_degree_max": max_degree,
        "inventory": [
            {"degree": degree, "available": available}
            for degree, available in _inventory(record, max_degree=max_degree)
        ],
        "total_configurations": int(stats["total_configurations"]),
        "evaluated_configurations": int(stats["evaluated_configurations"]),
        "pruned_configurations": int(stats["cost_pruned_configurations"]),
        "pruned_branches": int(stats["cost_pruned_branches"]),
        "accepted_configurations": int(stats["accepted_configurations"]),
        "rejected_configurations": int(stats["rejected_configurations"]),
        "no_feasible_t": int(stats["no_feasible_t"]),
        "gs_failures": int(stats["gs_failures"]),
        "beating_benchmark": beats,
        "ties_benchmark": int(stats["ties_incumbent"]),
        "best_within_pruned_region": best,
        "best_claim": best_claim,
        "cost_threshold_for_strict_improvement": _jsonable(
            engine_result["cost_threshold_for_strict_improvement"]
        ),
        "elapsed_seconds": round(elapsed_seconds, 6),
        "status": "COMPLETED",
    }


def _strongest_observed(completed: list[dict]) -> dict | None:
    candidates = [
        result["best_within_pruned_region"]
        for result in completed
        if result["best_within_pruned_region"] is not None
    ]
    if not candidates:
        return None
    best = max(candidates, key=lambda candidate: Fraction(candidate["ratio_lower_bound"]))
    owner = next(
        result
        for result in completed
        if result["best_within_pruned_region"] is best
    )
    return {
        "cover_id": owner["id"],
        "index": owner["index"],
        "rank": owner["rank"],
        "basis_masks": owner["basis_masks"],
        "ratio_lower_bound": best["ratio_lower_bound"],
        "t": best["t"],
        "rows": best["rows"],
        "strictly_beats_benchmark": (
            Fraction(best["ratio_lower_bound"]) > BENCHMARK
        ),
    }


def build_report(
    database_path: Path = DEFAULT_DATABASE,
    *,
    timeout_seconds: float = 300.0,
    max_degree: int = MAX_DEGREE,
) -> dict:
    """Run all cover boxes until completion or the explicit time budget."""

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if max_degree < 2:
        raise ValueError("max_degree must be at least two")
    database_path = Path(database_path)
    database = json.loads(database_path.read_text())
    records = database.get("records")
    if not isinstance(records, list) or len(records) != 373:
        raise ValueError("the intermediate database must contain 373 records")

    started = time.monotonic()
    completed: list[dict] = []
    stopped_before_index: int | None = None
    for index, record in enumerate(records):
        if time.monotonic() - started >= timeout_seconds:
            stopped_before_index = index
            break
        inventory = _inventory(record, max_degree=max_degree)
        if not inventory:
            raise ValueError(f"cover {index} has no nonrational inventory")
        cover_started = time.monotonic()
        engine_result = search_nu2(
            genus=int(record["genus"]),
            rational_places=int(record["rational_places"]),
            inventory=inventory,
            incumbent=BENCHMARK,
            prune=True,
        )
        completed.append(
            _per_cover_result(
                index,
                record,
                engine_result,
                time.monotonic() - cover_started,
                max_degree=max_degree,
            )
        )

    complete = stopped_before_index is None and len(completed) == len(records)
    strict_improvements = [
        result for result in completed if result["beating_benchmark"] > 0
    ]
    report = {
        "date": str(date.today()),
        "experiment": (
            "bounded nu=2 search over all certified intermediate "
            "Artin-Schreier covers"
        ),
        "status": (
            "COMPLETE FINITE BOX; GEOMETRY AND TOWER OBLIGATIONS OPEN"
            if complete
            else "PARTIAL TIME-BOUNDED RUN; NO CLAIM OUTSIDE COMPLETED BOXES"
        ),
        "benchmark": {
            "ratio": str(BENCHMARK),
            "source": "already observed M2 arithmetic candidate",
            "comparison": "strict improvement only",
        },
        "input": {
            "database": str(database_path.relative_to(REPOSITORY_ROOT)),
            "database_sha256": hashlib.sha256(
                database_path.read_bytes()
            ).hexdigest(),
            "database_status": database.get("status"),
            "cover_count_declared": len(records),
            "covers_completed": len(completed),
            "covers_remaining": len(records) - len(completed),
            "maximum_degree": max_degree,
            "depth": 2,
            "rational_places_from_cover_record": True,
            "nonrational_inventory_only": True,
        },
        "pruning": {
            "enabled": True,
            "engine": "src/theorem_search.py::search_nu2",
            "rule": "partial conductor cost >= N/benchmark-(g-1)",
            "sound_for": "strict improvements over benchmark",
            "equality_is_pruned": True,
            "remaining_costs_nonnegative": True,
            "warning": (
                "If beating_benchmark is zero, best_within_pruned_region "
                "is not a global optimum claim."
            ),
        },
        "completed_cover_results": completed,
        "completed_boxes_with_strict_improvement": len(strict_improvements),
        "covers_beating_benchmark": [
            result["id"] for result in strict_improvements
        ],
        "strongest_observed_score": _strongest_observed(completed),
        "stopped_before_index": stopped_before_index,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "proof_status": {
            "finite_cover_input": (
                "intermediate-covers.json is derived from the certified "
                "quotient zetas and finite trace inventory"
            ),
            "arithmetic": (
                "exact integer/rational theorem-search arithmetic; no "
                "ray-class-group computation"
            ),
            "open": [
                "selected places must be exhibited and distinct",
                "T must be explicit and disjoint from S",
                "p-primary T-ray tower hypotheses remain theorem obligations",
                "no result here is a new Ihara bound or novelty claim",
            ],
        },
        "reproduction": (
            "python3 experiments/search_intermediate_covers.py "
            "--timeout-seconds 300"
        ),
    }
    if not complete:
        report["partial_run_note"] = (
            "Only completed cover boxes are summarized.  No conclusion is "
            "drawn for the remaining covers."
        )
    return report


def markdown_report(report: Mapping[str, object]) -> str:
    """Render a compact human-readable report without overstating pruning."""

    benchmark = report["benchmark"]
    assert isinstance(benchmark, Mapping)
    input_data = report["input"]
    assert isinstance(input_data, Mapping)
    pruning = report["pruning"]
    assert isinstance(pruning, Mapping)
    strongest = report.get("strongest_observed_score")
    completed = report["completed_cover_results"]
    assert isinstance(completed, list)
    complete = str(report["status"]).startswith("COMPLETE")
    total_evaluated = sum(
        int(result["evaluated_configurations"]) for result in completed
    )
    total_pruned = sum(
        int(result["pruned_configurations"]) for result in completed
    )
    total_no_feasible = sum(int(result["no_feasible_t"]) for result in completed)
    lines = [
        "# Intermediate-cover bounded search",
        "",
        str(report["status"]),
        "",
        "This artifact runs the existing exact nu=2 engine on every completed",
        "intermediate-cover inventory through degree "
        f"{input_data['maximum_degree']}.  The benchmark is "
        f"{benchmark['ratio']}; comparisons are strict.",
        "",
        "## Scope and pruning",
        "",
        f"- Declared covers: {input_data['cover_count_declared']}",
        f"- Completed cover boxes: {input_data['covers_completed']}",
        f"- Elapsed seconds: {report['elapsed_seconds']}",
        f"- Benchmark: {benchmark['ratio']}",
        f"- Engine: {pruning['engine']}",
        f"- Cut: {pruning['rule']}",
        "- The cut is sound for strict improvements because t is bounded by N",
        "  and all remaining conductor costs are nonnegative.",
        "- Equality is pruned.  A box with no beating candidate has only a",
        "  best evaluated candidate, not a claimed global optimum.",
        "",
        "## Aggregate result",
        "",
        f"- Completed boxes with a strict improvement: "
        f"{report['completed_boxes_with_strict_improvement']}",
        f"- Covers beating the benchmark: "
        f"{report['covers_beating_benchmark']}",
        f"- Evaluated configurations (all completed boxes): {total_evaluated}",
        f"- Pruned configurations (all completed boxes): {total_pruned}",
        f"- No-feasible-t configurations: {total_no_feasible}",
    ]
    if strongest is None:
        lines.append("- Strongest observed score: none (no feasible candidate returned)")
    else:
        assert isinstance(strongest, Mapping)
        lines.append(
            "- Strongest observed evaluated score: "
            f"{strongest['ratio_lower_bound']} on {strongest['cover_id']} "
            f"(rank {strongest['rank']}, basis {strongest['basis_masks']})"
        )
        if strongest["strictly_beats_benchmark"]:
            lines.append(
                "  This is a strict-improvement result within the completed "
                "finite box; geometry and tower obligations remain open."
            )
        else:
            lines.append(
                "  This is only the strongest evaluated score; pruned "
                "candidates may be better up to the benchmark."
            )
    if not complete:
        lines.extend(
            [
                "",
                "The time budget stopped the run before all 373 boxes.  The",
                "remaining boxes have no reported search result and are not",
                "covered by the aggregate conclusion.",
            ]
        )
    lines.extend(
        [
            "",
            "## Per-cover records",
            "",
            "The JSON retains each completed box's evaluated configurations,",
            "pruned configurations and branches, no-feasible-t count, exact",
            "best evaluated candidate, and strict-improvement count.",
            "",
            "| index | rank | basis masks | evaluated | pruned | no feasible t | beats benchmark | best evaluated ratio |",
            "| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for result in completed:
        best = result["best_within_pruned_region"]
        ratio = "none" if best is None else str(best["ratio_lower_bound"])
        lines.append(
            f"| {result['index']} | {result['rank']} | "
            f"{result['basis_masks']} | {result['evaluated_configurations']} | "
            f"{result['pruned_configurations']} | {result['no_feasible_t']} | "
            f"{result['beating_benchmark']} | {ratio} |"
        )
    lines.extend(
        [
            "",
            "## Proof status",
            "",
            "The cover geometries and character zeta inputs come from the",
            "certified intermediate-cover database.  The search computes only",
            "the Duursma–Mak sufficient arithmetic criterion and its binary",
            "conductor-filtration upper bound.  It does not compute a ray class",
            "group, prove a new bound, or make a novelty claim.",
            "",
            "Reproduce with:",
            "",
            "    python3 experiments/search_intermediate_covers.py",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    parser.add_argument("--max-degree", type=int, default=MAX_DEGREE)
    args = parser.parse_args()
    database_path = args.database
    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path
    report = build_report(
        database_path,
        timeout_seconds=args.timeout_seconds,
        max_degree=args.max_degree,
    )
    output_json = args.output_json
    output_md = args.output_md
    if not output_json.is_absolute():
        output_json = Path.cwd() / output_json
    if not output_md.is_absolute():
        output_md = Path.cwd() / output_md
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2) + "\n")
    output_md.write_text(markdown_report(report))
    print(
        f"{report['status']}; completed "
        f"{report['input']['covers_completed']}/"
        f"{report['input']['cover_count_declared']} cover boxes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
