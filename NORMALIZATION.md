# Normalisation et obligations de preuve

Sur F_q, N_q(g) est le maximum de #X(F_q) parmi les courbes lisses,
projectives, géométriquement irréductibles de genre g. A(q)=limsup_{g→∞} N_q(g)/g.
La courbe associée à un corps de fonctions F/F_q est son modèle projectif lisse ;
F_q doit être le corps complet des constantes. Une équation affine seule ne certifie
ni la lissité de sa clôture plane ni son genre.

Une place P est un point fermé ; deg(P)=[κ(P):F_q]. Écrire B_d(F) pour le nombre
de places de degré d, N_n(F)=#X(F_{q^n}). Alors N_n=Σ_{d|n} d B_d et
B_n=(1/n)Σ_{d|n} μ(n/d)N_d. N(F)=B_1=N_1.

Z_X(T)=exp(Σ_{n≥1}N_n T^n/n)=P_X(T)/((1-T)(1-qT)).
P_X(T)=∏_{i=1}^{2g}(1-α_i T), |α_i|=sqrt(q).
Attention : les zéros en T ont module 1/sqrt(q) ; ce sont les racines réciproques
α_i (valeurs propres de Frobenius) qui ont module sqrt(q).
Le nombre de classes de degré zéro est P_X(1), pas nécessairement sa structure.

Pour une tour géométrique F_i de genres tendant vers l'infini,
liminf N(F_i)/g(F_i) donne une borne inférieure de A(q).
Dans une tour non ramifiée au-dessus de K de genre >1 et de degrés non bornés,
g(F_i)-1=[F_i:K](g(K)-1). Si t places rationnelles se décomposent totalement,
N(F_i)≥t[F_i:K], donc A(q)≥t/(g(K)-1).
Un unique grand ratio N/g n'est pas une borne asymptotique.

Conventions : m=Σν_P P est une borne de conducteur, S son support effectif,
T un ensemble non vide de places rationnelles disjoint de S. ν_P désigne
l'exposant du conducteur d'Artin, pas la valuation du discriminant. Pour une
extension Artin–Schreier réduite z²+z=f et un pôle d'ordre impair m_P,
le conducteur local vaut m_P+1 et la différente vaut m_P+1.
Le genre se calcule par Riemann–Hurwitz sur le modèle normalisé.

Tous les scores de preuve sont des entiers ou fractions exacts. Une décimale
est uniquement un affichage. Statuts séparés : EXACT FINITE FIELD,
EXACT INTEGER, EXACT RATIONAL, PROVED TOWER, CERTIFIED CLASS GROUP,
HEURISTIC SEARCH, CONJECTURED FAMILY. Un nombre de classes n'est pas un
certificat de groupe de classes. Une inégalité suffisante échouée ne démontre
pas qu'une tour est finie.

Niveaux 0–5 : candidat numérique ; calcul exact reproduit ; contrôles indépendants ;
certificats algébriques finis complets ; preuve asymptotique complète ; seconde
implémentation et revue Astra contradictoire. VERIFIED RESULT ≠ NOVEL RESULT.

Sources : Duursma–Mak, arXiv:1102.4127v4, §§1–3,5 ; conventions standards des
corps de fonctions. Les limites effectives du validateur figurent dans README.md.
