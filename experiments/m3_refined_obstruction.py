#!/usr/bin/env python3
"""Certify the necessary pairs for the refined elementary-ray M3 score."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import platform
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
B = F(196608, 620201)
BETA = sum(m*f*(F(1, 2**f-1)-F(1, 1023)) for f, m in [(5, 2), (6, 16), (8, 16)])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def optimize_assignment(rows, inventory):
    """Choose optimal t; odd cutoffs give the same elementary-ray field."""
    stocks = Counter()
    a = c = rational = 0
    cost = F(0)
    for f, m, nu in rows:
        require(all(type(v) is int for v in (f, m, nu)), 'integer row required')
        require(f >= 1 and m >= 1 and nu >= 2, 'invalid row')
        stocks[f] += m
        rational += m if f == 1 else 0
        s = nu//2
        rank = f*s
        a += m*rank
        c += m*rank*(rank+1)
        cost += m*(rank-F(f, 2**f-1)*(1-F(1, 2**rank)))
    require(all(m <= inventory.get(f, 0) for f, m in stocks.items()), 'stock exceeded')
    q = 2*c+4*a
    z = isqrt(q)
    ceil = z+(z*z != q)
    t = max(0, min(192-rational, a, 1+a-ceil))
    return {'rows': rows, 'T_size': t, 'rational_support': rational, 'A': a,
            'C_refined': c, 'D': 1+a-t, 'GS_margin': (1+a-t)**2-2*c-4*a,
            'conductor_average_bound': 2*cost, 'genus_denominator': 342+cost,
            'exact_score': F(t)/(342+cost),
            'scope': 'arithmetic assignment, not a new geometric tower certificate'}


def run():
    started = time.perf_counter()
    frozen = json.loads((ROOT/'certificates/m2-frozen.json').read_text())
    for name, digest in frozen['files_sha256'].items():
        require(sha(ROOT/name) == digest, 'frozen M2 input changed: '+name)
    inventory_data = json.loads((ROOT/'curves/k343-place-counts-30.json').read_text())
    require(inventory_data['place_counts'][:12] == [192,0,0,0,2,16,0,16,0,64,0,208], 'inventory changed')
    require(BETA == F(1290176, 608685), 'beta mismatch')
    counts = Counter()
    survivors = []
    caps = []
    for n in range(192):
        endpoint = ((192-n)/B-342+n+BETA-F(n, 1023))*F(1023, 1022)
        cap = (endpoint.numerator-1)//endpoint.denominator
        caps.append({'n': n, 'strict_A_endpoint': endpoint, 'A_cap': cap})
        for a in range(n, cap+1):
            counts['pairs_tested'] += 1
            lower_cost = max(F(0), a-n-BETA-F(a-n, 1023))
            cut = B*(342+lower_cost)
            t_min = cut.numerator//cut.denominator+1
            if t_min > min(a, 192-n):
                counts['splitting_rejected'] += 1
                continue
            c_min = max(0, 11*a-690-25*n)
            c_max = ((1+a-t_min)**2-4*a)//2
            if c_min > c_max:
                counts['relation_rejected'] += 1
                continue
            survivors.append({'n': n, 'A': a, 't_min': t_min, 't_max': min(a, 192-n),
                              'C_min': c_min, 'C_max': c_max})
    require(survivors == [{'n':0,'A':266,'t_min':192,'t_max':192,'C_min':2236,'C_max':2280}], 'unexpected necessary pair')
    residuals = []
    for omitted8, mass, budget in [(0,27,316),(1,35,388)]:
        number_cap = mass//10
        c_lower = F(mass*mass, number_cap)+mass
        require(c_lower > budget, 'deep pattern not excluded')
        residuals.append({'omitted_degree8': omitted8, 'high_degree_rank_mass': mass,
                          'C_budget': budget, 'number_cap': number_cap,
                          'Cauchy_lower_bound': c_lower, 'rejected': True})
    old = json.loads((ROOT/'results/m3-obstruction.json').read_text())
    inventory = dict(enumerate(inventory_data['place_counts'], 1))
    cases = [optimize_assignment(row['rows'], inventory) for row in old['data']['illustrative_assignments']]
    require(cases[0]['exact_score'] == B, 'baseline attainment mismatch')
    require(all(c['exact_score'] <= B for c in cases), 'illustration contradicts obstruction')
    payload = {'base_field':'F2','genus':343,'N1':192,'baseline':B,'beta':BETA,
               'scope':'refined elementary-ray conservative score; all finite supports including rational; all nu>=2; t optimized',
               'counts':dict(counts),'caps':caps,'survivors':survivors,
               'deep_penalties':{'f5_s2':25,'f5_s3':100,'f6_s2':48,'f8_s2':112,'f10_s2':200},
               'remaining_slack':44,'residual_high_degree_patterns':residuals,
               'assignments':cases,'exact_optimum':B,
               'terminal_dependency':'frozen independent M2 all-degree nu2 obstruction',
               'conclusion':'No strict improvement of this refined score. Actual inertia averages and tower ratios remain outside scope.'}
    paths = ['experiments/m3_refined_obstruction.py','proofs/M3_REFINED_RAY_CRITERION.md',
             'proofs/M3_REFINED_OBSTRUCTION.md','certificates/m2-frozen.json',
             'curves/k343-place-counts-30.json','results/m3-obstruction.json']
    canonical = json.dumps(encode(payload), sort_keys=True, separators=(',', ':')).encode()
    receipt = {'experiment_id':'m3-refined-elementary-ray-obstruction',
               'UTC':datetime.now(timezone.utc).isoformat(),
               'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
               'input_hashes':{p:sha(ROOT/p) for p in paths},
               'curve_hash':sha(ROOT/'certificates/k343-zeta.json'),
               'output_payload_sha256':hashlib.sha256(canonical).hexdigest(),
               'runtime_seconds':round(time.perf_counter()-started,6),
               'software_versions':{'Python':platform.python_version()},
               'agent':'Astra root','verification_status':'production arithmetic PASS; independent proof/implementation review separate',
               'data':payload}
    (ROOT/'results/m3-refined-obstruction.json').write_text(json.dumps(encode(receipt),indent=2)+'\n')
    print('M3_REFINED_OBSTRUCTION_ARITHMETIC=PASS')
    print(json.dumps(dict(counts),sort_keys=True))
    print('SURVIVORS='+json.dumps(survivors))


if __name__ == '__main__':
    run()
