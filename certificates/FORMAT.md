# Format de certificat et règles de lecture

Les rationnels sont des chaînes canoniques « numérateur/dénominateur ».
Les éléments finis sont des entiers encodant un polynôme sur F₂ ; le module
irréductible, son degré et l'ordre des coordonnées sont toujours fournis.
Une place est une orbite de Frobenius, décrite par son représentant minimal.
Les identifiants sont déterministes pour le module documenté, non absolus.

Champs minimaux d'une candidature :

- base_field, base_curve_equations, smooth_model_proof, geometric_irreducibility_proof ;
- genus, rational_places, splitting_T, ramification_S, modulus, place_degrees ;
- ramification_indices (valeurs certifiées, bornes ou « non calculé »), extension_degree ;
- class_group_data, ray_class_group_data, generator_rank_lower_bound ;
- relation_minus_generator_upper_bound, GS_margin, infinitude_status ;
- genus_denominator_upper_bound, rational_place_numerator, resulting_Ihara_lower_bound ;
- exactness_status, proof_level, proof_obligations, sources, novelty_status ;
- coding_consequence et independent_checks.

Une donnée inconnue est explicitement `null` avec une explication. L'ordre d'un
groupe ne remplace jamais sa structure. Une borne sur le conducteur moyen doit
être étiquetée « upper bound », même si cette borne numérique est calculée exactement.
`infinitude_status` ne vaut « PROVED TOWER » que si les données géométriques et
toutes les hypothèses du théorème sont établies. Un score admissible sur un
inventaire hypothétique reste conditionnel.

Pour la baseline : le certificat du corps fini k/H donne un degré exact32 et
des indices d'inertie exacts32 aux deux places5. Pour K/k (rayon2), le calcul
du groupe de rayon complet n'est pas fait. Chaque indice d'inertie est au plus
2^{deg P}. Le degré se simplifie dans la borne. La preuve peut donc être complète
pour l'inégalité A(2) tout en laissant l'ordre exact du corps auxiliaire inconnu ;
elle ne peut être présentée comme un calcul complet du groupe de rayon.

`ramification_S` désigne les places où la ramification est **permise**, c'est-à-dire
le support du module imposé. Cela n'affirme pas que chaque place ramifie dans
le quotient global après les relations de décomposition de T. La ramification
réelle de K/k doit rester inconnue lorsqu'on dispose seulement de bornes.
Cette convention diffère des deux places P₅ de k/H, dont la ramification totale
est effectivement prouvée par les matrices locales.
