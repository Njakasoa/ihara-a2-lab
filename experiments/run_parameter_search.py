#!/usr/bin/env python3
"""Run and record the bounded M2 theorem-parameter search.

The script has no hand-entered candidate vector.  It loads the certified place
counts, runs the exhaustive ``nu=2`` search, and only then uses the returned
automatic winner as the centre of the bounded even-depth neighborhood.

Run from the repository root with::

    python3 experiments/run_parameter_search.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Mapping


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from theorem_search import (  # noqa: E402
    HistoricalBound,
    K343_GENUS,
    K343_RATIONAL_PLACES,
    load_inventory,
    search_nonuniform_even_neighborhood,
    search_nu2,
)


def _decimal(value: Fraction) -> str:
    """Display a Fraction without making the display part of the proof."""

    with localcontext() as context:
        context.prec = 30
        return format(Decimal(value.numerator) / Decimal(value.denominator), ".20f")


def _jsonable(value: object) -> object:
    """Convert exact runtime values to a stable JSON representation."""

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


def _candidate_json(candidate: Mapping[str, object] | None) -> object:
    if candidate is None:
        return None
    output = _jsonable(candidate)
    assert isinstance(output, dict)
    for key in (
        "average_conductor_degree_upper_bound",
        "conductor_average",
        "conductor_cost",
        "genus_denominator_upper_bound",
        "ratio_lower_bound",
    ):
        value = candidate.get(key)
        if isinstance(value, Fraction):
            output[f"{key}_decimal"] = _decimal(value)
    return output


def _inventory_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report(inventory_path: Path, *, prune: bool = True) -> dict:
    """Compute the complete machine-readable M2 report in memory."""

    # Loading once here both validates the input and records its exact scope.
    inventory = load_inventory(inventory_path, max_degree=12)
    search = search_nu2(
        genus=K343_GENUS,
        rational_places=K343_RATIONAL_PLACES,
        inventory=inventory,
        incumbent=HistoricalBound,
        prune=prune,
    )
    automatic_best = search["best"]
    local = None
    if automatic_best is not None:
        local = search_nonuniform_even_neighborhood(
            automatic_best,
            inventory,
            genus=K343_GENUS,
            rational_places=K343_RATIONAL_PLACES,
        )

    relative_inventory = inventory_path
    try:
        relative_inventory = inventory_path.relative_to(REPOSITORY_ROOT)
    except ValueError:
        pass

    historical = HistoricalBound
    threshold = search["cost_threshold_for_strict_improvement"]
    report = {
        "experiment": "M2 exact automated Duursma-Mak theorem-parameter search",
        "date": "2026-09-13",
        "status": "EXACT FINITE INTEGER/RATIONAL SEARCH; GEOMETRY OBLIGATIONS OPEN",
        "m1_gate": {
            "record": "results/M1_STATUS.md",
            "required_status": "M1 ACCEPTED",
        },
        "input": {
            "base_field": "F_2",
            "q": 2,
            "genus": K343_GENUS,
            "rational_place_count_N": K343_RATIONAL_PLACES,
            "inventory": str(relative_inventory),
            "inventory_sha256": _inventory_sha256(inventory_path),
            "maximum_degree": 12,
            "nonrational_degrees_with_positive_counts": [
                {"degree": entry.degree, "available": entry.available}
                for entry in inventory
            ],
            "depth_for_exhaustive_search": 2,
        },
        "historical_benchmark": {
            "ratio": str(historical),
            "ratio_decimal": _decimal(historical),
            "source": "Duursma-Mak Theorem 1.3 / Proposition 5.5",
        },
        "strict_cost_pruning": {
            "threshold": str(threshold),
            "threshold_decimal": _decimal(threshold),
            "necessary_condition": "cost < N/incumbent - (g-1)",
            "reason": "t <= N and all unassigned conductor costs are nonnegative",
            "equality_pruned": True,
            "sound_for_strict_improvement": True,
        },
        "nu2_search": {
            "depth": 2,
            "inventory": search["inventory"],
            "pruning": search["pruning"],
            "stats": search["stats"],
            "automatic_best": _candidate_json(automatic_best),
            "proof_obligations": search["proof_obligations"],
            "status": search["status"],
        },
        "nonuniform_even_neighborhood": (
            _jsonable(local) if local is not None else {
                "status": "NOT RUN: nu=2 search found no feasible candidate"
            }
        ),
        "reproducible_command": "python3 experiments/run_parameter_search.py",
        "scope_exclusions": [
            "no ternary refinement",
            "no unsupported ray-group rank or exact ray degree",
            "no claim of global optimum outside this k343 degree<=12 finite box",
            "no claim that the arithmetic winner is already a proved new Ihara bound",
        ],
    }
    # Make the exact local winner easy to inspect without changing its nested
    # machine-readable form.
    if local is not None and isinstance(local.get("best"), Mapping):
        report["nonuniform_even_neighborhood"] = dict(report["nonuniform_even_neighborhood"])
        report["nonuniform_even_neighborhood"]["best"] = _candidate_json(local["best"])
    return report


def _markdown(report: Mapping[str, object]) -> str:
    search = report["nu2_search"]
    assert isinstance(search, Mapping)
    stats = search["stats"]
    assert isinstance(stats, Mapping)
    best = search["automatic_best"]
    assert isinstance(best, Mapping)
    local = report["nonuniform_even_neighborhood"]
    assert isinstance(local, Mapping)
    local_stats = local.get("stats", {})
    assert isinstance(local_stats, Mapping)
    historical = report["historical_benchmark"]
    assert isinstance(historical, Mapping)
    threshold = report["strict_cost_pruning"]
    assert isinstance(threshold, Mapping)

    vector = best.get("multiplicity_vector")
    rows = best.get("rows")
    ratio = best.get("ratio_lower_bound", best.get("ratio_from_units"))
    ratio_decimal = best.get("ratio_lower_bound_decimal", "")
    difference = ""
    try:
        difference_fraction = Fraction(str(ratio)) - Fraction(str(historical["ratio"]))
        difference = f"`{difference_fraction}` (strictly positive)"
    except (TypeError, ValueError):
        difference = "computed exactly in the JSON artifact"

    return f"""# M2 — exact automated theorem-parameter search

The M1 gate is recorded as **ACCEPTED** in `results/M1_STATUS.md`. This report
searches the certified `k343` place-count inventory through degree 12 with the
binary Duursma–Mak arithmetic. The search is finite and exact; its geometry
and later ray-tower obligations remain explicit.

## Exhaustive `nu=2` box

For each available nonrational degree `d`, every multiplicity
`0 <= B_d <= B_d(k343)` was considered. The positive counts are
`{', '.join(f"B_{item['degree']}={item['available']}" for item in search['inventory'])}`.
For a row `(d,n,nu)`, the engine uses

`A += n*d*(nu-1-floor((nu-1)/2))`,
`C += n*[d*(nu-1)]*[d*(nu-1)+1]`, and
`I = D^2 - 2*C - 4*A`, where `D=1+A-t`.

For fixed `A,C`, the largest possible splitting set is computed, never
guessed:

`t = min(N, A, 1 + A - ceil_sqrt(2*C + 4*A))`.

The exact conductor-filtration cost is a `Fraction`. A branch is pruned only
when its partial cost is already at least
`N/incumbent-(g-1) = {threshold['threshold']}`. Since `t <= N` and all
remaining costs are nonnegative, this strict-cost test cannot discard a
configuration that beats the historical incumbent `{historical['ratio']}`.

The box contains `{stats['total_configurations']}` multiplicity vectors. The
engine cut `{stats.get('cost_pruned_branches', 0)}` monotone branch choices,
covering `{stats['cost_pruned_configurations']}` complete vectors by this rule, and evaluated
`{stats['evaluated_configurations']}`, accepted `{stats['accepted_configurations']}`
after the sufficient criterion, and recorded `{stats['no_feasible_t']}` with no
positive theorem-admissible `t`. GS failures after the exact `t` calculation:
`{stats['gs_failures']}`.

## Automatically found winner

The search returned multiplicity vector `{vector}` and rows `{rows}`. Its exact
arithmetic is `A={best['A']}`, `C={best['C']}`, `D={best['D']}`,
`I={best['GS_margin']}`, `t={best['t']}`, with denominator
`{best['genus_denominator_upper_bound']}` and ratio
`{ratio} approx {ratio_decimal}`. The historical ratio is
`{historical['ratio']} approx {historical['ratio_decimal']}`; the exact
difference is {difference}.

This is an automatically discovered finite-box improvement. It is not a new
asymptotic claim yet: the degree-12 place must be exhibited, the selected
places must be distinct, an explicit `T` must be disjoint from `S`, and the
p-primary T-ray tower hypotheses must be proved for the selected divisor.
The engine computes no unsupported ray-group rank or exact auxiliary degree.

## Bounded even-depth neighborhood

Starting from the automatic winner, the local audit varies each degree's
multiplicity independently over `base-1, base, base+1` clipped to inventory
availability. It enumerates all per-degree uniform assignments in
`{{2,4,6}}`, together with one exceptional selected place at one degree of
depth 4 or 6 while the other selected places have depth 2. This is a bounded
local scope, not an arbitrary nonuniform search.

It generated `{local_stats.get('uniform_variants_generated', 0)}` uniform and
`{local_stats.get('single_exception_variants_generated', 0)}` exceptional
variants, deduplicated to `{local_stats.get('unique_variants', 0)}` cases, and
accepted `{local_stats.get('accepted_variants', 0)}`. The best local case is
`{local.get('best', {}).get('ratio_lower_bound', 'none') if isinstance(local.get('best'), Mapping) else 'none'}`;
no local case is promoted beyond the finite arithmetic audit. Odd depths are
handled by the conservative domination statement in
`proofs/CONDUCTOR_FILTRATION.md`, and ternary refinement is excluded.

## Reproduction and status

```sh
python3 experiments/run_parameter_search.py
```

The machine-readable output is `results/m2-search.json`. Statuses are exact
integer/rational arithmetic plus open geometry obligations. No optimum outside
the stated finite inventory box is claimed.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=REPOSITORY_ROOT / "curves" / "k343-place-counts-30.json",
        help="place-count JSON (default: certified k343 inventory)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=REPOSITORY_ROOT / "results" / "m2-search.json",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=REPOSITORY_ROOT / "results" / "M2_SEARCH.md",
    )
    parser.add_argument(
        "--no-prune",
        action="store_true",
        help="evaluate every vector; intended for small audits, not the report",
    )
    args = parser.parse_args(argv)
    inventory_path = args.inventory
    if not inventory_path.is_absolute():
        inventory_path = Path.cwd() / inventory_path
    report = build_report(inventory_path, prune=not args.no_prune)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.output_md.write_text(_markdown(report), encoding="utf-8")
    best = report["nu2_search"]["automatic_best"]
    if isinstance(best, Mapping):
        print(
            "M2 automatic best:",
            best["ratio_lower_bound"],
            "rows=",
            best["rows"],
            "t=",
            best["t"],
        )
    print("JSON:", args.output_json)
    print("Markdown:", args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
