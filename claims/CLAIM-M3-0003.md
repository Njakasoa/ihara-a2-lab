# CLAIM-M3-0003 — Five exact T-unit relations and a smaller ray-order cap

Mathematical validity: **VERIFIED RESULT, internal level 5** for the stated
component result: Sage calculation, independent coordinates and Astra acceptance. Novelty: **KNOWN method**,
**POSSIBLY NOVEL instance**, no priority claim.

Exact statement: for the frozen M2 support, the local direct sum
⊕_P U_P^1/U_P^2 has dimension266 over F2. The T-units x,x+1,y,y+1,y+x
give a subspace of dimension5. Its intersection with every single local
block is zero. With the accepted v2 of the complete Jacobian order equal to51,
the T-split 2-primary ray group G satisfies **2^75≤|G|≤2^312**.

Relation to M2: improves the previous upper cap2^317 by five bits. Neither
degree bound changes the proved Ihara ratio, because degree cancels there.
The complete ray group, its generator rank and cyclic factors remain unknown.
All individual inertia orders and the actual conductor mean remain unknown.

Exact data: 37 residue-field representatives, ten explicit unit rows of
266 bits, rank5; projected ranks at degrees5,6,8,10,12 are0,3,4,5,5.
Projection ranks do not equal supported relation dimensions. Additional
unknown T-units may still shrink individual inertia images.

Ray assumptions: the five base units have zeros/poles only above the six
rational places of H, all splitting in k. Norms are x(x+1), x²(x+1), and
x²(x+1)² for y,y+1,y+x. The standard split-ray exact sequence gives the
upper order bound without assuming those units generate all T-units.
The Jacobian valuation51 is an order datum, not a generator rank.

Proof/data: `proofs/M3_RAY_DUALITY.md`, `results/RAY_CLASS_STRUCTURE.md`,
`experiments/m3_ray_structure.py`, `results/m3-ray-structure.json`.
The Sage global maximal-order pilot timed out at120 seconds. No full ray
computation or exhaustive character enumeration is implied.

Independent verification: Astra reduced the raw rows and checked every
block intersection and the sequence argument. `tests/independent_m3.py`
independently reconstructs residue fields and local coordinates with PASS
(results/M3_INDEPENDENT_VALIDATION.md). Mutated degree, Frobenius and rank fields are explicit targets.

Novelty search: `references/M3_RAY_LITERATURE.md`; Auer supplies the standard
local-unit approach. Generalization: explicit T-unit subspaces can improve
order caps on other bases, but only supported relations reduce inertia.

Open objections: no material internal objection remains within the stated scope. The distinction between known
subspace and full image is an essential limitation; no coding benefit claimed.
