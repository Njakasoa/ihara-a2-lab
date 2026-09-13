# Verdict M2 : amélioration de paramètre, 2026-09-13

## Verdict recommandé

**Étiquette : `POSSIBLY NOVEL (likely)`**, sous réserve d'un passage
arithmétique indépendant et d'une vérification ultérieure de priorité. Le
résultat est suffisamment distinct du repère publié pour justifier, si ces
vérifications passent, une courte note mathématique ou un addendum
computationnel. Il faut le présenter comme une amélioration de paramètres dans
la méthode existante, avec attribution explicite à Duursma–Mak ; ce n'est pas
un nouveau théorème général de tours et aucune action de publication n'est
recommandée ici.

## Ce qui a été vérifié

Les fichiers lus sont `proofs/IMPROVED_BOUND.md` et
`proofs/DEGREE_EXCHANGE_LEMMA.md`. Le candidat conserve exactement la même
construction de corps $k/\mathbf F_2$ que Duursma–Mak :

\[
  g(k)=343,\qquad N=a_1(k)=192.
\]

Il remplace les multiplicités de support, par degrés $(5,6,8,10,12)$,

\[
 (2,16,15,4,0)\longmapsto(2,16,16,2,1),
\]

avec tous les exposants $\nu_P=2$. La somme des degrés reste $A=266$ ; le
nouveau calcul donne $C=2260$, $D=1+A-N=75$ et

\[
 I=D^2-2C-4A=41>0.
\]

Ainsi le critère du théorème 1.1 de Duursma–Mak est appliqué à un autre module
sur le même corps. La preuve locale fait intervenir une place de degré $12$
disponible dans l'inventaire du certificat ; elle ne construit ni nouvelle
courbe, ni nouvelle équation récursive, ni nouveau critère de tour.

Le dénominateur conducteur majorant passe de

\[
 \frac{77527}{128}=\frac{620216}{1024}
 \quad\text{à}\quad
 \frac{620201}{1024},
\]

soit une diminution exacte de $15/1024$. Le calcul rationnel indépendant donne

\[
 \frac{196608}{620201}
   =0.3170069058256919934021389839745\ldots,
\]

contre

\[
 \frac{24576}{77527}
   =0.3169992389748087762972899763953\ldots,
\]

et

\[
 \frac{196608}{620201}-\frac{24576}{77527}
 =\frac{368640}{48082322927}>0.
\]

La décimale annoncée $0.317006905825692$ est donc l'arrondi correct. Cette
vérification porte sur les fractions et les identités de score ; elle ne
remplace pas l'audit indépendant des certificats de places, de la distinction
du support et de toutes les hypothèses du critère.

## Corollaire de paramètre ou nouveau résultat de tour ?

La classification correcte est :

* **corollaire paramétrique potentiellement nouveau** : le théorème de
  Duursma–Mak, son estimation moyenne du conducteur et sa tour de corps de
  classes sont réutilisés avec le support modifié ;
* **pas un nouveau théorème de tour** : aucun nouveau corps de base, aucune
  nouvelle famille récursive et aucun calcul exact du corps de rayon complet
  ne sont fournis ;
* **pas une preuve d'optimalité** : l'échange $(10,10)\to(8,12)$ montre une
  amélioration locale du score, mais ne borne pas les autres supports,
  exposants, conducteurs ou constructions ;
* **pas une valeur exacte de $A(2)$** : le résultat proposé reste une borne
  inférieure conditionnée par le critère de tour.

Une note courte est donc justifiée si l'arithmétique et les certificats passent,
avec un titre et un résumé qui disent « amélioration de la borne de Duursma–Mak
par changement de support » plutôt que « nouvelle tour » ou « meilleur résultat
prouvé au sens absolu ».

## Vérification de la littérature primaire la plus proche

1. **Duursma–Mak (publication 2013 ; prépublication v4 du 14-10-2012).**
   L'article *On lower bounds for the Ihara constants $A(2)$ and $A(3)$*
   emploie une variante de la méthode de tour de corps de classes de Serre. La
   fiche arXiv donne les auteurs, la date de v4 et la référence **Compositio
   Mathematica 149 (2013), 1108–1128** : [arXiv:1102.4127](https://arxiv.org/abs/1102.4127),
   [DOI 10.1112/S0010437X12000796](https://doi.org/10.1112/S0010437X12000796).
   Les références utilisées localement sont le théorème 1.1, le théorème 1.3
   et la proposition 5.5. La sélection publiée correspond au vecteur
   $(2,16,15,4,0)$ et fournit le repère $24576/77527$ dans les normalisations
   du laboratoire.

2. **Stichtenoth–Tutdere (publication 2015).** La page primaire de *Quadratic
   recursive towers of function fields over $\mathbf F_2$* décrit une
   classification de fonctions rationnelles définissant des tours récursives
   quadratiques et l'estimation des invariants $\beta_r$ : [page de l'article](https://journals.tubitak.gov.tr/math/vol39/iss5/6/),
   [DOI 10.3906/mat-1411-42](https://doi.org/10.3906/mat-1411-42). Cette étude
   est pertinente pour le contexte binaire et les recherches de tours, mais
   l'abstract et les métadonnées ne décrivent pas une optimisation du support
   de rayons du corps $(g,N)=(343,192)$ de Duursma–Mak.

3. **Hallouin–Perret (prépublication 2015, publication 2016).** Leur travail
   *A graph aided strategy to produce good recursive towers over finite fields*
   propose une méthode systématique utilisant le point de vue des graphes et
   des calculs Magma/Sage pour chercher des tours récursives :
   [arXiv:1503.06591](https://arxiv.org/abs/1503.06591), [article FFA 42
   (2016), 200–224](https://www.sciencedirect.com/science/article/pii/S1071579716300478),
   [DOI 10.1016/j.ffa.2016.07.008](https://doi.org/10.1016/j.ffa.2016.07.008).
   C'est un précédent d'automatisation, pas un antécédent identifié de
   l'optimisation des degrés de support dans le critère de Duursma–Mak.

Les recherches récentes ciblées n'ont pas révélé, dans les résultats publics
consultés, de publication 2025–2026 annonçant cette fraction ou cette
modification de support. Un résultat 2026 repéré sur un **analogue** de la
constante d'Ihara pour des sommes exponentielles est hors objet : [Mok–Wang,
DOI 10.1016/j.ffa.2026.102866](https://doi.org/10.1016/j.ffa.2026.102866).
Son numéro étant daté octobre 2026, il est en outre postérieur à la date de
recherche du 13 septembre 2026.

## Requêtes exactes de contrôle

Exécutées le 13-09-2026, indépendamment de l'énumération locale :

```text
"196608/620201" Ihara
"0.317006905825692" Ihara
"Duursma Mak" "degree 12"
"Duursma Mak" "A(2)" 2025 OR 2026
"196608/620201"
"0.3170069058"
```

Les résultats pertinents renvoyaient au papier Duursma–Mak, à des travaux
généraux sur les tours récursives ou à des résultats hors sujet ; aucun article
ou dépôt public identifié par ces chaînes ne donnait le vecteur
$(2,16,16,2,1)$, la fraction $196608/620201$ ou une amélioration explicitement
attribuée au théorème 1.1. Cette observation est une borne de recherche, pas une
preuve d'absence ni une preuve de priorité.

## Portée et recommandation

La date de consultation est le **13-09-2026** ; les dates de publication sont
indiquées séparément ci-dessus. La couverture est limitée aux pages, PDF et
index publics rencontrés par ces requêtes, arXiv, les pages d'éditeurs et les
dépôts publics. Elle n'est pas une recherche exhaustive de MathSciNet, zbMATH,
prépublications non indexées, résultats non publiés ou dépôts privés.

Recommandation opérationnelle : si un second calcul arithmétique et les
certificats locaux passent, conserver l'étiquette **POSSIBLY NOVEL (likely)**
et préparer une note courte centrée sur la conséquence paramétrique exacte
$A(2)\ge196608/620201$. Ne pas employer « priorité établie », « optimalité » ou
« nouvelle tour » sans audit bibliographique et mathématique supplémentaires.
