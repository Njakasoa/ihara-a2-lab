# M3 bounded ray-class component receipt

This is a bounded exact component calculation for the M2 modulus on \(k_{343}\). It evaluates the selected support representatives in their certified finite residue fields, computes the principal-unit coordinates of explicit \(T\)-units, and records the resulting \(\mathbf F_2\)-linear relation space. It does not assert that these units exhaust the \(T\)-unit group.

The reproducible command is:

```sh
scripts/sage-python experiments/m3_ray_structure.py
```

The complete machine-readable receipt is [m3-ray-structure.json](m3-ray-structure.json). The following metadata describe the initial historical execution, not later
replays; current metadata and output hashes are in m3-reproduction.json and
m3-ray-structure.json. It was executed on 2026-09-13 at 12:38:58 UTC with SageMath 10.9, at commit `ad69023e028081a54980c18d8a9070ac11feb7c2`. The source hash is `c67381954bc8d2cc01142904b1bf1e074e84f4b872d1608ebb808f9329ea873b`; the output hash for that execution is `0958d95af56fb677763e2280429bc3a80f1e1756c8008acc2b3e8b84850e0ed3`. Input hashes are:

```text
certificates/m2-tower.json  46b0438a4e29c725f724fbd56f7752e235c2ec86d3c097745ec0c2fd671848e7
certificates/k343-zeta.json ba6f37c928ec3e08e6eb105f5ea36d0f9984f3536dbe174b0553ea7fd6069ffc
```

The full nested Artin–Schreier field was constructible as five successive degree-two extensions in a short historical pilot. Sage then entered `K.maximal_order()` and did not return during the bounded 120-second pilot; consequently no full \(k\)-class-group or Sage ray-class call is claimed. The exact source is [m3_sage_maximal_order_pilot.py](../experiments/m3_sage_maximal_order_pilot.py), invoked with `timeout 120s scripts/sage-python experiments/m3_sage_maximal_order_pilot.py`. The current receipt command does not rerun it. The timeout is recorded in the JSON receipt as `TIMEOUT_OBSERVED_HISTORICAL`.

## Exact local term

For every selected place \(P\) of degree \(f\), characteristic two gives

\[
 U_P^{(1)}/U_P^{(2)}\simeq (\kappa(P),+),
 \qquad \dim_{\mathbf F _2}=f,
 \qquad |U_P^{(1)}/U_P^{(2)}|=2^f.
\]

The 37 representatives were reconstructed from their modulus-bit encodings, their \(H\) and five Artin–Schreier equations were checked, and every Frobenius orbit had exactly the declared degree. The exact local direct-sum dimension is

\[
2\cdot5+16\cdot6+16\cdot8+2\cdot10+1\cdot12=266.
\]

The local-image data computed for the exhibited relation space are:

| selected support chart | degree | count | local dimension | projection rank of known relations | known \(R\cap V_P\) | inertia order upper bound | exact inertia |
|---|---:|---:|---:|---:|---:|---:|---|
| ramified \(k/H\) | 5 | 2 | 5 | 0 | 0 | \(2^5=32\) | unknown |
| regular, \(y-y(P)\) uniformizer | 6 | 16 | 6 | 3 | 0 | \(2^6=64\) | unknown |
| regular, \(x-x(P)\) uniformizer | 8 | 16 | 8 | 4 | 0 | \(2^8=256\) | unknown |
| regular, \(x-x(P)\) uniformizer | 10 | 2 | 10 | 5 | 0 | \(2^{10}=1024\) | unknown |
| regular, \(x-x(P)\) uniformizer | 12 | 1 | 12 | 5 | 0 | \(2^{12}=4096\) | unknown |

The degree-six rows are a useful chart check: there \(a=x^3+x+1=0\), so \(x-x(P)\) is not a uniformizer. Since \(F_x(P)=(x^2+1)y+1\ne0\), \(t=y-y(P)\) is a uniformizer and \(dx=0\) in the cotangent space. All 16 such rows were handled with that chart.

## Certified \(T\)-unit relations

The five base units used were

\[
 x,\quad x+1,\quad y,\quad y+1,\quad y+x.
\]

Their zeros and poles lie over the six rational places of \(H\), which split completely in \(k\). The norm identities checked algebraically are

\[
 N(y)=x(x+1),\qquad
 N(y+1)=x^2(x+1),\qquad
 N(y+x)=x^2(x+1)^2.
\]

For each \(h\in\{1,x,x^2,y,y^2\}\), let \(z_h^2+z_h=bh/c^2\) and

\[
 \eta_h=\frac{z_h}{z_h+1}.
\]

At regular support places the script checked the exact identity

\[
 \eta_h=\frac{z_h^2}{bh/c^2},
\]

so \([\eta_h]=[bh]\) in \(k^*/k^{*2}\). Thus these five Artin–Schreier ratios are \(T\)-units but add no square-class directions beyond the base \(T\)-units.

For \(a\ne0\), \(t=x-x(P)\) and

\[
 y'=\frac{(x^2+1)y+1}{a},\qquad
 \ell_P(g)=\frac{g'(P)}{g(P)},
\]

where \(\ell_P\) is the \(U_P^{(1)}/U_P^{(2)}\) coordinate after removing the odd-order residue. In particular,

\[
 \ell_P(\eta_h)=\frac{(bh/c^2)'(P)}{(bh/c^2)(P)}
 =\frac1b+\frac{h'}h,
\]

because \((c^2)'=0\) in characteristic two. For \(a=0\), the same calculation uses \(t=y-y(P)\), \(dx=0\), \(dy=1\). At the two degree-five ramified places, \(e(k/H)=32\); every listed base unit has expansion \(u_0+O(\tau^{32})\), and every \(\eta_h=1+O(\tau^{32})\), so all ten displayed local coordinates are exactly zero.

Packing all 10 rows into the 266-dimensional local direct sum and doing exact integer Gaussian elimination gives

\[
 \operatorname{rank}_{\mathbf F _2}(R_{\rm known})=5,
 \qquad
 R_{\rm known}=\langle x,x+1,y,y+1,y+x\rangle.
\]

For every one of the 37 individual local blocks \(V_P\), the calculation gives

\[
 \dim(R_{\rm known}\cap V_P)=0.
\]

This is a statement about the five displayed relations. It does not prove the corresponding intersection for the full, currently unknown, \(T\)-unit relation space.

## Ray and class-group status

The complete Jacobian order is available from the zeta certificate. Its exact 2-adic valuation is

\[
 v_2\bigl(|\operatorname{Pic}^0(k)(\mathbf F _2)|\bigr)=51.
\]

Its 2-primary rank and cyclic factors were not computed. The standard split ray exact sequence has a 266-dimensional local principal-unit term. Quotienting by the five exhibited independent \(T\)-unit relation rows leaves a known quotient dimension of 261. Therefore, under the standard exact-sequence identification, the displayed relations give the explicit component bound

\[
 v_2\!\left(|\operatorname{Cl}_{2S,T}(k)|\right)
 \le 51+(266-5)=312,
 \qquad |\operatorname{Cl}_{2S,T}(k)|_2\le 2^{312}.
\]

This is an upper bound from exhibited relations, with the exact-sequence convention and all additional \(T\)-unit relations still requiring a full proof. The exact split ray-class order, its 2-rank, and its cyclic decomposition remain **unknown**.

For a local block, the duality calculation would have the form

\[
 |I_P|=2^{f-\dim(R_{\rm all}\cap V_P)},
\]

when \(R_{\rm all}\) is the full principal \(T\)-unit relation space. The receipt only establishes \(R_{\rm known}\subseteq R_{\rm all}\) and zero single-block intersections for \(R_{\rm known}\). Consequently the rigorous current local statement remains \(1\le |I_P|\le2^f\), with the exact order unknown at every selected place. No strict improvement of the M2 mean-conductor bound follows from this bounded relation matrix.

The machine receipt marks the finite-field equations, Frobenius degrees, local derivative identities, rank-five relation result, and zero known single-block intersections as `PASS`; full ray group, full inertia orders, and exact conductor mean are marked `UNKNOWN`.

## Final archival capability repeat

The integrator repeated only the bounded capability observation to preserve
the original-output evidence missing from the first pilot. Sage10.9 again
built the nested field, entered `K.maximal_order()`, and reached the120-second
limit. The process was terminated and collected. Exact UTC, source commit,
software, runtime and raw output hashes are in [m3-sage-pilot.json](m3-sage-pilot.json).
This optional command is excluded from default M3 reproduction and establishes
no mathematical impossibility of computing the full group.
