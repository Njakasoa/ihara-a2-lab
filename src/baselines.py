"""Exact published tower arithmetic. No candidate search in this M1 module."""
from fractions import Fraction


def dm_parameters(genus, t, places):
    """Duursma–Mak (1.1) and conductor-2 averaging for q=2.

places is [(degree,multiplicity)]. Existence of these places and genus are
external proof obligations; this function only checks the theorem arithmetic.
"""
    if genus <= 1 or t <= 0 or any(d <= 1 or m < 0 for d, m in places):
        raise ValueError('require g>1, t>0, nonrational disjoint places')
    dimension = sum(d*m for d, m in places)
    local_relations = sum(m*d*(d+1) for d, m in places)
    margin = (1+dimension-t)**2 - 2*local_relations - 4*dimension
    genus_cost = sum(m*d*(1-Fraction(1,2**d)) for d, m in places)
    denominator = genus-1+genus_cost
    return {'genus':genus, 't':t, 'places':places, 'p':2, 'constant_degree':1,
            'conductor_exponent':2, 'local_dimension':dimension,
            'generator_lower_bound':1+dimension-t,
            'GS_margin':margin, 't_le_dimension': t <= dimension,
            'inequality_passes': t <= dimension and margin >= 0,
            'genus_denominator_upper_bound':str(denominator),
            'ratio_lower_bound':str(Fraction(t,1)/denominator),
            'coarse_ratio':str(Fraction(t,genus-1+dimension)),
            'status':'EXACT RATIONAL',
            'geometry_status':'EXTERNAL PROOF OBLIGATION'}


def published_controls():
    return {
        'duursma_mak_343': dm_parameters(343,192,[(5,2),(6,16),(8,15),(10,4)]),
        'duursma_mak_276': dm_parameters(276,160,[(5,1),(8,27),(10,1)])
    }
