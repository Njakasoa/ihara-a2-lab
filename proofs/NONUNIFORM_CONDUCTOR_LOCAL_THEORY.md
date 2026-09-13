# Local units and character conductors in characteristic two

This note fixes the local formulae used before any nonuniform-conductor
search.  The input is a place \(P\) of degree \(f\) of a function field over
\(\mathbf F _2\).  Put

\[
  \kappa_P=\mathbf F_{q},\qquad q=2^f,
  \qquad \mathcal O=\kappa_P[[\pi]],
  \qquad U^r=1+\pi^r\mathcal O .
\]

The finite local group at depth \(\nu\) is

\[
             G_{f,\nu}=U^1/U^\nu .
\]

The formulas below concern this maximal local quotient.  An inertia image in
a global ray group can be a proper quotient of it; no equality with a global
image is assumed.

## 1. The unit quotient is generally not elementary abelian

The valuation map gives exact additive layers

\[
 U^r/U^{r+1}\simeq (\kappa_P,+),
 \qquad 1\leq r<\nu.
\]

Consequently

\[
 |G_{f,\nu}|=q^{\nu-1}=2^{f(\nu-1)},
 \qquad
 \dim_{\mathbf F _2}(U^r/U^{r+1})=f.
\]

These layers do not normally split as elementary abelian groups.  In
characteristic two,

\[
 (1+x)^{2^j}=1+x^{2^j}.
\]

Thus an element of \(G_{f,\nu}\) represented by \(1+x\) is killed by \(2^j\)
exactly when \(v(x)\geq\lceil\nu/2^j\rceil\).  Therefore, for \(j\geq0\),

\[
 \log_2|G_{f,\nu}[2^j]|
   = f\left(\nu-\left\lceil\frac{\nu}{2^j}\right\rceil\right).
 \tag{1}
\]

For \(j=0\) the right side is zero, and for \(2^j\geq\nu\) it is
\(f(\nu-1)\).  Define

\[
 d_j=f\left(\left\lceil\frac{\nu}{2^{j-1}}\right\rceil
       -\left\lceil\frac{\nu}{2^j}\right\rceil\right),
 \qquad j\geq1.
\]

Then \(d_j\) is the number of cyclic factors whose order is at least
\(2^j\).  The exact cyclic decomposition is

\[
 G_{f,\nu}
 \simeq
 \prod_{j\geq1}
   (\mathbf Z/2^j\mathbf Z)^{m_j},
 \tag{2}
\]

where only finitely many \(m_j\) are nonzero and

\[
 m_j=d_j-d_{j+1}
 =f\left(\left\lceil\frac{\nu}{2^{j-1}}\right\rceil
 -2\left\lceil\frac{\nu}{2^j}\right\rceil
 +\left\lceil\frac{\nu}{2^{j+1}}\right\rceil\right).
 \tag{3}
\]

In particular,

\[
 \boxed{\dim_{\mathbf F _2}(G_{f,\nu}/2G_{f,\nu})
       =f\left\lfloor\frac\nu2\right\rfloor},
 \tag{4}
\]

and the exponent of \(G_{f,\nu}\) is the least power of two at least
\(\nu\):

\[
 \exp(G_{f,\nu})=2^{\lceil\log_2\nu\rceil}
 \quad(\exp(G_{f,1})=1).
 \tag{5}
\]

For example, with one residue-field bit,

\[
 G_{1,2}\simeq C_2,\quad
 G_{1,3}\simeq C_4,\quad
 G_{1,4}\simeq C_4\times C_2,
\]

and

\[
 G_{1,6}\simeq C_8\times C_2^2.
\]

For general \(f\), every multiplicity in these examples is multiplied by
\(f\) whenever formula (3) gives the same exponent pattern.  In particular,
\(G_{f,\nu}\) is elementary abelian for all \(f\) only at depth
\(\nu\leq2\); the order \(q^{\nu-1}\) must not be confused with its
2-rank.

The exponent-two quotient in (4) is \(G_{f,\nu}/2G_{f,\nu}\), where
\(2G=G^2\) in multiplicative notation.  It is not the same object as the
valuation subgroup \(U^2/U^\nu\).  At \(\nu=4\), for example, the square
subgroup is the subgroup of squares in the truncated series group; replacing
it by a valuation layer gives the wrong quotient map even when cardinalities
happen to agree.  The direct checker computes the square subgroup explicitly.

## 2. Full abelian character law

Let \(\widehat G_{f,\nu}\) be the character group of \(G_{f,\nu}\), and give
the trivial wild restriction conductor zero.  For a character \(\chi\), its
wild conductor is the least \(r\geq1\) for which \(\chi\) is trivial on
\(U^r/U^\nu\).  There is no conductor-one jump for a 2-primary character;
the tame residue-field quotient has odd order.

The subgroup \(H_r=U^r/U^\nu\) has order \(q^{\nu-r}\).  The annihilator of
\(H_r\) in the full dual has order

\[
 \left|\{\chi\in\widehat G_{f,\nu}:a(\chi)\leq r\}\right|
  =|G_{f,\nu}/H_r|=q^{r-1},
 \qquad 2\leq r\leq\nu.
 \tag{6}
\]

Including the two initial conductor levels, the cumulative counts are

\[
 N_{\leq0}=1,
 \qquad N_{\leq1}=1,
 \qquad N_{\leq r}=q^{r-1}\quad(2\leq r\leq\nu).
 \tag{7}
\]

The exact counts are consequently

\[
 N_0=1,
 \qquad N_1=0,
 \qquad N_r=q^{r-2}(q-1)\quad(2\leq r\leq\nu).
 \tag{8}
\]

The exact average over all \(q^{\nu-1}\) local characters is

\[
 \begin{aligned}
 \overline a_{\rm all}(f,\nu)
 &=\frac{1}{q^{\nu-1}}
   \sum_{r=2}^{\nu}r\bigl(q^{r-1}-q^{r-2}\bigr)\\
 &=\nu-2q^{-(\nu-1)}-\sum_{j=1}^{\nu-2}q^{-j}.
 \end{aligned}
 \tag{9}
\]

The second line is the tail-sum form used in the conductor-discriminant
average.  At \(\nu=2\), it is \(2(1-q^{-1})\), the expression used in M2.
For \(\nu>2\), the additional filtration layers in (9) are mandatory.

Equation (9) is exact for the full local quotient.  If a global ray-class
character restricts through a proper inertia image \(I_P\), the local average
depends on the image and on the restriction map.  A global uniform character
distribution gives the probability \(1/|I_P^r|\) of triviality on each
image layer, but it does not assert that \(|I_P^r|=q^{\nu-r}\), nor that
different places are independent.

## 3. The order-two (Artin--Schreier) character law

Order-two characters are the dual of the elementary quotient

\[
 E_{f,\nu}=G_{f,\nu}/2G_{f,\nu},
 \qquad |E_{f,\nu}|=q^{\lfloor\nu/2\rfloor}.
 \tag{10}
\]

Local Artin--Schreier theory gives a second, stricter conductor law.  A
reduced Artin--Schreier representative has a pole of odd order \(m\), and
its conductor is \(m+1\).  Hence the allowed pole orders below a conductor
bound \(r\) are

\[
 1,3,5,\ldots <r,
\]

of which there are \(\lfloor r/2\rfloor\); each coefficient lies in
\(\mathbf F_q\).  Equivalently, direct annihilator computation in
\(G_{f,\nu}/2G_{f,\nu}\) gives

\[
 N^{\rm AS}_{\leq r}=q^{\lfloor r/2\rfloor},
 \qquad 0\leq r\leq\nu.
 \tag{11}
\]

Thus

\[
 N^{\rm AS}_0=1,
 \quad N^{\rm AS}_{2j}=q^j-q^{j-1}\ (j\geq1),
 \quad N^{\rm AS}_{2j+1}=0,
 \tag{12}
\]

with only exponents \(2j\leq\nu\) present.  The average over the order-dividing-two character quotient is

\[
 \overline a_{\rm AS}(f,\nu)
 =\frac{1}{q^{\lfloor\nu/2\rfloor}}
   \sum_{j=1}^{\lfloor\nu/2\rfloor}
      2j\bigl(q^j-q^{j-1}\bigr).
 \tag{13}
\]

The distinction is visible already at depth three.  The full group is
\(C_4^f\), and its full character group has \(q^2-q\) characters of
conductor three.  The Artin--Schreier quotient is only \(C_2^f\), with all
its nontrivial characters of conductor two.  Treating every abelian
2-primary character as Artin--Schreier would therefore undercount both the
character group and the possible conductor levels.

## 4. Duursma--Mak terms and the corrected nonuniform input

For the characteristic-two theorem of Duursma--Mak, Proposition 3.3 gives
the local generator contribution

\[
 A_P=f\left(\nu-1-\left\lfloor\frac{\nu-1}{2}\right\rfloor\right)
    =f\left\lfloor\frac\nu2\right\rfloor.
 \tag{14}
\]

This is exactly the local 2-rank in (4), while the theorem's relation estimate
uses

\[
 b_P=f(\nu-1),
 \qquad C_P=b_P(b_P+1).
 \tag{15}
\]

The global quantities in the sufficient criterion are the sums of \(A_P\)
and \(C_P\).  Formula (15) is a theorem upper-bound contribution; it does not
claim that a global ray group has this relation rank or that all local units
survive the global relations.

Odd conductor depths can be removed in this conservative score.  For
\(\nu=2s+1\), (14) equals the value at \(2s\), whereas (15) decreases after
replacing \(2s+1\) by \(2s\).  From (9),

\[
 \overline a_{\rm all}(f,2s+1)
 -\overline a_{\rm all}(f,2s)
 =1+(q-2)q^{-2s}>0.
 \tag{16}
\]

So the even depth \(2s\) has the same generator contribution and strictly
smaller conductor cost.  This reduction is a proof step, not a search
heuristic.

For an even depth \(\nu=2s\), the exact local full-character rebate from the
conductor average is

\[
 R_P=A_P-\frac f2\overline a_{\rm all}(f,2s)
 =f\left(q^{-(2s-1)}+\frac12\sum_{j=1}^{2s-2}q^{-j}\right).
 \tag{17}
\]

It satisfies

\[
 0\leq R_P\leq\frac f q,
 \qquad
 \frac f q-R_P
 =\frac{f(q-2)}{2q(q-1)}
       \left(1-q^{-(2s-2)}\right).
 \tag{18}
\]

Equality holds for \(s=1\) or \(q=2\).  In particular, deeper even layers
do not improve the per-place rebate beyond the depth-two value; for residue
fields larger than \(\mathbf F_2\), they strictly reduce it.

For comparison with the M3 obstruction, the relation contribution obeys

\[
 C_P-11A_P
 =f\left[f(2s-1)^2-9s-1\right]
 \quad(\nu=2s).
 \tag{19}
\]

At \(f=1\) this is \(4s^2-13s\), whose minimum is \(-10\).  For the certified
k343 nonrational stocks, the depth-two deficits at degrees \(5,6,8\) are
\(-25,-24,-16\) per selected place, and their available deficits sum to
\(-690\); degrees \(f\geq10\) have nonnegative contribution.  These are
aggregate inventory facts used by the separate M3 obstruction, not assertions
about exact global ray groups.

## 5. Independent finite arithmetic gate

src/m3_local_units.py contains both the closed formulas above and an
independent direct checker.  For \(q^{\nu-1}\leq4096\), it constructs
\(\mathbf F_q\) from an exact irreducible binary polynomial, enumerates all
coefficient tuples

\[
  1+a_1\pi+\cdots+a_{\nu-1}\pi^{\nu-1}\pmod{\pi^\nu},
\]

and multiplies them by truncated convolution.  It derives the element-order
profile, square subgroup, valuation subgroups, and both annihilator counts
directly.  The checker then compares these values with (1)--(15).  It does
not calculate a global ray-class group, an inertia image, a tower degree, or a
new Ihara score.

The correction implemented here is driven by the local unit calculation and
by Proposition 3.3 and Lemma 4.9 of the supplied Duursma--Mak source.  The
M2 expression \(2(1-2^{-f})\) is retained only at depth two; extending it to
\(\nu>2\), or treating \(G_{f,\nu}\) as elementary abelian, is rejected by
the exact formulas and the tiny-group enumeration.
