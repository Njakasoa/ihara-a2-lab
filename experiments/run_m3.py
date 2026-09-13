#!/usr/bin/env python3
"""Replay the bounded M3 gates and bind their exact outputs to source hashes.

Requires the existing Sage runtime via scripts/sage-python. This does not run
the historical maximal-order pilot or launch another parameter search.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_freeze():
    frozen = json.loads((ROOT / 'certificates/m2-frozen.json').read_text())
    for name, expected in frozen['files_sha256'].items():
        if digest(ROOT / name) != expected:
            raise ValueError('Frozen M2 file changed: ' + name)
    return frozen


def main():
    started = time.perf_counter()
    frozen = check_freeze()
    sources = sorted(set(
        list(ROOT.glob('experiments/*m3*.py'))
        + list(ROOT.glob('src/m3*.py'))
        + list(ROOT.glob('tests/*m3*.py'))
        + list(ROOT.glob('proofs/*M3*.md'))
        + [ROOT / 'proofs/NONUNIFORM_CONDUCTOR_LOCAL_THEORY.md',
           ROOT / 'proofs/CONSERVATIVE_GAPS.md',
           ROOT / 'tests/independent_candidate.py',
           ROOT / 'tests/independent_obstruction.py',
           ROOT / 'certificates/m2-frozen.json']))
    commands = [
        ('local-units', [sys.executable, 'experiments/m3_local_units.py'],
         'results/m3-local-units.json'),
        ('ray-components', ['scripts/sage-python', 'experiments/m3_ray_structure.py'],
         'results/m3-ray-structure.json'),
        ('full-ray-obstruction', [sys.executable, 'experiments/m3_obstruction.py'],
         'results/m3-obstruction.json'),
        ('refined-obstruction', [sys.executable, 'experiments/m3_refined_obstruction.py'],
         'results/m3-refined-obstruction.json'),
        ('unit-tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], None),
        ('independent-m3', [sys.executable, 'tests/independent_m3.py'],
         'results/m3-independent.json'),
        ('independent-m2-geometry', ['scripts/sage-python', 'tests/independent_candidate.py'], None),
        ('frozen-m2-terminal-obstruction', [sys.executable, 'tests/independent_obstruction.py'], None),
    ]
    receipt = {
        'experiment_id': 'M3-complete-bounded-reproduction',
        'UTC': datetime.now(timezone.utc).isoformat(),
        'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'agent': 'Astra root integration of independent Luna/Astra work',
        'software_versions': {'Python': platform.python_version(),
                              'Sage': 'runtime version in ray-components receipt'},
        'input_hashes': {str(p.relative_to(ROOT)): digest(p) for p in sources},
        'frozen_M2': frozen,
        'base_field': 'F2', 'base_genus': 343,
        'curve_hash': digest(ROOT / 'certificates/k343-zeta.json'),
        'baseline_context': {'T': 192, 'degrees': [5, 6, 8, 10, 12],
                             'support': [2, 16, 16, 2, 1], 'nu': [2]*5,
                             'GS_margin': 41, 'genus_bound_per_degree': '620201/1024',
                             'exact_score': '196608/620201', 'Ihara_bound': '196608/620201'},
        'scope': 'Local fixtures have no T or tower score; global obstructions cover all finite S, nu>=2 and disjoint T of size 1..192. Per-assignment quantities are in their output receipts.',
        'historical_pilot': 'Recorded separately; no maximal-order pilot rerun.',
        'commands': [], 'verification_status': 'RUNNING',
    }
    logdir = ROOT / 'results/m3-run-logs'
    logdir.mkdir(exist_ok=True)
    target = ROOT / 'results/m3-reproduction.json'
    for name, command, output in commands:
        tick = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=180)
        log = logdir / (name + '.txt')
        log.write_text(run.stdout)
        item = {'experiment_id': name, 'command': command,
                'UTC_finished': datetime.now(timezone.utc).isoformat(),
                'runtime_seconds': round(time.perf_counter()-tick, 6),
                'exit_code': run.returncode,
                'output_hashes': {str(log.relative_to(ROOT)): digest(log)}}
        if output and (ROOT / output).exists():
            item['output_hashes'][output] = digest(ROOT / output)
        receipt['commands'].append(item)
        print(name + ': ' + ('PASS' if run.returncode == 0 else 'FAIL'), flush=True)
        check_freeze()
        if run.returncode:
            receipt['verification_status'] = 'FAIL'
            target.write_text(json.dumps(receipt, indent=2)+'\n')
            print(run.stdout)
            return run.returncode
    for path, expected in receipt['input_hashes'].items():
        if digest(ROOT / path) != expected:
            raise ValueError('Source changed during replay: '+path)
    receipt['verification_status'] = 'PASS'
    receipt['runtime_seconds'] = round(time.perf_counter()-started, 6)
    target.write_text(json.dumps(receipt, indent=2)+'\n')
    print('M3_REPRODUCTION=PASS; frozen M2 unchanged')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
