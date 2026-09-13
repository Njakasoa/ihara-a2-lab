# M3 — résultat structurel et clôture du cycle borné

État : preuves acceptées par la revue Astra et validation indépendante PASS.
Les huit commandes de reproduction passent, dont40 tests unitaires et
les contrôles indépendants Sage/Python. Le reçu consolidé documente cette exécution. La borne M2 reste **A(2) ≥ 196608/620201**.

Le résultat principal est une obstruction plus large : sur la base k343,
le score élémentaire de rayon défini dans
[le critère raffiné](proofs/M3_REFINED_RAY_CRITERION.md) a pour maximum
196608/620201, pour tous les supports finis, tous les conducteurs ≥2,
avec places rationnelles ramifiées autorisées et T optimisé parmi les
ensembles rationnels disjoints de taille 1 à 192. Cette obstruction porte
sur ce score suffisant, pas sur les ratios réels des tours ni sur A(2).

Le critère utilise le rang local a=f⌊ν/2⌋ à la place du logarithme de
l'ordre local dans le terme de relations. Pour le sous-corps élémentaire
du corps de rayon, la moyenne locale maximale à ν=2s vaut exactement
2s−2(1−2^(−fs))/(2^f−1). C'est une meilleure estimation que celle du groupe
local complet dès s>1 ; elle concerne un choix de corps différent.
L'argument de relations s'applique aussi aux bases de rayon abéliennes
complètes et se généralise à d'autres caractéristiques.

[La preuve d'obstruction](proofs/M3_REFINED_OBSTRUCTION.md) réduit les
degrés et profondeurs arbitraires à 11 384 paires nécessaires (n,A).
Seule (0,266) subsiste, avec t=192. Deux inégalités de Cauchy éliminent
le dernier motif de profondeur supérieure à deux, puis l'obstruction M2
gelée termine la preuve. Les petits essais négatifs sont conservés.

L'axe de calcul exact a fourni un résultat partiel : cinq relations
indépendantes d'unités T dans les 266 coordonnées locales ramènent la
borne supérieure de l'ordre 2-primaire du groupe de rayon T-décomposé
de 2^317 à **2^312**. Sa borne inférieure reste 2^75. Les ordres des
inerties, le rang global exact et les facteurs cycliques restent inconnus.
Aucune diminution de la moyenne réelle des conducteurs M2 n'est certifiée.
Le pilote Sage de calcul global a atteint sa limite de 120 secondes ;
les calculs de composantes ont ensuite utilisé les corps résiduels exacts.

## Vérification et portée

- [Théorie locale](proofs/NONUNIFORM_CONDUCTOR_LOCAL_THEORY.md) : quotients
  finis, facteurs cycliques, caractères complets et d'ordre deux distingués.
- [Structure de rayon](results/RAY_CLASS_STRUCTURE.md) : données calculées,
  majorations et inconnues indiquées séparément.
- [Validation indépendante](results/M3_INDEPENDENT_VALIDATION.md) : seconde
  implémentation sans imports de production, neuf mutations rejetées.
- [Revue contradictoire Astra](results/M3_ASTRA_REVIEW.md) : acceptation
  mathématique ; la validation arithmétique indépendante a également passé.
- [Revue finale du périmètre et des échanges](results/M3_FINAL_SCOPE_REVIEW.md) :
  acceptation ; signe auxiliaire corrigé avant reproduction.
- [Audit bibliographique](references/M3_RAY_LITERATURE.md) : ingrédients
  standards ; priorité des applications et de l'obstruction non établie.

Commande complète, avec l'environnement Sage documenté du laboratoire :

```sh
python3 experiments/run_m3.py
```

Le reçu [results/m3-reproduction.json](results/m3-reproduction.json) associe les commandes, versions,
durées, sorties et hashes au commit exécuté. Les fichiers M2 gelés sont
vérifiés avant et après les expériences. Le pilote lent est exclu de cette commande. Son reçu d'archivage borné
est `results/m3-sage-pilot.json`.

Les sorties utiles sont SUCCESS-D (obstruction non uniforme) et SUCCESS-E
(principes d'échange et critère de relations amélioré). Aucun SUCCESS-A
ni calcul du groupe de rayon entier n'est revendiqué. La borne AG binaire
standard reste R+δ ≥ 1−1/b = −423593/196608, donc sans garantie positive.

Le cycle s'arrête après validation de ces résultats. Augmenter la recherche
du score maintenant obstrué n'apporterait rien. Une autre campagne devrait
apporter une information nouvelle sur les images d'inertie ou le rang global,
ou changer de famille après une décision scientifique explicite. Ce complément M3 accompagne maintenant M2 dans le dépôt public GitHub.
Il ne constitue pas une soumission à une revue ou à arXiv.
