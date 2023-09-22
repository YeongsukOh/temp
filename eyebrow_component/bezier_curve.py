# author: Yeongsuk Oh


import maya.cmds as cmds


def typeTest(node):
    '''

    :node: String
    :return: String : node type
    '''
    return (cmds.nodeType(node))


def getNode(node):
    '''

    :node: String
    :return: String : node name
    '''
    return (node)


def lerp(point1, point2, ratio=0.5):
    '''
    # using the linear interpolation formula
    # (p2 - p1)*ratio + p1 : currently using this one
    # p(t) = (1 - t)*p1 + p2
    :point1: String
    :point2: String
    :ratio: Float
    :return: String : totalLengthNode
    '''
    distanceNode = cmds.createNode("plusMinusAverage")
    cmds.setAttr(distanceNode + ".operation", 2)
    multiplyDivideNode = cmds.createNode("multiplyDivide")
    totalLengthNode = cmds.createNode("plusMinusAverage")
    cmds.setAttr(totalLengthNode + ".operation", 1)

    if 'transform' in typeTest(point1) and typeTest(point2):
        p1_decompose = cmds.createNode('decomposeMatrix', n="{}_decomposeMatrix".format(point1))
        p2_decompose = cmds.createNode('decomposeMatrix', n="{}_decomposeMatrix".format(point2))
        cmds.connectAttr(point1 + ".worldMatrix[0]", p1_decompose + '.inputMatrix')
        cmds.connectAttr(point2 + ".worldMatrix[0]", p2_decompose + '.inputMatrix')

        cmds.connectAttr(p1_decompose + '.outputTranslate', distanceNode + '.input3D[1]')
        cmds.connectAttr(p2_decompose + '.outputTranslate', distanceNode + '.input3D[0]')

        cmds.connectAttr(distanceNode + ".output3D", multiplyDivideNode + ".input1")
        for i in ["input2X", "input2Y", "input2Z"]:
            cmds.setAttr(multiplyDivideNode + ".{}".format(i), ratio)

        cmds.connectAttr(multiplyDivideNode + '.output', totalLengthNode + '.input3D[0]')
        cmds.connectAttr(p1_decompose + '.outputTranslate', totalLengthNode + '.input3D[1]')

    elif 'plusMinusAverage' in typeTest(point1) and typeTest(point2):
        cmds.connectAttr(getNode(point1) + '.output3D', distanceNode + '.input3D[1]')
        cmds.connectAttr(getNode(point2) + '.output3D', distanceNode + '.input3D[0]')

        cmds.connectAttr(distanceNode + ".output3D", multiplyDivideNode + ".input1")
        for i in ["input2X", "input2Y", "input2Z"]:
            cmds.setAttr(multiplyDivideNode + ".{}".format(i), ratio)

        cmds.connectAttr(multiplyDivideNode + '.output', totalLengthNode + '.input3D[0]')
        cmds.connectAttr(getNode(point1) + '.output3D', totalLengthNode + '.input3D[1]')

    return totalLengthNode


def guideLine(*args):
    '''

    :args: point of locators
    :return: N/A
    '''
    pointList = list()
    for position in args:
        point = cmds.xform(position, q=True, ws=True, t=True)
        pointList.append(point)
    curveTransform = cmds.curve(n='TEST_CURVE', d=3, p=pointList)
    curveShape = cmds.listRelatives(curveTransform, s=True)[0]
    for index in range(len(args)):
        decompM = cmds.createNode('decomposeMatrix', n="{}_decompNode".format(args[index]))
        cmds.connectAttr(args[index] + '.worldMatrix[0]', decompM + '.inputMatrix')
        cmds.connectAttr(decompM + '.outputTranslate', curveShape + '.controlPoints[{}]'.format(index))


def createLine(*args):
    pass


'''
###########
# EXAMPLE #
###########

# create curve based on the calculated point
count = 10
curvePointList = list()
controlPointList = list()
for i in range(count+1):
    ratio = i/count
    q1 = lerp(p1, p2, ratio)
    q2 = lerp(p2, p3, ratio)
    q3 = lerp(p3, p4, ratio)

    r1 = lerp(q1, q2, ratio)
    r2 = lerp(q2, q3, ratio)

    s1 = lerp(r1, r2, ratio)
    controlPointList.append(s1)
    data = cmds.getAttr(s1 + '.output3D')[0]
    curvePointList.append(data)


# connect to points on the curve
bezierCurveTRS = cmds.curve(n = 'bezier_curve', d=3, p = curvePointList)
bezierShape = cmds.listRelatives(bezierCurveTRS, s = True)[0]


# attaching the joint on the curve
for a in range(len(controlPointList)):
	ratio = a/(len(controlPointList)-1)
	cmds.connectAttr(controlPointList[a] + '.output3D', bezierShape + '.controlPoints[{}]'.format(a))
	pointOnCurveNode = cmds.createNode("pointOnCurveInfo")
	cmds.connectAttr(bezierShape + '.worldSpace', pointOnCurveNode + '.inputCurve')
	cmds.setAttr(pointOnCurveNode + '.turnOnPercentage', True)
	cmds.setAttr(pointOnCurveNode + '.parameter', ratio)
	jnt = cmds.createNode('joint')
	cmds.connectAttr(pointOnCurveNode + '.position', jnt + '.t')



# creating the matrix which is aiming to next joint
joints = cmds.ls(sl = True)
len(joints)
for jnt in joints:
	blendMatrix = cmds.createNode("blendMatrix", n = "{}_blendMatrix".format(jnt))
	cmds.connectAttr("p1_fourByFourMatrix.output", blendMatrix +'.inputMatrix')
	cmds.connectAttr("p2_fourByFourMatrix.output", blendMatrix +'.target[0].targetMatrix')
	decompNode = cmds.createNode("decomposeMatrix", n = "{}_decompMatrix".format(jnt))
	cmds.connectAttr(blendMatrix + '.outputMatrix', decompNode + '.inputMatrix')
	cmds.connectAttr(decompNode + '.outputRotate', jnt + '.rotate')
	cmds.setAttr(blendMatrix + '.envelope', 0)
'''