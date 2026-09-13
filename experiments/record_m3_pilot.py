#!/usr/bin/env python3
"""Optional 120-second capability observation with a complete archival receipt.

Not part of the default M3 replay. A timeout is a bounded capability result,
not a mathematical obstruction or a failed mathematical verification.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    source = 'experiments/m3_sage_maximal_order_pilot.py'
    command = ['scripts/sage-python', source]
    source_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    sage = subprocess.check_output(['scripts/sage-python', '-c',
                                   'from sage.version import version; print(version)'],
                                  cwd=ROOT, text=True).strip()
    started = time.perf_counter()
    utc = datetime.now(timezone.utc).isoformat()
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, start_new_session=True)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate()
    elapsed = time.perf_counter()-started
    log = 'results/m3-run-logs/maximal-order-pilot.txt'
    (ROOT / log).parent.mkdir(exist_ok=True)
    (ROOT / log).write_text(output)
    receipt = {
        'experiment_id': 'M3-BOUNDED-SAGE-CAPABILITY-ARCHIVE',
        'UTC': utc, 'commit': source_commit, 'agent': 'Astra root',
        'command': command, 'timeout_seconds': 120,
        'runtime_seconds': round(elapsed, 6), 'exit_code': process.returncode,
        'software_versions': {'Python_driver': platform.python_version(), 'Sage': sage},
        'base_field': 'F2', 'base_genus': 343,
        'curve_hash': sha('certificates/k343-zeta.json'),
        'T': None, 'support': None, 'nu_vector': None,
        'exact_score': None, 'GS_margin': None, 'genus_bound': None, 'Ihara_bound': None,
        'applicability': 'Base maximal-order API capability only; no ray modulus, T or tower score computed.',
        'input_hashes': {p: sha(p) for p in [source, 'experiments/record_m3_pilot.py',
                                         'certificates/k343-zeta.json']},
        'output_hashes': {log: sha(log)},
        'verification_status': ('TIMEOUT_OBSERVED' if timed_out else
                                'COMPLETED_REQUIRES_INSPECTION' if process.returncode == 0 else
                                'API_ERROR_OBSERVED'),
        'nested_field_built': 'K built' in output,
        'maximal_order_call_reached': 'max order...' in output,
        'interpretation': 'Archival repeat of the historical capability pilot; no mathematical result is inferred from runtime.'
    }
    (ROOT / 'results/m3-sage-pilot.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == '__main__':
    main()
