# Un jet isolé améliore la borne du théorème 6.1 sur la base de genre 334

Pour un support explicite dans les fibres indiquées au §6.1 de Ma, Xing et
Xing, la place de degré 12 a une inertie d’ordre **2 048** dans leur rayon
élémentaire. Le premier jet de valeur **3400** y donne une relation avec
zéro aux trente autres places du module. Le gain sur le dénominateur du
rapport de tour est $3/1024$, d’où
$$
A(2)\ \ge\ \frac{32768}{103115}=0{,}3177811181690346\ldots .
$$
La fraction de départ est $65536/206231$. Nous utilisons la même courbe,
les mêmes multiplicités et le même critère d’infinitude. [Théorème 6.1, v2](https://arxiv.org/html/2610.33649v2#S6.SS1) · [Reproduction de la borne de départ](../publication/THEOREM_6_1_M3.md)

## Choix des places

Posons $a=x^3+x+1$, $b=x^2+x$, $q=x^2+x+1$,
$H=\mathbf F_2(x,y)$ avec $y^2+ay=b$, et
$c=(x^4+x^3+x^2+x)y+q$. Sur $H$, le corps $k$ de genre 334 est engendré
par cinq $w_i$ vérifiant $w_i^2+w_i=bh_i/c^2$, avec
$(h_0,\ldots,h_4)=(1,x,x^2,x^3,y)$. Son groupe de Galois sur $H$ agit par
les 32 translations binaires des $w_i$. Les deux zéros de $c$ sont
$R_3,R_7$, de degrés 3 et 7. Leurs indices de ramification dans $k/H$
valent 8 et 32, leurs degrés résiduels 2 et 1, et leurs exposants de
différente 14 et 62. Ce sont des extensions de saut 1 sur leur partie
non ramifiée. Les six places rationnelles de $H$ se décomposent en
$|T|=192$ places. [Calcul de la géométrie](../experiments/mxx_genus334_sage.py)

Les auteurs donnent les fibres qui assurent l’existence des places, puis
fixent les degrés et multiplicités du module. Les étiquettes individuelles
ci-dessous rendent ce choix reproductible. Dans chaque fibre non ramifiée,
la translation de Frobenius $t$ regroupe les 32 points géométriques en
seize paires. L’étiquette est le plus petit entier de la paire
$\{g,g\mathbin{\mathrm{xor}}t\}$, relativement au point de départ du reçu.
Les cartes régulières ont pour paramètre $x-x(P)$.

| Degré sur $k$ | Lieu de $H$ | Choix sur $k$ |
|---:|---|---|
| 6 | $R_3$ | Les deux places. Le caractère de masque 11 y prend les résidus 4 et 5 sur $\mathbf F_8$, d’exposants respectifs 2 et 3 dans le module. |
| 8 | $Q_4$ au-dessus de $q$ | Les seize places. |
| 10 | $Q_5$ au-dessus de $x^5+x^2+1$ où le masque 4 se décompose et le masque 8 est inerte | Les douze étiquettes $0,1,2,3,4,5,6,7,16,17,18,19$, avec $t=8$. |
| 12 | $Q_6$ au-dessus de $x^6+x^3+1$ où le masque 1 se décompose et le masque 2 est inerte | L’étiquette 0, avec $t=2$. |

Toutes les places de degrés 8, 10 et 12 ont exposant 2. Les polynômes des
corps finis, les points de départ et leurs orbites sont reconstruits par
le [programme de sélection](../experiments/mxx_degree12_support.py) et publiés
dans le [reçu du support](../results/mxx-degree12-support.json).

## Quelles relations comptent dans le rayon élémentaire ?

Dans le corps de rayon élémentaire $K=k^T_{\mathfrak m}$ du théorème 1.1,
les carrés locaux ont une image triviale par réciprocité. Aux exposants
2 et 3 le quotient élémentaire des unités principales est donc, dans les
deux cas, le groupe additif du corps résiduel. En particulier, en
caractéristique 2, $1+b_2t^2$ est un carré modulo $t^3$ pour tout
coefficient résiduel $b_2$. Le premier jet suffit aussi à la place
d’exposant 3. [Construction du corps du théorème et corollaire 5.5](https://arxiv.org/html/2610.33649v2#S5)

Soit $f\in k^\times$ de valuations paires hors de $T$. En chaque place
du support $S$, on retire un carré local pour rendre $f$ inversible, puis
sa constante résiduelle, elle aussi carrée. Le premier jet qui subsiste est
le coefficient de $d\log f$ dans le paramètre local. Son vecteur dans le
produit des blocs de $S$ est une relation dans $\operatorname{Gal}(K/k)$.
Réciproquement, une relation est représentée dans les idèles par le
produit d’un élément principal, d’un carré et des sous-groupes locaux du
rayon. En dehors de $S\cup T$ ces sous-groupes sont les unités, en $S$
ce sont les unités congrues à 1 modulo le module, et en $T$ le corps
local entier est autorisé. L’élément principal a donc valuation paire
hors de $T$ et donne les jets de la relation. La décomposition d’un lieu
rationnel dans $T$ assure la condition sur les constantes.

Ainsi l’espace des jets isolés au lieu de degré 12 est exactement l’image,
en ce lieu, des $d\log f$ ci-dessus qui ont leurs trente autres jets nuls.
Sa dimension $\rho$ donne l’ordre d’inertie $2^{12-\rho}$. Les fonctions
à diviseur pair hors de $T$ suffisent pour cet argument élémentaire.
Le [calcul antérieur sur la base de genre 343](M3_DEGREE12_INERTIA.md)
demandait une correction supplémentaire par un carré pour produire une
véritable $T$-unité dans le rayon complet.

## La trace borne l’espace de recherche

Une forme $\omega=d\log f$ comme ci-dessus a des pôles au plus simples
sur $T$ et est régulière ailleurs. Si son jet est nul en une place hors
de $T$, elle y a un zéro d’ordre au moins deux. En effet, après le retrait
des carrés, la dérivée d’une unité en caractéristique 2 ne reçoit de
contribution que des puissances impaires du paramètre.

Sur $H$, la différentielle $\gamma=q^2dx/(ab)$ a pour diviseur
$2Q_4-T_H$, où $T_H$ est la somme des six places rationnelles. On le
voit à partir de $\operatorname{div}(dx)=2R_3-2T_\infty$ et des zéros
de $q,a,b$, où $T_\infty$ désigne la somme des deux infinis. Écrivons
$F=\omega/\gamma=\sum_I A_I w_I$, $w_I=\prod_{i\in I}w_i$.
La fibre de $Q_4$ est complète et de jets nuls, donc $F$ y est régulière.
Les pôles possibles de $F$ sont au-dessus de $R_3,R_7$. En $R_3$ la
relève de $\gamma$ a ordre 14 et $\omega$ a ordre au moins deux, d’où
$v_k(F)\ge-12$. En $R_7$ la relève a ordre 62 et $\omega$ est régulière,
d’où $v_k(F)\ge-62$.

La base duale pour la trace donne
$A_I=\operatorname{Tr}_{k/H}(F\prod_{j\notin I}(1+w_j))$. Posons
$m=5-|I|$. Là où l’indice de ramification est $e$, les $w_i$ ont
valuation au moins $-e$ par leurs équations. Pour une différente
d’exposant $\delta$, la trace locale de $\mathfrak m_k^r$ est contenue
dans $\mathfrak m_H^{\lfloor(r+\delta)/e\rfloor}$. Cela borne à $m$
l’ordre du pôle de $A_I$ en chacun de $R_3,R_7$. En $R_3$, la somme des
deux traces locales satisfait la même inclusion. Ailleurs les
coefficients sont réguliers. Ainsi $A_I\in L(m(R_3+R_7))$.

La dimension de cet espace en genre 2 vaut $10m-1$ pour $m\ge1$ et 1
pour $m=0$. Voici la base utilisée dans le certificat. Écrivons
$A_I=P_I/c^m$. Aux deux infinis, les pôles permis de $P_I$ ont ordres
au plus $3m$ et $7m$, respectivement. Dans la branche où $y\sim1/x$,
prenons les $x^i$ jusqu’à $i=3m$ et les $x^j y$ jusqu’à $j=7m-3$ en
retirant de ces derniers les termes en $x$ de degré supérieur à $3m$
à cet infini. À l’autre infini $y$ a un pôle d’ordre trois.
Ces éléments respectent donc les deux bornes. Leur indépendance résulte
de celle de $1,y$ sur $\mathbf F_2(x)$, et leur nombre atteint la
dimension annoncée. Pour $m=0$ on garde la constante. Le total est
$49+5\cdot39+10\cdot29+10\cdot19+5\cdot9+1=\mathbf{770}$ colonnes.

## Calcul symbolique et réalisation de la direction restante

Soit $B$ le coefficient de $\omega$ sur $dx$. La dérivation
$\partial=d/dx$ satisfait $\partial^2=0$ car $x$ est séparante en
caractéristique 2. Une différentielle logarithmique vérifie donc
$\partial B=B^2$. Réciproquement, toute solution $B\ne0$ donne
$B\,dx=d\log B$. L’identité est linéaire sur $\mathbf F_2$.

Avec $V_i=cw_i$, une colonne s’écrit
$B=q^2P_I V_I/(abc^5)$. Le programme réduit l’identité rationnelle
sur $1,y$ et les 32 monômes $V_I$ à l’aide de $y^2=ay+b$ et
$V_i^2=cV_i+bh_i$. La matrice a **rang 702 sur 770**. L’annulation
des jets aux douze lieux de degré 10 laisse **une seule dimension**
parmi les 68 restantes. Le certificat donne la solution sous la forme
$$
B=\frac{q^2}{abc^5}\sum_{I} (p_I(x)+r_I(x)y)V_I .
$$
Dans le tableau, le bit $j$ d’un entier représente le coefficient de $x^j$.

| Masque de $I$ | $p_I$ | $r_I$ |
|---:|---:|---:|
| 0 | 1341628902 | 3347338846 |
| 4 | 2802548 | 7813815 |
| 16 | 26746098 | 47491250 |
| 20 | 96686 | 247597 |

Il reste à vérifier que cette solution donne une relation globale. Elle
appartient au sous-corps quartique $E=H(w_2,w_4)$. En $R_3$, les trois
caractères de $E/H$ (4, 16 et 20) sont ramifiés. Il y a un seul
prolongement dans $E$, de degré résiduel 1. Le déterminant de la
multiplication par $B$ dans la base $1,V_2,V_4,V_2V_4$ donne
$v_{R_3}(N_{E/H}B)=-14$. C’est donc aussi la valuation de $B$ dans
$E$. Elle est paire, d’où la régularité de $d\log B$ dans $E$ en ce lieu.
Après relève dans $k$, l’indice relatif est 2 et la différente relative
a exposant $14-2\cdot6=2$. Le jet de $\omega$ est donc nul aux deux
places de degré 6.

En $R_7$, la valuation de la norme est $-7$, avec degré résiduel 1 dans
$E/H$. L’indice de $k/E$ est 8, donc $B$ a valuation paire dans $k$.
Ailleurs hors de $T$, $B\,dx$ est régulière par sa formule : ses seuls
dénominateurs possibles sont $a,b,c$. Un zéro de valuation impaire de $B$
y donnerait un pôle de $d\log B$, ce qui est impossible. Ainsi $B$ a
bien son diviseur pair hors de $T$. Les seize jets de degré 8 sont nuls
par le facteur $q^2$, les douze de degré 10 sont nuls par évaluation et
le jet en la place choisie de degré 12 vaut **3400**. Il en résulte
$\rho=1$ et $|I_{12}|=2048$.

Avec les mêmes douze lieux de degré 10, chacun des seize choix de la place
au-dessus de $Q_6$ donne également une direction non nulle. Les valeurs
obtenues sont 3400, 1097, 1227 et 1187, chacune quatre fois. Un deuxième
support autorisé, avec huit places de degré 10 dans une fibre et quatre
dans une autre, admet un témoin dans le seul sous-corps quadratique de
masque 8. Il donne le jet isolé 2467 à la même place cible.
[Reçu et norme du témoin quartique](../results/mxx-degree12-grouped.json) · [Témoin quadratique du second support](../results/mxx-degree12-quadratic-witness.json)

## Conséquence pour la tour

La restriction d’un caractère global uniforme à l’inertie est uniforme
sur le dual de celle-ci. À la place de degré 12, l’exposant de conducteur
est 0 ou 2. Sa contribution moyenne pondérée vaut donc exactement
$24(1-1/2048)$. En gardant les majorations du théorème pour tous les autres
lieux, la borne supérieure sur le degré moyen baisse de
$24(1/2048-1/4096)=3/512$, passant de $277701/512$ à $138849/256$.
Le dénominateur est donc au plus $333+(138849/256)/2=309345/512$.
Les multiplicités et les exposants donnent toujours $P(1/40)=-3/400$
dans le critère d’infinitude des auteurs. Finalement,
$$
A(2)\ge \frac{192}{309345/512}=\frac{32768}{103115}
       >\frac{65536}{206231}.
$$
Le gain exact est $32768/21265509565$, soit environ $1{,}541\cdot10^{-6}$.
[Théorème d’infinitude et estimation du conducteur](https://arxiv.org/html/2610.33649v2#S5) · [Certificat du calcul du théorème 6.1](../certificates/mxx-theorem61.json)

## Rejeu sous Sage 10.9

Depuis la racine du dépôt, exécuter

~~~sh
sage -python experiments/reproduce_mxx_theorem61.py
sage -python experiments/mxx_degree12_support.py
sage -python experiments/mxx_degree12_grouped.py
sage -python experiments/mxx_degree12_independent.py
sage -python experiments/mxx_degree12_quadratic_witness.py
~~~

Le [calcul symbolique](../experiments/mxx_degree12_grouped.py) vérifie
l’identité dans le corps de fonctions. Le [contrôle par évaluations](../experiments/mxx_degree12_independent.py)
reprend la base de Riemann–Roch et construit une autre matrice dans sept
fibres scindées sur $\mathbf F_{4096}$. Ses rangs cumulés sont
182, 343, 488, 584, 650, 686 et 702. Il retrouve les directions 3400 et
2467 pour les deux supports. Le [calcul quadratique](../experiments/mxx_degree12_quadratic_witness.py)
vérifie séparément la réalisation du deuxième jet.
