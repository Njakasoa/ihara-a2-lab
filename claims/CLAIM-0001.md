# CLAIM-0001 — Reproduction de la borne Duursma–Mak

**Statut de nouveauté : KNOWN. Niveau de preuve du laboratoire : 5, VERIFIED RESULT (reproduction connue).**

Énoncé : A(2)≥24576/77527. Aucune amélioration sur Duursma–Mak.
Construction : H:y²+(x³+x+1)y=x²+x ; compositum des cinq équations décrites
dans proofs/FINITE_GEOMETRY.md donnant k de genre343, N=192.
Choisir S de multiplicités (B₅,B₆,B₈,B₁₀)=(2,16,15,4), conducteur2 partout,
et T les192 places rationnelles. Les lieux précis d'une réalisation sont dans
certificates/dm-selected-places.json. La tour utilise la partie2-primaire
du corps de classes de rayon, puis les extensions2 non ramifiées T-décomposées.

Arithmétique : somme des degrés266 ; rang minoré75 ; marge GS57 ;
coût moyen du genre≤33751/128 ; dénominateur≤77527/128 ; quotient≥24576/77527.

Certificat fini : résidus locaux, indépendance de cinq classes AS, conductor20
pour31 caractères ; inventaire de places jusqu'au degré10 ; zêta complet via
les31 quotients de genre13. Groupe de classes : ordre exact calculé par P_k(1),
structure non calculée. Le degré exact du corps de rayon n'est pas calculé :
il s'élimine de la borne. Il ne doit pas être remplacé par une valeur inventée.

Certificat de tour : application du théorème1.1 avec données finies reproduites ;
constantes F₂ fixées par les places rationnelles décomposées, genre de base>1,
degrés non bornés et Riemann–Hurwitz. Voir reconstruction détaillée dans proofs/.

Attaque contradictoire : contrôles locaux aux deux places ramifiées et à leurs
conjugués ; comptages sur extensions ; récurrences zêta testées hors coefficients
ayant servi à leur construction ; seconde implémentation Sage PASS et revue Astra ACCEPT, rapports dans results/.

Travail antérieur le plus proche : Duursma–Mak, arXiv:1102.4127v4, §5.3,
proposition5.5/théorème1.3. Recherche2025–2026 : voir STATE_OF_THE_ART.md.
Conséquence codes : borne AG élémentaire R+δ≥−52951/24576, non positive.

Objections matérielles ouvertes : aucune dans le périmètre binaire validé.
Limites conservées : convention2-primaire, conducteur moyen majoré et non calculé
exactement, ordre du jacobien distinct de sa structure.
