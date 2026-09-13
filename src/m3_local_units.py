"""Exact local principal-unit arithmetic in characteristic two.

This module records the local information needed before a nonuniform
conductor search is meaningful.  If ``P`` has degree ``f`` over ``F_2`` and
``nu >= 1``, write

``G(f, nu) = U_P^(1) / U_P^(nu)``.

The formulas below use ``q = 2**f``.  They distinguish the full finite
abelian 2-group ``G(f, nu)`` from its elementary (exponent-two) quotient,
whose dual is the set of Artin--Schreier characters.  The latter is much
smaller when ``nu > 2``.

For an independent arithmetic check, :func:`enumerate_truncated_units`
enumerates ``1 + a_1*pi + ... + a_(nu-1)*pi^(nu-1)`` directly and performs
truncated-series multiplication over a deterministically constructed binary
finite field.  Enumeration is deliberately bounded by 4096 elements and is
never used by the production formulas.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable, Mapping, Sequence


MAX_ENUMERATED_GROUP_ORDER = 4096


def _integer(value: object, name: str) -> int:
    """Accept a genuine integer, rejecting booleans and lossy coercions."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _validate_parameters(f: object, nu: object) -> tuple[int, int]:
    f_value = _integer(f, "f")
    nu_value = _integer(nu, "nu")
    if f_value <= 0:
        raise ValueError("f must be positive")
    if nu_value <= 0:
        raise ValueError("nu must be positive")
    return f_value, nu_value


def _ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def _ceil_log2(value: int) -> int:
    if value <= 1:
        return 0
    return (value - 1).bit_length()


def _poly_mul(left: int, right: int) -> int:
    """Multiply binary polynomials represented by coefficient bit masks."""

    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
    return result


def _poly_mod(value: int, modulus: int) -> int:
    """Reduce a binary polynomial modulo a monic binary polynomial."""

    if modulus <= 0:
        raise ValueError("a polynomial modulus must be positive")
    modulus_degree = modulus.bit_length() - 1
    while value and value.bit_length() - 1 >= modulus_degree:
        value ^= modulus << (value.bit_length() - 1 - modulus_degree)
    return value


def _poly_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, _poly_mod(left, right)
    return left


def _poly_pow_mod(base: int, exponent: int, modulus: int) -> int:
    result = 1
    base = _poly_mod(base, modulus)
    while exponent:
        if exponent & 1:
            result = _poly_mod(_poly_mul(result, base), modulus)
        base = _poly_mod(_poly_mul(base, base), modulus)
        exponent >>= 1
    return result


def _prime_divisors(value: int) -> tuple[int, ...]:
    divisors: list[int] = []
    candidate = 2
    remainder = value
    while candidate * candidate <= remainder:
        if remainder % candidate == 0:
            divisors.append(candidate)
            while remainder % candidate == 0:
                remainder //= candidate
        candidate += 1
    if remainder > 1:
        divisors.append(remainder)
    return tuple(divisors)


def _is_irreducible_binary_polynomial(modulus: int, degree: int) -> bool:
    """Rabin's exact irreducibility test for a monic binary polynomial."""

    if modulus.bit_length() - 1 != degree or not (modulus & 1):
        return False
    x = 2
    x_mod = _poly_mod(x, modulus)
    if _poly_pow_mod(x, 1 << degree, modulus) != x_mod:
        return False
    for prime in _prime_divisors(degree):
        test = _poly_pow_mod(x, 1 << (degree // prime), modulus) ^ x_mod
        if _poly_gcd(test, modulus) != 1:
            return False
    return True


def irreducible_binary_polynomial(degree: int) -> int:
    """Return a deterministic monic irreducible polynomial of ``degree``.

    The integer is a coefficient bit mask, with bit ``i`` representing
    ``X**i``.  The small exact enumeration gate only needs degrees whose
    resulting group has at most 4096 elements, but this routine is valid for
    any positive degree for which the search is practical.
    """

    degree = _integer(degree, "degree")
    if degree <= 0:
        raise ValueError("degree must be positive")
    leading = 1 << degree
    # A reducible polynomial with constant coefficient zero is excluded.  The
    # odd tails are visited in ascending order to make artifacts reproducible.
    for tail in range(1, leading, 2):
        candidate = leading | tail
        if _is_irreducible_binary_polynomial(candidate, degree):
            return candidate
    # A binary irreducible polynomial exists in every positive degree.  This
    # branch is defensive and should be unreachable.
    raise ArithmeticError(f"failed to find an irreducible polynomial of degree {degree}")


@dataclass(frozen=True)
class BinaryField:
    """The field ``F_(2**f)`` represented by polynomial coefficient masks."""

    degree: int
    modulus: int

    def __post_init__(self) -> None:
        degree = _integer(self.degree, "degree")
        modulus = _integer(self.modulus, "modulus")
        if degree <= 0:
            raise ValueError("field degree must be positive")
        if modulus.bit_length() - 1 != degree or not (modulus & 1):
            raise ValueError("modulus must be monic of the requested degree with nonzero constant")
        if not _is_irreducible_binary_polynomial(modulus, degree):
            raise ValueError("modulus must be irreducible over F_2")

    @property
    def q(self) -> int:
        return 1 << self.degree

    def add(self, left: int, right: int) -> int:
        self._check_element(left)
        self._check_element(right)
        return left ^ right

    def mul(self, left: int, right: int) -> int:
        self._check_element(left)
        self._check_element(right)
        return _poly_mod(_poly_mul(left, right), self.modulus)

    def power(self, value: int, exponent: int) -> int:
        self._check_element(value)
        exponent = _integer(exponent, "exponent")
        if exponent < 0:
            raise ValueError("exponent must be nonnegative")
        result = 1
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exponent >>= 1
        return result

    def _check_element(self, value: object) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("field elements must be integers")
        if value < 0 or value >= self.q:
            raise ValueError("field element is outside the field")


def binary_field(f: int) -> BinaryField:
    """Construct the deterministic binary field used by the direct checker."""

    f, _ = _validate_parameters(f, 1)
    return BinaryField(f, irreducible_binary_polynomial(f))


def local_unit_order(f: int, nu: int) -> int:
    """Return ``|U^1/U^nu| = (2**f)**(nu-1)`` exactly."""

    f, nu = _validate_parameters(f, nu)
    return (1 << f) ** (nu - 1)


def local_unit_log2_order(f: int, nu: int) -> int:
    """Return the binary logarithm of the local unit-group order."""

    f, nu = _validate_parameters(f, nu)
    return f * (nu - 1)


def local_unit_layer_dimensions(f: int, nu: int) -> tuple[int, ...]:
    """Dimensions of successive ``2^r``-killed layers of the group.

    The entry at index ``r-1`` is

    ``log_2 |G[2^r]/G[2^(r-1)]|``

    and equals the number of cyclic factors whose order is at least ``2^r``.
    It is different from the dimensions of the valuation filtration, which
    are simply ``f`` at each of the ``nu-1`` successive unit layers.
    """

    f, nu = _validate_parameters(f, nu)
    exponent = _ceil_log2(nu)
    return tuple(
        f * (
            _ceil_div(nu, 1 << (r - 1))
            - _ceil_div(nu, 1 << r)
        )
        for r in range(1, exponent + 1)
    )


def valuation_layer_dimensions(f: int, nu: int) -> tuple[int, ...]:
    """Dimensions of ``U^r/U^(r+1)`` for ``1 <= r < nu``."""

    f, nu = _validate_parameters(f, nu)
    return (f,) * (nu - 1)


def local_unit_cyclic_factors(f: int, nu: int) -> dict[int, int]:
    """Return cyclic-factor multiplicities ``{e: m_e}`` for ``C_(2**e)``.

    If ``d_r`` is :func:`local_unit_layer_dimensions`, then
    ``m_e=d_e-d_(e+1)``.  Equivalently,

    ``m_e = f*(ceil(nu/2^(e-1)) - 2*ceil(nu/2^e)
              + ceil(nu/2^(e+1)))``.
    """

    f, nu = _validate_parameters(f, nu)
    layers = local_unit_layer_dimensions(f, nu)
    factors: dict[int, int] = {}
    for index, dimension in enumerate(layers):
        next_dimension = layers[index + 1] if index + 1 < len(layers) else 0
        multiplicity = dimension - next_dimension
        if multiplicity:
            factors[index + 1] = multiplicity
    return factors


def local_unit_p_rank(f: int, nu: int) -> int:
    """Return the 2-rank ``dim_F2(G/2G)=f*floor(nu/2)``."""

    f, nu = _validate_parameters(f, nu)
    return f * (nu // 2)


def local_unit_exponent(f: int, nu: int) -> int:
    """Return the largest element order in ``U^1/U^nu``."""

    _, nu = _validate_parameters(f, nu)
    return 1 << _ceil_log2(nu)


def _difference(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(values[index] - values[index - 1]
                 for index in range(1, len(values)))


def full_character_cumulative_counts(f: int, nu: int) -> tuple[int, ...]:
    """Counts of all local 2-power characters with conductor at most ``r``.

    The tuple is indexed by ``r=0,...,nu``.  The first two entries are both
    one: a wild 2-primary character has no conductor-one (tame) jump.  For
    ``r >= 2`` the exact count is ``q**(r-1)``.
    """

    f, nu = _validate_parameters(f, nu)
    q = 1 << f
    counts = [1]
    if nu >= 1:
        counts.append(1)
    counts.extend(q ** (r - 1) for r in range(2, nu + 1))
    return tuple(counts)


def full_character_exact_counts(f: int, nu: int) -> tuple[int, ...]:
    """Counts of all local characters having each exact conductor exponent."""

    return _difference((0,) + full_character_cumulative_counts(f, nu))


def full_character_average_conductor(f: int, nu: int) -> Fraction:
    """Exact average conductor over all ``|G|`` characters of ``G``."""

    counts = full_character_exact_counts(f, nu)
    order = local_unit_order(f, nu)
    return Fraction(sum(index * count for index, count in enumerate(counts)), order)


def full_character_filtration_formula(f: int, nu: int) -> Fraction:
    """The same average in the tail-sum form used in the conductor proof."""

    f, nu = _validate_parameters(f, nu)
    if nu == 1:
        return Fraction(0)
    q = 1 << f
    result = Fraction(nu, 1) - Fraction(2, q ** (nu - 1))
    for j in range(1, nu - 1):
        result -= Fraction(1, q ** j)
    return result


def exponent_two_character_cumulative_counts(f: int, nu: int) -> tuple[int, ...]:
    """Counts of order-dividing-two characters with conductor at most ``r``.

    These are the characters of the elementary quotient ``G/2G``.  The
    cumulative count is ``q**floor(r/2)``.  Thus all nontrivial jumps are at
    even exponents, as required for Artin--Schreier characters in
    characteristic two.
    """

    f, nu = _validate_parameters(f, nu)
    q = 1 << f
    return tuple(q ** (r // 2) for r in range(nu + 1))


def exponent_two_character_exact_counts(f: int, nu: int) -> tuple[int, ...]:
    """Counts of order-dividing-two characters at each exact conductor."""

    return _difference((0,) + exponent_two_character_cumulative_counts(f, nu))


def exponent_two_character_average_conductor(f: int, nu: int) -> Fraction:
    """Exact average conductor over the exponent-two character quotient."""

    counts = exponent_two_character_exact_counts(f, nu)
    order = 1 << local_unit_p_rank(f, nu)
    return Fraction(sum(index * count for index, count in enumerate(counts)), order)


def local_rebate(f: int, nu: int) -> Fraction:
    """Return ``A_P - f*E[a_P]/2`` for the full local character law."""

    f, nu = _validate_parameters(f, nu)
    return Fraction(local_unit_p_rank(f, nu), 1) - Fraction(
        f, 2
    ) * full_character_average_conductor(f, nu)


def duursma_mak_local_terms(f: int, nu: int) -> dict[str, int]:
    """Return the local ``A``, relation ``b`` and ``C`` terms of Theorem 1.1.

    The ``A`` term is the exact local 2-rank supplied by the unit quotient.
    The relation term ``C=b(b+1)`` is the theorem's local upper-bound
    contribution, with ``b=f*(nu-1)``.  It is deliberately labelled as a
    theorem contribution rather than an assertion that the global ray group
    attains either bound.
    """

    f, nu = _validate_parameters(f, nu)
    a_term = local_unit_p_rank(f, nu)
    b_term = f * (nu - 1)
    return {
        "A": a_term,
        "a_local": a_term,
        "b": b_term,
        "C": b_term * (b_term + 1),
        "c_local_bound": b_term * (b_term + 1),
    }


@dataclass(frozen=True)
class LocalUnitStructure:
    """JSON-friendly exact summary of one local unit quotient."""

    f: int
    q: int
    nu: int
    order: int
    log2_order: int
    p_rank: int
    exponent: int
    valuation_layers: tuple[int, ...]
    killed_layers: tuple[int, ...]
    cyclic_factors: tuple[tuple[int, int], ...]
    full_character_cumulative: tuple[int, ...]
    full_character_exact: tuple[int, ...]
    full_average_conductor: Fraction
    exponent_two_order: int
    exponent_two_rank: int
    exponent_two_character_cumulative: tuple[int, ...]
    exponent_two_character_exact: tuple[int, ...]
    exponent_two_average_conductor: Fraction
    local_rebate: Fraction
    theorem_terms: tuple[tuple[str, int], ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "f": self.f,
            "q": self.q,
            "nu": self.nu,
            "order": self.order,
            "log2_order": self.log2_order,
            "p_rank": self.p_rank,
            "exponent": self.exponent,
            "valuation_layers": list(self.valuation_layers),
            "killed_layers": list(self.killed_layers),
            "cyclic_factors": {
                str(exponent): multiplicity
                for exponent, multiplicity in self.cyclic_factors
            },
            "full_character_cumulative": list(self.full_character_cumulative),
            "full_character_exact": list(self.full_character_exact),
            "full_average_conductor": str(self.full_average_conductor),
            "exponent_two_order": self.exponent_two_order,
            "exponent_two_rank": self.exponent_two_rank,
            "exponent_two_character_cumulative": list(
                self.exponent_two_character_cumulative
            ),
            "exponent_two_character_exact": list(
                self.exponent_two_character_exact
            ),
            "exponent_two_average_conductor": str(
                self.exponent_two_average_conductor
            ),
            "local_rebate": str(self.local_rebate),
            "theorem_terms": dict(self.theorem_terms),
        }

    def __getitem__(self, key: str) -> object:
        """Permit convenient mapping-style access in small audits."""

        return self.as_dict()[key]


def local_unit_structure(f: int, nu: int) -> LocalUnitStructure:
    """Build the exact closed-form local structure summary."""

    f, nu = _validate_parameters(f, nu)
    factors = local_unit_cyclic_factors(f, nu)
    terms = duursma_mak_local_terms(f, nu)
    return LocalUnitStructure(
        f=f,
        q=1 << f,
        nu=nu,
        order=local_unit_order(f, nu),
        log2_order=local_unit_log2_order(f, nu),
        p_rank=local_unit_p_rank(f, nu),
        exponent=local_unit_exponent(f, nu),
        valuation_layers=valuation_layer_dimensions(f, nu),
        killed_layers=local_unit_layer_dimensions(f, nu),
        cyclic_factors=tuple(sorted(factors.items())),
        full_character_cumulative=full_character_cumulative_counts(f, nu),
        full_character_exact=full_character_exact_counts(f, nu),
        full_average_conductor=full_character_average_conductor(f, nu),
        exponent_two_order=1 << local_unit_p_rank(f, nu),
        exponent_two_rank=local_unit_p_rank(f, nu),
        exponent_two_character_cumulative=(
            exponent_two_character_cumulative_counts(f, nu)
        ),
        exponent_two_character_exact=exponent_two_character_exact_counts(f, nu),
        exponent_two_average_conductor=(
            exponent_two_character_average_conductor(f, nu)
        ),
        local_rebate=local_rebate(f, nu),
        theorem_terms=tuple(sorted(terms.items())),
    )


def local_character_laws(f: int, nu: int) -> dict[str, object]:
    """Return both full and order-two local conductor laws."""

    structure = local_unit_structure(f, nu)
    return {
        "f": structure.f,
        "q": structure.q,
        "nu": structure.nu,
        "full": {
            "cumulative": list(structure.full_character_cumulative),
            "exact": list(structure.full_character_exact),
            "average_conductor": str(structure.full_average_conductor),
        },
        "artin_schreier": {
            "cumulative": list(structure.exponent_two_character_cumulative),
            "exact": list(structure.exponent_two_character_exact),
            "average_conductor": str(
                structure.exponent_two_average_conductor
            ),
        },
    }


def _coerce_coefficients(
    coefficients: Iterable[object], nu: int, field: BinaryField
) -> tuple[int, ...]:
    try:
        values = tuple(coefficients)
    except TypeError as exc:
        raise ValueError("series coefficients must be a sequence") from exc
    if len(values) != nu - 1:
        raise ValueError(f"a truncated unit needs exactly {nu - 1} coefficients")
    result: list[int] = []
    for index, value in enumerate(values, start=1):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"coefficient {index} must be an integer field element")
        field._check_element(value)
        result.append(value)
    return tuple(result)


def multiply_truncated_units(
    left: Iterable[object],
    right: Iterable[object],
    f: int,
    nu: int,
    *,
    field: BinaryField | None = None,
) -> tuple[int, ...]:
    """Multiply two truncated principal units by direct convolution.

    A coefficient tuple ``(a_1,...,a_(nu-1))`` denotes
    ``1 + sum(a_i*pi**i)`` modulo ``pi**nu``.  The constant coefficient is
    omitted.  No group-structure formula is used here.
    """

    f, nu = _validate_parameters(f, nu)
    if field is None:
        field = binary_field(f)
    elif field.degree != f:
        raise ValueError("the supplied field has the wrong degree")
    left_values = _coerce_coefficients(left, nu, field)
    right_values = _coerce_coefficients(right, nu, field)
    coefficients = [left_value ^ right_value
                    for left_value, right_value in zip(left_values, right_values)]
    # The coefficient at pi**j receives a_i*b_(j-i), 1 <= i < j.
    for j in range(2, nu):
        value = coefficients[j - 1]
        for i in range(1, j):
            value ^= field.mul(left_values[i - 1], right_values[j - i - 1])
        coefficients[j - 1] = value
    return tuple(coefficients)


def truncated_unit_elements(
    f: int, nu: int, *, cap: int = MAX_ENUMERATED_GROUP_ORDER
) -> tuple[tuple[int, ...], ...]:
    """Enumerate all coefficient tuples for ``U^1/U^nu`` under a hard cap."""

    f, nu = _validate_parameters(f, nu)
    cap = _integer(cap, "cap")
    if cap <= 0:
        raise ValueError("cap must be positive")
    order = local_unit_order(f, nu)
    if order > cap:
        raise ValueError(
            f"direct enumeration has {order} elements, exceeding cap {cap}"
        )
    q = 1 << f
    return tuple(product(range(q), repeat=nu - 1))


def _series_power_order(
    element: tuple[int, ...], identity: tuple[int, ...],
    multiply,
) -> int:
    current = identity
    order = 0
    while True:
        order += 1
        current = multiply(current, element)
        if current == identity:
            return order
        # A finite quotient of units here has exponent at most the least
        # power of two >= nu.  This guard catches an arithmetic bug rather
        # than looping forever if the direct multiplier is ever changed.
        if order > 1 << 20:
            raise ArithmeticError("failed to find a finite truncated-unit order")


def _powers_of_two_profile(order_profile: Mapping[int, int]) -> tuple[int, ...]:
    profile: list[int] = []
    for order, count in sorted(order_profile.items()):
        if order <= 0 or order & (order - 1):
            raise ArithmeticError("truncated-unit order is not a power of two")
        while len(profile) <= order.bit_length() - 1:
            profile.append(0)
        profile[order.bit_length() - 1] = count
    return tuple(profile)


def _square_coset_image(
    subgroup: Sequence[tuple[int, ...]],
    squares: Sequence[tuple[int, ...]],
    multiply,
) -> set[tuple[int, ...]]:
    return {
        multiply(element, square)
        for element in subgroup
        for square in squares
    }


def enumerate_truncated_units(
    f: int,
    nu: int,
    *,
    cap: int = MAX_ENUMERATED_GROUP_ORDER,
    include_elements: bool = False,
) -> dict[str, object]:
    """Directly enumerate a small truncated local unit group.

    The returned cumulative character counts are obtained from finite-group
    annihilator sizes after direct enumeration of ``U^r/U^nu`` and the square
    subgroup.  This checks both the full character law and the order-two
    (Artin--Schreier) law without importing their closed-form expressions.
    """

    f, nu = _validate_parameters(f, nu)
    cap = _integer(cap, "cap")
    elements = truncated_unit_elements(f, nu, cap=cap)
    field = binary_field(f)
    identity = (0,) * (nu - 1)

    def multiply(left: Iterable[object], right: Iterable[object]) -> tuple[int, ...]:
        return multiply_truncated_units(left, right, f, nu, field=field)

    orders = Counter(
        _series_power_order(element, identity, multiply)
        for element in elements
    )
    if sum(orders.values()) != len(elements):
        raise ArithmeticError("direct order profile does not cover the group")
    if any(order & (order - 1) for order in orders):
        raise ArithmeticError("direct order profile contains a non-2-power order")

    squares = tuple(sorted({multiply(element, element) for element in elements}))
    if not squares or identity not in squares:
        raise ArithmeticError("squares do not form a subgroup containing identity")

    filtration_sizes: list[int] = []
    full_cumulative: list[int] = [1]
    exponent_two_cumulative: list[int] = [1]
    for r in range(1, nu + 1):
        subgroup = tuple(
            element for element in elements
            if all(value == 0 for value in element[: r - 1])
        )
        filtration_sizes.append(len(subgroup))
        full_cumulative.append(len(elements) // len(subgroup))
        image = _square_coset_image(subgroup, squares, multiply)
        exponent_two_cumulative.append(len(elements) // len(image))

    order = len(elements)
    exponent_two_order = order // len(squares)
    if exponent_two_order & (exponent_two_order - 1):
        raise ArithmeticError("square quotient does not have 2-power order")
    exponent_two_rank = exponent_two_order.bit_length() - 1

    full_exact = _difference((0,) + tuple(full_cumulative))
    exponent_two_exact = _difference((0,) + tuple(exponent_two_cumulative))
    result: dict[str, object] = {
        "f": f,
        "q": 1 << f,
        "nu": nu,
        "field_modulus": field.modulus,
        "group_order": order,
        "elements_count": len(elements),
        "order_profile": {
            str(order_value): count
            for order_value, count in sorted(orders.items())
        },
        "square_subgroup_order": len(squares),
        "exponent_two_quotient_order": exponent_two_order,
        "exponent_two_rank": exponent_two_rank,
        "filtration_sizes": filtration_sizes,
        "full_character_cumulative_direct": full_cumulative,
        "full_character_exact_direct": list(full_exact),
        "exponent_two_character_cumulative_direct": exponent_two_cumulative,
        "exponent_two_character_exact_direct": list(exponent_two_exact),
        "full_average_conductor_direct": str(
            Fraction(sum(index * count for index, count in enumerate(full_exact)), order)
        ),
        "exponent_two_average_conductor_direct": str(
            Fraction(
                sum(index * count for index, count in enumerate(exponent_two_exact)),
                exponent_two_order,
            )
        ),
        "cyclic_factors_direct": _cyclic_factors_from_order_profile(orders),
    }
    if include_elements:
        result["elements"] = [list(element) for element in elements]
    return result


def _cyclic_factors_from_order_profile(profile: Mapping[int, int]) -> dict[str, int]:
    """Recover cyclic-factor multiplicities from direct killed-element counts."""

    if not profile:
        raise ValueError("an order profile cannot be empty")
    max_exponent = max(order.bit_length() - 1 for order in profile)
    # ``G[2**0]`` consists of the identity, so its order is one.  Starting
    # from zero would make ``bit_length() - 1`` report ``-1`` and inflate the
    # first layer by one.
    killed = [1]
    for exponent in range(1, max_exponent + 1):
        killed.append(sum(
            count for order, count in profile.items()
            if order <= 1 << exponent
        ))
    dimensions = [
        (killed[exponent].bit_length() - 1)
        - (killed[exponent - 1].bit_length() - 1)
        for exponent in range(1, len(killed))
    ]
    factors: dict[str, int] = {}
    for exponent, dimension in enumerate(dimensions, start=1):
        next_dimension = dimensions[exponent] if exponent < len(dimensions) else 0
        if dimension - next_dimension:
            factors[str(exponent)] = dimension - next_dimension
    return factors


def verify_local_formula(
    f: int,
    nu: int,
    *,
    cap: int = MAX_ENUMERATED_GROUP_ORDER,
) -> dict[str, object]:
    """Compare closed formulas with the independent direct enumeration."""

    f, nu = _validate_parameters(f, nu)
    structure = local_unit_structure(f, nu)
    direct = enumerate_truncated_units(f, nu, cap=cap)
    expected_factors = {
        str(exponent): multiplicity
        for exponent, multiplicity in structure.cyclic_factors
    }
    checks = {
        "order": direct["group_order"] == structure.order,
        "order_profile_finite": sum(direct["order_profile"].values()) == structure.order,
        "p_rank": direct["exponent_two_rank"] == structure.p_rank,
        "exponent_two_order": direct["exponent_two_quotient_order"] == structure.exponent_two_order,
        "cyclic_factors": direct["cyclic_factors_direct"] == expected_factors,
        "valuation_layers": direct["filtration_sizes"] == [
            (1 << f) ** (nu - r) for r in range(1, nu + 1)
        ],
        "full_character_cumulative": direct["full_character_cumulative_direct"]
        == list(structure.full_character_cumulative),
        "full_character_exact": direct["full_character_exact_direct"]
        == list(structure.full_character_exact),
        "as_character_cumulative": direct[
            "exponent_two_character_cumulative_direct"
        ] == list(structure.exponent_two_character_cumulative),
        "as_character_exact": direct["exponent_two_character_exact_direct"]
        == list(structure.exponent_two_character_exact),
        "full_average": direct["full_average_conductor_direct"]
        == str(structure.full_average_conductor),
        "as_average": direct["exponent_two_average_conductor_direct"]
        == str(structure.exponent_two_average_conductor),
    }
    return {
        "f": f,
        "nu": nu,
        "passed": all(checks.values()),
        "checks": checks,
        "formula": structure.as_dict(),
        "direct": direct,
    }


def validate_structure_record(record: Mapping[str, object]) -> bool:
    """Reject a mutated or inconsistent serialized structure record.

    This small adversarial checker is useful for experiment artifacts: a
    changed degree, exponent, rank, or character count must not be accepted as
    if it were an exact local result.
    """

    try:
        f = _integer(record["f"], "f")
        nu = _integer(record["nu"], "nu")
        expected = local_unit_structure(f, nu).as_dict()
    except (KeyError, TypeError, ValueError):
        return False
    for key in (
        "q",
        "order",
        "log2_order",
        "p_rank",
        "exponent",
        "valuation_layers",
        "killed_layers",
        "cyclic_factors",
        "full_character_cumulative",
        "full_character_exact",
        "full_average_conductor",
        "exponent_two_order",
        "exponent_two_rank",
        "exponent_two_character_cumulative",
        "exponent_two_character_exact",
        "exponent_two_average_conductor",
        "local_rebate",
        "theorem_terms",
    ):
        if record.get(key) != expected.get(key):
            return False
    return True


# Short aliases keep the API discoverable for callers that use the terminology
# from the mission text.
unit_group_order = local_unit_order
unit_group_p_rank = local_unit_p_rank
unit_group_cyclic_factors = local_unit_cyclic_factors
unit_group_structure = local_unit_structure
unit_group_invariants = local_unit_structure
character_cumulative_counts = full_character_cumulative_counts
character_exact_counts = full_character_exact_counts
artin_schreier_cumulative_counts = exponent_two_character_cumulative_counts
artin_schreier_exact_counts = exponent_two_character_exact_counts
enumerate_local_units = enumerate_truncated_units


__all__ = [
    "MAX_ENUMERATED_GROUP_ORDER",
    "BinaryField",
    "LocalUnitStructure",
    "artin_schreier_cumulative_counts",
    "artin_schreier_exact_counts",
    "binary_field",
    "character_cumulative_counts",
    "character_exact_counts",
    "duursma_mak_local_terms",
    "enumerate_local_units",
    "enumerate_truncated_units",
    "exponent_two_character_average_conductor",
    "exponent_two_character_cumulative_counts",
    "exponent_two_character_exact_counts",
    "full_character_average_conductor",
    "full_character_cumulative_counts",
    "full_character_exact_counts",
    "full_character_filtration_formula",
    "irreducible_binary_polynomial",
    "local_character_laws",
    "local_rebate",
    "local_unit_cyclic_factors",
    "local_unit_exponent",
    "local_unit_layer_dimensions",
    "local_unit_log2_order",
    "local_unit_order",
    "local_unit_p_rank",
    "local_unit_structure",
    "multiply_truncated_units",
    "truncated_unit_elements",
    "unit_group_cyclic_factors",
    "unit_group_invariants",
    "unit_group_order",
    "unit_group_p_rank",
    "unit_group_structure",
    "validate_structure_record",
    "valuation_layer_dimensions",
    "verify_local_formula",
]
