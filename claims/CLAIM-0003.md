# CLAIM-0003 — Fixed-base conductor-two score obstruction

**VERIFIED RESULT, internal level 5.** Novelty is not established; this
auxiliary optimization result is recorded separately from CLAIM-0002.

Exact statement: for the fixed Duursma–Mak base k of genus 343 with 192
rational places, all finite nonrational supports S, conductor two at every
selected place and splitting sizes 1 <= t <= 192, the conservative score
specified in `proofs/NU2_OBSTRUCTION.md`, subject to its sufficient GS
criterion, has maximum **196608/620201**. This is an optimum of that score,
not an upper bound on the actual ratio of those towers or on A(2).

Proof: every strict improvement must have A <= 266, C <= 2280 and degrees
<= 47. The certified low stocks and hypothetical larger stocks form a
superset of all improving actual supports. Exact dynamic programming finds
no improvement; independent deficit/partition enumeration confirms this.
Attainment is provided by the geometric certificate of CLAIM-0002.

Evidence: `proofs/NU2_OBSTRUCTION.md`,
`results/all-degree-relaxation.json`, `tests/independent_obstruction.py`,
`results/INDEPENDENT_OBSTRUCTION.md`, and
`results/ASTRA_OBSTRUCTION_REVIEW.md`. Root-observed independent PASS closes
the reviewer's computational condition. Six corrupted certificate fields
are rejected. The low inventory prefix is pinned in production code.

Closest prior art: Duursma–Mak's theorem and genus-343 construction.
Separate bounded novelty audit: `references/obstruction-novelty-audit.md`.
No priority claim is made and this result is not added to the reviewed note.

Coding consequence: none beyond CLAIM-0002; its elementary binary AG
guarantee remains nonpositive. No exact ray degree or group structure is
claimed. Rational support, nonuniform or larger conductors, different bases,
stronger criteria and exact conductor averages are outside this obstruction.
No material objection remains open within the stated internal verification;
external mathematical review and bibliographic priority remain outstanding.
