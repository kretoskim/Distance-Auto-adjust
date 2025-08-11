import bpy
from mathutils import Vector

class ObjectLocationPropertyGroup(bpy.types.PropertyGroup):
    #propertyGrouip to store saved location
    saved_location: bpy.props.FloatVectorProperty(
        name = "Saved Location",
        description = "Stored location (X, Y, Z) of the selected object",
        size = 3,
        default = (0.03, 0.0, 0.0)
    )
    has_saved_location: bpy.props.BoolProperty(
        name = "Has Saved location",
        description = "Indicates if  location is saved",
        default = False
    )      

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

class ResetObjectLocationOperator(bpy.types.Operator):
    #Reset object to origin/relative origin
    bl_idname = "object.reset_location"
    bl_label = "Reset Location"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Execute reset operation
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            print("ERROR: No object selected")
            return {'CANCELLED'}
            
        #Reset object location
        obj.location = Vector((0.03, 0.0, 0.0))
        self.report({'INFO'}, f"Reset {obj.name} location to (0.03, 0.0, 0.0)")
        print("DEBUG: Reset {obj.name} location to (0.03, 0.0, 0.0)")
        context.view_layer.update()
        return {'FINISHED'}    
    
class SaveObjectLocationOperator(bpy.types.Operator):
    #Operator to save current location
    bl_idname = "object.save_location"
    bl_label = "Save Location"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Execute save operation
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            print("ERROR: No object selected")
            return {'CANCELLED'}
        
        #Save object current location
        context.scene.object_location.saved_location = obj.location
        context.scene.object_location.has_saved_location = True
        self.report({'INFO'}, f"Saved {obj.name} location: ({obj.location.x:.4f}, {obj.location.y:.4f}, {obj.location.z:.4f})")
        print(f"DEBUG: Saved {obj.name} location: ({obj.location.x:.4f}, {obj.location.y:.4f}, {obj.location.z:.4f})")
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
        box.label(text = "Location Info", icon = 'INFO')
        if scene.object_location.has_saved_location:
            loc = scene.object_location.saved_location
            box.label(text = f"Saved: ({loc[0]: .4f}, {loc[1]: .4f}, {loc[2]: .4f})")
        else:
            box.label(text = "No saved location")
        
        box = layout.box()
        box.label(text = "Actions", icon = 'TOOL_SETTINGS')
        box.operator("object.move_x_offset", text = "Move X by 0.01")
        box.operator("object.save_location", text = "Save Location")
        box.operator("object.reset_location", text = "Reset Location")
            
classes = [
    ObjectLocationPropertyGroup,
    MoveObjectXOperator, 
    ResetObjectLocationOperator,
    SaveObjectLocationOperator,
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
    bpy.types.Scene.object_location = bpy.props.PointerProperty( 
        type = ObjectLocationPropertyGroup
    )
    
def unregister():
    #Unregister classes and properties
    print ("Unregistering Move object Toll classes")
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    if hasattr(bpy.types.Scene, "move_object"):
        del bpy.types.Scene.move_object
    if hasattr(bpy.types.Scene, "object_location"):
        del bpy.types.Scene.object_location  

if __name__ == "__main__":
    register()
    