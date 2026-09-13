# Audit de l’environnement d’arithmétique exacte

Audit exécuté le 13 septembre 2026 dans WSL2 Ubuntu 24.04.3 LTS, x86_64
(Linux 6.18.33.2-microsoft-standard-WSL2). La machine dispose de 16 CPU,
42 GiB de mémoire et 777 GiB libres sur le volume du projet. Le dépôt était
encore un squelette au moment de l’audit ; les calculs du laboratoire restent
donc dans `src/` et `reproduce.py`, avec une arithmétique Python sans dépendance
pour la première certification.

## Verdict opérationnel

Le chemin recommandé pour tous les calculs qui touchent aux corps de fonctions
est le préfixe Sage local :

```text
.runtime/sage
```

Il contient SageMath 10.9 (version publiée le 4 mai 2026), Python 3.14.7,
PARI/GP 2.17.3, FLINT 3.3.1, GAP 4.15.1, Singular 4.4.1.p5, cypari2 2.2.4,
SymPy 1.14.0, NumPy 2.5.3 et SciPy 1.18.1. L’installation est pilotée par
micromamba 2.9.0, lui aussi conservé sous `.runtime/`, avec le canal conda-forge
et la priorité stricte. Le graphe résolu contient 387 paquets et représentait
1 446 381 677 octets de téléchargement ; l’environnement lié occupe environ
5,43 GB et le cache de paquets environ 2,58 GB.

Les wrappers évitent `micromamba activate` et les écritures dans le `$HOME`
en lecture seule de ce runner :

```bash
scripts/sage-local --version
scripts/sage-local -python -c 'from sage.all import GF; print(GF(2**5).cardinality())'
scripts/gp-local --version
scripts/environment_audit.sh
```

`scripts/sage-local -python` et `scripts/sage-python` exportent `DOT_SAGE` vers
`.runtime/sage-home`. `scripts/micromamba-local` fixe le préfixe de cache à
`.runtime/mamba`. Tous les fichiers sous `.runtime/` sont ignorés par Git.

## Installation reproductible

Le manifeste minimal est [environment/sage-environment.yml](environment/sage-environment.yml)
et le reçu de versions et sommes SHA-256 est
[environment/runtime.lock](environment/runtime.lock). Pour recréer le préfixe
sur une machine Linux x86_64, télécharger l’archive micromamba dont le SHA est
dans le reçu, l’extraire sous `.runtime/micromamba`, puis lancer :

```bash
scripts/micromamba-local create \
  --file environment/sage-environment.yml \
  --prefix "$PWD/.runtime/sage"
```

La résolution conda peut évoluer ; le reçu conserve la date, les versions de
la pile scientifique et la taille du graphe observé. Une liste URL complète
peut être produite pour figer un runner donné avec :

```bash
scripts/micromamba-local list --explicit --prefix .runtime/sage
```

L’installation globale par `apt` n’était pas possible dans le runner (verrou
appartenant à `nobody` et option no-new-privileges). Un fallback autonome PARI
2.15.4 a donc été extrait dans `.runtime/pari` depuis les trois paquets Ubuntu
`pari-gp`, `libpari-dev` et `libpari-gmp-tls8t64`; leurs sommes figurent dans le
reçu. Sage/PARI 2.17.3 reste le chemin préféré.

## Matrice des composants

| Composant | État observé | Portée et limites |
| --- | --- | --- |
| Python système | Disponible, `/usr/bin/python3` 3.12.3 | `fractions.Fraction` est disponible ; Sage, cypari2, FLINT Python, SymPy, NumPy, SciPy et `galois` ne le sont pas dans cet interpréteur. |
| SageMath | Disponible dans `.runtime/sage`, 10.9 | Corps finis, courbes, corps de fonctions, groupe d’idéaux affine, Jacobien complet et Riemann–Roch passent les smoke checks ci-dessous. |
| PARI/GP | Disponible via Sage (`gp-2.17`) et fallback `scripts/gp-local` (`2.15.4`) | Factorisation, corps finis et groupe de classes de corps de nombres passent ; GP n’a pas fourni d’API directe de Riemann–Roch de corps de fonctions pour ce projet. |
| FLINT | Disponible comme bibliothèque Sage `libflint` 3.3.1 | Aucun `flint-config` ni module Python `flint` dans le système ; Sage et Singular l’emploient en interne. |
| GAP | Disponible dans le préfixe Sage, GAP 4.15.1 | Exécutable et bibliothèques présents ; aucun GAP système séparé. |
| Singular | Disponible dans le préfixe Sage, 4.4.1.p5 | Construit avec FLINT 3.3.1 et NTL 11.6.0 ; Sage utilise Brill–Noether pour certaines bases Riemann–Roch de courbes planes. |
| Julia / Nemo / Hecke | Non disponible | Aucun exécutable Julia ou paquet Nemo/Hecke n’a été trouvé ; aucune installation séparée n’a été lancée. |
| C / C++ | Disponibles | GCC/G++ système 13.3.0 ; les compilateurs conda-forge de la pile Sage sont également présents (16.2.0). |
| Git | Disponible, 2.43.0 | Le checkout courant est la branche `codex/ihara-lab` sans commit initial au moment de l’audit. |
| Magma | Non installé | Aucune licence ou installation commerciale utilisée. |

## Smoke checks effectivement exécutés

La commande canonique est `scripts/environment_audit.sh`; elle termine avec
`AUDIT_FAILURES=0`. Les lignes suivantes sont les résultats déterministes de
l’exécution du 13 septembre 2026 :

```text
SAGE_FINITE_FIELD=PASS field_size=32 generator_order=31 algebraic_roots=PASS
SAGE_POLYNOMIAL_FACTOR=PASS factors=(x - 1) * (x + 1) * (x^2 - x + 1) * (x^2 + x + 1)
SAGE_NUMBER_FIELD_CLASS_GROUP=PASS class_number=3
SAGE_FUNCTION_FIELD=PASS genus=2 constant_field=F2 degree1_places=6
SAGE_AFFINE_S_CLASS_GROUP=PASS order=1
SAGE_JACOBIAN=PASS order=19
SAGE_RIEMANN_ROCH=PASS divisor_degree=4 l(D)=3
PARI_FINITE_FIELD=PASS field_size=32 primitive_order=31
PARI_INTEGER_FACTOR=PASS
PARI_POLYNOMIAL_FACTOR=PASS
PARI_NUMBER_FIELD_CLASS_GROUP=PASS class_number=3
PARI_RIEMANN_ROCH=UNTESTED (GP has no project function-field RR API)
JULIA_NEMO_HECKE=UNAVAILABLE (no Julia executable)
AUDIT_FAILURES=0
```

Le test Sage du corps de fonctions est directement aligné sur la preuve de
`proofs/FINITE_GEOMETRY.md` :

\[
 H/F_2 : y^2+(x^3+x+1)y=x^2+x.
\]

Sage confirme le degré 2, le genre 2, le corps exact des constantes
\(\mathbf F_2\) et six places de degré 1. L’appel `H.class_group()` calcule
le groupe des idéaux de l’ordre maximal affine (le groupe d’idéaux
`S`-fractionnaires associé aux places retirées à l’infini) ; son ordre observé
est 1. Cette API est distincte de \(\operatorname{Pic}^0(H)(\mathbf F_2)\),
le groupe des points rationnels du Jacobien complet :
`H.jacobian(model='hess').group().order(algorithm='algebraic')` donne l’ordre
exact 19, en accord avec `H.L_polynomial() = 4*t^4 + 6*t^3 + 5*t^2 + 3*t + 1`
et le polynôme de Weil du certificat du projet. Pour la place à l’infini
\(P_\infty\), le diviseur \(D=4P_\infty\) a
\(\deg D=4\), une base Riemann–Roch de dimension \(\ell(D)=3\), et
`basis_function_space()` renvoie bien trois fonctions. Cela valide un chemin
réel de calcul Riemann–Roch ; cela ne constitue pas à lui seul une preuve de la
construction de degré 32 ni un calcul de groupe de classes de rayon demandé
par une tour. Le groupe d’idéaux affine ci-dessus ne doit donc pas être cité
comme un groupe de classes de rayon, ni comme le Jacobien complet.

Le contrôle indépendant sur \(\mathbf Q(\sqrt{-23})\) vérifie le nombre de
classes 3 et la structure cyclique d’ordre 3 avec Sage, et `bnfinit(x^2+23)`
vérifie le même nombre avec PARI. Pour les futurs calculs de tours, conserver
la distinction entre groupe de classes ordinaire, groupe de classes de rayon et
preuve d’une propriété de corps de fonctions : les smoke checks ne certifient
aucune infinitude de tour.

## Limites et invocation recommandée

Le calcul exact sans dépendance de `src/exact_curves.py` reste utile pour les
certificats binaires déjà produits. Pour une nouvelle courbe ou un diviseur,
utiliser Sage via `scripts/sage-local -python` et enregistrer l’équation, le
corps des constantes, le modèle normalisé, le genre, les places et les bases
Riemann–Roch. Utiliser `scripts/gp-local` seulement lorsque l’algorithme est
spécifiquement PARI ; le GP autonome ne remplace pas le chemin Sage pour les
corps de fonctions. Julia/Nemo/Hecke est une dépendance optionnelle à auditer
séparément si les calculs de Jacobiennes ou de groupes de classes de rayon le
requièrent.

## Verrouillage supplémentaire par la racine

`environment/conda-explicit-linux-64.txt` fige les387 archives effectivement
installées avec leurs URL et sommes MD5. Le fichier YAML reste une recette
souple ; utiliser la liste explicite pour retrouver exactement les builds :

```sh
scripts/micromamba-local create -p "$PWD/.runtime/sage" -f environment/conda-explicit-linux-64.txt
```

Les paquets binaires eux-mêmes restent ignorés par Git. La liste explicite
est réservée à linux-64 ; une autre plateforme nécessite sa propre résolution.

## Optional note compiler, added after result validation

Tectonic0.17.0 installed into .runtime/tex, independently of the Sage prefix.
No global package changes. Exact conda URLs/MD5 are recorded in
environment/tectonic-explicit-linux-64.txt. The wrapper scripts/tectonic-local
keeps all cache data under .runtime/tex-cache. The defaultv33 bundle ID observed
was6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c.
The note compiles successfully to4pages. Python3.12.3 with local PyMuPDF was
used to render and inspect all pages; the only remaining TeX warning is a
non-overflow underfull bibliography paragraph.
