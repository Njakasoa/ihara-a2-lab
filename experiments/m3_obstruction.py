#!/usr/bin/env python3
"""Exact necessary-condition optimization for the fixed-k343 M3 score.

The proof eliminates arbitrary degrees/depths before enumeration. This script
enumerates only (rational support count, total rank contribution), and reuses
the frozen M2 obstruction for the final shallow case. No new tower is claimed.
"""
from __future__ import annotations

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
PREFIX = [192, 0, 0, 0, 2, 16, 0, 16, 0, 64, 0, 208]
BASE_ROWS = [(5, 2, 2), (6, 16, 2), (8, 16, 2), (10, 2, 2), (12, 1, 2)]


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def rebate(f, s):
    q = 2**f
    return F(f, 2*(q-1)) * (1 + F(q-2, q**(2*s-1)))


def necessary_pairs():
    counts = Counter()
    survivors = []
    by_n = []
    for n in range(192):
        endpoint = (F(269993, 1024) + F(37, 16)
                    - n*(1/B-F(1, 2))) * F(1024, 1023)
        cap = (endpoint.numerator-1)//endpoint.denominator
        tested = 0
        for a in range(n, cap+1):
            tested += 1
            counts['pairs_tested'] += 1
            lower_cost = max(F(0), a-F(n, 2)-F(37, 16)-F(a, 1024))
            bound = B*(342+lower_cost)
            t_min = bound.numerator//bound.denominator+1
            if t_min > min(a, 192-n):
                counts['splitting_rejected'] += 1
                continue
            c_min = max(0, 11*a-690-10*n)
            c_max = ((1+a-t_min)**2-4*a)//2
            if c_min > c_max:
                counts['relation_rejected'] += 1
                continue
            survivors.append({'rational_support': n, 'A': a, 't_min': t_min,
                              't_max': min(a, 192-n), 'C_min': c_min, 'C_max': c_max})
        by_n.append({'rational_support': n, 'strict_A_endpoint': endpoint,
                     'A_cap': cap, 'pairs_tested': tested})
    return {'counts': dict(counts), 'by_rational_support': by_n, 'survivors': survivors}


def evaluate(rows, inventory):
    """Optimize t exactly for a specified even-depth assignment with shared stock."""
    totals = Counter()
    a = c = rational = 0
    cost = F(0)
    for f, m, nu in rows:
        require(all(type(v) is int for v in (f, m, nu)), 'integer row required')
        require(f >= 1 and m >= 1 and nu >= 2 and nu % 2 == 0, 'invalid even row')
        totals[f] += m
        if f == 1:
            rational += m
        s = nu//2
        a += m*f*s
        c += m*f*(nu-1)*(f*(nu-1)+1)
        cost += m*(f*s-rebate(f, s))
    require(all(m <= inventory.get(f, 0) for f, m in totals.items()), 'stock exceeded')
    q = 2*c+4*a
    z = isqrt(q)
    ceil = z + (z*z != q)
    t = max(0, min(192-rational, a, 1+a-ceil))
    denominator = 342+cost
    return {'rows': rows, 'T_size': t, 'rational_support': rational,
            'A': a, 'C': c, 'D': 1+a-t, 'GS_margin': (1+a-t)**2-2*c-4*a,
            'conductor_average_bound': 2*cost, 'genus_denominator': denominator,
            'exact_score': F(t)/denominator, 'Ihara_bound_status':
            'arithmetic score only; concrete geometry and tower proof required'}


def run():
    started = time.perf_counter()
    frozen = json.loads((ROOT/'certificates/m2-frozen.json').read_text())
    require(frozen['bound'] == str(B), 'frozen fraction changed')
    for name, expected in frozen['files_sha256'].items():
        require(sha(ROOT/name) == expected, 'frozen M2 file changed: '+name)
    data = json.loads((ROOT/'curves/k343-place-counts-30.json').read_text())
    require(data['place_counts'][:12] == PREFIX, 'reviewed inventory changed')
    inventory = dict(enumerate(data['place_counts'], 1))
    finite = necessary_pairs()
    expected = [{'rational_support': 0, 'A': 266, 't_min': 192,
                 't_max': 192, 'C_min': 2236, 'C_max': 2280}]
    require(finite['survivors'] == expected, 'unexpected survivor; proof must be reconsidered')
    cases = []
    for n in (0, 1, 2, 4):
        for depth in (2, 4, 6):
            if n == 0 and depth != 2:
                continue
            rows = BASE_ROWS + ([(1, n, depth)] if n else [])
            cases.append(evaluate(rows, inventory))
    for f in (5, 6, 8, 10, 12):
        for depth in (4, 6):
            rows = [(d, m-1 if d == f else m, nu) for d, m, nu in BASE_ROWS]
            rows = [r for r in rows if r[1]] + [(f, 1, depth)]
            cases.append(evaluate(rows, inventory))
    require(cases[0]['exact_score'] == B, 'baseline arithmetic mismatch')
    require(all(c['exact_score'] <= B for c in cases), 'illustration contradicts obstruction')
    payload = {'base_field': 'F2', 'genus': 343, 'rational_places': 192,
               'baseline': str(B), 'scope': 'fixed conservative DM score; all finite supports including rational; all integer nu>=2; variable t',
               'finite_certificate': finite, 'minimum_deep_penalty': 155,
               'remaining_relation_slack': 44,
               'terminal_dependency': 'proofs/NU2_OBSTRUCTION.md and its frozen independent certificate',
               'illustrative_assignments': cases,
               'conclusion': 'No strict score improvement; baseline attained. Not an upper bound on actual tower ratios or A(2).'}
    paths = ['certificates/m2-frozen.json', 'curves/k343-place-counts-30.json',
             'certificates/m2-tower.json', 'proofs/M3_NONUNIFORM_OBSTRUCTION.md',
             'experiments/m3_obstruction.py']
    canonical = json.dumps(encode(payload), sort_keys=True, separators=(',', ':')).encode()
    receipt = {'experiment_id': 'm3-all-depth-rational-obstruction',
               'UTC': datetime.now(timezone.utc).isoformat(),
               'commit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
               'software_versions': {'Python': platform.python_version()},
               'input_hashes': {p: sha(ROOT/p) for p in paths},
               'curve_hash': sha(ROOT/'certificates/k343-zeta.json'),
               'output_payload_sha256': hashlib.sha256(canonical).hexdigest(),
               'runtime_seconds': round(time.perf_counter()-started, 6),
               'agent': 'Astra root', 'verification_status': 'production arithmetic PASS; independent review separate',
               'data': payload}
    (ROOT/'results/m3-obstruction.json').write_text(json.dumps(encode(receipt), indent=2)+'\n')
    print('M3_OBSTRUCTION_ARITHMETIC=PASS')
    print(json.dumps(finite['counts'], sort_keys=True))
    print('SURVIVORS='+json.dumps(finite['survivors']))
    return receipt


if __name__ == '__main__':
    run()
