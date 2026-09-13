# A rank-based local relation bound and elementary-ray conductor score

Status: final mathematical transcription accepted by Astra in
results/M3_ASTRA_REVIEW.md; independent arithmetic PASS in
results/M3_INDEPENDENT_VALIDATION.md. Internal verification level 5.
The ingredients are standard class-field and finite abelian-group facts.
No novelty of these general ingredients is asserted.

## 1. Local relation refinement

Let E/k be a finite abelian p-extension of global function fields, and let
L/E be its maximal unramified p-extension with a nonempty rational splitting
set. Suppose, for a contradiction, that L/k is finite. At a base place P,
each completion L_w/E_v is unramified. Any such finite local extension is
the compositum of E_v with the unramified extension of k_P of degree
f(L_w/k_P), the residue degree of the full local extension. Use
uniqueness of finite unramified extensions inside a fixed separable closure.
Since both E_v/k_P and the unramified base extension are abelian, L_w/k_P is
abelian. Write D_P for its decomposition group and I_P for inertia.

Inertia injects into inertia of E_v/k_P because L_w/E_v is unramified. If
a_P bounds its generator p-rank, the cyclic residue quotient gives

    d_p(D_P) <= a_P+1.

A finite abelian p-group with d cyclic factors has a presentation with d
power relations and d(d-1)/2 commutators. Hence

    r_p(D_P)-d_p(D_P) <= d_p(D_P)(d_p(D_P)-1)/2
                            <= a_P(a_P+1)/2.

For an abelian ray extension with conductor bound nu at a degree-f place
over F_(p^e), one may take

    a_P = e*f*(nu-1-floor((nu-1)/p)),

the generator rank of the local principal-unit quotient. Quotients and
subgroups of finite abelian p-groups do not increase the number of cyclic
factors. This improves the order-based bound using e*f*(nu-1) when they differ.

Apply Duursma–Mak Theorem4.1 (Kuhnt), discarding its nonnegative correction,
to obtain

    r_p(G)-d_p(G) <= (1/2)*sum a_P(a_P+1)+t-1,
    G=Gal(L/k).

This local improvement works for the full p-primary ray field as well as for
its maximal elementary abelian subfield. It does not require an exact ray
group computation. It remains an upper estimate, not an exact presentation.

## 2. Binary elementary-ray choice

Now work over F2, with g(k)>1. Let E be the maximal elementary abelian quotient
field of the T-split ray extension. For nu_P=2*s_P, put

    a_P=f_P*s_P, A=sum a_P, C_el=sum a_P(a_P+1), D=1+A-t.

The rank of the maximal elementary quotient is the generator rank of the
full ray group, so Proposition5.3 gives d_2(G)>=d_2(Gal(E/k))>=D.
If t<=A and

    I_el = D^2-2*C_el-4*A >= 0,

then D>=2 (indeed C_el>=2A and A>=1). The function d^2/4-d is increasing
for d>=2. The local relation bound and the strict finite-group
Golod–Shafarevich inequality therefore contradict finiteness of G. The
unramified T-split tower of E is infinite.

## 3. Correct conductor average for E

The local elementary character space at depth2s has size Q^s, Q=2^f.
Characters of conductor at most2j or2j+1 form a subspace of size Q^j
(0<=j<=s, within the cutoff). In particular the full local elementary mean is

    mean_el(f,2s)=2s-2*sum_{j=1}^s Q^(-j)
                 =2s-2*(1-Q^(-s))/(Q-1).

A global character is uniform upon restriction to every inertia subgroup.
The image of each local unit filtration step in E is a quotient of its
maximal elementary local image. Tail probabilities consequently give
E[a_P] <= mean_el(f,2s). Independence across different places is unnecessary.

Conductor-discriminant and the unramified tower imply

    A(2) >= t / (g(k)-1 + sum_P [f_P*s_P-r_el(f_P,s_P)]),
    r_el(f,s)=f*(1-2^(-f*s))/(2^f-1).

For s=1 this is the M2 local bound. For s>1 it is strictly below the full
local-quotient conductor mean. This is a bound for the DIFFERENT field E,
not an asserted exact conductor mean of the original full ray field.

An odd cutoff2s+1 defines the same local elementary quotient as2s: no
order-two character has odd positive conductor. The global elementary ray
field is therefore unchanged by lowering all such cutoffs. Even depths cover
all conductor bounds>=2 for this elementary-ray choice.

## 4. Comparison and scope

For fixed rows and t, the elementary score's relation bound is no worse than
the old one, and its conductor estimate is no worse than the full ray one.
An upper obstruction for this elementary score thus also covers the old score
and the full-ray score with the rank-based relation refinement.

Additional exact inertia reductions, extra generator rank, a sharper Kuhnt
correction, and other base curves are not included in this comparison.
The general local relation proof applies at other primes and base fields;
the explicit elementary conductor formula displayed here is binary.

Sources: Duursma–Mak, arXiv:1102.4127v4, Theorem4.1 and Propositions3.3,
5.1–5.3; local computations in NONUNIFORM_CONDUCTOR_LOCAL_THEORY.md.
