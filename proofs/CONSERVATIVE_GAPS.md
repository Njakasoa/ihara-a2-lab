# M3: where the M2 proof loses information

Baseline b=196608/620201, k/F2 genus343, N=192; source proof frozen in
M2_BASELINE.md. This audit distinguishes exact formulas from their numerical
evaluation. It does not change the accepted M2 bound.

| Quantity | M2 value or bound | Why / source of loss | Exact computation and likely cost | Potential effect |
|---|---|---|---|---|
| Local inertia at a nu2 place | order(I_P) <= 2^f | Full local units bound the image after T relations | Rank of single-coordinate intersection with global T-unit relation image; high-genus global arithmetic | Direct denominator decrease if any local image is smaller |
| Mean local conductor | E[a_P] <= 2(1-2^-f) | Exact identity is 2(1-1/order(I_P)) | Easy exact rational once inertia order is proved | Highest direct target; equality if all images maximal |
| Mean total conductor | <=269993/512 | Sum of those local bounds | Marginal image sizes suffice; no full character enumeration needed | No further saving from correlations alone, by linearity |
| Generator 2-rank | d_2(G)>=1+A-t=75 | Ignores additional class-group/relations data | Split ray group mod2, distinct from valuation of group order | May allow cheaper supports or fewer ramification places |
| Relation minus generator rank | <=C/2+t-1=1321 | Universal local/global relation bound | Exact pro-2 presentation not currently available; inspect local decomposition/image bounds | Could strengthen infinitude condition; requires new proof |
| Ray degree [K:k] | power of2, >=2^75; exact unknown | Generic ray lower bound; order and cyclic structure not computed | T-unit exact sequence, class quotient and local images | Cancels from final ratio; knowing it alone yields no improvement |
| Rational points splitting upstairs | >=192[K:k] | Counts guaranteed T lifts only | Additional splitting outside T; k has exactly192 rational places and T is all of them | No extra degree-one places available over k in M2 |
| Genus relation | g(K)-1=n(342+mean conductor/2) | Exact conductor-discriminant identity | Known once exact mean obtained | No independent slack in this identity |
| Tower infinitude and constant field | Proved by GS and T nonempty | Sufficient criterion, not a numerical equality | Review any proposed stronger criterion separately | A failing sufficient test never proves a finite tower |

## Priority and finite computations

First derive the ray exact sequence and inertia image formulas; then compute
feasible components with Sage. The known Jacobian order has 2-adic valuation51,
which is not the 2-rank and does not specify the T-split quotient. The
elementary abelian k/H degree32 cover is not the later K/k ray extension.

Uniform restriction of global characters onto a finite inertia subgroup is a
surjective dual map with equal-size fibers. For general depth nu, if I^r is
the image of U^r and I^0=I^1, the exact identity is

    E[a_P] = nu - 2/|I^1| - sum_{r=2}^{nu-1} 1/|I^r|.

Computing these orders is enough; local character variables need not be
independent. Full ray groups at depth greater than2 can have characters of
order4 and higher. An Artin–Schreier-only conductor law cannot be substituted
for the full ray law without changing and reproving the tower argument.

## First structural question for the optimizer

For the existing conservative score, odd nu>=3 are dominated by nu-1.
For even nu=2s, examine the rank A_P=f*s, relation contribution
C_P=f(2s-1)[f(2s-1)+1], and rebate A_P-f*E[a_P]/2.
Compare extra depth with the cheapest unused first layers before expanding
the search. Rational places require explicit t<=192-|S rational|.

M3 closure: exact local theory and five T-unit relations reduce the ray-order
cap to2^312, but no individual inertia order or actual mean is resolved. The
rank-based local relation estimate and elementary-ray mean improve the scoring
law at higher depths; the refined obstruction proves no score gain on k343.
No unknown group data is filled speculatively.
