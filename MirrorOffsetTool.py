import bpy

def set_mirror_object(mirror_object_name = 'Centre-Target'):
    #Get the object
    obj = bpy.context.active_object
    mirror_obj = bpy.data.objects.get(mirror_object_name)
    
    #Check if object exists
    if not obj:
        print("Object not found")
        return
    if not mirror_obj:
        print(f"Mirror object '{mirror_object_name}' not found")
        return
    
    #Check for mirror modifiers
    has_mirror = False
    for modifier in obj.modifiers:
        if modifier.type == 'MIRROR':
            has_mirror = True
            #Assign the mirror object
            modifier.mirror_object = mirror_obj
            print(f"Assigned '{mirror_object_name}' to Mirror Modifier of {obj.name}'")
            break
    
    if not has_mirror:
        print(f"No Mirror modifier found on '{obj.name}'")   
        
         
set_mirror_object()    