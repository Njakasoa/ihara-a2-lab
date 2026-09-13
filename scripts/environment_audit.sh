#!/usr/bin/env bash
set -u -o pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
RUNTIME_ROOT=${IHARA_RUNTIME_ROOT:-"$ROOT/.runtime"}
SAGE_PREFIX=${SAGE_PREFIX:-"$RUNTIME_ROOT/sage"}
DOT_SAGE=${DOT_SAGE:-"$RUNTIME_ROOT/sage-home"}
PARI_PREFIX=${PARI_PREFIX:-"$RUNTIME_ROOT/pari"}
MAMBA_ROOT_PREFIX=${MAMBA_ROOT_PREFIX:-"$RUNTIME_ROOT/mamba"}
MAMBA_BIN=${MAMBA_BIN:-"$RUNTIME_ROOT/micromamba/bin/micromamba"}
SAGE_PYTHON="$SAGE_PREFIX/bin/python"
FAILURES=0

printf '%s\n' "IHARA_ENVIRONMENT_AUDIT=2026-09-13"
printf '%s\n' "ROOT=$ROOT"
printf '%s\n' "PLATFORM=$(uname -srm 2>/dev/null || true)"

show_external() {
    local label=$1 name=$2 path
    shift 2
    if path=$(command -v "$name" 2>/dev/null); then
        printf '%s=AVAILABLE path=%s\n' "$label" "$path"
        "$path" "$@" 2>&1 | sed -n '1,3p'
    else
        printf '%s=UNAVAILABLE\n' "$label"
    fi
}

show_external PYTHON_SYSTEM python3 --version
show_external SAGE_SYSTEM sage --version
show_external PARI_SYSTEM gp --version
show_external FLINT_CONFIG flint-config --version
show_external GAP_SYSTEM gap --version
show_external SINGULAR_SYSTEM Singular --version
show_external JULIA_SYSTEM julia --version
show_external GCC_SYSTEM gcc --version
show_external GXX_SYSTEM g++ --version
show_external GIT_SYSTEM git --version

if [[ -x "$MAMBA_BIN" ]]; then
    printf 'MICROMAMBA_LOCAL=AVAILABLE path=%s version=' "$MAMBA_BIN"
    "$MAMBA_BIN" --version 2>&1 | sed -n '1p'
else
    printf '%s\n' 'MICROMAMBA_LOCAL=UNAVAILABLE'
fi

if [[ -x "$SAGE_PREFIX/bin/sage" ]]; then
    printf 'SAGE_LOCAL=AVAILABLE prefix=%s version=' "$SAGE_PREFIX"
    DOT_SAGE="$DOT_SAGE" "$SAGE_PREFIX/bin/sage" --version 2>&1 | sed -n '1p'
    if [[ -x "$SAGE_PYTHON" ]]; then
        printf 'SAGE_PYTHON='; "$SAGE_PYTHON" --version 2>&1 | sed -n '1p'
    fi
    for tool in gp-2.17 gap Singular; do
        if [[ -x "$SAGE_PREFIX/bin/$tool" ]]; then
            printf 'SAGE_BUNDLED_%s=AVAILABLE path=%s\n' "$tool" "$SAGE_PREFIX/bin/$tool"
        else
            printf 'SAGE_BUNDLED_%s=UNAVAILABLE\n' "$tool"
        fi
    done
    if compgen -G "$SAGE_PREFIX/lib/libflint.so*" >/dev/null; then
        printf '%s\n' 'SAGE_FLINT_LIBRARY=AVAILABLE'
    else
        printf '%s\n' 'SAGE_FLINT_LIBRARY=UNAVAILABLE'
    fi
else
    printf '%s\n' "SAGE_LOCAL=UNAVAILABLE expected=$SAGE_PREFIX/bin/sage"
fi

if [[ -x "$ROOT/scripts/gp-local" ]]; then
    printf 'PARI_LOCAL_WRAPPER=AVAILABLE path=%s\n' "$ROOT/scripts/gp-local"
elif [[ -x "$PARI_PREFIX/usr/bin/gp-2.15" ]]; then
    printf 'PARI_LOCAL=AVAILABLE prefix=%s\n' "$PARI_PREFIX"
else
    printf '%s\n' 'PARI_LOCAL=UNAVAILABLE'
fi

printf '%s\n' 'PYTHON_MODULES_SYSTEM='
if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY'
import importlib.util
for name in ('sage', 'cypari2', 'flint', 'sympy', 'numpy', 'scipy', 'galois'):
    print(f'{name}=' + ('AVAILABLE' if importlib.util.find_spec(name) else 'UNAVAILABLE'))
PY
fi

if [[ -x "$SAGE_PYTHON" ]]; then
    printf '%s\n' 'SAGE_SMOKE_BEGIN'
    if output=$(DOT_SAGE="$DOT_SAGE" PYTHONNOUSERSITE=1 "$SAGE_PYTHON" - <<'PY'
from sage.all import AA, GF, FunctionField, NumberField, PolynomialRing, QQ

# Finite fields and an exact algebraic root check.
F = GF(2**5, 'a')
a = F.gen()
assert F.cardinality() == 32
assert a.multiplicative_order() == 31
Paa = PolynomialRing(QQ, 'u')
u = Paa.gen()
roots = (u**2 - 2).roots(AA)
assert len(roots) == 2 and all(root**2 == 2 for root, _ in roots)
print('SAGE_FINITE_FIELD=PASS field_size=32 generator_order=31 algebraic_roots=PASS')

# Exact polynomial factorisation over QQ.
P = PolynomialRing(QQ, 'x')
x = P.gen()
f = x**6 - 1
fac = f.factor()
assert fac.prod() == f
print('SAGE_POLYNOMIAL_FACTOR=PASS factors=' + str(fac))

# Number-field class group (Q(sqrt(-23)) has class number 3).
K = NumberField(Paa.gen()**2 + 23, 'z')
assert K.class_number() == 3
assert K.class_group().order() == 3
print('SAGE_NUMBER_FIELD_CLASS_GROUP=PASS class_number=3')

# The base function field from proofs/FINITE_GEOMETRY.md.
F2 = GF(2)
F0 = FunctionField(F2, 'x')
x0 = F0.gen()
Py = F0['y']
y = Py.gen()
H = F0.extension(y**2 + (x0**3 + x0 + 1)*y + (x0**2 + x0), 'y')
assert H.genus() == 2
assert H.constant_field() == F2
assert len(H.places()) == 6
# ``class_group`` is the affine maximal-order S-ideal class group.  Report it
# separately from Pic^0(H)(F2), represented by the complete Jacobian below.
affine_S_class_group = H.class_group()
assert affine_S_class_group.order() == 1
J = H.jacobian(model='hess')
jacobian_group = J.group()
assert jacobian_group.order(algorithm='algebraic') == 19
Pinf = H.places_infinite()[0]
D = Pinf.divisor(4)
assert D.degree() == 4 and D.dimension() == 3
assert len(D.basis_function_space()) == 3
print('SAGE_FUNCTION_FIELD=PASS genus=2 constant_field=F2 degree1_places=6')
print('SAGE_AFFINE_S_CLASS_GROUP=PASS order=1')
print('SAGE_JACOBIAN=PASS order=19')
print('SAGE_RIEMANN_ROCH=PASS divisor_degree=4 l(D)=3')
PY
); then
        printf '%s\n' "$output"
    else
        status=$?
        printf '%s\n' "$output"
        printf 'SAGE_SMOKE=FAIL status=%s\n' "$status"
        FAILURES=1
    fi
    printf '%s\n' 'SAGE_SMOKE_END'
else
    printf '%s\n' 'SAGE_SMOKE=UNTESTED (Sage prefix absent)'
fi

GP_CMD=()
if [[ -x "$SAGE_PREFIX/bin/gp-2.17" ]]; then
    GP_CMD=("$SAGE_PREFIX/bin/gp-2.17")
elif [[ -x "$ROOT/scripts/gp-local" ]]; then
    GP_CMD=("$ROOT/scripts/gp-local")
elif command -v gp >/dev/null 2>&1; then
    GP_CMD=("$(command -v gp)")
fi

if ((${#GP_CMD[@]})); then
    printf '%s\n' "PARI_SMOKE_BEGIN command=${GP_CMD[*]}"
    if output=$("${GP_CMD[@]}" -q 2>&1 <<'GP'
F = ffgen(2^5);
g = ffprimroot(F);
if (fforder(g) != 31, error("finite-field primitive-root check failed"));
print("PARI_FINITE_FIELD=PASS field_size=32 primitive_order=31");
if (factor(2^31-1)[1,1] != 2147483647, error("integer factor check failed"));
print("PARI_INTEGER_FACTOR=PASS");
fac = factor(x^6-1);
if (prod(i=1,#fac[,1],fac[i,1]^fac[i,2]) != x^6-1, error("polynomial factor check failed"));
print("PARI_POLYNOMIAL_FACTOR=PASS");
bnf = bnfinit(x^2+23);
if (bnf.no != 3, error("class-number check failed"));
print("PARI_NUMBER_FIELD_CLASS_GROUP=PASS class_number=3");
print("PARI_RIEMANN_ROCH=UNTESTED (GP has no project function-field RR API)");
quit;
GP
); then
        printf '%s\n' "$output"
    else
        status=$?
        printf '%s\n' "$output"
        printf 'PARI_SMOKE=FAIL status=%s\n' "$status"
        FAILURES=1
    fi
    printf '%s\n' 'PARI_SMOKE_END'
else
    printf '%s\n' 'PARI_SMOKE=UNTESTED (PARI/GP absent)'
fi

if [[ -x "$SAGE_PREFIX/bin/julia" ]]; then
    printf '%s\n' 'JULIA_NEMO_HECKE=UNTESTED (Julia executable present; package probe not configured)'
else
    printf '%s\n' 'JULIA_NEMO_HECKE=UNAVAILABLE (no Julia executable)'
fi

printf 'AUDIT_FAILURES=%s\n' "$FAILURES"
exit "$FAILURES"
