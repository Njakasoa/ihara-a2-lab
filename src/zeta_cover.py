"""Exact zeta of k343 from its 31 genus-13 quadratic quotients over H.

Conductor certificates prove quotient genera. First g extension counts plus
functional equations determine each zeta polynomial. Point counts beyond g
are reserved for independent recurrence checks.
"""
from fractions import Fraction
from exact_curves import field,h_fiber


def character_counts(n):
    F=field(n)
    counts=[4]*31  # two H infinity points, two lifts in each quadratic quotient
    for x in range(F.q):
        b,c=F.eval(0b110,x),F.eval(0b100101,x)
        for y in h_fiber(F,x):
            if c==0:
                counts=[v+1 for v in counts]
                continue
            factor=F.div(b,F.squares[c])
            syndrome=sum(F.traces[F.mul(factor,h)]<<i for i,h in enumerate([1,x,F.squares[x],y,F.squares[y]]))
            for h in range(1,32):
                if (h&syndrome).bit_count()%2==0:
                    counts[h-1]+=2
    return counts


def from_half_counts(counts,g,q=2):
    if len(counts)<g: raise ValueError('need genus many counts')
    c=[1]
    s=[q**n+1-counts[n-1] for n in range(1,g+1)]
    for k in range(1,g+1):
        v=-Fraction(sum(s[i-1]*c[k-i] for i in range(1,k+1)),k)
        if v.denominator!=1: raise ValueError('noninteger coefficient')
        c.append(int(v))
    return c+[q**(i-g)*c[2*g-i] for i in range(g+1,2*g+1)]


def poly_product(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c


def poly_quotient(a,b):
    """Exact division from constant coefficient b[0]=1, checked remainder."""
    if b[0]!=1: raise ValueError('unit constant coefficient required')
    r=list(a); q=[0]*(len(a)-len(b)+1)
    for i in range(len(q)):
        q[i]=r[i]
        for j,v in enumerate(b): r[i+j]-=q[i]*v
    if any(r): raise ValueError('nonzero polynomial remainder')
    return q


def points_from_zeta(c,nmax,q=2):
    degree=len(c)-1; s=[]
    for n in range(1,nmax+1):
        v=-sum(c[i]*s[n-i-1] for i in range(1,min(n,degree+1)))
        if n<=degree: v-=n*c[n]
        s.append(v)
    return [q**n+1-s[n-1] for n in range(1,nmax+1)]


def certificate(check_through=14):
    if check_through<14: raise ValueError('require at least one out-of-fit check')
    by_degree=[character_counts(n) for n in range(1,check_through+1)]
    PH=[1,3,5,6,4]
    P=[1]; quotient_records=[]
    for h in range(1,32):
        counts=[row[h-1] for row in by_degree]
        c=from_half_counts(counts,13)
        if points_from_zeta(c,check_through)!=counts: raise ValueError('held-out point count mismatch')
        quotient_records.append({'h_mask':h,'genus':13,'point_counts':counts,'zeta_coefficients':c,'jacobian_order':sum(c)})
        P=poly_product(P,c)
    for _ in range(30): P=poly_quotient(P,PH)
    assert len(P)==687
    assert all(P[686-i]==2**(343-i)*P[i] for i in range(344))
    return {'base_H_zeta':PH,'quotients':quotient_records,'k_genus':343,
            'k_zeta_coefficients':P,'k_jacobian_order':sum(P),
            'counts_used_for_fit':13,'counts_checked_through':check_through,
            'identity':'P_k = product_{h != 0} P_{C_h} / P_H^30',
            'group_structure':'not computed; order is not structure',
            'status':'EXACT INTEGER; derived from certified genera and exact point counts'}

if __name__=='__main__':
    import json
    from pathlib import Path
    c=certificate()
    (Path(__file__).resolve().parents[1]/'certificates/k343-zeta.json').write_text(json.dumps(c,indent=2)+'\n')
    print('k343 zeta degree:',len(c['k_zeta_coefficients'])-1)
    print('Jacobian order:',c['k_jacobian_order'])
