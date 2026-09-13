# M3: exact ray duality and conductor averages

This note records exact ray identities and finite proof obligations.

The frozen base is the genus-343 field \(k/\mathbf F _2\), with
\(N_1(k)=192\).  The M2 ramification inventory is
\[
 (f_P,n_P)=(5,2),(6,16),(8,16),(10,2),(12,1),\qquad \nu_P=2,
\]
where \(n_P\) counts places of degree \(f_P\).  Thus
\(\sum_{P\in S}f_P=266\), and the certified Jacobian-order datum is
\(v_2(|\operatorname{Cl}^0(k)|)=51\).  The latter is a valuation of an order;
it is not a claim about the \(2\)-rank or invariant factors.

## 1. The \(2\)-primary ray exact sequence

For a place \(P\), put
\[
 U_P^{(r)}=1+\mathfrak p_P^r\subset k_P^\times,\qquad
 U_P^{(0)}=\mathcal O_P^\times,
\]
and let
\[
 \mathfrak m=\sum_{P\in S}\nu_P P,\qquad
 V_P:=U_P^{(1)}/U_P^{(\nu_P)},\qquad
 U_{\mathfrak m}=\prod_{P\in S}V_P.
\]
Write \(C_{\mathfrak m}=\operatorname{Cl}_{\mathfrak m}^0(k)\) for the
degree-zero ray divisor class group, and set
\[
 C=(C_{\mathfrak m})_{(2)},\qquad
 A_0=(\operatorname{Cl}^0(k))_{(2)}.
\]
The standard ray sequence, after taking \(2\)-primary parts, is
\[
 0\longrightarrow U_{\mathfrak m}\longrightarrow C
   \xrightarrow{\pi} A_0\longrightarrow0. \tag{1}
\]
At \(P\), the local factor
\(\mathcal O_P^\times/U_P^{(\nu_P)}\) has a residue-unit factor
\(\kappa(P)^\times\) and a principal-unit factor
\(U_P^{(1)}/U_P^{(\nu_P)}\).  Since
\(|\kappa(P)^\times|=2^{f_P}-1\) is odd and
\(\mathbf F _2^\times=1\), the \(2\)-Sylow is exactly the principal-unit
factor.  Primary parts are exact for finite abelian groups, giving (1).
No splitting of (1) is assumed.

Because every graded quotient \(U_P^{(r)}/U_P^{(r+1)}\) has size \(2^{f_P}\),
\[
 |C|=|A_0|\prod_{P\in S}2^{f_P(\nu_P-1)}. \tag{2}
\]
For M2, \(U_{\mathfrak m}\simeq(\mathbf F _2)^{266}\), hence
\[
 |C|=2^{51+266}=2^{317}. \tag{3}
\]
This is the order before imposing \(T\)-splitting, not the order of the
\(T\)-split ray group.

## 2. Imposing \(T\)-splitting

All 192 M2 splitting places are rational.  Fix \(P_0\in T\), and define
\[
 \tau_Q=[Q-P_0]_{\mathfrak m,2}\quad(Q\in T\setminus\{P_0\}),\qquad
 J_T=\langle\tau_Q:Q\in T\setminus\{P_0\}\rangle\leq C.
\]
The geometric maximal abelian \(2\)-extension with conductor bounded by
\(\mathfrak m\) and \(T\) split is classified by
\[
 G_{\mathfrak m,T}^{(2)}=C/J_T. \tag{4}
\]
The degree-zero formulation is valid because \(T\) is rational.  A
non-rational splitting set requires degree-zero combinations with degree
weights.

Put \(J_A=\pi(J_T)\leq A_0\) and \(J_U=J_T\cap U_{\mathfrak m}\).  Quotienting
(1) gives
\[
 0\longrightarrow U_{\mathfrak m}/J_U\longrightarrow
 G_{\mathfrak m,T}^{(2)}\longrightarrow A_0/J_A\longrightarrow0. \tag{5}
\]
In particular,
\[
 |G_{\mathfrak m,T}^{(2)}|
 =\frac{|U_{\mathfrak m}|\,|A_0|}{|J_T|}. \tag{6}
\]
There are 191 displayed generators for \(J_T\), but this does not imply
\(|J_T|\leq2^{191}\): a generator can have order \(2^a\), and (1) need not
split.  The certified data give (3) and
\(d_2(G_{\mathfrak m,T}^{(2)})\geq75\), but not \(J_T,J_A\), invariant factors,
or the exact order in (6).

## 3. The \(T\)-unit relation image

Define
\[
 \mathcal E_T=
 \{u\in k^\times:v_Q(u)=0\text{ for }Q\notin T\}/\mathbf F _2^\times .
\]
This is a free abelian group of rank \(|T|-1=191\).  A \(T\)-unit is a local
unit at every \(P\in S\), so its \(2\)-primary local residues define
\[
 \lambda_{\mathfrak m,2}:\mathcal E_T\longrightarrow U_{\mathfrak m}. \tag{7}
\]
The sign depends on the Artin-map convention and does not affect the subgroup.
The exact relation identity is
\[
 \operatorname{im}(\lambda_{\mathfrak m,2})
   =J_U=U_{\mathfrak m}\cap J_T. \tag{8}
\]
Indeed, a \(T\)-unit has a degree-zero divisor supported on \(T\), with
principal ordinary class, giving one inclusion.  Conversely, an element of
\(J_U\) is represented by a \(T\)-supported degree-zero divisor \(D\) whose
\(2\)-primary ordinary class is trivial.  The remaining ordinary class has
odd order, so an odd integer \(a\) kills it and \(aD=(u)\) for a \(T\)-unit \(u\).
Multiplication by \(a\) is an automorphism of the \(2\)-group \(U_{\mathfrak m}\),
giving the other inclusion.

Thus the local relation image needs the principal-divisor lattice supported
on \(T\), not a decomposition of the whole Jacobian.  Exact
Riemann--Roch/principality tests followed by local residue evaluation give a
finite route.  The certified information is
\[
 5\leq\dim_{\mathbf F _2}\operatorname{im}(\lambda_{\mathfrak m,2})
 \leq191. \tag{9}
\]

For the explicit genus-343 field, the five functions
\[
 x,\quad x+1,\quad y,\quad y+1,\quad y+x \tag{10}
\]
are certified \(T\)-units.  Their zeros and poles lie above the six rational
places of \(H\), which split completely in \(k\); the norm identities
\[
 N(y)=x(x+1),\qquad N(y+1)=x^2(x+1),\qquad
 N(y+x)=x^2(x+1)^2
\]
give an exact divisor check.  The five additional functions
\[
 \eta_h=\frac{w_h}{w_h+1},\qquad h\in\{1,x,x^2,y,y^2\}, \tag{10a}
\]
are also certified \(T\)-units: from \(w_h^2+w_h=bh/c^2\),
\(\eta_h=w_h^2/(bh/c^2)\), so their zeros and poles are over the checked
zero loci of \(bh\), while at a pole of \(w_h\) the ratio is a unit.  Their
local rows add no rank to the five base-unit rows.  The exact finite receipt
results/m3-ray-structure.json records rank 5 for the known relation space and
\(\dim(R_{\rm known}\cap V_P)=0\) for every one of the 37 local blocks.  This
proves no single-block inertia drop from the displayed relations; it does not
prove the same for the full, still unknown, \(T\)-unit group.

## 4. Exact local inertia and mean conductor

Let \(\iota_P\) be local reciprocity from the finite local block
\(V_P=U_P^{(1)}/U_P^{(\nu_P)}\) into
\(G=G_{\mathfrak m,T}^{(2)}\), and let \(I_P\) be its image.  With \(V_P\)
embedded as the \(P\)-block of \(U_{\mathfrak m}\),
\[
 I_P\simeq
 V_P/\bigl(V_P\cap J_T\bigr). \tag{11}
\]
For \(\nu_P=2\),
\(U_P^{(1)}/U_P^{(2)}\simeq(\kappa(P),+)\simeq(\mathbf F _2)^{f_P}\).
Set
\[
 \rho_P=\dim_{\mathbf F _2}\bigl(V_P\cap J_T\bigr). \tag{12}
\]
Then
\[
 |I_P|=2^{f_P-\rho_P}. \tag{13}
\]

A drop can be proved without the full Picard group by exhibiting a \(T\)-unit
whose vector under (7) is nonzero in the \(P\)-block and zero in every other
\(S\)-block.  To prove \(\rho_P=0\), the complete image in (8) must have no
such vector; a partial unit list is insufficient.  A relation supported in
several blocks changes \(J_U\), but by itself does not reduce any individual
inertia order.

Let \(\widehat G\) be the character group of \(G\), with the uniform
distribution used in the conductor--discriminant average.  Restriction
\(\widehat G\to\widehat{I_P}\) is onto and has equal-size fibers, so
\[
 \Pr_{\chi\in\widehat G}(\chi|_{I_P}=1)=\frac1{|I_P|}. \tag{14}
\]
There are no conductor-one \(2\)-primary characters: the residue-unit quotient
has odd order.  Thus \(a_P(\chi)\) is 0 for the trivial local restriction and
2 otherwise.  Equations (13)--(14) give
\[
 \mathbb E[a_P]
 =2\left(1-\frac1{|I_P|}\right)
 =2\left(1-2^{-f_P+\rho_P}\right). \tag{15}
\]
Consequently the exact mean conductor degree is
\[
 \overline F_{\rm exact}
 :=\frac1{|G|}\sum_{\chi\in\widehat G}\deg f_\chi
 =2\sum_{P\in S}f_P\left(1-2^{-f_P+\rho_P}\right). \tag{16}
\]
M2 used the safe specialization \(\rho_P=0\):
\[
 \overline F_{\rm M2,safe}
 =2\sum_{P\in S}f_P(1-2^{-f_P})
 =\frac{269993}{512}. \tag{17}
\]
Equation (17) remains an upper bound when the \(\rho_P\) are unknown.  The
exact saving is
\[
 \overline F_{\rm M2,safe}-\overline F_{\rm exact}
 =2\sum_{P\in S}f_P
   \left(2^{-f_P+\rho_P}-2^{-f_P}\right). \tag{18}
\]
It is positive exactly when some \(\rho_P\) is positive.

No independence assumption occurs in (16): degree is a sum of local
exponents, so linearity of expectation suffices.  Correlations matter for the
joint conductor distribution, multi-place character constraints, and
enumeration, but cannot alter the mean once the local inertia orders are known.
Duursma--Mak therefore gives
\[
 \frac{t}{g(k)-1+\overline F_{\rm exact}/2}, \tag{19}
\]
without knowing \(|G|\); the ray degree cancels.

## 5. All conductor depths

For arbitrary \(\nu_P\geq2\), let \(I_{P,r}\) be the image in \(G\) of
\(U_P^{(r)}\), with \(I_{P,\nu_P}=1\).  On the \(2\)-primary quotient tame
inertia is absent, so \(I_{P,0}=I_{P,1}\).  For
\(0\leq r\leq\nu_P-1\),
\[
 \Pr(a_P(\chi)\leq r)=\frac1{|I_{P,r}|}. \tag{20}
\]
The tail-sum identity gives
\[
 \mathbb E[a_P]
 =\nu_P-\sum_{r=0}^{\nu_P-1}\frac1{|I_{P,r}|}. \tag{21}
\]
Using only \(|I_{P,r}|\leq2^{f_P(\nu_P-r)}\) and \(I_{P,0}=I_{P,1}\) gives
\[
 \mathbb E[a_P]\leq\nu_P
 -2\,2^{-f_P(\nu_P-1)}
 -\sum_{j=1}^{\nu_P-2}2^{-f_Pj}. \tag{22}
\]
For \(\nu_P=2\), this is \(2(1-2^{-f_P})\).  At higher depth, exact
calculation needs every unit-layer image order, not only the order of the full
local quotient.  The depth-two formula cannot be reused at higher depth.

## 6. Full ray group versus an elementary quotient

The full \(T\)-split group \(G\) may have cyclic factors of order \(4,8,\ldots\).
Its maximal elementary abelian quotient is
\[
 G_{\rm el}=G/2G,\qquad
 \widehat{G_{\rm el}}=\widehat G[2]. \tag{23}
\]
The elementary quotient averages only order-two characters, whereas (16)
averages all characters of \(G\).  There is no general inequality between the
two means.

With \(C,J_T\) as above,
\[
 G_{\rm el}\simeq C/(2C+J_T), \tag{24}
\]
and
\[
 I_{P,\rm el}\simeq
 V_P/\bigl(V_P\cap(2C+J_T)\bigr). \tag{25}
\]
At depth two,
\[
 \mathbb E_{\widehat{G_{\rm el}}}[a_P]
 =2\left(1-\frac1{|I_{P,\rm el}|}\right). \tag{26}
\]
The extra \(2C\) in (25) matters: a local unit can survive in the full ray
group but vanish after passage to the elementary quotient.  A full-group
relation also need not describe the order-two average unless it is visible
modulo \(2C\).

For the maximal local elementary quotient at even depth \(\nu=2s\), put
\(Q=2^{f_P}\).  The subspace of order-two characters with conductor at most
\(2j\) (equivalently at most \(2j+1\)) has size \(Q^j\), for
\(0\leq j\leq s\).  Its uniform local mean is therefore
\[
 \overline a_{\rm el}(f_P,2s)
 =2s-2\sum_{j=1}^{s}Q^{-j}
 =2s-2\frac{1-Q^{-s}}{Q-1}. \tag{26a}
\]
For a proper global elementary inertia image, (26a) is a safe upper bound:
each image filtration layer can only be smaller, increasing the probability
of a lower conductor.  Equality requires the corresponding local image
orders.  An odd cutoff \(2s+1\) gives the same order-two character space,
because its positive conductor exponents are even.  This elementary formula
must not be substituted for the full-ray law (21).

### Elementary-base refinement of the GS relation term

There is a valid route beyond the full-group conductor mean, provided the
finite base of the tower is chosen to be an abelian elementary extension.
Let \(E/k\) be an abelian elementary \(2\)-extension with \(T\) split and
depth at most \(\nu\), and let \(L/E\) be an unramified finite \(2\)-extension
at a finite stage of the Kuhnt tower.  For a place \(P\) of \(k\), choose
compatible places in \(E\) and \(L\).

First, \(L_P/E_Q\) is unramified.  The inertia exact sequence therefore
injects \(I(L_P/k_P)\) into \(I(E_Q/k_P)\), which is elementary because
\(E/k\) is elementary.  Thus \(I(L_P/k_P)\) is elementary.  Next, the local
extension \(E_Q/k_P\) is abelian.  Every finite unramified extension of \(E_Q\)
is the compositum of \(E_Q\) with a suitable finite unramified extension of
\(k_P\): both fields have the required finite residue extension inside a
fixed maximal unramified extension.  The latter extension is cyclic, so the
compositum is abelian.  Hence \(L_P/k_P\) is abelian even when \(L/k\) is not
globally abelian.

Put
\[
 a_P^{\rm loc}=d_2\bigl(I(E_Q/k_P)\bigr).
\]
For a finite abelian \(2\)-group \(D\), \(r_2(D)=d_2(D)(d_2(D)+1)/2\).
Since \(D_P:=\operatorname{Gal}(L_P/k_P)\) has cyclic unramified quotient,
\(d_2(D_P)\leq d_2(I(D_P))+1\).  Therefore
\[
 r_2(D_P)-d_2(D_P)
 \leq \frac{a_P^{\rm loc}(a_P^{\rm loc}+1)}2. \tag{27}
\]
This is the local estimate needed in Theorem 4.1.  It uses the finite-stage
facts just proved, rather than assuming that the whole tower is abelian.

The local rank bound for an abelian elementary \(E/k\) of depth at most
\(\nu_P\) is the DM/Kuhnt bound
\[
 a_P^{\rm loc}\leq A_P^{\rm el}
 :=f_P\left(\nu_P-1-\left\lfloor\frac{\nu_P-1}{2}\right\rfloor\right)
 =f_P\left\lfloor\frac{\nu_P}{2}\right\rfloor. \tag{28}
\]
Consequently the published GS relation term can be replaced, after this
finite-stage argument is inserted in the proof, by
\[
 C_{\rm el}=\sum_{P\in S}A_P^{\rm el}(A_P^{\rm el}+1),\qquad
 R\leq C_{\rm el}/2+t-1. \tag{29}
\]
For \(\nu_P=2\), \(A_P^{\rm el}=f_P\), so there is no numerical change from
the M2 local term.  For depth four or higher, (29) is strictly smaller than
the conservative \(C\), whose local parameter is \(B_P=f_P(\nu_P-1)\).

This refinement applies when \(E\) is actually used as the finite base of the
unramified tower.  It does not follow merely by averaging order-two
characters of a full ray group while retaining the full ray field as base.
For the proposed choice of \(E\) as the subfield with
\[
\operatorname{Gal}(E/k)\simeq
G_{\mathfrak m,T}^{(2)}/2G_{\mathfrak m,T}^{(2)},
\]
\(E/k\) is abelian elementary, \(T\) remains split, and the DM generator
bound still gives \(d_2(E/k)\geq75\).  The exact rank may be larger, but is
unknown.

The local relation replacement itself does not require \(E/k\) to be
elementary.  If \(E/k\) is the full abelian \(2\)-primary ray extension, then
its local inertia is an abelian quotient of \(U_P^{(1)}/U_P^{(\nu_P)}\), whose
minimal generator number is at most \(A_P^{\rm el}\).  A subgroup of a finite
abelian \(2\)-group has no larger minimal generator number, so the same
argument gives (28)--(29) for the full abelian ray base.  Elementary \(E\) is
needed for the simpler order-two/all-even conductor average, not for this
rank-based local relation bound.

The final root proof has supplied these finite-stage and generator/removal
checks, and the mathematical review in `results/M3_ASTRA_REVIEW.md` accepted
the resulting criterion.  An independent execution/test of that proof is
complete with PASS (results/M3_INDEPENDENT_VALIDATION.md).  The published Proposition 5.1 does not state (27)--(29) in
this specialized form, so the derivation must remain explicit in the final
proof rather than being cited as a verbatim result.

With frozen depth-two numbers, \(d\geq75\) and
\(R\leq2260/2+192-1=1321\), while finite
Golod--Shafarevich stabilization would require
\(R>75^2/4-75=1331.25\).  An exact conductor mean changes (19), not this
comparison.  The proved version of (28) changes the relation estimate at depths
greater than two; the refined obstruction still excludes a score improvement.

## 7. Finite path and exact unknowns

The smallest finite computation deciding whether M2's mean is strictly
conservative is:

1. Compute the principal-divisor lattice supported on \(T\), equivalently a
   complete basis of \(\mathcal E_T\), by exact Riemann--Roch/principality
   tests.
2. Evaluate that basis in every local block of \(U_{\mathfrak m}\).
3. For each \(P\), compute the block-supported intersection in (12).
4. Substitute the resulting \(\rho_P\) in (16).  One nonzero block intersection
   gives a strict mean-conductor improvement.
5. At higher depth compute successive congruence-layer image orders and use
   (21).
6. If switching to the subfield \(E\) with
   \(\operatorname{Gal}(E/k)\simeq G_{\rm el}\), certify the local hypotheses
   in (27)--(29) before changing the GS relation term.

The exact unknowns are the complete \(T\)-unit principal-divisor lattice, its
local residue image, every \(\rho_P\), higher-layer images for nonuniform
depth, the class image \(J_A\) if the ray degree is wanted, and any strengthened
finite-stage relation estimate.  None follows from
\(v_2(|\operatorname{Jac}(k)(\mathbf F _2)|)=51\).

Equations (16), (21), and the conditional local lemma (28) define the finite
proof obligations.  Equations (17), (22), and the published GS numbers remain
the currently certified inputs.  No strict new Ihara bound is claimed by this
note alone.
