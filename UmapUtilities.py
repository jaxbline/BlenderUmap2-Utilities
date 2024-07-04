bl_info = {
    "name": "Umap Utilities",
    "blender": (4, 1, 0),
    "category": "Object",
    "version": (1, 0, 6),
    "author": "Jax",
    "description": "A bunch of random QoL stuff I made for working with Umap Exporter.",
}

import bpy
import mathutils

def disconnect_shader_nodes():
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mat_slot in obj.material_slots:
                if mat_slot.material and mat_slot.material.use_nodes:
                    node_tree = mat_slot.material.node_tree
                    links_to_remove = []
                    for link in node_tree.links:
                        if link.from_node.type == 'GROUP' or link.to_node.type == 'GROUP':
                            links_to_remove.append(link)
                    for link in links_to_remove:
                        node_tree.links.remove(link)

def replace_with_principled_bsdf(node_tree, diffuse_suffix, normals_suffix, metallic_roughness_suffix):
    nodes_to_delete = [node for node in node_tree.nodes if node.type == 'GROUP']

    for node in nodes_to_delete:
        location = node.location

        principled_bsdf = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_bsdf.location = location

        normal_map_nodes = {}

        separate_rgb = node_tree.nodes.new(type='ShaderNodeSeparateRGB')
        separate_rgb.location = location + mathutils.Vector((200, -200))
        node_tree.links.new(separate_rgb.outputs['R'], principled_bsdf.inputs['Metallic'])
        node_tree.links.new(separate_rgb.outputs['G'], principled_bsdf.inputs['Roughness'])

        for tex_node in node_tree.nodes:
            if tex_node.type == 'TEX_IMAGE' and tex_node.image:
                if tex_node.image.name.endswith(diffuse_suffix):
                    node_tree.links.new(tex_node.outputs.get('Color'), principled_bsdf.inputs.get('Base Color'))
                elif tex_node.image.name.endswith(normals_suffix):
                    normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
                    normal_map_node.location = tex_node.location + mathutils.Vector((200, 0))
                    node_tree.links.new(tex_node.outputs.get('Color'), normal_map_node.inputs.get('Color'))
                    normal_map_nodes[tex_node] = normal_map_node
                elif tex_node.image.name.endswith(metallic_roughness_suffix):
                    node_tree.links.new(tex_node.outputs.get('Color'), separate_rgb.inputs['Image'])

        for tex_node, normal_map_node in normal_map_nodes.items():
            node_tree.links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

        material_output = None
        for output_node in node_tree.nodes:
            if output_node.type == 'OUTPUT_MATERIAL':
                material_output = output_node
                break

        if material_output:
            node_tree.links.new(principled_bsdf.outputs['BSDF'], material_output.inputs['Surface'])

        links_to_reconnect = [link for link in node_tree.links if link.to_node == node or link.from_node == node]
        for link in links_to_reconnect:
            if link.to_node == node:
                new_input = principled_bsdf.inputs.get(link.to_socket.name)
                if new_input:
                    node_tree.links.new(link.from_socket, new_input)
            if link.from_node == node:
                new_output = principled_bsdf.outputs.get(link.from_socket.name)
                if new_output:
                    node_tree.links.new(new_output, link.to_socket)

        node_tree.nodes.remove(node)

def fix_materials(context):
    disconnect_shader_nodes()
    diffuse_suffix = context.scene.diffuse_suffix
    normals_suffix = context.scene.normals_suffix
    metallic_roughness_suffix = context.scene.metallic_roughness_suffix

    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            for slot in obj.material_slots:
                material = slot.material
                if material and material.use_nodes:
                    replace_with_principled_bsdf(material.node_tree, diffuse_suffix, normals_suffix, metallic_roughness_suffix)
    print("Disconnected shader nodes connected to node groups and replaced group nodes with Principled BSDF nodes.")

class OBJECT_OT_join_same_material(bpy.types.Operator):
    bl_idname = "object.join_same_material"
    bl_label = "Join Meshes"
    bl_description = "Joins meshes by material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        active_obj = context.active_object
        hide_after_join = context.scene.hide_after_join
        apply_to_all = context.scene.apply_to_all

        if active_obj and active_obj.material_slots:
            active_material = active_obj.material_slots[0].material

            bpy.ops.object.select_all(action='DESELECT')

            if apply_to_all:
                # Group objects by material
                material_groups = {}
                for obj in context.view_layer.objects:
                    if obj.type == 'MESH' and obj.material_slots:
                        for slot in obj.material_slots:
                            material = slot.material
                            if material:
                                if material not in material_groups:
                                    material_groups[material] = []
                                material_groups[material].append(obj)

                # Join each group of objects
                for material, objs in material_groups.items():
                    bpy.ops.object.select_all(action='DESELECT')
                    for obj in objs:
                        obj.select_set(True)
                    if objs:
                        context.view_layer.objects.active = objs[0]
                        bpy.ops.object.join()
                        if hide_after_join:
                            context.active_object.hide_set(True)
            else:
                for obj in context.view_layer.objects:
                    if obj.type == 'MESH' and obj.material_slots:
                        if any(slot.material == active_material for slot in obj.material_slots):
                            obj.select_set(True)

                context.view_layer.objects.active = active_obj
                bpy.ops.object.join()

                if hide_after_join:
                    context.active_object.hide_set(True)
        else:
            self.report({'WARNING'}, "The active object does not have any material assigned.")
            return {'CANCELLED'}

        return {'FINISHED'}

class OBJECT_OT_fix_materials(bpy.types.Operator):
    bl_idname = "object.fix_materials"
    bl_label = "Fix Materials"
    bl_description = "Disconnects shader nodes connected to node groups and replaces group nodes with Principled BSDF nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        fix_materials(context)
        return {'FINISHED'}

class OBJECT_OT_make_instance_real(bpy.types.Operator):
    bl_idname = "object.make_instance_real"
    bl_label = "Make Instance Real"
    bl_description = "Make the selected instance real"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.duplicates_make_real()
        return {'FINISHED'}

class OBJECT_OT_merge_verts_by_distance(bpy.types.Operator):
    bl_idname = "object.merge_verts_by_distance"
    bl_label = "Merge Vertices by Distance"
    bl_description = "Merge vertices of the selected object by distance"
    bl_options = {'REGISTER', 'UNDO'}
    
    distance: bpy.props.FloatProperty(
        name="Distance",
        description="Distance within which to merge vertices",
        default=0.001,
        min=0.001,
        max=10.0
    )

    def execute(self, context):
        active_obj = context.active_object
        apply_to_all = context.scene.apply_to_all

        if active_obj and active_obj.type == 'MESH':
            if apply_to_all:
                # Group objects by material
                material_groups = {}
                for obj in context.view_layer.objects:
                    if obj.type == 'MESH' and obj.material_slots:
                        for slot in obj.material_slots:
                            material = slot.material
                            if material:
                                if material not in material_groups:
                                    material_groups[material] = []
                                material_groups[material].append(obj)

                # Merge vertices for each group of objects
                for material, objs in material_groups.items():
                    bpy.ops.object.select_all(action='DESELECT')
                    for obj in objs:
                        obj.select_set(True)
                    if objs:
                        context.view_layer.objects.active = objs[0]
                        bpy.ops.object.mode_set(mode='EDIT')
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.remove_doubles(threshold=self.distance)
                        bpy.ops.object.mode_set(mode='OBJECT')
            else:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=self.distance)
                bpy.ops.object.mode_set(mode='OBJECT')
        else:
            self.report({'WARNING'}, "The active object is not a mesh.")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class VIEW3D_PT_umap_utilities(bpy.types.Panel):
    bl_label = "Umap Utilities"
    bl_idname = "VIEW3D_PT_umap_utilities"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.join_same_material")
        layout.operator("object.make_instance_real")
        layout.label(text="Merge Vertices")
        box = layout.box()
        box.operator("object.merge_verts_by_distance")
        box.prop(context.scene, "merge_distance")
        layout.label(text="Options")
        box = layout.box()
        box.prop(context.scene, "hide_after_join")
        box.prop(context.scene, "apply_to_all")
        layout.label(text="Fix Materials")
        box = layout.box()
        box.operator("object.fix_materials")
        box.prop(context.scene, "diffuse_suffix")
        box.prop(context.scene, "normals_suffix")
        box.prop(context.scene, "metallic_roughness_suffix")

def register():
    bpy.utils.register_class(OBJECT_OT_join_same_material)
    bpy.utils.register_class(OBJECT_OT_fix_materials)
    bpy.utils.register_class(OBJECT_OT_make_instance_real)
    bpy.utils.register_class(OBJECT_OT_merge_verts_by_distance)
    bpy.utils.register_class(VIEW3D_PT_umap_utilities)
    bpy.types.Scene.hide_after_join = bpy.props.BoolProperty(
        name="Hide After Join",
        description="Hide meshes after joining",
        default=False
    )
    bpy.types.Scene.apply_to_all = bpy.props.BoolProperty(
        name="Apply to All",
        description="Apply actions to all meshes",
        default=False
    )
    bpy.types.Scene.diffuse_suffix = bpy.props.StringProperty(
        name="Diffuse Suffix",
        description="Suffix for Diffuse textures",
        default="_di"
    )
    bpy.types.Scene.normals_suffix = bpy.props.StringProperty(
        name="Normals Suffix",
        description="Suffix for Normals textures",
        default="_no"
    )
    bpy.types.Scene.metallic_roughness_suffix = bpy.props.StringProperty(
        name="Metallic/Roughness Suffix",
        description="Suffix for Metallic/Roughness textures",
        default="_mr"
    )
    bpy.types.Scene.merge_distance = bpy.props.FloatProperty(
        name="Merge Distance",
        description="Distance within which to merge vertices",
        default=0.001,
        min=0.001,
        max=10.0
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_join_same_material)
    bpy.utils.unregister_class(OBJECT_OT_fix_materials)
    bpy.utils.unregister_class(OBJECT_OT_make_instance_real)
    bpy.utils.unregister_class(OBJECT_OT_merge_verts_by_distance)
    bpy.utils.unregister_class(VIEW3D_PT_umap_utilities)
    del bpy.types.Scene.hide_after_join
    del bpy.types.Scene.apply_to_all
    del bpy.types.Scene.diffuse_suffix
    del bpy.types.Scene.normals_suffix
    del bpy.types.Scene.metallic_roughness_suffix
    del bpy.types.Scene.merge_distance

if __name__ == "__main__":
    register()
