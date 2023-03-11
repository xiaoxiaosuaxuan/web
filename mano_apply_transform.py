import ze 
import numpy as np

if __name__ == '__main__':
    ret_prim = ze.ZenoPrimitiveObject.new()
    ret_verts = []
    ret_verts_size = []
    verts_offset = 0
    ret_tris = []
    thumb_verts = None         # by xuyuhang

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
        if key.endswith("m_avg_rmiddle2"):      # by xuyuhang
            thumb_verts = verts


    ret_verts = np.concatenate(ret_verts, axis=0)
    ret_tris = np.concatenate(ret_tris, axis=0)
    zprint(ret_verts.shape)
    zprint(ret_tris.shape)
    ret_prim.verts.resize(ret_verts.shape[0])
    ret_prim.verts.pos.from_numpy(ret_verts)
    ret_prim.tris.resize(ret_tris.shape[0])
    ret_prim.tris.pos.from_numpy(ret_tris)
    ze.rets.obj0 = ret_prim

    ###### by xuyuhang
    thumb_prim = ze.ZenoPrimitiveObject.new()
    #thumb_prim.verts.resize(thumb_verts.shape[0])
    #thumb_prim.verts.pos.from_numpy(thumb_verts)
    thumb_prim.verts.resize(4)
    thumb_prim
    index = [9, 12]
    for i in range(2):
        thumb_prim.verts.pos[i] = [thumb_verts[index[i]][j] for j in range(3)]
    ze.rets.obj1 = thumb_prim
    