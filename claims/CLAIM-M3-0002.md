# CLAIM-M3-0002 — All-depth, rational-support refined-score obstruction

Mathematical validity: **VERIFIED RESULT, internal level 5**; final Astra
proof acceptance and independent execution PASS. Publication novelty: **POSSIBLY NOVEL**, priority unresolved.

Exact statement: on the fixed genus-343 Duursma–Mak base over F2, the score
of CLAIM-M3-0001 has exact maximum **196608/620201** over all finite supports,
all conductor bounds ν≥2, rational ramification allowed, and all nonempty
rational splitting sets T disjoint from S, subject to that sufficient
criterion. The theorem covers both the original conservative full-ray score
and its local-rank refinement by pointwise domination.

Relation to M2: extends the frozen ν=2/nonrational obstruction to arbitrary
depth, rational support and a stronger score. It does not bound actual tower
ratios or A(2) from above. Attainment is the frozen geometric M2 witness.

Exact arithmetic data: beta=1290176/608685, 11384 necessary (n,A) pairs,
7862 splitting rejections, 3521 relation rejections; sole survivor
(n,A,t,C_min,C_max)=(0,266,192,2236,2280). Slack44 admits only one possible
deep degree-five place; remaining high-degree Cauchy bounds 783/2>316 and
1330/3>388 exclude its two residual patterns. The terminal depth-two case
uses the already verified all-degree M2 obstruction.

Proof: `proofs/M3_REFINED_OBSTRUCTION.md`; computation:
`experiments/m3_refined_obstruction.py`, `results/m3-refined-obstruction.json`.
Ray assumptions are precisely those in CLAIM-M3-0001. Exact group ranks,
extra global correction and reduced actual inertias are outside this score.

Independent verification: Astra independently derived both caps/counts and
accepted the final proof in `results/M3_ASTRA_REVIEW.md`. The separate
`tests/independent_m3.py` arithmetic and mutation gate passes (results/M3_INDEPENDENT_VALIDATION.md).
The terminal M2 implementation is `tests/independent_obstruction.py`.

Counterexample search: necessary bounds are proved before enumeration, so
the finite arithmetic covers arbitrary degrees/depths; the 20 illustrative
assignments are not used to claim exhaustive coverage. False degree,
Frobenius, exponent, rank, multiplicity and GS certificates must be rejected.

Novelty search: separate `references/M3_RAY_LITERATURE.md`; Duursma–Mak is the
closest base and criterion. The audit located no identical obstruction, but
does not establish priority. Generalization potential: deficit/rebate caps
adapt to other inventories, with constants re-proved.

Open objections: no material internal objection remains. No new numerical A(2) bound or
coding improvement; the standard binary AG expression remains nonpositive.
