# SpeedTree fbxprep

Python TkInter GUI program / script to convert Speed Tree exported FBX files into Unreal Engine compatible FBX files with proper custom object properties and conformed LOD naming.

this is a simple python GUI program and Blender script to convert 
a fbx file exported from Speed Tree Modeler to an Unreal Engine ready
fbx scene file.

It works by executing a Blender python script that:
    - imports the target file
    - applies all transforms (output fbx objects have "0" transform)
    - adds the custom prop to root obj: fbx_type=LodGroup
    - renames billboard lod obj so it fits with the other lod objs.
    - exports the "corrected" fbx file with specific settings at the specified file location

requires:
    Blender 4.5 (version can be changed when modifiying the fbxprepui.py)
    python with tkinter (tested with ver 3.11.9 on windows)
    Windows centric paths in scipt for now... wont work on Linux

Background:

    I found that when working with Speed Tree Modeler -> Unreal Engine.
    That the lod formatting started to take too long when I was iterating
    on some tree / plant design and repeatedly exported / imported it to visualize
    the asset in context.

    As my day job is literally mostly to come up with automation solutions for
    various VFX studio scenarios. This problem was very fit for me to solve.

    Unreal engine static mesh importer needs the fbx file scene root object to have the specific 
    property named "fbx_type" set to "LodGroup" so that it would "know" that the objects should
    be imported as LOD-s for the static mesh.

    That's why I felt compelled to create a "one click" solution to this process.

    So instead of importing the exported FBX into blender and doing all the repetetive
    simple motions with it. I now have a program to do it with much more convenience and speed.

    PS 
        I think I also need to implement something on the Unreal side as well, because
        importing new plant assets still require too many clicks and motions that are
        very repetetive and simplistic. I would be content with having "1 click to format the fbx" and
        "1 click in unreal engine" to import a new plant asset. The unreal engine side is still
        quite messy when in comes to importing a LOD static mesh. mainly because of the default settings
        applied to static meshes at start. (nanite and all the auto LOD options that usually get in the way 
        more than they help)

    PPS
        This is a python program so no "exe". If you are here you'll figure it out ;D
