import bpy 
from bpy.props import PointerProperty

bpy.types.Scene.target1 = PointerProperty(
    type = bpy.types.Object,
    name = "Object 1"
    )
bpy.types.Scene.target2 = PointerProperty(
    type = bpy.types.Object,  
    name = "Object 2"
    )  
    
class OBJECTPICKER_PT_Panel(bpy.types.Panel):
    bl_label = "Object Picker Panel"
    bl_idname = "PT_ObjectPickerPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Addon'
    bl_context = 'objectmode'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "target1", text = "Select Object 1")
        layout.prop(scene, "target2", text = "Select Object 2")
        
        layout.label(text = f"Object 1: {scene.target1.name if scene.target1 else 'None'}")
        layout.label(text = f"Object 2: {scene.target2.name if scene.target2 else 'None'}")

#Refister classes
classes = (
    OBJECTPICKER_PT_Panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)             
        
    del bpy.types.Scene.target1
    del bpy.types.Scene.target2

if __name__ == "__main__":
    register()        