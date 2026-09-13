import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from intermediate_covers import (  # noqa: E402
    certified_point_counts,
    enumerate_subspaces,
    load_database,
    place_counts,
    parity_dot,
    span_masks,
)


class IntermediateCovers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = load_database(ROOT / "curves" / "intermediate-covers.json")
        cls.records = cls.database["records"]

    def test_gaussian_binomial_counts(self):
        subspaces = enumerate_subspaces()
        self.assertEqual(
            Counter(subspace.rank for subspace in subspaces),
            Counter({1: 31, 2: 155, 3: 155, 4: 31, 5: 1}),
        )
        self.assertEqual(
            len({subspace.fullspan_masks for subspace in subspaces}),
            373,
        )

    def test_every_span_is_closed_and_canonical(self):
        for subspace in enumerate_subspaces():
            self.assertEqual(
                subspace.fullspan_masks,
                span_masks(subspace.basis_masks),
            )
            self.assertEqual(len(subspace.fullspan_masks), 1 << subspace.rank)
            self.assertEqual(subspace.fullspan_masks[0], 0)
            for left in subspace.fullspan_masks:
                for right in subspace.fullspan_masks:
                    self.assertIn(
                        left ^ right,
                        subspace.fullspan_masks,
                    )
            for vector in subspace.fullspan_masks:
                self.assertLessEqual(vector, 31)

    def test_rank_one_covers_agree_with_certified_quotients(self):
        _, quotient_counts = certified_point_counts(30)
        rank_one = [record for record in self.records if record["rank"] == 1]
        self.assertEqual(len(rank_one), 31)
        for record in rank_one:
            mask = record["basis_masks"][0]
            self.assertEqual(record["point_counts"], quotient_counts[mask])
            self.assertEqual(
                record["place_counts"],
                place_counts(record["point_counts"]),
            )

    def test_full_rank_agrees_with_k343_certificate(self):
        full = [record for record in self.records if record["rank"] == 5]
        self.assertEqual(len(full), 1)
        full = full[0]
        k343 = json.loads(
            (ROOT / "certificates" / "k343-zeta.json").read_text()
        )
        from_zeta = __import__(
            "intermediate_covers",
            fromlist=["points_from_zeta"],
        ).points_from_zeta(
            k343["k_zeta_coefficients"], 30
        )
        self.assertEqual(full["point_counts"], from_zeta)
        self.assertEqual(
            full["place_counts"],
            place_counts(full["point_counts"]),
        )

    def test_genus_rational_places_and_rh_for_every_record(self):
        for record in self.records:
            rank = record["rank"]
            degree = 1 << rank
            self.assertEqual(record["extension_degree_over_H"], degree)
            self.assertEqual(record["genus"], 11 * degree - 9)
            self.assertEqual(record["rational_places"], 6 * degree)
            self.assertEqual(record["point_counts"][0], 6 * degree)
            self.assertEqual(
                2 * record["genus"] - 2,
                degree * (2 * 2 - 2) + (degree - 1) * 20,
            )

    def test_place_inversion_recomposes_all_counts(self):
        for record in self.records:
            places = record["place_counts"]
            self.assertEqual(places, place_counts(record["point_counts"]))
            for n, count in enumerate(record["point_counts"], start=1):
                self.assertEqual(
                    count,
                    sum(
                        divisor * places[divisor - 1]
                        for divisor in range(1, n + 1)
                        if n % divisor == 0
                    ),
                )

    def test_rank_four_degree_three_four_trace_obstruction(self):
        summary = self.database["rank4_degree3_degree4_split_summary"]
        self.assertEqual(summary["trace_masks"], {"degree3": [18], "degree4": [24]})
        self.assertEqual(summary["degree3_split_cover_count"], 1)
        self.assertEqual(summary["degree4_split_cover_count"], 1)
        self.assertEqual(summary["both_split_cover_count"], 0)
        for record in self.records:
            if record["rank"] == 4:
                both = (
                    record["split_place_inventory"]["3"] > 0
                    and record["split_place_inventory"]["4"] > 0
                )
                self.assertFalse(both)

        # The two unique nonzero trace vectors cannot both annihilate a
        # rank-four hyperplane.  This checks the database claim directly.
        self.assertTrue(
            all(
                parity_dot(vector, 18) == 0
                for vector in summary["degree3_split_basis_masks"][0]
            )
        )
        self.assertTrue(
            all(
                parity_dot(vector, 24) == 0
                for vector in summary["degree4_split_basis_masks"][0]
            )
        )
        self.assertNotEqual(18, 24)


if __name__ == "__main__":
    unittest.main()
