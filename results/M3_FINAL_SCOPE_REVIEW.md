# M3 final scope and exchange review

Reviewer: independent Astra reviewer. Date: 2026-09-13.
Bounded review of M3_RESULT.md, CLAIM-M3-0001 through CLAIM-M3-0003,
EXCHANGE_LEMMAS_M3.md, the refined criterion and obstruction, the prior Astra
review, the independent validation report, and relevant ray-duality formulas.
No production files changed and no new literature or priority audit performed.

## Verdict

**ACCEPT for the final claim scope and exchange principle.** The claims
distinguish sufficient-score optimization from actual tower ratios and A(2),
the elementary conductor estimate from a full-ray actual mean, and a ray-order
cap from exact group structure or inertia. The maximum 196608/620201 is scoped
to the specified fixed-base sufficient score. CLAIM-M3-0003 asserts only
2^75 <= |G| <= 2^312, consistent with the generator lower bound and the five
known independent unit relations; zero intersection of their known subspace
with every block is not promoted to a full-inertia assertion.

The independent report records PASS, including 11384 necessary pairs and raw
finite-field reconstruction of the rank-five relation space. This review does
not substitute for the root's consolidated replay or its commit/hash receipt.
Pending-status prose will be updated by the integrator and is not a blocker.
Novelty remains expressly unresolved, with no new numerical Ihara or coding
improvement and no public-priority assertion.

## Explicit exchange check

For the old conservative C, a degree-f place of depth 2s contributes

    C_old = f(2s-1)[f(2s-1)+1].

Replacing it by s distinct degree-f places of depth two contributes

    C_new = s*f*(f+1).

Direct expansion gives

    C_old-C_new
      = f^2*(4s^2-5s+1)+f*(s-1)
      = f*(s-1)*(4fs-f+1).

This vanishes at s=1 and is positive for every integer f>=1, s>1.
A_old=A_new=fs and t is unchanged, so the GS margin increases by twice
this difference. The old full-character rebate

    r_f(s)=f/[2(2^f-1)]*[1+(2^f-2)*2^(-f(2s-1))]

is at most f/2^f, whereas the new aggregate rebate is s*f/2^f.
Thus the genus cost strictly decreases for s>1, and the positive-t score
strictly improves while admissibility is preserved. This includes f=1,
where the old rebate is exactly 1/2 at all depths. The required stock and
disjointness conditions are explicit: all replacement places must be distinct,
outside T, and outside the retained support. The removed original place may
be reused as one of these shallow places.

The displayed old-C identity must not be relabeled as the refined-C identity.
For the refined C it would instead be f^2*s*(s-1); the document consistently
uses the conservative convention in this discussion and its deficit method.
Odd-depth reduction also keeps A fixed while lowering conservative C and
the full-character conductor estimate, as asserted.

## Actionable ancillary correction

In proofs/M3_RAY_DUALITY.md, equation (18) displays the two exponential terms
in the wrong order. Subtracting equation (16) from equation (17) gives

    safe mean - exact mean = 2*sum f*(2^(-f+rho)-2^(-f)).

This is positive when some rho>0, agreeing with the following prose. The
printed reversed difference is negative in that case. Correct this sign
before final integration. It does not affect the accepted score obstruction,
exchange proof, or ray-order cap, which do not use this erroneous saving
expression. The reviewer reported this finding directly to the integrator.

## Root integration resolution

The integrator corrected equation (18) to the exact expression requested
above and checked it against equations (16) and (17). This closes the sole
ancillary finding; the mathematical claims and executable scores are unchanged.
