# Astra review of the fixed-k conductor-two obstruction

**Conditional ACCEPT**, 13 September 2026: proofs/NU2_OBSTRUCTION.md and the recorded all-degree relaxation correctly reduce every possible strict improvement of the specified conservative score to a finite, dominating arithmetic problem. The DP compression and pruning are valid. Final computational acceptance requires the separate independent implementation to confirm the no-improvement conclusion; checking only the best witness is insufficient.

Scope reviewed: proofs/NU2_OBSTRUCTION.md, experiments/search_all_degree_relaxation.py, results/all-degree-relaxation.json, and the imported optimal_t definition. No accepted bound, claim or publication file was changed. Novelty of this obstruction was not assessed.

## Universal caps

Write R=sum f*B_f/2^f and cost=A-R. The exact certified low-degree stocks give R from degrees 5,6,8 at most 10/32+96/64+128/256=37/16. Every remaining available nonrational degree is at least ten, so its contribution is at most its degree mass divided by 1024, and hence at most A/1024. Using all of A here deliberately overcounts the low-degree mass; this weakens the estimate safely. This argument already applies to arbitrary finite supports and uses no prior degree cutoff.

For b=196608/620201, strict improvement implies cost<192/b-342=269993/1024. Therefore A<(269993/1024+37/16)*1024/1023=90787/341, and integer A<=266. The strict rounding formula (numerator-1)//denominator is correct even if the rational endpoint were an integer.

For each final A, put L=max(0,A-37/16-A/1024). Since t/(342+cost)>b, one necessarily has t>b(342+L), hence the stated floor-plus-one minimum. This is valid even if the lower cost estimate is attained exactly. Under the theorem's t<=A, D=1+A-t is positive. Combining t>=t_min with GS therefore gives C<=floor(((1+A-t_min)^2-4A)/2). A standalone Fraction loop over A=0,...,266 recomputed the maximum as 2280, attained at A=266,t_min=192. No branch with negative D is admissible or omitted incorrectly.

Every selected degree f contributes f(f+1)<=C. Since 47*48=2256<=2280 and 48*49=2352>2280, f<=47 follows. Thus the all-degree quantifier is justified before the finite relaxation is built. For degrees 12 through 47, granting floor(266/f) hypothetical places includes every support that could improve, regardless of actual higher-degree inventories. These are caps on selected multiplicities, not asserted upper bounds on actual place counts. The exact certified prefix B2,...,B11 remains essential, especially its zero entries.

## Dynamic program and strictness

At a fixed processed degree, two partial supports with identical (A,C) have identical legal remaining degree choices and identical possible final t values after any shared continuation. The larger rebate gives no larger denominator. Retaining only its maximum therefore preserves the existence of a strict improvement. Equal-rebate tie replacement affects witnesses, not the optimum. This dominance is valid because the inventories are independent upper multiplicity constraints, not constraints coupling choices at different degrees.

The partial-state caps use the global maxima A<=266,C<=2280. Both quantities are additive and nondecreasing as places are added. Consequently every prefix of an improving final support passes those caps. The code correctly avoids applying a final-A-dependent C cap or a t_min test prematurely to prefixes; those would need separate justification. Final t selection uses the exact integer square-root criterion already reviewed in M2. Final filtering with the necessary t_min cannot exclude an improving support.

Scaling rebates by 2^47 is exact for all surviving degrees. The DP's recorded zero strict improvements therefore yields a valid obstruction if independently reproduced. The equality witness at b is not itself an improvement and is retained correctly. The proof needs neither preservation of every equal-scoring witness nor a uniqueness claim. The separately accepted concrete configuration attains b, so no strict improvement plus attainment proves the maximum of this score, not merely an upper bound.

## Scope and actionable findings

- **Completion condition:** independently establish zero improving configurations under the proved caps. Re-evaluating the single DP winner through src/theorem_search.py checks its arithmetic but does not independently certify DP exhaustion. The separately assigned tester can close this condition using its different enumeration.
- **P3 input hardening:** the experiment exposes an alternate inventory path but retains hardcoded SPECIAL_REBATE=37/16 and degree cap 47. It should assert the exact reviewed low prefix (0,0,0,2,16,0,16,0,64,0), or derive and validate all constants from a changed prefix. A modified inventory with more low-degree places would otherwise invalidate the rebate bound. The recorded current input has the correct prefix, so this does not invalidate the present certificate.
- **P3 evidence wording:** call the theorem_search winner evaluation a cross-check rather than an independent implementation of the obstruction. The code imports optimal_t from that same module. Reserve independent-obstruction language for the separate tester's full result.

The resulting barrier applies to the fixed genus-343 k, all finite nonrational S, conductor two everywhere, variable rational splitting size 1<=t<=192, and this sufficient GS inequality with the conservative conductor-average score. It is stronger than the degree<=12 search statement, but it does not bound the actual ratio of an individual ray tower: an actual conductor average can be smaller, or a stronger infinitude criterion can succeed where this one fails. It says nothing about rational ramification support, other depths, other bases or the value of A(2). Preserve these limits whenever describing structural optimality.

No blocking mathematical defect found. **Final verdict: proof ACCEPT conditional on independent computational exhaustion; main lower bound unchanged; novelty unassessed.**
