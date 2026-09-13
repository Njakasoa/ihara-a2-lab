# M3 adversarial mathematical review

Reviewer: Astra delegated reviewer. Date: 2026-09-13.
Scope: mathematical review of the original conservative obstruction, proposed
local rank refinement, and exhibited T-unit receipt. No production code changed;
no novelty or public-priority approval is supplied.

## Verdict

**ACCEPT** the original all-depth obstruction for its expressly specified full
local conductor bound and conservative relation term b(b+1). The independent
scratch Fraction calculation reproduced 9861 candidate pairs, 7374 splitting
rejections, 2486 relation rejections, and the sole surviving tuple
(n,A,t,C_min,C_max)=(0,266,192,2236,2280). The accepted M2 obstruction is an
input, not re-proved here. Independent execution of the actual production
runner and receipt validation remain the assigned tester's responsibility.

**ACCEPT** the proposed stronger local relation argument under the finite-tower
contradiction hypothesis, for both the elementary ray quotient and full
2-primary abelian ray field. This is a genuinely different sufficient score:
the original obstruction must not be promoted to cover it.

**ACCEPT** v2(order of the T-split M2 ray group) <=312 from the exhibited
relations and accepted Jacobian order. This is an upper bound only. It supplies
neither the exact ray degree, group structure, nor inertia orders.

**Ray-structure status boundary.** The accepted claim is the conditional
upper bound \(v_2(|\operatorname{Cl}_{2S,T}(k)|)\le312\) obtained from the five
exhibited \(T\)-unit relations and the accepted Jacobian-order valuation. The
exact split ray-class order, its 2-rank and cyclic factors, and every exact
local inertia order remain **UNKNOWN**.

## Local decomposition argument

Let F=k_P and E_v/F be the finite abelian local extension coming from the
chosen global abelian ray field. Suppose the maximal unramified T-split tower
L/E is finite. It is Galois over k: E/k is Galois and the defining maximal
unramified splitting property is invariant under its automorphisms.

Every finite unramified extension M/E_v equals E_v F' for a suitable finite
unramified extension F'/F. For example, choose the degree of F'/F to be the
residue degree of M/F; uniqueness of unramified extensions in a fixed separable
closure gives the assertion. Both E_v/F and F'/F are abelian, hence M/F is
abelian. Apply this to M=L_w. The local decomposition group D is therefore
finite abelian, despite the global group possibly being nonabelian.

Since L_w/E_v is unramified, restriction injects inertia I(L_w/F) into
I(E_v/F), in fact identifies them by equality of ramification indices.
For an elementary ray field its rank is at most a=f floor(nu/2). For the
full abelian ray field the same bound holds: its inertia is a quotient of
U^1/U^nu, whose minimal generator number is a. (Subgroups of finite abelian
p-groups also have generator number no larger than their ambient group.)
The residue quotient D/I is cyclic, so d(D)<=a+1.

A finite abelian p-group on d minimal generators has a pro-p presentation
with d power relations and binom(d,2) commutators. Thus
r(D)-d(D)<=binom(d(D),2)<=a(a+1)/2. The inequality alone suffices; no exact
local group or minimal-presentation equality is needed. Substitution into
Duursma–Mak Theorem 4.1, dropping its nonpositive Delta term, gives the proposed
relation estimate. Proposition 5.3 supplies d(G)>=1+A-t, also for the maximal
elementary quotient because passing to G/2G preserves generator rank.

When using the scalar GS criterion, explicitly retain the increasing branch
of d^2/4-d (d>=2). With nonempty support, t>=1, t<=A, and a nonnegative proposed
margin, D0=1+A-t cannot equal 1 or 2; their squared margins are negative.
Thus no small-generator exception compromises the relevant application.

This argument cannot be extended merely by assuming that the global base
extension is a nonabelian p-extension: the abelian local compositum step is
essential. Nor does it justify treating the full abelian ray characters as
Artin–Schreier characters.

## Elementary conductor mean

For nu=2s and q=2^f the local exponent-two quotient has q^s characters, with
q^j-q^(j-1) of conductor 2j. Direct summation gives

    mean = 2s - 2(1-q^(-s))/(q-1),
    genus rebate = f(1-q^(-s))/(q-1).

For a proper global inertia image, the same expression is an upper bound
on mean conductor, not necessarily equality. The probability that a uniform
global character is trivial on an image filtration layer is the reciprocal
of that layer's order; quotienting can only reduce its order and hence reduce
the conductor tail probabilities. This supplies the required direction.
The AS rebate increases with s, unlike the full-ray rebate, so the old
rebate bound f/q must not be imported into this refined elementary score.

## Original obstruction and exchange audit

The full-character rebate identity, odd-depth reduction, degree-stock bound
37/16, rational rebate n/2, and high-degree bound A/1024 have the required
inequality directions. Overcounting low-degree A in the last term is harmless.
The global deficit C>=11A-690-10n follows from the exact rational minimum
min_{s>=1}(4s^2-13s)=-10 and the increasing nonrational deficit for f>=5.
The strict improvement endpoint uses ceil(E_n)-1, correctly excluding equality.
The t_min replacement makes the relation upper bound weaker on the positive
D branch and is legitimate.

At the surviving tuple, raising even depth beyond two costs at least155 in
the deficit accounting, whereas available slack is44. This excludes every
deep nonrational place without a degree cutoff. Rational support is already
excluded by the finite necessary-condition calculation. The remaining case
is exactly inside the accepted M2 all-degree depth-two obstruction.

The shallow replacement exchange identity is
C_old-C_new=f(s-1)(4fs-f+1), and its conductor improvement is strict for s>1.
It requires s distinct available places; the note states that condition.
These conclusions concern conservative sufficient scores, not finiteness of
rejected towers, actual tower ratios, or an upper bound on A(2).

## T-unit receipt and exact sequence

For nonempty rational T, use the localization/ray exact sequence

    O_T^* -> product_{P in S}(O_P^*/U_P^2)
          -> Cl_m(O_T) -> Cl(O_T) -> 0.

Here “T-split” describes the ray condition; the exact sequence is not asserted
to split as groups. Its local 2-primary part has order2^266. The five exhibited
base units x,x+1,y,y+1,y+x have divisors supported on T: the displayed norm
identities show their zeros are above x=0,1, and their poles are at infinity;
these six rational base places split completely in k. Their first local
coordinates are dlog(u), using the correct regular parameter in each chart.
At the two degree-five places the pullback of any base differential has
vanishing first coefficient because ramification index is32. Thus the five
base-unit rows alone suffice; additional eta rows are unnecessary for the
order bound.

I independently reduced the ten hexadecimal receipt rows over F2 and obtained
rank5. Deleting each individual local coordinate block preserves rank5,
which proves zero intersection of this known row space with every single
local block. This is not a proof of full inertia: hidden unit relations can
still meet those blocks. A nonzero projection of a relation onto a block is
also not enough to establish a relation supported only on that block.

Taking primary orders in the exact sequence yields local kernel order at
most2^(266-5). Since T contains a rational place, Cl(O_T) is a quotient of
Pic^0(k); its 2-primary order is at most2^51 from the frozen zeta certificate.
Consequently v2|Cl_m(O_T)|<=261+51=312. No assumption that the ten units generate
O_T^*, or that the Jacobian has rank51, is made. The accepted finite-field
coordinate geometry is an input; the separate tester should independently
recompute the coordinates, not merely rerun row elimination.

## Required remaining gates

1. Independent tester execution for production arithmetic and exact local
   finite-field coordinates, preserving the frozen certificate hashes.
2. Review of the final written refined criterion and its separate obstruction
   after integration; this report approves the mathematical argument described
   above, not unseen future edits or any finite search's exhaustiveness.
3. Separate claim and novelty audit before promoting any new result.

## Final refined-proof follow-up

Reviewed the complete written `proofs/M3_REFINED_RAY_CRITERION.md`,
`proofs/M3_REFINED_OBSTRUCTION.md`, and the production runner
`experiments/m3_refined_obstruction.py` after their creation.

**Final mathematical transcription verdict: ACCEPT.** Acceptance of the
production certificate as an independently executed artifact remains subject
to the separate tester's pass. The mathematical argument and finite necessary
calculation have no outstanding blocking finding from this review.

I independently reconstructed the refined rational arithmetic using only
Python Fraction and the displayed inequalities, without importing production
functions. It gives beta=1290176/608685, 11384 tested pairs, 7862 splitting
rejections, 3521 relation rejections, and exactly
(n,A,t,C_min,C_max)=(0,266,192,2236,2280).

The rebate accounting is valid also for rational places of depth above two:
subtracting n rather than their full rank mass only weakens the upper bound.
The refined deficit a(a-10) has rational minimum -25 and the claimed
nonrational minima. The complete argument imposes no unproved degree cutoff.

The available deficit slack is44. A single degree-five a=10 place consumes25;
two such places, a degree-six a=12 place, a degree-eight a=16 place, any deep
place of degree at least10, and a degree-five a>=15 place all exceed44.
With the single deep degree-five place, omitting the other degree-five place
or any degree-six place exceeds the remaining19, while at most one degree-eight
place may be omitted. With all sixteen degree-eight places the low contribution
is A=239,C=1964, leaving high mass27 and budget316. Omitting one leaves high
mass35 and budget388. Since high degrees are at least10, Cauchy gives the valid
relaxed lower bounds783/2 and1330/3, both above budget. Thus the reduction to
frozen M2 depth-two nonrational scope is complete.

**Pointwise comparison: ACCEPT.** For even depths, the elementary-ray and
rank-refined full-ray criteria use identical A and C. The elementary local
conductor mean is no larger than the full local mean, so every admissible
full-ray score is at most the elementary score with the same support and t.
At odd depths, lowering to the preceding even cutoff preserves local rank
and refined relation cost while lowering the full-character conductor cost;
it leaves the elementary ray field unchanged. Thus the all-depth elementary
obstruction covers the full-ray rank-refined score, and therefore the older
order-based score as well. This comparison does not include exact inertia
rebates or additional actual generator information.

One nonblocking wording improvement: in the local-compositum explanation,
choose the unramified base extension of degree f(L_w/k_P). Merely saying
“a degree divisible by f(E_v/k_P)” does not specify which multiple yields
exactly L_w, although the surrounding existence assertion is correct.
The scalar GS use, character restriction argument, and odd-cutoff reduction
in the final text otherwise preserve all hypotheses reviewed above.
