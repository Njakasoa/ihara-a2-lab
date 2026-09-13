# Independent Sage validation — M2 concrete candidate

Run on 2026-09-13 with SageMath 10.9:

```text
./scripts/sage-python -u tests/independent_candidate.py
```

The command completed with `M2_CERTIFICATE=PASS` and exit status 0 in about
2 seconds.  The checker reconstructs every field from the stored modulus bits,
uses Sage finite-field arithmetic and Frobenius, and does not import `src/` or
the search implementation.

## Concrete place checks

- The main inventory has exactly 290 checked representatives, with normalized
  place counts
  `(d=1,d=5,d=6,d=8,d=10)=(192,2,16,16,64)`.  Every representative satisfies
  the displayed `H` equation and the five independent Artin–Schreier
  equations.  Every declared Frobenius orbit has exactly its declared degree,
  and all 290 orbit signatures are distinct.
- The degree-one infinity chart contains all 64 six-bit points exactly once;
  the degree-one regular chart supplies the other 128 points.  The two degree-
  five representatives are on the ramified chart, and all degree 6, 8, and 10
  representatives are on the regular chart.
- The selected splitting set is exactly
  `k343-d1-001,...,k343-d1-192`, so `|T|=192`.  It is disjoint from the
  non-rational inventory and from the selected ramification set.
- The complete stored degree-12 inventory has 208 distinct regular
  representatives and exact degree-12 Frobenius orbits.  Independently, the
  compact lifting certificate has 13 distinct degree-6 `H` orbits.  Their
  five trace bits agree with Sage computation, each vector is nonzero, and
  the recorded 16 places above each orbit give the certified lower bound
  `13*16=208`.

The certificate's selected set `S` contains 37 actual checked rows: two degree
5 rows, all 16 degree 6 rows, all 16 degree 8 rows, the first two degree 10
rows, and the first degree 12 row.  The checker compares each stored row and
ID with the inventory and checks that the modulus contains exactly those IDs,
each with exponent 2.

## Exact candidate arithmetic

For rows
`(5,2),(6,16),(8,16),(10,2),(12,1)`, independent `Fraction` arithmetic gives

```text
A_S = 266
C_S = 2260
D   = 75
GS margin = D^2 - 2*C_S - 4*A_S = 41
average conductor upper bound = 269993/512
genus denominator upper bound = 620201/1024
Ihara ratio lower bound = 196608/620201
```

The fixed-`S` scan of every `t=1,...,192` accepts all 192 values and has
maximum feasible `t=192`.  The exact ratio is strictly above the historical
`24576/77527` by
`368640/48082322927`.  The corresponding exact coding expression is
`1 - 620201/196608 = -423593/196608`, so the certificate correctly records
that it gives no positive coding guarantee.

The checker also recomputes the winner recorded in `results/m2-search.json`.
Its `nu2_search.automatic_best` and local-neighborhood winner both have the
same five rows and exact arithmetic above; the reported finite-search counts
are 99,835 evaluated configurations, 99,806 accepted configurations, and
14,112 local variants.  The checker cross-validates the winner fields and
baseline comparison; it does not treat those traversal counters as a proof
outside the recorded finite search box.

## Tower certificate fields

The `k/H` ramification row records both degree-5 places with residue degree 1
and index 32.  For `K/k`, the exact degree remains explicitly unknown.  The
checker requires `K_over_k` and the exact ray-group order/invariant factors to
remain null, while checking every local inertia upper bound against `2^d`:
32 at degree 5, 64 at degree 6, 256 at degree 8, 1024 at degree 10, and 4096
at degree 12.  It also checks `k/H=32`, p-rank lower bound 75, relation-minus-
generator bound 1321, and the recorded GS comparison `41 >= 0`.

## Adversarial inputs

The same validator predicates reject all of these mutations:

| Mutation | Result |
|---|---|
| duplicate selected place | `REJECTED` |
| wrong declared degree | `REJECTED` |
| wrong chart | `REJECTED` |
| altered AS coordinate/equation | `REJECTED` |
| changed arithmetic field | `REJECTED` |
| failed GS condition | `REJECTED` |
| unavailable multiplicity | `REJECTED` |
| duplicate certificate `S` row | `REJECTED` |
| modulus exponent changed from 2 | `REJECTED` |
| fabricated exact `K/k` degree | `REJECTED` |
| changed certificate denominator | `REJECTED` |

This artifact independently certifies the finite representative, orbit,
selection, and exact arithmetic checks through the displayed degree-12
inventory.  It leaves the exact auxiliary ray degree and ray-group structure
unknown, as required by the certificate, and does not independently establish
the global tower or exchange lemma.
