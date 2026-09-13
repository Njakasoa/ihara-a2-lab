# Extended degree search — k343, binary `nu=2`

This bounded follow-up checks whether degrees 13 through 30 can improve the
automatically discovered degree-12-box ratio `196608/620201`. It uses the
certified `curves/k343-place-counts-30.json` inventory, with `g=343` and
`N=192`. It makes no claim outside this finite arithmetic box.

## Exact caps and compressed dynamic program

The incumbent is `b=196608/620201`. A strict improvement has conductor cost

`cost < 192/b - 342 = 269993/1024`.

Using the exact rebate bound
`rebate <= 37/16 + A/1024` gives

`A < 90787/341`, hence the integer cap
`A <= 266`. For each integer A, the necessary numerator bound is

`t >= floor(b*(342+max(0,A-37/16-A/1024)))+1`.

Combining this with `I>=0` gives a computed global `C` cap of
`2280`; it is attained at
`[{'A': 266, 't_min': 192, 'D_at_t_min': 75, 'C_limit': 2280}]`. These A and C caps are global monotone bounds, so they are the
only arithmetic caps applied to partial DP states.

For each degree, multiplicities are bounded by both its certified stock and
`floor(266/d)`. The raw bounded product is
`92424908105348442624000000` and is not enumerated. A DP
state is `(A,C)` and retains the maximum exact rebate
`sum(m*d/2^d)`, scaled by `2^30`, together with one witness. At a fixed `(A,C)`
this rebate uniquely minimizes the conductor cost, so the dominance rule is
exact for the theorem objective.

The DP produced `90989` final states after
`2681271` transition attempts. Globally capped choices:
`14329877`; dominated rebate transitions:
`1276249`. After the final necessary t and GS
checks, `0` states strictly beat the
incumbent and `2` do not.

## Result

The best DP witness has multiplicity vector `{'5': 2, '6': 16, '8': 16, '10': 2, '12': 1, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0, '30': 0}` and rows
`[[5, 2, 2], [6, 16, 2], [8, 16, 2], [10, 2, 2], [12, 1, 2]]`. The JSON records its DP state and an independent evaluation by
`src/theorem_search.py`; the exact ratio is
`196608/620201`. The independent evaluator agrees
with the DP state and witness. No candidate vector was supplied to the DP.

This is an arithmetic search result. The selected degree-12 and higher-degree
places must be exhibited as distinct places, `T` must be explicitly chosen and
disjoint from `S`, and the constant-field and p-primary ray-tower hypotheses
remain proof obligations. No ray-group rank or exact ray degree is inferred.

## Reproduction and scope

```sh
python3 experiments/search_extended_degrees.py
```

The search covers only `k343`, degrees at most 30, and uniform depth `nu=2`.
It does not search all depths, other base curves, ternary refinement, or an
unrestricted global optimum.
