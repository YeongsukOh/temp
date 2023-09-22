# author : yeongsuk

import maya.cmds as cmds
import os
import json

# creating rigMaster hierarchy
# file path for curve shape
filePath = '/home/users/yeongsuko/Desktop/yeongsukRigPractice/AL/src/curveShapes/curveShapeTest.json'

# here is the test constant to use
asset_name = 'test'
type_group = 'grp'
type_control = 'ctrl'
type_geometry = 'geo'
type_joint = 'jnt'
type_center = 'C'
type_left = 'L'
type_right = 'R'

# drawing the structure of cog sys
# .....
source_group_list = ['rig', 'bindings', 'geo']
component_list = ['control', 'guide', 'deform', 'input', 'output']

# rule of name convention as example
# .....

# creating the cog system
main_grp = cmds.createNode('transform', n = '{}_{}_base'.format(type_group, asset_name))

# before running the script, double check the folders are existed in the scene or not
# rig : controls, guide, deform(joint), input node, output node
# minor_group_list : ['grp_{}_rig', 'grp_{}_bindings', 'grp_{}_geo']

minor_group_list = list()
if asset_name.isidentifier():
	for grp in source_group_list:
		if cmds.objExists(grp):
			pass
		else:
			minor_group = cmds.createNode('transform', n = '{}_{}_{}'.format(type_group, asset_name, grp))
			minor_group_list.append(minor_group)
			cmds.parent(minor_group, main_grp)
else:
	raise Exception('{} is not valid for naming convention'.format(asset_name))

# assign to the specific named variable to use in further
rig_grp = minor_group_list[0]
binding_grp = minor_group_list[1]
geo_grp = minor_group_list[2]

# in single_component_list : ['grp_{}_rig_control', 'grp_{}_rig_guide', 'grp_{}_rig_deform', 'grp_{}_rig_input', 'grp_{}_rig_output']
single_component_list = list()
for component in component_list:
	data = cmds.createNode('transform', n = '{}_{}_rig_{}'.format(type_group, asset_name, component))
	cmds.parent(data, rig_grp)
	single_component_list.append(data)

comp_control_grp = single_component_list[0]
comp_guide_grp = single_component_list[1]
comp_deform_grp = single_component_list[2]
comp_input_grp = single_component_list[3]
comp_output_grp = single_component_list[4]

# checking os.path.exist for the filepath and if there is the filepath
# use the path to create curve

if os.path.exists(filePath):
	json_curve_data = open(filePath).read()
	json_dict_data = json.loads(json_curve_data)
	key = json_dict_data.keys()
	item_list = []
	for i in key:
		item_list.append(i)
		key = json_dict_data['{}'.format(i)].keys()
		for a in key:
			test = json_dict_data['{}'.format(i)]['{}'.format(a)]
			item_list.append(test)
else:
	raise Exception('{} is not valid path, check the path again'.format(filePath))

# assign to the variable to use for making the master
curve_name = item_list[0]
control_point = item_list[1]
knot = item_list[2]

# creating master curve
master_curve = cmds.curve(n = curve_name, p = control_point, k = knot)
grp_master_curve = cmds.createNode('transform', n = '{}_{}_{}'.format(type_group, type_control, curve_name))
cmds.parent(master_curve, grp_master_curve)
cmds.parent(grp_master_curve, comp_control_grp)

# create the offset ctrl
# ...

# create the attribute for global scale
# ...

# set the attributes to lock for the ctrl
# ...

# set the visibility

# creating joint
cog_jnt = cmds.createNode('joint', n = '{}_{}'.format(asset_name, type_joint))
grp_cog_jnt = cmds.createNode('transform', n = '{}_{}'.format(type_group, cog_jnt))
cmds.parent(cog_jnt, grp_cog_jnt)
cmds.parent(grp_cog_jnt, comp_deform_grp)