# M3 public export validation

Scientific source:08ae780f7422d1cc0baf63f1cd1a198463d7a95f, 2026-09-13.
The original M3 scientific cycle passed independent arithmetic and Astra
review before this export. Public-copy reproduction is the final export gate.

Only provenance and presentation are adapted: private mission input references
become M3_RESULT.md, local output paths become repository-relative, and public
status/README/citation are updated. All mathematics and frozen M2 files are
preserved. Historical proof-review reports remain dated records; fresh public
execution metadata belong to the JSON receipts.

Commands: python3 experiments/run_m3.py (existing Sage10.9 runtime supplied
through SAGE_PREFIX), python3 scripts/check_public_snapshot.py. The first
command regenerates all primary M3 receipts and runs the independent baseline
and terminal obstruction. The historical optional pilot is not rerun.

Public-copy execution PASS at commit `b39b6a6988cf234e120baeac3a7946062222ddce`:
all eight commands exited0 in 9.674212seconds;40 unit tests passed,
and all nine M3 mutations were rejected. The exact obstruction data, all local
fixture reports, raw ray coordinates/ranks, and independent scientific payloads
match the validated original lab. The ten frozen M2 hashes remain unchanged.
Input/output receipt hashes were checked against actual public-copy files.

A scan of exported source and receipts found no private filesystem or attachment
paths or credential-pattern matches. The source manifest was refreshed after
validation. Original historical pilot evidence is preserved without rerunning
the slow pilot; original-science commit references in that receipt are provenance,
not revisions in this separate public Git history. GitHub
publication is separate from external peer review, priority and submission.
