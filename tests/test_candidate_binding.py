"""Certificate binding rejects inconsistent search and place data."""
import unittest,json,sys
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from candidate_certificate import assemble

class CandidateBinding(unittest.TestCase):
    def setUp(self):
        self.args=[json.loads((ROOT/p).read_text()) for p in [
          'results/reference-nu2-search.json','curves/k343-places.json',
          'curves/k343-degree12-places.json','certificates/dm-finite-geometry.json',
          'certificates/k343-zeta.json','certificates/dm-selected-places.json']]
    def test_bound_to_available_distinct_places(self):
        cert=assemble(*self.args)
        self.assertEqual(cert['resulting_Ihara_ratio_lower_bound'],'196608/620201')
        self.assertEqual(len(cert['modulus']),37)
        self.assertEqual(len(cert['selected_splitting_places']),192)
        self.assertIsNone(cert['extension_degree']['K_over_k'])
        self.assertIsNone(cert['ray_class_group_data']['invariant_factors'])
    def test_altered_score_rejected(self):
        self.args[0]['maximizers'][0]['GS_margin']+=1
        with self.assertRaises(ValueError):assemble(*self.args)
    def test_missing_degree12_place_rejected(self):
        self.args[2]=[]
        with self.assertRaises(ValueError):assemble(*self.args)
    def test_duplicate_support_rejected(self):
        self.args[1]['8'][1]=deepcopy(self.args[1]['8'][0])
        with self.assertRaises(ValueError):assemble(*self.args)
    def test_failed_gs_rejected(self):
        self.args[0]['maximizers'][0]['multiplicities']=[2,16,16,0,0]
        with self.assertRaises(ValueError):assemble(*self.args)

if __name__=='__main__':unittest.main()
