# Inertie exacte aux seize places de degré 6 du support M2

Soient $k=k_{343}$, $S$ le support M2 de 37 places, de conducteur 2
en chacune, et $T$ les 192 places rationnelles décomposées. **Pour toute
$T$-unité de $k$, si son premier jet est nul en 36 places de $S$ et si
la place restante est de degré 6, le jet y est également nul.** Cela
couvre simultanément les seize choix de la place restante. En particulier,
les unités des sous-corps intermédiaires et leurs produits ne peuvent
fournir le témoin recherché. [Support certifié](../certificates/m2-tower.json)

Le premier jet d’une unité $u$ est son image dans le facteur 2-primaire
$U_P^{(1)}/U_P^{(2)}$. En caractéristique deux, c’est le coefficient de
$du/u$ dans une uniformisante. La valeur ordinaire de $u$ dans le corps
résiduel est inversible. La preuve utilise les deux places de degré 5,
les seize de degré 6 et les seize de degré 8. Les places de degrés 10 et
12 n’interviennent pas.

## Descente aux courbes de genre 13

La courbe de base $H$ a genre 2 et six places rationnelles $T_H$.
Le groupe de Galois de $k/H$ est $\mathbf F_2^5$, dans la base des
translations des cinq générateurs d’Artin–Schreier indexés par
$1,x,x^2,y,y^2$. À la place $Q_3$ de degré 3, le Frobenius est le vecteur
$t$ de masque 18, soit $(0,1,0,0,1)$ en numérotant les bits à partir de
zéro. La fibre entière est constituée des seize places de degré 6 de $S$.
La fibre entière de $Q_4$, de degré 4, donne de même les seize places
de degré 8. Ces places sont non ramifiées. Les deux places de degré 5
de $H$ au-dessus de $c=x^5+x^2+1$ sont totalement ramifiées dans $k$.
[Géométrie locale](FINITE_GEOMETRY.md) · [Sous-corps intermédiaires](INTERMEDIATE_COVERS.md)

Pour un caractère non nul $h$, soit $C_h=k^{\ker h}$ le sous-corps
quadratique. Sa courbe a genre 13. Les six places de $T_H$ s’y décomposent
en douze places rationnelles $T_h$. Chacune des deux places de degré 5
a un unique prolongement de même degré, d’exposant de différente 2 pour
$C_h/H$ (équation réduite à pôle simple). La somme des degrés des
places de $C_h$ au-dessus de $Q_4$ est 8, que cette place soit inerte ou
décomposée.

Supposons qu’une $T$-unité $u$ ait exactement le profil demandé.
Écrivons $u_h=N_{k/C_h}(u)$, une $T_h$-unité. Son jet est nul au-dessus
de $Q_4$ car la norme y multiplie des unités de jets nuls dans des
extensions non ramifiées. Il est aussi nul aux deux places de degré 5.
Voici la justification au lieu ramifié. Dans une étape quadratique
totalement ramifiée de corps locaux, une uniformisante $\pi$ du corps
supérieur donne une base entière $1,\pi$ sur le corps inférieur
(les valuations des deux termes ont parités distinctes et les corps
résiduels sont égaux). Une unité de jet nul s’écrit $A+B\pi$ avec
$A$ unité et $B$ dans l’idéal maximal du corps inférieur. En effet $A$
est constant modulo $\pi^2$ dans le développement sur le corps résiduel.
La norme vaut
$$
A^2+AB\,\operatorname{Tr}(\pi)+B^2 N(\pi).
$$
La trace de $\pi$ est dans l’idéal maximal du bas. La norme est donc
congrue à $A^2$ modulo le carré de cet idéal, et son jet est nul.
On itère sur les quatre étages quadratiques de $k/C_h$.

## Une seule différentielle peut survivre

Localement, en caractéristique deux, le premier terme non nul de la
dérivée d’une unité provient d’une puissance impaire du paramètre.
Un zéro régulier de $d\log u_h$ a donc un ordre pair, au moins deux si
le jet est nul. De plus, $d\log u_h$ a au plus un pôle simple par place
de $T_h$. Les zéros imposés aux places au-dessus de $Q_4$ et des deux
places de degré 5 ont degré au moins $2(8+5+5)=36$. Pour une
différentielle non nulle, le total des zéros est au plus
$2g(C_h)-2+\deg T_h=24+12=36$.

Plus précisément, si $D_h$ est la somme des places où ces zéros sont
imposés, l’espace des différentielles à pôles bornés par $T_h$ et à
zéros prescrits par $2D_h$ a dimension au plus un. Le diviseur associé
a degré zéro, donc le quotient de deux solutions non nulles est constant.
Le corps des constantes est $\mathbf F_2$.

Une solution explicite est $\omega_0=d\log v$ tirée depuis $H$, avec
$v=x(x+1)(y+x)$. Le certificat des unités de base et le calcul des jets
sur $H$ donnent un jet nul en $Q_4$ et non nul en $Q_3$. La différentielle
est régulière aux deux places de degré 5 de $H$. Dans $C_h$, son ordre en
chacune devient $2\operatorname{ord}_{Q_5}(\omega_0)+2\ge2$, par la
formule de la différente. Son jet reste non nul au-dessus de $Q_3$.
Ainsi $d\log u_h$ vaut soit zéro, soit $\omega_0$.
[Diviseurs des unités de base](M3_RAY_DUALITY.md)

Le choix est forcé par la fibre de $Q_3$. Si $h(t)=1$, $Q_3$ est inerte
dans $C_h/H$ et sa place de degré 6 se décompose complètement dans
$k/C_h$. Un seul facteur de la norme a un jet non nul. Si $h(t)=0$,
l’une des deux places de $C_h$ au-dessus de $Q_3$ reçoit uniquement
des jets nuls, ce qui exclut $\omega_0$. Dans les deux cas
$$
d\log u_h=h(t)\,d\log v .
$$

## Trois normes incompatibles

Dans un corps de fonctions d’une variable sur le corps parfait
$\mathbf F_2$, le noyau de la dérivation est le sous-corps des carrés
(on peut utiliser la base $1,x$ sur les carrés pour une variable séparante
$x$). Il existe donc $a_h\in C_h^\times$ tel que $u_h=v^{h(t)}a_h^2$,
avec $h(t)$ représenté par 0 ou 1. La transitivité des normes donne
$$
N_{k/H}(u)=\big(v^{h(t)}N_{C_h/H}(a_h)\big)^2 .
$$
La racine carrée $w\in H$ du membre de gauche est unique, donc la même pour
tous les caractères. Les éléments $a_h$, $v$ et $w$ sont des unités aux
deux places de degré 5.

Fixons l’une de ces places et la coordonnée $z=x-x(Q_5)$. Soient $r_i$
les cinq coefficients des pôles simples après réduction locale des
équations d’Artin–Schreier. La réduction est additive en caractéristique
deux, et le coefficient associé à $h$ est $r_h=\sum h_i r_i$.
Si $\lambda$ est le jet d’une norme locale d’unité depuis $C_h$, alors
$\operatorname{Tr}_{\mathbf F_{32}/\mathbf F_2}(r_h\lambda)=0$.
En effet un générateur réduit $\xi^2+\xi=r_h/z+O(1)$ a valuation $-1$.
Une unité $a+b\xi$ a $a$ unité et $b$ divisible par $z$, par parité des
valuations. Sa norme vaut $a^2+ab+b^2(r_h/z+O(1))$. En posant
$d=(b/z)(0)/a(0)$, on obtient $r_h\lambda=r_hd+(r_hd)^2$, de trace nulle.

Pour une unité locale $g$ de jet $\lambda_g$, posons
$J(g)_i=\operatorname{Tr}(r_i\lambda_g)$. Les jets logarithmiques sont
additifs sur les produits. Le test de norme appliqué à
$w/v^{h(t)}=N_{C_h/H}(a_h)$ impose
$$
h\cdot J(w)=(h\cdot t)(h\cdot J(v)).
$$
Sage donne $J(v)=(0,1,0,1,0)$, de masque 10, aux deux places de degré 5.
Le membre de gauche est linéaire en $h$. Or le membre de droite vaut 0
pour le caractère de masque 8, vaut 0 pour celui de masque 16, et vaut 1
pour leur somme de masque 24. Cela contredit l’existence de $u$.

## Conséquence et reproduction

Dans la notation de la [dualité de rayon, équations (8) et (11)–(16)](M3_RAY_DUALITY.md),
l’image des unités globales intersecte trivialement chacun des seize blocs
de degré 6. Ainsi $\rho_P=0$ et $|I_P|=2^6=64$ pour chacune de ces
places dans le groupe de rayon abélien **2-primaire complet** avec
décomposition de $T$. La contribution de ces places au degré du conducteur
moyen est exactement $16\cdot6\cdot2(1-1/64)=189$. Les autres inerties
et le passage au quotient élémentaire $G/2G$ demandent leurs propres calculs.

Depuis la racine du dépôt, utiliser Sage 10.9.

~~~sh
sage -python experiments/m3_degree6_norm_obstruction.py
sage -python experiments/m3_quadratic_tunit_search.py
sage -python experiments/m3_degree6_descent.py
~~~

Le [contrôle des normes](../experiments/m3_degree6_norm_obstruction.py)
recalcule les entrées finies de la preuve. Le [reçu](../results/m3-degree6-norm-obstruction.json)
donne les corps résiduels et les traces sous leur encodage binaire.
Les recherches explicites ont leurs propres reçus
[quadratique](../results/m3-quadratic-tunit-search.json) et
[de degré 16](../results/m3-degree6-descent.json).
