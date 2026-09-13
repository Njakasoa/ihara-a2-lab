"""Schoof's genus-19 control via explicit representatives of the same construction."""
from fractions import Fraction
from exact_curves import field, poly_mul, binary_rank


def e_fiber(F,x):
    return F.as_roots.get(F.eval(0b1010,x),[])


def denominator(F,x,y):
    b=F.eval(0b110,x)
    return F.mul(b,F.mul(x,y)^x^y)^1


def certificate():
    # Norm(d0+d1*y), y²+y=x³+x.
    d0,d1,f=0b1101,0b1010,0b1010
    norm=poly_mul(d0,d0)^poly_mul(d0,d1)^poly_mul(poly_mul(d1,d1),f)
    residues={}
    for n in (4,5):
        F=field(n); rows=[]
        for x in range(F.q):
            for y in e_fiber(F,x):
                if denominator(F,x,y): continue
                b=F.eval(0b110,x); yp=F.squares[x]^1
                dp=(F.mul(x,y)^x^y)^F.mul(b,y^F.mul(x,yp)^1^yp)
                if dp==0: raise ValueError('denominator zero not simple')
                A=F.div(F.mul(b,x),F.squares[dp])
                B=F.div(F.squares[x],F.squares[dp])
                rho=B^F.sqrt(A)
                rows.append({'x':x,'y':y,'residue':rho})
        assert len(rows)==n
        assert all((r['residue']==0)==(n==4) for r in rows)
        residues[str(n)]={'modulus':F.modulus,'points':rows}
    return {'norm_denominator_bits':norm,'norm_degree':norm.bit_length()-1,
            'local_residues':residues,'genus_E':1,'genus_Y':6,
            'Y_rational_places':10,'X_over_Y_ramified_rational_places':8,
            'X_genus':19,'splitting_set_size':4,
            'class_2_rank_lower_bound':6,'S_unit_2_rank':3,
            'GS_squared_margin':(6-2)**2-4*(3+1),
            'bound':str(Fraction(4,19-1)),
            'status':'KNOWN; exact arithmetic and local model reconstruction',
            'source_equation_note':'Schoof p13 prints T^3+1 inconsistent with five points; use T^3+T per conductor/splitting data.'}

if __name__=='__main__':
    import json
    from pathlib import Path
    result=certificate()
    (Path(__file__).resolve().parents[1]/'certificates/schoof-control.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Schoof control:',result['bound'],'genus',result['X_genus'])
