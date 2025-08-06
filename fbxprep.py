####################################################################################
# Kalev Mölder       2025       https://tinkering.ee        molder.kalev@gmail.com #
#                                                                                  #
# Speed Tree FBX formatter script                                                  #
####################################################################################

# input fbx file is assumed to be a "generic fbx"
# exported from Speed Tree Modeller
# it should have one root object and multiple LOD objects
# as its children

#   - root_obj
#      - LOD0
#      - LOD1
#      - LOD2
#      - root_obj_Billboard_LOD3

# the script prepares the fbx scene so that it would be
# compatible with Unreal Engine static mesh importer

# this way the LOD levels are imported as intended

# basically sets a custom prop on the root obj: fbx_type=LodGroup
# and changes the last LOD obj name so it would be similar to the other lods
# speed tree adds "TreeName_Billboard" to the last lod level obj name

# obj transforms are also applied, so the resulting fbx scene objects
# will all have identity transform

# uses the "copy" path option so the textures will be copied to the 
# exported fbx dir as .fbm subfolder

import bpy
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] # only keep args after "--"

if len(argv) < 2:
    print("Usage: blender --background --python script.py -- input.fbx output.fbx")
    sys.exit(1)
    
input_fbx = argv[0]
output_fbx = argv[1]

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.import_scene.fbx(filepath=input_fbx)

print("fbx imported, prepping objects now...")

root_obj = None

def apply_transform(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

for o in bpy.data.objects:
    if o.parent == None:
        root_obj = o
        break

if root_obj != None:
    print("starting to prep obj: %s" % (root_obj.name))
    
    # adding special LodGroup fbx_type property
    # so lods are imported by Unreal Engine properly
    
    root_obj["fbx_type"] = "LodGroup"
    
    apply_transform(root_obj)
    
    for child in root_obj.children:
        print("\thandling child:", child.name)
        
        # fixing billboard lod name
        if len(child.name) > 4:
            child.name = child.name[-4:]
            
        apply_transform(child)

else:
    print("Could not find root object?") # very unusual, mabye empty fbx scene
    sys.exit(1)

print("objects prepared, exporting now...")

bpy.ops.export_scene.fbx(
    filepath=output_fbx,
    bake_space_transform=True,
    mesh_smooth_type="FACE",
    use_custom_props=True,
    path_mode="COPY"
)