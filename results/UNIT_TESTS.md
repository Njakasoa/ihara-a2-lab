# Internal regression tests — 2026-09-13

Root execution:

```text
python3 -m unittest discover -s tests -v
Ran 29 tests in 1.707s
OK
```

Coverage:9 M1 finite arithmetic/geometry/zeta controls,7 intermediate-cover
checks,8 theorem-search/evaluator tests,5 candidate-binding tests. The search
checks compare the optimized t rule to direct enumeration and pruned search
to unpruned small boxes. The binding tests reject altered arithmetic, missing
degree12 inventory, duplicate support and a failed GS row.

This is internal regression coverage, distinct from the independent Sage
implementations and the adversarial mathematical review. The subsequent
standalone publication/checkers/degree12.py also returned PASS.
