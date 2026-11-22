import Std

/-!
# Finite reduction of the M3 obstruction

Here `n` is the number of ramified rational places, `A` the total local
rank, `t` the number of split rational places, and `C` the sum of
`a * (a + 1)` over local ranks. The rebate estimate for the genus-343
inventory gives the two strict score inequalities in `necessary_pairs`.
All floors and ceilings below use natural-number division.
-/

namespace IharaM3

private def scoreScale : Nat := 620201 * 608685
private def massScale : Nat := 196608 * 608090
private def intercept : Nat := 196608 * (342 * 608685)
private def allowance (n : Nat) : Nat := 196608 * (608090 * n + 1290176)

/-- Exclusive upper endpoint for the mass in row `n`. It is zero for
    an empty row whose real-valued upper endpoint is nonpositive. -/
private def massLimit (n : Nat) : Nat :=
  (scoreScale * (192 - n) + allowance n - intercept + (massScale - 1)) / massScale

/-- Smallest splitting size permitted by both strict score inequalities. -/
private def minSplits (n A : Nat) : Nat :=
  max (196608 * 342 / 620201 + 1)
    ((intercept + massScale * A - allowance n) / scoreScale + 1)

private def passes (n A : Nat) : Prop :=
  let t := minSplits n A
  let c := 11 * A - (690 + 25 * n)
  t ≤ A ∧ n + t ≤ 192 ∧ 2 * c + 4 * A ≤ (1 + A - t)^2

private instance (n A : Nat) : Decidable (passes n A) := by
  unfold passes
  infer_instance

/-- Rows are indexed by `n`; offsets in a row encode masses starting at `n`. -/
private def rowLength (n : Nat) : Nat := massLimit n - n

/-- Size of the search after the strict mass bound, before the splitting
    and relation filters. -/
def testedPairCount : Nat := ((List.range 192).map rowLength).sum

set_option maxRecDepth 80000 in
theorem m3_pair_count : testedPairCount = 11384 := by decide +kernel

private def checkRow (n : Nat) : Bool :=
  (List.range (rowLength n)).all fun offset =>
    let A := n + offset
    decide (passes n A → n = 0 ∧ A = 266)

set_option maxRecDepth 80000 in
set_option maxHeartbeats 4000000 in
private theorem checkedRows : (List.range 192).all checkRow = true := by decide +kernel

/-- Any admissible putative strict improvement is represented in the
    checked rows. The last inequality clears the denominator of the rebate
    bound using `608685 = 1023 * 595` and `608090 = 1022 * 595`. -/
theorem necessary_pairs (n A t C : Nat)
    (hn : n ≤ A) (htn : t + n ≤ 192) (hta : t ≤ A)
    (hm : 11 * A ≤ C + 690 + 25 * n)
    (hgs : 2 * C + 4 * A ≤ (1 + A - t)^2)
    (hzero : 196608 * 342 < 620201 * t)
    (hlinear : 196608 * (342 * 608685 + 608090 * A) <
      620201 * 608685 * t + 196608 * (608090 * n + 1290176)) :
    n = 0 ∧ A = 266 ∧ t = 192 ∧ 2236 ≤ C ∧ C ≤ 2280 := by
  have hnRange : n < 192 := by omega
  have hcap : A < massLimit n := by
    unfold massLimit scoreScale massScale allowance intercept
    omega
  have htmin : minSplits n A ≤ t := by
    unfold minSplits scoreScale massScale allowance intercept
    omega
  have hbase : 1 + A - t ≤ 1 + A - minSplits n A := by omega
  have hsquare := Nat.pow_le_pow_left hbase 2
  have hpass : passes n A := by
    unfold passes
    exact ⟨by omega, by omega, by omega⟩
  have hrow := List.all_eq_true.mp checkedRows n (List.mem_range.mpr hnRange)
  have hoff : A - n < rowLength n := by
    unfold rowLength
    omega
  have hentry := List.all_eq_true.mp hrow (A - n) (List.mem_range.mpr hoff)
  have hsum : n + (A - n) = A := by omega
  change decide (passes n (n + (A - n)) → n = 0 ∧ n + (A - n) = 266) = true at hentry
  rw [hsum] at hentry
  obtain ⟨rfl, rfl⟩ := of_decide_eq_true hentry hpass
  have hvalue : minSplits 0 266 = 192 := by decide
  rw [hvalue] at htmin
  have ht : t = 192 := by omega
  subst t
  exact ⟨rfl, rfl, rfl, by omega, by omega⟩

end IharaM3
