# Inertie exacte aux seize places de degré 8 du support M2

Chacune des seize places de degré 8 a pour groupe d’inertie
$(\mathbf Z/2\mathbf Z)^8$, d’ordre **256**, dans le corps de rayon abélien
2-primaire complet du module M2 avec décomposition de $T$. Les normes vers
les sous-corps quadratiques laissent une seule valeur possible pour un jet
isolé non nul. Une norme vers un sous-corps de degré 4 exclut cette valeur.

Fixons l’une des seize places, $P$. Soit $u$ une $T$-unité de $k=k_{343}$
dont le premier jet est nul sur les 36 autres places du support. Le jet
est le coefficient de $d\log u=du/u$ dans le paramètre local, évalué
dans le corps résiduel. Nous montrons que le jet en $P$ est nul lui aussi.
[Support M2](../certificates/m2-tower.json) · [Dualité de rayon](M3_RAY_DUALITY.md)

## Ce que déterminent les normes quadratiques

Le corps de genre 2 est $H=\mathbf F_2(x,y)$ avec
$y^2+ay=b$, $a=x^3+x+1$, $b=x^2+x$ et $c=x^5+x^2+1$.
Le groupe $G=\operatorname{Gal}(k/H)$ est $\mathbf F_2^5$. Les bits des
caractères correspondent, dans l’ordre, aux générateurs d’Artin–Schreier
indexés par $1,x,x^2,y,y^2$. Les fibres entières des places $Q_3,Q_4$ de
degrés 3 et 4 donnent les seize places de chacun des degrés 6 et 8.
Le Frobenius en $Q_4$ est $t$ de masque 24. Les deux places $R_1,R_2$
de degré 5 au-dessus de $c=0$ sont totalement ramifiées. Les six
places rationnelles $T_H$ au-dessus de $x=0,1,\infty$ se décomposent
complètement. [Géométrie et différentes](FINITE_GEOMETRY.md)

Pour $h\ne0$, posons $C_h=k^{\ker h}$ et $\omega_h=d\log N_{k/C_h}u$.
Le jet de la norme est nul sur la fibre de $Q_3$, par produit de conjugués,
et aux places au-dessus de $R_1,R_2$, par itération du calcul de norme
quadratique totalement ramifiée. Un jet nul de différentielle logarithmique
donne un zéro d’ordre au moins deux en caractéristique 2. Cela impose
$2(6+5+5)=32$ degrés de zéros dans $C_h$, de genre 13, pour un maximum
de $2\cdot13-2+12=36$ si $\omega_h\ne0$. Si $h(t)=0$, l’une des deux
places de degré 4 dans $C_h$ au-dessus de $Q_4$ reçoit uniquement des jets
nuls. Les huit degrés de zéros supplémentaires forcent $\omega_h=0$.
[Lemme sur les normes aux places ramifiées](M3_DEGREE5_INERTIA.md)

La norme jusqu’à $H$ a jet nul en $Q_3,R_1,R_2$. Les 26 degrés de zéros
excèdent ici $2g(H)-2+6=8$, donc $d\log N_{k/H}u=0$. Par transitivité
la trace de $\omega_h$ vers $H$ est nulle. En caractéristique 2 cela
signifie que l’involution fixe $\omega_h$. En écrivant $\omega_h=f\,dx$
dans l’extension séparable, on voit que $\omega_h$ descend à une
différentielle de $H$. Celle-ci a des pôles au plus simples en $T_H$,
un zéro d’ordre au moins deux en $Q_3$ et est régulière ailleurs.
En effet, en $R_i$ l’ordre après relève quadratique est deux fois
l’ordre en bas plus la différente 2, et cet ordre en haut vaut au moins deux.

Le diviseur de l’espace de ces différentielles a degré
$2g(H)-2+6-2\cdot3=2$. Par Riemann–Roch sa dimension est au plus deux.
Les formes $d\log x$ et $d\log(x+1)$ y appartiennent puisque $dx$
a un zéro d’ordre deux en $Q_3$. Leurs valeurs en $Q_4$ dans la carte
$x-x(Q_4)$, codées en bits comme dans le certificat, sont 189 et 188.
Elles sont indépendantes sur $\mathbf F_2$, donc forment une base et
l’évaluation en $Q_4$ est injective.

Supposons le jet en $P$ non nul. Pour chaque $h(t)=1$, la place au-dessus
de $Q_4$ est inerte dans $C_h/H$ et décomposée dans $k/C_h$. Un seul
facteur de la norme y apporte un jet non nul. Comme $\omega_h$ descend,
ce jet appartient au sous-corps résiduel $\mathbf F_{16}$ et est invariant
par le Frobenius relatif à $Q_4$. En fixant le même point géométrique
de $Q_4$ pour toutes les évaluations, on retrouve donc le même jet et,
par injectivité, la même forme. Il existe un seul choix de $v$ parmi
$x,x+1,x(x+1)$ tel que $\omega_h=h(t)\,d\log v$ pour tous les $h$.

Le noyau de la dérivation est le sous-corps des carrés. Il existe ainsi
$a_h\in C_h^\times$ et une racine carrée commune $w$ de $N_{k/H}u$
tels que $N_{k/C_h}u=v^{h(t)}a_h^2$ et $w=v^{h(t)}N_{C_h/H}a_h$.
En chaque $R_i$, pour une unité $g$ de jet $\lambda$, posons
$J(g)_j=\operatorname{Tr}_{\mathbf F_{32}/\mathbf F_2}(r_j\lambda)$,
où $r_j$ est le coefficient du pôle simple de l’équation locale réduite.
Le test de norme quadratique impose
$$
h\cdot J(w)=(h\cdot t)(h\cdot J(v)).
$$
Les valeurs ci-dessous sont les mêmes aux deux places ramifiées.
[Dérivation du test local](M3_DEGREE6_INERTIA.md)

| $v$ | Jet en $Q_4$ | Masque de $J(v)$ en $R_i$ | Membre de droite pour $h=8,16,24$ |
|---|---:|---:|---|
| $x$ | 189 | 16 | $0,1,0$ |
| $x+1$ | 188 | 24 | $1,1,0$ |
| $x(x+1)$ | 1 | 8 | $1,0,0$ |

Le membre de gauche est linéaire en $h$ et $8+16=24$ dans le groupe
binaire. La première et la troisième ligne sont impossibles. La deuxième
passe le test pour les 31 caractères, puisque $J(x+1)=t$ et que le carré
d’un bit est ce même bit. Désormais $\beta=d\log(x+1)=dx/(x+1)$ et
$\omega_h=h(t)\beta$.

## Une norme vers un corps de degré 4 exclut le dernier jet

Prenons le sous-corps $E=C_2 C_8$, d’indice 8 dans $k$, où les indices
2 et 8 désignent les masques. Dans $\Gamma=\operatorname{Gal}(E/H)$,
les coordonnées sont données par ces deux caractères et l’image de $t$
est $\tau=(0,1)$. Posons $\omega=d\log N_{k/E}u$. Pour toute translation
$\sigma\ne0$ de $\Gamma$, le caractère de noyau $\langle\sigma\rangle$ est
$h_\sigma(v)=\det(\sigma,v)$. Par transitivité,
$$
\omega+\sigma\omega=\omega_{h_\sigma}=\det(\sigma,\tau)\,\beta.
$$
La fonction $\det(\sigma,\tau)$ est la première coordonnée de $\sigma$.
Le générateur $\xi$ de $C_2$ associé à $x$ est translaté par ce même bit.
Il vérifie $\xi^2+\xi=f$ avec $f=bx/c^2=(x+1)(x/c)^2$. Ainsi
$A=\omega/\beta+\xi$ est invariant par $\Gamma$ et appartient à $H$.

**Bornes sur les pôles de $A$.** Le diviseur de $\beta$ sur $H$ a pour
zéros $2Q_3$ et pour pôles simples les quatre places au-dessus de
$x=1,\infty$. Cela suit du diviseur de $dx$ et de la différente 2 de
$H/\mathbf F_2(x)$ en $Q_3$. La norme définissant $\omega$ a jet nul
sur la fibre de $Q_3$, donc $\omega/\beta$ y est régulière. Aux places
de $T_H$, $\omega$ a au plus des pôles simples et $E/H$ est non ramifiée.
Au-dessus de chaque $R_i$, $E/H$ a indice de ramification 4 et différente
6 (ses trois caractères non triviaux y ont conducteur 2). L’ordre de la
relève de $\beta$ y vaut 6 et celui de $\omega$ est au moins deux, car la
norme préserve le jet nul en ce lieu. Enfin $\xi$ est entière hors des
$R_i$, et son équation donne un ordre au moins $-4$ dans $E$ au-dessus
des $R_i$. Il en résulte que $A$ a dans $H$ au plus des pôles simples
aux deux $R_i$ et aux deux places au-dessus de $x=0$.

Ce diviseur de pôles $D$ a degré 12. Riemann–Roch donne
$\dim_{\mathbf F_2} L(D)=12+1-2=11$. Les onze fonctions
$$
\frac{x^i}{xc}\quad(0\le i\le6),\qquad
\frac{x^iy}{xc}\quad(0\le i\le3)
$$
sont dans $L(D)$ car $y$ a des pôles d’ordre au plus trois aux infinis.
Elles sont indépendantes puisque $1,y$ sont indépendants sur
$\mathbf F_2(x)$. Il y a donc exactement 2 048 fonctions $A=(p+qy)/(xc)$
à tester, avec $\deg p\le6$ et $\deg q\le3$.

**Deux conditions incompatibles.** Écrivons $\partial=d/dx$.
Comme $x$ est séparante, $\partial^2=0$ (en caractéristique 2, son carré
est une dérivation nulle sur $\mathbf F_2(x)$, donc sur son extension
séparable). Si $B\,dx=d\log g$, alors $\partial B=B^2$.
Appliquons l’identité à $B=(A+\xi)/(x+1)$. Avec $\partial\xi=\partial f$
elle donne
$$
(x+1)\partial A+A^2+A=(x+1)\partial f+f=0.
$$
La dernière égalité utilise $f=(x+1)(x/c)^2$.

En $Q_4$ il y a dans $E$ deux places de degré 8, toutes deux décomposées
dans $k/E$. La norme a le jet de $\beta$ en celle qui reçoit $P$ et le jet
nul en l’autre. Ainsi $A+\xi$ doit prendre respectivement les valeurs 1
et 0. Les deux valeurs de $\xi$ diffèrent de 1. À l’un quelconque des
deux points au-dessus du représentant fixé de $Q_4$, il est donc
nécessaire que $A(Q_4)\in\{\xi(Q_4),\xi(Q_4)+1\}$.

Dans l’encodage polynomial de $\mathbf F_{256}$ du support, le représentant
de $Q_4$ est $(x,y)=(188,12)$. Le calcul sur les 2 048 fonctions donne

| Quantité vérifiée | Résultat |
|---|---|
| Candidats satisfaisant l’identité différentielle | 16 |
| Valeurs de ces candidats en $(188,12)$ | $0,1,12,13,176,177,188,189$ |
| Racines de $Z^2+Z=f(188,12)$ | $92,93$ |

Les deux ensembles sont disjoints. Le même calcul exclut les deux places
de $E$ et donc chacun des seize choix de $P$ dans $k$. Le raisonnement
utilise seulement les fibres complètes en degrés 6 et 8 et les deux
places ramifiées en degré 5.

## Conséquence pour M3 et reproduction

L’image des jets de toutes les $T$-unités intersecte trivialement chaque
bloc de degré 8. Dans l’identité d’inertie du rayon complet,
$|I_P|=2^{8-\rho_P}$, cela donne $\rho_P=0$ et $|I_P|=256$.
La contribution des seize places au degré moyen du conducteur vaut
$16\cdot 8\cdot 2(1-1/256)=255$. Avec les degrés 5 et 6, le sous-total
exact est $1667/8+255=3707/8$. L’inertie des deux places de degré 10 et
de la place de degré 12 reste ouverte. Le calcul concerne le module M2
fixé et laisse la borne publiée du laboratoire pour $A(2)$ inchangée.
[Identités de conducteur](M3_RAY_DUALITY.md)

Depuis la racine du dépôt, avec Sage 10.9, exécuter les deux vérifications.

~~~sh
sage -python experiments/m3_degree8_norm_obstruction.py
sage -python experiments/m3_degree8_quartic_norm.py
~~~

Le [calcul quadratique](../experiments/m3_degree8_norm_obstruction.py)
et son [reçu](../results/m3-degree8-norm-obstruction.json) vérifient les
fibres, les jets et les traces. Le [calcul quartique](../experiments/m3_degree8_quartic_norm.py)
et son [reçu](../results/m3-degree8-quartic-norm.json) vérifient l’exclusion
du dernier jet sur les seize places du support.
