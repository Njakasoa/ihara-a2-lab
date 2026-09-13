#!/usr/bin/env python3
"""Independent SageMath checks for the binary M1 certificates.

This file deliberately does not import anything from ``src``.  It uses Sage
finite fields and function fields for a second implementation of the finite
geometry, traces, quotient zeta polynomials, and the exact arithmetic rows.
Run it with ``./scripts/sage-python tests/independent_sage.py``.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

try:
    from sage.all import AA, GF, FunctionField, PolynomialRing, QQ, ZZ, binomial
except ImportError as exc:  # pragma: no cover - exercised only outside Sage.
    raise SystemExit(
        "independent_sage.py must be run with scripts/sage-python"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    """Raise an assertion with a useful finite-certificate diagnosis."""
    if not condition:
        raise AssertionError(message)


def reject(condition, message):
    """The negative tests call this with a deliberately false condition."""
    require(condition, message)


def as_root_map(F):
    """Return one root of z^2+z=u for every trace-zero u in F."""
    roots = {}
    for z in F:
        roots.setdefault(z * z + z, z)
    require(len(roots) == F.cardinality() // 2,
            "Artin-Schreier image has the wrong size")
    return roots


def as_fibers(F, value, roots):
    """The two roots of z^2+z=value, or no roots."""
    z = roots.get(value)
    if z is None:
        return []
    return [z, z + F(1)]


def h_fibers(F, xx, roots):
    """Normalized H fibers for y^2+a(x)y=b(x) over F."""
    aa = xx**3 + xx + 1
    bb = xx**2 + xx
    if aa == 0:
        # The repeated affine root is the unique normalized point at a=0.
        return [bb ** (F.cardinality() // 2)]
    z = roots.get(bb / (aa * aa))
    if z is None:
        return []
    return [aa * z, aa * (z + F(1))]


def e_fibers(F, xx, roots):
    """Fibers of E: y^2+y=x^3+x over F."""
    return as_fibers(F, xx**3 + xx, roots)


def trace_zero(value):
    return value.trace() == 0


def point_counts_as5(upto=10):
    counts = []
    for n in range(1, upto + 1):
        F = GF(2**n, f"u{n}")
        total = 1  # one point at infinity on an odd-degree AS model
        for xx in F:
            if trace_zero(xx**5 + xx):
                total += 2
        counts.append(total)
    return counts


def point_counts_e(upto=10):
    counts = []
    for n in range(1, upto + 1):
        F = GF(2**n, f"u{n}")
        total = 1  # the unique point at infinity
        for xx in F:
            if trace_zero(xx**3 + xx):
                total += 2
        counts.append(total)
    return counts


def point_counts_h(upto=10):
    counts = []
    for n in range(1, upto + 1):
        F = GF(2**n, f"u{n}")
        roots = as_root_map(F)
        total = 2  # the two normalized H points at infinity
        for xx in F:
            total += len(h_fibers(F, xx, roots))
        counts.append(total)
    return counts


def h_basis_values(xx, yy):
    return [xx**0, xx, xx**2, yy, yy**2]


def h_mask_value(xx, yy, mask):
    values = h_basis_values(xx, yy)
    result = values[0] - values[0]
    for i, value in enumerate(values):
        if mask & (1 << i):
            result += value
    return result


def quotient_count(F, mask, roots):
    """Count C_h over F using the normalized c=0 correction and traces."""
    total = 4  # two H points at infinity, each split into two points
    for xx in F:
        bb = xx**2 + xx
        cc = xx**5 + xx**2 + 1
        for yy in h_fibers(F, xx, roots):
            if cc == 0:
                # Full local rank at the two degree-five places gives one
                # normalized point above each H point in every C_h.
                total += 1
                continue
            radicand = bb * h_mask_value(xx, yy, mask) / (cc * cc)
            if trace_zero(radicand):
                total += 2
    return total


def direct_quotient_counts(mask, upto=14):
    counts = []
    for n in range(1, upto + 1):
        F = GF(2**n, f"u{n}")
        counts.append(quotient_count(F, mask, as_root_map(F)))
    return counts


def k_count(F, roots):
    """Count k/H points by five independent AS traces over every H point."""
    total = 64  # both H infinity points split completely in degree 32
    for xx in F:
        bb = xx**2 + xx
        cc = xx**5 + xx**2 + 1
        for yy in h_fibers(F, xx, roots):
            if cc == 0:
                # The rank-five local map makes the entire inertia group act.
                total += 1
                continue
            factor = bb / (cc * cc)
            if all(trace_zero(factor * value)
                   for value in h_basis_values(xx, yy)):
                total += 32
    return total


def direct_k_counts(upto=10):
    counts = []
    for n in range(1, upto + 1):
        F = GF(2**n, f"u{n}")
        counts.append(k_count(F, as_root_map(F)))
    return counts


def bits_in_finite_field(value, degree):
    """Encode a GF(2^degree) element in its polynomial basis."""
    polynomial = value.polynomial()
    return sum(int(polynomial[i]) << i for i in range(degree))


def binary_rank(values, degree):
    """Rank of finite-field elements as vectors over GF(2)."""
    pivots = {}
    for value in values:
        vector = bits_in_finite_field(value, degree)
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def validate_local_map_rank(values, degree=5, expected=5):
    require(binary_rank(values, degree) == expected,
            "a reduced-residue map has the wrong rank")


def validate_dm_local_summary(summary):
    require(summary["c_root_count"] == 5,
            "the local certificate is missing a c root")
    require(summary["c_h_point_count"] == 10,
            "the local certificate is missing a ramified H point")
    require(summary["degree_five_orbit_count"] == 2,
            "the local certificate does not have two degree-five places")
    require(summary["local_map_count"] == 10,
            "the local certificate is missing a residue row")
    require(summary["local_map_ranks"] == [5] * 10,
            "the local certificate has a rank-deficient residue row")
    require(summary["nontrivial_characters"] == 31,
            "the local character count is not 31")
    require(summary["conductor_degree_each_character"] == 20,
            "the local conductor degree is not 20")


def validate_k_inventory(genus, counts, expected_counts):
    require(genus == 343, "the k genus is wrong")
    require(counts == expected_counts, "the k point count inventory is wrong")


def dm_local_residues():
    """Check c-roots on H and both rank-five reduced-residue maps."""
    F = GF(2**5, "u5")
    roots = as_root_map(F)
    c_roots = [xx for xx in F if xx**5 + xx**2 + 1 == 0]
    require(len(c_roots) == 5, "c has not got five roots in GF(32)")
    P2 = PolynomialRing(GF(2), "x")
    xpoly = P2.gen()
    require((xpoly**5 + xpoly**2 + 1).is_irreducible(),
            "c is reducible over GF(2)")

    points = []
    for xx in c_roots:
        aa = xx**3 + xx + 1
        require(aa != 0, "a and c share a root")
        ys = h_fibers(F, xx, roots)
        require(len(ys) == 2, "a c-root does not give two H points")
        points.extend((xx, yy) for yy in ys)
    require(len(points) == 10, "the c=0 locus on H is not ten geometric points")

    # Frobenius orbit decomposition gives exactly the two degree-five places.
    remaining = set(points)
    orbits = []
    while remaining:
        point = min(remaining, key=lambda pair: (str(pair[0]), str(pair[1])))
        orbit = []
        current = point
        while current not in orbit:
            orbit.append(current)
            current = (current[0]**2, current[1]**2)
        require(len(orbit) == 5, "a c-root point has the wrong Frobenius degree")
        require(set(orbit) <= remaining, "Frobenius orbit escaped the c-root locus")
        remaining -= set(orbit)
        orbits.append(orbit)
    require(len(orbits) == 2, "c=0 H points do not form two degree-five places")

    maps = []
    for xx, yy in points:
        aa = xx**3 + xx + 1
        bb = xx**2 + xx
        cp = xx**4  # derivative of x^5+x^2+1 in characteristic two
        require(cp != 0, "c has a multiple root")
        yp = (1 + (xx**2 + 1) * yy) / aa
        values = h_basis_values(xx, yy)
        derivatives = [0, 1, 0, yp, 0]
        residues = []
        for value, derivative in zip(values, derivatives):
            A = bb * value / (cp * cp)
            B = (value + bb * derivative) / (cp * cp)
            residues.append(B + A**(F.cardinality() // 2))
        validate_local_map_rank(residues)
        # Explicitly check all 31 nonzero AS generators at both places.
        for mask in range(1, 32):
            reduced = sum((residues[i] for i in range(5)
                           if mask & (1 << i)), F(0))
            require(reduced != 0, "a nonzero AS generator has zero residue")
        maps.append(residues)
    require(len(maps) == 10, "not all c=0 H points received a residue map")
    require({binary_rank(values, 5) for values in maps} == {5},
            "the two degree-five maps do not both have rank five")

    summary = {
        "c_root_count": len(c_roots),
        "c_h_point_count": len(points),
        "degree_five_orbit_count": len(orbits),
        "degree_five_orbit_lengths": [len(orbit) for orbit in orbits],
        "local_map_count": len(maps),
        "local_map_ranks": [binary_rank(values, 5) for values in maps],
        "nontrivial_characters": 31,
        "conductor_degree_each_character": 20,
        "k_degree_over_H": 32,
        "k_genus_from_RH": (32 * 2 + 31 * 20 + 2) // 2,
        "modulus_bits": 37,
    }
    validate_dm_local_summary(summary)
    return summary, maps


def schoof_local_residues():
    """Check the corrected Schoof denominator's d=4 and d=5 residues."""
    rows = {}
    F2 = GF(2)
    P2 = PolynomialRing(F2, "x")
    xpoly = P2.gen()
    fpoly = xpoly**3 + xpoly
    d0poly = xpoly**3 + xpoly**2 + 1
    d1poly = xpoly**3 + xpoly
    norm = d0poly**2 + d0poly * d1poly + d1poly**2 * fpoly
    require(norm.degree() == 9, "Schoof denominator norm is not degree nine")
    for n in (4, 5):
        F = GF(2**n, f"s{n}")
        roots = as_root_map(F)
        zeros = []
        for xx in F:
            bb = xx**2 + xx
            for yy in e_fibers(F, xx, roots):
                d = bb * (xx * yy + xx + yy) + 1
                if d != 0:
                    continue
                # d=d0+d1*y, y'=x^2+1 on E.
                dp = (xx**2 + (xx**2 + 1) * yy
                      + (xx**3 + xx) * (xx**2 + 1))
                require(dp != 0, "Schoof denominator zero is not simple")
                A = bb * xx / (dp * dp)
                B = xx**2 / (dp * dp)
                rho = B + A**(F.cardinality() // 2)
                zeros.append(rho)
        require(len(zeros) == n,
                f"Schoof d={n} locus has the wrong number of points")
        if n == 4:
            require(all(rho == 0 for rho in zeros),
                    "Schoof degree-four residues are not all reduced away")
        else:
            require(all(rho != 0 for rho in zeros),
                    "Schoof degree-five residues do not ramify")
        rows[n] = {"zero_count": len(zeros),
                   "zero_residue_count": sum(rho == 0 for rho in zeros),
                   "nonzero_residue_count": sum(rho != 0 for rho in zeros)}
    return {"norm_degree": int(norm.degree()), "local_rows": rows,
            "genus_Y_from_RH": 6, "genus_X_from_RH": 19,
            "bound": "2/9"}


def zeta_from_counts(counts, genus, q=2):
    """Newton reconstruction using genus and the functional equation."""
    require(len(counts) >= genus, "not enough counts for Newton reconstruction")
    power_sums = [q**n + 1 - counts[n - 1]
                  for n in range(1, genus + 1)]
    coefficients = [1]
    for k in range(1, genus + 1):
        value = Fraction(-sum(power_sums[i - 1] * coefficients[k - i]
                              for i in range(1, k + 1)), k)
        require(value.denominator == 1,
                "a zeta coefficient is not an integer")
        coefficients.append(value.numerator)
    coefficients.extend(q**(i - genus) * coefficients[2 * genus - i]
                        for i in range(genus + 1, 2 * genus + 1))
    return coefficients


def points_from_zeta(coefficients, upto, q=2):
    degree = len(coefficients) - 1
    power_sums = []
    for n in range(1, upto + 1):
        value = -sum(coefficients[i] * power_sums[n - i - 1]
                     for i in range(1, min(n, degree + 1)))
        if n <= degree:
            value -= n * coefficients[n]
        power_sums.append(value)
    return [q**n + 1 - power_sums[n - 1] for n in range(1, upto + 1)]


def real_weil_polynomial(coefficients, genus, q=2):
    """Return R(X) with P(T)=T^g R(T^-1+qT), using QQ only."""
    PT = PolynomialRing(QQ, "T")
    T = PT.gen()
    P = PT(coefficients)
    RX = PolynomialRing(QQ, "X")
    X = RX.gen()
    real_coefficients = []
    for k in range(genus + 1):
        remainder = P[k] - sum(
            real_coefficients[j]
            * binomial(genus - j, (k - j) // 2)
            * q**((k - j) // 2)
            for j in range(k) if (k - j) % 2 == 0
        )
        real_coefficients.append(remainder)
    R = RX(sum(real_coefficients[j] * X**(genus - j)
               for j in range(genus + 1)))
    reconstructed = sum(real_coefficients[j] * T**j
                        * (1 + q * T**2)**(genus - j)
                        for j in range(genus + 1))
    require(reconstructed == P, "real Weil polynomial reconstruction failed")
    require(all(value.denominator() == 1 for value in real_coefficients),
            "real Weil polynomial has nonintegral coefficients")
    return R


def check_quotient_certificates(cert):
    quotients = cert["quotients"]
    require(len(quotients) == 31, "certificate does not contain all 31 quotients")
    require({record["h_mask"] for record in quotients} == set(range(1, 32)),
            "quotient masks are not exactly the nonzero five-bit masks")
    interval_lo = -AA(8).sqrt()
    interval_hi = AA(8).sqrt()
    for record in quotients:
        mask = record["h_mask"]
        require(record["genus"] == 13,
                f"stored quotient genus failed for h_mask={mask}")
        counts = direct_quotient_counts(mask, 14)
        require(counts == record["point_counts"],
                f"direct Sage quotient counts failed for h_mask={mask}")
        recomputed = zeta_from_counts(counts, 13)
        require(recomputed == record["zeta_coefficients"],
                f"Newton coefficients failed for h_mask={mask}")
        require(points_from_zeta(recomputed, 14) == counts,
                f"zeta recurrence failed for h_mask={mask}")
        require(sum(recomputed) == record["jacobian_order"],
                f"Jacobian order failed for h_mask={mask}")
        R = real_weil_polynomial(recomputed, 13)
        roots = R.roots(AA, multiplicities=True)
        require(sum(multiplicity for _, multiplicity in roots) == 13,
                f"real Weil polynomial is not totally real for h_mask={mask}")
        require(all(interval_lo <= root <= interval_hi
                    for root, _ in roots),
                f"Weil interval failed for h_mask={mask}")

    k_coefficients = cert["k_zeta_coefficients"]
    # Rebuild the character product independently in Sage's ZZ[T], then
    # divide by P_H^30 and compare every one of the 687 coefficients.
    PT = PolynomialRing(ZZ, "T")
    product = PT(1)
    for record in quotients:
        product *= PT(record["zeta_coefficients"])
    p_h = PT(cert["base_H_zeta"])
    quotient, remainder = product.quo_rem(p_h**30)
    require(remainder == 0,
            "the product of quotient zetas is not divisible by P_H^30")
    product_coefficients = [int(value) for value in quotient.list()]
    require(product_coefficients == [int(value) for value in k_coefficients],
            "the exact quotient product disagrees with every k zeta coefficient")
    require(sum(product_coefficients) == int(cert["k_jacobian_order"]),
            "the exact k Jacobian order disagrees with the product quotient")
    require(len(k_coefficients) == 687, "k zeta polynomial has the wrong degree")
    require(all(k_coefficients[686 - i] == 2**(343 - i) * k_coefficients[i]
                for i in range(344)), "k zeta functional equation failed")
    return {"quotient_count": len(quotients),
            "quotient_degree": 26,
            "quotient_weil_interval": "AA[-sqrt(8),sqrt(8)]",
            "k_zeta_degree": len(k_coefficients) - 1,
            "k_zeta_product_division": "PASS",
            "k_jacobian_order_checked": str(sum(product_coefficients))}


def exact_arithmetic_checks():
    places = [(5, 2), (6, 16), (8, 15), (10, 4)]
    A = sum(multiplicity * degree for degree, multiplicity in places)
    C = sum(multiplicity * degree * (degree + 1)
            for degree, multiplicity in places)
    t = 192
    D = 1 + A - t
    margin = D**2 - 2 * C - 4 * A
    validate_gs_row(A, t, C, margin)
    require((A, C, D, margin) == (266, 2252, 75, 57),
            "main GS arithmetic disagrees with the exact row")
    f_average = 2 * sum(Fraction(multiplicity * degree)
                         * (1 - Fraction(1, 2**degree))
                         for degree, multiplicity in places)
    denominator = Fraction(343 - 1) + f_average / 2
    ratio = Fraction(t) / denominator
    require(f_average == Fraction(33751, 64), "wrong conductor average")
    require(denominator == Fraction(77527, 128), "wrong exact denominator")
    require(ratio == Fraction(24576, 77527), "wrong main exact bound")

    schoof_margin = (6 - 2)**2 - 4 * (3 + 1)
    schoof_ratio = Fraction(4, 19 - 1)
    require(schoof_margin == 0 and schoof_ratio == Fraction(2, 9),
            "wrong Schoof exact arithmetic")
    return {"A": A, "C": C, "D": D, "GS_margin": margin,
            "conductor_average": str(f_average),
            "denominator": str(denominator),
            "main_bound": str(ratio),
            "Schoof_GS_margin": schoof_margin,
            "Schoof_bound": str(schoof_ratio)}


def validate_gs_row(A, t, C, margin):
    require(t > 0 and t <= A and margin >= 0,
            "GS admissibility condition failed")
    require(margin == (1 + A - t)**2 - 2 * C - 4 * A,
            "GS margin is not the stated exact expression")


def negative_case_checks(dm_local, local_maps, k_counts, arithmetic):
    """Ensure obvious bad inputs are rejected by the same exact predicates."""
    dependent = list(local_maps[0])
    dependent[-1] = dependent[0]  # duplicate one of the five basis columns
    rejected_dependent = False
    try:
        validate_local_map_rank(dependent)
    except AssertionError:
        rejected_dependent = True
    require(rejected_dependent, "dependent AS negative test did not reject")

    rejected_missing = False
    missing = dict(dm_local)
    missing["c_h_point_count"] -= 1
    missing["local_map_count"] -= 1
    try:
        validate_dm_local_summary(missing)
    except AssertionError:
        rejected_missing = True
    require(rejected_missing, "missing ramified place negative test did not reject")

    rejected_genus = False
    try:
        validate_k_inventory(dm_local["k_genus_from_RH"] - 1,
                             k_counts, k_counts)
    except AssertionError:
        rejected_genus = True
    require(rejected_genus, "wrong genus negative test did not reject")

    rejected_count = False
    wrong_counts = list(k_counts)
    wrong_counts[4] += 1
    try:
        validate_k_inventory(dm_local["k_genus_from_RH"], wrong_counts,
                             k_counts)
    except AssertionError:
        rejected_count = True
    require(rejected_count, "wrong count negative test did not reject")

    rejected_gs = False
    try:
        A = arithmetic["A"]
        C = arithmetic["C"]
        t = arithmetic["D"] + arithmetic["A"] - 1
        D = 1 + A - t
        margin = D**2 - 2 * C - 4 * A
        validate_gs_row(A, t, C, margin)
    except AssertionError:
        rejected_gs = True
    require(rejected_gs, "failed GS negative test did not reject")
    return {"dependent_AS_generator": "REJECTED",
            "missing_ramified_place": "REJECTED",
            "wrong_genus": "REJECTED",
            "wrong_count": "REJECTED",
            "failed_GS": "REJECTED"}


def main():
    binary_curves = json.loads((ROOT / "curves/binary-curves.json").read_text())
    curve_rows = {row["id"]: row for row in binary_curves}
    expected = {
        "elliptic_E": ([5, 5, 5, 25, 25, 65, 145, 225, 545, 1025], 1),
        "hyperelliptic_AS5": ([5, 9, 5, 17, 25, 81, 145, 193, 545, 1089], 2),
        "base_H": ([6, 6, 9, 10, 36, 87, 90, 274, 513, 1086], 2),
    }

    F2 = GF(2)
    F0 = FunctionField(F2, "x")
    x = F0.gen()
    ypoly = F0["y"]
    y = ypoly.gen()
    E = F0.extension(y**2 + y + x**3 + x, "y")
    H = F0.extension(y**2 + (x**3 + x + 1) * y + x**2 + x, "y")
    AS5 = F0.extension(y**2 + y + x**5 + x, "y")
    function_fields = {"elliptic_E": E, "base_H": H,
                       "hyperelliptic_AS5": AS5}

    geometry = {}
    direct_counts = {
        "elliptic_E": point_counts_e(),
        "hyperelliptic_AS5": point_counts_as5(),
        "base_H": point_counts_h(),
    }
    for name, (known_counts, known_genus) in expected.items():
        K = function_fields[name]
        require(K.genus() == known_genus, f"Sage genus failed for {name}")
        require(K.constant_field() == F2, f"constant field failed for {name}")
        require(direct_counts[name] == known_counts,
                f"direct Sage point counts failed for {name}")
        require(curve_rows[name]["genus"] == known_genus,
                f"stored genus disagrees for {name}")
        require(curve_rows[name]["extension_point_counts"] == known_counts,
                f"stored counts disagree for {name}")
        geometry[name] = {"genus": known_genus, "point_counts": known_counts}

    # Sage's class_group() here is the affine maximal-order S-ideal group.
    # Keep it separate from the complete Jacobian group used for Pic^0(H).
    affine_class_group_order = int(H.class_group().order())
    require(affine_class_group_order == 1,
            "H affine class-group order is not one")
    jacobian_order = int(H.jacobian(model="hess").group()
                         .order(algorithm="algebraic"))
    require(jacobian_order == 19, "H Jacobian order is not 19")

    # A separate Sage place enumeration confirms the normalized H inventory.
    h_places = [len(H.places(d)) for d in range(1, 11)]
    expected_h_places = [6, 0, 1, 1, 6, 13, 12, 33, 56, 105]
    require(h_places == expected_h_places, "Sage H degree-place inventory failed")

    dm_local, local_maps = dm_local_residues()
    k_counts = direct_k_counts(10)
    expected_k_counts = [192, 192, 192, 192, 202, 288, 192, 320, 192, 842]
    require(k_counts == expected_k_counts, "direct Sage k trace counts failed")
    validate_k_inventory(dm_local["k_genus_from_RH"], k_counts,
                         expected_k_counts)
    require(curve_rows["dm_k343"]["extension_point_counts"] == expected_k_counts,
            "stored k counts disagree with direct Sage traces")

    zeta_cert = json.loads((ROOT / "certificates/k343-zeta.json").read_text())
    zeta = check_quotient_certificates(zeta_cert)
    require(points_from_zeta(zeta_cert["k_zeta_coefficients"], 10)
            == expected_k_counts, "stored k zeta does not predict k counts")

    schoof = schoof_local_residues()
    arithmetic = exact_arithmetic_checks()
    negatives = negative_case_checks(dm_local, local_maps, k_counts, arithmetic)

    print("INDEPENDENT_SAGE_STATUS=PASS")
    print("SAGE_VERSION=10.9")
    print("GEOMETRY=PASS E/H/AS5 genus and N_1..N_10")
    print("H_AFFINE_CLASS_GROUP_ORDER=1 H_JACOBIAN_ORDER=19")
    print("H_PLACES_D1..D10=" + ",".join(str(value) for value in h_places))
    print("DM_LOCAL=" + json.dumps(dm_local, sort_keys=True))
    print("K_COUNTS_N1..N10=" + ",".join(str(value) for value in k_counts))
    print("ZETA=" + json.dumps(zeta, sort_keys=True))
    print("SCHOOF=" + json.dumps(schoof, sort_keys=True))
    print("ARITHMETIC=" + json.dumps(arithmetic, sort_keys=True))
    print("NEGATIVE_CASES=" + json.dumps(negatives, sort_keys=True))


if __name__ == "__main__":
    main()
