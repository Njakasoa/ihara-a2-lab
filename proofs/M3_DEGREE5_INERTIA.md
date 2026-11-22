# Inertie exacte aux deux places de degré 5 du support M2

Sur la base $k_{343}$, chacune des deux places de degré 5 du support M2
a pour groupe d’inertie $(\mathbf Z/2\mathbf Z)^5$ dans le corps de rayon
abélien 2-primaire de module $2\sum_{P\in S}P$ avec décomposition de $T$.
La preuve porte sur toutes les $T$-unités du corps de fonctions $k=k_{343}$.
Les deux places sont traitées séparément. [Support M2](../certificates/m2-tower.json)
· [Géométrie de la base et des ramifications](FINITE_GEOMETRY.md)

## La descente impose 38 degrés de zéros

Choisissons l’une de ces places, $P$, et appelons $P'$ l’autre. Supposons
qu’une $T$-unité $u$ ait son premier jet nul sur les 36 autres places de
$S$. Pour chaque caractère non nul $h$ de $\operatorname{Gal}(k/H)$, soit
$C_h$ le sous-corps quadratique de $k/H$ et $u_h=N_{k/C_h}(u)$.
Cette norme est une unité en dehors des douze places rationnelles de
$C_h$ au-dessus de $T_H$. Son premier jet est nul aux endroits suivants.

| Places de $C_h$ | Pourquoi le jet de la norme y est nul | Somme des degrés |
|---|---|---:|
| Fibre de $Q_3$ | Les seize places de degré 6 de $k$ forment la fibre entière et ont jet nul. L’extension est non ramifiée. | 6 |
| Fibre de $Q_4$ | Les seize places de degré 8 de $k$ forment la fibre entière et ont jet nul. L’extension est non ramifiée. | 8 |
| Place au-dessous de $P'$ | $P'$ a jet nul. Chacune des quatre normes quadratiques dans la tour totalement ramifiée préserve cette annulation. | 5 |

Pour la dernière ligne, dans chaque étage totalement ramifié $E/F$ on
peut diviser l’unité par son représentant constant dans le corps résiduel
commun. Une unité normalisée de jet nul a la forme $1+\pi_F b$ avec
$b\in\mathcal O_E$, puisque $\mathfrak m_E^2=\pi_F\mathcal O_E$. Sa norme
est $1+\pi_F\operatorname{Tr}(b)+\pi_F^2N(b)$. La trace de $b$ a résidu
nul, les deux conjugués ayant le même résidu en caractéristique deux.
La norme a donc jet nul dans $F$. Aux places non ramifiées le même fait
résulte directement du produit des conjugués, avec un paramètre du bas.

Une différentielle logarithmique d’unité dont le premier jet s’annule a
un zéro d’ordre au moins deux. En caractéristique deux, le premier terme
survivant dans la dérivée d’une série d’unité provient d’une puissance
impaire. Ainsi, si $du_h/u_h$ était non nulle, ses zéros auraient degré
au moins $2(6+8+5)=38$. Or $g(C_h)=13$ et elle a au plus un pôle simple
en chacune des douze places au-dessus de $T_H$. Le degré total de ses
zéros est donc au plus $2\cdot13-2+12=36$. Il en résulte que $du_h/u_h=0$
pour les 31 caractères. En particulier, **toutes les normes ont jet nul
à la place au-dessous de $P$**. [Inventaire des sous-corps](INTERMEDIATE_COVERS.md)

## Les normes distinguent tous les jets à la place ramifiée

Voici un calcul local de la famille de normes dont le noyau commun nous
intéresse. Au-dessous de $P$, le complété de $H$ s’écrit
$F=\kappa((z))$ avec $\kappa=\mathbf F_{32}$ et $z=x-x(Q_5)$.
Après réduction du pôle double, les cinq équations d’Artin–Schreier
ont pour membres de droite $r_i/z+b_i+O(z)$. Les $r_i$ forment une base
binaire de $\kappa$ à chacune des deux places. Par non-dégénérescence de
la trace il existe $d\in\kappa$ vérifiant
$\operatorname{Tr}(r_i d)=\operatorname{Tr}(b_i)$ pour les cinq indices.

Le calcul emploie le codage polynomial binaire du certificat, de polynôme
irréductible de masque 37. Le terme constant $d$ et la base des pôles sont
reconstruits pour chaque représentant.

| Place de $k$ | Représentant $(x,y)$ en bas | Coefficients $r_i$ | $d$ |
|---|---|---|---:|
| `k343-d5-001` | $(2,17)$ | $23,19,12,30,15$ | 11 |
| `k343-d5-002` | $(2,26)$ | $23,19,12,5,3$ | 11 |

Le complété de $k$ est le corps $F(Y)$ défini par
$$
Y^{32}+Y=z^{-1}+d .
$$
En effet $Y$ a valuation $-1/32$ dans la normalisation du bas, donc
l’extension a degré 32 et $\pi=1/Y$ est une uniformisante en haut. Ses
automorphismes sont les translations $Y\mapsto Y+s$, $s\in\kappa$.
Pour $r\in\kappa$, posons $L_r(Y)=\sum_{j=0}^4(rY)^{2^j}$. On a
$L_r(Y)^2+L_r(Y)=r(z^{-1}+d)$. Pour $r=r_i$, ce membre de droite diffère
de l’équation réduite du laboratoire par une série entière de trace
résiduelle nulle. Une telle série est de la forme $a^2+a$ dans
$\kappa[[z]]$ par relèvement d’une solution résiduelle (la dérivée vaut 1).
Les cinq extensions quadratiques sont donc les mêmes que celles du
laboratoire. Leurs caractères de translation $s\mapsto\operatorname{Tr}(r_i s)$
sont indépendants et engendrent le dual du groupe.

Pour un caractère de paramètre $r\ne0$, soit
$B_r=\{s\in\kappa:\operatorname{Tr}(rs)=0\}$. Le polynôme
$D_r(X)=\prod_{s\in B_r}(X+s)$ est additif. En effet il est égal à
$L_r(X)/r^{16}$, les deux polynômes étant unitaires de degré 16 avec les
mêmes racines. Dans le corps fixé par $B_r$, $\pi_r=1/D_r(Y)$ est une
uniformisante (c’est la norme de $\pi$). Pour un jet $\lambda\in\kappa$
on obtient
$$
N_{B_r}(1+\lambda\pi)
=\frac{D_r(Y+\lambda)}{D_r(Y)}
=1+D_r(\lambda)\pi_r .
$$
Le calcul précédent sur les étages quadratiques permet de remplacer
toute unité normalisée par $1+\lambda\pi$ modulo $U^2=1+\mathfrak m^2$.
Le noyau sur les premiers jets est donc exactement $B_r$. Lorsque $h$
parcourt les 31 caractères, $r$ parcourt $\kappa^\times$. Le seul élément
commun aux noyaux est zéro. Plus précisément, chaque $\lambda\ne0$ donne
$\operatorname{Tr}(r\lambda)=1$ pour exactement 16 valeurs de $r$.
Ceci vérifie la détection requise **à chacune des deux places**.

## Conséquence pour le rayon complet

Un jet supporté sur le seul bloc de $P$ serait annulé par toutes les
normes en vertu du décompte global. Le calcul local impose alors sa nullité.
Ainsi $\rho_P=0$ et $|I_P|=2^5=32$ pour les deux places dans le rayon
2-primaire complet. Leur contribution au degré moyen du conducteur est
$2\cdot5\cdot2(1-1/32)=155/8$. Avec les seize places de degré 6, le total
de ces contributions est $1667/8$. La question du quotient élémentaire
$G/2G$ demande un calcul distinct. [Identité de rayon et moyenne des conducteurs](M3_RAY_DUALITY.md)
· [Contribution du degré 6](M3_DEGREE6_INERTIA.md)

## Reproduire avec Sage 10.9

Depuis la racine du dépôt, exécuter

~~~sh
sage -python experiments/m3_degree5_norm_obstruction.py
~~~

Le [programme Sage](../experiments/m3_degree5_norm_obstruction.py) et le
[reçu de calcul](../results/m3-degree5-norm-obstruction.json) vérifient
les données locales et les 31 applications de norme sur chacun des 32
jets aux deux places. La descente qui relie ces calculs aux unités globales
est démontrée ci-dessus.
