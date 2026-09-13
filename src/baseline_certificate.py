"""Assemble the full published binary tower certificate; unknowns stay explicit."""
from baselines import published_controls


def assemble(geometry,zeta,selected):
    if (geometry['H_genus'],geometry['k_genus'],geometry['k_degree_over_H']) != (2,343,32):
        raise ValueError('finite geometry does not match the published baseline')
    if len(selected['splitting_T'])!=192 or len(set(selected['splitting_T']))!=192:
        raise ValueError('splitting inventory does not contain192 distinct places')
    arith=published_controls()['duursma_mak_343']
    order=zeta['k_jacobian_order']
    valuation=0
    while order%2==0:
        order//=2; valuation+=1
    return {
      'id':'DM-343-BASELINE','base_field':'F2','base_function_field':'k343',
      'base_curve_equations':['H: y^2+(x^3+x+1)*y=x^2+x',
        'k/H: v_i^2+(x^5+x^2+1)*v_i=(x^2+x)*h_i; h=[1,x,x^2,y,y^2]'],
      'smoothness_certificate':'smooth projective normalization; proofs/FINITE_GEOMETRY.md',
      'geometric_irreducibility_certificate':'nonzero reduced poles; both five-column residue maps rank5',
      'full_constant_field_certificate':'F2-rational places on the geometric cover; nonempty split T in tower',
      'genus':343,'rational_place_count':192,'rational_place_inventory':'curves/k343-places.json',
      'selected_splitting_places':selected['splitting_T'],
      'selected_allowed_ramification_places':selected['ramification_S'],
      'modulus':[{'place_id':p['id'],'degree':p['degree'],'exponent':2} for p in selected['ramification_S']],
      'ramification_indices':{
        'k_over_H':{'both_degree5_places':32,'residue_degrees':1,'certificate':'certificates/dm-finite-geometry.json'},
        'K_over_k':{'exact':None,'upper_bounds':{p['id']:2**p['degree'] for p in selected['ramification_S']},
          'note':'allowed places can become unramified after splitting relations; no exact inertia claim'}},
      'extension_degree':{'k_over_H':32,'K_over_k':None,'K_over_k_lower_bound':2**arith['generator_lower_bound'],
                          'K_over_k_upper_bound':2**(arith['local_dimension']+valuation),
                          'note':'bounds only; auxiliary degree cancels in the asymptotic ratio'},
      'class_group_data':{'Jac_k_order':zeta['k_jacobian_order'],'order_2_adic_valuation':valuation,
                         'structure':None,'certificate':'certificates/k343-zeta.json'},
      'ray_class_group_data':{'definition':'maximal abelian2 quotient with modulus m and T split',
                             'exact_order':None,'invariant_factors':None,'p_rank_lower_bound':75},
      'Golod_Shafarevich_parameters':{'generator_lower_bound':75,'relation_minus_generator_upper_bound':1317,
                                    'local_dimension':266,'twice_local_relation_cost':2252},
      'tower_infinitude_inequality':{'integer_margin':57,'comparison':'57 >= 0',
                                   'theorem':'Duursma–Mak1.1 /3.2 /4.1, p-primary convention'},
      'genus_denominator_upper_bound':'77527/128',
      'rational_place_numerator':192,'resulting_Ihara_ratio_lower_bound':'24576/77527',
      'average_conductor_degree_upper_bound':'33751/64',
      'exactness_status':['EXACT FINITE FIELD','EXACT INTEGER','EXACT RATIONAL'],
      'proof_status':'known published bound; local reconstruction; see live gate results/M1_STATUS.md',
      'proof_obligations':['See results/M1_STATUS.md and results/ASTRA_M1_REVIEW.md for independent verification gate',
        'Exact auxiliary ray degree and group structure are not computed and not required by this bound'],
      'coding_consequence':{'elementary_R_plus_delta_lower_bound':'-52951/24576','positive_guarantee':False},
      'novelty_status':'KNOWN','source':'https://arxiv.org/abs/1102.4127'}
