# Independent obstruction verification

Date: 2026-09-13. **PASS**, with process exit code 0 observed by the root.
The checker was independently authored by the Luna tester. This report was
persisted by the root from its actual execution output.

Command: `python3 tests/independent_obstruction.py`.
The checker uses Python standard-library `Fraction` arithmetic and does not
import the search engine or its dynamic program. It derives the caps anew,
then enumerates low-degree deficits and nondecreasing high-degree partitions.
It checks exhaustion, rather than only re-evaluating the winning witness.

```text
INDEPENDENT_OBSTRUCTION=PASS
A_cap=266; C_cap=2280; degree_cap=47
continuous_survivors: A=266, t_min=192, C_min=2236, C_max=2280
low_total=867; low_pruned=860; low_cases=7
partition_nodes=107; partition_pruned=32
candidate_count=2; strict_improvement_count=0; equal_incumbent_count=1
CERTIFICATE=PASS
```

The remaining configurations have degree multiplicities:

| Support | C | GS margin | Exact cost | Exact score |
|---|---:|---:|---:|---:|
| 5:2, 6:16, 8:15, 10:4 | 2252 | 57 | 33751/128 | 24576/77527 |
| 5:2, 6:16, 8:16, 10:2, 12:1 | 2260 | 41 | 269993/1024 | 196608/620201 |

Six altered certificate fields were rejected: A cap, C cap, degree cap,
result ratio, conclusion and relaxation rule. The production searches also
pin the reviewed low-degree inventory; altered low-degree stock is rejected.

This closes the independent-exhaustion condition in
`results/ASTRA_OBSTRUCTION_REVIEW.md`. The theorem-search call inside the
production experiment is only a witness cross-check, not this independent
verification. The reviewer report remains unchanged as an audit trail.

Accepted scope: fixed genus-343 base k, finite nonrational support, conductor
two everywhere, 1 <= t <= 192 and the specified conservative Duursma–Mak
criterion and score. The maximum is 196608/620201. This does not bound actual
tower ratios, stronger infinitude criteria, other conductors or A(2) itself.
The review is internal AI-assisted verification, not external peer review.
