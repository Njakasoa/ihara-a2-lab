# Après M1 : choix structurels et paramètres de recherche

La preuve de Duursma–Mak utilise un théorème général et une réalisation finie
particulière. La courbe de genre343 n'est pas imposée par le théorème. Pour
cette courbe fixée, la géométrie est désormais une entrée certifiée et les
multiplicités du module restent des variables discrètes.

| Paramètre | Pourquoi ce choix dans la réalisation | Contrainte de preuve | Recherche historique attestée | Domaine initial du laboratoire | Gain possible |
|---|---|---|---|---|---|
| q=2 | objet A(2) | constantes exactement F2 à chaque étage | fixé par le problème | fixé | aucun changement de corps silencieux |
| H de genre2, N=6 | plusieurs fonctions AS avec pôles communs et zéros rationnels | irréductibilité, conducteur, genre | modèle explicite du papier | fixé en M2 initial | autres bases, sous-extensions ensuite |
| sous-espace AS de dimension5 | produit de fibres de degré32 avec192 points | rang5 des résidus locaux, indépendance géométrique | construction explicite du papier | fixé en M2 initial | faire varier le sous-espace nécessite de nouvelles preuves finies |
| deux places de H de degré5 | conducteur20 pour chaque caractère non trivial | vérifier les pôles réduits et toute autre ramification | choix de polynôme dans le papier | géométrie fixée | changer ces places change la courbe k |
| g(k)=343,N(k)=192 | conséquences exactes du modèle | Riemann–Hurwitz et décomposition rationnelle | calculés dans le papier | certifiés indépendamment | pas des variables libres pour k fixé |
| T, ensemble de places rationnelles | numérateur de la borne et pénalité de rang | T non vide, distinct, disjoint de S | les192 places dans l'exemple principal | t=1,…,192 ; identités indifférentes au score universel | moins de T peut faciliter GS mais baisse le numérateur |
| S, places permises au module | dimensions locales contre coût de genre | inventaire disponible et inégalité GS | le papier expose une bonne sélection, sans certificat d'optimalité exhaustive | degrés5,6,8,10,12, multiplicité de0 au stock disponible | échanges de degrés, places omises historiquement |
| profondeur ν_P | davantage de générateurs locaux avec davantage de relations/conducteur | contribution exacte au rang et majorant de conducteur justifié | ν=2 pour les exemples binaires retenus | ν=2 globalement puis variations locales ν=4,6 | conducteurs non uniformes à tester ; ν impair dominé pour ce score |
| partie2-primaire du corps de rayon | application du critère de2-tour | extension abélienne finie de degré puissance de2, T décomposé | argument p-groupe du papier | définition fixée | le groupe exact peut améliorer des estimations mais n'est pas calculé ici |
| théorème GS et bornes de relations | certificat suffisant d'infinitude | I≥0 avec D≥2 | démontrés dans le papier | théorème1.1, version binaire auditée | un autre critère nécessite son propre adaptateur de preuve |
| majorant du conducteur moyen | transforme la ramification en dénominateur | moyenne de caractères, restriction uniforme aux images locales | raffinement binaire du papier | filtration locale prouvée | calculer des images plus petites pourrait renforcer la borne |

Le stock initial non rationnel jusqu'au degré12 est (2,16,16,64,208) aux
degrés(5,6,8,10,12). Le nombre brut de vecteurs de multiplicités est
3·17·17·65·209=11 778 195, avant le choix de t. Les branches trop coûteuses
pour battre la borne témoin peuvent être coupées exactement. Pour un module
fixé, le dénominateur ne dépend pas de t ; le meilleur t admissible est

    min(N, A, 1+A−ceil(sqrt(2C+4A))).

S'il est inférieur à1, ce certificat d'infinitude échoue. Ce n'est pas une
preuve de finitude de la tour. Le moteur doit valider cette élimination de t
contre une énumération exhaustive sur de petits cas.

Aucune recherche historique exhaustive n'est déduite de l'absence de détail
dans le papier. Aucun optimum sur cette boîte n'est annoncé pour la famille
entière, pour d'autres conducteurs ou pour des groupes de rayon exacts.
