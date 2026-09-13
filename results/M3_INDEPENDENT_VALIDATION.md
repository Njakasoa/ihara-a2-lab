# Independent M3 validation

Status: **PASS**.  This is an independent standard-library checker for the
refined elementary-ray obstruction, the frozen M2 arithmetic, and the finite
ray representative component.  The checker is
`tests/independent_m3.py`; it imports no production module from `src/` or
`experiments/`.

Command executed:

```text
python3 tests/independent_m3.py
```

Receipt: `results/m3-independent.json`.  The metadata block below records the
captured run used for this report; after later commits, a fresh JSON receipt
from `python3 tests/independent_m3.py` is authoritative.

## Initial historical receipt

Later root reruns replace the JSON receipt with current commit/hashes; the
metadata below document the initial successful tester run.

```text
experiment_id: M3-INDEPENDENT-VALIDATION-001
UTC: 2026-09-13T13:03:08.672692+00:00
commit: ad69023e028081a54980c18d8a9070ac11feb7c2
runtime_seconds: 0.348817
script_sha256: 5068aab5b4141f10be359de4dd495424af97ae4acdedb1c6bf6586e59ddd072a
payload_sha256: b1e2ce1797fb1da50d6d59cec1a8786bfa124a1e723ad42e85aac3d6efd2091c
verification_status: PASS
```

The complete current input hash map is recorded in the JSON receipt.  The
public checker hashes the scientific result notes, M2 freeze, refined proofs, local certificates,
place inventory, and all three production receipts on every run, so a rerun
after a root commit records fresh metadata.

## Refined obstruction arithmetic

The checker independently derives the elementary-ray rebate

```text
beta = 1290176/608685
```

and enumerates the exact necessary `(n,A)` caps with Fraction arithmetic.  It
obtains:

```text
pairs_tested       = 11384
splitting_rejected = 7862
relation_rejected  = 3521
survivors          = [(n=0, A=266, t_min=192, t_max=192,
                       C_min=2236, C_max=2280)]
```

The two high-degree residual cases are checked by the independent Cauchy
bounds `783/2 > 316` and `1330/3 > 388`.  All 20 recorded assignments are
recomputed from their rows; the maximum is exactly
`196608/620201`, and no assignment exceeds it.  The old all-degree
obstruction is also cross-checked independently: `9861` pairs, `7374`
splitting rejections, `2486` relation rejections, and the same sole survivor.

The frozen M2 row independently recomputes as

```text
A=266, C=2260, D=75, GS_margin=41,
genus_denominator=620201/1024, ratio=196608/620201.
```

## Local and ray checks

The checker uses its own binary-polynomial finite fields and verifies the
irreducibility of each certificate modulus.  It reconstructs all 37 selected
representatives, checks the base-curve and five Artin--Schreier equations,
and checks every declared Frobenius orbit.  The degree-six lifting certificate
is independently checked, including all 13 five-bit Frobenius vectors and the
`208` lower bound.

It derives all ten local `U_P^(1)/U_P^(2)` coordinates from the raw residue
representatives and independently checks the derivative identities.  Packing
those coordinates gives the recorded 266-column matrix.  A separate
lowest-pivot F2 Gaussian elimination gives relation rank `5`, independent
units `x, x+1, y, y+1, y+x`, and zero intersection of the known relation space
with each of the 37 local blocks.  The Jacobian checksum gives `v2=51` and
the displayed known-relation quotient dimension is `261`.

The compact local-unit check directly multiplies truncated series over binary
fields for 15 fixtures, including odd and even cutoffs and the 4096-element
boundary `(f,nu)=(12,2)`.  It verifies orders, killed layers, cyclic order
profiles, full character conductor counts and averages, exponent-two
Artin--Schreier counts and averages, elementary rebates, and rank-based
relation terms.  No global ray group is inferred from these finite checks.

## Mutation gate

Every required mutation was rejected by recomputation:

| Mutation | Result |
|---|---|
| selected place degree | `REJECTED` |
| Frobenius vector | `REJECTED` |
| conductor `nu` | `REJECTED` |
| known group rank | `REJECTED` |
| support multiplicity | `REJECTED` |
| GS margin | `REJECTED` |
| refined proof cap | `REJECTED` |
| refined proof constant (`beta`) | `REJECTED` |
| refined survivor list | `REJECTED` |

## Coverage and unknowns

Covered are the exact necessary-condition arithmetic, all-depth refined
constants and survivors, baseline arithmetic, raw finite-field equations and
Frobenius data, raw ray relation coordinates and rank/intersection arithmetic,
and the bounded local unit laws.  The checker does not establish the full
split ray-class-group order or cyclic factors, hidden `(T)`-unit relations,
exact global inertia orders or conductor means, actual tower ratios, or a new
unconditional `A(2)` bound.  Those remain explicitly unknown in the ray
receipt and outside this independent finite gate.

Public-export adaptation: the private session mission input is replaced by
M3_RESULT.md for receipt provenance. Mathematical computations are unchanged.
The JSON receipt is refreshed by the public-copy replay.
