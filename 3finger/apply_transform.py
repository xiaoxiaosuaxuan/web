import ze 
import numpy as np

if __name__ == '__main__':
    ret_prim = ze.ZenoPrimitiveObject.new()
    ret_verts = []
    ret_verts_size = []
    verts_offset = 0
    ret_tris = []

    for key in ze._args.keys():
        prim = ze.args[key].asPrim()
        transform = prim.points.transform.to_numpy()
        verts = prim.verts.pos.to_numpy()
        ones = np.ones_like(verts[:, [0]])
        verts = (transform @ np.concatenate([verts, ones], axis=1).T)[:3, :].T
        ret_verts.append(verts)
        tris = prim.tris.pos.to_numpy() + verts_offset
        verts_offset += verts.shape[0]
        ret_tris.append(tris)



    ret_verts = np.concatenate(ret_verts, axis=0)
    ret_tris = np.concatenate(ret_tris, axis=0)
    zprint(ret_verts.shape)
    zprint(ret_tris.shape)
    ret_prim.verts.resize(ret_verts.shape[0])
    ret_prim.verts.pos.from_numpy(ret_verts)
    ret_prim.tris.resize(ret_tris.shape[0])
    ret_prim.tris.pos.from_numpy(ret_tris)
    ze.rets.obj0 = ret_prim

 