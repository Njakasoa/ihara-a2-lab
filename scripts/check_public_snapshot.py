#!/usr/bin/env python3
"""Check the frozen public file hashes without relying on private Git history."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    failures = []
    for name, expected in manifest['files'].items():
        path = ROOT / name
        if not path.is_file():
            failures.append(name + ': missing')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected['sha256']:
            failures.append(name + ': SHA-256 mismatch')
    if failures:
        raise SystemExit('PUBLIC_SNAPSHOT=FAIL\n' + '\n'.join(failures))
    print('PUBLIC_SNAPSHOT=PASS files=' + str(len(manifest['files'])))

if __name__ == '__main__':
    main()
