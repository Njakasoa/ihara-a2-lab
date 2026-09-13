#!/usr/bin/env python3
"""Independent fixed-domain reference enumeration; no candidate vector supplied."""
import json
from math import isqrt
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def run():
    source=json.loads((ROOT/'curves/k343-place-counts-30.json').read_text())
    degrees=[d for d in range(2,13) if source['place_counts'][d-1]]
    stocks=[source['place_counts'][d-1] for d in degrees]
    scale=2**max(degrees)
    costs=[d*(scale-scale//2**d) for d in degrees]
    baseline=Fraction(24576,77527)
    cost_limit=(Fraction(192)/baseline-342)*scale
    best=baseline; winners=[]
    leaves=0; feasible=0; cut_subtrees=0
    def visit(i, A,C,cost,counts):
        nonlocal best,winners,leaves,feasible,cut_subtrees
        if i==len(degrees):
            leaves+=1
            n=2*C+4*A; r=isqrt(n); r+=r*r<n
            t=min(192,A,1+A-r)
            if t<1:return
            feasible+=1
            bound=Fraction(t*scale,342*scale+cost)
            if bound>best:
                best=bound;winners=[{'multiplicities':list(counts),'t':t,'A':A,'C':C,'D':1+A-t,'GS_margin':(1+A-t)**2-2*C-4*A,'denominator':str(Fraction(342*scale+cost,scale)),'bound':str(bound)}]
            elif bound==best:
                winners.append({'multiplicities':list(counts),'t':t,'A':A,'C':C,'D':1+A-t,'GS_margin':(1+A-t)**2-2*C-4*A,'denominator':str(Fraction(342*scale+cost,scale)),'bound':str(bound)})
            return
        for m in range(stocks[i]+1):
            next_cost=cost+m*costs[i]
            if next_cost>=cost_limit:
                cut_subtrees+=stocks[i]+1-m
                break
            d=degrees[i]
            visit(i+1,A+m*d,C+m*d*(d+1),next_cost,counts+[m])
    visit(0,0,0,0,[])
    result={'kind':'independent reference enumeration','scope':'g343,N192,nonrational S,degree<=12,nu2; only strict improvements over baseline need enumeration','degrees':degrees,'stocks':stocks,'fixed_cost_cap_exclusive':str(cost_limit/scale),'pruning_proof':'Any bound above b requires denominator <192/b. All remaining place costs are nonnegative. Cap uses fixed baseline, not evolving incumbent.','visited_leaves':leaves,'feasible_leaves':feasible,'pruned_subtrees':cut_subtrees,'best_bound':str(best),'maximizers':winners,'all_t_handling':'For fixed S, best t=min(192,A,1+A-ceil_sqrt(2C+4A)); validated independently elsewhere','novelty_status':'UNASSESSED; arithmetic candidates only'}
    (ROOT/'results/reference-nu2-search.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
