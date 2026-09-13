# Proposed all-depth, rational-support obstruction for the fixed-base score

Status: independent arithmetic PASS and Astra mathematical ACCEPT.
The stronger refined obstruction is proved separately in M3_REFINED_OBSTRUCTION.md. This is an obstruction to the specified conservative Duursma–Mak
score, not to exact conductor averages or actual tower ratios.

Let k be the frozen genus-343 field, N=192 and b=196608/620201. Allow any
finite support, including rational places, any integer conductor bound nu>=2,
and any disjoint nonempty set of t rational splitting places. The available
nonrational degrees below10 are exactly B5=2, B6=16, B8=16; B2=B3=B4=B7=B9=0.
Use the existing sufficient criterion

    A=sum f*(nu-1-floor((nu-1)/2)),
    C=sum f*(nu-1)*(f*(nu-1)+1),
    t<=A, I=(1+A-t)^2-2C-4A>=0,

and the full-local-quotient conductor mean bound from M2.

## 1. Even-depth reduction and rebate

An odd nu=2s+1 can be replaced by 2s at the same place. A and availability
are unchanged, C and the conservative genus cost decrease, and the sufficient
criterion remains true. Thus a strict improvement would also exist with all
depths even. This only compares these theorem scores, not exact ray groups.

For nu=2s, put Q=2^f. Then A_P=f*s, C_P=f(2s-1)[f(2s-1)+1], and write the
place's genus contribution as A_P-r_f(s). The filtration formula gives

    r_f(s)= f/(2(Q-1)) * (1+(Q-2)*Q^(-(2s-1))).

Hence 0<r_f(s)<=f/Q. For f=1, r_1(s)=1/2 for every s>=1. Let n be the number
of rational places in S, so 0<=n<=191 and t<=192-n. The low nonrational
stocks contribute at most

    2*5/32 + 16*6/64 + 16*8/256 = 37/16.

All remaining degrees are >=10 and their rebates are at most A_P/1024.
Overcounting with all of A only weakens this estimate. Therefore

    R=sum r_f(s) <= n/2 + 37/16 + A/1024,
    cost=A-R >= L_n(A)=max(0,A-n/2-37/16-A/1024).

No finite bound on degree or depth has been assumed.

## 2. A global lower bound on relation cost

At a rational place,

    C_P-11*A_P=4s^2-13s >= -10  (integer s>=1).

For nonrational f, C_P-11*A_P increases with integer s>=1. At s=1 it equals
f(f-10), whose only negative available cases are f=5,6,8. Their total possible
deficit is

    2*25 + 16*24 + 16*16 = 690.

The increment from s to s+1 is f*(8*f*s-9)>0 for every available
nonrational f>=5. The rational quadratic attains its integer minimum -10
at s=2, which establishes the all-depth claims rather than a finite check.

For all f>=10 the contribution is nonnegative. Consequently

    C >= max(0,11*A-690-10*n).

The coefficient11 is chosen because first layers of degree10 attain C/A=11;
the finitely many smaller-degree stocks give an exact bounded deficit.

## 3. Necessary finite arithmetic problem

Any strict improvement t/(342+cost)>b must satisfy

    A < E_n = (269993/1024+37/16-n*(1/b-1/2))*1024/1023,

using t<=192-n. Thus the exact integer bound is A<=ceil(E_n)-1, while A>=n.
Also necessarily

    t >= t_min(n,A)=floor(b*(342+L_n(A)))+1.

Discard a pair when t_min>min(A,192-n). Otherwise D=1+A-t is positive and
the GS inequality implies

    C <= floor(((1+A-t_min)^2-4*A)/2).

The root's exact Fraction implementation over n=0,...,191 and
A=n,...,ceil(E_n)-1 leaves only

    n=0, A=266, t_min=192, C_min=2236, C_max=2280.

This small necessary-condition computation must be independently certified;
it is not a re-enumeration of the frozen nu2 supports. The inequalities
derive finite caps before a degree/depth cutoff, covering arbitrary support.
The production certificate in results/m3-obstruction.json records 9861 pairs:
7374 fail the splitting constraint and 2486 fail the relation bound, leaving
the displayed single pair. The runner is experiments/m3_obstruction.py.

## 4. Eliminate all higher depths

For the surviving n=0 case, write C>=11*A-690. Any available nonrational
place with s>=2 raises C-(11*A-690) by at least155: the smallest case is
f=5,s=2, where C_P-11*A_P=130, instead of the permitted low-stock deficit
-25. Thus its penalty is155. For f=6,8 the respective minimal penalties are
234 and440; for f>=10 the contribution itself is at least710. Missing cheap
places only increases the total deficit correction.

But the surviving interval leaves at most2280-2236=44. Hence every place
has s=1 and n=0. The independently accepted M2 all-degree nu2 obstruction
then excludes every strict improvement. Its known geometric witness attains b.

Subject to completing the independent finite check and review, the maximum
of this conservative score on this fixed base is therefore b even with
arbitrary nonuniform conductors, rational ramification and variable t.

## Scope of the conclusion

No exact ray inertia, extra class-group generator rank, stronger relation
estimate or additional splitting information is used. Those changes can
escape this obstruction. It is not a lower bound on actual conductor means,
not an upper bound on A(2), and not an obstruction for another base field.
