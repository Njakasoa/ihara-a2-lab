# M2/M3 — acceptation du résultat

**M2 accepté. CLAIM-0002 : VERIFIED RESULT, niveau5 du laboratoire.**

Borne : A(2)≥196608/620201. Paramètres(A,C,D,I)=(266,2260,75,41),
dénominateur620201/1024, numérateur192. Preuve : proofs/IMPROVED_BOUND.md.

- Deux recherches automatiques convergent sans vecteur amélioré fourni en entrée.
- Le moteur évalue exactement les paramètres binaires de Duursma–Mak, avec
  calcul optimal de t, multiplicités, profondeur et inventaire comme entrées.
- Le domaine exhaustif initial est k343, S non rationnel, degrés≤12, ν=2.
  99 835 configurations évaluées ; 11 678 360 exclues par une borne exacte.
- 14 112 variantes locales ν∈{2,4,6} : aucune amélioration. Domaine détaillé
  dans results/M2_SEARCH.md, sans assertion sur tous les modules non uniformes.
- Sage indépendant final : PASS, sortie0 observée par la racine ; lieux,
  Frobenius, sélection, module, arithmétique et mutations négatives vérifiés.
- Astra : ACCEPT de la preuve de tour, de l'échange général et de la
  transcription de la note. La condition de contrôle indépendant est satisfaite.
- L'audit séparé de nouveauté recommande POSSIBLY NOVEL, priorité non établie.
- Conséquence AG élémentaire négative ; aucun meilleur code binaire revendiqué.

Le résultat utilise la méthode et la courbe de Duursma–Mak ; sa contribution
est une sélection améliorée du support du module et son certificat exact.
Les groupes de rayon exacts, les degrés auxiliaires exacts et les structures
de groupes de classes ne sont pas artificiellement remplis.

Explorations annexes : base des373 sous-corps, comparaisons de leurs scores,
recherche étendue des degrés. Consulter leurs rapports séparés pour le domaine
et les limites ; aucune extrapolation à toutes les tours n'est autorisée.

CLAIM-0003 : l'obstruction tous degrés pour le score nu2 sur la base fixée
est également validée. Le checker indépendant par déficits et partitions
confirme zéro amélioration et ferme la condition de la revue Astra.
Rapport : results/INDEPENDENT_OBSTRUCTION.md. Priorité non établie.

La condition de préparation d'une note locale est remplie. La condition de
publication externe ne l'est pas : aucune publication ou prise de contact.
