# Inertie exacte aux deux places de degré 10 de M2

Dans le groupe de rayon abélien 2-primaire complet du module M2, les deux
places de degré 10 ont chacune pour inertie $(\mathbf Z/2\mathbf Z)^{10}$,
d’ordre **1 024**. Plus précisément, si une $T$-unité a son premier jet nul
aux 34 places de degrés 5, 6 et 8, ses jets aux deux places de degré 10
sont **égaux** dans les cartes du certificat. L’hypothèse sur ces 34 places
suffit, quelle que soit la valeur du jet en degré 12.
[Support M2](../certificates/m2-tower.json) · [Identité d’inertie](M3_RAY_DUALITY.md)

## Pourquoi la fibre de degré 10 demande une autre descente

Écrivons $H=\mathbf F_2(x,y)$, $y^2+ay=b$, avec
$a=x^3+x+1$, $b=x^2+x$ et $c=x^5+x^2+1$. Le corps $k=k_{343}$ est engendré
sur $H$ par cinq éléments $w_i$ avec $w_i^2+w_i=bh_i/c^2$, où
$(h_0,\ldots,h_4)=(1,x,x^2,y,y^2)$. Le groupe de Galois
$G=(\mathbf F_2)^5$ agit par translations des $w_i$. Les indices de masque
sont écrits en binaire, avec le bit de poids 1 pour $w_0$.
[Géométrie de la construction](FINITE_GEOMETRY.md)

Les deux places $P,P'$ du support sont au-dessus du même point
$(x,y)=(15,315)$ de degré 5 sur $H$, en codage polynomial de
$\mathbf F_{1024}$ de module 1033. Le cinquième itéré de Frobenius translate
les $w_i$ par le masque 21. Il y a donc seize places fermées de degré 10
dans la fibre. À point géométrique de base fixé, les représentants de $P$
et $P'$ se déduisent l’un de l’autre par la translation $\sigma$ de masque
16, qui change seulement $w_4$. Le paramètre est $x-x(P)$ dans les deux
cartes.

Soit $u$ une $T$-unité dont les jets sont nuls aux 34 places indiquées.
Ces places sont les deux places totalement ramifiées au-dessus de $c=0$
et les deux fibres complètes au-dessus de $Q_3,Q_4$ de degrés 3 et 4.
Dans chaque sous-corps quadratique $C/H$, le logarithme différentiel de
$N_{k/C}u$ a au moins $2(5+5+6+8)=48$ degrés de zéros s’il est non nul.
La norme préserve le jet nul aux places ramifiées par étapes quadratiques.
Or le genre 13 et les douze pôles rationnels possibles donnent un maximum
de 36. Toutes ces différentielles de normes sont donc nulles.
[Calcul aux places ramifiées](M3_DEGREE5_INERTIA.md)

Dans la fibre de degré 10, les quatorze places hors du support peuvent
contribuer aux mêmes sommes de jets que $P$ et $P'$. Le calcul local
l’illustre exactement. Sur les $16\cdot10=160$ bits de la fibre, la
nullité des sommes quadratiques impose 30 contraintes indépendantes.
La projection de leur noyau sur les deux blocs sélectionnés a encore
rang 20. Même en imposant en plus la nullité de toutes les sommes
quartiques, cette projection garde rang 20. Ce dernier test porte
uniquement sur des données locales possibles. Pour trancher, nous
utilisons l’identité différentielle satisfaite par toute unité globale.

## Encadrer toutes les différentielles possibles par des traces vers $H$

Posons $\omega=du/u$ et
$$
\gamma=d\log((x+1)c)
       =\frac{(x^2+x+1)^2}{(x+1)c}\,dx,\qquad F=\omega/\gamma\in k .
$$
Sur $H$, le diviseur de $\gamma$ est
$2Q_3+2Q_4-T_1-R_1-R_2$, où $T_i$ est la somme des deux places de $H$
au-dessus de $x=i$ et les $R_j$ sont les deux zéros de $c$. En effet
$\operatorname{div}(dx)=2Q_3-2T_\infty$ par la différente de
$H/\mathbf F_2(x)$, et $x^2+x+1$ a pour diviseur de zéros $Q_4$.
Le représentant de $Q_4$ vérifie cette équation et sa place a degré 4,
ce qui épuise le degré du diviseur de zéros. Ainsi $\gamma$ est régulière
et non nulle aux places de $T_0,T_\infty$.

Un jet nul de $d\log u$ donne un zéro d’ordre au moins deux en
caractéristique 2. La fonction $F$ est donc régulière sur les fibres de
$Q_3,Q_4$. Elle est régulière au-dessus de $T_1$, et a au plus un pôle
simple au-dessus de $T_0,T_\infty$. L’extension $k/H$ est totalement
ramifiée d’indice 32 et de différente 62 à chaque $R_j$ (les
31 caractères non triviaux ont conducteur 2). La relève de $\gamma$
y a ordre $-32+62=30$. Comme $\omega$ y a ordre au moins deux,
$v_k(F)\ge-28$. Partout ailleurs $F$ est régulière.

Écrivons $F=\sum_I A_I w_I$ avec $w_I=\prod_{i\in I}w_i$, les indices
parcourant les parties de $\{0,1,2,3,4\}$. Les coefficients sur $H$ sont
$$
A_I=\operatorname{Tr}_{k/H}\!\left(F\prod_{j\notin I}(1+w_j)\right).
$$
La formule résulte de la base duale pour la trace. Dans chaque facteur
quadratique, $1,w_i$ ont pour base duale $1+w_i,1$, et la somme sur les 32
translations factorise ces accouplements. Les $w_i$ sont entiers hors de
$R_1,R_2$, de sorte que la trace conserve les bornes de pôles aux places
non ramifiées. À chacune des places ramifiées $v_k(w_i)\ge-32$ par
l’équation d’Artin–Schreier. Pour tout entier $r$, la trace locale de
$\mathfrak m_k^r$ est contenue dans
$\mathfrak m_H^{\lfloor(r+62)/32\rfloor}$, par définition de l’inverse
de la différente. En prenant $r=-28-32(5-|I|)$ on obtient
$v_{R_j}(A_I)\ge |I|-4$.

Pour $m=4-|I|$, le coefficient appartient donc à
$L(D_m)$ avec $D_m=m(R_1+R_2)+T_0+T_\infty$. Si $m=-1$ son degré vaut
$-6$ et le coefficient est nul. Si $m\ge0$ ce degré vaut $10m+4$ et
Riemann–Roch en genre 2 donne $\dim L(D_m)=10m+3$. Une base explicite est
$$
\frac{x^j}{x c^m}\quad (0\le j\le5m+2),\qquad
\frac{x^j y}{x c^m}\quad (0\le j\le5m-1).
$$
La seconde famille est vide pour $m=0$. Ces fonctions satisfont les
bornes aux infinis puisque $y$ y a des pôles d’ordre au plus trois.
Leur indépendance résulte de celle de $1,y$ sur $\mathbf F_2(x)$ et leur
nombre est la dimension attendue. Le nombre total de coefficients
binaires libres est ainsi
$43+5\cdot33+10\cdot23+10\cdot13+5\cdot3=583$. Cette majoration contient
les différentielles de **toutes** les $T$-unités satisfaisant les 34 zéros.

## Le calcul de rang et la norme qui sépare les deux places

Écrivons $\gamma=L\,dx$. La dérivation $\partial=d/dx$ satisfait
$\partial^2=0$, puisque $k/\mathbf F_2(x)$ est séparable en
caractéristique 2. Pour tout $B\,dx=d\log u$ on a donc $\partial B=B^2$.
Appliquée à $\omega=FL\,dx$ et à $\gamma$, cette identité impose
$$
\partial F+L(F^2+F)=0 .
$$
Cette équation est linéaire sur $\mathbf F_2$. Sage l’évalue sur les
583 colonnes ci-dessus en huit points de $H$ sur $\mathbf F_{4096}$ et
sur leurs 32 translatés dans $k$. Les rangs binaires cumulés sont
166, 316, 423, 508, 544, 567, 573 et **575**. Une identité rationnelle
doit être vraie en tous ces points réguliers, si bien que le noyau de
dimension huit suffit comme majoration. Les points, le codage et les
contrôles de rang figurent dans le [certificat du calcul](../results/m3-degree10-cartier.json).

Dans chacun des huit vecteurs d’une base de ce noyau, **aucun monôme ne
contient $w_3$ ou $w_4$**. En particulier $\sigma F=F$ et
$\sigma\omega=\omega$ pour toute unité considérée. La norme vers le
corps fixe de $\sigma$, de degré 16 sur $H$, vérifie donc
$$
d\log N_{k/k^{\langle\sigma\rangle}}u=\omega+\sigma\omega=0 .
$$
Les deux places $P,P'$ sont échangées par $\sigma$, et leurs points
géométriques sont alignés dans la même carte. L’identité impose
$j_P(u)=j_{P'}(u)$. Si le jet est isolé en l’une des deux places, l’autre
vaut zéro et le premier vaut donc zéro aussi. Ainsi $\rho_P=\rho_{P'}=0$
et l’ordre d’inertie vaut $2^{10}$ en chacune. Leur contribution au
degré moyen du conducteur est exactement
$2\cdot10\cdot2(1-1/1024)=5115/128$.

L’égalité des deux jets permet des valeurs communes non nulles. Par
exemple, pour $w_6=w_1+w_2$ (masque 6), l’élément $(x+1)c\,w_6$
est une $T$-unité de différentielle $\gamma$. En effet
$w_6^2+w_6=(b/c)^2$, donc $w_6=(w_6+b/c)^2$, et la norme de $cw_6$
depuis $C_6$ vers $H$ vaut $b^2$. Sage retrouve ses jets nuls aux 34
places et ses trois autres jets $(315,315,3433)$ dans l’ordre des deux
places de degré 10 puis de la place de degré 12.

## Conséquence pour le rang global des jets de M3

Sur l’espace de dimension huit du crible, l’évaluation en l’une des
deux places de degré 10 a rang sept. L’unique vecteur non nul du noyau
a, au représentant de degré 12, $F(P_{12})=1173$ et un jet
$(\omega/dx)(P_{12})=1043$ dans l’encodage du support. Imposer la
nullité à cette dernière place porte donc le rang de l’évaluation à huit.
Une $T$-unité de jets nuls aux 37 places a nécessairement $\omega=0$.
Elle est un carré dans $k$ puisque $\ker\partial=k^2$, et sa racine est
encore une $T$-unité par les valuations hors de $T$.

Le groupe des $T$-unités modulo carrés a dimension $|T|-1=191$.
L’application des jets sur les 37 blocs est donc injective sur ce
quotient. Son image a **rang exact 191** dans les 266 coordonnées locales.
Le quotient de la partie locale par les relations a ordre $2^{266-191}=2^{75}$.
La partie 2-primaire de la jacobienne a ordre $2^{51}$ avant d’imposer
la décomposition de $T$. La suite exacte du rayon complet donne ainsi
**$2^{75}\le |G_{\mathfrak m,T}^{(2)}|\le2^{126}$**.
[Suite exacte, unités et ordre de la jacobienne](M3_RAY_DUALITY.md)

Pour la place de degré 12, l’espace des jets isolés a dimension au plus
un. Le calcul laisse les ordres 2 048 et 4 096 possibles. La
[preuve de réalisation en degré 12](M3_DEGREE12_INERTIA.md) construit
la différentielle d’une $T$-unité de jet 1043 et établit l’ordre 2 048.

## Reproduire avec Sage 10.9

Depuis la racine du dépôt, exécuter

~~~sh
sage -python experiments/m3_degree10_norm_obstruction.py
sage -python experiments/m3_degree10_cartier.py
~~~

Le [calcul de la fibre et des normes locales](../experiments/m3_degree10_norm_obstruction.py)
vérifie aussi l’unité explicite sur les 37 places et compare sa sortie au
[reçu local](../results/m3-degree10-norm-obstruction.json).
Le [calcul des différentielles](../experiments/m3_degree10_cartier.py)
reconstruit la matrice et les évaluations du noyau.
