# Note validation record

Date: 13 September 2026.

| Check | Evidence and status |
|---|---|
| M1 independent Sage geometry/zeta | [INDEPENDENT_VALIDATION.md](../results/INDEPENDENT_VALIDATION.md): INDEPENDENT_SAGE_STATUS=PASS. |
| M2 independent finite places and candidate | [INDEPENDENT_M2_VALIDATION.md](../results/INDEPENDENT_M2_VALIDATION.md): M2_CERTIFICATE=PASS, exit 0, SageMath 10.9; root reports a confirming final rerun with exit 0. |
| Unit tests | 29 tests passed in the root execution; persisted record: [UNIT_TESTS.md](../results/UNIT_TESTS.md). The mathematical reviewer did not rerun the suite. |
| Reproduction entrypoint | Root executed `python3 publication/reproduce.py` end to end: PUBLICATION_REPRODUCTION=PASS, including the independent auxiliary obstruction checker. |
| Standalone note degree-twelve certificate | Reviewer ran `python3 publication/checkers/degree12.py`: DEGREE12_NOTE_CHECK=PASS, exit 0. |
| Full proof and exchange lemma | [ASTRA_M2_REVIEW.md](../results/ASTRA_M2_REVIEW.md): mathematical acceptance; its independent-candidate completion condition is now satisfied by the final Sage pass. |
| Note mathematical transcription | [CONTRIBUTION_REVIEW.md](CONTRIBUTION_REVIEW.md): ACCEPT. |
| PDF build | Root completed Tectonic0.17.0 compilation, exit0. PDF has4 pages; all4 rendered pages visually inspected, no clipping or overflow. One harmless underfull bibliography paragraph remains in the TeX log. |

The independent M2 checker verifies all selected places and their exact Frobenius orbits, binds S/T and modulus rows to the inventories, recomputes the exact bound, and rejects adversarial mutations. Those checks support the finite and arithmetic inputs; the tower implication is covered by the mathematical review and published theorem inputs.

The note checker has no Sage dependency and imports no laboratory modules. It tests irreducibility by excluding every monic possible factor of degrees one through three, checks the H point, verifies its degree and the trace vector, and checks the six displayed conjugate encodings. This establishes the small arithmetic certificate; the passage from nonzero Frobenius to sixteen degree-twelve places uses the already proved geometry of k/H.

Validation does not compute the exact ray degree or group structure, prove unrestricted optimality, establish a positive binary coding gain, or settle priority. The [novelty audit](../references/M2_NOVELTY_VERDICT.md) remains a bounded public-source review with label POSSIBLY NOVEL and priority not established. These are internal checks, not external peer review. Draft preparation does not authorize external submission.
