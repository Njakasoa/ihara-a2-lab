"""Finite geometry of the genus-334 base in Ma--Xing--Xing, Theorem 6.1.

Run with Sage's Python.  Source: https://arxiv.org/html/2610.33649v2#S6.SS1
Masks encode characters in the ordered basis (1, x, x^2, x^3, y).
"""

import json
from collections import Counter

from sage.all import GF, FunctionField, PolynomialRing


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def coefficient(x, y):
    return (x**4 + x**3 + x**2 + x) * y + x**2 + x + 1


def basis(x, y):
    return [x.parent().one(), x, x**2, x**3, y]


def characters_at_place(H, place, generators):
    """Classify every AS character by its conductor and residue extension."""
    complete = H.completion(place, prec=4)
    series = [complete(g) for g in generators]
    require(all(s.valuation() >= -2 and s.precision_absolute() > 0 for s in series),
            "expected at most a double pole and a known constant coefficient")
    ramified, inert = [], []
    for mask in range(1, 32):
        expansion = sum(s for i, s in enumerate(series) if mask & (1 << i))
        # Subtract (sqrt(a)/t)^2 + sqrt(a)/t from a/t^2 + b/t + c.
        # The odd pole has conductor 2. If it disappears, Tr(c) detects an inert place.
        if expansion[-1] + expansion[-2].sqrt():
            ramified.append(mask)
        elif expansion[0].trace():
            inert.append(mask)
    return ramified, inert


def count_places(cover_degree, ramification):
    """Count points over F_(2^n) on the normalization, then recover places."""
    counts, places = [], []
    for n in range(1, 13):
        F = GF(2**n, name="u")
        roots = {z*z + z: z for z in F}
        points = 2 * cover_degree  # both infinity places of H split
        for x in F:
            a, b = x**3 + x + 1, x**2 + x
            if a:
                z = roots.get(b / a**2)
                if z is None:
                    continue
                ys = (a*z, a*(z+1))
            else:
                y = b.sqrt()
                require((x**2+1)*y + 1 != 0, "singular point in the affine H model")
                ys = (y,)
            for y in ys:
                c = coefficient(x, y)
                if c:
                    factor = b / c**2
                    if all(factor*h in roots for h in basis(x, y)):
                        points += cover_degree
                else:
                    degree = 3 if a == 0 else 7
                    require(n % degree == 0, "unexpected zero of c")
                    e, f = ramification[degree]
                    if n % (degree*f) == 0:
                        points += cover_degree // e
        counts.append(points)
        residual = points - sum(d*places[d-1] for d in range(1, n) if n % d == 0)
        require(residual >= 0 and residual % n == 0, "inconsistent closed-place count")
        places.append(residual // n)
    return counts, places


def verify_geometry():
    K = FunctionField(GF(2), "x")
    x = K.gen()
    Y = PolynomialRing(K, "Y").gen()
    H = K.extension(Y**2 + (x**3+x+1)*Y + x**2+x, "y")
    x, y = H(x), H.gen()
    c = coefficient(x, y)
    generators = [(x**2+x)*h/c**2 for h in basis(x, y)]
    genus_H = int(H.genus())
    require(genus_H == 2, "unexpected genus of H")

    pole_places = sorted(c.zeros(), key=lambda p: p.degree())
    require([p.degree() for p in pole_places] == [3, 7], "unexpected zero divisor of c")
    p3, p7 = pole_places
    require((x**3+x+1).valuation(p3) > 0 and (y+x**2).valuation(p3) > 0,
            "degree-three place differs from P3")
    require((x**7+x**3+1).valuation(p7) > 0 and (y+x**5+x**2).valuation(p7) > 0,
            "degree-seven place differs from P7")
    require(all(set(g.poles()) <= set(pole_places) for g in generators),
            "additional pole of an Artin--Schreier generator")

    ram3, inert3 = characters_at_place(H, p3, generators)
    ram7, inert7 = characters_at_place(H, p7, generators)
    unram3 = sorted(set(range(1, 32)) - set(ram3))
    require(unram3 == [11, 19, 24] and 11 not in inert3 and len(inert3) == 2,
            "unexpected splitting of the degree-three unramified characters")
    require(len(ram7) == 31 and not inert7, "P7 does not detect all nonzero characters")
    # Every nonzero character ramifies at P7, so the five generators are independent.
    cover_degree = 1 + len(ram7)
    ramification = {
        3: (cover_degree // (1 + len(unram3)), 2 if inert3 else 1),
        7: (cover_degree, 1),
    }
    conductors = Counter(2*(3*(m in ram3) + 7*(m in ram7)) for m in range(1, 32))
    different_degree = sum(deg*count for deg, count in conductors.items())
    twice_genus = 2 + cover_degree*(2*genus_H-2) + different_degree
    require(twice_genus == 668, "conductor-discriminant genus check failed")

    rational_places = H.places(1)
    require(len(rational_places) == 6 and sum(p.is_infinite_place() for p in rational_places) == 2,
            "unexpected rational places of H")
    require(all(g.evaluate(p) == 0 for p in rational_places for g in generators),
            "a rational place fails to split")
    counts, places = count_places(cover_degree, ramification)
    require(places == [192, 0, 0, 0, 0, 2, 1, 16, 0, 96, 0, 240],
            "unexpected genus-334 place inventory")
    return {
        "genus_H": genus_H, "degree_over_H": cover_degree, "genus_k": twice_genus // 2,
        "character_conductor_degree_counts": dict(sorted(conductors.items())),
        "P3_unramified_nonzero_masks": unram3, "P3_inert_masks": inert3,
        "ramification_index_and_residue_degree": ramification,
        "point_counts_1_to_12": counts, "place_counts_1_to_12": places,
    }


if __name__ == "__main__":
    print(json.dumps(verify_geometry(), indent=2))
