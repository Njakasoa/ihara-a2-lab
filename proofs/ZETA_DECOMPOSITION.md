# Zêta complet du corps k de genre343

La preuve locale établit [k:H]=32 et g(H)=2. Chaque sous-corps quadratique
C_h/H, h∈F₂⁵\{0}, a deux places de degré5 ramifiées avec conducteur2.
Donc 2g(C_h)−2=2(2g(H)−2)+20=24, soit g(C_h)=13.

La décomposition en caractères du groupe (Z/2)⁵ donne
Z_k=Z_H∏_{h≠0}(Z_{C_h}/Z_H), et donc
P_k=∏_{h≠0}P_{C_h}/P_H³⁰.
C'est une identité de fonctions zêta, pas une déduction à partir d'une
seule liste de premiers coefficients.

`src/zeta_cover.py` compte chaque C_h sur F_{2^n}, n=1,…,14.
Une fonction h est un masque binaire sur [1,x,x²,y,y²]. À un point régulier,
le nombre de solutions est2 si la trace du radicand est nulle, sinon0.
À chaque point ramifié c=0 le modèle normalisé a une seule place au-dessus.
Les deux places de H à l'infini donnent chacune deux points de C_h.

Les identités de Newton donnent c₁,…,c₁₃ pour P_{C_h} à partir des treize
premiers comptes. Le genre déjà prouvé et l'équation fonctionnelle imposent
c_{26−i}=2^{13−i}c_i. Il ne s'agit pas d'utiliser l'équation fonctionnelle
pour deviner un genre inconnu. Le compte n=14, non utilisé pour ajuster les
coefficients, est comparé à la récurrence de chaque polynôme.

Le produit est divisé exactement trente fois par P_H=1+3T+5T²+6T³+4T⁴.
Tous les restes sont nuls. Le résultat a degré686 et satisfait
c_{686−i}=2^{343−i}c_i. Le certificat fournit chaque quotient, tous les comptes,
les coefficients complets et P_k(1)=#Jac(k)(F₂). La valuation2 de cet ordre
vaut51 ; cela ne détermine ni la structure du groupe, ni son rang2.

Les racines de Weil découlent de la réalisation géométrique et du théorème de
Weil. La seconde implémentation Sage a également vérifié exactement, dans AA, les
racines des31 polynômes de Weil réels associés et leur appartenance à
[−sqrt(8),sqrt(8)] ; voir results/INDEPENDENT_VALIDATION.md. L'intégralité et
l'équation fonctionnelle seules ne certifieraient pas un polynôme arbitraire.
