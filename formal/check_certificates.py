"""Cross-check the published Sage/Python inputs against the compiled Lean model."""

import json
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

FORMAL = Path(__file__).resolve().parent
ROOT = FORMAL.parent


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def nat(value):
    if type(value) is not int or value < 0:
        raise ValueError(f"Expected a natural number in the certificate, got {value!r}")
    return value


def rows_literal(rows):
    return "[" + ", ".join(f"({nat(f)}, {nat(nu)})" for f, nu in rows) + "]"


def rational_literal(value):
    value = Fraction(value)
    return f"({value.numerator} / {value.denominator} : ℚ)"


def main():
    counts = read("curves/k343-place-counts-30.json")["place_counts"][:12]
    m2 = read("certificates/m2-frozen.json")
    mxx = read("certificates/mxx-theorem61.json")
    m2_places = [(f, nu) for f, nu, count in
                 zip(m2["degrees"], m2["nu"], m2["multiplicities"], strict=True)
                 for _ in range(nat(count))]
    mxx_places = [(row["degree"], row["exponent"]) for row in mxx["support"]
                  for _ in range(nat(row["count"]))]
    genus = nat(mxx["geometry"]["genus_k"])
    t = nat(mxx["splitting_places"])
    checks = [
        f"(List.range 12).map (fun i => genus343Inventory (fun _ => 0) (i+1)) = "
        f"{[nat(count) for count in counts]}",
        f"witness = {rows_literal(m2_places)}",
        f"mxxModulus = {rows_literal(mxx_places)}",
        f"score (normalize witness) 192 = {rational_literal(m2['bound'])}",
        f"score mxxSupport {t} = {rational_literal(mxx['same_support_on_k343'])}",
        f"{t} / (({genus} : ℚ) - 1 + cost mxxSupport) = {rational_literal(mxx['bound'])}",
        f"towerPolynomial mxxSupport {t} {rational_literal(mxx['tau'])} = "
        f"{rational_literal(mxx['P(tau)'])}",
    ]
    header = "import IharaM3\nopen IharaM3\n"
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "CertificateInputs.lean"
        target.write_text(header + "".join(f"example : {c} := by decide +kernel\n" for c in checks),
                          encoding="utf-8")
        subprocess.run(["lake", "env", "lean", str(target)], cwd=FORMAL, check=True)
    print(f"{len(checks)} Lean checks passed against the archived inputs.")


if __name__ == "__main__":
    main()
