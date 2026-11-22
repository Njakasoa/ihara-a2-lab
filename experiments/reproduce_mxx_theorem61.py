"""Reproduce Ma--Xing--Xing, arXiv:2610.33649v2, Theorem 6.1, in Sage."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from sage.all import QQ, binomial
from sage.env import SAGE_VERSION

from mxx_genus334_sage import require, verify_geometry

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.m3_local_units import exponent_two_character_average_conductor, local_unit_p_rank

CERTIFICATE = ROOT / "certificates" / "mxx-theorem61.json"
# (place degree, exponent in the printed modulus, number of distinct places)
SUPPORT = [(6, 2, 1), (6, 3, 1), (8, 2, 16), (10, 2, 12), (12, 2, 1)]


def compute_certificate():
    geometry = verify_geometry()
    genus = geometry["genus_k"]
    inventory = geometry["place_counts_1_to_12"]
    t = inventory[0]  # all rational places split
    required = Counter()
    rank_sum = 0
    commutators = 0
    mean_degree = QQ.zero()
    local_terms = []
    for degree, exponent, count in SUPPORT:
        required[degree] += count
        # Theorem 1.1 and Corollary 5.5, specialized to q = p = 2.
        rank = degree * (exponent - 1 - (exponent - 1) // 2)
        tail = 2 + sum(2**(degree * (j - 1 - (j - 1)//2)) for j in range(2, exponent))
        mean = exponent - QQ(tail) / 2**rank
        require(rank == local_unit_p_rank(degree, exponent), "local rank differs from M3")
        m3_mean = exponent_two_character_average_conductor(degree, exponent)
        require(mean * m3_mean.denominator == m3_mean.numerator,
                f"character filtration differs at degree {degree}, exponent {exponent}")
        rank_sum += count * rank
        commutators += count * binomial(rank, 2)
        mean_degree += count * degree * mean
        local_terms.append({"degree": degree, "exponent": exponent, "count": count,
                            "rank": rank, "mean_exponent_upper_bound": str(mean)})

    require(all(required[f] <= inventory[f-1] for f in required), "support unavailable on k334")
    d = 1 + rank_sum - t
    # At p=2 the power relations contribute rank_sum to the quadratic coefficient.
    quadratic = d + t - 1 + commutators + rank_sum
    tau = QQ(1) / 40
    witness_value = 1 - d*tau + quadratic*tau**2
    require(d >= 1 and 0 < tau < 1 and witness_value < 0, "tower criterion failed")
    denominator = genus - 1 + mean_degree / 2
    bound = t / denominator

    baseline = json.loads((ROOT / "certificates/m2-frozen.json").read_text())
    previous_inventory = json.loads((ROOT / "curves/k343-place-counts-30.json").read_text())
    require(t == baseline["rational_places"] and
            all(required[f] <= previous_inventory["place_counts"][f-1] for f in required),
            "same-support comparison is infeasible on k343")
    m3 = QQ(baseline["bound"])
    same_support = t / (baseline["genus"] - 1 + mean_degree / 2)
    require(same_support < m3 < bound and bound == QQ(65536) / 206231,
            "unexpected ordering or value of the three scores")

    return {
        "source": "https://arxiv.org/html/2610.33649v2#S6.SS1",
        "geometry": geometry, "support": local_terms, "splitting_places": t,
        "rank_sum": rank_sum, "generator_lower_bound": d,
        "quadratic_coefficient": int(quadratic), "tau": str(tau), "P(tau)": str(witness_value),
        "mean_conductor_degree_upper_bound": str(mean_degree),
        "genus_denominator_upper_bound": str(denominator), "bound": str(bound),
        "same_support_on_k343": str(same_support), "M3_optimum_on_k343": str(m3),
        "gain_over_M3": str(bound - m3),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true", help="regenerate the archived JSON")
    args = parser.parse_args()
    certificate = compute_certificate()
    serialized = json.dumps(certificate, indent=2) + "\n"
    if args.write_certificate:
        CERTIFICATE.write_text(serialized, encoding="utf-8", newline="\n")
    else:
        require(json.loads(CERTIFICATE.read_text()) == json.loads(serialized),
                "archived certificate differs from the computation")
    print(f"SageMath {SAGE_VERSION} | genus {certificate['geometry']['genus_k']} | "
          f"P(1/40) = {certificate['P(tau)']} | A(2) >= {certificate['bound']}")
    print(f"Same support on k343: {certificate['same_support_on_k343']} | "
          f"M3 optimum: {certificate['M3_optimum_on_k343']}")


if __name__ == "__main__":
    main()
