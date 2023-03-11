import ze 
import numpy as np 
from functools import partial
import sys 

#zprint = partial(print, file=sys.stderr)
in_prim = ze.args.view_bc.asPrim()
prim = ze.ZenoPrimitiveObject.new()
prim.verts.resize(4)
for i in range(4):
    prim.verts.pos[i] = in_prim.verts.pos[i]

#zprint(f'prim.verts.pos[0]: {prim.verts.pos[0]}')

ze.rets.prim = prim