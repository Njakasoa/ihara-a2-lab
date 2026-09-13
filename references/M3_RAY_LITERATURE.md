# M3 primary literature audit: exact ray images and nonuniform conductors

Search cut-off: 2026-09-13. This is a bounded primary-source audit focused on
the following question: has the Duursma--Mak conductor-average method already
been combined with exact multi-place inertia images, exact character averages,
or a nonuniform-conductor optimization for an Ihara class-field tower?

The bounded search found no paper making that combination, and no prior exact
ray-group computation for the genus-343 Duursma--Mak base. Roland Auer's work
is the closest technical precedent: it computes ray fields through exact
local-unit images and a unit subgroup, but it predates Duursma--Mak and does
not give the M2 multi-place character average or the present GS optimization.

## Primary sources

### Duursma--Mak: the target method

Iwan Duursma and Kit-Ho Mak, “On lower bounds for the Ihara constants A(2) and
A(3),” Compositio Mathematica 149 (2013), 1108--1128.

* [arXiv record](https://arxiv.org/abs/1102.4127)
* [published PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B5E3A008AF40575A7B13F8F26236BEC1/S0010437X12000796a.pdf/on-lower-bounds-for-the-ihara-constants-a-2-and-a-3.pdf)
* [published DOI](https://doi.org/10.1112/S0010437X12000796)
* Local audited text: papers/duursma-mak-1102.4127.pdf and
  references/duursma-mak-paper.txt.

The relevant statements are:

* Theorem 1.1, pp. 1--2, gives the exact conductor--discriminant denominator
  \[
    g-1+\frac{1}{2[K:k]}\sum_{\chi}\deg f_\chi
  \]
  and explicitly says that exact character-conductor degrees are generally
  difficult; Corollary 1.2 replaces them by the modulus degree.
* Theorem 4.1, p. 5 and pp. 10--14, is Kuhnt's relation-generator argument
  for a finite \(L/K/k\) tower. It leaves the local term as
  \(r_p(G_P)-d_p(G_P)\).
* Proposition 5.1, pp. 14--15, bounds this local term for an abelian
  \(p\)-extension by
  \[
    \binom{e f_P(\nu_P-1)+1}{2}.
  \]
  The proof uses the order bound on a general inertia \(p\)-group. The paper
  does not replace that order by an exact inertia-image rank in its binary
  construction.
* Proposition 5.2, p. 15, is the conductor--discriminant formula. Proposition
  5.3 gives the ray p-rank lower bound.
* In the main binary construction, Proposition 5.5, pp. 18--19, the displayed
  quantity
  \[
    f'=2\sum_P n_P f_P(1-2^{-f_P})
  \]
  is used as an upper bound for the average conductor. The source does not
  enumerate the later ray characters, compute the T-unit image, or state exact
  local inertia orders.
* Remark 5.2, p. 20, compares the method with earlier elementary-abelian
  finite base extensions. It does not give the elementary-inertia replacement
  for Proposition 5.1 derived in proofs/M3_RAY_DUALITY.md.

This source confirms the M2 loss of information rather than supplying the M3
refinement.

### Auer: exact ray local images

Roland Auer, “Ray class fields of global function fields with many rational
places,” Acta Arithmetica 95 (2000), no. 2, 97--122.

* [arXiv record and PDF](https://arxiv.org/abs/math/9803065)
* [journal record](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/95/2/111908/ray-class-fields-of-global-function-fields-with-many-rational-places)
* [DOI](https://doi.org/10.4064/aa-95-2-97-122)

This is the closest primary precedent for the algebraic path in M3.

* Proposition 1.1, pp. 2--3, gives the exact idelic/ray sequence. Its local
  term is the product of \(U_P/U_P^{(m_P)}\), modulo the relevant global
  \(S\)-unit term. Taking the 2-primary part over F2 gives the principal-unit
  sequence used in (1) of proofs/M3_RAY_DUALITY.md.
* The Conductor Lemma (Proposition 1.2, p. 3) says that local reciprocity maps
  \(U_P^{(n)}\) onto the n-th upper ramification group. This is the source
  for the exact image-filtration law in (20)--(21) of that proof note.
* Proposition 1.3, pp. 4--5, identifies the maximal abelian extension with
  bounded conductor and prescribed completely split places.
* On p. 9 (equation (3)), Auer rewrites the sequence for a single modulus
  place as
  \[
    1\to U_S\cap U^{(n)}\to U_S\to U^{(1)}/U^{(n)}
      \to\operatorname{Gal}(K_S^{np}/K)\to\operatorname{Cl}(\mathcal O_S)\to1,
  \]
  and obtains the quotient \(U^{(1)}/U_SU^{(n)}\). This is an exact
  local-unit image computation, not a character-independence assertion.
* Section 3.5--3.6, pp. 17--18, gives a finite recursive procedure for the
  orders of the images of a chosen S-unit basis in all higher-unit quotients,
  and says that the resulting description determines ray-field degrees and
  genera.

Auer's setup generally uses one modulus place (often rational) and computes
specific ray fields and genera. It does not compute the multi-place,
T-split, 2-primary genus-343 group, the average in Theorem 1.1, or the M3
local relation term. It is a method precedent, not a prior M3 result.

### Kuhnt: relation ranks in the finite-base tower

Thomas Kuhnt, “Generalizations of Golod-Shafarevich and applications,” Ph.D.
thesis, University of Illinois at Urbana-Champaign, 2002.

* [doctoral record and abstract](https://globethesis.com/?t=1460390011978494) —
  bibliographic discovery only; this secondary record is not used as the
  mathematical source.
* The thesis is cited as reference [13] in Duursma--Mak.

The mathematical statement used here is Duursma--Mak Theorem 4.1, which
reproduces Kuhnt's Theorem 8.10. It bounds the relation-generator difference
of the finite
\(L/K/k\) tower by local decomposition terms, a split-place term, and a
global unit correction. Kuhnt's framework allows the finite base \(K/k\) to
be a p-extension and is the reason an elementary finite base can be useful.

The bounded audit found no theorem in the accessible record that computes
Duursma--Mak's character-conductor average from exact inertia images, and no
genus-343 or nonuniform-conductor optimization. The elementary-inertia
specialization in proofs/M3_RAY_DUALITY.md is consequently recorded as a
derived lemma with its finite-stage hypotheses, not attributed to Kuhnt
verbatim.

### Hajir--Maire: bounded wild depth and relation growth

Farshid Hajir and Christian Maire, “Extensions of number fields with wild
ramification of bounded depth,” International Mathematics Research Notices
2002, no. 13, 667--696.

* [arXiv record](https://arxiv.org/abs/math/0112319)
* [journal DOI](https://doi.org/10.1155/S1073792802106015)
* [open author PDF](https://members.femto-st.fr/christian-maire/sites/femto-st.fr.christian-maire/files/content/fichiers/hajir-maire-bounded_ramification.pdf)

This is a primary result on higher-ramification depth and relation-rank
difficulties, but it is a number-field paper. Its framework concerns
prescribed wild depth and root-discriminant bounds; it does not calculate a
finite-function-field ray class group's local character marginals. It is
relevant background for the warning that deeper ramification can add
relation cost, not a prior exact-inertia improvement of Duursma--Mak.

### Russell: geometric class field theory with modulus

Henrik Russell, “Geometric class field theory with bounded ramification,”
arXiv:1211.0883 (2012; current version 2023).

* [arXiv record](https://arxiv.org/abs/1211.0883)

Russell proves a general reciprocity and existence theorem for abelian
coverings with bounded ramification. This is a useful modern framework for
ray class fields with modulus, but the bounded search found no application
there to the Duursma--Mak A(2) parameter score, multi-place exact conductor
averages, or the genus-343 base.

### El Boukhari--Forrás: a 2026 adjacent p-primary result

Saad El Boukhari and Ben Forrás, “Class Number Relations in Abelian Extensions
of Global Fields,” arXiv:2607.10326 (11 July 2026).

* [arXiv record](https://arxiv.org/abs/2607.10326)

The paper studies generalized Stickelberger modules and p-primary
class-number divisibility relations, including the non-semisimple case
\(p\mid |G|\). It is a current primary source within the 2026 search window,
but it does not provide an exact inertia-image or character-average formula
for a multi-place T-ray field and does not improve the Duursma--Mak
genus-343 construction.

## Internal M3 broader-score audit (not literature)

The repository now contains a separate all-depth arithmetic obstruction using
the elementary-ray conductor mean and the rank-based local relation term:
proofs/M3_REFINED_RAY_CRITERION.md and proofs/M3_REFINED_OBSTRUCTION.md.
The receipt results/m3-refined-obstruction.json records 11,384 necessary
(n,A) pairs, 7,862 splitting rejections, 3,521 relation rejections, and the
single surviving necessary tuple
\[
 (n,A,t)=(0,266,192),\qquad 2236\leq C\leq2280.
\]
The deep-place cases are then excluded by the finite deficit and Cauchy
arguments in that proof.  This is an internal bounded arithmetic result.  The
mathematical review in results/M3_ASTRA_REVIEW.md accepted the criterion; an
independent execution/test now passes (results/M3_INDEPENDENT_VALIDATION.md).  It is not evidence that the
true ray group has been computed, and it is not a literature priority claim.
Its relation term relies on the elementary-base/local-abelianity lemma
recorded in proofs/M3_RAY_DUALITY.md.

## What the bounded audit establishes

The source comparison leaves four distinct statements:

1. Auer supplies an exact ray/local-unit sequence and a workable
   higher-unit image algorithm.
2. Duursma--Mak supplies the exact character-average denominator but uses a
   safe local modulus bound in the genus-343 example.
3. Kuhnt supplies the global relation-generator mechanism; its published
   instantiation does not automatically replace the local bound by exact
   T-unit block ranks.
4. No located primary source combines all three ingredients for the present
   multi-place binary ray field or performs the proposed nonuniform
   optimization.

The finite algebraic path is concrete: compute the principal-divisor lattice
of the 192 split places, evaluate its image in the 266-dimensional
principal-unit product, and then apply the exact marginal formula. For higher
depths, retain every unit-filtration layer. If the finite base is chosen
elementary abelian, the elementary-inertia lemma in
proofs/M3_RAY_DUALITY.md gives the separate relation-term proof obligation.

This audit records no strict new Ihara bound and makes no priority claim.
