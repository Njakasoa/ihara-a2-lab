# Audit de nouveauté M2 : paramètres de Duursma–Mak

**Date de recherche : 2026-09-13 (Indian/Antananarivo).** La date ci-dessus est la
date de consultation des sources et des index publics ; elle ne doit pas être
confondue avec les dates de publication indiquées ci-dessous.

## Question auditée

Le point de départ est la construction de Duursma–Mak pour $A(2)$. Dans la
notation de leur article, on a une extension élémentaire de degré $32$ du corps
de fonctions de base de genre $2$, avec

\[
  g(k)=343,\qquad a_1(k)=N=192,
\]

et un support de ramification comportant $2$ places de degré $5$, $16$ de
degré $6$, $15$ de degré $8$ et $4$ de degré $10$. Leur valeur de conducteur est

\[
 f'=\frac{33751}{64},\qquad
 g(k)-1+\frac{f'}2=\frac{77527}{128}.
\]

Le quotient exact testé par le laboratoire est donc

\[
 \frac{192}{77527/128}=\frac{24576}{77527}
   =0.316999238974809\ldots .
\]

La question M2 est de savoir si une autre sélection de places, notamment avec
des degrés $>10$ (par exemple $12$), ou d'autres exposants de conducteur,
pourrait améliorer ce quotient dans le critère du théorème 1.1 de Duursma–Mak.
À la date de rédaction, aucun vecteur gagnant n'a été communiqué par le moteur
de recherche local ; ce fichier ne valide donc aucun gain numérique.

## Résultat de la recherche bibliographique

Dans la couverture explicitement listée ci-dessous, je n'ai trouvé ni article,
ni dépôt public décrivant une optimisation des paramètres du théorème 1.1 pour
la base précise $(g,N)=(343,192)$, ni une borne publiée explicitement supérieure
à $24576/77527$. Je n'en déduis pas une absence dans la littérature : il s'agit
d'un audit borné de sources indexées publiquement, sans prétention
d'exhaustivité ni de preuve de nouveauté.

Je n'ai pas trouvé de publication mentionnant une exploration systématique du
support de Duursma–Mak avec des places de degré $12$ ou davantage. Cette
absence de mention ne constitue pas une obstruction mathématique : elle laisse
ouverte une recherche computationnelle locale, qui doit être rapportée avec ses
paramètres, ses certificats et une comparaison exacte des fractions.

## Sources les plus proches

| Source (date de publication) | Résultat ou méthode pertinent | Limite pour M2 |
|---|---|---|
| **Duursma–Mak**, *On lower bounds for the Ihara constant $A(2)$*, arXiv:1102.4127v4 (14-10-2012) ; **Compositio Mathematica 149 (2013)**, DOI [10.1112/S0010437X12000796](https://doi.org/10.1112/S0010437X12000796), [arXiv](https://arxiv.org/abs/1102.4127) | Théorème 1.1 : critère de tour de corps de classes ; théorème 1.3 : borne pour $A(2)$ ; proposition 5.5 : la construction donnant $g=343$, $N=192$ et la valeur ci-dessus. Le repère universel est $A(2)\leq\sqrt2-1$ (Drinfeld–Vlăduț). | C'est le point de départ de l'audit, pas une étude publiée de l'optimisation des supports de degrés $>10$ autour de cette construction. |
| **Stichtenoth–Tutdere**, *Quadratic recursive towers of function fields over $\mathbf F_2$*, **Turkish Journal of Mathematics 39 (2015), 665–682**, DOI [10.3906/mat-1411-42](https://doi.org/10.3906/mat-1411-42), [page de l'article](https://journals.tubitak.gov.tr/math/vol39/iss5/6/) | Classifie des fonctions rationnelles susceptibles de définir des tours récursives quadratiques sur $\mathbf F_2$ et estime l'invariant positif $\beta_1$ des tours obtenues. | Famille récursive quadratique et invariant asymptotique ; aucune optimisation publiée retrouvée du support de ramification ou du conducteur dans le théorème 1.1 de Duursma–Mak, ni de certificat pour $(343,192)$. |
| **Hallouin–Perret**, *A graph aided strategy to produce good recursive towers over finite fields*, **Finite Fields and Their Applications (2016)**, DOI [10.1016/j.ffa.2016.07.008](https://doi.org/10.1016/j.ffa.2016.07.008) | Exemple de recherche assistée par graphe pour produire des tours récursives ; c'est le précédent méthodologique public le plus proche trouvé pour une recherche automatisée de tours. | L'espace de recherche et la notion de tour sont différents ; le résultat ne teste pas les supports de places du corps $k$ de Duursma–Mak et n'améliore pas la fraction ci-dessus. |
| Yoo–Lee, **Finite Fields and Their Applications 101 (2025)**, DOI [10.1016/j.ffa.2024.102538](https://doi.org/10.1016/j.ffa.2024.102538) | Travail récent retrouvé lors des recherches sur des améliorations de bornes Hasse–Weil–Serre pour des familles de corps de fonctions. | Je n'y ai pas trouvé d'optimisation du critère de Duursma–Mak, de support de degré $12$, ni de borne annoncée pour $A(2)$ dépassant $24576/77527$. |
| C. P. Mok–X. Wang, *On an analogue of the Ihara constant for exponential sums*, **Finite Fields and Their Applications 115 (numéro daté octobre 2026)**, article 102866, DOI [10.1016/j.ffa.2026.102866](https://doi.org/10.1016/j.ffa.2026.102866) | Résultat récent repéré dans l'indexation 2026, sur un analogue de la constante d'Ihara pour les sommes exponentielles. | Le numéro est postérieur à la date de recherche du 13-09-2026 et l'objet est un analogue, pas la constante originale $A(2)$ ; il ne constitue donc pas une amélioration M2 comptabilisée. |

Les recherches plus anciennes sur Schoof et les tours récursives, ainsi que les
enquêtes générales et les surveys sur $A(q)$, servent de contexte dans
`references/frontier-search.md`. Elles ne contiennent pas, dans les passages
consultés pour cet audit, un balayage des paramètres M2.

## Requêtes exécutées

Les chaînes suivantes ont été soumises telles quelles à la recherche web
publique (les variantes de casse et les résultats de navigation ne sont pas
interprétés comme des preuves d'absence) :

```text
"24576/77527" Ihara
"0.316999" "A(2)"
"33751/64" Ihara
"genus 343" "192" rational places F2
site:arxiv.org Ihara constant A(2) 2024 OR 2025 OR 2026
site:arxiv.org "Ihara" "F_2" "tower" 2024
site:github.com "Ihara" "A(2)"
site:github.com "Duursma" Mak function field
"Ihara constant" binary field tower recent
"Ihara constant" "F_2" class field tower
"Ihara constant" "degree 12" function field
"Duursma-Mak" class field tower
"A(2)" "Ihara's constant" 2023
"A(2)" "Ihara's constant" 2024
"A(2)" "Ihara's constant" 2025
"A(2)" "Ihara's constant" 2026
site:arxiv.org/abs "Ihara constant" "A(2)"
"best known" "A(2)" curves finite fields
"Ihara limit" "A(2)" lower bound
"A(2) ≥" "Ihara" curve
"Ihara function" "A(2)" 2024
"Ihara function" "A(2)" 2025
"lower bounds for A(q)" 2024 function fields
"lower bounds for A(q)" 2025 function fields
site:github.com "Stichtenoth" "Ihara"
site:github.com "class field tower" "F_2"
```

Les résultats GitHub accessibles par ces requêtes étaient des bibliothèques ou
des implémentations sans lien démontré avec l'optimisation M2. Les résultats
arXiv et web 2024–2026 retrouvés concernaient des tours récursives, des bornes
pour des familles particulières ou des analogues de $A(q)$ ; aucun ne fournissait
le vecteur de support/conducteur recherché ici.

## Limites et règle de lecture

* La recherche a porté sur les pages et PDF publics renvoyés par les index web,
  arXiv, les pages d'éditeurs et GitHub ; elle n'a pas couvert exhaustivement
  MathSciNet, zbMATH, les prépublications non indexées, les dépôts privés, les
  actes difficiles à indexer ou les résultats non publiés.
* Une date d'indexation 2026 ne remplace pas une date de publication : l'article
  Mok–Wang ci-dessus est signalé comme numéro d'octobre 2026, donc postérieur à
  la date de recherche.
* « Aucun résultat trouvé » signifie seulement « aucun résultat dans cette
  couverture et avec ces requêtes ». Le laboratoire ne doit annoncer une
  amélioration qu'après avoir produit un vecteur admissible, le calcul exact de
  $f'$, le dénominateur du théorème 1.1 et une fraction strictement supérieure à
  $24576/77527$.

## Complément après découverte automatique (racine, 2026-09-13)

L'énumération de référence a ensuite trouvé196608/620201. Requêtes web exactes :

```text
"Ihara" "196608" "620201"
"Ihara" "0.317006"
"Duursma" "degree 12" tower
"Ihara" "620201"
```

Aucun antécédent mathématique pertinent n'est apparu dans les résultats de ces
requêtes ; les résultats relâchant les contraintes étaient hors sujet
(applications médicales du nom Ihara, codes administratifs620201, pairings).
Ils ne sont pas utilisés comme sources scientifiques. Ce contrôle de chaîne
complète complète l'audit thématique précédent mais ne prouve pas la priorité.
Statut provisoire : POSSIBLY NOVEL ; amélioration de paramètres du théorème
existant, avec même base, et non nouveau théorème général de tours.
