"""
    forwarding kinematics of articulated objects loaded from the input urdf file
"""
import yourdfpy
import sys
from functools import partial
import trimesh
import ze

zprint = partial(print, file=sys.stderr)

def parse_cfg(prefix):
    ret = dict()
    prefix_len = len(f'cfg_{prefix}_')
    for key in ze._args.keys():
        if key.startswith(f'cfg_{prefix}_'):
            ret[key[prefix_len:]] = ze.args[key] # should be float 
    return ret 

if __name__ == '__main__':
    # TODO: make it faster, do not use yourdfpy to compute link transformation 
    urdf_prefix = ze.args.prefix
    urdf_path = ze.args.path  # './assets/ur5/ur5.urdf'
    joint_cfg = ze.args.joint_cfg.asPrim()
    urdf_cfg = list(joint_cfg.verts.joint_cfg.to_numpy())
#    urdf_cfg = parse_cfg(urdf_prefix)
    mesh_dir = "./assets/MANO_urdf/meshes"
    urdf = yourdfpy.URDF.load(urdf_path, force_mesh=False, mesh_dir=mesh_dir)
    robot = urdf.robot
    links = robot.links

    scene = urdf.scene
    urdf.update_cfg(urdf_cfg)
    link_transforms = {link.name: scene.graph.get(
        link.name)[0] for link in links}

    for link in links:
        prim = ze.ZenoPrimitiveObject.new()

        prim.points.resize(4)
        prim.points.add_attr("transform", (float, 4))
        prim.points.transform.from_numpy(link_transforms[link.name])
        ze.rets[f'{urdf_prefix}_{link.name}'] = prim
