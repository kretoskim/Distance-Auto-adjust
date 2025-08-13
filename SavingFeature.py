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
    saved_rotation: bpy.props.FloatVectorProperty(
        name = "Saved Rotation",
        description = "Stored location (X, Y, Z) of the selected object",
        size = 3,
        default = (0.0, 0.0, 0.0)
    ) 
    has_saved_location: bpy.props.BoolProperty(default = False) 
    has_saved_rotation: bpy.props.BoolProperty(default = False) 
    
#Utility to get current active object
def get_active_move_object(context):
    scene = context.scene
    if scene.active_object_slot == 'SLOT1':
        return scene.object_slot_1
    elif scene.active_object_slot == 'SLOT2':
        return scene.object_slot_2
    return None

#Auto-hide inactive slot object
def update_active_slot(self, context):
    active_obj = get_active_move_object(context)
    context.scene.move_object = active_obj
    
    for obj in [context.scene.object_slot_1, context.scene.object_slot_2]:
        if obj:
            if obj == active_obj:
                obj.hide_set(False) #Visible in viewport
                obj.hide_viewport = False
                obj.hide_render = False
                obj.hide_select = False        
            else:
                obj.hide_set(True) #Hidden in viewport
                obj.hide_viewport = False
                obj.hide_render = False
                obj.hide_select = False

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

#Dynamic dropdown update
def active_slot_items(self, context):
    scene = context.scene
    slot1_name = scene.object_slot_1.name if scene.object_slot_1 else "Slot 1 (Empty)"
    slot2_name = scene.object_slot_2.name if scene.object_slot_2 else "Slot 2 (Empty)"
    return [
        ('SLOT1', slot1_name, "Use object in Slot 1"),
        ('SLOT2', slot2_name, "Use object in Slot 2"),
    ]   
        
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
        box.prop(scene, "object_slot_1", text = "Slot_1")
        box.prop(scene, "object_slot_2", text = "Slot_2")
        box.prop(scene, "active_object_slot", text = "Active Slot")
        
        active_obj = get_active_move_object(context)
        if active_obj:
            box.label(text = f"Active Object: {active_obj.name}", icon = 'INFO')
        else:
            box.label(text = "No Object in active slot", icon = 'ERROR')
        
        box = layout.box()
        box.label(text = "Actions", icon = 'TOOL_SETTINGS')
        box.operator("object.move_x_offset")
        box.operator("object.save_location_rotation")
        box.operator("object.recall_saved_location_rotation")
        box.operator("object.reset_location")
        box.operator("object.clear_saved_location")
        box.operator("object.rotate_45_z")
                 
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
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.object_slot_1 = bpy.props.PointerProperty(type = bpy.types.Object)    
    bpy.types.Scene.object_slot_2 = bpy.props.PointerProperty(type = bpy.types.Object)  
     
    bpy.types.Scene.active_object_slot = bpy.props.EnumProperty(
        name = "Active Object Slot",
        items = active_slot_items,
        update = update_active_slot
    )
    bpy.types.Scene.object_location = bpy.props.PointerProperty(type = ObjectLocationPropertyGroup)
    bpy.types.Scene.move_object = bpy.props.PointerProperty(type = bpy.types.Object)
    
        
    
def unregister():
    #Unregister classes and properties
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.object_slot_1
    del bpy.types.Scene.object_slot_2
    del bpy.types.Scene.active_object_slot
    del bpy.types.Scene.object_location  
    del bpy.types.Scene.move_object  

if __name__ == "__main__":
    register()
    