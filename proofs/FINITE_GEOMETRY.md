# Certificat fini de la construction de genre 343

Ce document fournit la dérivation du laboratoire, à contrôler indépendamment.
Source de l'équation : Duursma–Mak, arXiv:1102.4127v4, §5.3, pp.18–19.
Les résultats calculés sont dans certificates/dm-finite-geometry.json.
Les éléments de F_{2^n} sont encodés en bits, coefficient constant en premier.

Posons a=x³+x+1, b=x²+x, c=x⁵+x²+1 et H : y²+a y=b.
L'irréductibilité de a et de c est vérifiée par Frobenius et PGCD polynomiaux.
La courbe est toujours le modèle projectif lisse du corps de fonctions.

## Courbe H

En posant z=y/a, z²+z=b/a². Aux trois racines α de a dans F₈, la variable
locale t=x−α est une uniformisante sur la droite. Écrivons
b/a²=A/t²+B/t+O(1). Comme le carré d'une série en caractéristique 2 n'a
pas de terme de degré impair, A=b(α)/a'(α)² et B=b'(α)/a'(α)².
Le remplacement z↦z+sqrt(A)/t réduit le pôle à
(B+sqrt(A))/t. Les trois résidus calculés sont non nuls.
Il y a donc une place ramifiée de degré 3, saut 1, différente 2.
Riemann–Hurwitz donne 2g(H)−2=−4+2·3=2, donc g(H)=2.
Un pôle réduit impair empêche b/a² d'être u²+u, même après extension des
constantes : irréductibilité géométrique. À l'infini b/a² s'annule, donc
les deux places au-dessus de l'infini sont rationnelles. Le corps complet
des constantes est F₂. La projection affine n'a pas à elle seule le rôle
de certificat de lissité de sa clôture plane.

## Extension k/H

Pour h dans W=⟨1,x,x²,y,y²⟩_{F₂}, poser w_h=v_h/c :
w_h²+w_h=b h/c². Le corps k est le compositum pour une base de W.
Les cinq racines de c dans F₃₂ ont chacune deux valeurs y dans F₃₂.
Ces dix points forment deux places de degré 5 de H, puisque c est irréductible.
Ils sont distincts des zéros de a, donc x−α est une uniformisante sur H.

Différentiation dans H : y'=(1+(x²+1)y)/a ; (y²)'=0.
Pour N=b h, les deux coefficients polaires valent
A=N/c'² et B=N'/c'², évalués au point (α,y).
Le résidu réduit est ρ(h)=B+sqrt(A).

Le calcul dans F₃₂ montre que la matrice des cinq ρ(h) a rang 5 sur F₂
à chacun des dix points. Il s'agit de deux orbites de Frobenius ; tous les
représentants sont contrôlés pour éviter un choix implicite de place.
Ainsi chaque h non nul a un pôle réduit simple aux deux places de degré 5.
Les cinq classes Artin–Schreier sont indépendantes, donc Gal(k/H)≅(Z/2)⁵
et [k:H]=32, y compris géométriquement. L'inertie à chaque P₅ est le groupe
entier : sinon un caractère non nul trivial sur l'inertie donnerait une
sous-extension quadratique non ramifiée à cette place, contredisant le rang 5.
Les deux places sont donc totalement ramifiées, avec degré résiduel 1.

Les fonctions b h/c² n'ont pas d'autre pôle fini. À chacune des deux places
à l'infini de H, y a un pôle d'ordre au plus 3 ; les ordres au numérateur
sont au plus 8 et celui de c² est 10. Toutes les fonctions s'annulent donc
à l'infini. Les deux places s'y décomposent totalement.

Les 31 caractères non triviaux ont chacun conducteur 2P₅+2P'₅, de degré 20.
La formule conducteur–discriminant et Riemann–Hurwitz donnent
2g(k)−2=32(2g(H)−2)+31·20=684, donc g(k)=343.
Au-dessus de x=0,1, le facteur b est nul et c=1 : les quatre places de H
se décomposent totalement ; avec les deux à l'infini, N(k)=6·32=192.
Aucune autre place rationnelle n'est possible puisque toute place rationnelle
de k se restreint à une place rationnelle de H. Les constantes sont F₂.

## Comptage des places

Sur F_{2^n}, pour chaque x et chaque y de H, hors c=0, les cinq équations
Artin–Schreier ont 32 solutions exactement lorsque leurs cinq traces sont
nulles, sinon aucune. Pour c=0, on compte la place du modèle normalisé,
une par point de H, par la ramification totale certifiée ci-dessus.
À l'infini, on ajoute 64 points.
Les comptes jusqu'à n=10, suivis de l'inversion N_n=Σ_{d|n}d B_d, donnent
(B₁,…,B₁₀)=(192,0,0,0,2,16,0,16,0,64).
Ces premiers comptes ne suffisent pas à reconstruire directement le polynôme
zêta de degré686. Celui-ci est maintenant reconstruit séparément via les31
quotients quadratiques : voir ZETA_DECOMPOSITION.md. E, H et y²+y=x⁵+x ont
aussi leurs polynômes zêta complets et leurs contrôles distincts.

## Portée et dépendances

La preuve utilise les théorèmes standards Artin–Schreier, conducteur–discriminant
et Riemann–Hurwitz. Aucun groupe de classes n'est déduit de ces seules données.
Le code fournit l'algèbre finie ; la preuve ci-dessus justifie les modèles
normalisés, les points à l'infini et les corrections aux lieux ramifiés.
