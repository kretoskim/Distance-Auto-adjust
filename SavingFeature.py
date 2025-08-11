import bpy
from mathutils import Vector
import math

class ObjectLocationPropertyGroup(bpy.types.PropertyGroup):
    saved_location: bpy.props.FloatVectorProperty(
        name = "Saved Location",
        description = "Stored location (X, Y, Z) of the selected object",
        size = 3,
        default = (0.03, 0.0, 0.0)
    )
    
    #propertyGroup to store saved rotation
    saved_rotation: bpy.props.FloatVectorProperty(
        name = "Saved Rotation",
        description = "Stored location (X, Y, Z) of the selected object",
        size = 3,
        default = (0.0, 0.0, 0.0)
    )
    
    has_saved_location: bpy.props.BoolProperty(
        name = "Has Saved location",
        description = "Indicates if location is saved",
        default = False
    ) 
    has_saved_rotation: bpy.props.BoolProperty(
        name = "Has Saved rotation",
        description = "Indicates if rotation is saved",
        default = False  
    )      

class MoveObjectXOperator(bpy.types.Operator):
    bl_idname = "object.move_x_offset"
    bl_label = "Move X by 0.01"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            print("ERROR: No object selected for movement")
            return{'CANCELLED'}
        
        obj.location.x += 0.01
        self.report({'INFO'}, f"Moved {obj.name}to X = {obj.location.x:.4f}")
        context.view_layer.update()
        return {'FINISHED'}

class ResetObjectLocationOperator(bpy.types.Operator):
    bl_idname = "object.reset_location"
    bl_label = "Reset Location & Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
                  
        obj.location = Vector((0.03, 0.0, 0.0))
        obj.rotation_euler = Vector((0.0, 0.0, 0.0))       
        self.report({'INFO'}, f"Reset {obj.name} to origin")
        context.view_layer.update()
        return {'FINISHED'}    
    
class SaveObjectLocationOperator(bpy.types.Operator):
    bl_idname = "object.save_location_rotation"
    bl_label = "Save Location & Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            print("ERROR: No object selected")
            return {'CANCELLED'}
        
        saved_data = context.scene.object_location
        saved_data.saved_location = obj.location.copy()
        saved_data.saved_rotation = obj.rotation_euler.copy()     
        saved_data.has_saved_location = True
        saved_data.has_saved_rotation = True
        
        self.report({'INFO'}, f"Saved {obj.name} location and rotation")
        return {'FINISHED'}
    
class RecallObjectLocationOperator(bpy.types.Operator):
    bl_idname = "object.recall_saved_location_rotation"
    bl_label = "Recall Saved Location & Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        saved_data = context.scene.object_location
        if not saved_data.has_saved_location and not saved_data.has_saved_rotation:
            self.report({'ERROR'}, "No saved data to recall")
            return {'CANCELLED'}
        obj.location = saved_data.saved_location
        obj.rotation_euler = saved_data.saved_rotation
        self.report({'INFO'}, f"Recalled {obj.name} saved location and rotation")
        context.view_layer.update()
        return {'FINISHED'}
    
class ClearSavedLocationOperator(bpy.types.Operator):
    bl_idname = "object.clear_saved_location"
    bl_label = "Clear Saves"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj_location = context.scene.object_location      
        obj_location.saved_location = Vector((0.03, 0.0, 0.0))
        obj_location.saved_rotation = Vector((0.0, 0.0, 0.0))
        obj_location.has_saved_location = False
        obj_location.has_saved_rotation = False
        
        self.report({'INFO'}, "Cleared Save")
        print("DEBUG: Cleared save")
        return {'FINISHED'}
    
class RotateObjectOperator(bpy.types.Operator):
    bl_idname = "object.rotate_45_z"
    bl_label = "Rotate 45"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.scene.move_object
        if not obj:
            self.report({'ERROR'}, "No object")
            return {'CANCELLED'}
        
        obj.rotation_euler.z += math.radians(45)
        self.report({'INFO'}, f"Rotated {obj.name} by 45")
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
        box.label(text = "Location Info", icon = 'INFO')
        if scene.object_location.has_saved_location:
            loc = scene.object_location.saved_location
            box.label(text = f"Saved: ({loc[0]: .4f}, {loc[1]: .4f}, {loc[2]: .4f})")
        else:
            box.label(text = "No saved location")
        
        box = layout.box()
        box.label(text = "Actions", icon = 'TOOL_SETTINGS')
        box.operator("object.move_x_offset", text = "Move X by 0.01")
        box.operator("object.save_location_rotation", text = "Save Location & Rotation")
        box.operator("object.recall_saved_location_rotation", text = "Recall Save")
        box.operator("object.reset_location", text = "Reset Location & Rotation")
        box.operator("object.clear_saved_location", text = "Clear Saves")
        box.operator("object.rotate_45_z", text = "Rotate 45")
                 
classes = [
    ObjectLocationPropertyGroup,
    MoveObjectXOperator, 
    ResetObjectLocationOperator,
    SaveObjectLocationOperator,
    RecallObjectLocationOperator,
    ClearSavedLocationOperator,
    RotateObjectOperator,
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
    