# Fixed-k ν=2 obstruction with relaxed all-degree stocks

This is a separate bounded arithmetic audit of the automatically discovered
ratio `196608/620201`. It uses certified `k343` counts for degrees 2 through
11, including zeros, and then grants **hypothetical** stocks
`floor(266/f)` for every degree 12 through 47. Those high-degree stocks are
not certified place counts and are used only to form a superset of every
actual configuration that could beat the incumbent.

## Why the relaxation is finite

Let `b=196608/620201`, `g=343`, `N=192`, and let `cost` be the ν=2
conductor-filtration cost. A strict improvement requires

`cost < N/b-(g-1) = 269993/1024`.

The certified stocks in degrees 5, 6 and 8 contribute at most `37/16` rebate;
every other nonzero degree in the certified prefix or relaxation is at least
10, so its rebate is at most `A/1024`. Therefore

`cost >= A-37/16-A/1024`,

which gives `A < 90787/341` and hence `A<=266`.
This also bounds every hypothetical multiplicity by `floor(266/f)`. Combining
the necessary

`t >= floor(b*(342+max(0,A-37/16-A/1024)))+1`

with `I>=0` gives the computed global cap `C<=2280`. Since each selected
degree contributes `f(f+1)` to C, any selected degree satisfies `f<=47`.
Thus degrees 2 through 47 cover every possible strict improvement under this
fixed-k, ν=2 score, while degrees above 47 are ruled out arithmetically.

## Exact DP and result

The raw relaxed multiplicity product is
`56105893364599166726515358592663552000000` and is not enumerated. The DP
state is `(A,C)` and retains the maximal exact rebate
`sum(m*d/2^d)`, scaled by `2^47`, with a witness. Equal `(A,C)` states with a
smaller rebate are dominated because they have the same optimal t and a larger
denominator. Partial states are pruned only by the global caps `A<=266` and
`C<=2280`.

The DP has `95103` final states after
`4402558` transition attempts. It applied
`24513863` global cap choices and removed
`1387271` dominated transitions. After the
final t and GS checks, it found
`0` strict improvements over the
incumbent. The best witness is
`{'2': 0, '3': 0, '4': 0, '5': 2, '6': 16, '7': 0, '8': 16, '9': 0, '10': 2, '11': 0, '12': 1, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0, '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0, '37': 0, '38': 0, '39': 0, '40': 0, '41': 0, '42': 0, '43': 0, '44': 0, '45': 0, '46': 0, '47': 0}`, with rows `[[5, 2, 2], [6, 16, 2], [8, 16, 2], [10, 2, 2], [12, 1, 2]]` and exact
ratio `196608/620201`. A witness cross-check using
`src/theorem_search.py` agrees with the DP state and witness. Independent
exhaustion is checked by `tests/independent_obstruction.py`; see
`results/INDEPENDENT_OBSTRUCTION.md` for its separate verification report.

The bounded conclusion is: No hypothetical degree<=47 ν=2 configuration beats the incumbent. Consequently, after the separate geometric obligations are met for the winner, this certifies the conservative fixed-k ν=2 score optimum.
It does not certify place existence for the hypothetical high-degree stocks and
makes no claim about other depths, curves, criteria, exact ray groups, or
global `A(2)`.

## Reproduction

```sh
python3 experiments/search_all_degree_relaxation.py
```

The machine-readable artifact is `results/all-degree-relaxation.json`.
