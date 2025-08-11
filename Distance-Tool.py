import bpy
from mathutils import Vector
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, FloatProperty, StringProperty, FloatVectorProperty

def get_bounding_box_x_distance(obj1, obj2):
    """Calculate the X-axis distance from the right side of obj1 to the left side of obj2 using bounding boxes."""
    if obj1.type != 'MESH' or obj2.type != 'MESH':
        raise ValueError("Both objects must be meshes")
    
    # Validate mesh data
    if not obj1.data or not obj2.data or len(obj1.data.vertices) == 0 or len(obj2.data.vertices) == 0:
        raise ValueError(f"Invalid mesh data for {obj1.name} (vertices: {len(obj1.data.vertices)}) or {obj2.name} (vertices: {len(obj2.data.vertices)})")
    
    # Check for unapplied transforms
    for obj in (obj1, obj2):
        if not all(abs(v - 1.0) < 1e-6 for v in obj.scale):
            print(f"WARNING: {obj.name} has unapplied scale {obj.scale}. Apply transforms (Ctrl+A > Scale) for accurate results.")
        if not all(abs(v) < 1e-6 for v in obj.rotation_euler):
            print(f"WARNING: {obj.name} has unapplied rotation {obj.rotation_euler}. Apply transforms (Ctrl+A > Rotation) for accurate results.")
    
    # Get bounding box vertices in world space
    matrix1 = obj1.matrix_world
    matrix2 = obj2.matrix_world
    
    # Compute X-range for obj1 (Object 1)
    bound_box1 = [matrix1 @ Vector(corner) for corner in obj1.bound_box]
    x_coords1 = [v.x for v in bound_box1]
    max_x1 = max(x_coords1)  # Right side of Object 1
    
    # Compute X-range for obj2 (Object 2)
    bound_box2 = [matrix2 @ Vector(corner) for corner in obj2.bound_box]
    x_coords2 = [v.x for v in bound_box2]
    min_x2 = min(x_coords2)  # Left side of Object 2
    
    # Calculate X-distance from right side of obj1 to left side of obj2
    x_distance = min_x2 - max_x1
    
    print(f"DEBUG: Bounding box X-ranges - Object 1 ({obj1.name}): Right X={max_x1:.4f}, "
          f"Object 2 ({obj2.name}): Left X={min_x2:.4f}, X-distance: {x_distance:.4f}")
    return x_distance

def update_empty_cube_target_location(self, context):
    """Update original_location when Empty Cube Target is set."""
    if self.empty_cube_target:
        self.original_location = self.empty_cube_target.location.copy()
    else:
        self.original_location = (0, 0, 0)

class DistanceOperator(Operator):
    """Calculate the X-axis distance between Object 1's right side and Object 2's left side."""
    bl_idname = "object.measure_distance"
    bl_label = "Calculate Distance"
    bl_description = "Calculate X-axis distance between Object 1's right side and Object 2's left side"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.dist_tool
        if not props.obj1 or not props.obj2:
            self.report({'ERROR'}, "Please select two mesh objects")
            props.result = "Error: Select two mesh objects"
            return {'CANCELLED'}

        if props.obj1 == props.obj2:
            self.report({'ERROR'}, "Please select two different mesh objects")
            props.result = "Error: Select different objects"
            return {'CANCELLED'}

        try:
            distance = get_bounding_box_x_distance(props.obj1, props.obj2)
            props.distance = distance
            props.result = f"X Distance: {distance:.4f} units"
            self.report({'INFO'}, props.result)
            print(f"DEBUG: Calculated X-distance: {distance:.4f} units")
            return {'FINISHED'}
        except ValueError as e:
            self.report({'ERROR'}, str(e))
            props.result = f"Error: {str(e)}"
            return {'CANCELLED'}

class MoveObjectOperator(Operator):
    """Move Empty Cube Target based on X-distance and reference empty."""
    bl_idname = "object.move_object"
    bl_label = "Move Empty Cube Target"
    bl_description = "Move Empty Cube Target based on X-distance from Object 1 to Object 2 and reference empty"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.dist_tool
        obj1, obj2, ref, empty_cube_target = props.obj1, props.obj2, props.reference, props.empty_cube_target

        if not obj1 or not obj2 or not ref or not empty_cube_target:
            self.report({'ERROR'}, "Please select Object 1, Object 2, Reference Empty, and Empty Cube Target")
            props.result = "Error: Select all objects"
            return {'CANCELLED'}

        if obj1 == obj2:
            self.report({'ERROR'}, "Object 1 and Object 2 must be different")
            props.result = "Error: Select different objects"
            return {'CANCELLED'}

        try:
            distance = get_bounding_box_x_distance(obj1, obj2)
            direction = 1 if empty_cube_target.location.x > ref.location.x else -1
            move_distance = distance + props.distance_offset
            # Store original location if not already set
            if props.original_location == (0, 0, 0) and empty_cube_target:
                props.original_location = empty_cube_target.location.copy()
            empty_cube_target.location.x += direction * move_distance
            props.result = f"Moved Empty Cube Target by {move_distance:.4f} units {'right' if direction > 0 else 'left'}"
            self.report({'INFO'}, props.result)
            print(f"DEBUG: Moved {empty_cube_target.name} by {move_distance:.4f} units {'right' if direction > 0 else 'left'}")
            return {'FINISHED'}
        except ValueError as e:
            self.report({'ERROR'}, str(e))
            props.result = f"Error: {str(e)}"
            return {'CANCELLED'}

class ResetPositionOperator(Operator):
    """Reset Empty Cube Target to its original position."""
    bl_idname = "object.reset_position"
    bl_label = "Reset Empty Cube Target Position"
    bl_description = "Reset Empty Cube Target to its original position"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.dist_tool
        if not props.empty_cube_target:
            self.report({'ERROR'}, "Please select Empty Cube Target")
            props.result = "Error: Select Empty Cube Target"
            return {'CANCELLED'}

        if props.original_location == (0, 0, 0):
            self.report({'WARNING'}, "No valid original location stored. Please select Empty Cube Target again or move it first.")
            props.result = "Warning: No valid original location stored"
            return {'CANCELLED'}

        props.empty_cube_target.location = props.original_location
        props.result = "Empty Cube Target position reset"
        self.report({'INFO'}, props.result)
        print(f"DEBUG: Reset {props.empty_cube_target.name} to {props.original_location}")
        return {'FINISHED'}

class DistanceToolProperties(PropertyGroup):
    obj1: PointerProperty(type=bpy.types.Object, name="Object 1")
    obj2: PointerProperty(type=bpy.types.Object, name="Object 2")
    reference: PointerProperty(type=bpy.types.Object, name="Reference Empty")
    empty_cube_target: PointerProperty(
        type=bpy.types.Object,
        name="Empty Cube Target",
        update=update_empty_cube_target_location
    )
    distance: FloatProperty(name="X Distance", default=0.0, precision=4, description="Measured X-axis distance between Object 1's right side and Object 2's left side")
    distance_offset: FloatProperty(name="Distance Offset", default=0.0, precision=4, description="Additional distance to move Empty Cube Target")
    original_location: FloatVectorProperty(name="Original Location", size=3, default=(0, 0, 0))
    result: StringProperty(name="Result", default="No result yet", description="Result of the last operation")

class DistanceToolPanel(Panel):
    """Panel in 3D Viewport > Sidebar > Distance Tool to calculate X-distance and move Empty Cube Target."""
    bl_label = "Distance Tool"
    bl_idname = "VIEW3D_PT_distance_tool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Distance Tool'

    def draw(self, context):
        layout = self.layout
        props = context.scene.dist_tool

        layout.prop(props, "obj1")
        layout.prop(props, "obj2")
        layout.prop(props, "reference")
        layout.prop(props, "empty_cube_target")
        layout.prop(props, "distance_offset")
        layout.operator("object.measure_distance")
        layout.label(text=f"X Distance: {props.distance:.4f}")
        layout.operator("object.move_object")
        layout.operator("object.reset_position")
        layout.label(text=props.result)

def register():
    print("Registering Distance Tool classes")
    try:
        bpy.utils.register_class(DistanceOperator)
        bpy.utils.register_class(MoveObjectOperator)
        bpy.utils.register_class(ResetPositionOperator)
        bpy.utils.register_class(DistanceToolProperties)
        bpy.utils.register_class(DistanceToolPanel)
        bpy.types.Scene.dist_tool = PointerProperty(type=DistanceToolProperties)
        print("Registration successful")
    except Exception as e:
        print(f"Registration failed: {str(e)}")

def unregister():
    print("Unregistering Distance Tool classes")
    try:
        bpy.utils.unregister_class(DistanceOperator)
        bpy.utils.unregister_class(MoveObjectOperator)
        bpy.utils.unregister_class(ResetPositionOperator)
        bpy.utils.unregister_class(DistanceToolProperties)
        bpy.utils.unregister_class(DistanceToolPanel)
        del bpy.types.Scene.dist_tool
        print("Unregistration successful")
    except Exception as e:
        print(f"Unregistration failed: {str(e)}")

if __name__ == "__main__":
    register()