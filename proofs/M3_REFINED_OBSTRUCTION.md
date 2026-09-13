# All-depth obstruction after elementary-ray and local-rank refinements

Status: VERIFIED RESULT, internal level 5: final Astra proof acceptance and
independent finite verification PASS; see results/M3_ASTRA_REVIEW.md and
results/M3_INDEPENDENT_VALIDATION.md. The scoring theorem is M3_REFINED_RAY_CRITERION.md.

Fix k343, b=196608/620201, arbitrary finite ramification support including
rational places, and a disjoint splitting set of size1<=t<=192. By the
elementary character cutoff reduction it suffices to take nu_P=2s_P.
Let n be the number of rational ramified places, A=sum f*s and
C=sum (f*s)(f*s+1). Thus t<=192-n, A>=n, t<=A, and

    (1+A-t)^2 >= 2C+4A.

## 1. New rebate estimate, not the old full-ray estimate

The elementary rebate is r=f*(1-2^(-fs))/(2^f-1). At a rational place r<1.
At a degree f>=10 place, r<=f/(2^f-1)<=f*s/1023. For f=5,6,8,

    r - f*s/1023 <= f/(2^f-1)-f/1023.

Their stock is respectively2,16,16. Define exactly

    beta=sum_{f=5,6,8} B_f*f*(1/(2^f-1)-1/1023)
        =1290176/608685.

Using at least n units of A at rational places gives the universal bound

    R <= n+beta+(A-n)/1023,
    cost=A-R >= L_n(A)=max(0,A-n-beta-(A-n)/1023).

This is weaker than possible because it grants saturation of every rebate;
it therefore includes all potential improvements, at arbitrary depths/degrees.

## 2. Refined relation deficit

Write a=f*s. Then C_P-11a=a(a-10). For rational places this is bounded below
by-25, with minimum at a=5. For nonrational f=5,6,8 the minima over s>=1
are respectively-25,-24,-16; for f>=10 the expression is nonnegative.
Consequently

    C >= max(0,11*A-690-25*n).

## 3. Finite necessary pairs

A strict improvement requires

    A < ((192-n)/b-342+n+beta-n/1023)*1023/1022 = E_n,
    t >= floor(b*(342+L_n(A)))+1 = t_min.

Enumerate n=0,...,191 and A=n,...,ceil(E_n)-1. Discard t_min>min(A,192-n)
and then C_min>floor(((1+A-t_min)^2-4A)/2). Exact root arithmetic leaves only

    n=0, A=266, t=192, 2236<=C<=2280.

These necessary caps are proved before imposing any degree or depth cutoff.

## 4. The single possible higher-depth pattern also fails

Against the floor11A-690, a degree5 place of depth4 (a=10) has penalty25.
A degree6 place of depth4 has penalty48; degree8 has penalty112; any
degree>=10 place of depth4 has penalty at least200. Depth6 at degree5
already has penalty100. Monotonicity beyond these cases follows because
a(a-10) increases for a>=5.

Only44 units of penalty are available. Thus every non-shallow configuration
would have exactly one degree5 place at depth4, all other depths2. Both
degree5 places and all16 degree6 places must be selected: omitting one costs
another25 or24, exceeding the remaining19. At most one degree8 place can
be omitted, each omission costing16. This leaves exactly two possibilities
for the total rank mass R_h carried by degrees>=10 and their C budget:

| Missing degree8 places | R_h | Remaining C budget | Maximum number of high places | Cauchy lower bound on C_h |
|---|---:|---:|---:|---:|
| 0 | 27 | 316 | 2 | 27^2/2+27=783/2 |
| 1 | 35 | 388 | 3 | 35^2/3+35=1330/3 |

For positive high degrees f_i>=10 with sum R_h, their number is at most
floor(R_h/10), and sum f_i(f_i+1)>=R_h^2/count+R_h by Cauchy. Both lower
bounds exceed their C budgets. Hence the higher-depth case is impossible.

All surviving places must therefore have depth2 and nonrational support.
The frozen M2 all-degree obstruction excludes a strict improvement, and
the geometric M2 witness attains b. The maximum of this REFINED elementary
score is exactly b, with all degrees, all depths, rational support and t
included. No further search of that certified score is justified.

This also obstructs the original conservative score and the full-ray score
with the rank-based relation bound. It does not determine actual inertia
images, the true mean conductor, exact ray-class ranks, or actual tower ratios.
Those improvements and different bases lie outside this theorem.
