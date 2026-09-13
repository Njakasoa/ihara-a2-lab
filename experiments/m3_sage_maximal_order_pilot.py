#!/usr/bin/env python3
"""Historical nested Artin--Schreier capability pilot.

This source is retained to make the earlier capability observation
reproducible.  Run it only as an explicitly bounded external process:

    timeout 120s scripts/sage-python experiments/m3_sage_maximal_order_pilot.py

The five successive degree-two extensions build quickly, but the subsequent
K.maximal_order() call did not return during the 120-second observation.  The
production receipt in m3_ray_structure.py records this as historical evidence
and never invokes this script.
"""

from __future__ import annotations

import time

from sage.all import GF, FunctionField


started = time.time()
F2 = GF(2)
F0 = FunctionField(F2, "x")
x = F0.gen()
Y = F0["y"]
y = Y.gen()
H = F0.extension(y**2 + (x**3 + x + 1) * y + x**2 + x, "y")
xh = H(H.base_field().gen())
yh = H.gen()
bh = xh**2 + xh
c = xh**5 + xh**2 + 1

K = H
for index, h in enumerate((H(1), xh, xh**2, yh, yh**2)):
    R = K["z" + str(index)]
    z = R.gen()
    f = K(bh * h / (c * c))
    K = K.extension(z**2 + z - f, "w" + str(index))

print("K built", time.time() - started, flush=True)
print("max order...", flush=True)
O = K.maximal_order()
print("O", O, "time", time.time() - started, flush=True)
print("O basis len", len(O.basis()), "time", time.time() - started, flush=True)
print("places d1...", flush=True)
places = K.places(1)
print("len", len(places), time.time() - started, flush=True)
for place in places[:5]:
    print(place, flush=True)
