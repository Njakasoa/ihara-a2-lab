# Après M3 — arrêter la recherche du score obstrué

Le cycle M3 produit une obstruction pour tous les conducteurs, les supports
rationnels et non rationnels, et les tailles de T, même après le renforcement
du critère local et le passage au rayon élémentaire. Voir M3_RESULT.md.
Le maximum de ce score sur k343 reste196608/620201. Ne plus rechercher une
amélioration de ce même score par davantage d'itérations.

La recherche dans les sous-corps quadratiques porte le rang certifié des
relations de T-unités à 31 et donne |G|≤2^286. Pour le module M2 fixé, la
descente par les normes prouve que l’inertie dans le groupe 2-primaire
complet a ordre 32 en chacune des deux places de degré 5 et ordre 64
en chacune des seize places de degré 6. En degré 8, les normes quadratiques
laissent un seul jet non nul possible. Une norme vers un sous-corps de
degré 4 l’exclut pour chacune des seize places, d’où une inertie d’ordre
256 et une contribution totale de 255 au degré moyen du conducteur.
La recherche d’une relation isolée en degrés 5, 6 et 8 est donc close.
Les inerties des deux places de degré 10 et de la place de degré 12,
le rang global effectif, le raffinement du théorème de
relations et les nouvelles bases restent des pistes.
[Inerties de degré 5](proofs/M3_DEGREE5_INERTIA.md) ·
[Inerties de degré 6](proofs/M3_DEGREE6_INERTIA.md) ·
[Inerties de degré 8](proofs/M3_DEGREE8_INERTIA.md) ·
[Relations indépendantes](results/M3_QUADRATIC_TUNIT_SEARCH.md).
Le pilote maximal-order
Sage a été borné à120secondes ; aucune relance lourde automatique n'est prévue.

La priorité bibliographique et une revue humaine restent ouvertes. M2 est
publié sur https://github.com/Njakasoa/ihara-a2-lab ; M3 est publié comme complément scientifique dans le même dépôt. Aucune soumission ni prise de contact ne découle de ces perspectives.
