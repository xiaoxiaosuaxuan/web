import sys
from functools import partial
import trimesh
import ze
import yourdfpy

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
    #urdf_prefix = ze.args.prefix
    urdf_prefix = "3finger"
    #urdf_path = ze.args.path  # './assets/ur5/ur5.urdf'
    urdf_path = "assets/iiwa_3finger_description/urdf/iiwa_3finger_.urdf"
    joint_cfg = ze.args.joint_cfg.asPrim()
#    urdf_cfg = parse_cfg(urdf_prefix)
    mesh_dir = "assets/iiwa_3finger_description/meshes"
    urdf = yourdfpy.URDF.load(urdf_path, force_mesh=False, mesh_dir=mesh_dir)
    robot = urdf.robot
    links = robot.links

    urdf_cfg = joint_cfg.verts.joint_cfg.to_numpy()
    urdf_cfg = list(urdf_cfg + urdf.cfg)
    scene = urdf.scene
    urdf.update_cfg(urdf.cfg)
    link_transforms = {link.name: scene.graph.get(
        link.name)[0] for link in links}
    #zprint(link_transforms)
    for link in links:
        prim = ze.ZenoPrimitiveObject.new()

        prim.points.resize(4)
        prim.points.add_attr("transform", (float, 4))
        prim.points.transform.from_numpy(link_transforms[link.name])
        ze.rets[f'{urdf_prefix}_{link.name}'] = prim
        