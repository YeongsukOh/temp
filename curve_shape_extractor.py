# author : yeongsuk
import maya.cmds as cmds
import json
import os

# This is an example how to write the curveShape data into json file format
'''
import maya.cmds as cmds
import json

jsonData = json.dumps(curves)

curves = cmds.ls(os = True, fl = True)
nestedDic = dict()
for crv in curves:
    nestedDic[crv] = dict()
    nestedDic[crv]['name'] = 'yeongsuk'
    nestedDic[crv]['age'] = 35
    nestedDic[crv]['coutry'] = 'Canada'
'''

# actual code for the execution
curves = cmds.ls(os = True, fl = True)

tempList = list()
nestedDic = dict()
for crv in curves:
    nestedDic[crv] = dict()
    curveInfoNode = cmds.createNode( 'curveInfo' )
    tempList.append(curveInfoNode)
    cmds.connectAttr( crv + '.worldSpace', curveInfoNode + '.inputCurve' )
    knots = cmds.getAttr( curveInfoNode + '.knots[*]' )
    nestedDic[crv]['knot'] = knots
    controlPoints = cmds.getAttr( curveInfoNode + '.controlPoints[*]' )
    nestedDic[crv]['controlPoint'] = controlPoints

cmds.delete(tempList)

# convert to jsonData and organize the data as well
jsonData = json.dumps(nestedDic, sort_keys = True, indent = 4)

filePath = r'/home/users/yeongsuko/Desktop/yeongsukRigPractice/AL/src/curveShapes'
if os.path.exists(filePath) == False:
    json_data_read = open(filePath, 'w')
    json_data_read.write(jsonData)
    json_data_read.close()
else:
    json_data_read = open(filePath, 'w')
    json_data_read.write(jsonData)
    json_data_read.close()


jsonData = open(filePath).read()
jsonConverted = json.loads(jsonData)
curve_types = jsonConverted.keys()
datalist = list()
for curve_type in curve_types:
    curve_keys = jsonConverted['{}'.format(curve_type)].keys()
    for curve_key in curve_keys:
        keys = jsonConverted['{}'.format(curve_type)]['{}'.format(curve_key)]
        datalist.append(keys)

curve_points = datalist[0]
curve_knots = datalist[1]