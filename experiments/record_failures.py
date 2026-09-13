#!/usr/bin/env python3
"""Preserve exact rejected or inferior variations around the automatic candidate."""
import json,sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from theorem_search import evaluate_binary,optimal_t

def main():
    data=json.loads((ROOT/'results/m2-search.json').read_text())
    best=data['nu2_search']['automatic_best'];rows=[tuple(r) for r in best['rows']]
    cases=[('remove degree12 at fixed t',[(d,m-(d==12),nu) for d,m,nu in rows]),
      ('uniform depth4',[(d,m,4) for d,m,nu in rows]),
      ('one degree5 depth4',[r for r in rows if r[0]!=5]+[(5,1,2),(5,1,4)]),
      ('one degree5 depth4 and remove degree8',[r for r in rows if r[0] not in (5,8)]+[(5,1,2),(5,1,4),(8,15,2)])]
    result=[]
    for name,variant in cases:
        fixed=evaluate_binary(343,192,variant,rational_places=192)
        t=optimal_t(fixed['A'],fixed['C'],192)
        optimized=evaluate_binary(343,t,variant,rational_places=192)
        assert optimized['ratio_lower_bound']<Fraction(best['ratio_lower_bound'])
        result.append({'case':name,'fixed_t':fixed,'best_t_for_this_support':optimized,
                       'interpretation':'failed sufficient criterion means no certificate, not finite tower; lower score is not an upper bound for the actual tower'})
    (ROOT/'results/failed-or-inferior-variants.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    for r in result:print(r['case'],'fixed GS',r['fixed_t']['GS'],'optimal t',r['best_t_for_this_support']['t'],'score',r['best_t_for_this_support']['ratio_lower_bound'])
if __name__=='__main__':main()
