# Places supplémentaires de degré12 sur k

La disponibilité de places de degré12 peut être certifiée sans développer le
polynôme zêta de degré686. Le certificat `certificates/degree12-lifting.json`
travaille uniquement dans F64=F2[u]/(u6+u+1), codé par le module binaire67.

Les treize couples (x,y) du certificat vérifient l'équation de H. Chacun a
une orbite de Frobenius de longueur6, et leurs orbites sont distinctes. Aucun
n'annule c=x5+x2+1. Il s'agit donc de treize places distinctes de degré6 de H,
non ramifiées dans l'extension élémentaire abélienne k/H de degré32 déjà
certifiée dans M1.

À une telle place, le Frobenius dans Gal(k/H)=(F2)^5 a pour coordonnées

    Tr_F64/F2((x²+x) h / (x⁵+x²+1)²), h∈[1,x,x²,y,y²].

C'est la description usuelle du Frobenius d'une équation w²+w=f : son action
sur w est la translation par Tr(f). Les treize vecteurs consignés sont non
nuls. Ils sont donc d'ordre2. La décomposition non ramifiée fournit, au-dessus
de chacune de ces places, 32/2=16 places distinctes de degré6·2=12.
Les places au-dessus de places différentes de H sont disjointes. Ainsi

    B12(k) ≥ 13·16 = 208.

Ce minorant suffit pour choisir n'importe quel nombre de places jusqu'à208 ;
il n'exige aucune affirmation sur les autres places de H. Le calcul complet
du zêta donne en outre l'égalité B12(k)=208.

`curves/k343-degree12-places.json` contient les208 représentants explicites
sur F4096, avec leurs sept coordonnées (x,y,w1,…,w5), leur module irréductible
et leur degré d'orbite. `src/degree12_certificate.py` régénère le petit
certificat de remontée ; `src/exact_curves.py:enumerate_k_places(12)` régénère
les représentants sur k. Leur contrôle indépendant Sage initial est PASS ; voir
`results/INDEPENDENT_M2_VALIDATION.md`. La revue Astra du raisonnement de
remontée est favorable. Ces contrôles de places ne constituent pas encore une
validation arithmétique d’un candidat M2.
