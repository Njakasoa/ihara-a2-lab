# Contrôle historique : Schoof, A(2) ≥ 2/9

Source primaire : René Schoof, *Algebraic curves over F₂ with many rational
points*, J. Number Theory 41 (1992), 6–14, §§2–3.
PDF auteur : https://reneschoof.github.io/CurvesF2.pdf

## Correction d'une équation imprimée

La page13 a été inspectée visuellement : elle imprime E : Y²+Y=T³+1 tout
en affirmant cinq points rationnels et la décomposition de 0 et1.
Cette équation n'a que trois points sur F₂. Le contrôle adopte
E : y²+y=x³+x, qui satisfait les propriétés de conducteur et de décomposition
utilisées dans la preuve. Nous ne reproduisons donc pas aveuglément l'équation
imprimée. Une étude d'éventuels errata est distincte de ce constat arithmétique.

## Modèles explicites

Prendre E ci-dessus, b=x²+x, d=b(xy+x+y)+1.
Une réalisation de l'extension Y/E de Schoof est
w²+w=bx/d², équation donnée aussi dans Duursma–Mak §5.3 (leur h=x).
La norme de d sur F₂(x) est un polynôme de degré9. Le code trouve exactement
quatre zéros géométriques de degré4 et cinq de degré5 sur E ; les dérivées
locales de d sont non nulles. Cela épuise les zéros puisque deg Norm(d)=9.

Dans l'uniformisante x−α, les résidus après réduction Artin–Schreier valent
ρ= x²/(d')² + sqrt(bx/(d')²). Ils s'annulent aux quatre zéros de degré4
et sont non nuls aux cinq de degré5. Aucun autre pôle fini n'existe.
À l'infini de E, x et y ont ordres polaires2 et3 ; d a ordre9, bx ordre6.
Le membre droit s'annule. Le conducteur de Y/E est donc exactement2P₅.
D'où 2g(Y)−2=2(0)+10, soit g(Y)=6.
Le facteur b assure la décomposition des quatre points affines rationnels de E,
et le point à l'infini se décompose aussi ; Y a dix points rationnels.

Poser E' : u²+u=1/b sur F₂(x) et X=Y E'. E' ramifie à x=0,1, conducteur2
à chacun, et se décompose à l'infini. Ces deux points ont chacun quatre places
rationnelles au-dessus dans Y, toutes non ramifiées dans Y/F₂(x).
X/Y a donc huit places rationnelles ramifiées, chacune de différente2.
Ailleurs, la régularité du membre droit interdit une ramification nouvelle.
Au-dessus de l'infini, les deux places de Y se décomposent, donnant |S|=4.
Le genre est g(X)=1+(2(2·6−2)+2·8)/2=19.

## Infinitude

Appliquer la théorie des genres, proposition2.4 de Schoof, à X/Y :
d₂Cl_S ≥8−1−1=6, les deux places de Y au-dessus de l'infini donnant
rang1 pour les S'-unités. Sur X, le rang des S-unités est |S|−1=3.
Le critère2.3 exige d₂Cl_S ≥2+2sqrt(3+1)=6 ; l'égalité suffit.
La tour (2,S) est infinie. Les places rationnelles décomposées fixent le corps
des constantes et le genre croît sans borne. Par Riemann–Hurwitz,
A(2)≥4/(19−1)=2/9.

Le fichier certificates/schoof-control.json contient les résidus, matrices
implicites de rang1, genres, nombres de places, rang minoré et comparaison
entière du critère. Il ne prétend pas calculer tout le groupe Cl_S.
La théorie des genres et le critère d'infinitude sont invoqués comme théorèmes
publiés ; les données locales de cette réalisation sont recalculées.
