import yourdfpy
import sys
from functools import partial
import trimesh
#from vedo import show

zprint = partial(print, file=sys.stderr)

if __name__ == '__main__':
    #urdf_prefix = ze.args.prefix
    urdf_prefix = "3finger"
    #urdf_path = ze.args.path # './assets/ur5/ur5.urdf'
    urdf_path = "assets/iiwa_3finger_description/urdf/iiwa_3finger_.urdf"
    mesh_dir = "assets/iiwa_3finger_description/meshes"
    urdf = yourdfpy.URDF.load(urdf_path, force_mesh=True, mesh_dir=mesh_dir)
    robot = urdf.robot
    links = robot.links
    joints = robot.joints
    actuated_joints = urdf.actuated_joints
    urdf.show()
    #zprint(f'[read_urdf] links: {[link.name for link in links]}')
    #zprint(f'[read_urdf] actuated_joints: {[j.name for j in actuated_joints]}')
    #zprint(len(actuated_joints))

    scene = urdf.scene
    link_mesh = {link.name: [] for link in links}
    for name in scene.graph.nodes_geometry:
        parent_name = scene.graph.transforms.parents[name]
        link_mesh[parent_name].append(scene.geometry[name])
    for link_name, geoms in link_mesh.items():
        result = trimesh.util.concatenate(geoms)
        if result == []:
            result = None
        link_mesh[link_name] = result

    # urdf.update_cfg({
    #     'shoulder_lift_joint': -2.0,
    #     'elbow_joint': 2.0
    # })
    link_transforms = {link.name: scene.graph.get(
        link.name)[0] for link in links}
    #zprint(link_transforms)
    # for link in links:
    #     mesh = link_mesh[link.name]
    #     if mesh:
    #         mesh.apply_transform(link_transforms[link.name])
    # show([mesh for _, mesh in link_mesh.items()])

    '''for link in links:
        prim = ze.ZenoPrimitiveObject.new()
        mesh = link_mesh[link.name]
        if not mesh:
            continue

        verts = mesh.vertices
        prim.verts.resize(verts.shape[0])
        prim.verts.pos.from_numpy(verts)
        tris = mesh.faces
        prim.tris.resize(tris.shape[0])
        prim.tris.pos.from_numpy(tris)
        prim.points.resize(4)
        prim.points.add_attr("transform", (float, 4))
        prim.points.transform.from_numpy(link_transforms[link.name])
        ze.rets[f'{urdf_prefix}_{link.name}'] = prim
    '''