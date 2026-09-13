# CLAIM-0002 — Modification du support de Duursma–Mak

Énoncé vérifié : **A(2)≥196608/620201≈0,317006905825692**.
Statut mathématique : **VERIFIED RESULT, niveau5** ; preuve complète,
Sage indépendant PASS et Astra ACCEPT. Statut de nouveauté : **POSSIBLY NOVEL**, distinct de la validité.

Construction : même k/F2 de genre343,N192 que Duursma–Mak ; T toutes les places
rationnelles ; module2 aux places de multiplicités(2,16,16,2,1) aux
degrés(5,6,8,10,12). Partie2-primaire du corps de rayon et tour2 non ramifiée
T-décomposée. Ni le degré exact du corps de rayon, ni sa structure de groupe
ne sont calculés ou nécessaires au quotient démontré.

Preuve : proofs/IMPROVED_BOUND.md. Certificat fini : M1 et
certificates/degree12-lifting.json ; coordonnées explicites dans
certificates/m2-tower.json. Paramètres GS(A,C,D,I)=(266,2260,75,41).
Dénominateur≤620201/1024 ; numérateur192.

Découverte : experiments/reference_nu2_search.py a énuméré99 835 feuilles
sous un élagage exact fondé sur la borne historique. Le vecteur amélioré
n'était pas une entrée. Le moteur général Luna retrouve indépendamment le même résultat.
Ce vecteur de multiplicités et t est le seul maximum du score conservateur
dans le domaine restreint exploré
par la référence : k fixé, S non rationnel, degrés≤12, ν=2,1≤t≤192. La preuve
d'optimalité dans ce domaine ne vaut pas pour d'autres bases, degrés ou critères.

Comparaison avec Duursma–Mak : gain exact368640/48082322927. On remplace
(10,10) par(8,12), coût de genre réduit de15/1024, marge GS encore positive.

Contrôles indépendants : Sage pour tous les lieux et treize remontées degré6
vers12 ; arithmétique du candidat et attaques négatives PASS dans
results/INDEPENDENT_M2_VALIDATION.md. Revue Astra ACCEPT dans
results/ASTRA_M2_REVIEW.md. Les conditions de promotion sont satisfaites ; toute nouvelle objection
matérielle devra être instruite.

Travail antérieur : Duursma–Mak2013, même théorème et même courbe. Recherche
2025–2026 : STATE_OF_THE_ART.md et references/m2-novelty-search.md ; recherches
complémentaires de la fraction consignées au journal. Aucun antécédent exact
identifié dans cette couverture ; aucune affirmation d'exhaustivité.

Conséquence codes : R+δ≥−423593/196608, garantie élémentaire non positive.
Pas de nouveau meilleur code binaire affirmé.

Objections mathématiques matérielles ouvertes : aucune identifiée dans le
périmètre certifié. Priorité non établie ; audit séparé de nouveauté dans
references/M2_NOVELTY_VERDICT.md. Publication externe interdite
sans autorisation explicite de l'utilisateur.
