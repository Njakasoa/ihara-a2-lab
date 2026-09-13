# All intermediate covers between H and k343

This file documents the exact database in
curves/intermediate-covers.json and its generator
src/intermediate_covers.py.  The database enumerates every nonzero
F_2-linear subspace V of

    W = <1,x,x^2,y,y^2>_F2,

where

    H = F_2(x,y),       y^2+(x^3+x+1)y=x^2+x.

For a subspace V, k_V/H is the compositum of the Artin–Schreier quadratic
extensions indexed by the nonzero h in V.  The rank of V is r, so
[k_V:H]=2^r.  This is a finite cover inventory; it does not search for a
class-field tower or claim a new Ihara bound.

## Certified input and character decomposition

The local residue calculation in
[FINITE_GEOMETRY.md](FINITE_GEOMETRY.md) proves that all 31 nonzero
characters h in W have conductor 2P_5+2P'_5 and that the full span gives
Gal(k/H)=(Z/2Z)^5.  The quotient zeta certificate
certificates/k343-zeta.json contains the exact genus-13 numerator
P_{C_h}(T) for every nonzero h and the genus-2 numerator

    P_H(T)=1+3T+5T^2+6T^3+4T^4.

For any V, character factorization gives

    Z_{k_V}(T)
      = Z_H(T) product_{0 != h in V} (Z_{C_h}(T)/Z_H(T)).

Writing N_n(F) for the number of F_{2^n}-points, the database uses the
equivalent exact integer formula

    N_n(k_V)
      = sum_{0 != h in V} N_n(C_h)
          - (2^r-2) N_n(H).                         (1)

The quotient zeta coefficients determine N_n through degree 30 by the Newton
power-sum recurrence.  The first fourteen counts in each quotient certificate
are retained as a direct-count check; degrees 15–30 are exact recurrence
values from the certified full numerator.  Exact-degree places are then
recovered by

    n a_n = N_n - sum_{d|n, d<n} d a_d.              (2)

Every residual is checked to be a nonnegative multiple of n before being
stored.

## Canonical subspace enumeration

The generator enumerates the unique reduced-row-echelon binary matrix for
each subspace.  For a fixed pivot set, entries in non-pivot columns to the
right of a row pivot are free; entries to the left and entries in pivot
columns are forced by RREF.  The basis masks use bit positions

    bit 0,1,2,3,4 = 1,x,x^2,y,y^2.

The full span is the sorted XOR closure including zero.  The resulting
Gaussian-binomial counts are:

| rank r | number of subspaces |
| ---: | ---: |
| 1 | 31 |
| 2 | 155 |
| 3 | 155 |
| 4 | 31 |
| 5 | 1 |

Thus the database has 373 records, with no duplicate full spans.  Each record
stores basis_masks, fullspan_masks, extension degree, genus, rational
places, point counts through degree 30, exact-degree place counts through
degree 30, and the trace-derived split-place inventory through degree 12.

## Uniform geometry of the records

Every nonzero h has the same conductor degree 20.  Therefore Riemann–Hurwitz
for a rank-r cover gives

    2g(k_V)-2
      = 2^r (2g(H)-2) + (2^r-1)20
      = 22*2^r-20,

and hence

    g(k_V)=11*2^r-9.                                (3)

All six rational places of H split in every Artin–Schreier quotient, so

    N_1(k_V)=6*2^r.                                 (4)

The stored rank table is consequently:

| rank | degree over H | genus | rational places |
| ---: | ---: | ---: | ---: |
| 1 | 2 | 13 | 12 |
| 2 | 4 | 35 | 24 |
| 3 | 8 | 79 | 48 |
| 4 | 16 | 167 | 96 |
| 5 | 32 | 343 | 192 |

The rank-five record agrees with the existing k343 point-count certificate
through degree 30 and its place inventory agrees after inversion.  Rank one
records agree individually with the 31 certified quotient zetas.

## Trace-based splitting result

At an unramified H place Q, let τ(Q) be the five-bit trace vector of the
five Artin–Schreier radicands.  An H place splits completely in k_V exactly
when

    <h,τ(Q)>_F2=0 for every h in V.                 (5)

The trace inventory is calculated directly from normalized H points and
Frobenius orbits.  The unique degree-three place has

    τ_3 = 18,

and the unique degree-four place has

    τ_4 = 24.

The rank-four subspace that splits the degree-three place has canonical basis
[1,18,4,8], while the rank-four subspace that splits the degree-four place
has canonical basis [1,2,4,24].  They are distinct.  A rank-four subspace is
a hyperplane, whose annihilator is one-dimensional; it cannot be contained in
both distinct kernels.  The database therefore records

    rank-four covers splitting degree 3: 1,
    rank-four covers splitting degree 4: 1,
    rank-four covers splitting both: 0.

This is a structural trace statement only.  It does not select a candidate
for the later theorem search.  The full trace mask multiplicities through
degree 12 are stored at the top level of the JSON database, while each record
stores the number of splitting H places by degree.

## Reproduction and scope

From the repository root, regenerate the artifact with

    python3 src/intermediate_covers.py --nmax 30 --trace-max-degree 12

The tests in tests/test_intermediate_covers.py check the
Gaussian-binomial counts, XOR closure, rank-one and rank-five zeta identities,
Riemann–Hurwitz, exact place inversion, and the rank-four trace obstruction.
The input zetas come from the finite certificate and character decomposition
documented in [ZETA_DECOMPOSITION.md](ZETA_DECOMPOSITION.md).  No class-group
structure, full ray-group order, future theorem search, or manually chosen
“best” subspace is used.
