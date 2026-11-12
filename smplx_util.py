import torch
import smplx
from smplx.joint_names import JOINT_NAMES

from scipy.spatial.transform import Rotation as R

#
# source venv/bin/activate
# exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
# exec(open('simplx_util.py').read())
#

_device_ = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def genModel(gender='neutral', flat_hand_mean=True, device=_device_):
    model = smplx.create(
        model_path='models',  # モデルファイルが置かれているディレクトリ
        model_type='smplx',   # 'smpl', 'smplh', 'smplx', 'mano', 'flame' から選択
        gender=gender,        # 'neutral', 'male', 'female'
        num_betas=10,             # 体型パラメータの次元
        num_expression_coeffs=10, # 表情パラメータの次元
        use_face_contour=False,
        use_pca=False,      # without hand-pca
        flat_hand_mean=flat_hand_mean,# default-pose: flat-hand
        ext='npz'                # 'npz' または 'pkl'
    ).to(device)
    return model

def genModels():
    global m_neutral_flat, m_neutral_mean, m_male_flat, m_male_mean, m_female_flat, m_female_mean
    m_neutral_flat = genModel(gender='neutral', flat_hand_mean=True)
    m_neutral_mean = genModel(gender='neutral', flat_hand_mean=False)
    m_male_flat = genModel(gender='male', flat_hand_mean=True)
    m_male_mean = genModel(gender='male', flat_hand_mean=False)
    m_female_flat = genModel(gender='female', flat_hand_mean=True)
    m_female_mean = genModel(gender='female', flat_hand_mean=False)

def genInitialJoints(model):
    batch_size = 1
    betas      = torch.zeros([batch_size, 10], device=device)    # 体型パラメータ
    body_pose  = torch.zeros([batch_size, 21, 3], device=device) # 身体の関節回転 (軸角表現)
    expression = torch.randn([batch_size, 10], device=device)    # 表情
    global_orient = torch.zeros([batch_size, 3], device=device) # 全体の向き
    transl        = torch.zeros([batch_size, 3], device=device) # 平行移動量
    output = model(
        betas=betas,
        body_pose=body_pose,
        expression=expression,
        global_orient=global_orient,
        transl=transl,
        return_full_pose=True, # full_pose
        return_verts=False,    # 頂点座標を計算するために True にする
    )
    return output.joints.detach().cpu().numpy().squeeze()

def genDefaultParameters(batch_size=1):
    global betas, expression, b_pose, g_rotation, g_translation, right_hand, left_hand
    betas      = torch.zeros([batch_size, 10], device=device)    # 体型パラメータ
    expression = torch.randn([batch_size, 10], device=device)    # 表情
    ##
    b_pose        = torch.zeros([batch_size, 21, 3], device=device) # 身体の関節回転 (軸角表現)
    g_rotation    = torch.zeros([batch_size, 3], device=device) # 全体の向き
    g_translation = torch.zeros([batch_size, 3], device=device) # 平行移動量
    #
    right_hand_pose = torch.zeros([batch_size, 15, 3], device=device) # 
    left_hand_pose  = torch.zeros([batch_size, 15, 3], device=device) # 

def getOutput(model, return_full_pose=True, return_verts=True):
    output = model(
        betas=betas,
        expression=expression,
        #
        body_pose=body_pose,
        global_orient=g_rotation,
        transl=g_translation,
        #
        right_hand_pose=right_hand_pose,
        left_hand_pose=left_hand_pose,
        return_full_pose=return_full_pose, # full_pose
        return_verts=return_verts,  # 頂点座標を計算するために True にする
    )
    return output

def makeBodyShape(model, output, **kwargs):
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    indices = model.faces.reshape(-1)
    return mkshapes.makeTriangles(vertices, indices)

def drawBodyShape(model, output, di, clear=True, **kwargs):
    res=makeBodyShape(model, output, **kwargs)
    if clear:
        di.clear()
    di.addObject(res)
    return res

def _setFullPose(robot, full_pose, st, ed, flush=False):
    for idx in range(st, ed):
        rot = R.from_rotvec(full_pose[idx])
        # 大文字 'XYZ' で直列関節（内因性回転）を指定
        theta_x, theta_y, theta_z = rot.as_euler("XYZ")
        base_i = 3*(idx - 1)
        robot.robot.joint(base_i + 0).q = theta_x
        robot.robot.joint(base_i + 1).q = theta_y
        robot.robot.joint(base_i + 2).q = theta_z
        if flush:
            robot.flush()

def setBodyAngles(robot, full_pose, flush=False):
    return _setFullPose(robot, full_pose, 1, 22, flush=flush)
def seRightHand(robot, full_pose, flush=False):
    return _setFullPose(robot, full_pose, 25, 40, flush=flush)
def setLeftHand(robot, full_pose, flush=False):
    return _setFullPose(robot, full_pose, 40, 55, flush=flush)

def _getAngles(robot, st, ed):
    res = np.zeros((ed - st, 3), dtype='float32')
    for idx in range(st, ed):
        base_i = idx*3
        angles = [robot.robot.joint(base_i+0).q,
                  robot.robot.joint(base_i+1).q,
                  robot.robot.joint(base_i+2).q ]
        rot = R.from_euler("XYZ", angles)
        res[idx-st, :] = rot.as_rotvec()
    return res

def getBodyAngles(robot):
    return _getAngles(robot, 0, 21)
def getRightHand(robot):
    return _getAngles(robot, 24, 39)
def getLeftHand(robot):
    return _getAngles(robot, 39, 54)
