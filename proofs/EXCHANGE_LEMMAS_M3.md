# M3 exchange and optimization principles

Status: algebraic optimization principles; independent local laws PASS.
Final scope/exchange review is recorded in results/M3_FINAL_SCOPE_REVIEW.md.

## Odd-depth reduction for the conservative criterion

At characteristic2 and fixed place degree f, replace nu=2s+1 by2s. The
generator contribution f*(nu-1-floor((nu-1)/2)) remains f*s, the local
relation upper bound decreases and the full-local-quotient mean conductor
bound decreases. Availability, support and splitting count are unchanged.
The conservative score improves while GS admissibility is preserved.
This does not compare the exact inertia images of the two ray extensions.

## Split a deep conductor into shallow places, when available

Replace one place of degree f and depth2s by s distinct available places of
degree f and depth2. Keep T unchanged and disjoint. A remains f*s.

    C_old - C_new
      = f*(s-1)*(4*f*s-f+1) >= 0.

It is positive for s>1. The old conductor rebate is at most f/2^f; the new
rebate is s*f/2^f. Hence the genus cost decreases strictly for s>1 and GS
admissibility is preserved. This replacement requires actual spare places;
it is not valid merely because the degree exists in the inventory. The lemma
explains why depth is only potentially competitive when shallow stock runs out.

## Global deficit method when stocks run out

For nu=2s, compare C_P with lambda*A_P for a selected slope lambda. For
lambda=11 and the fixed k343 inventory, only degrees5,6,8 have negative
nonrational first-layer deficits, with total budget690. Rational places have
integer-depth deficit at most10 each. Thus C>=11*A-690-10*n.

Together with an upper bound for the conductor rebate, this gives a finite
necessary (n,A,t) problem before any degree/depth enumeration. See
M3_NONUNIFORM_OBSTRUCTION.md. This method can be reused with another slope
and another certified inventory, but its numerical constants are specific
to k343. No universality of the numerical bound is claimed.
