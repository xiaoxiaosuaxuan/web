import ze
import numpy as np

frame = ze.args.frame
joint_num = ze.args.joint_num 

joint_cfg = [0 for _ in range(joint_num)]
grab_joints = [2, 3, 6, 9, 12]  # the indexes of joints that grab the cloth


rate = 0.07
#frame = frame % 40
'''for i in grab_joints:
    if i == 0: 
        joint_cfg[i] = -frame * rate
    else:
        joint_cfg[i] = frame * rate'''
joint_cfg[9] = frame * rate 
#joint_cfg[1] = -frame * rate 
#joint_cfg[1] = -frame * rate / 3

joint_cfg = np.array(joint_cfg)
prim = ze.ZenoPrimitiveObject.new()
prim.verts.resize(joint_num)
prim.verts.add_attr('joint_cfg', (float, 1))
prim.verts.joint_cfg.from_numpy(joint_cfg)
ze.rets['joint_cfg'] = prim
