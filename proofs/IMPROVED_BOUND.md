# Une sélection améliorée sur le corps de Duursma–Mak

**Énoncé vérifié : A(2) ≥ 196608/620201.** Niveau5 du laboratoire. Preuve ci-dessous ; état de
validation indépendant dans results/INDEPENDENT_M2_VALIDATION.md et
results/ASTRA_M2_REVIEW.md. La nouveauté est une question séparée.

## 1. Corps fini de départ et disponibilité des places

Sur F2, poser a=x³+x+1, b=x²+x, c=x⁵+x²+1. Soit H le corps de fonctions de
la normalisation projective de y²+ay=b. Il a genre2 et six places rationnelles.
Soit k le compositum des cinq extensions

    w_i²+w_i = b h_i/c²,  (h_1,…,h_5)=(1,x,x²,y,y²).

La réduction locale aux dix points géométriques de c=0 donne deux applications
F2-linéaires de rang5, une à chaque place de H de degré5. Tout caractère
non trivial du compositum a conducteur2 à chacune de ces deux places, et
aucune autre ramification. Les cinq classes AS sont donc géométriquement
indépendantes et [k:H]=32. Riemann–Hurwitz/conducteur-discriminant donne

    2g(k)−2 = 32·(2g(H)−2)+31·20 = 684.

D'où g(k)=343. Les six places rationnelles de H se décomposent complètement,
donnant exactement192 places rationnelles de k. Le corps des constantes est
F2. Cette construction est celle de Duursma–Mak, non une nouvelle courbe.
Les détails locaux et contrôles indépendants sont ceux de M1.

Les inventaires exacts donnent au moins2,16,16,64 places de degrés5,6,8,10.
En outre k possède au moins208 places de degré12 : les treize places de degré6
de H du petit certificat degree12-lifting.json ont toutes un Frobenius
non nul dans (F2)^5, donc d'ordre2, et chacune fournit16 places de degré12.
Voir proofs/DEGREE12_PLACES.md. La preuve n'exige que l'existence d'une seule
place supplémentaire de degré12.

Choisir T égal à l'ensemble des192 places rationnelles de k, et choisir S de
multiplicités

| degré f |5|6|8|10|12|
|---|---:|---:|---:|---:|---:|
| nombre de places |2|16|16|2|1|

Toutes ces places fermées sont distinctes et S est disjoint de T. Le fichier
certificates/m2-tower.json fixe une réalisation par les premiers représentants
canoniques de chaque inventaire. Le choix des représentants n'affecte pas le
critère universel employé ci-dessous. Poser m=2Σ_{P∈S}P.

## 2. Application du critère de tour

Soit K/k la partie2-primaire du corps de classes de rayon de module m où T
se décompose complètement. C'est une extension abélienne finie géométrique ;
son degré n est une puissance de2, dont la valeur exacte n'est pas requise.
Construire au-dessus de K sa tour2 maximale non ramifiée dans laquelle les
places T_K au-dessus de T restent complètement décomposées. Noter L son union.

Dans le théorème1.1 de Duursma–Mak, avec p=q=2 et tous les ν_P=2, poser

    A = Σ f_P = 2·5+16·6+16·8+2·10+12 = 266,
    C = Σ f_P(f_P+1) = 60+672+1152+220+156 = 2260,
    D = 1+A−|T| = 75.

On a |T|=192≤266=A et

    I = D²−2C−4A = 5625−4520−1064 = 41 > 0.

Pour expliciter l'argument, si G=Gal(L/k) était fini, les bornes des
propositions3.3/5.3 et théorème4.1 donneraient

    d_2(G)≥75,   r_2(G)−d_2(G)≤C/2+192−1=1321.

Pour d≥75, la fonction d²/4−d est croissante et vaut au moins5325/4.
Or1321<5325/4, en contradiction avec l'inégalité stricte de
Golod–Shafarevich r>d²/4 pour un2-groupe fini non trivial. La tour est infinie.
Cette preuve utilise les estimations de rang, pas un calcul du groupe de rayon.

## 3. Conducteur moyen et quotient asymptotique

À une place P de degré f, l'image de l'inertie locale dans Gal(K/k) a ordre
au plus2^f, car ν_P=2 et le quotient sauvage U¹/U² a cet ordre. Un caractère
uniforme du groupe global est trivial sur cette image avec probabilité
1/|I_P|≥2^(−f). Les caractères2-primaires ont conducteur local0 ou2 : le
quotient modéré a ordre impair. Ainsi

    E[a_P(χ)] ≤ 2(1−2^(−f)).

Cette affirmation reste vraie si certaines places de S ne ramifient finalement
pas après les relations de décomposition. Elle ne suppose ni inertie maximale,
ni indépendance entre places, ni connaissance de n. Par linéarité,

    E[deg f_χ] ≤ 2[10(1−2^(−5))+96(1−2^(−6))
                    +128(1−2^(−8))+20(1−2^(−10))+12(1−2^(−12))]
                = 269993/512.

La formule conducteur-discriminant donne alors

    g(K)−1 = n(342+E[deg f_χ]/2) ≤ n·620201/1024.

Les192 places de T fournissent192n places rationnelles de K décomposées dans
la tour. Toute sous-extension finie K_j/K de cette tour est non ramifiée,
donc g(K_j)−1=[K_j:K](g(K)−1) et N(K_j)≥[K_j:K]192n.
La décomposition de T non vide fixe F2 comme corps complet des constantes.
L'infinitude de la tour et g(K)>1 donnent des genres non bornés. En passant à
la limite du quotient points/genre,

    A(2) ≥ 192n/(g(K)−1) ≥ 192/(620201/1024) = 196608/620201.

## 4. Comparaison exacte et portée

La sélection publiée utilise(2,16,15,4,0). Le nouveau module échange deux
places de degré10 contre une de degré8 et une de degré12. La somme des degrés
reste266 ; C augmente de8 et la marge I diminue de16, passant de57 à41.
Le dénominateur majorant diminue strictement de15/1024 :

    77527/128 − 620201/1024 = 15/1024.

Par conséquent

    196608/620201 − 24576/77527 = 368640/48082322927 > 0.

Le gain provient du même théorème et de la même courbe, grâce à un autre support
du module. Il ne donne ni la valeur exacte de A(2), ni une nouvelle équation
récursive, ni un calcul du corps de rayon complet. Une recherche finie de
paramètres et une preuve du résultat sont des objets distincts : le présent
argument n'a pas besoin d'affirmer une optimalité globale du candidat.

La conséquence AG élémentaire formelle est

    R+δ ≥ 1−620201/196608 = −423593/196608.

Elle n'offre pas de garantie binaire positive ; aucune amélioration de code
industriel ou de borne optimale de codes n'en est déduite.

## 5. Dépendances contrôlables

- Duursma–Mak, *On lower bounds for the Ihara constants A(2) and A(3)*,
  arXiv1102.4127v4, théorème1.1, propositions5.1–5.3 et5.5 ; version publiée
  Compositio149(2013), DOI10.1112/S0010437X12000796.
- M1 : proofs/FINITE_GEOMETRY.md, DUURSMA_MAK_RECONSTRUCTION.md,
  CONDUCTOR_FILTRATION.md, results/INDEPENDENT_VALIDATION.md.
- Places supplémentaires : certificates/degree12-lifting.json,
  curves/k343-degree12-places.json, tests/independent_candidate.py.
- Découverte automatique : experiments/reference_nu2_search.py ; le seul
  témoin fourni à la recherche est la borne publiée, sans vecteur amélioré.
- Certificat lié aux lieux : experiments/bind_candidate.py,
  certificates/m2-tower.json.
