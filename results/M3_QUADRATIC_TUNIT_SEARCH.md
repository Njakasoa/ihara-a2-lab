# Quadratic subfield units for the M2 modulus

For the genus-343 field and the 37 places in [the M2 inventory](../certificates/m2-tower.json),
the [Sage search](../experiments/m3_quadratic_tunit_search.py) certifies **31 independent
relations** in the 266-dimensional binary jet space, including the five previously known.
Their span intersects each of the 37 individual blocks trivially.

## Producing the units

Put \(a=x^3+x+1,\ b=x^2+x,\ c=x^5+x^2+1\).
Write \(y^2+ay=b\). For each nonzero binary combination \(h\) of
\(1,x,x^2,y,y^2\), the corresponding intermediate field has
\(v_h=cw_h\) with \(v_h^2+cv_h=bh\).
The search tests \(g=A v_h+B\), where \(A\) runs over \(1,x,x+1,x(x+1)\)
and \(B=P+Qy\) with \(\deg P\le4,\ \deg Q\le2\), including zero polynomials.
There are \(31\cdot4\cdot32\cdot8=31{,}744\) recipes.

The norm to \(H\) equals \(A^2bh+AcB+B^2\). Express it as \(u+vy\).
The norm to \(\mathbf F_2(x)\) then equals \(u^2+auv+bv^2\).
Exactly **1,372 recipes** have this last norm of the form \(x^i(x+1)^j\).
These include conjugates and multiplicatively dependent units. The monic
equations for \(y,v_h\) imply integrality at every finite place. Consequently
the norm test rules out every finite zero away from \(x=0,1\). All points above
\(0,1,\infty\) belong to the splitting set \(T\), so the functions are \(T\)-units in \(k\).

In the [receipt](m3-quadratic-tunit-search.json), each accepted row contains
the mask for \(h\), binary polynomial encodings and both norm exponents.
The receipt lists the retained basis and its packed jets in inventory order,
low block first. In the first new row, \(g=v_1\) has absolute norm
\(b^2=x^2(x+1)^2\). The previously tested \(w_1/(w_1+1)\) has a different divisor.

## Rank and verification

On regular charts the parameter is \(x-x(P)\) when \(a(P)\ne0\) and
\(y-y(P)\) otherwise. Differentiate \(v_h^2+cv_h=bh\) to obtain
\(c\,dv_h=h\,db+b\,dh+v_h\,dc\).
The first jet of a unit is its logarithmic derivative in this parameter.
At each of the two totally ramified degree-five places, the ramification index
from any quadratic intermediate field to \(k\) is 16. Pullback therefore
kills the first jet. Indeed, over the common finite residue field, a unit
differs from its residue lift by an element of the intermediate maximal ideal.

The new independent rows have their iterated norms recomputed as
determinants of multiplication on \(1,y,v_h,yv_h\) over \(\mathbf F_2(x)\).
The packed binary elimination is checked against a Sage binary matrix containing
every certified jet. For each place \(P\) the difference between the rank and
the rank after erasing the \(P\)-block equals the single-block intersection
dimension. The resulting 37 zeros are statements about the computed span.

The new rank also bounds the order of the full 2-primary split ray group.
Before imposing splitting its order is \(2^{317}\). The splitting subgroup
contains the 31-dimensional relation space, hence the quotient has order
at most \(2^{317-31}=2^{286}\).
[Exact sequence and order formula](../proofs/M3_RAY_DUALITY.md)

## Why degree six requires an intermediate field of degree at least 16

The sixteen selected degree-six places are the complete fiber above one
degree-three place of \(H\). Fix one geometric representative of this base
place. The extension is unramified there, so its 32 geometric lifts are a
torsor for \(V=\mathrm{Gal}(k/H)\cong\mathbf F_2^5\). Frobenius cubed acts
on it by one nonzero translation, partitioning the lifts into the 16 pairs
corresponding to the closed places. Use the pullback of a common base
uniformizer \(y-y(P)\) to compare their jets. Within a pair the two jet
values are conjugate under the eighth-power map, so their vanishing agrees.

For a \(T\)-unit from a quadratic subfield, the function
\(s\mapsto(d\log g)(sP)\) on \(V\) depends on a single binary linear form
in \(s\). It is affine with values in \(\mathbf F_{64}\).
Products add these functions. A nonzero affine function on \(V\) vanishes
on at most 16 points, hence any nonzero restriction from such products
occupies at least **eight closed places**. The Sage receipt checks the affine
identities on the 32 lifts for all retained basis vectors.

More generally, a unit from a degree-\(2^r\) intermediate field yields
a function depending on \(r\) linear coordinates. Each binary component
is represented by a multilinear polynomial of degree at most \(r\).
The same holds after summing logarithmic jets from any number of
intermediate fields of degree \(\le 2^r\). A nonzero binary polynomial
function of degree \(\le r\) on \(\mathbf F_2^m\) has weight at least
\(2^{m-r}\) for \(0\le r\le m\). To see this, split on the last coordinate
as \(A+tB\). If \(B\ne0\), the two slices \(A,A+B\) have total weight at
least the weight of \(B\), whose degree is at most \(r-1\). If \(B=0\)
the slices are equal, doubling their common weight. Induction, with the
constant and full-degree cases immediate, gives the bound.

For \(m=5\), choose any nonzero binary component of the field-valued jet.
The whole jet is nonzero on at least \(2^{5-r}\) lifts, hence on at least
\(2^{4-r}\) closed places for \(r\le4\). In particular, **even arbitrary
products of units from quadratic, quartic and degree-eight intermediate
fields cannot isolate one degree-six place**. Degree 16 is the first
intermediate degree allowed by this fiber estimate alone. The
[full inertia proof](../proofs/M3_DEGREE6_INERTIA.md) uses the degree-eight
fiber and the ramified degree-five places to rule out isolation even for an
arbitrary \(T\)-unit of \(k\).

To recompute and check the full archived receipt, run at the repository root with SageMath 10.9

~~~sh
sage -python experiments/m3_quadratic_tunit_search.py
~~~

Use `--emit` for the complete JSON or `--check FILE` to verify a separate copy.
