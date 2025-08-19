import bpy

# Custom panel in the 3D Viewport sidebar (N-panel)
class VIEW3D_PT_custom_albedo(bpy.types.Panel):
    bl_label = "Custom Reflection Changer"
    bl_idname = "VIEW3D_PT_custom_albedo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom"  
    bl_context = "objectmode" 
    
    def draw(self, context):
        layout = self.layout
        
        # Dropdown to select an existing material
        layout.prop(context.scene, "custom_material", text="Material")
        
        # Get the selected material
        mat = bpy.data.materials.get(context.scene.custom_material)
        
        if mat and mat.use_nodes:
            # Check for Octane Specular Material node by bl_idname
            octane_specular = next((node for node in mat.node_tree.nodes if node.bl_idname == 'OctaneSpecularMaterial'), None)
            if octane_specular:
                # Color picker for Reflection input
                layout.prop(octane_specular.inputs['Transmission'], "default_value", text="Transmission Color")
            else:
                layout.label(text="No Octane Specular Material found.")
        else:
            layout.label(text="No material selected or nodes not enabled.")

# Register the custom material property, panel, and operator
def register():
    bpy.types.Scene.custom_material = bpy.props.EnumProperty(
        name="Material",
        description="Select an existing material",
        items=lambda self, context: [(mat.name, mat.name, "") for mat in bpy.data.materials],
        update=lambda self, context: None
    )
    bpy.utils.register_class(VIEW3D_PT_custom_albedo)

# Unregister the property, panel, and operator
def unregister():
    del bpy.types.Scene.custom_material
    bpy.utils.unregister_class(VIEW3D_PT_custom_albedo)

# Register when running the script
if __name__ == "__main__":
    register()