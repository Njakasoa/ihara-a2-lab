#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from candidate_certificate import assemble

def main():
    def read(p):return json.loads((ROOT/p).read_text())
    cert=assemble(read('results/reference-nu2-search.json'),read('curves/k343-places.json'),read('curves/k343-degree12-places.json'),read('certificates/dm-finite-geometry.json'),read('certificates/k343-zeta.json'),read('certificates/dm-selected-places.json'))
    (ROOT/'certificates/m2-tower.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(cert['id'],cert['resulting_Ihara_ratio_lower_bound'],cert['tower_infinitude_inequality'])
if __name__=='__main__':main()
