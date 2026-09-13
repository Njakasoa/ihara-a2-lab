# Duursma–Mak parameter map and engine contract

This file translates Theorem 1.1 of Duursma–Mak into integer operations that a
search or validation engine can evaluate without floating point.  The source is
arXiv:1102.4127v4, pp. 1–2 and 15–17; the worked candidates are on pp. 18–19.

## Inputs

Use a prime characteristic `p`, `q=p^e`, a base function field of genus `g`, a
positive integer `t`, and a finite multiset of allowed ramified places.  A
multiset row `(f,n,nu)` means `n` distinct places of degree `f`, each with
conductor-depth bound `nu`; it contributes `n` copies of the placewise terms
below.  The set `T` has `t` rational places and must be disjoint from `S`.

The theorem’s `K=k_m^T` must be read p-primary in the proof: take the maximal
abelian p-subextension of the full T-ray class field with modulus
`m=sum nu_P P`.  The full ray field can have prime-to-p tame factors of order
`q^f-1` and a prime-to-p class-group factor, so it need not be a p-extension.
Theorem 4.1 and the Golod–Shafarevich argument require `K/k` to be a finite
Galois p-extension.  Passing to the maximal p-subextension preserves the
complete splitting of `T`, the p-rank lower bound, and the conductor upper
bound used by Theorem 1.1.  Do not infer an exact degree for this p-ray field
from the theorem’s rank bound.

## Integer formulas

For one place of degree `f` define

\[
A(f,nu)=ef\left(nu-1-\left\lfloor\frac{nu-1}{p}\right\rfloor\right),
\qquad B(f,nu)=ef(nu-1).
\]

For rows `(f,n,nu)`, set

\[
A_S=\sum nA(f,nu),\qquad
C_S=\sum nB(f,nu)(B(f,nu)+1).
\]

Theorem 3.2 and Proposition 5.3 give the generator-rank lower bound

\[
D=1+A_S-t,\qquad d_p(G)\ge D.
\]

Theorem 4.1 and Proposition 5.1 give, under the finite-tower assumption,

\[
r_p(G)-d_p(G)\le R=\frac{C_S}{2}+t-1.
\]

The admissibility integer is

\[
I=D^2-2C_S-4A_S.
\]

The exact acceptance conditions are

\[
t\in\mathbf Z,\quad t>0,\quad t\le A_S,\quad I\ge0,
\]

plus the geometric conditions (distinct places, `T cap S=emptyset`, complete
constant field `F_q`, and the stated conductor-depth bounds).  If `I>=0`, then

\[
R\le D^2/4-D,
\]

so a nontrivial finite p-group would violate
`r_p(G)>d_p(G)^2/4` from Theorem 2.1.  The acceptance test is sufficient; a
failed test says nothing about finiteness of the tower.

For a search over multiplicities, the rows are the only combinatorial input to
`I`.  In particular, do not replace `C_S` by `(sum B)^2` and do not omit the
place multiplicities.

## Conductor-average score

Theorem 1.1 gives

\[
A(q)\ge
\frac{t}{g-1+\frac1{2[K:k]}\sum_{chi}\deg f_chi}.
\]

The refined averaging formula is certified here only for the binary
p-primary filtration.  Put `Q=q^f=2^{ef}` at a degree-`f` place and suppose
the local depth bound is `nu>=2`.  For `1<=r<=nu-1`, the subgroup of local
characters trivial on `U^(r)` has index at most
`|U^(r)/U^(nu)|=Q^(nu-r)`.  Intersecting this subgroup with the image of the
global character group therefore gives

\[
 \Pr(a_P\le r)\ge Q^{-(\nu-r)}.
\]

Here `a_P` is the local Artin-conductor exponent.  In the p-primary part there
are no conductor-one characters (the tame residue-unit quotient has order
coprime to `p`), so the bounds for `a_P<=0` and `a_P<=1` coincide.  Summing
the cumulative probabilities gives the safe binary upper bound

\[
 \mathbb E(a_P)\le
 \nu-2Q^{-(\nu-1)}-\sum_{j=1}^{\nu-2}Q^{-j}.
\]

For `nu=2` this is `2(1-Q^(-1))`, hence the formula used by the main binary
example is

\[
F_{avg}=2\sum n f(1-q^{-f}),
\qquad
A(q)\ge \frac{t}{g-1+F_{avg}/2}.
\]

This is an upper bound for the average conductor, not a claim that the exact
ray-class-group character distribution has been enumerated.  For binary
depths larger than two, an engine may use the preceding filtration formula
place by place.  If exact local conductor frequencies are computed, they may
replace this upper bound by a smaller exact average.

The same one-layer argument must not be transferred to the ternary
`nu=3` example.  There `U^(1)/U^(3)` has order `3^(2ef)`, not `3^(ef)`.  For
the full local quotient, with `Q=3^(ef)`, the uniform average exponent is

\[
 3-Q^{-1}-2Q^{-2},
\]

where the characters trivial on `U^(1)`, nontrivial only on
`U^(1)/U^(2)`, and genuinely depth three have exponents `0`, `2`, and `3`.
The paper's ternary displayed average `3(1-3^{-f})` is retained below as a
published arithmetic transcription; it is not independently certified by the
binary argument and is out of scope for the engine's certified score.

## Published candidates, recomputed exactly

### Main binary candidate (Theorem 1.3 / Proposition 5.5)

\[
(p,e,g,t)=(2,1,343,192),
\]

with rows

\[
(f,n,nu)=(5,2,2),(6,16,2),(8,15,2),(10,4,2).
\]

Here

\[
A_S=2(5)+16(6)+15(8)+4(10)=266,
\]

\[
C_S=2(5\cdot6)+16(6\cdot7)+15(8\cdot9)+4(10\cdot11)=2252,
\]

and

\[
D=1+266-192=75,\qquad I=75^2-2(2252)-4(266)=57.
\]

The relation-rank upper bound is `R=2252/2+191=1317`, while
`D^2/4-D=1331.25`, so the finite case is excluded.

The coarse Corollary 1.2 denominator is

\[
342+\frac12(2\cdot266)=608,
\qquad 192/608=6/19.
\]

The refined score is

\[
F_{avg}=2\left(10(1-2^{-5})+96(1-2^{-6})
 +120(1-2^{-8})+40(1-2^{-10})\right)
 =\frac{33751}{64}.
\]

Thus

\[
g-1+F_{avg}/2=342+\frac{33751}{128}
 =\frac{77527}{128},
\qquad
\frac{192}{77527/128}=\frac{24576}{77527}
 =0.31699923897480875\ldots.
\]

The paper displays only `0.316999...`; the fraction above is the exact rational
value obtained from its displayed local upper bound.

### First binary candidate (Proposition 5.4)

\[
(p,e,g,t)=(2,1,276,160),
\]

with rows `(5,1,2),(8,27,2),(10,1,2)`.  Then

\[
A_S=231,\quad C_S=2084,\quad D=72,\quad I=72^2-2(2084)-4(231)=92.
\]

The refined score is

\[
F_{avg}=2\left(5(1-2^{-5})+216(1-2^{-8})+10(1-2^{-10})\right)
 =\frac{117755}{256},
\]

so the exact displayed bound is

\[
\frac{160}{275+117755/512}=\frac{16384}{51711}
 =0.31683781013710816\ldots,
\]

and the coarse bound is `80/253`.

### Ternary candidates: published arithmetic transcription

The following GS arithmetic and the coarse bound are direct transcriptions of
Theorem 1.4 and Proposition 5.6.  The refined conductor average at depth three
is deliberately not marked as certified; see the filtration warning above.

For the coarse candidate, use `(p,e,g,t)=(3,1,601,567)` and `(8,46,3)`.
Then `A_S=736`, `C_S=12512`, `D=170`, and

\[
I=170^2-2(12512)-4(736)=932.
\]

The coarse denominator is `600+(3*368)/2=1152`, yielding `63/128`.

For the refined candidate, use rows `(5,1,3),(8,43,3),(9,2,3)`.  Then

\[
A_S=2(5+43\cdot8+2\cdot9)=734,
\]

\[
C_S=10\cdot11+43(16\cdot17)+2(18\cdot19)=12490,
\]

\[
D=1+734-567=168,\qquad I=168^2-2(12490)-4(734)=308.
\]

The paper's refined average score and denominator are printed as

\[
F_{avg}=3\left(5(1-3^{-5})+43\cdot8(1-3^{-8})
 +2\cdot9(1-3^{-9})\right)=\frac{2407402}{2187},
\]

\[
600+F_{avg}/2=\frac{2515901}{2187},
\qquad
A(3)\ge\frac{567\cdot2187}{2515901}
 =\frac{1240029}{2515901}
 =0.49287670699284275\ldots.
\]

This last fraction is a faithful exact evaluation of the paper's displayed
expression, not an independently certified refined lower bound.  The coarse
`63/128` value is the theorem-safe ternary score currently recorded here.

## Geometry versus theorem status

The finite model `H`, the degree-32 cover `k/H`, its conductor-20 characters,
genus 343, rational splitting, and low-degree place counts are finite-field
claims and are audited in `references/dm-finite-certificate.md`.  The GS
criterion and the binary conductor-filtration inequality are published theorem
inputs plus the indicated finite-group argument.  The ternary refined average
and its local restriction calculation remain open in this reconstruction.
The exact order, structure, and complete character conductor distribution of the
later p-primary ray group `Gal(K/k)` are not inferred from the rank or from the
31 characters of `Gal(k/H)`.  A numerical score is therefore not labelled a
ray-class-group certificate unless that group is separately computed.

## Explicit monotonicity in the GS step (Astra review repair)

The accepted conditions give A_S≥t≥1 and D=1+A_S−t≥1. Since I≥0 implies
D²≥2C_S+4A_S≥4, we have D≥2. The function x²/4−x is increasing on [2,∞).
Thus d≥D implies d²/4−d≥D²/4−D, justifying the rank substitution used in
combining the relation bound with Golod–Shafarevich. A bare lower bound on d
without this domain check would not justify the monotonicity step.
