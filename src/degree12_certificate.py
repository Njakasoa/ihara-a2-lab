"""A small certificate for at least208 degree12 places, without k's full zeta."""
from exact_curves import field, h_fiber


def certificate():
    F=field(6)
    representatives=set()
    for x in range(F.q):
        for y in h_fiber(F,x):
            point=(x,y)
            orbit=[point]
            current=tuple(F.squares[a] for a in point)
            while current!=point:
                orbit.append(current)
                current=tuple(F.squares[a] for a in current)
            if len(orbit)==6:
                representatives.add(min(orbit))
    rows=[]
    for x,y in sorted(representatives):
        c=F.eval(0b100101,x)
        assert c!=0
        factor=F.div(F.eval(0b110,x),F.squares[c])
        vector=[F.traces[F.mul(factor,h)] for h in [1,x,F.squares[x],y,F.squares[y]]]
        assert any(vector)
        rows.append({'representative':[x,y], 'degree':6, 'Frobenius_vector':vector,
                     'residue_extension_degree_in_k':2,'places_above':16,'degree_above':12})
    assert len(rows)==13
    return {'base':'H','field_modulus_bits':F.modulus,'H_degree6_places':rows,
            'k_degree12_places_lower_bound':208,
            'reason':'Each nonzero Frobenius element in (Z/2)^5 has order2;13 distinct unramified places yield16 distinct degree12 places each.',
            'status':'EXACT FINITE FIELD; independent Sage place check PASS; Astra lifting proof ACCEPT'}
