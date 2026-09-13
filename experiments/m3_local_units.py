#!/usr/bin/env python3
"""Run the bounded independent local-unit arithmetic gate for M3.

The experiment enumerates only groups with at most 4096 elements.  It records
the exact formula summaries and direct truncated-series checks; it does not
search supports, calculate a global ray class group, or claim a tower score.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from m3_local_units import (  # noqa: E402
    MAX_ENUMERATED_GROUP_ORDER,
    local_unit_structure,
    validate_structure_record,
    verify_local_formula,
)


REQUEST_PATH = REPOSITORY_ROOT / 'M3_RESULT.md'

# These fixtures include odd and even depths, several residue degrees, and the
# cap boundary.  They are small enough for a direct operation-by-operation
# check while exposing C4, C8, and mixed cyclic factors.
FIXTURES = (
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (4, 2),
    (4, 3),
    (4, 4),
    (6, 2),
    (6, 3),
    (12, 2),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPOSITORY_ROOT,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def _mutations(record: dict[str, object]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for field in ("f", "nu", "p_rank", "exponent", "order"):
        mutated = deepcopy(record)
        value = mutated[field]
        if not isinstance(value, int):
            statuses[field] = "REJECTED"
            continue
        mutated[field] = value + 1
        statuses[field] = (
            "REJECTED" if not validate_structure_record(mutated) else "ACCEPTED"
        )
    return statuses


def build_report() -> dict[str, object]:
    started = time.perf_counter()
    fixture_reports: list[dict[str, object]] = []
    all_passed = True
    mutation_statuses: dict[str, dict[str, str]] = {}
    for f, nu in FIXTURES:
        checked = verify_local_formula(
            f,
            nu,
            cap=MAX_ENUMERATED_GROUP_ORDER,
        )
        all_passed = all_passed and bool(checked["passed"])
        formula = checked["formula"]
        assert isinstance(formula, dict)
        mutation_statuses[f"{f},{nu}"] = _mutations(formula)
        fixture_reports.append(
            {
                "f": f,
                "nu": nu,
                "formula": formula,
                "direct": checked["direct"],
                "checks": checked["checks"],
                "passed": checked["passed"],
            }
        )

    input_paths = [
        REPOSITORY_ROOT / "proofs" / "CONDUCTOR_FILTRATION.md",
        REPOSITORY_ROOT / "proofs" / "NONUNIFORM_CONDUCTOR_LOCAL_THEORY.md",
        REPOSITORY_ROOT / "src" / "m3_local_units.py",
    ]
    input_hashes = {
        str(path.relative_to(REPOSITORY_ROOT)): _sha256(path)
        for path in input_paths
    }
    if REQUEST_PATH.is_file():
        input_hashes[str(REQUEST_PATH.relative_to(REPOSITORY_ROOT))] = _sha256(REQUEST_PATH)

    elapsed = time.perf_counter() - started
    utc = datetime.now(timezone.utc).isoformat()
    commit = _commit()
    software = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "module": "src/m3_local_units.py",
    }
    return {
        "experiment_id": "M3-local-unit-character-law-gate",
        "utc": utc,
        "UTC": utc,
        "source_commit": commit,
        "commit": commit,
        "software": software,
        "software_versions": software,
        "input_hashes": input_hashes,
        "runtime_seconds": elapsed,
        "agent": "/root/m3_local_units",
        "verification_scope": [
            "exact orders and element-order profiles of U^1/U^nu",
            "exact cyclic factor decomposition and 2-rank",
            "valuation filtration subgroup sizes",
            "full abelian character cumulative and exact conductor counts",
            "order-two Artin-Schreier character cumulative and exact counts",
            "exact full and Artin-Schreier average conductors",
            "adversarial mutation rejection for degree, depth, rank, exponent, and order",
        ],
        "enumeration": {
            "method": "direct truncated-series multiplication over F_(2^f)",
            "group_order_cap": MAX_ENUMERATED_GROUP_ORDER,
            "fixtures": [[f, nu] for f, nu in FIXTURES],
            "production_search": "NOT RUN",
        },
        "fixtures": fixture_reports,
        "adversarial_mutations": mutation_statuses,
        "all_formula_checks_passed": all_passed,
        "all_mutation_checks_rejected": all(
            status == "REJECTED"
            for fields in mutation_statuses.values()
            for status in fields.values()
        ),
        "verification_status": (
            "PASS" if all_passed else "FAIL"
        ),
        "exact_score": None,
        "tower_status": "NO TOWER COMPUTATION; LOCAL ARITHMETIC ONLY",
        "status": (
            "EXACT FINITE LOCAL ARITHMETIC PASS"
            if all_passed
            else "FAILED LOCAL ARITHMETIC GATE"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY_ROOT / "results" / "m3-local-units.json",
    )
    args = parser.parse_args()
    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output.relative_to(REPOSITORY_ROOT)) if args.output.is_relative_to(REPOSITORY_ROOT) else str(args.output),
        "status": report["status"],
        "runtime_seconds": report["runtime_seconds"],
    }, sort_keys=True))
    return 0 if report["all_formula_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
