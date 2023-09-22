# author : Yeongsuk Oh


import maya.cmds as cmds


fbxJnt_list = ['Hips', 'Spine', 'Spine1', 'Spine2', 'Neck', 'Head', 'LeftShoulder', 'LeftArm', 'LeftForeArm',
               'LeftHand', 'LeftHandThumb1', 'LeftHandThumb2', 'LeftHandThumb3', 'LeftHandIndex1',
               'LeftHandIndex2', 'LeftHandIndex3', 'LeftHandMiddle1', 'LeftHandMiddle2', 'LeftHandMiddle3',
               'LeftHandRing1', 'LeftHandRing2', 'LeftHandRing3', 'LeftHandPinky1', 'LeftHandPinky2',
               'LeftHandPinky3', 'RightShoulder', 'RightArm', 'RightForeArm', 'RightHand', 'RightHandPinky1',
               'RightHandPinky2', 'RightHandPinky3', 'RightHandRing1', 'RightHandRing2', 'RightHandRing3',
               'RightHandMiddle1', 'RightHandMiddle2', 'RightHandMiddle3', 'RightHandIndex1', 'RightHandIndex2',
               'RightHandIndex3', 'RightHandThumb1', 'RightHandThumb2', 'RightHandThumb3', 'LeftUpLeg', 'LeftLeg',
               'LeftFoot', 'LeftToeBase', 'RightUpLeg', 'RightLeg', 'RightFoot', 'RightToeBase']


rigJnt_list = ['jnt_c_spine_main', 'jnt_c_spine_01', 'jnt_c_spine_02', 'jnt_c_neck', 'jnt_c_neck_01', 'jnt_c_head', 'jnt_l_clavicle', 'jnt_l_shoulder',
               'jnt_l_elbow', 'jnt_l_wrist', 'jnt_l_thumb_metacarpal', 'jnt_l_thumb_finger_00', 'jnt_l_thumb_finger_01', 'jnt_l_index_finger_00', 'jnt_l_index_finger_01',
               'jnt_l_index_finger_02', 'jnt_l_mid_finger_00', 'jnt_l_mid_finger_01', 'jnt_l_mid_finger_02', 'jnt_l_ring_finger_00', 'jnt_l_ring_finger_01', 'jnt_l_ring_finger_02',
               'jnt_l_pinky_finger_00', 'jnt_l_pinky_finger_01', 'jnt_l_pinky_finger_02', 'jnt_r_clavicle', 'jnt_r_shoulder', 'jnt_r_elbow', 'jnt_r_wrist',
               'jnt_r_pinky_finger_00', 'jnt_r_pinky_finger_01', 'jnt_r_pinky_finger_02', 'jnt_r_ring_finger_00', 'jnt_r_ring_finger_01', 'jnt_r_ring_finger_02', 'jnt_r_mid_finger_00',
               'jnt_r_mid_finger_01', 'jnt_r_mid_finger_02', 'jnt_r_index_finger_00', 'jnt_r_index_finger_01', 'jnt_r_index_finger_02', 'jnt_r_thumb_metacarpal',
               'jnt_r_thumb_finger_00', 'jnt_r_thumb_finger_01', 'jnt_l_thigh', 'jnt_l_knee', 'jnt_l_ankle', 'jnt_l_ball', 'jnt_r_thigh', 'jnt_r_knee',
               'jnt_r_ankle', 'jnt_r_ball']


"""
INSTRUCTION
'C:/Users/Yourim Kim/PycharmProjects/maya_utilities/'
import applyFBX
from importlib import reload
reload (applyFBX)
applyFBX.add_fbx_anim('FBX file')
"""


def add_fbx_anim(anim_name):
    """
    Test the joints placement for body and check the motion range as well
    Args:
        anim_name (string): FBX file name
    Return:
        (list) constraint_list : Easily access to the list that script made and manage to remove as well
    """
    constraint_list = list()
    for num in range(0, len(fbxJnt_list)):
        orient_const = cmds.orientConstraint(anim_name + '_' + fbxJnt_list[num], rigJnt_list[num], mo=True)
        constraint_list.append(orient_const)
    return constraint_list
