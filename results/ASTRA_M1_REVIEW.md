# Astra adversarial M1 review — 2026-09-13

**Decision: ACCEPT the binary mathematical baseline conditionally on the independent arithmetic tests passing.** No mathematical counterexample or blocking defect was found in the reviewed binary proof. This is a reproduction of known bounds, not a new result. M2 may open after the root records successful independent verification and resolves any material discrepancies; this review alone does not assert that those runs finished.

Scope: NORMALIZATION.md; FINITE_GEOMETRY.md; SCHOOF_RECONSTRUCTION.md; ZETA_DECOMPOSITION.md; DUURSMA_MAK_RECONSTRUCTION.md; CONDUCTOR_FILTRATION.md; src/exact_curves.py, baselines.py, zeta_cover.py, schoof_control.py. Reviewed the stored Duursma–Mak transcription and Schoof's author PDF. Applied the repository's Astra reviewer role; no further agents were spawned. Only this report was edited.

## Findings and exact repairs

- **P2, verification gate:** independent field arithmetic and point counts remain an external completion condition of this review. Require recorded agreement for the local residue ranks, normalized low-degree counts/place inventories, all 31 quotient polynomials and their held-out n=14 counts, polynomial division, and the Schoof local data. A run that is pending or merely starts Sage is not a pass. The tester owns this evidence; do not rerun expensive checks solely to duplicate this review.
- **P3, proof exposition:** the step from d>=D to d²/4-d>=D²/4-D in DUURSMA_MAK_RECONSTRUCTION.md §3 needs the monotonicity domain stated. Add: “For an accepted row, I>=0 and A_S>=t>0 imply D²>=2C_S+4A_S>=4, while D>=1; hence D>=2. The function u²/4-u is nondecreasing for u>=2.” This is a clarification, not a counterexample to the acceptance test.
- **P3, status language:** “independently recomputed/certified” in FINITE_GEOMETRY.md and DUURSMA_MAK_RECONSTRUCTION.md should refer to a named completed independent artifact, not merely the shared Python implementation. Until the tester finishes, use “exactly recomputed; independent verification pending.” README's claim of three complete zeta polynomials is stale now that the k343 polynomial is included; update the count or omit it. Neither issue changes the bound.

## Geometry and counting audit

The local reduction is correct: adding sqrt(A)/t changes A/t²+B/t to (B+sqrt(A))/t modulo regular terms. The denominators a² and c² have no odd terms in their inverse-square expansion, so the derivative expressions for B omit no denominator term. Perfect residue fields supply the square root. Nonzero reduced simple poles remain nontrivial after extension of constants.

At a=0 the H chart also causes no hidden point-count correction: its derivative in x is 1+a'y; at y=sqrt(b), the nonzero reduced residue is exactly the assertion that this derivative is nonzero, up to a nonzero factor. Thus its unique affine point is the unique normalized point. At c=0, the rank-five maps rule out every nontrivial unramified quadratic character locally. Hence inertia is all of (Z/2)^5, with ramification index 32 and residual degree one. The two Frobenius orbits have degree five. This proves geometric degree 32, not just arithmetic degree 32.

All other finite functions are regular. At each H infinity place y has pole order at most three; bh/c² vanishes even for h=y². The two infinity places split into 64 rational points. The four finite rational H places split into 128 more. Total N(k)=192 is exact. Riemann–Hurwitz gives 2g(k)-2=32*2+31*20=684, hence g=343. Counting one point per H-point at c=0 is the normalized count; solving the unnormalized v equations there would not be a valid alternative. The low-degree inventory supplies every S multiplicity used in the bound, subject to independent arithmetic agreement.

## Zeta and class-group audit

Each nonzero character gives a genus-13 quadratic quotient: 2g-2=2*2+20=24. Character factorization gives P_k=product(P_C)/P_H^30. Thirteen counts plus the previously proved genus and functional equation determine each degree-26 polynomial uniquely; n=14 is a genuine held-out check. The code's Newton signs and reciprocal coefficient powers are correct. Repeated exact division produces degree 31*26-30*4=686.

Weil's theorem applies to the proved smooth projective geometrically connected models, so this geometric reconstruction proves the Weil property. Integrality and functional equation alone would not do so. An independent polynomial root-region check is useful verification, but is not an additional theorem needed once the geometry and counts are certified. P_k(1) is the Jacobian order. Its 2-adic valuation 51 does not certify generator rank 51 or any invariant-factor structure.

## Tower and conductor audit

For the main binary row, A_S=266, C_S=2252, D=75 and I=57. The finite-group relation bound 1317 is below 75²/4-75=5325/4. The exact conductor average upper bound is 33751/64, giving denominator 77527/128 and A(2)>=24576/77527. These are inequalities for an infinite split tower, not a conclusion from finite N/g.

K must mean the p-primary T-ray field in this proof. Its exact degree is not known here and is unnecessary: the degree cancels between split rational points and Riemann–Hurwitz. Taking a full ray field literally could introduce tame and prime-to-p factors outside the stated p-group argument. The explicit convention in the reconstruction repairs that problem. Nonempty rational T fixes constants throughout; g(K)>1 then forces genus growth in an infinite unramified tower.

The filtration proof is valid for every stated binary depth: restriction of uniform global characters to the image I^r is uniform, so Pr(a<=r)=1/|I^r|. The local image can be smaller than U^r/U^nu, only improving the bound. I^0=I^1 for a p-primary extension gives the duplicated initial term. Thus E[a]<=nu-2Q^{-(nu-1)}-sum_{j=1}^{nu-2}Q^{-j}, with no independence assumption between places. It is an upper bound, not an asserted exact global average.

Odd binary depth nu=2m+1 has the same generator contribution as nu-1, a smaller relation cost after replacement, and a smaller conductor upper bound. Indeed the difference of successive conductor bounds is 1+(Q-2)/Q^{nu-1}>0. Therefore odd depths >=3 are dominated for this conservative Theorem 1.1 score. This does not establish dominance for exact ray groups or other tower criteria.

## Schoof control and exclusions

The corrected model y²+y=x³+x has five rational points. For w²+w=bx/d², the nine simple denominator zeros are exhausted by the four degree-four and five degree-five points. Reduction removes the poles at the former and leaves conductor 2P5 at the latter; infinity is regular with zero residue. Hence Y has genus six and ten rational points. Base-changing u²+u=1/b produces eight rational simple poles on Y, hence genus X=19, and four split infinity places.

The S-unit ranks are one on Y and three on X. The published genus-theory bound is d2 Cl_S>=8-1-1=6; Schoof's criterion permits equality at 2+2sqrt(3+1)=6. Thus the resulting bound is 4/18=2/9. This uses the corrected explicit realization and published criterion, not an invented full class-group calculation. Source: [Schoof author PDF](https://reneschoof.github.io/CurvesF2.pdf), §§2–3.

The ternary refined fraction is explicitly NOT certified here and is outside this gate. No inference about novelty, global family optimality, exact ray degree, or class-group structure is accepted. Preserve those exclusions in M2.

Targeted reviewer execution: local_certificate(), published_controls(), and schoof_control.certificate() completed successfully using the existing Python code. These are consistency checks, not an independent Sage implementation. Final gate: **binary proof ACCEPT; independent computational completion required before M1 is marked complete and M2 starts.**
