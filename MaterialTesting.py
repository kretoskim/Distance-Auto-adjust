import bpy

#Panel
class VIEW3D_PT_custom_albedo(bpy.types.Panel):
    bl_label = "Custom Albedo Changer"
    bl_idname = "VIEW3D_PT_custom_albedo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        
        #Dropdown
        layout.prop(context.scene, "custom_material", text = "Materal")
        
        #Get material
        mat = bpy.data.materials.get(context.scene.custom_material)
        
        if mat and mat.use_nodes:
            principled = next((node for node in mat.node_tree.nodes if node.type == 'BSDF_PRINCIPLED'), None)
            if principled:
                #Color picker 
                layout.prop(principled.inputs['Base Color'], "default_value", text = "Albedo Color")
            else:
                layout.label(text = "No principled BSDF")
        else:
            layout.label(text = "No nodes enabled")

#Register property & panel
def register():
    # Define the EnumProperty for material selection
    bpy.types.Scene.custom_material = bpy.props.EnumProperty(
        name="Material",
        description="Select an existing material",
        items=lambda self, context: [(mat.name, mat.name, "") for mat in bpy.data.materials],
        update=lambda self, context: None
    )
    bpy.utils.register_class(VIEW3D_PT_custom_albedo)

# Unregister the property and panel
def unregister():
    del bpy.types.Scene.custom_material
    bpy.utils.unregister_class(VIEW3D_PT_custom_albedo)

# Register when running the script
if __name__ == "__main__":
    register()                        