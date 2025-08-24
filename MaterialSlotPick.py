import bpy 
from bpy.props import PointerProperty

# Function to assign material to object and show feedback
def assign_material(obj, mat, obj_name, mat_name):
    if obj and mat:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        # Show feedback in Blender UI
        bpy.context.window_manager.popup_menu(
            lambda self, ctx: self.layout.label(text=f"Assigned {mat.name} to {obj.name}"),
            title="Info"
        )
    elif obj:
        bpy.context.window_manager.popup_menu(
            lambda self, ctx: self.layout.label(text=f"No material selected for {obj_name}"),
            title="Warning"
        )
    elif mat:
        bpy.context.window_manager.popup_menu(
            lambda self, ctx: self.layout.label(text=f"No object selected for {mat_name}"),
            title="Warning"
        )

#Update Functions        
def update_target1(self, context):
    assign_material(self.target1, self.material1, "Object 1", "Material 1")
    
def update_target2(self, context):
    assign_material(self.target2, self.material1, "Object 2", "Material 2")

def update_material1(self, context):
    assign_material(self.target1, self.material1, "Object 1", "Material 1")
    
def update_material2(self, context):
    assign_material(self.target2, self.material2, "Object 2", "Material 2")            
                            
#Define PointerProperty                             
bpy.types.Scene.target1 = PointerProperty(
    type = bpy.types.Object,
    name = "Object 1",
    update = update_target1
    )
bpy.types.Scene.target2 = PointerProperty(
    type = bpy.types.Object,  
    name = "Object 2",
    update = update_target2
    )  
bpy.types.Scene.material1 = PointerProperty(
    type = bpy.types.Material, 
    name = "Material 1", 
    update = update_material1   
    )
bpy.types.Scene.material2 = PointerProperty(
    type = bpy.types.Material,
    name = "Material 2",
    update = update_material2
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
        
        layout.prop(scene, "material1", text = "Material for object1")
        layout.prop(scene, "material2", text = "Material for object2")
        

#Register classes
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
    del bpy.types.Scene.material1
    del bpy.types.Scene.material2

if __name__ == "__main__":
    register()        