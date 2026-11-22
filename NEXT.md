# Après M3 — arrêter la recherche du score obstrué

Le cycle M3 produit une obstruction pour tous les conducteurs, les supports
rationnels et non rationnels, et les tailles de T, même après le renforcement
du critère local et le passage au rayon élémentaire. Voir M3_RESULT.md.
Le maximum de ce score sur k343 reste196608/620201. Ne plus rechercher une
amélioration de ce même score par davantage d'itérations.

La recherche dans les sous-corps quadratiques fournit 31 relations
explicites indépendantes de T-unités. Pour le module M2 fixé, la
descente par les normes prouve que l’inertie dans le groupe 2-primaire
complet a ordre 32 en chacune des deux places de degré 5 et ordre 64
en chacune des seize places de degré 6. En degré 8, les normes quadratiques
laissent un seul jet non nul possible. Une norme vers un sous-corps de
degré 4 l’exclut pour chacune des seize places, d’où une inertie d’ordre
256 et une contribution totale de 255 au degré moyen du conducteur.
Les deux places de degré 10 ont chacune une inertie d’ordre 1 024 et
contribuent ensemble pour 5115/128 au degré moyen du conducteur.
L’évaluation sur les 37 blocs donne en outre le rang exact 191 de l’image
des jets de T-unités, d’où 2^75 ≤ |G| ≤ 2^126.

En degré 12, une seule direction de jet isolé reste possible. L’existence
d’une T-unité qui la réalise départagerait les ordres 2 048 et 4 096.
L’ordre exact du groupe de rayon et ses facteurs cycliques, le raffinement
du théorème de relations et les nouvelles bases restent à étudier.
[Inerties de degré 5](proofs/M3_DEGREE5_INERTIA.md) ·
[Inerties de degré 6](proofs/M3_DEGREE6_INERTIA.md) ·
[Inerties de degré 8](proofs/M3_DEGREE8_INERTIA.md) ·
[Inerties de degré 10 et rang des jets](proofs/M3_DEGREE10_INERTIA.md) ·
[Relations indépendantes](results/M3_QUADRATIC_TUNIT_SEARCH.md).
Le pilote maximal-order
Sage a été borné à120secondes ; aucune relance lourde automatique n'est prévue.

La priorité bibliographique et une revue humaine restent ouvertes. M2 est
publié sur https://github.com/Njakasoa/ihara-a2-lab ; M3 est publié comme complément scientifique dans le même dépôt. Aucune soumission ni prise de contact ne découle de ces perspectives.
