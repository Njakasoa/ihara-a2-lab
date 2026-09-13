# Duursma–Mak reconstruction

This is a theorem-by-theorem audit of Iwan Duursma and Kit-Ho Mak, *On lower
bounds for the Ihara constants A(2) and A(3)*.  The version used here is
arXiv:1102.4127v4 (14 October 2012), 22 pages.  The primary sources are the
[arXiv record](https://arxiv.org/abs/1102.4127), the
[v4 PDF](https://arxiv.org/pdf/1102.4127v4), the
[HTML transcription](https://arxiv.org/html/1102.4127), and the published
[Compositio Mathematica article](https://doi.org/10.1112/S0010437X12000796).
Printed page numbers below refer to the article pages.

The labels in this document have a precise meaning:

* **Published input** means a theorem, formula, or construction stated in
  Duursma–Mak.  Its use here is a transcription of the cited source.
* **Finite certificate** means a finite-field calculation exactly
  recomputed in this repository.  The genus-343 calculations are collected in
  [dm-finite-certificate.md](../references/dm-finite-certificate.md) and the
  machine-readable residue data in certificates/dm-finite-geometry.json.
* **Open audit item** means that this reconstruction does not claim a complete
  computation.  In particular, no exact degree or structure of the later ray
  class group is inferred from a p-rank lower bound.

## 1. The source convention and the p-primary field

Let k be a function field of genus g with exact constant field
F_q, q=p^e.  Let S be a finite set of places, let f_P be the degree of
P in k, and let ν_P be a positive integer.  The modulus is

    m = sum_{P in S} ν_P P.

Let T be a set of t>0 rational places disjoint from S.  The source writes
K=k_m^T for the maximal subfield of the ray class field of conductor m in
which T splits completely.

There is a convention that must be made explicit when applying the proof.
A literal full ray class field can have prime-to-p tame factors of order
q^{f_P}-1 and a prime-to-p class-group factor.  The Golod–Shafarevich and
Kuhnt arguments in Theorem 4.1 are arguments for a finite Galois p-extension.
Accordingly, throughout this audit K means the maximal abelian
p-subextension of the T-ray field, equivalently the p-primary ray field under
the convention commonly used in the class-field-tower argument.  Complete
splitting of T is inherited by this subfield, and the p-rank and conductor
upper bounds used below remain valid.  The exact value of [K:k] is not
deduced from the rank estimate; the full ray group has not been computed.

There is also a local source typo in the main binary construction.  On p. 18
the paper says that k is the compositum of extensions E(v) immediately after
introducing H and then uses functions in H.  The equations define H(v), not
E(v).  This is recorded in dm-finite-certificate.md; the literal symbol is
not used as a mathematical input.

## 2. Theorem 1.1 and the engine inequalities

For one P in S define

    A_P = e f_P (ν_P - 1 - floor((ν_P - 1)/p)),
    B_P = e f_P (ν_P - 1).

Theorem 1.1 (pp. 1–2) first requires

    t <= sum_{P in S} A_P.

Its displayed admissibility condition is

    (1 + sum A_P - t)^2
      - 2 sum B_P(B_P+1)
      - 4 sum A_P >= 0.                         (DM 1.1)

When these conditions hold, the (T,p)-class-field tower over K is infinite and

    A(q) >=
      t / ( g - 1 + (1/(2[K:k])) sum_chi deg(f_chi) ),                 (2.1)

where the sum runs over the characters of Gal(K/k), and f_chi is the
Artin conductor of chi.

Corollary 1.2 (p. 2) replaces each conductor by the modulus and gives the
coarser, always easier denominator

    A(q) >= t / ( g - 1 + (1/2) sum_{P in S} f_P ν_P ).                (2.2)

For a search engine, rows (f,n,ν) representing n distinct degree-f places
give

    A_S = sum n e f (ν - 1 - floor((ν-1)/p)),
    C_S = sum n [e f (ν - 1)] [e f (ν - 1)+1],
    D   = 1 + A_S - t,
    I   = D^2 - 2 C_S - 4 A_S.

The theorem-safe acceptance test is t>0, t<=A_S, I>=0, together with the
geometric conditions on the places, T, constants, and conductor depths.  It
is sufficient, not necessary.

## 3. Where the inequalities come from

### Golod–Shafarevich (Theorem 2.1, p. 3)

For a finite nontrivial p-group G, write d=d_p(G) for its generator rank and
r=r_p(G) for its relation rank.  Theorem 2.1 states

    r > d^2/4.

Thus it is enough to force a lower bound on d and an upper bound on r-d that
are incompatible with this strict inequality.

### Bounded-depth p-extensions (Section 3, pp. 3–5)

Duursma–Mak define G_{S,ν} as the Galois group of the maximal p-extension
unramified outside S whose upper-numbering ramification depth at P is at most
ν_P.  Their Proposition 3.1 identifies the corresponding iterated abelian
construction with this maximal extension.

With U_P^(r) the r-th higher unit group and Δ_{S,ν} the global principal-unit
term, Proposition 3.2 gives

    d_{S,ν}
      = 1 + d_p(Δ_{S,ν})
          + sum_{P in S} d_p(U_P^(1)/U_P^(ν_P)).

Proposition 3.3 evaluates the local term:

    d_p(U_P^(1)/U_P^(ν_P))
      = e f_P (ν_P - 1 - floor((ν_P-1)/p)).

Theorem 3.2 is their combination, namely

    d_{S,ν}
      = 1 + d_p(Δ_{S,ν})
          + sum_{P in S} A_P.                         (3.1)

For the T-ray class field, Proposition 5.3 (p. 15) subtracts t-1 for the
splitting conditions at T and gives

    d_p(Gal(K/k)) >= 1 + sum A_P - t = D.              (3.2)

The right side is a lower bound; it is not an assertion that the ray group
has exactly p^D elements.

### Relation rank and removal of excess ramification (Theorem 4.1,
pp. 5 and 10–14)

For a tower L/K/k of Galois p-extensions with L/K unramified, T_L a finite
nonempty set of places in L, and T_k its image in k, Theorem 4.1 defines

    δ = r_p(G)-d_p(G)
        - sum_{P in S}(r_p(G_P)-d_p(G_P))
        - (|T_k|-1)
        + d_p(Δ_S),

where G=Gal(L/k) and G_P is a local decomposition group.  If δ>0, the
embedding-problem construction supplies another unramified p-extension in
which T_L splits.  At a finite maximal tower the resulting inequality is

    r_p(G)-d_p(G)
      <= sum_{P in S}(r_p(G_P)-d_p(G_P))
           + (|T_k|-1) - d_p(Δ_S).                    (4.1)

Dropping the final nonpositive term is the only relaxation used in the
displayed search condition.

The proof has three substantive stages.  Proposition 4.2 solves each
non-split central embedding problem with kernel Z/pZ.  Proposition 4.3 shows
that linearly independent cohomology classes give independent solutions.
The proof of Theorem 4.1 then (i) solves the unramified local embedding
problems, (ii) removes any new ramification deeper than ν using the
bounded-depth generator calculation, and (iii) removes the remaining local
ramification while preserving enough p-rank.  The final Frobenius fixed field
costs at most |T_k| generators, producing (4.1).

### The local relation estimate (Proposition 5.1, pp. 14–15)

For an abelian p-extension of local depth at most ν_P, Proposition 5.1 uses
the exact inertia sequence and the standard bound on an inertia p-group to
obtain

    r_p(G_P)-d_p(G_P)
      <= binom(e f_P(ν_P-1)+1, 2)
       = B_P(B_P+1)/2.                               (5.1)

Inserting (5.1) into (4.1), and using |T_k|=t in the base-level
application, gives

    r_p(G)-d_p(G) <= C_S/2 + t - 1 = R.                (5.2)

If the tower were finite, (3.2), (5.2), and Theorem 2.1 would require

    R > D^2/4 - D.

The negation of this strict inequality is exactly I>=0:

    D^2 - 2 C_S - 4 A_S >= 0.

This explains every term in the engine contract and why C_S is a sum of
placewise B_P(B_P+1), rather than the square of a total.

## 4. Conductors and the asymptotic denominator

Proposition 5.2 (p. 15) is the conductor–discriminant formula.  For a
geometric abelian extension K/F,

    2g(K)-2 = [K:F](2g(F)-2) + sum_chi deg(f_chi).      (5.3)

Consequently

    g(K)-1 = [K:k](
      g-1 + (1/(2[K:k])) sum_chi deg(f_chi)).          (5.4)

If the subsequent split (T,p)-tower is infinite, all |T_K|=[K:k]t
places above T split forever.  Dividing their count by (5.4) gives (2.1).
This is the only point at which the average character conductor enters the
Ihara bound.

### Certified binary filtration average

For p=2, put Q=q^f=2^{ef} at a degree-f place and let the depth bound be
ν>=2.  In the p-primary local quotient, the subgroup of characters trivial
on U^(r), for 1<=r<=ν-1, has index

    |U^(r)/U^(ν)| = Q^(ν-r).

Intersecting it with the image of the global character group cannot increase
the index.  Hence

    Pr(a_P <= r) >= Q^{-(ν-r)}.

There are no conductor-one p-primary characters because the tame residue-unit
quotient has order Q-1, prime to p.  The bounds for a_P<=0 and a_P<=1
therefore coincide.  Summing cumulative probabilities gives the safe upper
bound

    E(a_P) <= ν - 2 Q^{-(ν-1)}
                    - sum_{j=1}^{ν-2} Q^{-j}.         (5.5)

For ν=2 this is 2(1-Q^{-1}).  Thus for the binary examples in this paper

    F_avg = 2 sum n f (1-q^{-f})

is an upper bound for the average conductor degree, and the denominator is
g-1+F_avg/2.  Formula (5.5) is also suitable for later binary searches with
ν>2, place by place, without knowing the full ray group.

### Why the same line is not certified for the ternary refinement

For p=3 and ν=3, the local p-primary quotient U^(1)/U^(3) has order
3^(2ef), with two residue-field layers.  Writing Q=3^(ef), the full local
quotient has one character of exponent 0, Q-1 characters of exponent 2, and
Q^2-Q characters of exponent 3.  Its uniform average exponent is therefore

    [2(Q-1) + 3(Q^2-Q)]/Q^2
      = 3 - Q^{-1} - 2 Q^{-2}.                         (5.6)

The paper's ternary refinement uses 3(1-3^{-f}), which is a one-layer
arithmetic expression and is not certified here by (5.5).  The fraction
below is retained as an exact transcription of the paper's displayed
calculation, with the refinement explicitly marked published-only.  The
coarse ternary Corollary 1.2 score is unaffected.

## 5. The first binary construction (Proposition 5.4, pp. 17–18)

The paper starts with the maximal elliptic curve

    E/F_2 : y^2+y = x^3+x,

with genus 1 and

    (a_d(E))_{d>=1} = (5,0,0,5,4,10,20,25,...).

It chooses degree-four and degree-five places P_4 and P_5 and takes the
elementary abelian degree-32 subfield k/E of the T-ray field with modulus
2P_4+2P_5 in which the five rational places split.  The source states that
there is one quadratic subextension with conductor 2P_5 and that the other
30 nontrivial quadratic characters have conductor 2P_4+2P_5.  Therefore

    2g(k)-2 = 32(2g(E)-2) + 10 + 30(18) = 550,
    g(k)=276,
    a_1(k)=32*5=160.

The source lists

    (a_d(k))_{d=1}^{10}=(160,0,0,0,1,0,0,65,0,48,...).

It takes S to be one degree-five place, 27 degree-eight places, and one
degree-ten place, all with ν=2, and T to be all 160 rational places.  The
integer audit is

    A_S=5+27*8+10=231,
    C_S=5*6+27*(8*9)+10*11=2084,
    D=72,
    I=72^2-2(2084)-4(231)=92.

The coarse Corollary 1.2 value is 80/253.  Applying the certified binary
ν=2 filtration average gives

    F_avg = 2[5(1-2^-5)+216(1-2^-8)+10(1-2^-10)]
          = 117755/256,

    A(2) >= 160/(275+117755/512)
         = 16384/51711
         = 0.31683781013710816....

The construction and place list are published inputs; the integer arithmetic
and the binary averaging inequality are independently checkable from the
formulas above.  The exact later ray-group degree is not asserted.

## 6. The main binary construction (Proposition 5.5 and Theorem 1.3,
pp. 18–19)

### Base curve and the degree-32 cover

Set

    a=x^3+x+1,   b=x^2+x,   c=x^5+x^2+1,
    H=F_2(x,y),  y^2+a y=b.

The cubic a is irreducible.  In the quadratic presentation, its degree-three
place has a reduced odd Artin–Schreier pole, so the different has exponent 2
at that place and nowhere else.  Riemann–Hurwitz gives

    2g(H)-2 = -4 + 2*3 = 2,
    g(H)=2.

The model has six rational places.  An exact trace enumeration (independent Sage PASS: results/INDEPENDENT_VALIDATION.md) gives

    (a_d(H))_{d=1}^{10}=(6,0,1,1,6,13,12,33,56,105),

and the first four counts give

    P_H(T)=1+3T+5T^2+6T^3+4T^4.

The polynomial c is irreducible of degree five.  Over F_32, with
alpha^5=alpha^2+1, the two points above x=alpha have

    y=17=alpha^4+1,
    y=26=alpha^4+alpha^3+alpha.

Their Frobenius orbits are the two degree-five places P_5 and P'_5 of H.

Let V=<1,x,x^2,y,y^2> over F_2.  For h in V, the paper writes

    v_h^2 + c v_h = b h.

After w_h=v_h/c this is the Artin–Schreier equation

    w_h^2+w_h = b h/c^2.                              (6.1)

At a root alpha of c, use t=x-alpha.  Since c'=x^4 and squares have no
odd-degree term in characteristic two, reduction of the double pole leaves

    rho(h) = (b h)'(alpha,y)/c'(alpha)^2
             + sqrt( b(alpha)h(alpha,y)/c'(alpha)^2 ).  (6.2)

Differentiation in H uses

    y'=(1+(x^2+1)y)/(x^3+x+1),
    (1,x,x^2,y,y^2)'=(0,1,0,y',0).

The exactly recomputed residue vectors (independent Sage PASS: results/INDEPENDENT_VALIDATION.md) for the ordered basis
(1,x,x^2,y,y^2) are

    y=17: (23,19,12,30,15),
    y=26: (23,19,12,5,3),

in the polynomial basis of F_32.  Each resulting 5-by-5 F_2 matrix has
determinant one.  Hence both local maps V -> F_32 have rank five.  This
certifies that every nonzero h has a reduced simple pole at both P_5 and
P'_5.  Therefore all 31 nontrivial characters of k/H have conductor
2P_5+2P'_5, and

    Gal(k/H)=(Z/2Z)^5,
    [k:H]=32,
    2g(k)-2=32(2g(H)-2)+31*20=684,
    g(k)=343.

At x=0,1 one has b=0 and c=1, so the four affine rational places split.
At both infinity places the functions b h/c^2 are regular and vanish; those
two places split as well.  Thus

    a_1(k)=6*32=192.

The exact trace/place calculation gives

    (a_d(k))_{d=1}^{10}=(192,0,0,0,2,16,0,16,0,64),

with the degree-five row consisting of two ramified places, and with the
unramified degree-three, degree-four, and degree-five rows producing the
degree-six, degree-eight, and degree-ten places used below.  These finite
counts and the local rank calculation are the **finite certificate** part of
the reconstruction; they do not compute the later ray class group.

### The S/T choice and the exact binary bound

Take T to be the 192 rational places of k.  Take S to consist of

    2 places of degree 5,
    16 places of degree 6,
    15 places of degree 8,
    4 places of degree 10,

and set ν_P=2 at every P in S.  The modulus is m=sum_{P in S}2P.
The place degrees are disjoint from T, and the exact count supplies
the required multiplicities.  The parameter sums are

    A_S=2*5+16*6+15*8+4*10=266,
    C_S=2(5*6)+16(6*7)+15(8*9)+4(10*11)=2252,
    D=1+266-192=75,
    I=75^2-2(2252)-4(266)=57.

The relation estimate is R=2252/2+191=1317, while
D^2/4-D=1331.25.  Thus the finite-tower assumption contradicts
Golod–Shafarevich, exactly as required by Theorem 1.1.

The coarse denominator is

    g-1 + (1/2)(2*266)=342+266=608,
    A(2)>=192/608=6/19.

For ν=2 and q=2, the certified local filtration bound gives

    F_avg = 2[10(1-2^-5)+96(1-2^-6)
              +120(1-2^-8)+40(1-2^-10)]
          = 33751/64.

Consequently

    g-1+F_avg/2
       =342+33751/128
       =77527/128,

and the exact rational behind the paper's displayed 0.316999... is

    A(2) >= 192/(77527/128)
         = 24576/77527
         = 0.31699923897480875....

The paper prints the decimal, not this reduced rational.  The fraction is the
exact evaluation of its displayed conductor upper bound.  The construction's
finite geometry is exactly reconstructed (independent Sage PASS: results/INDEPENDENT_VALIDATION.md); the tower and class-field
statements are the published theorem application, with K understood
p-primarily as in Section 1.

## 7. The ternary construction (Proposition 5.6 and Theorem 1.4,
pp. 19–20)

The paper starts with

    E/F_3 : y^2=x^3-x+1,

which has genus one and

    (a_i(E))_{i>=1}=(7,0,7,21,42,...).

For one degree-five place P_5, the modulus is 3P_5 and all seven rational
places split.  Proposition 5.3 gives

    d_3 >= 1 + 2*5 - 7 = 4.

The source chooses an elementary abelian subfield k/E of degree 3^4=81.
It has a_1(k)=81*7=567, and Proposition 5.2 gives

    2g(k)-2=80*3*5=1200,
    g(k)=601.

The displayed model is the compositum of

    v^3-(xy+x^2-1)^2 v=(x^3-x)h,

for h in <1,x,y,xy> over F_3.  The source lists

    (a_d(k))_{d=1}^{9}=(567,0,0,0,1,0,0,162,1809).

For the coarse bound, S consists of 46 degree-eight places with ν=3, and
T consists of the 567 rational places.  The exact GS arithmetic is

    A_S=46*(8*2)=736,
    C_S=46*(16*17)=12512,
    D=1+736-567=170,
    I=170^2-2(12512)-4(736)=932.

Corollary 1.2 gives

    g-1 + (1/2)(3*46*8)=600+552=1152,
    A(3)>=567/1152=63/128=0.4921875.

The source then uses S with one degree-five, 43 degree-eight, and two
degree-nine places, all ν=3.  The parameter arithmetic is

    A_S=2(5+43*8+2*9)=734,
    C_S=10*11+43(16*17)+2(18*19)=12490,
    D=168,
    I=168^2-2(12490)-4(734)=308.

Its displayed refinement is

    F_avg = 3[5(1-3^-5)+43*8(1-3^-8)+2*9(1-3^-9)]
          = 2407402/2187,

    600+F_avg/2=2515901/2187,
    567/(2515901/2187)
      =1240029/2515901
      =0.49287670699284275....

This last fraction is a **published arithmetic transcription**, not a
certified refined lower bound in this repository.  For p=3 and ν=3 the full
local quotient has two wild layers, as shown in (5.6); the one-layer
expression used in the paper needs a separate conductor-filtration and global
restriction audit.  The coarse 63/128 value uses Corollary 1.2 and is the
ternary theorem-safe score currently recorded here.

## 8. Historical Schoof baseline

Schoof's *Algebraic curves over F_2 with many rational points*, J. Number
Theory 41 (1992), 6–14, gives the historical control bound

    A(2) >= 4/(19-1)=2/9.

The primary author PDF is
[CurvesF2.pdf](https://reneschoof.github.io/CurvesF2.pdf), with DOI
[10.1016/0022-314X(92)90079-5](https://doi.org/10.1016/0022-314X(92)90079-5).
The genus-19 construction has four rational places split in an infinite
2-class-field tower.  The normalized finite-field reconstruction and the
source's printed-equation inconsistency are documented in
[SCHOOF_RECONSTRUCTION.md](SCHOOF_RECONSTRUCTION.md): its p. 13 scan prints
Y^2+Y=T^3+1 while simultaneously claiming five rational points, whereas the
compatible maximal model is y^2+y=x^3+x.  This is recorded as a source
inconsistency, not as a new result.

## 9. Remaining audit boundaries

The following statements are deliberately kept separate:

1. The genus-343 equation, two degree-five places, local residue ranks,
   conductor-20 characters of k/H, rational splitting, and low-degree place
   counts are finite calculations audited in
   [dm-finite-certificate.md](../references/dm-finite-certificate.md).
2. The GS inequality, bounded-depth generator formula, Kuhnt relation estimate,
   conductor–discriminant formula, and class-field-tower implication are
   published theorem inputs from pp. 3–17.
3. The p-primary ray field K/k used in the proof is not assigned an exact
   degree.  The finite cover k/H and its 31 quadratic characters do not
   determine that later ray group.
4. The binary ν=2 conductor average is certified by the local filtration
   argument.  The ternary refined average is retained only as published
   arithmetic; use the coarse 63/128 score until its filtration is audited.

No claim of a new Ihara bound or of a computed class-group structure is made by
this reconstruction.

### Explicit GS monotonicity check added after Astra review

For accepted parameters, A_S≥t≥1, D=1+A_S−t≥1 and
I=D²−2C_S−4A_S≥0. Hence D²≥4 and D≥2. Since x²/4−x increases on
[2,∞), replacing d by the certified lower bound D in this expression is
valid. In the main example D=75, so the condition holds with a wide margin.
