# Separate novelty audit: restricted conductor-two obstruction

Date: 2026-09-13. This audit concerns CLAIM-0003, not the arithmetic or
exhaustion checks. **Priority not established; no novelty assertion.**

The closest source is Duursma–Mak, *On lower bounds for the Ihara constants
A(2) and A(3)*, [arXiv:1102.4127](https://arxiv.org/abs/1102.4127), published
in Compositio Mathematica 149 (2013). Its theorem and genus-343 construction
are the inputs to the laboratory's restricted optimization. The source
reconstruction and initial literature coverage are recorded in
`m2-novelty-search.md`; the later audit of the improved fraction is in
`M2_NOVELTY_VERDICT.md`. Neither audit by itself establishes novelty of an
all-degree obstruction.

Additional public-index queries executed by the root:

```text
"Duursma" "Mak" "optimal" conductor
"Ihara" "620201" obstruction
"Duursma" "Mak" "343" optimization
```

No matching obstruction was identified among the returned results. The
relevant results pointed back to Duursma–Mak and to a 2013 thesis on class
field methods; other results were unrelated. This limited search does not
exclude unindexed proofs, equivalent formulations, unpublished observations
or earlier computational optimizations. It gives insufficient evidence for
a separate priority claim. The method uses elementary inequalities and exact
enumeration; no new general infinitude criterion is claimed.

Maintain CLAIM-0003 as a verified auxiliary barrier with unestablished
novelty. Its purpose is to justify moving beyond this particular conservative
score, not to advertise a bound on every tower or on A(2).
