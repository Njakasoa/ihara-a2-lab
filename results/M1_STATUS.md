# M1 — tableau d'acceptation

| Obligation | État | Preuve ou action restante |
|---|---|---|
| Normalisation exacte | écrit | NORMALIZATION.md |
| État de l'art daté | terminé au 2026-09-13 | STATE_OF_THE_ART.md, couverture explicitée |
| Sage/PARI | installés localement | audit PASS et verrou exact de 387 paquets |
| Courbe elliptique, hyperelliptique, H | calculés | genre, comptes, zêta |
| Schoof2/9 | reconstruit | modèle corrigé, ramification, théorie des genres |
| Duursma–Mak24576/77527 | reconstruit | k/H degré32, g343,192 points, GS57 |
| Lieux explicites S,T | calculés | orbites de Frobenius canoniques |
| Zêta de k, degré686 | calculé |31 quotients de genre13, contrôle n14 |
| Ordre du jacobien de k | calculé | P_k(1), v₂=51 |
| Structure de groupe de classes de k | non calculée | non requise par la borne utilisée |
| Groupe/degré exact du corps de rayon K/k | non calculé | doit rester inconnu dans les certificats |
| Chemin calcul classes/rayon/Riemann–Roch | audité | ENVIRONMENT_AUDIT.md ; groupe de rayon exact non calculé |
| Tests internes |9 passés | test_exact_controls.py |
| Seconde implémentation | PASS | results/INDEPENDENT_VALIDATION.md ; exécution racine exit 0 |
| Revue Astra | ACCEPT conditionnel satisfait | results/ASTRA_M1_REVIEW.md |
| Conséquence codes | écrite | borne élémentaire négative |

**Gate : M1 ACCEPTÉ le 2026-09-13. M2 autorisé.**

La racine a exécuté la version corrigée de `tests/independent_sage.py` avec Sage10.9 : `INDEPENDENT_SAGE_STATUS=PASS`, sortie0, environ47 secondes. Les réserves de rédaction Astra ont été corrigées. Les données ternaires non certifiées restent exclues. L’ordre et la structure exacts du corps de rayon ne sont pas nécessaires au théorème binaire utilisé et ne sont pas présentés comme calculés.
