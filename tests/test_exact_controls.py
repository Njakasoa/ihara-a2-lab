import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from exact_curves import GF2, irreducible, poly_mul, poly_mod, count_curve, place_counts, zeta_numerator, local_certificate, enumerate_k_places
from baselines import published_controls
from schoof_control import certificate

class ExactControls(unittest.TestCase):
    def test_irreducibility_rejects_squares_and_products(self):
        self.assertFalse(irreducible(poly_mul(0b111,0b1011)))
        self.assertFalse(irreducible(poly_mul(0b1011,0b1011)))
        self.assertTrue(irreducible(0b100101))
        with self.assertRaises(ValueError): GF2(4,0b10101)
        with self.assertRaises(ZeroDivisionError): GF2(2).inv(0)

    def test_field_axioms_small(self):
        for n in range(1,6):
            F=GF2(n)
            for a in range(F.q):
                self.assertEqual(F.pow(a,F.q),a)
                self.assertEqual(F.mul(F.sqrt(a),F.sqrt(a)),a)
                if a: self.assertEqual(F.mul(a,F.inv(a)),1)
                for b in range(F.q):
                    self.assertEqual(F.mul(a,b),poly_mod(poly_mul(a,b),F.modulus))
                    self.assertEqual(F.trace(a^b),F.trace(a)^F.trace(b))

    def test_known_curve_places(self):
        self.assertEqual(place_counts([count_curve('dm_k343',n) for n in range(1,11)]),[192,0,0,0,2,16,0,16,0,64])
        self.assertEqual(count_curve('elliptic_E',1),5)
        self.assertEqual(count_curve('base_H',1),6)

    def test_zeta_predicts_unused_counts(self):
        for name,g in [('elliptic_E',1),('base_H',2),('hyperelliptic_AS5',2)]:
            counts=[count_curve(name,n) for n in range(1,11)]
            c=zeta_numerator(counts[:2*g],g)
            s=[2**n+1-counts[n-1] for n in range(1,2*g+1)]
            for n in range(2*g+1,11):
                value=-sum(c[i]*s[n-i-1] for i in range(1,2*g+1))
                s.append(value)
                self.assertEqual(2**n+1-value,counts[n-1])

    def test_local_rank_certificates(self):
        c=local_certificate()
        self.assertTrue(all(row['rank']==5 for row in c['k_local_maps']))
        self.assertEqual(2*c['k_genus']-2,32*(2*c['H_genus']-2)+31*20)

    def test_exact_bound(self):
        p=published_controls()
        self.assertEqual(p['duursma_mak_343']['ratio_lower_bound'],'24576/77527')
        self.assertEqual(p['duursma_mak_343']['GS_margin'],57)
        self.assertEqual(p['duursma_mak_276']['ratio_lower_bound'],'16384/51711')
        self.assertTrue(all(row['inequality_passes'] for row in p.values()))

    def test_places_are_orbits_of_correct_degree(self):
        for d,N in [(1,192),(5,2),(6,16),(8,16),(10,64)]:
            places=enumerate_k_places(d)
            self.assertEqual(len(places),N)
            for p in places:
                F=GF2(d,p['GF_modulus_bits'])
                point=tuple(p['representative']); orbit={point}
                current=tuple(F.squares[x] for x in point)
                while current!=point:
                    orbit.add(current)
                    current=tuple(F.squares[x] for x in current)
                self.assertEqual(len(orbit),d)

    def test_cover_zeta_saved_counts(self):
        from zeta_cover import points_from_zeta
        c=json.loads((ROOT/'certificates/k343-zeta.json').read_text())
        for Q in c['quotients']:
            self.assertEqual(points_from_zeta(Q['zeta_coefficients'],14),Q['point_counts'])
        self.assertEqual(points_from_zeta(c['k_zeta_coefficients'],10),[count_curve('dm_k343',n) for n in range(1,11)])
        self.assertEqual(sum(c['k_zeta_coefficients']),c['k_jacobian_order'])

    def test_schoof(self):
        c=certificate()
        self.assertEqual(c['GS_squared_margin'],0)
        self.assertEqual(c['bound'],'2/9')

if __name__=='__main__': unittest.main()
