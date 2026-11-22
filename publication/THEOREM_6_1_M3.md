# Reproduction du théorème 6.1 et portée de M3

**22 novembre 2026.** Le théorème 6.1 de Liming Ma, Chaoping Xing et Zugan Xing donne la borne inférieure **A(2) ≥ 65536/206231 = 0,3177795772701485…**. Cette fraction dépasse de **98828288/127904672431**, soit environ **0,00077267**, la borne de la note M2. M3 établit que le score suffisant du laboratoire atteint son maximum sur un corps fixé de genre 343. Les auteurs utilisent un corps de genre 334. [Prépublication, v2 du 27 octobre](https://arxiv.org/abs/2610.33649v2) · [Construction du §6.1](https://arxiv.org/html/2610.33649v2#S6.SS1) · [Énoncé de M3](../M3_RESULT.md)

## Reconstruction de la base

Les deux constructions partent du corps de genre deux défini sur le corps à deux éléments par

```text
H = F₂(x,y),   y² + (x³+x+1)y = x²+x.
```

Pour reproduire la construction du §6.1, Sage forme les cinq classes d’Artin–Schreier données par les fonctions `(x²+x)h/c²`, avec `c = (x⁴+x³+x²+x)y+x²+x+1` et `h = 1, x, x², x³, y`. Aux deux zéros de c, il développe les fonctions en séries locales et élimine le terme de pôle double par une translation d’Artin–Schreier. Les 31 caractères non triviaux ramifient à la place de degré 7, ce qui donne une extension de degré 32. Parmi eux, 28 ont un conducteur de degré 20 et trois un conducteur de degré 14. La formule conducteur-discriminant donne

```text
2g(k) − 2 = 32(2·2 − 2) + 28·20 + 3·14 = 666.
```

Les six places rationnelles de H se décomposent complètement. Le calcul des points du revêtement normalisé sur les extensions de F₂ jusqu’au degré 12 donne l’inventaire nécessaire ci-dessous. À la place de degré 3 de H, l’indice de ramification 8 et le degré résiduel 2 donnent bien **deux** places distinctes de degré 6 sur k. [Vérification géométrique Sage](../experiments/mxx_genus334_sage.py)

| Degré sur k | Places disponibles | Places choisies |
|---:|---:|---|
| 1 | 192 | 192 dans l’ensemble de décomposition T |
| 6 | 2 | Une d’exposant 2 et une d’exposant 3 dans le module |
| 8 | 16 | 16 d’exposant 2 |
| 10 | 96 | 12 d’exposant 2 |
| 12 | 240 | Une d’exposant 2 |

## Critère de tour et borne exacte

Dans le théorème 1.1, le rang local binaire est `n = f(ν−1−⌊(ν−1)/2⌋)` pour une place de degré f et d’exposant ν. Les exposants 2 et 3 donnent tous deux n = f. La somme des rangs vaut 272, d’où la minoration du rang global par d = 1 + 272 − 192 = 81. Pour p = 2, les termes de degré p se regroupent avec les termes quadratiques. Le polynôme du critère et un témoin rationnel sont

```text
P(τ) = 1 − 81τ + 1628τ² = (1 − 37τ)(1 − 44τ),
P(1/40) = −3/400 < 0.
```

Le théorème 1.1 implique alors l’infinitude de la tour. Pour chaque place choisie, le corollaire 5.5 majore la moyenne locale des exposants des conducteurs des caractères élémentaires par **2(1−2⁻ᶠ)**, y compris à la seconde place de degré 6 où ν = 3. La somme pondérée par les degrés donne une moyenne globale d’au plus **277701/512**. La formule de genre et les 192 places décomposées donnent

```text
D = 334 − 1 + (277701/512)/2 = 618693/1024,
A(2) ≥ 192/D = 65536/206231.
```

Sage vérifie les hypothèses numériques, l’inventaire et l’arithmétique exacte. L’implication entre le signe de P et l’infinitude de la tour est le théorème des auteurs. [Théorème 1.1](https://arxiv.org/html/2610.33649v2#S1) · [Corollaire 5.5](https://arxiv.org/html/2610.33649v2#S5)

## Comparaison à support fixé

Les mêmes **degrés, multiplicités et exposants** sont disponibles sur les deux corps. Avec 192 places décomposées, la partie locale du dénominateur et le témoin τ sont identiques. Le changement de genre ajoute exactement neuf au dénominateur sur k343. [Inventaire de k343](../curves/k343-place-counts-30.json) · [Score élémentaire de M3](../proofs/M3_REFINED_RAY_CRITERION.md)

| Construction | Score exact | Valeur approchée |
|---|---:|---:|
| Support du théorème 6.1, transporté sur k343 | 65536/209303 | 0,3131154 |
| Meilleur score M3 sur k343 | 196608/620201 | 0,3170069 |
| Support du théorème 6.1 sur k334 | 65536/206231 | 0,3177796 |

Pour ces données binaires, le test M3 appliqué à la nouvelle base donne déjà le polynôme ci-dessus et la même estimation des conducteurs. Le raffinement par Zassenhaus se compare dans l’article au critère historique de Duursma–Mak. L’amélioration sur le score **M3** s’explique ici par le changement de base. Le plafond de M3 continue donc à écarter toute recherche d’un meilleur score de cette forme sur k343. L’optimisation du support sur k334 est une question distincte de la reproduction du témoin des auteurs. [Comparaison du §6.2](https://arxiv.org/html/2610.33649v2#S6.SS2) · [Obstruction M3](../proofs/M3_REFINED_OBSTRUCTION.md)

## Rejouer le calcul

Depuis la racine du dépôt, avec SageMath 10.9, exécuter

```sh
sage -python experiments/reproduce_mxx_theorem61.py
```

Avec l’environnement conda du laboratoire, la commande équivalente est
`scripts/sage-python experiments/reproduce_mxx_theorem61.py`.

La commande reconstruit la géométrie, évalue les deux formules de l’article, compare les contributions locales avec l’implémentation M3 et vérifie le résultat champ par champ contre le certificat archivé. L’option `--write-certificate` régénère le JSON. [Programme de reproduction](../experiments/reproduce_mxx_theorem61.py) · [Certificat exact](../certificates/mxx-theorem61.json)
