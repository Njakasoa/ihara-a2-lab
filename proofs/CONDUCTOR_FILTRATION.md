# Majorant de conducteur moyen par filtration locale

Dérivation du laboratoire, **acceptée par la revue Astra M1** : voir
results/ASTRA_M1_REVIEW.md. Le passage M1 est accepté après les tests indépendants.
Les conventions sont celles du conducteur d'Artin des caractères de rang1.

Soit K/k une extension abélienne p-primaire, de conducteur local au plusν≥2
à une place de degréf sur F_q. Soit I^r l'image du groupe d'unités supérieures
U^r dans l'inertie. La partie modérée étant d'ordre premier à p, I^0=I^1.
Pour un caractère χ uniforme du groupe global, sa restriction à I^r est
uniforme dans le dual de I^r ; donc Pr(χ trivial sur I^r)=1/|I^r|.
La réciprocité locale identifie a_P(χ)≤r à cette trivialité pour r≥1,
et a_P(χ)=0 à la trivialité sur I^0. Aucun caractère p-primaire n'a conducteur1.

L'identité des queues pour une variable entière comprise entre0 etν donne

E[a_P]=Σ_{r=0}^{ν−1}Pr(a_P>r)=ν−Σ_{r=0}^{ν−1}1/|I^r|.

Or |I^r|≤q^{f(ν−r)} pour1≤r<ν, et |I^0|=|I^1|≤q^{f(ν−1)}.
Ainsi

E[a_P] ≤ ν − 2q^{−f(ν−1)} − Σ_{j=1}^{ν−2}q^{−fj}.

Multiplier par f pour la contribution au degré du conducteur global, puis
sommer sur les places. Aucune indépendance des inerties entre places n'est
supposée : la linéarité de l'espérance suffit.

Pour q=2,ν=2, on retrouve exactement2(1−2^{−f}), le majorant de la
construction principale de Duursma–Mak. Pour ν>2, ne pas réutiliser aveuglément
ν(1−q^{−f}) : la filtration contient davantage de couches.
Le majorant ne suppose pas que les inerties atteignent leur ordre maximal.

Dans le seul score du théorème1.1 en caractéristique2, remplacer un conducteur
impairν=2m+1 parν−1 conserve le terme de rang
f(ν−1−floor((ν−1)/2)), diminue le majorant de relations et diminue ce coût de
genre. Les conducteurs impairs≥3 sont donc dominés pour ce score conservateur.
Cette dominance ne prouve aucune inclusion optimale entre groupes de rayon
calculés exactement et ne s'étend pas sans examen à un autre critère de tour.
