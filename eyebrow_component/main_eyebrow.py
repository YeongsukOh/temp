# author : Yeongsuk Oh

import bezierCurve.bezierCurve_modified as bezier
import maya.cmds as cmds
import sys
from importlib import reload


def append_file_path():
    path = r'/home/users/yeongsuko/Desktop/jawComponent'

    if not path in sys.path:
        sys.path.append(path)
    else:
        pass

    # double check for file path
    for file_path in sys.path:
        print(file_path)


def create_guide(number=4):
    """
    :parameter number: the number of the guides
    :return: the list of guides to set up ctrls
    """
    guide_list = list()

    xVal = 0
    for index in range(number):
        loc = cmds.spaceLocator(n='loc_L_eyebrow_guide_{}'.format(index))[0]
        print(loc)
        cmds.setAttr(loc + '.tx', xVal)
        guide_list.append(loc)
        xVal += 1

    return guide_list


def create_control(items):
    """
    :parameter number: recieve the list of the guide of locators
    :return: the list of controls
    """
    ctrl_list = list()
    ctrl_grp_list = list()

    for guide in items:
        ctrl_name = guide.replace('loc', 'ctrl')
        position = cmds.xform(guide, q=True, ws=True, t=True)
        ctrl = cmds.circle(n=ctrl_name)[0]
        ctrl_grp = cmds.createNode('transform', n='grp_{}'.format(ctrl_name))
        cmds.parent(ctrl, ctrl_grp)
        cmds.setAttr(ctrl_grp + '.t', *position)
        ctrl_list.append(ctrl)
        ctrl_grp_list.append(ctrl_grp)

    # once the script has done, it needs to change to revert to code from the comment
    # cmds.delete(items)

    return ctrl_list, ctrl_grp_list


def create_joint(ctrl_list):
    """
    Create child joints based on the selected controllers
    :return: None
    """
    jnt_list = list()
    for ctrl in ctrl_list:
        jnt_name = ctrl.replace('ctrl', 'jnt')
        position = cmds.xform(ctrl, q=True, ws=True, t=True)
        jnt = cmds.createNode('joint', n=jnt_name)
        cmds.setAttr(jnt + '.t', *position)
        cmds.parent(jnt, ctrl)
        jnt_list.append()


###########
# EXAMPLE #
###########

# create curve based on the calculated point
def create_bezier_curve(number=10):
    curvePointList = list()
    controlPointList = list()
    for i in range(number + 1):
        ratio = i / number
        q1 = bezier.lerp(p1, p2, ratio)
        q2 = bezier.lerp(p2, p3, ratio)
        q3 = bezier.lerp(p3, p4, ratio)

        r1 = bezier.lerp(q1, q2, ratio)
        r2 = bezier.lerp(q2, q3, ratio)

        s1 = bezier.lerp(r1, r2, ratio)
        controlPointList.append(s1)
        data = cmds.getAttr(s1 + '.output3D')[0]
        curvePointList.append(data)

    # connect to points on the curve
    bezierCurveTRS = cmds.curve(n='bezier_curve', d=3, p=curvePointList)
    bezierShape = cmds.listRelatives(bezierCurveTRS, s=True)[0]

    # attaching the joint on the curve
    for a in range(len(controlPointList)):
        ratio = a / (len(controlPointList) - 1)
        cmds.connectAttr(controlPointList[a] + '.output3D', bezierShape + '.controlPoints[{}]'.format(a))
        pointOnCurveNode = cmds.createNode("pointOnCurveInfo")
        cmds.connectAttr(bezierShape + '.worldSpace', pointOnCurveNode + '.inputCurve')
        cmds.setAttr(pointOnCurveNode + '.turnOnPercentage', True)
        cmds.setAttr(pointOnCurveNode + '.parameter', ratio)
        jnt = cmds.createNode('joint')
        jnt_group = cmds.createNode('transform', n='grp_jnt_{}'.format(a))
        cmds.parent(jnt, jnt_group)
        cmds.connectAttr(pointOnCurveNode + '.position', jnt_group + '.t')


""" 
if __name__ == '__main__':
	append_file_path()
	create_bezier_curve(number = 14)

 """