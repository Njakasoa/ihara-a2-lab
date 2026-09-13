# CLAIM-M3-0001 — Rank-based local relations and elementary-ray score

Mathematical validity: **VERIFIED RESULT, internal level 5**; final written
proof accepted by Astra and independent arithmetic PASS. Publication novelty: **POSSIBLY NOVEL application**,
standard ingredients **KNOWN**. No priority claim.

Exact statement: for a finite abelian p-ray base E/k in the finite-tower
contradiction, the local decomposition groups upstairs are abelian and their
relation-minus-generator rank is at most a_P(a_P+1)/2, where
a_P=e f_P(ν_P−1−⌊(ν_P−1)/p⌋), over F_(p^e). For the binary maximal
elementary ray field, take ν_P=2s_P, A=Σf_Ps_P, C=Σ(f_Ps_P)(f_Ps_P+1).
With T nonempty rational and disjoint, t≤A and
(1+A−t)^2−2C−4A≥0 suffice for infinitude. The score is
t/(g(k)−1+Σ[f_Ps_P−f_P(1−2^(−f_Ps_P))/(2^f_P−1)]).

Relation to M2: at ν=2 both local rank and conductor law agree with M2.
For higher depths the local relation estimate improves; the elementary
conductor law is strictly smaller than the full local-character mean.
This changes the finite base field and does not compute the M2 actual mean.

Exact arithmetic: local unit orders, cyclic factors, all valuation layers,
full and order-two conductor histograms in `results/m3-local-units.json`.
The local enumeration is bounded to 22 fixtures of order at most 4096.

Ray assumptions and proof: `proofs/M3_REFINED_RAY_CRITERION.md`,
`proofs/M3_RAY_DUALITY.md`, and
`proofs/NONUNIFORM_CONDUCTOR_LOCAL_THEORY.md`. Finite base abelianity,
geometric constants, nonempty rational splitting, and g(k)>1 are retained.
Local independence is not assumed. Full groups need not have exponent two.

Independent verification/counterexamples: `tests/independent_m3.py` is the
separate implementation; its final report passes (results/M3_INDEPENDENT_VALIDATION.md).
`results/M3_ASTRA_REVIEW.md` accepts the final proof, including the scalar GS
branch and odd-cutoff comparison. Local mutation tests reject false arithmetic.

Novelty search: `references/M3_RAY_LITERATURE.md`; closest ingredients are
Duursma–Mak Theorem 4.1 (Kuhnt), Propositions 3.3 and 5.1–5.3, and Auer's
ray/local-unit theory. No general-criterion priority has been established.
Generalization: local relation argument works for other primes and base fields;
the displayed score uses binary elementary characters.

Open objections: no material internal objection remains; no exact global inertia or
rank is claimed. This does not yet improve the numerical Ihara bound or codes.

Related optimization principle: the stock-conditional exchange of one
degree-f depth-2s place into s shallow degree-f places preserves rank,
reduces the old relation cost by f(s−1)(4fs−f+1), and strictly improves
the conductor cost for s>1. See proofs/EXCHANGE_LEMMAS_M3.md and the final
scope/exchange review. This requires actual available places disjoint from T.
