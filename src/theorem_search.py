"""Exact finite searches for the binary Duursma--Mak parameter inequality.

The module deliberately separates three things which are easy to conflate in a
computer search:

* the integer sufficient criterion from Theorem 1.1;
* the rational upper bound for the conductor average; and
* the geometric work needed to exhibit the selected places.

Rows are triples ``(degree, multiplicity, nu)``.  A row describes that many
distinct places of the same degree and conductor-depth bound.  The evaluator
does no ray-class-group calculation and never turns an inventory count into a
claim about an explicit divisor.  In particular, every result returned by the
search carries a geometry proof obligation.

Only the finite ``k343`` search in :mod:`experiments.run_parameter_search` is
an experiment.  The functions below are generic for binary rows and are also
used by the small unit tests.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt
from pathlib import Path
from typing import Iterable, Mapping, Sequence


Row = tuple[int, int, int]
HistoricalBound = Fraction(24576, 77527)
K343_GENUS = 343
K343_RATIONAL_PLACES = 192
K343_MAX_DEGREE = 12
EVEN_DEPTHS = (2, 4, 6)


@dataclass(frozen=True)
class InventoryEntry:
    """A degree and the number of places available at that degree."""

    degree: int
    available: int


def _integer(value: object, name: str) -> int:
    """Return an actual integer, rejecting booleans and lossy coercions."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _coerce_row(row: object) -> Row:
    """Normalize one row, accepting a tuple/list or a named mapping."""

    if isinstance(row, Mapping):
        if "degree" not in row or "nu" not in row:
            raise ValueError("a row mapping needs degree and nu")
        multiplicity_key = (
            "multiplicity" if "multiplicity" in row else "count"
        )
        if multiplicity_key not in row:
            raise ValueError("a row mapping needs multiplicity")
        values = (row["degree"], row[multiplicity_key], row["nu"])
    else:
        try:
            values = tuple(row)  # type: ignore[arg-type]
        except TypeError as exc:
            raise ValueError("a row must be a length-three sequence") from exc
        if len(values) != 3:
            raise ValueError("a row must be a length-three sequence")

    degree = _integer(values[0], "degree")
    multiplicity = _integer(values[1], "multiplicity")
    nu = _integer(values[2], "nu")
    if degree <= 0:
        raise ValueError("degree must be positive")
    if multiplicity < 0:
        raise ValueError("multiplicity must be nonnegative")
    if nu <= 0:
        raise ValueError("nu must be positive")
    return degree, multiplicity, nu


def canonical_rows(rows: Iterable[object]) -> tuple[Row, ...]:
    """Validate rows and sort them by degree and depth.

    Zero-multiplicity rows are omitted.  Rows with the same degree and depth
    are combined, which makes equality and JSON output deterministic.  A
    repeated degree with *different* depths remains nonuniform and is kept as
    separate rows.
    """

    combined: dict[tuple[int, int], int] = {}
    for raw_row in rows:
        degree, multiplicity, nu = _coerce_row(raw_row)
        if multiplicity:
            key = (degree, nu)
            combined[key] = combined.get(key, 0) + multiplicity
    return tuple(
        (degree, multiplicity, nu)
        for (degree, nu), multiplicity in sorted(combined.items())
    )


def ceil_sqrt(value: int) -> int:
    """The exact least integer whose square is at least ``value``."""

    value = _integer(value, "value")
    if value < 0:
        raise ValueError("ceil_sqrt is undefined for negative values")
    root = isqrt(value)
    return root if root * root == value else root + 1


def optimal_t(local_dimension: int, relation_cost_twice: int,
              rational_places: int) -> int:
    """Return the largest theorem-admissible ``t`` for fixed ``A`` and ``C``.

    Here ``local_dimension`` is ``A_S`` and ``relation_cost_twice`` is
    ``C_S``.  Since ``D=1+A_S-t`` decreases with ``t``, the integer condition
    ``D**2 >= 2*C_S + 4*A_S`` gives

    ``t <= 1 + A_S - ceil_sqrt(2*C_S + 4*A_S)``.

    The result is capped by both the available rational places and ``A_S``;
    zero means that no positive ``t`` passes the sufficient criterion.
    """

    a = _integer(local_dimension, "local_dimension")
    c = _integer(relation_cost_twice, "relation_cost_twice")
    n = _integer(rational_places, "rational_places")
    if a < 0 or c < 0:
        raise ValueError("A_S and C_S must be nonnegative")
    if n < 0:
        raise ValueError("rational_places must be nonnegative")
    threshold = 1 + a - ceil_sqrt(2 * c + 4 * a)
    return max(0, min(n, a, threshold))


def binary_local_average_exponent(degree: int, nu: int) -> Fraction:
    """Certified binary filtration upper bound for a local exponent average.

    The returned value bounds ``E[a_P]`` for a place of degree ``degree``.
    It is the filtration expression from ``proofs/CONDUCTOR_FILTRATION.md``.
    Depth one has no wild p-primary contribution and is handled explicitly.
    """

    degree = _integer(degree, "degree")
    nu = _integer(nu, "nu")
    if degree <= 0 or nu <= 0:
        raise ValueError("degree and nu must be positive")
    if nu == 1:
        return Fraction(0)

    q_power = 2 ** degree
    expected = Fraction(nu, 1) - Fraction(2, q_power ** (nu - 1))
    for j in range(1, nu - 1):
        expected -= Fraction(1, q_power ** j)
    return expected


def _binary_row_terms(degree: int, nu: int) -> tuple[int, int, Fraction]:
    """Return the placewise ``A``, ``B`` and average exponent terms."""

    wild_dimension = degree * (nu - 1 - (nu - 1) // 2)
    b_term = degree * (nu - 1)
    return wild_dimension, b_term, binary_local_average_exponent(degree, nu)


def evaluate_binary(genus: int, t: int, rows: Iterable[object], *,
                    rational_places: int | None = None) -> dict:
    """Evaluate the exact binary theorem arithmetic for ``rows``.

    Parameters are intentionally arithmetic parameters.  ``rational_places``
    is optional and, when supplied, adds the finite inventory check ``t <= N``.
    The geometry of the rows, disjointness from ``T``, constant fields, and
    existence of a p-primary ray tower remain explicit proof obligations.

    The result keeps ``Fraction`` instances in Python.  The experiment writer
    converts them to strings for a JSON artifact.
    """

    genus = _integer(genus, "genus")
    t = _integer(t, "t")
    if genus <= 1:
        raise ValueError("the theorem requires genus > 1")
    if t < 0:
        raise ValueError("t must be nonnegative")
    if rational_places is not None:
        rational_places = _integer(rational_places, "rational_places")
        if rational_places < 0:
            raise ValueError("rational_places must be nonnegative")

    normalized = canonical_rows(rows)
    local_dimension = 0
    twice_local_relation_cost = 0
    average_conductor_degree = Fraction(0)
    geometry_reasons = [
        "selected places must be distinct and have the displayed degrees",
        "S must be disjoint from the t rational places in T",
        "the constant field must remain exactly F_2",
        "the p-primary T-ray tower and all theorem hypotheses require a separate proof",
    ]
    for degree, multiplicity, nu in normalized:
        a_term, b_term, expected_exponent = _binary_row_terms(degree, nu)
        local_dimension += multiplicity * a_term
        twice_local_relation_cost += (
            multiplicity * b_term * (b_term + 1)
        )
        average_conductor_degree += (
            multiplicity * degree * expected_exponent
        )

    generator_lower_bound = 1 + local_dimension - t
    gs_margin = (
        generator_lower_bound * generator_lower_bound
        - 2 * twice_local_relation_cost
        - 4 * local_dimension
    )
    relation_minus_generator_upper_bound = (
        Fraction(twice_local_relation_cost, 2) + t - 1
    )
    genus_denominator = (
        Fraction(genus - 1, 1) + average_conductor_degree / 2
    )

    failure_reasons: list[str] = []
    if t <= 0:
        failure_reasons.append("t must be positive")
    if t > local_dimension:
        failure_reasons.append("t exceeds A_S")
    if rational_places is not None and t > rational_places:
        failure_reasons.append("t exceeds the rational-place inventory")
    if gs_margin < 0:
        failure_reasons.append("GS sufficient inequality I >= 0 fails")
    theorem_passes = not failure_reasons

    result = {
        "genus": genus,
        "t": t,
        "rows": normalized,
        "p": 2,
        "q": 2,
        "constant_degree": 1,
        "local_dimension": local_dimension,
        "A": local_dimension,
        "twice_local_relation_cost": twice_local_relation_cost,
        "C": twice_local_relation_cost,
        "generator_lower_bound": generator_lower_bound,
        "D": generator_lower_bound,
        "GS_margin": gs_margin,
        "GS": gs_margin,
        "relation_minus_generator_upper_bound": relation_minus_generator_upper_bound,
        "average_conductor_degree_upper_bound": average_conductor_degree,
        "conductor_average": average_conductor_degree,
        "conductor_cost": average_conductor_degree / 2,
        "genus_denominator_upper_bound": genus_denominator,
        "ratio_lower_bound": Fraction(t, 1) / genus_denominator,
        "t_le_A": t <= local_dimension,
        "inequality_passes": theorem_passes,
        "theorem_passes": theorem_passes,
        "failure_reasons": failure_reasons,
        "geometry_status": "EXPLICIT PROOF OBLIGATION",
        "geometry_obligations": geometry_reasons,
        "status": "EXACT RATIONAL",
    }
    if rational_places is not None:
        result["rational_places"] = rational_places
    return result


def evaluate_rows(rows: Iterable[object], genus: int, t: int, *,
                  rational_places: int | None = None) -> dict:
    """Rows-first alias for callers that naturally start with a row list."""

    return evaluate_binary(
        genus, t, rows, rational_places=rational_places
    )


def _normalize_inventory(
    inventory: Mapping[object, object] | Iterable[object],
) -> tuple[InventoryEntry, ...]:
    """Validate an inventory supplied as a mapping or ``(degree,count)`` rows."""

    if isinstance(inventory, Mapping):
        raw_entries = inventory.items()
    else:
        raw_entries = inventory

    entries: dict[int, int] = {}
    for raw in raw_entries:
        if isinstance(inventory, Mapping):
            degree_value, available_value = raw  # type: ignore[misc]
        elif isinstance(raw, InventoryEntry):
            degree_value, available_value = raw.degree, raw.available
        elif isinstance(raw, Mapping):
            if "degree" not in raw:
                raise ValueError("inventory mapping needs degree")
            if "available" in raw:
                available_key = "available"
            elif "count" in raw:
                available_key = "count"
            else:
                raise ValueError("inventory mapping needs available")
            degree_value, available_value = raw["degree"], raw[available_key]
        else:
            try:
                pair = tuple(raw)  # type: ignore[arg-type]
            except TypeError as exc:
                raise ValueError("inventory rows need degree and available") from exc
            if len(pair) != 2:
                raise ValueError("inventory rows need degree and available")
            degree_value, available_value = pair

        degree = _integer(degree_value, "inventory degree")
        available = _integer(available_value, "inventory count")
        if degree <= 1:
            raise ValueError("the theorem search inventory must be nonrational")
        if available < 0:
            raise ValueError("inventory counts must be nonnegative")
        entries[degree] = entries.get(degree, 0) + available

    return tuple(
        InventoryEntry(degree, available)
        for degree, available in sorted(entries.items())
        if available
    )


def load_inventory(path: str | Path, *, max_degree: int = K343_MAX_DEGREE,
                   nonrational_only: bool = True) -> tuple[InventoryEntry, ...]:
    """Load the certified place-count inventory, optionally truncating degree."""

    max_degree = _integer(max_degree, "max_degree")
    if max_degree <= 1:
        raise ValueError("max_degree must exceed one")
    inventory_path = Path(path)
    with inventory_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, Mapping) or "place_counts" not in payload:
        raise ValueError("inventory JSON needs a place_counts array")
    counts = payload["place_counts"]
    if not isinstance(counts, Sequence) or isinstance(counts, (str, bytes)):
        raise ValueError("place_counts must be an array")
    declared_max = payload.get("degree_max", len(counts))
    declared_max = _integer(declared_max, "degree_max")
    upper = min(max_degree, declared_max, len(counts))
    entries = []
    for degree in range(1, upper + 1):
        available = _integer(counts[degree - 1], f"place_counts[{degree - 1}]")
        if available < 0:
            raise ValueError("inventory counts must be nonnegative")
        if available and (not nonrational_only or degree > 1):
            entries.append(InventoryEntry(degree, available))
    return tuple(entries)


def _inventory_records(inventory: tuple[InventoryEntry, ...]) -> list[dict]:
    return [
        {"degree": entry.degree, "available": entry.available}
        for entry in inventory
    ]


def _default_inventory_path() -> Path:
    return Path(__file__).resolve().parents[1] / "curves" / "k343-place-counts-30.json"


def _cost_units_nu2(degree: int, scale: int) -> int:
    """Cost ``degree*(1-2**(-degree))`` in units of ``1/scale``."""

    denominator = 2 ** degree
    if scale % denominator:
        raise ValueError("scale must be divisible by every 2**degree")
    return degree * (scale - scale // denominator)


def historical_cost_threshold(genus: int, rational_places: int,
                              incumbent: Fraction = HistoricalBound) -> Fraction:
    """Necessary strict cost threshold for beating an incumbent ratio.

    Every candidate has ``t <= rational_places``.  Therefore a strict
    improvement over ``incumbent`` requires

    ``cost < rational_places/incumbent - (genus - 1)``.

    This is a necessary condition only; using it to prune a branch is sound
    because conductor costs are nonnegative and extensions can only increase a
    partial cost.
    """

    genus = _integer(genus, "genus")
    rational_places = _integer(rational_places, "rational_places")
    if genus <= 1 or rational_places < 0:
        raise ValueError("invalid genus or rational-place count")
    if not isinstance(incumbent, Fraction) or incumbent <= 0:
        raise ValueError("incumbent must be a positive Fraction")
    return Fraction(rational_places, 1) / incumbent - (genus - 1)


def _ratio_from_units(t: int, genus: int, cost_units: int,
                      scale: int) -> Fraction:
    return Fraction(t * scale, (genus - 1) * scale + cost_units)


def _candidate_from_vector(
    vector: tuple[int, ...], inventory: tuple[InventoryEntry, ...], *,
    genus: int, rational_places: int, cost_units: int, scale: int,
    t: int | None = None,
) -> dict:
    rows = tuple(
        (entry.degree, multiplicity, 2)
        for entry, multiplicity in zip(inventory, vector)
        if multiplicity
    )
    a_value = sum(multiplicity * entry.degree
                  for entry, multiplicity in zip(inventory, vector))
    c_value = sum(multiplicity * entry.degree * (entry.degree + 1)
                  for entry, multiplicity in zip(inventory, vector))
    if t is None:
        t = optimal_t(a_value, c_value, rational_places)
    evaluation = evaluate_binary(
        genus, t, rows, rational_places=rational_places
    )
    evaluation["multiplicity_vector"] = {
        str(entry.degree): multiplicity
        for entry, multiplicity in zip(inventory, vector)
    }
    evaluation["cost_units_scale"] = scale
    evaluation["cost_units"] = cost_units
    evaluation["ratio_from_units"] = _ratio_from_units(
        t, genus, cost_units, scale
    )
    return evaluation


def search_nu2(
    *,
    genus: int = K343_GENUS,
    rational_places: int = K343_RATIONAL_PLACES,
    inventory: Mapping[object, object] | Iterable[object] | None = None,
    inventory_path: str | Path | None = None,
    incumbent: Fraction = HistoricalBound,
    prune: bool = True,
) -> dict:
    """Exhaustively search ``nu=2`` multiplicities with exact cost pruning.

    The default inventory is the certified ``k343`` place-count JSON truncated
    at degree 12.  A branch is pruned only when its current conductor cost is
    already at least ``N/incumbent-(g-1)``.  Such a branch cannot beat the
    incumbent even if all remaining multiplicities are zero, so this does not
    remove a possible strict improvement.  With the default data the one
    automatically found best vector is therefore a finite-box optimum once a
    strict improvement is found.

    ``prune=False`` is provided for small brute-force tests and audits.  It
    evaluates every multiplicity vector.
    """

    genus = _integer(genus, "genus")
    rational_places = _integer(rational_places, "rational_places")
    if genus <= 1 or rational_places < 0:
        raise ValueError("invalid genus or rational-place count")
    if inventory is not None and inventory_path is not None:
        raise ValueError("supply inventory or inventory_path, not both")
    if inventory is None:
        if inventory_path is None:
            inventory_path = _default_inventory_path()
        inventory_entries = load_inventory(inventory_path, max_degree=K343_MAX_DEGREE)
    else:
        inventory_entries = _normalize_inventory(inventory)
    if not inventory_entries:
        raise ValueError("the search inventory is empty")

    scale = 1 << max(entry.degree for entry in inventory_entries)
    cost_units_by_degree = tuple(
        _cost_units_nu2(entry.degree, scale)
        for entry in inventory_entries
    )
    counts = tuple(entry.available for entry in inventory_entries)
    suffix_products = [1] * (len(counts) + 1)
    for index in range(len(counts) - 1, -1, -1):
        suffix_products[index] = suffix_products[index + 1] * (counts[index] + 1)
    total_configurations = suffix_products[0]

    threshold = historical_cost_threshold(
        genus, rational_places, incumbent
    )
    threshold_num = threshold.numerator
    threshold_den = threshold.denominator

    stats = {
        "total_configurations": total_configurations,
        "cost_pruned_configurations": 0,
        "cost_pruned_branches": 0,
        "evaluated_configurations": 0,
        "accepted_configurations": 0,
        "rejected_configurations": 0,
        "no_feasible_t": 0,
        "gs_failures": 0,
        "beats_incumbent": 0,
        "ties_incumbent": 0,
    }
    best_vector: tuple[int, ...] | None = None
    best_t = 0
    best_ratio: Fraction | None = None
    best_cost_units = 0

    def visit(index: int, vector: list[int], a_value: int,
              c_value: int, cost_units: int) -> None:
        nonlocal best_vector, best_t, best_ratio, best_cost_units

        if index == len(counts):
            stats["evaluated_configurations"] += 1
            t_value = optimal_t(a_value, c_value, rational_places)
            if t_value <= 0:
                stats["no_feasible_t"] += 1
                stats["rejected_configurations"] += 1
                return

            d_value = 1 + a_value - t_value
            gs_value = d_value * d_value - 2 * c_value - 4 * a_value
            if gs_value < 0 or t_value > a_value:
                # The formula for optimal_t normally makes this impossible;
                # keep the check here so a future variant cannot silently
                # promote a failed sufficient criterion.
                stats["gs_failures"] += 1
                stats["rejected_configurations"] += 1
                return

            stats["accepted_configurations"] += 1
            ratio = _ratio_from_units(
                t_value, genus, cost_units, scale
            )
            if ratio > incumbent:
                stats["beats_incumbent"] += 1
            elif ratio == incumbent:
                stats["ties_incumbent"] += 1

            vector_tuple = tuple(vector)
            if (
                best_ratio is None
                or ratio > best_ratio
                or (ratio == best_ratio and vector_tuple < best_vector)
            ):
                best_ratio = ratio
                best_vector = vector_tuple
                best_t = t_value
                best_cost_units = cost_units
            return

        entry = inventory_entries[index]
        degree = entry.degree
        cost_term = cost_units_by_degree[index]
        for multiplicity in range(entry.available + 1):
            next_cost = cost_units + multiplicity * cost_term
            if prune and (
                next_cost * threshold_den >= scale * threshold_num
            ):
                # Cost grows strictly with multiplicity, so every later
                # choice at this degree is cut by the same certificate.
                remaining = entry.available - multiplicity + 1
                stats["cost_pruned_branches"] += remaining
                stats["cost_pruned_configurations"] += remaining * suffix_products[index + 1]
                break
            vector.append(multiplicity)
            visit(
                index + 1,
                vector,
                a_value + multiplicity * degree,
                c_value + multiplicity * degree * (degree + 1),
                next_cost,
            )
            vector.pop()

    visit(0, [], 0, 0, 0)

    best = None
    if best_vector is not None:
        best = _candidate_from_vector(
            best_vector,
            inventory_entries,
            genus=genus,
            rational_places=rational_places,
            cost_units=best_cost_units,
            scale=scale,
            t=best_t,
        )

    return {
        "genus": genus,
        "rational_places": rational_places,
        "inventory": _inventory_records(inventory_entries),
        "inventory_path": str(inventory_path) if inventory_path is not None else None,
        "depth": 2,
        "incumbent": incumbent,
        "cost_threshold_for_strict_improvement": threshold,
        "pruning": {
            "enabled": prune,
            "rule": "prune a partial branch when conductor cost >= N/incumbent-(g-1)",
            "comparison": "strict; equality cannot beat the incumbent",
            "sound": True,
            "cost_units_scale": scale,
        },
        "stats": stats,
        "best": best,
        "status": "EXACT FINITE SEARCH; GEOMETRY OBLIGATIONS OPEN",
        "proof_obligations": [
            "place counts certify availability, but every selected S place must be exhibited and distinct",
            "T must be an explicit set of t rational places disjoint from S",
            "the constant field and p-primary T-ray tower hypotheses are not computed by this search",
            "a finite-box optimum does not assert an optimum over other curves, degrees, depths, or the unrestricted family",
        ],
    }


def _base_vector_from_result(base: Mapping[object, object],
                             inventory: tuple[InventoryEntry, ...]) -> tuple[int, ...]:
    raw = base.get("multiplicity_vector")
    if raw is None:
        raw = base.get("vector")
    if isinstance(raw, Mapping):
        values = []
        for entry in inventory:
            value = raw.get(str(entry.degree), raw.get(entry.degree, 0))
            values.append(_integer(value, f"base multiplicity for degree {entry.degree}"))
        return tuple(values)
    if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
        values = tuple(_integer(value, "base multiplicity") for value in raw)
        if len(values) != len(inventory):
            raise ValueError("base vector does not match the inventory")
        return values
    rows = base.get("rows")
    if rows is not None:
        by_degree = {entry.degree: 0 for entry in inventory}
        for degree, multiplicity, nu in canonical_rows(rows):
            if nu != 2:
                raise ValueError("a base vector for local search must be nu=2")
            if degree not in by_degree:
                raise ValueError("base rows contain a degree outside the inventory")
            by_degree[degree] += multiplicity
        return tuple(by_degree[entry.degree] for entry in inventory)
    raise ValueError("base result needs multiplicity_vector, vector, or rows")


def _uniform_local_rows(
    vector: tuple[int, ...], inventory: tuple[InventoryEntry, ...],
    depths: tuple[int, ...],
) -> tuple[Row, ...]:
    return tuple(
        (entry.degree, multiplicity, depth)
        for entry, multiplicity, depth in zip(inventory, vector, depths)
        if multiplicity
    )


def _single_exception_rows(
    vector: tuple[int, ...], inventory: tuple[InventoryEntry, ...],
    exceptional_index: int, exceptional_depth: int,
) -> tuple[Row, ...]:
    rows: list[Row] = []
    for index, (entry, multiplicity) in enumerate(zip(inventory, vector)):
        if not multiplicity:
            continue
        if index == exceptional_index:
            if multiplicity > 1:
                rows.append((entry.degree, multiplicity - 1, 2))
            rows.append((entry.degree, 1, exceptional_depth))
        else:
            rows.append((entry.degree, multiplicity, 2))
    return canonical_rows(rows)


def search_nonuniform_even_neighborhood(
    base: Mapping[object, object],
    inventory: Mapping[object, object] | Iterable[object],
    *,
    genus: int = K343_GENUS,
    rational_places: int = K343_RATIONAL_PLACES,
    depths: tuple[int, ...] = EVEN_DEPTHS,
) -> dict:
    """Search a bounded local neighborhood with even depths 2, 4 and 6.

    The scope is intentionally finite and explicit:

    1. each degree's multiplicity may move independently by at most one from
       the supplied auto-best vector, clipped to its inventory count;
    2. for every such vector, all per-degree *uniform* choices from
       ``depths`` are enumerated; and
    3. the same vectors are also tested with one exceptional selected place at
       one degree changed from depth 2 to 4 or 6.

    The last family allows a genuinely nonuniform row at one degree while
    keeping the neighborhood bounded.  It is not a search over arbitrary
    depth assignments or arbitrary multiplicity perturbations.
    """

    if not isinstance(base, Mapping):
        raise ValueError("base must be the automatically found candidate result")
    inventory_entries = _normalize_inventory(inventory)
    depth_values = tuple(_integer(depth, "depth") for depth in depths)
    if not depth_values or any(depth <= 0 or depth % 2 for depth in depth_values):
        raise ValueError("depths must be positive even integers")
    if 2 not in depth_values or 4 not in depth_values or 6 not in depth_values:
        raise ValueError("the bounded neighborhood requires depths 2, 4 and 6")

    base_vector = _base_vector_from_result(base, inventory_entries)
    for entry, multiplicity in zip(inventory_entries, base_vector):
        if multiplicity < 0 or multiplicity > entry.available:
            raise ValueError("base multiplicity exceeds its inventory")

    multiplicity_options = tuple(
        range(max(0, multiplicity - 1),
              min(entry.available, multiplicity + 1) + 1)
        for entry, multiplicity in zip(inventory_entries, base_vector)
    )

    variants: set[tuple[Row, ...]] = set()
    uniform_variants = 0
    exceptional_variants = 0
    for vector in product(*multiplicity_options):
        nonzero_indices = [index for index, multiplicity in enumerate(vector)
                           if multiplicity]
        for chosen_depths in product(depth_values, repeat=len(inventory_entries)):
            variants.add(_uniform_local_rows(vector, inventory_entries, chosen_depths))
            uniform_variants += 1
        for index in nonzero_indices:
            for exceptional_depth in (4, 6):
                variants.add(_single_exception_rows(
                    vector, inventory_entries, index, exceptional_depth
                ))
                exceptional_variants += 1

    multiplicity_vector_count = 1
    for options in multiplicity_options:
        multiplicity_vector_count *= len(options)
    stats = {
        "multiplicity_vectors": multiplicity_vector_count,
        "uniform_variants_generated": uniform_variants,
        "single_exception_variants_generated": exceptional_variants,
        "duplicate_variants_removed": uniform_variants + exceptional_variants - len(variants),
        "unique_variants": len(variants),
        "evaluated_variants": 0,
        "accepted_variants": 0,
        "no_feasible_t": 0,
        "gs_failures": 0,
        "beats_auto_best": 0,
    }

    best: dict | None = None
    best_ratio: Fraction | None = None
    for rows in sorted(variants):
        stats["evaluated_variants"] += 1
        preliminary = evaluate_binary(
            genus, 0, rows, rational_places=rational_places
        )
        t_value = optimal_t(preliminary["A"], preliminary["C"], rational_places)
        if t_value <= 0:
            stats["no_feasible_t"] += 1
            continue
        evaluation = evaluate_binary(
            genus, t_value, rows, rational_places=rational_places
        )
        if not evaluation["theorem_passes"]:
            stats["gs_failures"] += 1
            continue
        stats["accepted_variants"] += 1
        ratio = evaluation["ratio_lower_bound"]
        if base.get("ratio_lower_bound") is not None:
            auto_ratio = base["ratio_lower_bound"]
            if not isinstance(auto_ratio, Fraction):
                auto_ratio = Fraction(str(auto_ratio))
            if ratio > auto_ratio:
                stats["beats_auto_best"] += 1
        if best_ratio is None or ratio > best_ratio:
            best_ratio = ratio
            best = evaluation

    return {
        "base_vector": {
            str(entry.degree): multiplicity
            for entry, multiplicity in zip(inventory_entries, base_vector)
        },
        "inventory": _inventory_records(inventory_entries),
        "depths": depth_values,
        "scope": [
            "each inventory multiplicity is independently varied over base-1, base, base+1, clipped to availability",
            "all per-degree uniform depth assignments in {2,4,6}",
            "one exceptional place at one degree may have depth 4 or 6 while all other selected places have depth 2",
        ],
        "stats": stats,
        "best": best,
        "status": "BOUNDED LOCAL EXACT SEARCH; GEOMETRY OBLIGATIONS OPEN",
        "proof_obligations": [
            "the neighborhood is exploratory and does not prove a result outside its finite scope",
            "selected places, disjoint T, exact constants, and the p-primary tower remain to be certified",
            "odd depths are excluded here because the filtration proof records their conservative domination by the preceding even depth",
        ],
    }


# A shorter spelling is useful in notebooks and keeps the public API obvious.
search_nonuniform_neighborhood = search_nonuniform_even_neighborhood


__all__ = [
    "EVEN_DEPTHS",
    "HistoricalBound",
    "InventoryEntry",
    "K343_GENUS",
    "K343_MAX_DEGREE",
    "K343_RATIONAL_PLACES",
    "binary_local_average_exponent",
    "canonical_rows",
    "ceil_sqrt",
    "evaluate_binary",
    "evaluate_rows",
    "historical_cost_threshold",
    "load_inventory",
    "optimal_t",
    "search_nonuniform_even_neighborhood",
    "search_nonuniform_neighborhood",
    "search_nu2",
]
