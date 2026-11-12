import pickle
import copy
import numpy as np

_template_ = {
    'node': None,
    'type': 'link',
    'joint': {
        'type': 'revolute',
        'id': None,
        'axis': None,
        'args': {'JointRange': [-PI, PI],
                 'JointVelocityRange': [-20.0, 20.0],
                 'JointEffortRange': [-100.0, 100.0]},
        'name': None },
    'translation': None,
    # 'rotation': None,
    'absolute': True
}

def _setValue(ldict, _name, _id, _jname, _axis, _pos):
    ldict['node'] = _name
    ldict['translation'] = _pos
    ldict['joint']['name'] = _jname
    ldict['joint']['axis'] = _axis
    ldict['joint']['id'] = _id

def makeJoint(name, id_base, pos):
    lx = copy.deepcopy(_template_)
    ly = copy.deepcopy(_template_)
    lz = copy.deepcopy(_template_)
    id_base * 3
    _setValue(lx, f'{name}',     id_base*3 - 3, f'j_{name}_x', np.array([1, 0, 0], dtype='float64'), pos)
    _setValue(ly, f'l_{name}_y', id_base*3 - 2, f'j_{name}_y', np.array([0, 1, 0], dtype='float64'), pos)
    _setValue(lz, f'l_{name}_z', id_base*3 - 1, f'j_{name}_z', np.array([0, 0, 1], dtype='float64'), pos)
    return lx, ly, lz

with open('default_joint_pos.pickle', 'rb') as f:
    joint_pos = pickle.load(f)

id_name_map = {
0: "pelvis",
#
1: "left_hip",
4: "left_knee",
7: "left_ankle",
10: "left_foot",
#
2: "right_hip",
5: "right_knee",
8: "right_ankle",
11: "right_foot",
#
3: "spine1",
6: "spine2",
9: "spine3",
#
12: "neck",
15: "head",
22: "jaw",
23: "left_eye_smplhf",
24: "right_eye_smplhf",
#
13: "left_collar",
16: "left_shoulder",
18: "left_elbow",
20: "left_wrist",
#
14: "right_collar",
17: "right_shoulder",
19: "right_elbow",
21: "right_wrist",
}
#>0 pelvis
#>1 left_hip
#>2 right_hip
#>3 spine1
#>4 left_knee
#>5 right_knee
#>6 spine2
#>7 left_ankle
#>8 right_ankle
#>9 spine3
#>10 left_foot
#>11 right_foot
#>12 neck
#>13 left_collar
#>14 right_collar
#>15 head
#>16 left_shoulder
#>17 right_shoulder
#>18 left_elbow
#>19 right_elbow
#>20 left_wrist
#>21 right_wrist
#>22 jaw
#>23 left_eye_smplhf
#>24 right_eye_smplhf
name_id_map = {}
for k,v in id_name_map.items():
    name_id_map[v] = k

pelvis = [
    { 'node': 'pelvis',
      'type': 'link',
      'translation': joint_pos[0],
      'joint': {
          'type': 'root',
      },
      # 'rotation': None,
      'absolute': True
      }
    ]

lleg = []
lleg.extend( makeJoint('left_hip',   1, joint_pos[ 1]) )
lleg.extend( makeJoint('left_knee',  4, joint_pos[ 4]) )
lleg.extend( makeJoint('left_ankle', 7, joint_pos[ 7]) )
lleg.append(
    {'node': 'left_foot_plate', 'type': 'geom',
     'geometry': {'primitive': 'box', 'args': {'x': 0.07, 'y': 0.02, 'z': 0.17, 'color': [0.4, 0.4, 0]}},
     'relative': True, 'translation': [0.0473-0.005, -0.068, 0.0332] }) # 0., ??, 0.1182 - 0.17/2
lleg.extend( makeJoint('left_foot', 10, joint_pos[10]) )
lleg.append(
    {'node': 'left_foot_toe', 'type': 'geom',
     'geometry': {'primitive': 'box', 'args': {'x': 0.09, 'y': 0.02, 'z': 0.06, 'color': [0.4, 0.4, 0]}},
     'relative': True, 'translation': [-0.005, -0.01, 0.03] })

rleg = []
rleg.extend( makeJoint('right_hip',   2, joint_pos[ 2]) )
rleg.extend( makeJoint('right_knee',  5, joint_pos[ 5]) )
rleg.extend( makeJoint('right_ankle', 8, joint_pos[ 8]) )
rleg.append(
    {'node': 'right_foot_plate', 'type': 'geom',
     'geometry': {'primitive': 'box', 'args': {'x': 0.07, 'y': 0.02, 'z': 0.17, 'color': [0.4, 0.4, 0]}},
     'relative': True, 'translation': [-0.03883+0.005 + 0.005, -0.068, 0.0332] }) # 0., ??, 0.1182 - 0.17/2
rleg.extend( makeJoint('right_foot', 11, joint_pos[11]) )
rleg.append(
    {'node': 'right_foot_toe', 'type': 'geom',
     'geometry': {'primitive': 'box', 'args': {'x': 0.09, 'y': 0.02, 'z': 0.06, 'color': [0.4, 0.4, 0]}},
     'relative': True, 'translation': [ 0.01, -0.01, 0.03] })

torso = []
torso.extend( makeJoint('spine1', 3, joint_pos[3]) )
torso.extend( makeJoint('spine2', 6, joint_pos[6]) )
torso.extend( makeJoint('spine3', 9, joint_pos[9]) )

neck = []
neck.extend( makeJoint("neck", 12, joint_pos[12]) )
neck.extend( makeJoint("head", 15, joint_pos[15]) )
neck.append( list(makeJoint("jaw",  22, joint_pos[22])) )# TODO tip geom
neck.append( list(makeJoint("left_eye_smplhf",  23, joint_pos[23])) )# TODO tip geom
neck.append( list(makeJoint("right_eye_smplhf", 24, joint_pos[24])) )# TODO tip geom

larm = []
larm.extend( makeJoint( "left_collar",  13, joint_pos[13]) )
larm.extend( makeJoint( "left_shoulder",16, joint_pos[16]) )
larm.extend( makeJoint( "left_elbow",   18, joint_pos[18]) )
larm.extend( makeJoint( "left_wrist",   20, joint_pos[20]) )

rarm = []
rarm.extend( makeJoint( "right_collar",  14, joint_pos[14]) )
rarm.extend( makeJoint( "right_shoulder",17, joint_pos[17]) )
rarm.extend( makeJoint( "right_elbow",   19, joint_pos[19]) )
rarm.extend( makeJoint( "right_wrist",   21, joint_pos[21]) )

lst = [
    *pelvis, ## root geom?
    [*lleg],
    [*rleg],
    [*torso,
     [*neck],
#>     [*rarm,
#>       [*rhand]],
#>     [*larm,
#>      [*lhand]],
     [*larm],
     [*rarm],
     #[*larm, larm_tip], # TODO tip geom
     #[*rarm, rarm_tip], # TODO tip geom
     ]
]

with open('smplx_body_lst.pickle', 'wb') as f:
    pickle.dump(lst, f)

l_hand = []
l_index = []
l_index.extend( makeJoint( 'left_index1', 25, joint_pos[25]))
l_index.extend( makeJoint( 'left_index2', 26, joint_pos[26]))
l_index.extend( makeJoint( 'left_index3', 27, joint_pos[27]))
l_index.append(
    {'node': 'left_index_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[27]-joint_pos[26] } )
l_middle = []
l_middle.extend( makeJoint( 'left_middle1',28, joint_pos[28]))
l_middle.extend( makeJoint( 'left_middle2',29, joint_pos[29]))
l_middle.extend( makeJoint( 'left_middle3',30, joint_pos[30]))
l_middle.append(
    {'node': 'left_middle_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[30]-joint_pos[29] } )
l_pinky = []
l_pinky.extend( makeJoint( 'left_pinky1', 31, joint_pos[31]))
l_pinky.extend( makeJoint( 'left_pinky2', 32, joint_pos[32]))
l_pinky.extend( makeJoint( 'left_pinky3', 33, joint_pos[33]))
l_pinky.append(
    {'node': 'left_pinky_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[33]-joint_pos[32] } )
l_ring = []
l_ring.extend( makeJoint( 'left_ring1',  34, joint_pos[34]))
l_ring.extend( makeJoint( 'left_ring2',  35, joint_pos[35]))
l_ring.extend( makeJoint( 'left_ring3',  36, joint_pos[36]))
l_ring.append(
    {'node': 'left_ring_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[36]-joint_pos[35] } )
l_thumb = []
l_thumb.extend( makeJoint( 'left_thumb1', 37, joint_pos[37]))
l_thumb.extend( makeJoint( 'left_thumb2', 38, joint_pos[38]))
l_thumb.extend( makeJoint( 'left_thumb3', 39, joint_pos[39]))
l_thumb.append(
    {'node': 'left_thumb_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[39]-joint_pos[38] } )
l_hand.append(l_index)
l_hand.append(l_middle)
l_hand.append(l_pinky)
l_hand.append(l_ring)
l_hand.append(l_thumb)

r_hand = []
r_index = []
r_index.extend( makeJoint( 'right_index1', 40, joint_pos[40]))
r_index.extend( makeJoint( 'right_index2', 41, joint_pos[41]))
r_index.extend( makeJoint( 'right_index3', 42, joint_pos[42]))
r_index.append(
    {'node': 'right_index_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[42]-joint_pos[41] } )
r_middle = []
r_middle.extend( makeJoint( 'right_middle1',43, joint_pos[43]))
r_middle.extend( makeJoint( 'right_middle2',44, joint_pos[44]))
r_middle.extend( makeJoint( 'right_middle3',45, joint_pos[45]))
r_middle.append(
    {'node': 'right_middle_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[45]-joint_pos[44] } )
r_pinky = []
r_pinky.extend( makeJoint( 'right_pinky1', 46, joint_pos[46]))
r_pinky.extend( makeJoint( 'right_pinky2', 47, joint_pos[47]))
r_pinky.extend( makeJoint( 'right_pinky3', 48, joint_pos[48]))
r_pinky.append(
    {'node': 'right_pinky_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[48]-joint_pos[47] } )
r_ring = []
r_ring.extend( makeJoint( 'right_ring1',  49, joint_pos[49]))
r_ring.extend( makeJoint( 'right_ring2',  50, joint_pos[50]))
r_ring.extend( makeJoint( 'right_ring3',  51, joint_pos[51]))
r_ring.append(
    {'node': 'right_ring_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[51]-joint_pos[50] } )
r_thumb = []
r_thumb.extend( makeJoint( 'right_thumb1', 52, joint_pos[52]))
r_thumb.extend( makeJoint( 'right_thumb2', 53, joint_pos[53]))
r_thumb.extend( makeJoint( 'right_thumb3', 54, joint_pos[54]))
r_thumb.append(
    {'node': 'right_thumb_tip', 'type': 'geom',
     'geometry': {'primitive': 'sphere', 'args': {'radius': 0.007, 'color': [0.4, 0.4, 0]}},
     'translation': 2*joint_pos[54]-joint_pos[53] } )

r_hand.append(r_index)
r_hand.append(r_middle)
r_hand.append(r_pinky)
r_hand.append(r_ring)
r_hand.append(r_thumb)

lst_hand = [
    *pelvis,
    [*lleg],
    [*rleg],
    [*torso,
     [*neck],
     [*larm,
      [*l_hand]],
     [*rarm,
      [*r_hand]],
     ]
]

with open('smplx_body_lst_hand.pickle', 'wb') as f:
    pickle.dump(lst_hand, f)

### generate
import irsl_cnoid.robot_graph.robot_graph as mrg
import pickle
with open('smplx_body_lst.pickle', 'rb') as f:
    lst = pickle.load(f)
with open('smplx_body_lst_hand.pickle', 'rb') as f:
    lst_hand = pickle.load(f)
## gen
#gg = mrg.RobotTree.generate_from_list(lst, add_root=False)
gg = mrg.RobotTree.generate_from_list(lst_hand, add_root=False)
gg.update_coords()
#gg.add_geometries_for_joints(scale=0.14)
#gg.add_geometries_for_links(scale=0.16)

node_set = set( gg.nodes )
small_set = set([ 'jaw', 'l_jaw_y', 'l_jaw_z', 'left_eye_smplhf', 'l_left_eye_smplhf_y',  'l_left_eye_smplhf_z',  'right_eye_smplhf',  'l_right_eye_smplhf_y',  'l_right_eye_smplhf_z' ])
_tmp = []
for lr in ['left', 'right']:
    for nm in ['index', 'middle', 'pinky', 'ring', 'thumb']:
        for idx in range(1,4):
            for jt in ['', '_y', '_z']:
                if len(jt) > 0:
                    _tmp.append(f'l_{lr}_{nm}{idx}{jt}')
                else:
                    _tmp.append(f'{lr}_{nm}{idx}')
hand_set = set(_tmp)
res = node_set.difference(small_set.union(hand_set))

#gg.add_geometries_for_joints(scale=0.04)
#gg.add_geometries_for_links(scale=0.06)
gg.add_geometries_for_joints(scale=0.14, white_list=list(res))
gg.add_geometries_for_links(scale=0.16, white_list=list(res))

rtb = mrg.RobotTreeBuilder(); rtb.buildRobotFromTree(gg)

obj=mkshapes.loadMesh('human_model.obj')

cds=mkshapes.makeCoords(length=0.1, lineWidth=4)

### simple
if True:
    lst_hand = [
        *pelvis,
        [*lleg],
        [*rleg],
        [*torso,
         [*neck],
         [*larm,
          [*l_hand]],
         [*rarm,
          [*r_hand]],
         ]
    ]
    gg = mrg.RobotTree.generate_from_list(lst_hand, add_root=False)
    gg.update_coords()
    gg.add_geometries_for_joints(scale=0.04)
    gg.add_geometries_for_links(scale=0.06)
    rtb = mrg.RobotTreeBuilder()
    rtb.buildRobotFromTree(gg)

###
if True:
    gg = mrg.RobotTree.generate_from_list(lst_hand, add_root=False)
    gg.update_coords()
    ##
    node_set = set( gg.nodes )
    small_set = set([ 'jaw', 'l_jaw_y', 'l_jaw_z', 'left_eye_smplhf', 'l_left_eye_smplhf_y',  'l_left_eye_smplhf_z',  'right_eye_smplhf',  'l_right_eye_smplhf_y',  'l_right_eye_smplhf_z' ])
    _tmp = []
    for nm in ('left_wrist', 'right_wrist', 'left_foot', 'right_foot'):
        for jt in ['', '_y', '_z']:
            if len(jt) > 0:
                _tmp.append(f'l_{nm}{jt}')
            else:
                _tmp.append(f'{nm}')
    for lr in ['left', 'right']:
        for nm in ['index', 'middle', 'pinky', 'ring', 'thumb']:
            for idx in range(1,4):
                for jt in ['', '_y', '_z']:
                    if len(jt) > 0:
                        _tmp.append(f'l_{lr}_{nm}{idx}{jt}')
                    else:
                        _tmp.append(f'{lr}_{nm}{idx}')
    hand_set = set(_tmp)
    small_set = small_set.union(hand_set)
    res = node_set.difference(small_set)
    ##
    gg.add_geometries_for_joints(scale=0.14, white_list=list(res))
    gg.add_geometries_for_links(scale=0.16,  white_list=list(res))
    gg.add_geometries_for_joints(scale=0.04, white_list=list(small_set))
    gg.add_geometries_for_links(scale=0.06, white_list=list(small_set))
    rtb = mrg.RobotTreeBuilder()
    rtb.buildRobotFromTree(gg)
    ##
    rtb.exportBody('human_model_neutral_w_flat_hand.body', 'human_model_neutral_w_flat_hand')
