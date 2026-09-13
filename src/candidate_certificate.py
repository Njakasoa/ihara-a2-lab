"""Bind an automatically found nu2 row to explicit places and tower obligations."""
from fractions import Fraction
from copy import deepcopy
from baselines import dm_parameters
from baseline_certificate import assemble as baseline


def assemble(reference, inventories, degree12, geometry, zeta, baseline_selection):
    if len(reference['maximizers'])!=1:
        raise ValueError('this candidate binder requires one reference maximizer')
    winner=reference['maximizers'][0]
    pairs=list(zip(reference['degrees'],winner['multiplicities']))
    inventory={int(d):places for d,places in inventories.items()}
    inventory[12]=degree12
    support=[]
    for d,m in pairs:
        if not isinstance(m,int) or not 0<=m<=len(inventory[d]):
            raise ValueError('unavailable place multiplicity')
        support.extend(inventory[d][:m])
    if len({p['id'] for p in support})!=len(support):
        raise ValueError('support has duplicate places')
    t=winner['t']
    if not 0<t<=len(inventory[1]):raise ValueError('invalid splitting set size')
    arith=dm_parameters(343,t,pairs)
    C=sum(m*d*(d+1) for d,m in pairs)
    D=arith['generator_lower_bound']
    if not arith['inequality_passes']:raise ValueError('GS criterion fails')
    if (arith['ratio_lower_bound']!=winner['bound'] or winner['bound']!=reference['best_bound']
        or arith['genus_denominator_upper_bound']!=winner['denominator']
        or (arith['local_dimension'],C,D,arith['GS_margin'])!=(winner['A'],winner['C'],winner['D'],winner['GS_margin'])):
        raise ValueError('reference arithmetic does not match the actual row')
    cert=deepcopy(baseline(geometry,zeta,baseline_selection))
    cert.update({'id':'M2-K343-NU2-001','selected_splitting_places':[p['id'] for p in inventory[1][:t]],
        'selected_allowed_ramification_places':support,
        'modulus':[{'place_id':p['id'],'degree':p['degree'],'exponent':2} for p in support],
        'Golod_Shafarevich_parameters':{'generator_lower_bound':D,'relation_minus_generator_upper_bound':str(Fraction(C,2)+t-1),'local_dimension':winner['A'],'twice_local_relation_cost':C},
        'tower_infinitude_inequality':{'integer_margin':winner['GS_margin'],'comparison':f"{winner['GS_margin']} >= 0",'theorem':'Duursma–Mak1.1 /3.2 /4.1, p-primary convention'},
        'genus_denominator_upper_bound':winner['denominator'],'rational_place_numerator':t,
        'resulting_Ihara_ratio_lower_bound':winner['bound'],
        'average_conductor_degree_upper_bound':str(2*(Fraction(winner['denominator'])-342)),
        'exactness_status':['EXACT FINITE FIELD','EXACT INTEGER','EXACT RATIONAL'],
        'proof_status':'PROVED TOWER; level5: independent Sage PASS and Astra proof ACCEPT',
        'proof_obligations':['Discharged binary geometry/arithmetic/theorem obligations: results/INDEPENDENT_M2_VALIDATION.md and results/ASTRA_M2_REVIEW.md','Exact auxiliary ray degree and group structure are not required and remain uncomputed'],
        'coding_consequence':{'elementary_R_plus_delta_lower_bound':str(1-1/Fraction(winner['bound'])),'positive_guarantee':False},
        'novelty_status':'POSSIBLY NOVEL; bounded literature audit, not a priority proof',
        'automatic_discovery':{'script':'experiments/reference_nu2_search.py','result':'results/reference-nu2-search.json','improved_vector_supplied_to_search':False},
        'improvement_over_DM':str(Fraction(winner['bound'])-Fraction(24576,77527))})
    cert['ramification_indices']['K_over_k']['upper_bounds']={p['id']:2**p['degree'] for p in support}
    cert['extension_degree']['K_over_k_lower_bound']=2**D
    cert['extension_degree']['K_over_k_upper_bound']=2**(winner['A']+cert['class_group_data']['order_2_adic_valuation'])
    cert['ray_class_group_data']['p_rank_lower_bound']=D
    return cert
