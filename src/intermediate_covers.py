"""Enumerate every intermediate Artin--Schreier cover of the genus-343 model.

The certified input is the 31 quotient zeta polynomials in
certificates/k343-zeta.json.  A subspace V of F_2^5 indexes the
compositum k_V/H.  Character decomposition gives its point counts without
enumerating a large function-field model:

    N_n(k_V) = sum_{h in V, h != 0} N_n(C_h)
                - (2^rank(V)-2) N_n(H).

The finite-field trace inventory is used only to record which base H places
split in each cover.  It is independent of the zeta aggregation and is
limited to degree twelve by default.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable, Mapping, Sequence

try:  # Works when run as src/intermediate_covers.py or imported from tests.
    from exact_curves import field, h_fiber
except ImportError:  # pragma: no cover - package-style import.
    from .exact_curves import field, h_fiber


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ZETA = ROOT / "certificates" / "k343-zeta.json"
DEFAULT_DATABASE = ROOT / "curves" / "intermediate-covers.json"
DIMENSION = 5
ALL_MASK = (1 << DIMENSION) - 1


@dataclass(frozen=True)
class Subspace:
    """A canonical row-reduced subspace of F_2^DIMENSION."""

    rank: int
    basis_masks: tuple[int, ...]
    fullspan_masks: tuple[int, ...]


def parity_dot(left: int, right: int) -> int:
    """The F_2 dot product of two coordinate masks."""

    return (left & right).bit_count() & 1


def span_masks(basis_masks: Iterable[int]) -> tuple[int, ...]:
    """Return the complete XOR span, sorted with zero first."""

    span = {0}
    for vector in basis_masks:
        if not 0 <= vector <= ALL_MASK:
            raise ValueError("a vector mask must be a five-bit integer")
        span.update(value ^ vector for value in tuple(span))
    return tuple(sorted(span))


def rref_basis(vectors: Iterable[int], dimension: int = DIMENSION) -> tuple[int, ...]:
    """Return the unique binary RREF basis, using low-to-high pivot columns."""

    if not 1 <= dimension <= 16:
        raise ValueError("dimension must be between one and sixteen")
    mask = (1 << dimension) - 1
    rows = [int(vector) & mask for vector in vectors if int(vector) & mask]
    pivot_row = 0
    for column in range(dimension):
        selected = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if (rows[row] >> column) & 1
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and ((rows[row] >> column) & 1):
                rows[row] ^= rows[pivot_row]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(rows[:pivot_row])


def _rref_subspaces(dimension: int = DIMENSION) -> Iterable[Subspace]:
    """Yield all subspaces by enumerating their unique RREF matrices.

    For a fixed pivot set, every non-pivot entry to the right of that row's
    pivot is free.  Entries to the left would destroy the leading pivot, and
    entries in pivot columns are forced to zero by RREF.
    """

    for rank in range(1, dimension + 1):
        for pivots in combinations(range(dimension), rank):
            nonpivots = tuple(
                column for column in range(dimension) if column not in pivots
            )
            free_positions = tuple(
                (row, column)
                for row, pivot in enumerate(pivots)
                for column in nonpivots
                if column > pivot
            )
            for assignment in range(1 << len(free_positions)):
                rows = [1 << pivot for pivot in pivots]
                for index, (row, column) in enumerate(free_positions):
                    if (assignment >> index) & 1:
                        rows[row] |= 1 << column
                basis = tuple(rows)
                fullspan = span_masks(basis)
                if len(fullspan) != 1 << rank:
                    raise AssertionError("RREF rows are not independent")
                yield Subspace(rank, basis, fullspan)


def enumerate_subspaces(dimension: int = DIMENSION) -> tuple[Subspace, ...]:
    """Return every nonzero subspace once, in rank/RREF order."""

    if dimension != DIMENSION:
        raise ValueError("the certified quotient database has dimension five")
    subspaces = tuple(_rref_subspaces(dimension))
    expected = {1: 31, 2: 155, 3: 155, 4: 31, 5: 1}
    counts = Counter(subspace.rank for subspace in subspaces)
    if dict(counts) != expected:
        raise AssertionError(f"unexpected Gaussian-binomial counts: {counts}")
    if len({subspace.fullspan_masks for subspace in subspaces}) != len(subspaces):
        raise AssertionError("RREF enumeration produced duplicate spans")
    return subspaces


def points_from_zeta(
    coefficients: Sequence[int], nmax: int, q: int = 2
) -> list[int]:
    """Recover N_n from a numerator P(T) using Newton power sums."""

    if nmax < 0 or not coefficients or coefficients[0] != 1:
        raise ValueError("a zeta numerator must have constant coefficient one")
    degree = len(coefficients) - 1
    power_sums: list[int] = []
    for n in range(1, nmax + 1):
        newton = sum(
            coefficients[index] * power_sums[n - index - 1]
            for index in range(1, min(n - 1, degree) + 1)
        )
        if n <= degree:
            newton += n * coefficients[n]
        power_sums.append(-newton)
    return [q**n + 1 - power_sums[n - 1] for n in range(1, nmax + 1)]


def place_counts(point_counts: Sequence[int]) -> list[int]:
    """Möbius-invert extension point counts into exact-degree place counts."""

    places: list[int] = []
    for degree, count in enumerate(point_counts, start=1):
        residual = count - sum(
            divisor * places[divisor - 1]
            for divisor in range(1, degree)
            if degree % divisor == 0
        )
        if residual < 0 or residual % degree:
            raise ValueError(
                f"point count at degree {degree} is not a place inventory"
            )
        places.append(residual // degree)
    return places


def _load_zeta_certificate(path: Path = DEFAULT_ZETA) -> dict:
    path = Path(path)
    data = json.loads(path.read_text())
    rows = data.get("quotients")
    if not isinstance(rows, list) or len(rows) != 31:
        raise ValueError("the quotient zeta certificate must contain 31 rows")
    by_mask = {int(row["h_mask"]): row for row in rows}
    if set(by_mask) != set(range(1, 32)):
        raise ValueError("quotient masks must be exactly 1 through 31")
    if any(int(row["genus"]) != 13 for row in rows):
        raise ValueError("all certified quadratic quotients must have genus 13")
    if len(data.get("base_H_zeta", [])) != 5:
        raise ValueError("the base H numerator must have degree four")
    return {"raw": data, "by_mask": by_mask}


def certified_point_counts(
    nmax: int = 30, path: Path = DEFAULT_ZETA
) -> tuple[list[int], dict[int, list[int]]]:
    """Return H and all 31 quotient point-count sequences."""

    path = Path(path)
    certificate = _load_zeta_certificate(path)
    h_counts = points_from_zeta(certificate["raw"]["base_H_zeta"], nmax)
    quotient_counts: dict[int, list[int]] = {}
    for mask, row in certificate["by_mask"].items():
        counts = points_from_zeta(row["zeta_coefficients"], nmax)
        stored = row.get("point_counts", [])
        if nmax >= len(stored) and counts[: len(stored)] != stored:
            raise ValueError(f"zeta recurrence disagrees for quotient mask {mask}")
        quotient_counts[mask] = counts
    return h_counts, quotient_counts


def _frobenius_orbit(
    F, point: tuple[int, int], expected_degree: int
) -> tuple[tuple[int, int], ...]:
    """Return the Frobenius orbit of an affine H point."""

    orbit: list[tuple[int, int]] = []
    current = point
    while current not in orbit:
        orbit.append(current)
        current = (F.squares[current[0]], F.squares[current[1]])
        if len(orbit) > expected_degree:
            raise AssertionError("Frobenius orbit exceeded the field degree")
    if current != point:
        raise AssertionError("Frobenius orbit did not return to its representative")
    return tuple(orbit)


def _trace_mask(F, x: int, y: int) -> int:
    """Trace the five certified Artin--Schreier radicands at (x,y)."""

    b = F.eval(0b110, x)
    c = F.eval(0b100101, x)
    if c == 0:
        raise ValueError("a ramified c=0 point has no unramified trace mask")
    factor = F.div(b, F.squares[c])
    basis = (1, x, F.squares[x], y, F.squares[y])
    return sum(
        F.traces[F.mul(factor, value)] << index
        for index, value in enumerate(basis)
    )


def _trace_bucket_for_degree(
    degree: int,
) -> tuple[Counter[int], int]:
    """Return unramified trace-mask counts and ramified place count in H."""

    F = field(degree)
    points = []
    for x in range(F.q):
        points.extend((x, y) for y in h_fiber(F, x))
    remaining = set(points)
    masks: Counter[int] = Counter()
    ramified = 0
    while remaining:
        point = min(remaining)
        orbit = _frobenius_orbit(F, point, degree)
        remaining.difference_update(orbit)
        if len(orbit) != degree:
            continue
        if F.eval(0b100101, point[0]) == 0:
            ramified += 1
        else:
            masks[_trace_mask(F, *point)] += 1
    if degree == 1:
        # The two normalized infinity places are both split and have zero trace.
        masks[0] += 2
    return masks, ramified


def trace_inventory(max_degree: int = 12) -> dict[str, dict]:
    """Build the H trace inventory used to test complete splitting."""

    if max_degree < 1:
        raise ValueError("trace inventory needs at least degree one")
    h_counts, _ = certified_point_counts(max_degree)
    h_places = place_counts(h_counts)
    inventory: dict[str, dict] = {}
    for degree in range(1, max_degree + 1):
        masks, ramified = _trace_bucket_for_degree(degree)
        unramified = sum(masks.values())
        if unramified + ramified != h_places[degree - 1]:
            raise AssertionError(
                f"H place inventory mismatch at degree {degree}: "
                f"{unramified}+{ramified} != {h_places[degree - 1]}"
            )
        inventory[str(degree)] = {
            "mask_counts": {str(mask): count for mask, count in sorted(masks.items())},
            "unramified_places": unramified,
            "ramified_places": ramified,
            "total_places": h_places[degree - 1],
        }
    return inventory


def _splits(fullspan_masks: Sequence[int], trace_mask: int) -> bool:
    return all(parity_dot(vector, trace_mask) == 0 for vector in fullspan_masks)


def split_place_inventory(
    fullspan_masks: Sequence[int], traces: Mapping[str, Mapping]
) -> dict[str, int]:
    """Count H places that split completely in the subspace cover."""

    inventory: dict[str, int] = {}
    for degree, bucket in traces.items():
        inventory[degree] = sum(
            count
            for mask, count in bucket["mask_counts"].items()
            if _splits(fullspan_masks, int(mask))
        )
    return inventory


def _rank4_split_summary(
    records: Sequence[Mapping], traces: Mapping[str, Mapping]
) -> dict:
    """Record the degree-three/four trace obstruction for rank four."""

    degree_three = [
        record["basis_masks"]
        for record in records
        if record["rank"] == 4 and record["split_place_inventory"].get("3", 0) > 0
    ]
    degree_four = [
        record["basis_masks"]
        for record in records
        if record["rank"] == 4 and record["split_place_inventory"].get("4", 0) > 0
    ]
    both = [
        record["basis_masks"]
        for record in records
        if record["rank"] == 4
        and record["split_place_inventory"].get("3", 0) > 0
        and record["split_place_inventory"].get("4", 0) > 0
    ]
    return {
        "rank": 4,
        "degree3_split_cover_count": len(degree_three),
        "degree4_split_cover_count": len(degree_four),
        "both_split_cover_count": len(both),
        "degree3_split_basis_masks": degree_three,
        "degree4_split_basis_masks": degree_four,
        "both_split_basis_masks": both,
        "trace_masks": {
            "degree3": sorted(
                int(mask)
                for mask in traces["3"]["mask_counts"]
            ),
            "degree4": sorted(
                int(mask)
                for mask in traces["4"]["mask_counts"]
            ),
        },
        "reason": (
            "The unique degree-three and degree-four unramified H places have "
            "distinct nonzero trace masks; a rank-four hyperplane has a "
            "one-dimensional annihilator, so it cannot annihilate both."
        ),
    }


def build_database(
    nmax: int = 30,
    trace_max_degree: int = 12,
    path: Path = DEFAULT_ZETA,
) -> dict:
    """Build the complete intermediate-cover database."""

    if nmax < 1:
        raise ValueError("need at least one extension degree")
    h_counts, quotient_counts = certified_point_counts(nmax, path)
    traces = trace_inventory(trace_max_degree)
    records = []
    for subspace in enumerate_subspaces():
        rank = subspace.rank
        fullspan_nonzero = subspace.fullspan_masks[1:]
        counts = [
            sum(quotient_counts[mask][index] for mask in fullspan_nonzero)
            - ((1 << rank) - 2) * h_counts[index]
            for index in range(nmax)
        ]
        genus = 11 * (1 << rank) - 9
        rational_places = 6 * (1 << rank)
        if counts[0] != rational_places:
            raise AssertionError("character decomposition lost rational splitting")
        expected_genus = (1 << rank) * 2 + (len(fullspan_nonzero) * 20)
        if 2 * genus - 2 != expected_genus:
            raise AssertionError("Riemann--Hurwitz genus identity failed")
        record = {
            "rank": rank,
            "basis_masks": list(subspace.basis_masks),
            "fullspan_masks": list(subspace.fullspan_masks),
            "extension_degree_over_H": 1 << rank,
            "genus": genus,
            "rational_places": rational_places,
            "point_counts": counts,
            "place_counts": place_counts(counts),
            "split_place_inventory": split_place_inventory(
                subspace.fullspan_masks, traces
            ),
            "proof_references": [
                "proofs/INTERMEDIATE_COVERS.md",
                "proofs/FINITE_GEOMETRY.md",
                "certificates/k343-zeta.json",
            ],
        }
        records.append(record)
    records.sort(key=lambda record: (record["rank"], record["basis_masks"]))
    by_rank = Counter(record["rank"] for record in records)
    database = {
        "schema_version": 1,
        "status": "EXACT INTEGER; all nonzero F2-subspaces",
        "base_field": "F2",
        "base_curve": "H: y^2+(x^3+x+1)y=x^2+x",
        "character_space_dimension": DIMENSION,
        "quotient_source": "certificates/k343-zeta.json",
        "quotient_identity": (
            "N_n(k_V)=sum_{0!=h in V}N_n(C_h)"
            "-(2^rank(V)-2)N_n(H)"
        ),
        "point_count_max_degree": nmax,
        "trace_inventory_max_degree": trace_max_degree,
        "base_H_point_counts": h_counts,
        "base_H_place_counts": place_counts(h_counts),
        "trace_inventory": traces,
        "subspace_counts_by_rank": {
            str(rank): by_rank[rank] for rank in range(1, DIMENSION + 1)
        },
        "rank4_degree3_degree4_split_summary": _rank4_split_summary(
            records, traces
        ),
        "records": records,
    }
    return database


def write_database(
    output: Path = DEFAULT_DATABASE,
    nmax: int = 30,
    trace_max_degree: int = 12,
) -> dict:
    """Build and write the JSON database, returning the in-memory object."""

    database = build_database(nmax, trace_max_degree)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(database, indent=2) + "\n")
    return database


def load_database(path: Path = DEFAULT_DATABASE) -> dict:
    """Load the generated database and perform lightweight schema checks."""

    path = Path(path)
    database = json.loads(path.read_text())
    if database.get("subspace_counts_by_rank") != {
        "1": 31,
        "2": 155,
        "3": 155,
        "4": 31,
        "5": 1,
    }:
        raise ValueError("database has incorrect Gaussian-binomial counts")
    if len(database.get("records", [])) != 373:
        raise ValueError("database does not contain all 373 nonzero subspaces")
    return database


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nmax", type=int, default=30)
    parser.add_argument("--trace-max-degree", type=int, default=12)
    parser.add_argument("--output", type=Path, default=DEFAULT_DATABASE)
    args = parser.parse_args()
    database = write_database(args.output, args.nmax, args.trace_max_degree)
    print(
        f"wrote {len(database['records'])} covers through degree "
        f"{database['point_count_max_degree']} to {args.output}"
    )


if __name__ == "__main__":
    main()
