# Astra M2 adversarial review — preliminary, 2026-09-13

**Decision at this stage: ACCEPT degree-12 support availability and its eligibility for the binary Duursma–Mak theorem; candidate acceptance remains pending.** M1's independent Sage pass was reported by the root. No M2 candidate or novelty claim is certified by this preliminary review.

Reviewed proofs/DEGREE12_PLACES.md, certificates/degree12-lifting.json and tests/independent_candidate.py, with the M1 geometry and p-primary theorem conventions retained.

## Degree-12 existence

The certificate lists thirteen distinct Frobenius orbits of length six on H over F64. The independent checker verifies the field modulus, H equations, nonvanishing c, orbit lengths, distinctness and all five trace coordinates. The nonzero trace vectors give elements of order two in Gal(k/H)=(Z/2)^5. The places are unramified because c is nonzero and M1 proves regularity elsewhere. Thus the decomposition group has order two, the residue extension degree is two, and each degree-six place has sixteen distinct degree-twelve places above it. Distinct base places give disjoint fibers. Therefore B12(k)>=208, independently of reconstructing the full zeta polynomial.

At zeros of a the affine H chart remains smooth by M1's nonzero reduced residues, so the use of affine coordinates and Frobenius orbits hides no normalization ambiguity. The separate 208-place inventory checker verifies seven coordinate equations and exact length-twelve orbits; it provides a second direct route to existence. The equality B12(k)=208 is unnecessary to any choice of at most 208 places and should continue to be attributed separately to the complete zeta computation.

## Arbitrary support and ray field

Any subset of these closed places can be included in S. The theorem requires distinct places disjoint from rational T; it requires no independence of their Frobenius elements in k/H, no complete fibers, and no stability under automorphisms of k/H. Each closed place is already a full constant-field Frobenius orbit. Additional nonrational degrees are automatically disjoint from T and from places of other degrees.

Take K to be the maximal abelian 2-primary subfield of the T-ray field with the proposed modulus, exactly as in M1. Passing to this subfield preserves T splitting and the local conductor bound, and preserves the 2-rank of the ray group. The generator estimate subtracts the splitting relations already; no extra independence assertion about the selected places is needed. The finite 32-degree field k/H and the later K/k must remain distinct in every candidate artifact.

For conductor two at a degree-f place, its inertia image has size at most 2^f. Restriction of a uniform character of Gal(K/k) to that inertia image is uniform: every character of a subgroup of a finite abelian group extends, and all fibers have equal size. The unramified fraction is at least 2^-f and there are no conductor-one 2-primary characters. Thus the mean local conductor is at most 2(1-2^-f), also for arbitrary degree-twelve support. Correlations between different places do not affect the sum of these expectations.

Writing n=[K:k], conductor-discriminant gives g(K)-1=n(g(k)-1+mean_conductor_degree/2), while T has n*t rational lifts. Their quotient cancels n exactly. An exact degree or class-group structure is unnecessary. Splitting of a nonempty rational T fixes the full constant field as F2. Since g(k)=343, an infinite unramified tower over K has unbounded genus.

## Pending candidate gate

- Check the actual candidate's t, distinct support IDs, available multiplicities, positive conductor depths, and exact GS inequality.
- Recompute the exact conductor upper bound and final rational comparison against 24576/77527 independently.
- Audit the claimed search scope and completeness separately; a found admissible row does not establish unrestricted optimality.
- At the time reviewed, tests/independent_candidate.py validates inventories but merely prints CANDIDATE_SEARCH=AVAILABLE (schema audit pending) when search output exists. Its INITIAL=PASS is **not a candidate arithmetic pass**. Extend and run that checker against the final schema before promoting a candidate.
- A novelty assertion requires the separate literature audit; none is made here. Ternary refinement remains excluded.

No mathematical obstruction to adding degree-twelve support was found. This is preliminary approval of an input and theorem applicability, not final approval of a bound.

## Final candidate attack — 2026-09-13

**Mathematical verdict: ACCEPT A(2)>=196608/620201, conditional only on completion of the independent candidate arithmetic/binding tests already assigned.** I read proofs/IMPROVED_BOUND.md end to end assuming its claim false, inspected certificates/m2-tower.json and CLAIM-0002.md, and checked the reference enumerator against the stated finite domain. No mathematical objection invalidating the bound was found. This verdict supersedes the preliminary candidate-pending conclusion above; the preliminary inventory and applicability arguments remain part of the review. This is not a novelty or priority verdict.

The candidate selects 37 distinct nonrational places, with degree multiplicities (2,16,16,2,1) at (5,6,8,10,12), and 192 distinct rational splitting IDs. Direct certificate arithmetic gives A=266, C=2260, D=75 and I=41. The finite-GS contradiction is strict: the relation-minus-generator upper bound is 1321, while 75²/4-75=5325/4=1331.25. Increasing d only strengthens this contradiction. The maximal split tower is Galois over k because its defining unramified and splitting conditions are stable under Gal(K/k); in the finite case its Galois group is a 2-group. The same published theorem inputs used in M1 therefore apply.

Potential hidden restrictions were attacked explicitly: S need not be a union of fibers in k/H, and previously ramified places of k/H are ordinary places of the new base k and may occur in the new modulus. The conductor bounds refer to K/k, not the composite K/H. No inertia independence, full-inertia assertion, exact ray degree, or class-group generator structure is needed. The p-primary quotient and conductor-two character restriction are exactly those justified above. T fixes constants at K and every tower stage. Riemann–Hurwitz ensures g(K)>1 and genus growth without relying on finite N/g.

Recomputation directly from the selected certificate rows gives conductor-degree upper mean 269993/512, denominator 620201/1024, and ratio 196608/620201. The exchange (10,10)->(8,12) preserves A, increases C by eight, reduces I by sixteen, and lowers the genus-denominator upper bound by 15/1024. The exact positive improvement is 368640/48082322927. All signs in the asymptotic inequality are correct: an upper bound on g(K)-1 gives a lower bound on the ratio. The optional certificate bounds 2^75<= [K:k] <=2^317 are consistent: 75 is the ray 2-rank lower bound, while the tame-free local ray factor has order at most 2^266 and the Jacobian 2-primary order is 2^51. Neither endpoint is asserted exact or used in the proof.

### Reference-search completeness

For fixed multiplicities and conductor two, the denominator is independent of t and positive. Under t<=A, D=1+A-t is positive. The GS condition is consequently equivalent to D>=ceil(sqrt(2C+4A)); the largest allowed t is exactly min(192,A,1+A-ceil(sqrt(2C+4A))). Thus choosing this single t exhausts every possible improving score for that support vector, including all t from 1 through 192. It does not silently exclude a negative-square branch because the theorem already requires t<=A.

The enumerator loops over all available multiplicities in the degrees supplied by the inventory. A score exceeding the historical b requires cost<192/b-342. Its fixed exclusive cap and nonnegative remaining costs therefore discard no strict improvement. Since an improvement is found, discarded equal-or-worse historical scores cannot affect the new optimum or its uniqueness. Integer isqrt with the explicit ceiling correction is exact; costs share the exact scale 4096. The output's unique maximizing multiplicity vector is consequently justified within this domain, conditional on the exact complete degree<=12 inventory and execution evidence. The same logic would not certify uniqueness at the historical bound if no improvement were found, because equality is pruned.

The scope must be described precisely: fixed k, nonrational S, degrees<=12, conductor two, rational splitting cardinality 1<=t<=192, and the particular conservative DM inequality/conductor-average score. “Unique maximum” means one multiplicity vector and t for this score. Many different concrete supports realize that vector; the computation proves neither a unique module nor optimality of exact ray-field conductor averages, nor an optimum across other degrees, conductors, curves or criteria. The bound itself does not depend on search completeness.

### Findings requiring integration

- **P2 documentation:** CLAIM-0002.md currently states that the general Luna engine supplies a second search, whereas the root reports no such artifact was delivered. Remove that sentence or mark the second search pending. No mathematical argument above relies on that engine.
- **P3 precision:** qualify the unique optimum as a multiplicity-vector optimum of the stated conservative score, not uniqueness of the support or tower. Preserve the distinction between mathematical validity and POSSIBLY NOVEL status.
- **Completion condition:** record a completed independent candidate check that binds every selected S/T ID and modulus row to the independently verified inventory and recomputes the arithmetic. The earlier INITIAL=PASS was not that check. The root reports five negative binding tests passed; final independent completion must still be evidenced separately. No second literature audit is needed for mathematical acceptance, but novelty remains a separate gate.

Reviewer execution additionally checked the certificate's multiplicities, ID uniqueness and disjointness, exact A/C/GS/denominator/ratio/gain and optional auxiliary-degree bounds using a short standalone Fraction calculation without importing the search engine. Source theorem and local-rank hypotheses were rechecked against the stored Duursma–Mak primary text, §5.1–5.2. No edits outside this review were made.

## Bounded review of the degree-exchange lemma

**ACCEPT** proofs/DEGREE_EXCHANGE_LEMMA.md as an elementary structural lemma for the binary conductor-two score. Degrees d and h are integers, h>=1, and d-h>=2; the required distinct replacement places must exist outside the current support and T. These hypotheses preserve a valid nonrational support and its splitting set.

The identities A'=A, C'=C+2h², D'=D and I'=I-4h² are exact. Computing 2w(d)-w(d-h)-w(d+h) gives the displayed Delta. Setting u=2^h, its numerator is d(u-1)²-h(u²-1)=(u-1)[d(u-1)-h(u+1)], proving the factorization and the stated strict positivity threshold. The condition I>=4h² includes equality correctly: the theorem accepts I'=0. Since t>0 and both denominators are positive, Delta>0 implies a strict improvement in the certified ratio. The specialization d=10,h=2 gives C'-C=8, I'=41 and Delta=15/1024, consistently with M2.

One implementation qualification for the final paragraph: using this lemma to prune a *restricted* search is legitimate only if the replacement also lies inside that search's declared domain (degree limits, multiplicity caps, and any other restrictions). A degree exchange leaving the domain does not disprove optimality within that domain. The lemma's unrestricted mathematical implication, with existence as stated, is sound. It says nothing about the exact genera of the two auxiliary ray fields or novelty of the identity. No numerical M1 rerun was needed.
