# Lemme d'échange de degrés pour le score binaire de profondeur2

Ce lemme explique le candidat issu de M2. C'est une identité élémentaire du
score du théorème existant ; aucune nouveauté de cette identité n'est présumée.

Fixer un corps de fonctions sur F2 de genre g>1, un ensemble rationnel
non vide T de taille t, et un module2ΣP satisfaisant le critère du laboratoire.
Écrire A=Σdeg(P), C=Σdeg(P)(deg(P)+1), D=1+A−t et I=D²−2C−4A≥0.
Le dénominateur majorant est

    B = g−1+Σ w(deg(P)),   w(f)=f(1−2^(−f)).

Supposons que le support possède au moins deux places distinctes de degré d,
et que deux nouvelles places distinctes, hors du support et hors de T, soient
disponibles aux degrés d−h et d+h, avec h≥1 et d−h≥2. Remplacer les deux
places de degré d par ces nouvelles places. Alors

    A' = A,   C' = C+2h²,   D'=D,   I'=I−4h²,
    B' = B−Δ(d,h),

avec

    Δ(d,h)=2^(−d)[(d−h)2^h+(d+h)2^(−h)−2d]
          =(2^h−1)[d(2^h−1)−h(2^h+1)] / 2^(d+h).

En particulier, si I≥4h² et

    d > h(2^h+1)/(2^h−1),

le nouveau module est encore admissible et le quotient t/B' est strictement
supérieur à t/B. La condition t≤A est conservée et B'>0, car g>1 et les coûts
locaux sont positifs. La conclusion concerne la borne certifiée, non une
égalité entre genres réels de deux corps de rayon.

Preuve : la somme des deux degrés reste2d. La somme f(f+1) augmente de
(d−h)(d−h+1)+(d+h)(d+h+1)−2d(d+1)=2h². Il en résulte la perte4h² de marge.
Les termes linéaires de w s'annulent dans2w(d)−w(d−h)−w(d+h), donnant Δ.
Sa factorisation donne exactement la condition de positivité. Appliquer le
même critère de tour et le même majorant de conducteur aux nouveaux lieux.

Pour la sélection publiée de Duursma–Mak : d=10,h=2,I=57. Une place de degré8
était disponible hors du support ; le certificat supplémentaire fournit des
places de degré12. L'échange laisse I'=41 et Δ=15/1024, donc transforme le
dénominateur77527/128 en620201/1024. Le gain ne provient pas d'un changement de
genre ou de nombre de points de la base, mais d'une réduction de ce majorant de
conducteur moyen.

Le lemme fournit un élagage ou une amélioration locale générique pour un moteur :
un module disposant d'un tel échange ne peut être optimal pour le score.
Pour élaguer une recherche restreinte, les deux nouveaux degrés et leurs
multiplicités doivent également rester dans son domaine déclaré.
Il ne montre aucune barrière pour les modules sans cet échange, pour les
conducteurs supérieurs, ou pour les corps de rayon calculés exactement.
