import bpy
import argparse
import sys
import os

# -------------------------
# Argument parsing
# -------------------------
argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []

parser = argparse.ArgumentParser(description="Import OBJ and save as .blend with camera & light")
parser.add_argument("--in", dest="infile", required=True, help="Input .obj path")
parser.add_argument("--out", dest="outfile", required=True, help="Output .blend path")
args = parser.parse_args(argv)

# -------------------------
# Reset scene
# -------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)

# -------------------------
# Import OBJ
# -------------------------
bpy.ops.import_scene.obj(filepath=args.infile)

# -------------------------
# Add Camera
# -------------------------
bpy.ops.object.camera_add(location=(0, -5, 3), rotation=(1.2, 0, 0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

# -------------------------
# Add Light
# -------------------------
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
light = bpy.context.active_object
light.data.energy = 5

# -------------------------
# Save .blend
# -------------------------
bpy.ops.wm.save_as_mainfile(filepath=args.outfile)

# -------------------------
# Render preview
# -------------------------
render_path = os.path.splitext(args.outfile)[0] + "_render.png"
bpy.context.scene.render.filepath = render_path
bpy.ops.render.render(write_still=True)

print(f"✅ Scene saved to {args.outfile}")
print(f"🖼️ Render saved to {render_path}")
