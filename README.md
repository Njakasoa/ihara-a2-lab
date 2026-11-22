# Ihara A(2) Lab

A reproducible research companion on curves over F₂ and class-field towers,
maintained by [Njakasoa](https://github.com/Njakasoa).

**Status: internally reviewed research manuscript. Publication priority is
unresolved. No external peer review or journal/arXiv submission is claimed.**

## Main result

On the genus-334 base of Ma, Xing and Xing, an isolated local relation at
the chosen degree-12 place gives

```text
A(2) ≥ 32768/103115 = 0.3177811181690346…
```

For an explicit support in the fibres cited in Theorem 6.1, the degree-12
inertia in the elementary ray field has order **2,048**. This lowers the
upper bound on the mean conductor degree by **3/512** and improves the
authors’ fraction **65536/206231** by about **0.000001541**.
[Genus-334 proof, support and Sage replay](proofs/MXX_GENUS334_DEGREE12.md) ·
[Ma–Xing–Xing, Theorem 6.1](https://arxiv.org/html/2610.33649v2#S6.SS1)

## Genus-343 base

The exact mean conductor of the full M2 ray field on the genus-343 base gives

```text
A(2) ≥ 98304/310099 = 0.3170084392403716…
```

The M2 manuscript first obtained `196608/620201 = 0.3170069058256919934…`.
The exact-inertia calculation determines all 37 inertia orders. At the
degree-12 place, one isolated T-unit relation lowers the mean conductor
degree by exactly 3/512 and gives the bound above.
[Degree-12 proof, conductor table and Sage replay](proofs/M3_DEGREE12_INERTIA.md)

The manuscript refines the displayed estimate `24576/77527 = 0.3169992389748087763…`
of [Duursma–Mak](https://arxiv.org/abs/1102.4127), using their same genus-343
base and class-field-tower criterion. Two places of degree 10 are replaced
by places of degrees 8 and 12. The denominator decreases by exactly 15/1024
and the sufficient Golod–Shafarevich inequality retains positive margin 41.

The M2 result is a parameter refinement, with exact finite-field certificates
and independent Sage verification. It does not determine A(2), provide a new
general tower criterion, or establish a better binary error-correcting code.
The exact auxiliary ray degree and group structure remain uncomputed and are
not needed for the proved ratio. Novelty is **POSSIBLY NOVEL**, not established.

Ma, C. Xing and Z. Xing obtain
`A(2) ≥ 65536/206231 = 0.3177795772701485…` in
Theorem 6.1 of their October preprint. The Sage replay reconstructs their
genus-334 field and checks the tower criterion. With precisely their support
degrees and multiplicities, the score on the laboratory’s genus-343 base is
`65536/209303`, below its M3 maximum. [Worked comparison and replay](publication/THEOREM_6_1_M3.md)
· [Preprint, v2](https://arxiv.org/abs/2610.33649v2).

- [Manuscript PDF — 4 pages](publication/main.pdf)
- [LaTeX source](publication/main.tex) and [reproduction guide](publication/README.md)
- [Full lower-bound proof](proofs/IMPROVED_BOUND.md) and [exact certificate](certificates/m2-tower.json)
- [Validation](publication/VALIDATION.md), [adversarial proof review](results/ASTRA_M2_REVIEW.md), and [novelty audit](references/M2_NOVELTY_VERDICT.md)
- [French results summary](results/FINAL_SUMMARY.md) and [research directions](NEXT.md)

## Restricted obstruction and exploration

A separate [verified obstruction](claims/CLAIM-0003.md) proves that
196608/620201 is the maximum of the specified conservative score on this genus-343
base, for all finite nonrational supports, conductor two everywhere, and
1 ≤ t ≤ 192, with no initial degree cutoff. Exact caps reduce the problem to
degrees ≤ 47; independent partition enumeration confirms zero improvements.
This does not bound the actual ratios of all such towers or A(2) from above.

The lab also reconstructs historical controls and the full zeta polynomial of
the base, searches 373 intermediate covers and 14,112 local conductor
variants, and retains inferior and failed sufficient-criterion cases.
See [normalization](NORMALIZATION.md), [baseline reconstruction](proofs/DUURSMA_MAK_RECONSTRUCTION.md),
[search results](results/M2_SEARCH.md) and [coding interpretation](codes/PHYSICAL_INTERPRETATION.md).

## M3: nonuniform conductors and refined ray score

The internally verified M3 supplement proves that **196608/620201 remains
exactly the maximum of the specified refined sufficient score** on the fixed
genus-343 base, allowing all finite ramification supports, rational ramified
places, every conductor bound ν≥2, and all nonempty disjoint rational splitting
sets T. This is a ceiling for that score, not for actual tower ratios or A(2).

The score uses the local generator rank in the relation bound and the maximal
elementary ray subfield for its conductor estimate. Exact inequalities reduce
arbitrary degrees and depths to 11,384 necessary pairs; the remaining deeper
pattern is excluded analytically. A Sage search constructs 31 independent
T-unit relations. The degree-10 calculation below proves that the full
T-unit jet image has **rank 191**, giving **2⁷⁵ ≤ |G| ≤ 2¹²⁶**.
For the fixed M2 modulus and splitting set, descent by
norms to the genus-13 quadratic subfields determines the inertia orders in the
full abelian 2-primary ray group. Each of the two degree-5 places has order
**32**, and each of the 16 degree-6 places has order **64**. Their respective
contributions to the mean conductor degree are 155/8 and 189. The inertia
order at each of the 16 degree-8 places is **256**. Here the quadratic
norms leave one possible nonzero jet. Descent to a single degree-four
subfield excludes it. The degree-8 contribution to the mean conductor
degree is exactly 255. The two degree-10 places each have inertia order
**1,024**. Once the jets vanish at the 34 places of degrees 5, 6 and 8,
a trace calculation and the logarithmic-derivative identity force the two
degree-10 jets to agree. The degree-12 place has inertia order **2,048**.
The exact mean conductor degree of the full ray field is **134995/256**.
[Degree-five inertia proof and Sage replay](proofs/M3_DEGREE5_INERTIA.md) ·
[Degree-six inertia proof and Sage replay](proofs/M3_DEGREE6_INERTIA.md) ·
[Degree-eight inertia proof and Sage replay](proofs/M3_DEGREE8_INERTIA.md) ·
[Degree-ten inertia, T-unit rank and Sage replay](proofs/M3_DEGREE10_INERTIA.md) ·
[Degree-twelve isolated jet and full conductor](proofs/M3_DEGREE12_INERTIA.md) ·
[Quadratic T-unit search](results/M3_QUADRATIC_TUNIT_SEARCH.md).

- [M3 result and scope](M3_RESULT.md), [refined criterion](proofs/M3_REFINED_RAY_CRITERION.md), and [all-depth obstruction](proofs/M3_REFINED_OBSTRUCTION.md)
- [Exact ray components](results/RAY_CLASS_STRUCTURE.md) and [claim records](claims/CLAIM-M3-0002.md)
- [Independent validation](results/M3_INDEPENDENT_VALIDATION.md), [Astra proof review](results/M3_ASTRA_REVIEW.md), and [final scope review](results/M3_FINAL_SCOPE_REVIEW.md)
- [Separate novelty audit](references/M3_RAY_LITERATURE.md): priority remains unresolved

The four-page manuscript below documents M2; M3 is supplied in the separate
proofs, certificates and checkers linked above.

**Lean 4 formalization (22 November 2026).** The kernel checks that every
admissible finite support has elementary-ray score at most `196608/620201`
on the genus-343 inventory and that the M2 witness attains it. The proof
allows arbitrary stocks above degree 12. It also checks the arithmetic of
Ma–Xing–Xing's Theorem 6.1 on the genus-334 base. The geometry is supplied by
the Sage certificates. [Build instructions and scope](formal/README.md) ·
[Maximum theorem](formal/IharaM3/Maximum.lean).

## Reproduce

Use Python 3.12 from the repository root. The core needs only the standard
library, with no account, API key, third-party paper download or Sage install:

```sh
python3 scripts/check_public_snapshot.py
python3 publication/reproduce.py
```

The reproduction command rebuilds the baseline, runs both exact parameter
searches, binds the winning places, replays failed variants, verifies the
standalone degree-12 certificate, runs 40 unit tests and checks the independent
all-degree obstruction. These are exact computations supporting the written
proof; they are not a proof-assistant formalization.

For the extended searches or independent Sage implementations:

```sh
python3 publication/reproduce.py --extended
python3 publication/reproduce.py --sage
```

`--sage` requires the separately installed Sage environment. The historical
audit used SageMath 10.9; [environment setup and exact package locks](ENVIRONMENT_AUDIT.md)
document reconstruction. The optional PDF build uses Tectonic 0.17.0.

For the genus-334 result alone, run `sage -python experiments/reproduce_mxx_theorem61.py`
from the repository root. It recomputes the [exact certificate](certificates/mxx-theorem61.json).

The manifest checker verifies the archived snapshot before a replay. Extended
searches overwrite historical reports with fresh elapsed-time measurements;
those timing changes intentionally change their file hashes. Scientific
payloads were compared separately for the public export, as recorded in
[PUBLIC_VALIDATION.md](PUBLIC_VALIDATION.md).

To check the archived M3 certificates with standard-library Python:

```sh
python3 tests/independent_m3.py
```

For the complete M3 replay, configure the Sage environment as documented in
[ENVIRONMENT_AUDIT.md](ENVIRONMENT_AUDIT.md), then run:

```sh
python3 experiments/run_m3.py
```

This executes eight validation commands, including 40 unit tests, separate
finite-field arithmetic and nine rejected certificate mutations. It refreshes
receipt timestamps and hashes; check the public snapshot before replaying it.
The optional 120-second Sage maximal-order capability pilot is excluded from
this command. [Public M3 validation](M3_PUBLIC_VALIDATION.md) records the export checks.

## Public snapshot and provenance

This repository starts from a curated source snapshot. The original Git
history, operational settings, session notes, runtime installations and
third-party paper copies are excluded. [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)
records the source revision and exported file hashes. Historical scientific
reviews are retained as dated evidence; statements in them about permission
or public availability describe the original research session. The current
GitHub publication is authorized, and is separate from journal submission.

AI-assisted research and internal Astra/Luna review are disclosed in the
manuscript and validation records. No external reviewer endorsement, DOI or
arXiv identifier is invented. See [publication record](PUBLICATION.md).

## License and citation

Project code and technical documentation: [MIT](LICENSE), following the
companion-laboratory format. Manuscript and third-party rights are separate:
[rights and attribution](publication/RIGHTS.md). Citation metadata are in
[CITATION.cff](CITATION.cff). Primary articles are [linked](papers/README.md),
not redistributed.

Related laboratories: [Quantum Max-Cut](https://github.com/Njakasoa/quantum-max-cut-lab),
[Self-Avoiding Walk](https://github.com/Njakasoa/self-avoiding-walk-lab), and
[Tight Knots](https://github.com/Njakasoa/tight-knots-ropelength).
