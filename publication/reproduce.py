#!/usr/bin/env python3
"""Rebuild the note's exact data from the surrounding laboratory repository."""
import argparse,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sage',action='store_true',help='also run the independent Sage checks and Theorem 6.1 replay')
    parser.add_argument('--extended',action='store_true',help='also rebuild intermediate and extended search audits')
    parser.add_argument('--pdf',action='store_true',help='compile with the optional local Tectonic runtime')
    args=parser.parse_args()
    commands=[
      [sys.executable,'reproduce.py'],
      [sys.executable,'experiments/reference_nu2_search.py'],
      [sys.executable,'experiments/run_parameter_search.py'],
      [sys.executable,'experiments/bind_candidate.py'],
      [sys.executable,'experiments/record_failures.py'],
      [sys.executable,'publication/checkers/degree12.py'],
      [sys.executable,'-m','unittest','discover','-s','tests','-v']]
    if args.extended:
        commands += [[sys.executable,'src/intermediate_covers.py'],
          [sys.executable,'experiments/search_intermediate_covers.py'],
          [sys.executable,'experiments/search_extended_degrees.py']]
        if (ROOT/'experiments/search_all_degree_relaxation.py').exists():
            commands += [[sys.executable,'experiments/search_all_degree_relaxation.py']]
    commands += [[sys.executable,'tests/independent_obstruction.py']]
    if args.sage:
        commands += [['scripts/sage-python','tests/independent_sage.py'],
                     ['scripts/sage-python','tests/independent_candidate.py'],
                     ['scripts/sage-python','experiments/reproduce_mxx_theorem61.py']]
    if args.pdf:commands += [['scripts/tectonic-local','--keep-logs','publication/main.tex']]
    for command in commands:
        print('RUN',*command,flush=True)
        subprocess.run(command,cwd=ROOT,check=True)
    print('PUBLICATION_REPRODUCTION=PASS')
if __name__=='__main__':main()
