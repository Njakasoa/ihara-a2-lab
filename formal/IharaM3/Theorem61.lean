import IharaM3.Support
import Mathlib.Tactic.NormNum

/-! Exact arithmetic of Ma–Xing–Xing, Theorem 6.1 (arXiv:2610.33649v2).
The five rows of the printed modulus are the inputs. The genus computation
uses the conductor counts independently reproduced by the Sage checker. -/

namespace IharaM3

/-- From a list of (degree, conductor exponent) to elementary half-depths. -/
def normalize (raw : List (ℕ × ℕ)) : Support :=
  raw.map fun p => (p.1, p.2 / 2)

theorem consecutive_cutoffs (s : ℕ) : (2*s)/2 = s ∧ (2*s+1)/2 = s := by omega

def mxxModulus : List (ℕ × ℕ) :=
  [(6, 2), (6, 3)] ++ List.replicate 16 (8, 2) ++
    List.replicate 12 (10, 2) ++ [(12, 2)]

def mxxSupport := normalize mxxModulus

theorem mxx_genus (g : ℕ)
    (h : 2*g-2 = 32 * (2 * 2 - 2) + (28 * 20 + 3 * 14)) : g = 334 := by omega

/-- The selected places fit the stocks of degrees 6, 8, 10 and 12 in k334.
The split rational places are disjoint from all selected ramified places. -/
theorem mxx_support_fits :
    stock 1 mxxSupport = 0 ∧ stock 6 mxxSupport = 2 ∧ stock 8 mxxSupport = 16 ∧
    stock 10 mxxSupport ≤ 96 ∧ stock 12 mxxSupport ≤ 240 := by decide

/-- Quadratic coefficient at p=2: d+t−1 plus the sum of n(n+1)/2. -/
def towerPolynomial (xs : Support) (t : ℕ) (τ : ℚ) : ℚ :=
  let d := 1 + mass xs - t
  1 - (d : ℚ) * τ + (((d + t - 1 : ℕ) : ℚ) + (moment xs : ℚ) / 2) * τ^2

theorem mxx_ranks : mass mxxSupport = 272 ∧ moment mxxSupport = 2712 := by decide

theorem mxx_polynomial (τ : ℚ) :
    towerPolynomial mxxSupport 192 τ = 1 - 81 * τ + 1628 * τ^2 := by
  norm_num [towerPolynomial, mxx_ranks.1, mxx_ranks.2]

theorem mxx_tower_witness : 0 < (1/40 : ℚ) ∧ (1/40 : ℚ) < 1 ∧
    towerPolynomial mxxSupport 192 (1/40) = -3/400 ∧
    towerPolynomial mxxSupport 192 (1/40) < 0 := by
  rw [mxx_polynomial]
  norm_num

theorem mxx_cost : cost mxxSupport = 277701/1024 := by decide +kernel

theorem theorem61_arithmetic :
    (333 + cost mxxSupport = 618693/1024) ∧
    (192 / (333 + cost mxxSupport) = 65536/206231) ∧
    score mxxSupport 192 = 65536/209303 ∧
    score mxxSupport 192 < baseBound ∧ baseBound < 65536/206231 ∧
    65536/206231 - baseBound = 98828288/127904672431 := by
  norm_num [score, mxx_cost, baseBound]

end IharaM3
