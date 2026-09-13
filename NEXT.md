# Après M3 — arrêter la recherche du score obstrué

Le cycle M3 produit une obstruction pour tous les conducteurs, les supports
rationnels et non rationnels, et les tailles de T, même après le renforcement
du critère local et le passage au rayon élémentaire. Voir M3_RESULT.md.
Le maximum de ce score sur k343 reste196608/620201. Ne plus rechercher une
amélioration de ce même score par davantage d'itérations.

Le calcul exact fournit cinq relations T-unités et la borne |G|≤2^312,
mais ni le groupe complet ni les inerties individuelles. Une éventuelle
campagne future doit apporter une information nouvelle : relations globales
supportées sur un seul bloc, rang global effectif, correction plus fine du
théorème de relations, ou nouvelle famille de bases. Le pilote maximal-order
Sage a été borné à120secondes ; aucune relance lourde automatique n'est prévue.

La priorité bibliographique et une revue humaine restent ouvertes. M2 est
publié sur https://github.com/Njakasoa/ihara-a2-lab ; M3 est publié comme complément scientifique dans le même dépôt. Aucune soumission ni prise de contact ne découle de ces perspectives.
