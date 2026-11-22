import IharaM3.Support
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-! The terminal case admits a short independent exhaustion. If the rank mass
is 266 and the moment is at most 2280, at most 44 units of penalty are
available. This leaves just seven possible (degree, half-depth) pairs. -/

namespace IharaM3

private def allowance (f : ℕ) :=
  (if f = 5 then 25 else 0) + (if f = 6 then 24 else 0) + (if f = 8 then 16 else 0)

private def penalty (p : Place) : ℕ :=
  let a := p.1 * p.2
  a * (a+1) + allowance p.1 - 11*a

private def penalties : Support → ℕ
  | [] => 0
  | p :: xs => penalty p + penalties xs

private theorem allowance_suffices {p : Place} (h : Allowed p) (hn : p.1 ≠ 1) :
    11*(p.1*p.2) ≤ (p.1*p.2)*(p.1*p.2+1) + allowance p.1 := by
  rcases p with ⟨f,s⟩
  rcases h with ⟨hs,hf⟩
  change f ≠ 1 at hn
  change 1 ≤ s at hs
  change f = 1 ∨ f = 5 ∨ f = 6 ∨ f = 8 ∨ f = 10 ∨ 12 ≤ f at hf
  change 11*(f*s) ≤ (f*s)*(f*s+1) + allowance f
  by_cases ha : 10 ≤ f*s
  · have hprod := Nat.mul_le_mul_left (f*s) ha
    rw [Nat.mul_add, Nat.mul_one]
    omega
  · have hfs : f ≤ f*s := by simpa using Nat.mul_le_mul_left f hs
    rcases hf with rfl | rfl | rfl | rfl | rfl | hf
    · contradiction
    · have : s = 1 := by omega
      subst s; decide
    · have : s = 1 := by omega
      subst s; decide
    · have : s = 1 := by omega
      subst s; decide
    · omega
    · omega

private theorem penalty_balance {xs : Support}
    (ht : ∀ p ∈ xs, Allowed p) (hn : stock 1 xs = 0) :
    11*mass xs + penalties xs =
      moment xs + 25*stock 5 xs + 24*stock 6 xs + 16*stock 8 xs := by
  induction xs with
  | nil => rfl
  | cons p xs ih =>
    have hn' : stock 1 xs = 0 := by simp only [stock] at hn; omega
    have hnr : p.1 ≠ 1 := by
      intro he; simp [stock, he] at hn
    have hi := ih (fun q hq => ht q (List.mem_cons_of_mem _ hq)) hn'
    have hp := allowance_suffices (ht p (by simp)) hnr
    simp only [mass, moment, penalties, stock, penalty]
    by_cases h5 : p.1 = 5 <;> by_cases h6 : p.1 = 6 <;> by_cases h8 : p.1 = 8 <;>
      simp [allowance, h5, h6, h8] at hp ⊢ <;> omega

private theorem member_penalty {xs : Support} {p : Place} (hp : p ∈ xs) :
    penalty p ≤ penalties xs := by
  induction xs with
  | nil => simp at hp
  | cons q xs ih =>
    rcases List.mem_cons.mp hp with rfl | h
    · simp [penalties]
    · have := ih h
      simp only [penalties]; omega

private theorem member_nonrational {xs : Support} {p : Place}
    (hp : p ∈ xs) (hn : stock 1 xs = 0) : p.1 ≠ 1 := by
  induction xs with
  | nil => simp at hp
  | cons q xs ih =>
    simp only [stock] at hn
    rcases List.mem_cons.mp hp with rfl | h
    · intro he; simp [he] at hn
    · exact ih h (by omega)

private def TerminalType (p : Place) : Prop :=
  p = (5,1) ∨ p = (5,2) ∨ p = (6,1) ∨ p = (8,1) ∨
  p = (10,1) ∨ p = (12,1) ∨ p = (13,1)

private theorem terminal_type {p : Place} (ht : Allowed p) (hn : p.1 ≠ 1)
    (hp : penalty p ≤ 44) : TerminalType p := by
  rcases p with ⟨f,s⟩
  rcases ht with ⟨hs,hf⟩
  change f ≠ 1 at hn
  change 1 ≤ s at hs
  change f = 1 ∨ f = 5 ∨ f = 6 ∨ f = 8 ∨ f = 10 ∨ 12 ≤ f at hf
  have ha : f*s ≤ 13 := by
    by_contra! h
    obtain ⟨k,hk⟩ := Nat.exists_eq_add_of_le (show 14 ≤ f*s by omega)
    change (f*s)*(f*s+1) + allowance f - 11*(f*s) ≤ 44 at hp
    rw [hk] at hp
    have : 56 + 11*(14+k) ≤ (14+k)*(14+k+1) := by
      rw [Nat.mul_add (14+k) (14+k) 1, Nat.mul_one]
      have := Nat.mul_le_mul_left (14+k) (show 14 ≤ 14+k by omega)
      omega
    omega
  have hfs : f ≤ f*s := by simpa using Nat.mul_le_mul_left f hs
  rcases hf with rfl | rfl | rfl | rfl | rfl | hf
  · contradiction
  · have h : s=1 ∨ s=2 := by omega
    rcases h with rfl | rfl <;> simp [TerminalType]
  · have h : s=1 ∨ s=2 := by omega
    rcases h with rfl | rfl
    · simp [TerminalType]
    · exact False.elim ((by decide : ¬ penalty (6,2) ≤ 44) hp)
  · have : s=1 := by omega
    subst s; simp [TerminalType]
  · have : s=1 := by omega
    subst s; simp [TerminalType]
  · have h : f=12 ∨ f=13 := by omega
    rcases h with rfl | rfl <;> have : s=1 := by omega
    all_goals subst s; simp [TerminalType]

private def occurrences (q : Place) : Support → ℕ
  | [] => 0
  | p :: xs => (if p = q then 1 else 0) + occurrences q xs

private theorem census {xs : Support} (ht : ∀ p ∈ xs, TerminalType p) :
    let a := occurrences (5,1) xs
    let b := occurrences (5,2) xs
    let c := occurrences (6,1) xs
    let d := occurrences (8,1) xs
    let e := occurrences (10,1) xs
    let f := occurrences (12,1) xs
    let g := occurrences (13,1) xs
    stock 5 xs = a+b ∧ stock 6 xs = c ∧ stock 8 xs = d ∧
    mass xs = 5*a+10*b+6*c+8*d+10*e+12*f+13*g ∧
    moment xs = 30*a+110*b+42*c+72*d+110*e+156*f+182*g ∧
    8192*rebate xs = ((1280*a+1320*b+768*c+256*d+80*e+24*f+13*g : ℕ) : ℚ) := by
  induction xs with
  | nil => norm_num [stock,mass,moment,rebate,occurrences]
  | cons p xs ih =>
    obtain ⟨h5,h6,h8,hA,hC,hR⟩ := ih (fun q hq => ht q (List.mem_cons_of_mem _ hq))
    rcases ht p (by simp) with h | h | h | h | h | h | h <;> subst p
    all_goals
      dsimp only
      norm_num [stock,mass,moment,rebate,occurrences,localRebate,h5,h6,h8,hA,hC,
        Nat.mul_add, mul_add]
      push_cast at *
      repeat' apply And.intro
      all_goals first | omega | linarith

set_option maxHeartbeats 2000000 in
private theorem seven_types_bound (a b c d e f g : ℕ)
    (h5 : a+b ≤ 2) (h6 : c ≤ 16) (h8 : d ≤ 16)
    (hA : 5*a+10*b+6*c+8*d+10*e+12*f+13*g = 266)
    (hC : 30*a+110*b+42*c+72*d+110*e+156*f+182*g ≤ 2280) :
    1280*a+1320*b+768*c+256*d+80*e+24*f+13*g ≤ 19128 := by
  have hpen : 25*(2-(a+b)) + 24*(16-c) + 16*(16-d) + 25*b + 24*f + 39*g ≤ 44 := by omega
  have hb : b=0 ∨ b=1 := by omega
  have hf : f=0 ∨ f=1 := by omega
  have hg : g=0 ∨ g=1 := by omega
  have hc : c=15 ∨ c=16 := by omega
  have hd : d=14 ∨ d=15 ∨ d=16 := by omega
  rcases hb with rfl | rfl <;> rcases hf with rfl | rfl <;> rcases hg with rfl | rfl <;>
    rcases hc with rfl | rfl <;> rcases hd with rfl | rfl | rfl <;> omega

/-- Exact terminal rebate bound, proved for arbitrary finite supports. -/
theorem terminal_rebate_bound {xs : Support} (hi : Inventory xs)
    (hn : stock 1 xs = 0) (hA : mass xs = 266) (hC : moment xs ≤ 2280) :
    rebate xs ≤ 2391/1024 := by
  have hB := penalty_balance hi.types hn
  have h5 := hi.five
  have h6 := hi.six
  have h8 := hi.eight
  have h44 : penalties xs ≤ 44 := by omega
  have ht (p : Place) (hp : p ∈ xs) : TerminalType p :=
    terminal_type (hi.types p hp) (member_nonrational hp hn) (le_trans (member_penalty hp) h44)
  obtain ⟨hs5,hs6,hs8,hm,hmo,hr⟩ := census ht
  have h := seven_types_bound _ _ _ _ _ _ _ (hs5 ▸ h5) (hs6 ▸ h6) (hs8 ▸ h8)
    (hm.symm.trans hA) (hmo ▸ hC)
  have hq : 8192 * rebate xs ≤ 19128 := by rw [hr]; exact_mod_cast h
  linarith

end IharaM3
