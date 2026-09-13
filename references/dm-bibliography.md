# Duursma–Mak source map

This file records the primary source used for the reconstruction.  The version
audited here is arXiv:1102.4127v4 (14 October 2012), the 22-page version that
became Compositio Mathematica 149 (2013), 1108–1128.

* arXiv record: <https://arxiv.org/abs/1102.4127>
* arXiv v4 PDF: <https://arxiv.org/pdf/1102.4127v4>
* arXiv HTML transcription: <https://arxiv.org/html/1102.4127>
* Published article DOI: <https://doi.org/10.1112/S0010437X12000796>
* Cambridge PDF: <https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B5E3A008AF40575A7B13F8F26236BEC1/S0010437X12000796a.pdf/on-lower-bounds-for-the-ihara-constants-a-2-and-a-3.pdf>

The original lab archived the PDF and extracted text locally. Those third-party
copies are excluded from this public snapshot; use the source links above.
Historical download hashes remain in `references/source-manifest.json`.
Printed page numbers below refer to the article pages.

## Page and theorem crosswalk

| Source item | Printed pages | Role in the reconstruction |
| --- | ---: | --- |
| Theorem 1.1 and Corollary 1.2 | 1–2 | General admissibility condition and the conductor-average lower bound. |
| Theorems 1.3 and 1.4 | 2 | Stated decimal bounds for `A(2)` and `A(3)`. |
| Theorem 2.1 | 3 | Golod–Shafarevich inequality `r_p(G)>d_p(G)^2/4`. |
| Proposition 3.3 and Theorem 3.2 | 4–5 | Higher-unit p-rank and generator-rank input. |
| Theorem 4.1 and its proof | 5, 10–14 | Kuhnt’s relation-rank estimate and removal of excess ramification. |
| Proposition 5.1 | 14–15 | Local upper bound `r_p(G_P)-d_p(G_P)`. |
| Propositions 5.2 and 5.3 | 15 | Conductor–discriminant genus formula and ray-field p-rank. |
| Construction proving Theorem 1.1 | 15–17 | `k`, `K=k_m^T`, the class-field tower, and the exact algebra leading to (1.1). |
| Proposition 5.4 | 17–18 | First binary example: genus 276 and bound `0.316837…`. |
| Proposition 5.5 / Theorem 1.3 | 18–19 | Main binary example: genus 343 and `0.316999…`. |
| Proposition 5.6 / Theorem 1.4 | 19 | Ternary example and `0.492876…`. |
| Remark 5.2 | 20 | Comparison with the usual class-field-tower inequalities. |

The paper’s displayed main binary model says “the compositum of the extensions
`E(v)`” on p. 18 immediately after defining `H`.  The coefficients and the
function `h` are elements of `H=F_2(x,y)`, and the preceding `E` is the base of
the *other* binary construction.  Throughout the reconstruction this is read
as `H(v)` and marked as a source typo/anomaly; no mathematical claim depends on
the literal symbol `E(v)`.

## Historical control

René Schoof, *Algebraic curves over F_2 with many rational points*, Journal of
Number Theory 41 (1992), 6–14:

* author PDF: <https://reneschoof.github.io/CurvesF2.pdf>
* DOI: <https://doi.org/10.1016/0022-314X(92)90079-5>

Schoof’s abstract and p. 14 give the genus-19 curve with an infinite split
class-field tower and the bound `A(2) >= 4/(19-1)=2/9`.  The scan on p. 13
prints `E: Y^2+Y=T^3+1` while simultaneously claiming five rational points;
that printed equation has only three `F_2`-points.  The control therefore uses
the arithmetically compatible maximal elliptic model
`E: y^2+y=x^3+x`, and labels this as a correction of an internal source
inconsistency rather than as a new result.
