import IharaM3.Theorem61
import IharaM3.Reduction
import IharaM3.Terminal
import Mathlib.Order.Bounds.Basic

namespace IharaM3

/-- Every support in the relaxed inventory used in the obstruction has score
at most the incumbent, irrespective of its largest degree or depth. -/
theorem m3_upper {xs : Support} {t : ℕ} (h : Eligible xs t) : score xs t ≤ baseBound := by
  by_contra! improve
  obtain ⟨hn, hA, ht, _, hC⟩ := improvement_caps xs t h improve
  have hr := terminal_rebate_bound h.inv hn hA hC
  have hc : (269993/1024 : ℚ) ≤ cost xs := by
    unfold cost
    rw [hA]
    norm_num at *
    linarith
  rw [score, ht] at improve
  have hd : 0 < 342 + cost xs := by linarith
  have hi := (lt_div_iff₀ hd).mp improve
  norm_num [baseBound] at hi
  linarith

/-- Only these facts about the stock B of closed places enter the proof.
Degrees above 12 can have any stock. Sage supplies the geometric counts. -/
structure K343Stock (B : ℕ → ℕ) : Prop where
  rational : B 1 = 192
  degrees : ∀ f, 0 < B f → f = 1 ∨ f = 5 ∨ f = 6 ∨ f = 8 ∨ f = 10 ∨ 12 ≤ f
  five : B 5 = 2
  six : B 6 = 16
  eight : B 8 = 16
  ten : 2 ≤ B 10
  twelve : 1 ≤ B 12

/-- Search on raw conductor exponents. Copies of a degree use distinct
places, and the ramified and split rational places share one stock. -/
structure Admissible (B : ℕ → ℕ) (raw : List (ℕ × ℕ)) (t : ℕ) : Prop where
  cutoffs : ∀ p ∈ raw, 2 ≤ p.2
  available : ∀ f, stock f (normalize raw) ≤ B f
  positive : 0 < t
  disjoint : t + stock 1 (normalize raw) ≤ B 1
  rank : t ≤ mass (normalize raw)
  tower : 2 * moment (normalize raw) + 4 * mass (normalize raw) ≤
    (1 + mass (normalize raw) - t)^2

private theorem stock_pos (p : Place) (xs : Support) (hm : p ∈ xs) : 0 < stock p.1 xs := by
  induction xs with
  | nil => simp at hm
  | cons q qs ih =>
    rcases List.mem_cons.mp hm with rfl | hm
    · simp [stock]
    · have hp := ih hm
      simp only [stock]
      omega

theorem Admissible.eligible {B raw t} (hb : K343Stock B) (h : Admissible B raw t) :
    Eligible (normalize raw) t := by
  constructor
  · constructor
    · intro p hp
      obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hp
      have hv := h.cutoffs q hq
      have positive := stock_pos (q.1, q.2 / 2) (normalize raw) hp
      exact ⟨by dsimp; omega, hb.degrees q.1 (lt_of_lt_of_le positive (h.available q.1))⟩
    · simpa [hb.five] using h.available 5
    · simpa [hb.six] using h.available 6
    · simpa [hb.eight] using h.available 8
  · exact h.positive
  · simpa [hb.rational] using h.disjoint
  · exact h.rank
  · exact h.tower

/-- M2 support, with actual conductor exponents (all equal to 2). -/
def witness : List (ℕ × ℕ) :=
  List.replicate 2 (5, 2) ++ List.replicate 16 (6, 2) ++
  List.replicate 16 (8, 2) ++ List.replicate 2 (10, 2) ++ [(12, 2)]

private theorem stock_absent (f : ℕ) (xs : Support) (h : ∀ p ∈ xs, p.1 ≠ f) :
    stock f xs = 0 := by
  induction xs with
  | nil => rfl
  | cons p ps ih =>
    have hp := h p List.mem_cons_self
    have hs := ih (fun q hq => h q (List.mem_cons_of_mem _ hq))
    simp [stock, hp, hs]

theorem witness_admissible {B} (hb : K343Stock B) : Admissible B witness 192 := by
  constructor
  · decide
  · intro f
    by_cases h5 : f = 5
    · subst f; rw [hb.five]; decide
    by_cases h6 : f = 6
    · subst f; rw [hb.six]; decide
    by_cases h8 : f = 8
    · subst f; rw [hb.eight]; decide
    by_cases h10 : f = 10
    · subst f; exact le_trans (by decide : stock 10 (normalize witness) ≤ 2) hb.ten
    by_cases h12 : f = 12
    · subst f; exact le_trans (by decide : stock 12 (normalize witness) ≤ 1) hb.twelve
    have kinds : ∀ p ∈ normalize witness,
        p.1 = 5 ∨ p.1 = 6 ∨ p.1 = 8 ∨ p.1 = 10 ∨ p.1 = 12 := by decide
    rw [stock_absent f _ (fun p hp => by have := kinds p hp; omega)]
    exact Nat.zero_le _
  · decide
  · rw [hb.rational]; decide
  · decide
  · decide

theorem witness_score : score (normalize witness) 192 = baseBound := by decide +kernel

/-- Exact maximum, including attainment, for the genus-343 elementary-ray
score over all finite supports and raw conductor exponents at least two. -/
theorem m3_maximum (B : ℕ → ℕ) (hb : K343Stock B) :
    IsGreatest { r : ℚ | ∃ raw t, Admissible B raw t ∧ score (normalize raw) t = r }
      baseBound := by
  refine ⟨⟨witness, 192, witness_admissible hb, witness_score⟩, ?_⟩
  intro r hr
  obtain ⟨raw, t, h, rfl⟩ := hr
  exact m3_upper (h.eligible hb)

/-- Closed-place counts through degree 12 from the Sage inventory. The
tail is an arbitrary function, so this model places no cap on higher degrees. -/
def genus343Inventory (tail : ℕ → ℕ) (f : ℕ) : ℕ :=
  if f = 1 then 192 else if f = 5 then 2 else if f = 6 then 16 else
  if f = 8 then 16 else if f = 10 then 64 else if f = 12 then 208 else
  if 13 ≤ f then tail f else 0

theorem genus343_stock (tail : ℕ → ℕ) : K343Stock (genus343Inventory tail) := by
  constructor
  · rfl
  · intro f h
    unfold genus343Inventory at h
    split_ifs at h <;> omega
  · rfl
  · rfl
  · rfl
  · change 2 ≤ 64
    decide
  · change 1 ≤ 208
    decide

/-- M3 for the certified degree-1 through degree-12 counts, uniformly in
all remaining stocks. The maximum is the displayed rational number. -/
theorem genus343_maximum (tail : ℕ → ℕ) :
    IsGreatest { r : ℚ | ∃ raw t, Admissible (genus343Inventory tail) raw t ∧
      score (normalize raw) t = r } (196608/620201 : ℚ) :=
  m3_maximum _ (genus343_stock tail)

end IharaM3
