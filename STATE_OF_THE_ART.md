# État de l’art de $A(2)$

**Mise à jour du 22 novembre 2026.** Le théorème 6.1 de la prépublication de
Ma, C. Xing et Z. Xing (v2 du 27 octobre) donne
**65536/206231 ≤ A(2) ≤ √2−1**, en combinant leur borne inférieure avec la
borne supérieure de Drinfeld–Vlăduţ. Le corps de genre 334 et la marge du
critère de tour ont été recalculés dans Sage. Le maximum M3 se rapporte à
la base de genre 343. [Addendum et reproduction](publication/THEOREM_6_1_M3.md)
· [Texte des auteurs](https://arxiv.org/html/2610.33649v2#S6.SS1).

Les sections suivantes conservent l’état bibliographique du **13 septembre 2026**.

## Convention et encadrement

Pour $N_q$g$$, le nombre maximal de points rationnels d’une courbe lisse,
projective et absolument irréductible de genre $g$ sur $\mathbf F_q$, on
écrit

\[
A(q)=\limsup_{g\to\infty}\frac{N_q$g$}g.
\]

La borne supérieure universelle de Drinfeld–Vlăduţ est

\[
A(q)\leq\sqrt q-1.
\]

Pour $q=2$, les sources primaires vérifiées donnent donc l’encadrement

\[
\boxed{\frac{24576}{77527}=0.316999238974809\ldots\leq A(2)
\leq\sqrt2-1=0.414213562373095\ldots}.
\]

La borne inférieure publiée la plus élevée que j’ai pu vérifier est celle de
Duursma–Mak (article paru en 2013). Leur **Théorème 1.3** imprime le nombre
`0.316999...`; la fraction ci-dessus est la forme exacte déduite de leur
**Théorème 1.1** et de la construction de la **Proposition 5.5**, et n’est pas
présentée sous cette forme dans l’article.

Pour cette construction, les données imprimées sont $a_1(k)=192$,
$g(k)=343$, et, pour l’ensemble ramifié $S$, 2 places de degré 5, 16 de
degré 6, 15 de degré 8 et 4 de degré 10. Leur majorant de conducteur moyen est

\[
f'=2\left(2\cdot5(1-2^{-5})+16\cdot6(1-2^{-6})
 +15\cdot8(1-2^{-8})+4\cdot10(1-2^{-10})\right)=\frac{33751}{64}.
\]

Ainsi

\[
\frac{192}{343-1+f'/2}
 =\frac{192}{342+33751/128}
 =\frac{24576}{77527}.
\]

La borne supérieure vient de V. G. Drinfeld et S. G. Vlăduţ, *The number of
points of an algebraic curve*, **Theorem 1**, Funct. Anal. Appl. 17 (1983),
53–54, [notice et texte](https://www.mathnet.ru/eng/faa1516),
[DOI](https://doi.org/10.1007/BF01083182).

## Chronologie vérifiée des bornes binaires

| Résultat (date du résultat ou de la publication) | Borne pour $A(2)$ | Source primaire et repère |
|---|---:|---|
| Ihara, article 1981 (la notice du dépôt porte le 20-02-1982) | — | Y. Ihara, *Some remarks on the number of rational points of algebraic curves over finite fields*, J. Fac. Sci. Univ. Tokyo 28 (1981), 721–724, [notice](https://doi.org/10.15083/00039603). Le papier introduit $A(q)$ et le cas carré; il ne fournit pas la borne binaire ci-dessous. |
| Serre, cours Harvard 1985 | $2/9=0.222222222222222\ldots$ | J.-P. Serre, *Rational Points on Curves over Finite Fields*, Cours no 6 (1985), Part II, construction pour $q=2$, [notice Numdam](https://numdam.org/item/CJPS_1985__6_/), [notes](https://www.math.rug.nl/~top/Serrelectures.pdf). La version révisée 2020 donne le repère **Théorème 5.11.1** ([édition SMF](https://smf.emath.fr/sites/default/files/2022-11/smf_doc-math_18__sample.pdf)); ce repère ne change pas la date du résultat de 1985. |
| Schoof, article 1992 | $2/9=0.222222222222222\ldots$ | R. Schoof, *Algebraic curves over $\mathbf F_2$ with many rational points*, J. Number Theory 41 (1992), 6–14, **Theorem 1.1**, [article](https://www.sciencedirect.com/science/article/pii/0022314X92900795), [DOI](https://doi.org/10.1016/0022-314X(92)90079-5), [PDF auteur](https://reneschoof.github.io/CurvesF2.pdf). L’abstract décrit une courbe de genre 19 avec un ensemble de quatre places rationnelles décomposées et une tour de corps de classes. |
| Niederreiter–Xing, article 1998 | $81/317=0.255520504731861\ldots$ | H. Niederreiter et C. Xing, *Towers of Global Function Fields with Asymptotically Many Rational Places and an Improvement on the Gilbert–Varshamov Bound*, Math. Nachr. 195 (1998), 171–186, [article/DOI](https://doi.org/10.1002/mana.19981950110). La construction est recopiée avec ses données $N_0=x^4$, $N_1=(x^2+x+1)(x^6+x^3+1)$, $[F:\mathbf F_2(x)]=84$, $|S|=81$ dans [Hajir–Maire, §4.1](https://www.math.uni-bielefeld.de/~rehmann/ECM/cdrom/3ecm/pdfs/pant3/maire.pdf). |
| Kuhnt, thèse soutenue 2002 (notice en ligne 2003) | $39/129=13/43=0.302325581395349\ldots$ | T. Kuhnt, *Generalizations of Golod–Shafarevich and applications*, thèse, University of Illinois at Urbana–Champaign, 2002, [notice institutionnelle](https://math.illinois.edu/academics/graduate/doctoral-graduates). Le résultat est localisé en **§11** par Duursma–Mak, **Remark 5.1**, qui donne explicitement $39/129$. |
| Xing–Yeo, article 2007 | $97/376=0.257978723404255\ldots$ | C. Xing et S. L. Yeo, *Algebraic curves with many points over the binary field*, J. Algebra 311 (2007), 775–780, [article](https://www.sciencedirect.com/science/article/pii/S0021869307001184), [DOI](https://doi.org/10.1016/j.jalgebra.2006.12.029). L’abstract annonce l’amélioration du meilleur résultat publié; la valeur exacte est reprise par Duursma–Mak, introduction. |
| Duursma–Mak, prépublication 2011–2012, article 2013 | $24576/77527=0.316999238974809\ldots$ | I. Duursma et K.-H. Mak, *On lower bounds for the Ihara constants $A(2)$ and $A(3)$*, Compositio Math. 149 (2013), 1108–1128, **Theorem 1.1**, **Theorem 1.3**, **Proposition 5.5**, [Cambridge/DOI](https://doi.org/10.1112/S0010437X12000796), [arXiv:1102.4127](https://arxiv.org/abs/1102.4127). L’arXiv date la v4 du 14-10-2012; la page Cambridge date la publication en ligne du 03-05-2013. |

La chronologie des publications et la chronologie numérique ne coïncident donc
pas parfaitement : la thèse de Kuhnt (2002), citée par Duursma–Mak, affiche une
valeur supérieure à celle de l’article Xing–Yeo (2007), alors que Xing–Yeo
améliorait le meilleur résultat **publié** qui leur servait de référence.

## Vérification de la période 2013–2026

Les travaux primaires retrouvés dans la fenêtre récente portent sur des
questions voisines ou sur d’autres corps finis :

- Hall-Seelig, *New lower bounds for the Ihara function $A(q)$ for small
  primes*, JNT 133 (2013), 3319–3324, [DOI](https://doi.org/10.1016/j.jnt.2013.04.002), annonce des améliorations pour $q=7,11,13$, pas pour $q=2$.
- Bassa–Beelen–García–Stichtenoth, *Galois towers over non-prime finite fields*,
  Acta Arith. 164 (2014), 163–179, [DOI](https://doi.org/10.4064/aa164-2-6), et *Towers of Function Fields over Non-prime Finite Fields*, Moscow Math. J. 15 (2015), 1–29, [DOI](https://doi.org/10.17323/1609-4514-2015-15-1-1-29) : les énoncés visent les corps non premiers et n’améliorent pas $A(2)$.
- Bassa–Ritzenthaler, *Good recursive towers over prime fields exist*, Math.
  Ann. 378 (2020), 599–604, [DOI](https://doi.org/10.1007/s00208-020-02039-9) : la construction exclut explicitement $q=2,3$.
- Faber–Grantham, *Binary curves of small fixed genus and gonality with many
  rational points*, J. Algebra 597 (2022), 24–46, [DOI](https://doi.org/10.1016/j.jalgebra.2022.01.008), et Dose–Lido–Mercuri–Stirpe, *Modular curves with many points over finite fields*, J. Algebra 635 (2023), 790–821, [DOI](https://doi.org/10.1016/j.jalgebra.2023.07.013) : résultats de genre fini, sans nouvelle limite asymptotique pour $A(2)$.
- Yoo–Lee, *Improvements of the Hasse–Weil–Serre bound over global function
  fields*, Finite Fields Appl. 101 (2025), article 102538,
  [DOI](https://doi.org/10.1016/j.ffa.2024.102538) : amélioration de bornes de comptage pour des corps/familles spécifiés; les résultats consultés ne donnent pas une nouvelle borne publiée pour la constante originale $A(2)$.
- *On an analogue of the Ihara constant for exponential sums*, volume 115
  annoncé pour octobre 2026, [DOI](https://doi.org/10.1016/j.ffa.2026.102866) : le sujet est un analogue $C(q)$ associé aux sommes exponentielles, et le fascicule est postérieur à la date de consultation; ce n’est pas une amélioration de $A(2)$.

Le constat documentaire à cette date est donc : je n’ai identifié aucune
publication primaire 2013–2026 donnant une borne strictement supérieure à
$24576/77527$ pour l’original $A(2)$. Il ne s’agit ni d’une preuve de
nouveauté ni d’une affirmation d’exhaustivité.

## Surveys et limites

La synthèse la plus utile pour le suivi est P. Beelen, *A survey on recursive
towers and Ihara’s constant*, arXiv:2203.03310 (2022), [§2.1 et tableau](https://arxiv.org/abs/2203.03310) : elle liste $2/9$, $81/317$, $97/376$, $39/129$ et $0.316999\ldots$, et qualifie la dernière borne de Duursma–Mak de meilleure connue dans cette synthèse. L’exposé antérieur de Hajir–Maire (2001), [§4.1](https://www.math.uni-bielefeld.de/~rehmann/ECM/cdrom/3ecm/pdfs/pant3/maire.pdf), donne un contrôle indépendant de la construction Niederreiter–Xing.

La couverture reste limitée aux requêtes consignées dans
[`references/frontier-search.md`](references/frontier-search.md), aux notices
arXiv/éditeurs accessibles et aux citations suivies depuis Duursma–Mak et
Beelen. Des prépublications non indexées, articles derrière des paywalls,
résultats formulés sans le nom $A(2)$, variantes de notation ou travaux
postérieurs peuvent manquer. La date de publication d’une source n’est jamais
remplacée par la date de cette recherche.

## Comparaison des méthodes et limites de reconstruction

Toutes les lignes inférieures concernent F₂. Les détails manquants restent
signalés ; le statut « source consultée » n'implique pas une reproduction locale.

| Année, valeur exacte | Méthode et base | Type de tour | Ingrédients de preuve / calcul | Limites du présent contrôle |
|---|---|---|---|---|
|1985,2/9 — Serre|Base non extraite des notices consultées|Corps de classes|Cours1985 ; repère de théorème dans l'édition2020|Construction détaillée à relire|
|1992,2/9 — Schoof|E de genre1, Y de genre6, X de genre19|Tour2 non ramifiée avec quatre places décomposées|Théorie des genres, GS, conducteurs, Riemann–Hurwitz ; résidus recalculés ici|Équation elliptique imprimée corrigée explicitement ; pas de calcul complet de Cl_S|
|1998,81/317 — Niederreiter–Xing|Base rationnelle, données cyclotomiques dans Hajir–Maire §4.1|Compositum et corps de classes|GS et calcul cyclotomique ; fraction contrôlée bibliographiquement|Reproduction locale complète non effectuée|
|2002,39/129=13/43 — Kuhnt|Base non extraite du texte intégral|Tour avec ramification contrôlée|Bornes de rangs, théorie des corps de classes|Valeur attestée par Duursma–Mak ; thèse intégrale non auditée|
|2007,97/376 — Xing–Yeo|Construction binaire décrite dans l'article|Corps de classes|Valeur exacte dans Duursma–Mak ; améliorations de rang commentées en remarque5.2|Notice primaire et citation, reproduction locale non effectuée|
|2013,24576/77527 — Duursma–Mak|H de genre2, k/H de degré32, g(k)=343, N(k)=192|Corps de rayon2-primaire puis tour2 non ramifiée|Matrices locales de rang5, conducteurs, places, GS, moyenne des conducteurs ; calculs exacts du laboratoire|Ordre et structure du corps de rayon auxiliaire non calculés ; inutiles à la simplification du quotient|
|1983,sqrt(2)−1 — Drinfeld–Vlăduţ|Toutes les courbes|Borne supérieure universelle|Méthode asymptotique des nombres de points|Aucune égalité déduite sur F₂|
