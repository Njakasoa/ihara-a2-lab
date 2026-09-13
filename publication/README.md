# Note et reproduction

Le texte principal est [main.tex](main.tex) ; [main.pdf](main.pdf) est la note
compilée de quatre pages. Elle décrit le raffinement 196608/620201, sans
revendication de priorité. Le dépôt GitHub est public ; aucune soumission
à une revue ou à arXiv ni revue externe n’est annoncée.

Depuis la racine du laboratoire :

```sh
python3 publication/reproduce.py
python3 publication/reproduce.py --sage
python3 publication/reproduce.py --extended
scripts/tectonic-local --keep-logs publication/main.tex
```

Le premier reconstruit les données et tests essentiels, ainsi que le contrôle
indépendant de l'obstruction annexe ; --sage ajoute les deux implémentations
Sage indépendantes. --extended ajoute les recherches annexes,
sans être nécessaire à la preuve de la borne. L'environnement local doit être
installé selon ENVIRONMENT_AUDIT.md. Les listes exactes de paquets sont dans
environment/. Le petit checker de l'existence d'une place de degré12 est
indépendant du dépôt et n'exige que Python3 :

```sh
python3 publication/checkers/degree12.py
```

Il vérifie l'entrée finie supplémentaire de la note ; les propriétés publiées
de k, le théorème de tour et les autres inventaires ont leur propre audit M1.
Voir CONTRIBUTION_REVIEW.md et VALIDATION.md pour la portée des vérifications.
