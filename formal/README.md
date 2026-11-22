# M3 en Lean 4

Le théorème `IharaM3.genus343_maximum` établit que **196608/620201 est le maximum atteint du score élémentaire de M3** pour l’inventaire de la base de genre 343. Il quantifie sur tous les supports finis, tous les exposants de conducteur ≥ 2 et toutes les tailles admissibles de l’ensemble de places rationnelles décomposées. Les effectifs de degrés 1 à 12 sont ceux du certificat géométrique. Les effectifs de degrés ≥ 13 sont arbitraires. [Énoncé Lean](IharaM3/Maximum.lean) · [Inventaire Sage](../curves/k343-place-counts-30.json)

## Reproduire

Depuis la racine du dépôt, avec Elan et Python 3.10 ou ultérieur installés, exécuter

```sh
cd formal
lake exe cache get Mathlib.Data.Rat.Cast.Order Mathlib.Tactic.NormNum Mathlib.Tactic.Linarith Mathlib.Tactic.Positivity Mathlib.Tactic.Ring Mathlib.Order.Bounds.Basic
lake build
python3 check_certificates.py
```

Le projet fixe **Lean 4.34.1** et la révision **d13f23b** de mathlib. La première commande Lake récupère les dépendances précompilées. La deuxième compile les preuves et contrôle les axiomes dont dépendent les résultats. La commande Python fait vérifier par le noyau Lean sept égalités tirées des fichiers JSON du dépôt, dont les deux supports, le signe du polynôme et la valeur de chaque score. [Versions des dépendances](lake-manifest.json) · [Contrôle des certificats](check_certificates.py)

## Du théorème 6.1 au maximum de M3

| Étape | Ce que vérifie Lean |
|---|---|
| [Calcul du théorème 6.1](IharaM3/Theorem61.lean) | À partir des 28 caractères de conducteur de degré 20 et des trois de degré 14, la formule de genre impose 334. Pour le module imprimé, y compris l’exposant 3 au degré 6, le polynôme vaut −3/400 en 1/40. Le rapport vaut 65536/206231 sur k334 et 65536/209303 pour les mêmes choix de degrés et exposants sur k343. |
| [Réduction de tout support](IharaM3/Reduction.lean) | Toute amélioration stricte du score satisfait les inégalités de coût et de moment qui rendent l’énumération finie. Ces inégalités sont démontrées par induction sur un support dont le degré maximal et les conducteurs sont libres. |
| [Énumération des couples](IharaM3/Pairs.lean) | Il y a exactement 11 384 couples à examiner. Le seul cas restant a zéro place rationnelle ramifiée, une masse de rang de 266, 192 places décomposées et un moment compris entre 2236 et 2280. Le noyau vérifie le dénombrement. |
| [Exclusion du dernier cas](IharaM3/Terminal.lean) | La marge de 44 laisse sept couples possibles (degré, demi-profondeur). Les stocks et le moment imposent alors une remise totale d’au plus 2391/1024. Le score est donc au plus égal à la borne M3. Cette preuve utilise notamment l’effectif nul au degré 11. |
| [Atteinte et maximum](IharaM3/Maximum.lean) | Le témoin de conducteur 2 utilise respectivement 2, 16, 16, 2 et 1 places de degrés 5, 6, 8, 10 et 12. Lean vérifie son admissibilité et son score, puis réunit les deux conclusions dans un énoncé `IsGreatest`. |

## Portée de la preuve

Une entrée du support désigne une place par son degré et son exposant. Deux places distinctes de même degré peuvent figurer deux fois, dans la limite du stock disponible. Les places rationnelles ramifiées et les places décomposées se partagent le stock de 192. Le score utilise la demi-profondeur entière ⌊ν/2⌋, ce qui couvre les exposants pairs et impairs. [Définitions](IharaM3/Support.lean) · [Justification du score par les caractères élémentaires](../proofs/M3_REFINED_RAY_CRITERION.md)

Le lien avec les corps de fonctions s’appuie sur la reconstruction Sage des places et des conducteurs. Pour interpréter le résultat de genre 334 comme une borne inférieure de **A(2)**, on applique le critère d’infinitude de Ma, Xing et Xing. L’énoncé Lean de maximum porte sur le score du laboratoire sur k343. [Calcul géométrique Sage](../experiments/mxx_genus334_sage.py) · [Théorèmes 1.1 et 6.1 des auteurs](https://arxiv.org/html/2610.33649v2)

L’audit intégré autorise uniquement `propext`, `Classical.choice` et `Quot.sound`. La compilation échoue si un des résultats audités dépend d’un autre axiome, y compris celui qu’introduirait une preuve laissée en `sorry`. Le dénombrement des 11 384 couples compile sans dépendance axiomatique. [Audit des axiomes](IharaM3/Audit.lean)
