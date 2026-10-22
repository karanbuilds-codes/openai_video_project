"""
Optional Blender scene builder. Run with:
  blender -b --python blender_renderer.py
Creates output/blender_preview.blend with a procedural glowing node network.
The default full pipeline uses the portable Pillow renderer in scenes.py so it can
run on machines without Blender. This file is a real, reusable Blender starter scene.
"""
import bpy, math, random
from mathutils import Vector
from pathlib import Path
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="CYCLES"
scene.render.resolution_x=1920; scene.render.resolution_y=1080; scene.render.resolution_percentage=50
scene.render.fps=30
scene.world.color=(0.002,0.004,0.02)
def emission(name,color,strength):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Emission Color"].default_value=(*color,1)
    bs.inputs["Emission Strength"].default_value=strength
    return m
cyan=emission("Cyan emissive",(.01,.45,1),3.0)
white=emission("White emissive",(.4,.8,1),1.5)
random.seed(12); pts=[]
for i in range(90):
    p=Vector((random.uniform(-8,8),random.uniform(-4.5,4.5),random.uniform(-3,3)))
    pts.append(p)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=6,radius=random.uniform(.035,.09), location=p)
    obj=bpy.context.object; obj.name=f"Neuron_{i:03}"; obj.data.materials.append(cyan)
    obj.keyframe_insert(data_path="location",frame=1)
    obj.location.z += random.uniform(-.4,.4); obj.keyframe_insert(data_path="location",frame=150)
for i,p in enumerate(pts):
    near=sorted(((p-q).length,j,q) for j,q in enumerate(pts) if j!=i)[:2]
    for dist,j,q in near:
        curve=bpy.data.curves.new("SignalLink","CURVE"); curve.dimensions="3D"; curve.bevel_depth=.008; curve.bevel_resolution=2
        spl=curve.splines.new("POLY"); spl.points.add(1)
        spl.points[0].co=(*p,1); spl.points[1].co=(*q,1)
        ob=bpy.data.objects.new("NeuralLink",curve); bpy.context.collection.objects.link(ob); ob.data.materials.append(white)
bpy.ops.object.camera_add(location=(0,-1,22), rotation=(0,0,0))
cam=bpy.context.object; cam.data.lens=42; scene.camera=cam
cam.keyframe_insert(data_path="location",frame=1); cam.location=(0,0,14); cam.keyframe_insert(data_path="location",frame=150)
scene.frame_end=150
scene.render.filepath=str(Path(__file__).resolve().parent/"output"/"blender_preview")
scene.render.image_settings.file_format="PNG"
scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs[0].default_value=(.001,.003,.015,1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value=.15
out=Path(__file__).resolve().parent/"output"; out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/"blender_preview.blend"))
print("Saved procedural Blender neural-network scene.")
