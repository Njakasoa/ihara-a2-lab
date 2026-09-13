# M2 frozen baseline for M3

Frozen before M3 experiments, 2026-09-13. Original scientific commit:
`28ea44a0fa0ff353f53cd410faa74ef8bb4048d6`. Public snapshot commit: `4ca760b24fc323cecd9242959937a668a27485d3`.

Exact bound: **A(2) >= 196608/620201**. Base: g(k)=343, N1(k)=192.
Support multiplicities (2,16,16,2,1), degrees (5,6,8,10,12), all conductors 2.
A=266, C=2260, D=75, I=41; splitting numerator 192;
genus denominator 620201/1024. Exact auxiliary ray degree and group structure
remain unknown. See certificates/m2-frozen.json for the frozen file hashes.

The uniform-conductor-two conservative score is already proved optimal on
this base with nonrational support, all degrees and 1<=t<=192. M3 must not
repeat that search. M3 comparisons use the exact fraction above.

## Hashes

- `proofs/IMPROVED_BOUND.md`: `b160daef63bc9c7dfcda1d746b2c4e8e8a82d97a1b4941bdf939a3bb298dc21d`
- `proofs/NU2_OBSTRUCTION.md`: `93a68d2e3998bd6cd9df8c6fe24bd9d202945a5daddf2f2759591f2f94b463e0`
- `proofs/CONDUCTOR_FILTRATION.md`: `c70ae51165cb01392e6e750c004ac8a8f095b52c6b6a424a2d74aa1432fb2226`
- `certificates/m2-tower.json`: `46b0438a4e29c725f724fbd56f7752e235c2ec86d3c097745ec0c2fd671848e7`
- `certificates/k343-zeta.json`: `ba6f37c928ec3e08e6eb105f5ea36d0f9984f3536dbe174b0553ea7fd6069ffc`
- `curves/k343-places.json`: `d8da6742ee578fa6d1480abd2675d82f267e2c958086ee685eefd8146102f14c`
- `curves/k343-degree12-places.json`: `e6d074f2db535d8a084b30aeec10bbf1c2605c4ab8838737e29a053339ad242a`
- `src/theorem_search.py`: `e5072322b97dc5110ceab6b61388774d33450735eff89df7219e9874fd30adce`
- `publication/main.tex`: `e1fd7f708206ec4e5d50800bb543163f2809b4438c133b80ff91130599ab5911`
- `publication/main.pdf`: `56119b83a13ecfa6f47352e870c9a74beba7e65042cfd70b05d84b24d028bed2`
