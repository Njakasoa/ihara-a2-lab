# Résultat de la première exécution

Le laboratoire a produit une preuve vérifiée de

    A(2) ≥ 196608/620201 ≈ 0,317006905825692.

La sélection publiée de Duursma–Mak donnait24576/77527. Le gain exact est
368640/48082322927. Sur leur même courbe de genre343 à192 points rationnels,
l'échange de deux places de degré10 contre des places de degrés8 et12 réduit
le majorant du dénominateur de15/1024. La marge d'infinitude reste positive :41.

Le certificat porte sur les lieux eux-mêmes, avec leurs coordonnées et leurs
orbites de Frobenius. M1 reconstruit les contrôles historiques et les fonctions
zêta ; deux recherches automatiques convergent ; Sage vérifie indépendamment
le candidat et ses mutations négatives ; Astra accepte la preuve complète,
l'identité d'échange et la note. Niveau5 interne du laboratoire.

La contribution est un raffinement de paramètres du théorème existant.
L'audit séparé classe la nouveauté POSSIBLY NOVEL, avec priorité non établie.
Une note locale de4pages est compilée ; aucune soumission n'a été effectuée.
L'expression AG binaire élémentaire reste négative, donc aucun meilleur code
binaire n'est annoncé. Le degré exact et la structure du corps de rayon restent
inconnus et ne sont pas requis par le quotient démontré.

## Exploration et limites

- Nu2, k343, degrés≤12 : maximum du score certifié trouvé automatiquement.
- Voisinage de14 112 variantes locales de profondeurs2,4,6 : pas de gain.
- 373 sous-corps AS, supports de degrés≤12 : pas de gain sur le repère nouveau.
- Degrés≤30 surk343 : pas de gain après compression en états(A,C).
- Tous les degrés sur k343, supports non rationnels, nu2 : maximum du score
  conservateur prouvé égal à 196608/620201. Revue Astra et énumération
  indépendante PASS ; voir CLAIM-0003 et results/INDEPENDENT_OBSTRUCTION.md.

Les espaces non explorés incluent les supports rationnels, tous les modules
non uniformes, d'autres familles de courbes et des groupes de rayon exacts
permettant éventuellement de renforcer les estimations conservatrices.

## Livrables et reproduction

Lire README.md, proofs/IMPROVED_BOUND.md, certificates/m2-tower.json,
claims/CLAIM-0002.md et publication/main.pdf. Les preuves, sources primaires,
verrous d'environnement et rapports contradictoires sont inclus dans le dépôt.

```sh
python3 publication/reproduce.py
python3 publication/reproduce.py --sage
```

La première commande a été exécutée de bout en bout avec succès. Les deux
checkers Sage ont aussi passé leurs exécutions indépendantes et leurs reprises
par la racine. Les29tests internes passent. Les recherches annexes peuvent
être reconstruites séparément avec l'option --extended.
