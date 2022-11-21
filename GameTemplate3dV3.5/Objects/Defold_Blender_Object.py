# See https://docs.blender.org/api/blender_python_api_2_78_0/info_tutorial_addon.html for more info

bl_info = {
	"name": "Defold Mesh (.go)",
	"author": "",
	"version": (1, 0),
	"blender": (2, 80, 0),
	"location": "File > Export > Defold Mesh (.go)",
	"description": "Defold Mesh (.go)",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"
}

import bpy , os
from bpy_extras.io_utils import ExportHelper, orientation_helper
from bpy.props import (
	StringProperty,
	BoolProperty,
	CollectionProperty,
	EnumProperty,
	FloatProperty,
	IntProperty,
)

import json
from collections import OrderedDict

def make_stream(name, component_count, data, typ="float32"):

	return OrderedDict([('name', name),
						('type', typ),
						('count', component_count),
						('data', data)
						])

def export_mesh(mesh):
	mesh.calc_loop_triangles()
	mesh.calc_normals_split()
	#mesh.calc_tangents()
	mesh_materials = mesh.materials
	mesh_loops = mesh.loops
	mesh_vertices = mesh.vertices
	mesh_uv_layers = mesh.uv_layers
	mesh_color_layers = mesh.vertex_colors

	position_values = []
	normal_values = []
	tangent_values = []
	bitangent_values = []
	bitangent_sign_values = []
	uv_values_by_layer = [[]] * len(mesh_uv_layers)
	color_values_by_layer = [[]] * len(mesh_color_layers)

	# https://docs.blender.org/api/current/bpy.types.MeshLoopTriangle.html#bpy.types.MeshLoopTriangle
	for triangle in mesh.loop_triangles:
		material_index = triangle.material_index
		use_smooth = triangle.use_smooth

		for triangle_vertex_index, mesh_vertex_index in enumerate(triangle.vertices):
			mesh_loop = mesh_loops[triangle.loops[triangle_vertex_index]]
			mesh_vertex = mesh_vertices[mesh_vertex_index]

			position = mesh_vertex.co.to_tuple()
			normal = (mesh_vertex.normal if use_smooth else triangle.normal).to_tuple()
			tangent = mesh_loop.tangent.to_tuple()
			bitangent = mesh_loop.bitangent.to_tuple()
			bitangent_sign = mesh_loop.bitangent_sign

			position_values.extend(position)
			normal_values.extend(normal)
			tangent_values.extend(tangent)
			bitangent_values.extend(bitangent)
			bitangent_sign_values.append(bitangent_sign)

		for loop_index in triangle.loops:

			for mesh_uv_layer_index, mesh_uv_layer in enumerate(mesh_uv_layers):
				uv = mesh_uv_layer.data[loop_index].uv
				uv_values_by_layer[mesh_uv_layer_index].extend(uv)

			for mesh_color_layer_index, mesh_color_layer in enumerate(mesh_color_layers):
				color = mesh_color_layer.data[loop_index].color
				color_values_by_layer[mesh_color_layer_index].extend(color)

	streams = [
		make_stream("position", 3, position_values),
		make_stream("normal", 3, normal_values)
	]

	streams.extend(map(lambda mesh_uv_layer, uv_values: make_stream("texcoord0", 2, uv_values), mesh_uv_layers, uv_values_by_layer))
	streams.append({'name':"color0" , "type":"float32","count":4,"data":[1.0 for i in range(4*int(len(streams[0]['data'])/3.0))]})
	return streams

def Export_Mesh_File(file_mesh_path) : 
	with open(file_mesh_path,"w") as msh : 
		msh.write(f"material:\"/Matrials/BaseTexture.material\"\n")
		folder_name = os.path.split(os.path.split(file_mesh_path)[0])[-1]
		msh.write(f"vertices:\"/Objects/{folder_name}/{folder_name}.buffer\"\n")
		msh.write(f"textures:\"/Objects/{folder_name}/{folder_name}.png\"\n")
		msh.write(f"primitive_type:PRIMITIVE_TRIANGLES\n")        
		msh.write('position_stream:"position"\n')     
		msh.write('normal_stream:"normal"\n')    


def export_to_file(f, indent=0):
	obj = bpy.context.active_object

	# if we don't exit edit mode, the (uv) layers will be empty!
	is_editmode = (obj.mode == 'EDIT')
	if is_editmode:
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

	mesh = obj.data

	streams = export_mesh(mesh)
	s = json.dumps(streams, separators=(',', ':'), indent=indent if indent > 0 else None)
	f.write(bytearray(s, 'utf-8'))
	###### save image texture 
	texture_list = list()
	images_names = list()
	Image_Bpy_Object_used = None
	for s in obj.material_slots:
		if s.material and s.material.use_nodes:
			for n in s.material.node_tree.nodes:
				if n.type == 'TEX_IMAGE':
					texture_list += [n.image]
					print(obj.name,'uses',n.image.name,'saved at',n.image.filepath)
					images_names.append(n.image.filepath)
					Image_Bpy_Object_used = n.image

	assert len(set(images_names)) == 1 , "[[[[[[[[[[Issam say : Object must have only one texture !!!!!!]]]]]]]]]]"
	image_path = list(set(images_names))[0]
	Image_Bpy_Object_used.save_render(filepath=f.name.replace(".buffer",".png"))
	###### save mesh file  : 
	Export_Mesh_File(f.name.replace(".buffer",".mesh"))



def Export_In_Folder(filepath,indent) : 
	if os.path.exists(filepath) : 
		if os.path.isdir(filepath):
			pass
		else : 
			os.mkdir(filepath)
	else : 
		os.mkdir(filepath)
	dir_name = os.path.split(filepath)[-1]
	with open(os.path.join(filepath,dir_name + ".buffer"),"wb") as goo : 
		export_to_file(goo, indent=indent)

 

# The main exporter class.
@orientation_helper(axis_forward='-Z', axis_up='Y')
class DefoldExporter(bpy.types.Operator, ExportHelper):
	bl_idname       = "export_mesh.defold_exporter"
	bl_label        = "Export"
	bl_description  = "Export Defold mesh data V2 "

	filename_ext    = ""
	filter_glob: StringProperty(default="*(/)", options={'HIDDEN'}) #*(/)

	use_selection: BoolProperty(
		name="Selection Only",
		description="Export selected objects only",
		default=False,
	)

	indent: IntProperty(
		name="Indent",
		min=0, max=8,
		default=0,
	)

	def execute(self, context):
		print("........................................................................................")
		Export_In_Folder(self.filepath,self.indent)
		return {'FINISHED'}

	def draw(self, context):
		pass


def menu_export(self, context):
	self.layout.operator(DefoldExporter.bl_idname, text="Defold Mesh (.go)")

def register():
	bpy.utils.register_class(DefoldExporter)
	bpy.types.TOPBAR_MT_file_export.append(menu_export)

def unregister():
	bpy.utils.unregister_class(DefoldExporter)
	bpy.types.TOPBAR_MT_file_export.remove(menu_export)


if (__name__ == "__main__"):
	register()

	try:
		with open("test.buffer", "wb") as f:
			export_to_file(f)
	finally:
		unregister()

