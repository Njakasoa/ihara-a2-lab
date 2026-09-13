# Public export validation

Date: 2026-09-13. These checks ran in the separate public export directory,
without the original Git history, session settings or third-party paper copies.

- Python 3.12: `python3 publication/reproduce.py --extended` completed with
  `PUBLICATION_REPRODUCTION=PASS`, including all 29 unit tests, 373-cover
  search, extended-degree search and independent obstruction enumeration.
- Independent Sage baseline checker: process exit 0; complete degree-686
  zeta reconstruction, historical control arithmetic and negative cases pass.
- Independent Sage candidate checker: `M2_CERTIFICATE=PASS`, process exit 0;
  the finite places, support, modulus, exact ratio and negative cases pass.
- Sage checks used the existing local SageMath 10.9 runtime through the
  documented SAGE_PREFIX override. No runtime binaries are exported.
- Scientific replay outputs match the archived data. Only elapsed_seconds
  fields and their presentation changed in the intermediate-cover reports;
  comparison excluding those timing fields passed. Archived bytes were then
  restored. The hash manifest covers those archived bytes, not future timings.
- The reviewed manuscript source and PDF are byte-identical to the source lab.
- Credential-pattern and private-path scans of exported text found no
  remaining matches after removing the Tectonic lock's local path header.
- Operational directories, session logs and third-party full papers/text
  are excluded. The largest exported file is below 2 MB.

This is local reproducibility and internal scientific review, not an external
peer-review report or proof of publication priority. Reproduce the portable
core with the commands in README.md; optionally install Sage for its checks.
