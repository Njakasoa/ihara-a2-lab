"""Small exact audits for the M2 theorem-parameter engine."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from theorem_search import (  # noqa: E402
    HistoricalBound,
    binary_local_average_exponent,
    ceil_sqrt,
    evaluate_binary,
    load_inventory,
    optimal_t,
    search_nonuniform_even_neighborhood,
    search_nu2,
)


class TheoremSearchTests(unittest.TestCase):
    def test_published_binary_arithmetic_is_exact(self):
        result = evaluate_binary(
            343,
            192,
            [(5, 2, 2), (6, 16, 2), (8, 15, 2), (10, 4, 2)],
            rational_places=192,
        )
        self.assertEqual(result["A"], 266)
        self.assertEqual(result["C"], 2252)
        self.assertEqual(result["D"], 75)
        self.assertEqual(result["GS"], 57)
        self.assertEqual(result["conductor_cost"], Fraction(33751, 128))
        self.assertEqual(result["genus_denominator_upper_bound"], Fraction(77527, 128))
        self.assertEqual(result["ratio_lower_bound"], HistoricalBound)
        self.assertTrue(result["theorem_passes"])

    def test_filtration_formula_supports_even_nonuniform_depths(self):
        # For q=2 and degree 2, the depth-four expression is
        # 4 - 2/2**6 - 1/2**2 - 1/2**4.
        self.assertEqual(
            binary_local_average_exponent(2, 4),
            Fraction(4, 1) - Fraction(2, 2**6)
            - Fraction(1, 2**2) - Fraction(1, 2**4),
        )
        result = evaluate_binary(20, 1, [(2, 1, 4), (3, 1, 6)])
        self.assertEqual(result["A"], 4 + 3 * (5 - 2))
        self.assertGreater(result["conductor_cost"], Fraction(0))

    def test_optimal_t_matches_direct_integer_brute_force(self):
        self.assertEqual(ceil_sqrt(0), 0)
        self.assertEqual(ceil_sqrt(1), 1)
        self.assertEqual(ceil_sqrt(2), 2)
        self.assertEqual(ceil_sqrt(9), 3)
        for rows in (
            (),
            ((2, 1, 2),),
            ((2, 2, 2), (3, 1, 4)),
            ((5, 1, 6), (6, 2, 2)),
        ):
            unrestricted = evaluate_binary(30, 0, rows)
            a_value, c_value = unrestricted["A"], unrestricted["C"]
            expected = 0
            for t_value in range(1, 13):
                candidate = evaluate_binary(30, t_value, rows,
                                             rational_places=12)
                if candidate["theorem_passes"]:
                    expected = t_value
            self.assertEqual(optimal_t(a_value, c_value, 12), expected)

    def test_pruned_search_matches_unpruned_small_box(self):
        inventory = [(2, 3), (4, 3), (6, 3)]
        full = search_nu2(
            genus=10,
            rational_places=8,
            inventory=inventory,
            incumbent=Fraction(1, 100),
            prune=False,
        )
        self.assertEqual(full["stats"]["evaluated_configurations"], 64)
        full_best = full["best"]
        self.assertIsNotNone(full_best)
        # Choose an incumbent just below the unpruned winner.  Some expensive
        # completions are then safely pruned, while the winner remains eligible.
        better_than = full_best["ratio_lower_bound"] * Fraction(99, 100)
        pruned = search_nu2(
            genus=10,
            rational_places=8,
            inventory=inventory,
            incumbent=better_than,
            prune=True,
        )
        self.assertGreater(pruned["stats"]["cost_pruned_configurations"], 0)
        self.assertEqual(
            pruned["best"]["ratio_lower_bound"],
            full_best["ratio_lower_bound"],
        )
        self.assertEqual(
            pruned["best"]["multiplicity_vector"],
            full_best["multiplicity_vector"],
        )

    def test_certified_k343_box_discovers_winner(self):
        result = search_nu2()
        self.assertEqual(result["stats"]["total_configurations"], 11778195)
        self.assertEqual(result["stats"]["evaluated_configurations"], 99835)
        self.assertEqual(result["stats"]["cost_pruned_configurations"], 11678360)
        self.assertEqual(
            result["best"]["multiplicity_vector"],
            {"5": 2, "6": 16, "8": 16, "10": 2, "12": 1},
        )
        self.assertEqual(result["best"]["ratio_lower_bound"], Fraction(196608, 620201))

    def test_failed_sufficient_criterion_is_reported(self):
        # This is a valid arithmetic input whose theorem criterion fails;
        # it must not be turned into a claim that a tower is finite.
        result = evaluate_binary(
            343, 5, [(2, 1, 2)], rational_places=192
        )
        self.assertFalse(result["theorem_passes"])
        self.assertIn("t exceeds A_S", result["failure_reasons"])
        self.assertIn("GS sufficient inequality I >= 0 fails",
                      result["failure_reasons"])
        self.assertFalse(evaluate_binary(343, 0, [(2, 1, 2)])[
            "theorem_passes"
        ])

    def test_malformed_rows_are_rejected(self):
        malformed = (
            [(0, 1, 2)],
            [(2, -1, 2)],
            [(2, 1, 0)],
            [(2, 1)],
            [{"degree": 2, "multiplicity": 1}],
        )
        for rows in malformed:
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError):
                    evaluate_binary(20, 1, rows)
        with self.assertRaises(ValueError):
            search_nu2(genus=20, rational_places=8, inventory=[(1, 2)])

    def test_inventory_truncation_and_local_neighborhood(self):
        path = ROOT / "curves" / "k343-place-counts-30.json"
        inventory = load_inventory(path, max_degree=12)
        self.assertEqual(
            [(entry.degree, entry.available) for entry in inventory],
            [(5, 2), (6, 16), (8, 16), (10, 64), (12, 208)],
        )
        local = search_nonuniform_even_neighborhood(
            {"multiplicity_vector": {"2": 1, "4": 1},
             "ratio_lower_bound": Fraction(1, 100)},
            [(2, 2), (4, 2)],
            genus=10,
            rational_places=8,
        )
        self.assertGreater(local["stats"]["unique_variants"], 0)
        self.assertEqual(
            local["stats"]["evaluated_variants"],
            local["stats"]["unique_variants"],
        )


if __name__ == "__main__":
    unittest.main()
