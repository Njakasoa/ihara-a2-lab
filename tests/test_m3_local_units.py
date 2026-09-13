"""Exact local-unit and character-law tests for M3."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from m3_local_units import (  # noqa: E402
    BinaryField,
    duursma_mak_local_terms,
    exponent_two_character_average_conductor,
    exponent_two_character_cumulative_counts,
    exponent_two_character_exact_counts,
    full_character_average_conductor,
    full_character_cumulative_counts,
    full_character_exact_counts,
    full_character_filtration_formula,
    local_rebate,
    local_unit_cyclic_factors,
    local_unit_exponent,
    local_unit_layer_dimensions,
    local_unit_order,
    local_unit_p_rank,
    local_unit_structure,
    multiply_truncated_units,
    truncated_unit_elements,
    validate_structure_record,
    valuation_layer_dimensions,
    verify_local_formula,
)


class LocalUnitFormulaTests(unittest.TestCase):
    def test_order_rank_and_cyclic_decomposition(self):
        fixtures = (
            (1, 1, 1, 0, {}),
            (1, 2, 2, 1, {1: 1}),
            (1, 3, 4, 1, {2: 1}),
            (1, 4, 8, 2, {1: 1, 2: 1}),
            (1, 6, 32, 3, {1: 2, 3: 1}),
            (2, 4, 64, 4, {1: 2, 2: 2}),
        )
        for f, nu, order, rank, factors in fixtures:
            with self.subTest(f=f, nu=nu):
                self.assertEqual(local_unit_order(f, nu), order)
                self.assertEqual(local_unit_p_rank(f, nu), rank)
                self.assertEqual(local_unit_cyclic_factors(f, nu), factors)
                self.assertEqual(local_unit_exponent(f, nu), max(
                    [1] + [2 ** exponent for exponent in factors]
                ))

    def test_successive_valuation_and_killed_layers_are_distinct_data(self):
        self.assertEqual(valuation_layer_dimensions(1, 6), (1, 1, 1, 1, 1))
        self.assertEqual(local_unit_layer_dimensions(1, 6), (3, 1, 1))
        self.assertEqual(local_unit_layer_dimensions(2, 5), (4, 2, 2))
        self.assertEqual(local_unit_p_rank(2, 5), 4)

    def test_full_and_artin_schreier_character_laws(self):
        self.assertEqual(
            full_character_cumulative_counts(2, 4),
            (1, 1, 4, 16, 64),
        )
        self.assertEqual(
            full_character_exact_counts(2, 4),
            (1, 0, 3, 12, 48),
        )
        self.assertEqual(full_character_average_conductor(2, 4),
                         Fraction(117, 32))
        self.assertEqual(full_character_filtration_formula(2, 4),
                         Fraction(117, 32))

        self.assertEqual(
            exponent_two_character_cumulative_counts(2, 4),
            (1, 1, 4, 4, 16),
        )
        self.assertEqual(
            exponent_two_character_exact_counts(2, 4),
            (1, 0, 3, 0, 12),
        )
        self.assertEqual(exponent_two_character_average_conductor(2, 4),
                         Fraction(27, 8))

        # At depth three, order-four characters exist in the full group but
        # are absent from the Artin--Schreier quotient.
        self.assertEqual(full_character_exact_counts(1, 3), (1, 0, 1, 2))
        self.assertEqual(exponent_two_character_exact_counts(1, 3),
                         (1, 0, 1, 0))

    def test_direct_truncated_series_gate(self):
        for f, nu in (
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 4),
            (3, 5),
        ):
            with self.subTest(f=f, nu=nu):
                checked = verify_local_formula(f, nu)
                self.assertTrue(checked["passed"], checked)
                self.assertTrue(all(checked["checks"].values()))

    def test_direct_multiplier_is_truncated_convolution(self):
        field = BinaryField(1, 0b11)
        # (1 + pi)^2 = 1 + pi^2 modulo pi^3.
        self.assertEqual(
            multiply_truncated_units((1, 0), (1, 0), 1, 3, field=field),
            (0, 1),
        )
        # The pi^2 and pi^3 coefficients include direct and cross terms.
        self.assertEqual(
            multiply_truncated_units((1, 1, 0), (1, 1, 1), 1, 4,
                                     field=field),
            (0, 1, 1),
        )
        elements = truncated_unit_elements(1, 4)
        identity = (0, 0, 0)
        for left in elements:
            self.assertEqual(
                multiply_truncated_units(left, identity, 1, 4,
                                         field=field),
                left,
            )

    def test_duursma_mak_terms_use_rank_but_relation_bound_uses_depth(self):
        self.assertEqual(
            duursma_mak_local_terms(2, 4),
            {
                "A": 4,
                "a_local": 4,
                "b": 6,
                "C": 42,
                "c_local_bound": 42,
            },
        )
        # A depth-three row has the same A as depth two but a larger b and
        # therefore a larger relation contribution.
        self.assertEqual(duursma_mak_local_terms(1, 3)["A"], 1)
        self.assertGreater(duursma_mak_local_terms(1, 3)["C"],
                           duursma_mak_local_terms(1, 2)["C"])

    def test_odd_depth_is_dominated_by_previous_even_depth(self):
        for f in (1, 2, 3, 5):
            for s in (1, 2, 3):
                with self.subTest(f=f, s=s):
                    q = 2 ** f
                    difference = (
                        full_character_average_conductor(f, 2 * s + 1)
                        - full_character_average_conductor(f, 2 * s)
                    )
                    self.assertEqual(
                        difference,
                        Fraction(1, 1) + Fraction(q - 2, q ** (2 * s)),
                    )
                    self.assertEqual(
                        local_unit_p_rank(f, 2 * s + 1),
                        local_unit_p_rank(f, 2 * s),
                    )

    def test_rebate_formula_and_depth_two_equality(self):
        for f in (1, 2, 3, 5):
            for s in (1, 2, 3):
                with self.subTest(f=f, s=s):
                    q = 2 ** f
                    rebate = local_rebate(f, 2 * s)
                    self.assertLessEqual(rebate, Fraction(f, q))
                    expected_gap = Fraction(
                        f * (q - 2) * (1 - Fraction(1, q ** (2 * s - 2))),
                        2 * q * (q - 1),
                    )
                    self.assertEqual(Fraction(f, q) - rebate,
                                     expected_gap)
        self.assertEqual(local_rebate(1, 2), Fraction(1, 2))
        self.assertEqual(local_rebate(1, 8), Fraction(1, 2))
        self.assertEqual(local_rebate(2, 4), Fraction(11, 32))

    def test_malformed_inputs_and_cap_are_rejected(self):
        for f, nu in ((0, 2), (-1, 2), (1, 0), (True, 2), (1, False)):
            with self.subTest(f=f, nu=nu):
                with self.assertRaises(ValueError):
                    local_unit_structure(f, nu)
        with self.assertRaises(ValueError):
            truncated_unit_elements(2, 8, cap=4096)
        with self.assertRaises(ValueError):
            BinaryField(2, 0b10101)

    def test_adversarial_structure_mutations_are_rejected(self):
        record = local_unit_structure(2, 4).as_dict()
        self.assertTrue(validate_structure_record(record))
        for field in ("f", "nu", "p_rank", "exponent", "order"):
            mutated = deepcopy(record)
            mutated[field] += 1
            with self.subTest(field=field):
                self.assertFalse(validate_structure_record(mutated))
        mutated = deepcopy(record)
        mutated["cyclic_factors"]["1"] += 1
        self.assertFalse(validate_structure_record(mutated))

    def test_saved_experiment_has_local_scope_and_no_score(self):
        path = ROOT / "results" / "m3-local-units.json"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertIsNone(payload["exact_score"])
        self.assertEqual(payload["tower_status"],
                         "NO TOWER COMPUTATION; LOCAL ARITHMETIC ONLY")
        self.assertTrue(payload["all_formula_checks_passed"])
        self.assertTrue(payload["all_mutation_checks_rejected"])
        self.assertIn("utc", payload)
        self.assertIn("UTC", payload)
        self.assertIn("source_commit", payload)
        self.assertIn("commit", payload)
        self.assertIn("input_hashes", payload)
        self.assertIn("runtime_seconds", payload)
        self.assertIn("software_versions", payload)
        self.assertIn("agent", payload)


if __name__ == "__main__":
    unittest.main()
