"""Small binary curves and the Duursma–Mak genus-343 cover, exact arithmetic.

All integers encoding field elements use polynomial-basis bits (least bit constant).
Only the documented curve families are supported; this is not a general validator.
"""
from fractions import Fraction
from functools import lru_cache


def poly_mod(a, b):
    if b <= 0:
        raise ValueError('nonzero polynomial divisor required')
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def poly_gcd(a, b):
    while b:
        a, b = b, poly_mod(a, b)
    return a


def poly_mul(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        a <<= 1
        b >>= 1
    return c


def irreducible(p):
    n = p.bit_length() - 1
    if n < 1:
        return False
    x = poly_mod(2, p)
    power = x
    for i in range(1, n + 1):
        power = poly_mod(poly_mul(power, power), p)
        if i <= n // 2 and poly_gcd(power ^ x, p) != 1:
            return False
    return power == x


class GF2:
    def __init__(self, n, modulus=None):
        if not isinstance(n, int) or n < 1:
            raise ValueError('positive extension degree required')
        self.n, self.q = n, 1 << n
        if modulus is None:
            modulus = next(p for p in range(self.q, 2*self.q) if irreducible(p))
        if modulus.bit_length() != n+1 or not irreducible(modulus):
            raise ValueError('modulus must be irreducible of the requested degree')
        self.modulus = modulus
        self.squares = [self.mul(x, x) for x in range(self.q)]
        self.as_roots = {}
        for x in range(self.q):
            self.as_roots.setdefault(self.squares[x] ^ x, []).append(x)
        self.traces = [self.trace(x) for x in range(self.q)]
        self.inverses = [0] + [self.pow(x, self.q-2) for x in range(1, self.q)]

    def mul(self, a, b):
        c = 0
        while b:
            if b & 1:
                c ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.modulus
        return c

    def pow(self, a, n):
        if n < 0:
            return self.pow(self.inv(a), -n)
        b = 1
        while n:
            if n & 1:
                b = self.mul(a, b)
            a = self.mul(a, a)
            n >>= 1
        return b

    def inv(self, a):
        if a == 0:
            raise ZeroDivisionError('zero has no field inverse')
        return self.inverses[a]

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def sqrt(self, a):
        return self.pow(a, self.q//2)

    def trace(self, a):
        t, x = 0, a
        for _ in range(self.n):
            t ^= x
            x = self.squares[x]
        assert t in (0, 1)
        return t

    def eval(self, polynomial, x):
        y = 0
        for i in range(polynomial.bit_length()-1, -1, -1):
            y = self.mul(y, x) ^ ((polynomial >> i) & 1)
        return y


@lru_cache(maxsize=None)
def field(n):
    return GF2(n)


def h_fiber(F, x):
    a = F.eval(0b1011, x)  # x^3+x+1
    b = F.eval(0b110, x)  # x^2+x
    if a == 0:
        return [F.sqrt(b)]
    return [F.mul(a, z) for z in F.as_roots.get(F.div(b, F.squares[a]), [])]


def count_curve(name, n):
    F = field(n)
    if name in ('elliptic_E', 'hyperelliptic_AS5'):
        p = 0b1010 if name == 'elliptic_E' else 0b100010
        return 1 + sum(len(F.as_roots.get(F.eval(p, x), [])) for x in range(F.q))
    if name == 'base_H':
        return 2 + sum(len(h_fiber(F, x)) for x in range(F.q))
    if name != 'dm_k343':
        raise ValueError('unsupported family')
    total = 64  # both H-points at infinity split completely
    for x in range(F.q):
        b, c = F.eval(0b110, x), F.eval(0b100101, x)
        for y in h_fiber(F, x):
            if c == 0:
                # Validated separately: inertia order32, residue degree1 at both P5.
                total += 1
                continue
            factor = F.div(b, F.squares[c])
            basis = [1, x, F.squares[x], y, F.squares[y]]
            if all(F.traces[F.mul(factor, h)] == 0 for h in basis):
                total += 32
    return total


def place_counts(counts):
    """Möbius inversion without floating point; counts[n-1]=N_n."""
    places = []
    for n, N in enumerate(counts, 1):
        residual = N - sum(d*places[d-1] for d in range(1, n) if n % d == 0)
        if residual < 0 or residual % n:
            raise ValueError('point counts inconsistent with places')
        places.append(residual//n)
    return places


def zeta_numerator(counts, genus, q=2):
    """Newton identities from >=2g exact extension point counts."""
    if len(counts) < 2*genus:
        raise ValueError('need at least 2g counts')
    c = [1]
    s = [q**n+1-counts[n-1] for n in range(1, 2*genus+1)]
    for k in range(1, 2*genus+1):
        ck = -Fraction(sum(s[i-1]*c[k-i] for i in range(1, k+1)), k)
        if ck.denominator != 1:
            raise ValueError('nonintegral zeta coefficient')
        c.append(int(ck))
    if any(c[2*genus-i] != q**(genus-i)*c[i] for i in range(genus+1)):
        raise ValueError('functional equation failed')
    return c


def binary_rank(vectors):
    basis = {}
    for v in vectors:
        while v:
            k = v.bit_length()-1
            if k in basis:
                v ^= basis[k]
            else:
                basis[k] = v
                break
    return len(basis)


def local_certificate():
    """Odd-pole residues certify geometric independence and cover genus.

For f=N/c² near x=alpha, put t=x-alpha. Its principal part is A/t²+B/t.
Modulo u²+u it reduces to (B+sqrt(A))/t. All residues are exact finite fields.
"""
    F = field(3)
    h_residues = []
    for x in range(F.q):
        if F.eval(0b1011, x) == 0:
            ap = F.squares[x] ^ 1
            b = F.eval(0b110, x)
            A = F.div(b, F.squares[ap])
            B = F.inv(F.squares[ap])
            residue = B ^ F.sqrt(A)
            assert residue != 0
            h_residues.append({'x': x, 'residue': residue})
    assert len(h_residues) == 3
    F = field(5)
    rows = []
    for x in range(F.q):
        if F.eval(0b100101, x):
            continue
        ys = h_fiber(F, x)
        assert len(ys) == 2
        b = F.eval(0b110, x)
        a = F.eval(0b1011, x)
        cp = F.pow(x, 4)
        for y in ys:
            yp = F.div(1 ^ F.mul(F.squares[x] ^ 1, y), a)
            basis = [1, x, F.squares[x], y, F.squares[y]]
            derivatives = [0, 1, 0, yp, 0]
            residues = []
            for h, hp in zip(basis, derivatives):
                A = F.div(F.mul(b, h), F.squares[cp])
                B = F.div(h ^ F.mul(b, hp), F.squares[cp])
                residues.append(B ^ F.sqrt(A))
            assert binary_rank(residues) == 5
            rows.append({'x': x, 'y': y, 'residues': residues, 'rank': 5})
    assert len(rows) == 10
    return {'GF8_modulus': field(3).modulus, 'H_reduced_poles': h_residues,
            'GF32_modulus': F.modulus, 'k_local_maps': rows,
            'H_genus': 2, 'k_degree_over_H': 32, 'nontrivial_characters': 31,
            'conductor_degree_each_character': 20, 'k_genus': 343,
            'status': 'EXACT FINITE FIELD',
            'proof_dependency': 'proofs/FINITE_GEOMETRY.md'}


def enumerate_k_places(n):
    """Canonical degree-n places of k343, via Frobenius orbits of normalized points.

Regular coordinates are (x,y,w1,...,w5), w_i=v_i/c. At ramified points
these w_i are not affine coordinates; total inertia supplies a unique point.
At infinity use (branch of y/a, w1,...,w5), all in F2.
"""
    from itertools import product
    F=field(n)
    points=[]
    if n==1:
        for branch in (0,1):
            points.extend(('infinity',(branch,*bits)) for bits in product((0,1),repeat=5))
    for x in range(F.q):
        c=F.eval(0b100101,x)
        b=F.eval(0b110,x)
        for y in h_fiber(F,x):
            if c==0:
                points.append(('ramified',(x,y)))
            else:
                factor=F.div(b,F.squares[c])
                roots=[F.as_roots.get(F.mul(factor,h),[]) for h in [1,x,F.squares[x],y,F.squares[y]]]
                points.extend(('regular',(x,y,*ws)) for ws in product(*roots))
    representatives=set()
    for kind,point in points:
        orbit=[point]
        current=tuple(F.squares[a] for a in point)
        while current!=point:
            if len(orbit)>=n: raise ValueError('invalid Frobenius orbit')
            orbit.append(current)
            current=tuple(F.squares[a] for a in current)
        if len(orbit)==n:
            representatives.add((kind,min(orbit)))
    result=[]
    for i,(kind,point) in enumerate(sorted(representatives),1):
        result.append({'id':f'k343-d{n}-{i:03d}','degree':n,'GF_modulus_bits':F.modulus,
                       'chart':kind,'representative':list(point)})
    return result
