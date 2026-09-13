# Independent Sage validation — M1

Run on 2026-09-13 with SageMath 10.9:

```text
./scripts/sage-python tests/independent_sage.py
```

The command completed with `INDEPENDENT_SAGE_STATUS=PASS` in about 48 seconds.
The checker is a separate implementation and does not import `src/`.

## Completed checks

- Sage function fields give genera `1,2,2` and exact constant field `F2` for
  `E: y^2+y=x^3+x`, `H: y^2+(x^3+x+1)y=x^2+x`, and
  `y^2+y=x^5+x`. Direct Sage trace counts for `N_1,...,N_10` are,
  respectively,
  `(5,5,5,25,25,65,145,225,545,1025)`,
  `(6,6,9,10,36,87,90,274,513,1086)`, and
  `(5,9,5,17,25,81,145,193,545,1089)`.
- Sage's normalized degree-place enumeration for `H`, `d=1,...,10`, is
  `(6,0,1,1,6,13,12,33,56,105)`. The affine `H.class_group()` order is
  `1`; the complete Jacobian check is separate and gives order `19`.
- The five roots of `c=x^5+x^2+1` in `F32` give ten points on `H`, split into
  two Frobenius orbits of length five. The reduced-residue maps at all ten
  points have rank five over `F2`. Every one of the
  31 nonzero masks has nonzero reduced residue at both places, giving degree
  20 for every nontrivial character and `k/H` degree `32`. The exact
  conductor/Riemann–Hurwitz computation gives `g(k)=343`.
- Direct normalized Sage trace counts for `k`, through degree ten, are
  `(192,192,192,192,202,288,192,320,192,842)`, matching both the stored curve
  data and the counts predicted by the saved degree-686 zeta polynomial.
- For every one of the 31 quotient masks, direct Sage counts through degree
  14 match the certificate. Newton reconstruction from the first 13 counts
  reproduces every stored degree-26 coefficient, and the independent degree-14
  recurrence check passes. The real Weil polynomial was reconstructed over
  `QQ`; all 13 roots for every quotient are real algebraic numbers in the
  exact interval `AA[-sqrt(8), sqrt(8)]`. Sage `ZZ[T]` multiplication of all
  31 quotient polynomials, followed by exact division by `P_H^30`, matches
  all 687 coefficients of `P_k` and its stored Jacobian order.
- The corrected Schoof model has denominator norm degree 9. The four degree-4
  zeros have reduced residue zero, while the five degree-5 zeros have nonzero
  reduced residue; all nine zeros are simple. The exact Riemann–Hurwitz values
  recorded by the check are `g(Y)=6`, `g(X)=19`, and `4/(19-1)=2/9`.
- Exact rational arithmetic reproduces
  `A_S=266`, `C_S=2252`, `D=75`, GS margin `57`, conductor average
  `33751/64`, denominator `77527/128`, and `24576/77527`. Schoof's GS
  margin is `0`.

## Adversarial inputs

The same validator predicates reject each mutated input:

| Mutation | Result |
|---|---|
| duplicate one of the five AS basis columns in a rank-five local map | `REJECTED` |
| remove one ramified H point/residue row | `REJECTED` |
| decrement the certified genus | `REJECTED` |
| alter one k point count | `REJECTED` |
| change the accepted GS row so its criterion fails | `REJECTED` |

No failure occurred in the bounded scope. This artifact certifies finite Sage
arithmetic and the recorded exact identities. It does not compute the later
full ray class group or its structure, and it makes no independent claim of a
new Ihara bound or of tower infinitude beyond the cited theorem obligations.
