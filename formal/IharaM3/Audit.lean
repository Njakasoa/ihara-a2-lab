import IharaM3.Maximum
import Lean.Util.CollectAxioms

/-! Fail the default build if a principal result depends on an assumption
outside Lean's standard extensionality, quotients and classical choice. -/
open Lean in
run_cmd do
  let allowed := [``propext, ``Quot.sound, ``Classical.choice]
  for name in [``IharaM3.theorem61_arithmetic, ``IharaM3.mxx_tower_witness,
               ``IharaM3.m3_pair_count, ``IharaM3.necessary_pairs,
               ``IharaM3.terminal_rebate_bound, ``IharaM3.genus343_maximum] do
    let axioms ← collectAxioms name
    for axiomName in axioms do
      unless allowed.contains axiomName do
        throwError "{name} depends on unexpected axiom {axiomName}"

#print axioms IharaM3.theorem61_arithmetic
#print axioms IharaM3.m3_pair_count
#print axioms IharaM3.genus343_maximum
