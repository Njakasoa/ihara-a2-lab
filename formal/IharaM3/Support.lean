import Mathlib.Data.Rat.Cast.Order

/-! A support is a list of degree / half-depth pairs. Each actual closed place
contributes one entry. Distinct places of the same degree may therefore give
identical entries. The elementary score for a conductor exponent ν ≥ 2
depends on its half-depth ν / 2. -/

namespace IharaM3

abbrev Place := ℕ × ℕ
abbrev Support := List Place

def mass : Support → ℕ
  | [] => 0
  | p :: xs => p.1 * p.2 + mass xs

def moment : Support → ℕ
  | [] => 0
  | p :: xs => (p.1 * p.2) * (p.1 * p.2 + 1) + moment xs

def stock (d : ℕ) : Support → ℕ
  | [] => 0
  | p :: xs => (if p.1 = d then 1 else 0) + stock d xs

def localRebate (p : Place) : ℚ :=
  (p.1 : ℚ) * (1 - 1 / (2 : ℚ) ^ (p.1 * p.2)) / ((2 : ℚ) ^ p.1 - 1)

def rebate : Support → ℚ
  | [] => 0
  | p :: xs => localRebate p + rebate xs

def cost (xs : Support) : ℚ := (mass xs : ℚ) - rebate xs
def score (xs : Support) (t : ℕ) : ℚ := (t : ℚ) / (342 + cost xs)
def baseBound : ℚ := 196608 / 620201

def Allowed (p : Place) : Prop :=
  1 ≤ p.2 ∧ (p.1 = 1 ∨ p.1 = 5 ∨ p.1 = 6 ∨ p.1 = 8 ∨ p.1 = 10 ∨ 12 ≤ p.1)

structure Inventory (xs : Support) : Prop where
  types : ∀ p ∈ xs, Allowed p
  five : stock 5 xs ≤ 2
  six : stock 6 xs ≤ 16
  eight : stock 8 xs ≤ 16

structure Eligible (xs : Support) (t : ℕ) : Prop where
  inv : Inventory xs
  positive : 0 < t
  split : t + stock 1 xs ≤ 192
  rank : t ≤ mass xs
  gs : 2 * moment xs + 4 * mass xs ≤ (1 + mass xs - t)^2

end IharaM3
