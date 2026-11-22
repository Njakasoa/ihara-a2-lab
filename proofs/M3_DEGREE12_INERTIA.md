# Inertie de degré 12 et conducteur exact de la tour de genre 343

La place *k343-d12-001* a pour inertie $(\mathbf Z/2\mathbf Z)^{11}$,
d’ordre **2 048**, dans le corps de rayon abélien 2-primaire complet de M2.
Il existe une $T$-unité de premier jet **1043** à cette place et de jet
nul aux 36 autres, dans les cartes de l’inventaire. C’est la seule
direction non nulle possible sur ce bloc. On connaît dès lors les
37 ordres d’inertie et le degré moyen du conducteur, ce qui donne
$A(2)\ge 98304/310099$ sur la base de genre 343.
[Inventaire M2](../certificates/m2-tower.json) · [Majoration de la dimension du bloc isolé](M3_DEGREE10_INERTIA.md)

## La forme logarithmique qui réalise le jet

Sur $\mathbf F_2(x)$, posons $b=x^2+x$, $c=x^5+x^2+1$ et $q=x^2+x+1$.
Les trois premiers générateurs $w_0,w_1,w_2$ du laboratoire ont pour
seconds membres d’Artin–Schreier $b/c^2,bx/c^2,bx^2/c^2$.
Posons $U=w_0+w_2$, $V=w_1$, et
$$
E'=\mathbf F_2(x,U,V),\qquad E_0=\mathbf F_2(x,w_0,w_1,w_2).
$$
Ces corps ont degrés respectifs 4 et 8 sur la droite rationnelle. Les
trois coefficients de pôles simples réduits sont indépendants à $c=0$.
Cela se vérifie sur la droite dans la carte $x-x(R)$, également utilisée
dans $H$ qui s’y décompose. Ainsi le seul lieu ramifié de $E_0/\mathbf F_2(x)$
est le lieu de degré 5 défini par $c$, totalement ramifié de saut 1.
Les trois lieux $0,1,\infty$ se décomposent complètement. Écrivons $T_0$
pour leurs 24 prolongements dans $E_0$. Les places de $k$ au-dessus de
$T_0$ sont exactement les 192 places de $T$. [Calcul de ramification](FINITE_GEOMETRY.md)

Soit $p=x^{12}+x^{11}+x^{10}+x^8+x^5+x^4+x^3+x^2+x+1$. Dans $E'$,
formons les deux fonctions
$$
s=\frac{p}{xc^2}+\frac{q}{xc}U+\frac{xq}{c}V+UV,\qquad
B=s\,\frac{q^2}{(x+1)c}.
$$
Pour $\partial=d/dx$, le calcul symbolique donne **$\partial B=B^2$**.
Il s’effectue sur la base $1,U,V,UV$ en remplaçant $U^2+U$ par
$b(1+x^2)/c^2$ et $V^2+V$ par $bx/c^2$. La dérivée de chaque générateur
est la dérivée de son second membre. Les quatre coefficients de
$\partial B+B^2$ s’annulent identiquement dans $\mathbf F_2(x)$. Puisque
$B\ne0$, on obtient $\omega=B\,dx=d\log B$.

La forme $\omega$ est régulière hors de $0,1,\infty,c$ dans $E'$ par
les expressions ci-dessus. En un lieu où $\omega$ est régulière,
la valuation de $B$ est paire : une valuation impaire donne à $d\log B$
un pôle simple de résidu 1. Au-dessus de $c$, le passage de $E'$ à
$E_0$ a indice 2, donc la valuation de $B$ y devient paire aussi.
Ainsi le diviseur de $B$ **hors de $T_0$** est de la forme $2D$ sur $E_0$.

## Corriger le diviseur sans changer les jets

Le groupe des classes de degré zéro de $E_0$ a ordre impair. Voici une
vérification par les facteurs eulériens qui utilise seulement la ramification
ci-dessus. Hors de $c$, à un lieu de degré $d$ le degré résiduel est 1 ou 2.
Le produit des facteurs au-dessus de ce lieu est donc congru à
$(1-t^{8d})^{-1}$ modulo 2. À $c$, le facteur effectif est $(1-t^5)^{-1}$.
On obtient, en écrivant $P_{E_0}$ pour le numérateur de la fonction zêta,
$$
Z_{E_0}(t)\equiv Z_{\mathbf P^1}(t^8)\frac{1-t^{40}}{1-t^5},
\qquad P_{E_0}(t)\equiv(1+t+t^2+t^3+t^4)^7 \pmod 2.
$$
Ainsi $P_{E_0}(1)$ est impair. Un second calcul sous Sage donne sa valeur
entière $242\,658\,009\,902\,187$. Les sept sous-corps quadratiques sont
de genre 4 (un pôle réduit simple de degré 5) et leurs numérateurs zêta
se multiplient pour donner celui de $E_0$, car les sept caractères non
triviaux de son groupe sont quadratiques. Leurs nombres de classes sont
$139,89,101,111,99,129,137$. Le script contrôle aussi les décomptes de
points du corps de degré 8 sur les dix premières extensions de constantes.

Comme $T_0$ contient un lieu rationnel, le groupe des classes de diviseurs
hors de $T_0$ modulo les diviseurs principaux restreints est un quotient
de $\operatorname{Pic}^0(E_0)(\mathbf F_2)$. Il a donc aussi ordre impair.
Or $2[D]=0$ dans ce quotient. Il existe alors $z\in E_0^\times$ dont le
diviseur hors de $T_0$ est $D$. La fonction **$u=B/z^2$** est une
$T_0$-unité, donc une $T$-unité dans $k$, et $d\log u=B\,dx$.
Le certificat fournit la formule explicite de la différentielle et la
preuve d’existence du facteur correctif $z$.

## Vérification sur les 37 places

| Degré | Nombre de places | Calcul du premier jet de $u$ |
|---:|---:|---|
| 5 | 2 | Nul. Après division par le relèvement constant de son résidu, $u$ est congrue à 1 modulo l’idéal maximal de $E_0$. Cet idéal a ordre 4 dans $k$. |
| 6 | 16 | Nul. Dans la carte $y-y(P)$, $dx/dy=0$ au point et $B$ y est régulière. |
| 8 | 16 | Nul. Le facteur $q^2$ s’annule sur la fibre de $Q_4$ et $s$ y est régulière. |
| 10 | 2 | L’évaluation de $B$ dans la carte $x-x(P)$ donne zéro pour chacun des deux représentants. |
| 12 | 1 | Dans cette même carte, la valeur de $B$ dans $\mathbf F_{4096}$ est 1043 en base polynomiale binaire de module 4105. |

Le [programme Sage](../experiments/m3_degree12_unit.py) reconstruit
l’identité dans $E'$, vérifie les lieux ramifiés, parcourt les représentants
du support et recoupe le jet obtenu avec le [crible de degré 10](../results/m3-degree10-cartier.json).
Ce crible borne à un la dimension des relations de $T$-unités isolées en
degré 12. La relation réalisée donne donc $\rho_{12}=1$ et
$|I_{12}|=2^{12-1}=2048$.

## Effet sur la borne du laboratoire

Au conducteur 2, la contribution moyenne des $n$ lieux de degré $d$
et d’inertie d’ordre $i$ est $2nd(1-1/i)$. Les contributions du rayon
complet sont maintenant toutes exactes. [Formule de la moyenne](M3_RAY_DUALITY.md)

| Degré | Nombre | Ordre de l’inertie | Contribution |
|---:|---:|---:|---:|
| 5 | 2 | 32 | $155/8$ |
| 6 | 16 | 64 | $189$ |
| 8 | 16 | 256 | $255$ |
| 10 | 2 | 1 024 | $5115/128$ |
| 12 | 1 | 2 048 | $6141/256$ |
| **Total** | **37** | | **$134995/256$** |

Le degré moyen baisse de $3/512$ par rapport à la majoration M2.
Le critère d’infinitude de la tour est déjà satisfait pour ce support,
avec une marge de 41. En appliquant le théorème 1.1 de Duursma et Mak
au rayon 2-primaire complet avec $t=192$ et $g=343$, on trouve
$$
A(2)\ \ge\ \frac{192}{342+\tfrac12(134995/256)}
=\frac{98304}{310099}=0{,}3170084392403716\ldots .
$$
Le calcul sur ce corps de genre 343 améliore la fraction M2
$196608/620201$. Le maximum formalisé du score élémentaire M3 reste
$196608/620201$ pour le critère correspondant. Le théorème 6.1 de
Ma, Xing et Xing donne une borne globale plus forte, $65536/206231$,
avec une base de genre 334.
[Critère de tour de Duursma–Mak](https://arxiv.org/html/1102.4127v4#S1) ·
[Vérification du support M2](IMPROVED_BOUND.md) ·
[Comparaison avec le théorème 6.1](../publication/THEOREM_6_1_M3.md)

Les deux commandes suivantes rejouent la majoration de dimension puis
le calcul qui réalise la direction restante, sous Sage 10.9.

~~~sh
sage -python experiments/m3_degree10_cartier.py
sage -python experiments/m3_degree12_unit.py
~~~

Le [reçu du degré 12](../results/m3-degree12-unit.json) contient les jets
de chaque lieu, les facteurs zêta et les vérifications du calcul.
