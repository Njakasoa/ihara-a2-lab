import IharaM3.Support
import IharaM3.Pairs
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-! Uniform bounds before imposing any cutoff on degree or depth. The hypotheses
about the field are exactly the degree inventory in `Inventory`. -/

namespace IharaM3

private def hit (f d : ℕ) : ℕ := if f = d then 1 else 0

private def allowance (A n u v w : ℕ) : ℚ :=
  (A : ℚ) / 1023 + (n : ℚ) * (1022/1023) +
    (u : ℚ) * (5/31 - 5/1023) + (v : ℚ) * (6/63 - 6/1023) +
    (w : ℚ) * (8/255 - 8/1023)

private theorem allowance_add (a b c d e f g h i j : ℕ) :
    allowance (a+f) (b+g) (c+h) (d+i) (e+j) =
      allowance a b c d e + allowance f g h i j := by
  unfold allowance
  push_cast
  ring

private theorem degree_le_mass (f s : ℕ) (hs : 1 ≤ s) : f ≤ f*s := by
  simpa using Nat.mul_le_mul_left f hs

private theorem simple_ceiling (f s : ℕ) (hf : 1 ≤ f) :
    localRebate (f,s) ≤ (f : ℚ) / ((2:ℚ)^f-1) := by
  have hp : (2:ℚ)^1 ≤ 2^f := pow_le_pow_right₀ (by norm_num) hf
  have hden : 0 < (2:ℚ)^f-1 := by norm_num at hp; linarith
  unfold localRebate
  dsimp only
  apply (div_le_div_iff_of_pos_right hden).2
  have hcast : (0:ℚ) ≤ f := by positivity
  have hinv : (0:ℚ) ≤ 1 / (2:ℚ)^(f*s) := by positivity
  nlinarith only [mul_nonneg hcast hinv]

private theorem local_cost_nonneg (p : Place) (ht : Allowed p) :
    localRebate p ≤ ((p.1*p.2 : ℕ) : ℚ) := by
  obtain ⟨f,s⟩ := p
  rcases ht with ⟨hs, ht⟩
  change 1 ≤ s at hs
  have hf : 1 ≤ f := by dsimp only at ht; omega
  have hp : (2:ℚ)^1 ≤ 2^f := pow_le_pow_right₀ (by norm_num) hf
  norm_num at hp
  have hden : 0 < (2:ℚ)^f-1 := by linarith
  have hfq : (0:ℚ) ≤ f := by positivity
  calc
    localRebate (f,s) ≤ (f:ℚ) / ((2:ℚ)^f-1) := simple_ceiling f s hf
    _ ≤ (f:ℚ) := (div_le_iff₀ hden).2 (by nlinarith only [mul_nonneg hfq (sub_nonneg.mpr hp)])
    _ ≤ ((f*s:ℕ):ℚ) := by exact_mod_cast degree_le_mass f s hs

private theorem local_allowance (p : Place) (ht : Allowed p) :
    localRebate p ≤ allowance (p.1*p.2) (hit p.1 1)
      (hit p.1 5) (hit p.1 6) (hit p.1 8) := by
  obtain ⟨f,s⟩ := p
  rcases ht with ⟨hs, ht⟩
  dsimp only at hs ht ⊢
  have hf : 1 ≤ f := by omega
  have hm : (f:ℚ) ≤ ((f*s:ℕ):ℚ) := by exact_mod_cast degree_le_mass f s hs
  have hsQ : (1:ℚ) ≤ (s:ℚ) := by exact_mod_cast hs
  apply le_trans (simple_ceiling f s hf)
  rcases ht with h|h|h|h|h|h
  · subst f; norm_num [allowance, hit]; linarith only [hsQ]
  · subst f; norm_num [allowance, hit]; linarith only [hsQ]
  · subst f; norm_num [allowance, hit]; linarith only [hsQ]
  · subst f; norm_num [allowance, hit]; linarith only [hsQ]
  all_goals
    have h10 : 10 ≤ f := by omega
    have hp : (2:ℚ)^10 ≤ 2^f := pow_le_pow_right₀ (by norm_num) h10
    norm_num at hp
    have hden : 0 < (2:ℚ)^f-1 := by linarith
    have hinv : (f:ℚ)/((2:ℚ)^f-1) ≤ (f:ℚ)/1023 := by
      apply (div_le_div_iff₀ hden (by norm_num : (0:ℚ) < 1023)).2
      nlinarith only [mul_nonneg (show (0:ℚ) ≤ f by positivity) (sub_nonneg.mpr hp)]
    have h1 : f ≠ 1 := by omega
    have h5 : f ≠ 5 := by omega
    have h6 : f ≠ 6 := by omega
    have h8 : f ≠ 8 := by omega
    simp only [allowance, hit, ite_eq_right h1, ite_eq_right h5, ite_eq_right h6, ite_eq_right h8,
      Nat.cast_zero, zero_mul, add_zero]
    linarith only [hinv, hm]

private theorem rebate_bounds (xs : Support) (ht : ∀ p ∈ xs, Allowed p) :
    rebate xs ≤ (mass xs : ℚ) ∧
    rebate xs ≤ allowance (mass xs) (stock 1 xs) (stock 5 xs) (stock 6 xs) (stock 8 xs) := by
  induction xs with
  | nil => norm_num [mass, rebate, stock, allowance]
  | cons p xs ih =>
    obtain ⟨hcost, hallow⟩ := ih (fun q hq => ht q (List.mem_cons_of_mem _ hq))
    have hp := ht p List.mem_cons_self
    constructor
    · simpa only [rebate, mass, Nat.cast_add] using add_le_add (local_cost_nonneg p hp) hcost
    · simpa only [rebate, mass, stock, hit, allowance_add]
        using add_le_add (local_allowance p hp) hallow

private theorem local_moment (p : Place) (ht : Allowed p) :
    11*(p.1*p.2) ≤ (p.1*p.2)*(p.1*p.2+1) +
      25*hit p.1 1 + 25*hit p.1 5 + 24*hit p.1 6 + 16*hit p.1 8 := by
  obtain ⟨f,s⟩ := p
  rcases ht with ⟨hs, ht⟩
  dsimp only at hs ht ⊢
  have hm := degree_le_mass f s hs
  generalize ha : f*s = a at hm ⊢
  have universal : 11*a ≤ a*(a+1)+25 := by
    zify
    nlinarith only [sq_nonneg ((a:ℤ)-5)]
  rcases ht with h|h|h|h|h|h
  · subst f; simpa [hit] using universal
  · subst f; simpa [hit] using universal
  · subst f; obtain ⟨k,rfl⟩ := Nat.exists_eq_add_of_le hm
    norm_num [hit]; nlinarith
  · subst f; obtain ⟨k,rfl⟩ := Nat.exists_eq_add_of_le hm
    norm_num [hit]; nlinarith
  all_goals
    have h10 : 10 ≤ f := by omega
    have h1 : f ≠ 1 := by omega
    have h5 : f ≠ 5 := by omega
    have h6 : f ≠ 6 := by omega
    have h8 : f ≠ 8 := by omega
    simp only [hit, ite_eq_right h1, ite_eq_right h5, ite_eq_right h6, ite_eq_right h8, mul_zero, add_zero]
    have ha10 := h10.trans hm
    nlinarith only [Nat.mul_le_mul_left a ha10]

private theorem support_moment (xs : Support) (ht : ∀ p ∈ xs, Allowed p) :
    11*mass xs ≤ moment xs + 25*stock 1 xs + 25*stock 5 xs +
      24*stock 6 xs + 16*stock 8 xs := by
  induction xs with
  | nil => simp [mass, moment, stock]
  | cons p xs ih =>
    have tail := ih (fun q hq => ht q (List.mem_cons_of_mem _ hq))
    have head := local_moment p (ht p List.mem_cons_self)
    simp only [hit, Nat.mul_add] at head
    simp only [mass, moment, stock, Nat.mul_add]
    omega

private theorem rational_stock_le_mass (xs : Support) (ht : ∀ p ∈ xs, Allowed p) :
    stock 1 xs ≤ mass xs := by
  induction xs with
  | nil => rfl
  | cons p xs ih =>
    have tail := ih (fun q hq => ht q (List.mem_cons_of_mem _ hq))
    have hp := (ht p List.mem_cons_self).1
    simp only [stock, mass]
    split
    next h => rw [h, one_mul]; omega
    next => omega

/-- A putative improvement has only one possible rational stock, rank mass and
splitting size. The bound on its quadratic moment will exclude deeper places. -/
theorem improvement_caps (xs : Support) (t : ℕ) (h : Eligible xs t)
    (improve : baseBound < score xs t) :
    stock 1 xs = 0 ∧ mass xs = 266 ∧ t = 192 ∧ 2236 ≤ moment xs ∧ moment xs ≤ 2280 := by
  obtain ⟨hcost, hallow⟩ := rebate_bounds xs h.inv.types
  have hden : 0 < 342 + cost xs := by unfold cost; linarith
  have hratio := (lt_div_iff₀ hden).mp improve
  unfold baseBound cost at hratio
  have hm := support_moment xs h.inv.types
  have hu := h.inv.five
  have hv := h.inv.six
  have hw := h.inv.eight
  apply necessary_pairs (stock 1 xs) (mass xs) t (moment xs)
    (rational_stock_le_mass xs h.inv.types) h.split h.rank (by omega) h.gs
  · exact_mod_cast (show (196608:ℚ)*342 < 620201*(t:ℚ) by linarith only [hratio,hcost])
  · have hu' : (stock 5 xs : ℚ) ≤ 2 := by exact_mod_cast hu
    have hv' : (stock 6 xs : ℚ) ≤ 16 := by exact_mod_cast hv
    have hw' : (stock 8 xs : ℚ) ≤ 16 := by exact_mod_cast hw
    unfold allowance at hallow
    exact_mod_cast (show (196608:ℚ)*(342*608685+608090*(mass xs:ℚ)) <
      620201*608685*(t:ℚ) + 196608*(608090*(stock 1 xs:ℚ)+1290176) by
      linarith only [hratio, hallow, hu', hv', hw'])

end IharaM3
