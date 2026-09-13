# Mathematical contribution and transcription review

Review date: 13 September 2026. Reviewer: Astra, independent adversarial role within the laboratory.

**ACCEPT the mathematical transcription in main.tex and tables/parameters.tex.** The final independent candidate Sage pass reported by the root satisfies the computational condition in the earlier [full M2 proof review](../results/ASTRA_M2_REVIEW.md). No mathematical defect or numerical drift was found in the note. This is an internal review, not external peer review or a priority determination.

The contribution is accurately scoped as a change of support in the Duursma–Mak construction and theorem: (2,16,15,4,0) becomes (2,16,16,2,1) at degrees (5,6,8,10,12). It does not introduce a new base curve, general tower criterion, or recursive presentation. The table, GS margin 41, conductor mean 269993/512, denominator 620201/1024, bound 196608/620201 and exact gain 368640/48082322927 match the accepted proof. The auxiliary degree remains unspecified and cancels correctly. Rational splitting fixes constants and genus grows in the infinite unramified tower.

The simplified degree-twelve existence proof is sufficient and correct. The irreducible polynomial u^6+u+1 gives x=u degree six; y=u^4+u^2 satisfies H and c(x) is nonzero. The trace vector is (0,0,1,1,0). For h3=x², bh3/c² has bit encoding 48, and its six Frobenius conjugates are 48,60,47,38,36,32, whose XOR is one. Thus Frobenius has order two in the degree-32 elementary abelian cover, yielding sixteen distinct degree-twelve places. Only one is needed in the modified support. The note does not require the larger 208-place enumeration for this lemma. The standalone checker was read and executed successfully by this reviewer.

The exchange identity, fixed-support t maximum, and exact pruning implication agree with the reviewed proofs. The finite-domain maximum is correctly limited to the multiplicity vector and t of the conservative score; it is not a uniqueness assertion for divisors or a global tower optimum. The new search artifact and the reference enumeration support the statement that two implementations found the same vector. The bounded higher-depth neighborhood is not promoted to exhaustive general optimality.

The coding expression -423593/196608 is correct and its absence of a positive guarantee is stated. Attribution to Duursma–Mak is prominent. The AI-assisted workflow is disclosed, and internal checks are distinguished from external review.

The [bounded novelty verdict](../references/M2_NOVELTY_VERDICT.md) supports preparing a short note with label **POSSIBLY NOVEL**. Its public-source searches did not identify the exact antecedent, but do not establish absence or priority; the note preserves that limitation. No external submission or dissemination is implied by this review.

No mandatory mathematical repair remains. PDF compilation was not verified by this reviewer; see VALIDATION.md for the separate build status.
