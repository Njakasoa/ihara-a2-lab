# M2 — exact automated theorem-parameter search

The M1 gate is recorded as **ACCEPTED** in `results/M1_STATUS.md`. This report
searches the certified `k343` place-count inventory through degree 12 with the
binary Duursma–Mak arithmetic. The search is finite and exact; its geometry
and later ray-tower obligations remain explicit.

## Exhaustive `nu=2` box

For each available nonrational degree `d`, every multiplicity
`0 <= B_d <= B_d(k343)` was considered. The positive counts are
`B_5=2, B_6=16, B_8=16, B_10=64, B_12=208`.
For a row `(d,n,nu)`, the engine uses

`A += n*d*(nu-1-floor((nu-1)/2))`,
`C += n*[d*(nu-1)]*[d*(nu-1)+1]`, and
`I = D^2 - 2*C - 4*A`, where `D=1+A-t`.

For fixed `A,C`, the largest possible splitting set is computed, never
guessed:

`t = min(N, A, 1 + A - ceil_sqrt(2*C + 4*A))`.

The exact conductor-filtration cost is a `Fraction`. A branch is pruned only
when its partial cost is already at least
`N/incumbent-(g-1) = 33751/128`. Since `t <= N` and all
remaining costs are nonnegative, this strict-cost test cannot discard a
configuration that beats the historical incumbent `24576/77527`.

The box contains `11778195` multiplicity vectors. The
engine cut `2715432` monotone branch choices,
covering `11678360` complete vectors by this rule, and evaluated
`99835`, accepted `99806`
after the sufficient criterion, and recorded `29` with no
positive theorem-admissible `t`. GS failures after the exact `t` calculation:
`0`.

## Automatically found winner

The search returned multiplicity vector `{'5': 2, '6': 16, '8': 16, '10': 2, '12': 1}` and rows `[[5, 2, 2], [6, 16, 2], [8, 16, 2], [10, 2, 2], [12, 1, 2]]`. Its exact
arithmetic is `A=266`, `C=2260`, `D=75`,
`I=41`, `t=192`, with denominator
`620201/1024` and ratio
`196608/620201 approx 0.31700690582569199340`. The historical ratio is
`24576/77527 approx 0.31699923897480877630`; the exact
difference is `368640/48082322927` (strictly positive).

This is an automatically discovered finite-box improvement. It is not a new
asymptotic claim yet: the degree-12 place must be exhibited, the selected
places must be distinct, an explicit `T` must be disjoint from `S`, and the
p-primary T-ray tower hypotheses must be proved for the selected divisor.
The engine computes no unsupported ray-group rank or exact auxiliary degree.

## Bounded even-depth neighborhood

Starting from the automatic winner, the local audit varies each degree's
multiplicity independently over `base-1, base, base+1` clipped to inventory
availability. It enumerates all per-degree uniform assignments in
`{2,4,6}`, together with one exceptional selected place at one degree of
depth 4 or 6 while the other selected places have depth 2. This is a bounded
local scope, not an arbitrary nonuniform search.

It generated `17496` uniform and
`672` exceptional
variants, deduplicated to `14112` cases, and
accepted `14112`. The best local case is
`196608/620201`;
no local case is promoted beyond the finite arithmetic audit. Odd depths are
handled by the conservative domination statement in
`proofs/CONDUCTOR_FILTRATION.md`, and ternary refinement is excluded.

## Reproduction and status

```sh
python3 experiments/run_parameter_search.py
```

The machine-readable output is `results/m2-search.json`. Statuses are exact
integer/rational arithmetic plus open geometry obligations. No optimum outside
the stated finite inventory box is claimed.
