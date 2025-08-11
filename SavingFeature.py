import bpy

class MoveObjectXOperator(bpy.types.Operator):
    bl_idname = "object.move_x_offset"
    bl_label = "Move X by 0.01"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Execture moving operation
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            print("ERROR: No object selected for movement")
            return{'CANCELLED'}
        #MOVE OBJECT BY 0.01 IN x-AXIS
        obj.location.x += 0.01
        self.report({'INFO'}, f"Moved {obj.name}to X = {obj.location.x:.4f}")
        print(f"DEBUG: Moved {obj.name}to X = {obj.location.x:.4f}")
        context.view_layer.update()
        return {'FINISHED'}
    
class MoveObjectPanel(bpy.types.Panel):
    bl_label = "Move Object Tool"
    bl_idname = "VIEW3D_PT_move_object_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SaveTesting'
    
    def draw(self, context):
        #Draw UI panel
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        box.label (text = "Object Selection", icon = 'OBJECT_DATA')
        if not scene.move_object:
            box.label (text = "Select Valid Object", icon = 'ERROR')
        box.prop(scene, "move_object", text = "Object")
        
        box = layout.box()
        box.label(text = "Actions", icon = 'TOOL_SETTINGS')
        box.operator("object.move_x_offset", text = "Move X by 0.01")
            

classes = [
    MoveObjectXOperator, 
    MoveObjectPanel,
]

def register():
    #Register class and properties
    print("Registering Move Objects Tool classes")
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.move_object = bpy.props.PointerProperty(
        name = "Move Object",
        description = "Object to move along the X-axis", 
        type = bpy.types.Object
    )
    
def unregister():
    #Unregister classes and properties
    print ("Unregistering Move object Toll classes")
    for cls in reversed(classes):
        bpy.utils.unregisters_class(cls)
        
        if hasattr(bpy.types.Scene, "move_object"):
            delattr(bpy.types.Scene, "move_object")

if __name__ == "__main__":
    register()