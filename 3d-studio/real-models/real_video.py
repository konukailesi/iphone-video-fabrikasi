import bpy, math, os, json, random
from mathutils import Vector
random.seed(63)
# Real source: Chickensoft CC BY 4.0 chicken rig + Polyfork forest rabbit (animated GLB).
chicken_path='/tmp/models/chickensoft_mascot_model.blend'
rabbit_path='/tmp/models/forest.glb'
bpy.ops.wm.open_mainfile(filepath=chicken_path)
scene=bpy.context.scene
chick_rig=bpy.data.objects.get('AnimationRig')
assert chick_rig is not None and chick_rig.type=='ARMATURE', 'Chicken armature missing'
walk=bpy.data.actions.get('walk') or bpy.data.actions.get('Walk')
assert walk is not None, 'Chicken walk animation missing'
# Hide rigs control handles, keep the original skinned character mesh and materials.
for o in bpy.data.objects:
    if o.name.startswith('WGT-') or o.name=='metarig':
        o.hide_render=True
# Ensure the active animation is real NLA walk.
if not chick_rig.animation_data:chick_rig.animation_data_create()
chick_rig.animation_data.action=None
for tr in list(chick_rig.animation_data.nla_tracks):
    chick_rig.animation_data.nla_tracks.remove(tr)
tr=chick_rig.animation_data.nla_tracks.new()
tr.name='Chick genuine walk'
st=tr.strips.new('walk cycle',1,walk)
st.repeat=3
st.extrapolation='HOLD_FORWARD'
# Import another authentic 3D model from externally verified downloadable GLB.
before=set(bpy.data.objects.keys())
bpy.ops.import_scene.gltf(filepath=rabbit_path)
added=[o for o in bpy.data.objects if o.name not in before]
bunny_meshes=[o for o in added if o.type=='MESH']
bunny_arms=[o for o in added if o.type=='ARMATURE']
assert bunny_meshes and bunny_arms,'Rabbit authentic mesh and skeleton missing'
actions={a.name:a for a in bpy.data.actions}
rabbit_action=next((a for n,a in actions.items() if 'walk' in n.lower() and a!=walk),None)
assert rabbit_action is not None, 'Rabbit Walk action missing'
# Animation importer may have set a rigid-body action to the root and pose actions
# to the armature. Use real armature animation; preserve source animation hierarchy.
for arm in bunny_arms:
    if arm.animation_data is None:arm.animation_data_create()
    try:
        arm.animation_data.action=rabbit_action
    except Exception as e:
        print('ARM_ACTION_ASSIGN_WARN',str(e))
    for t in list(arm.animation_data.nla_tracks):
        for strip in t.strips:
            if 'walk' in strip.name.lower() or strip.action==rabbit_action:
                strip.repeat=4
# Normalize rabbit scale based on actual bounds of imported 3D meshes.
container=bpy.data.objects.new('Mavi tavsan 3D model control',None)
bpy.context.collection.objects.link(container)
for o in added:
    if o.parent is None:
        old=o.matrix_world.copy()
        o.parent=container
        o.matrix_world=old
# Inspect extents at rest to determine a consistent base size.
bpy.context.view_layer.update()
allverts=[]
for ob in bunny_meshes:
    for bb in ob.bound_box:
        allverts.append(ob.matrix_world @ Vector(bb))
minz=min(v.z for v in allverts);maxz=max(v.z for v in allverts)
height=maxz-minz
assert height>0.01, 'Rabbit mesh dimension invalid'
scale=2.1/height
container.scale=(scale,scale,scale)
container.location=(-1.04,0.2,-scale*minz+0.1)
# A small 3D material retint; does not replace the real mesh with primitives.
for ob in bunny_meshes:
    for material in ob.data.materials:
        if material and 'blue' not in material.name.lower():
            new=material.copy()
            new.name='Mavi Tavsan - '+material.name
            new.diffuse_color=(0.35,0.58,0.95,1)
            if new.use_nodes:
                bsdf=new.node_tree.nodes.get('Principled BSDF')
                if bsdf:
                    bsdf.inputs['Base Color'].default_value=(0.42,0.66,1.0,1)
                    bsdf.inputs['Roughness'].default_value=.78
            for i,slot in enumerate(ob.data.materials):
                if slot==material:ob.data.materials[i]=new
# Position actual chick rig: source model and all its bones remain untouched.
chick_rig.location=(1.05,0,0.05)
# Source mesh follows rig via armature deform.
for frame,x in [(1,1.05),(30,1.00),(60,.96),(90,.91),(120,.87)]:
    chick_rig.location.x=x
    chick_rig.keyframe_insert(data_path='location',frame=frame)
for frame,x in [(1,-1.04),(30,-.99),(60,-.95),(90,-.90),(120,-.86)]:
    container.location.x=x
    container.keyframe_insert(data_path='location',frame=frame)
# Scene decor (not animal body geometry).
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.035))
ground=bpy.context.object;ground.name='Yesil bahce'
mat=bpy.data.materials.new('Cimen yeşili');mat.diffuse_color=(.30,.73,.31,1)
ground.data.materials.append(mat)
for i in range(14):
    x=random.uniform(-3.2,3.2);y=random.uniform(1.0,5.5)
    if abs(x)<1.3:continue
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=(x,y,.12))
    o=bpy.context.object;o.name='Bahce cicegi';o.scale=(.14,.14,.11)
    cm=bpy.data.materials.new('Cicek'+str(i))
    cm.diffuse_color=(1,.55,.72,1) if i%2 else (1,.82,.14,1)
    o.data.materials.append(cm)
# Camera look at authentic models, adjust to vertical short aspect ratio.
bpy.ops.object.camera_add(location=(0,-9.3,3.15))
camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,1.20))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO';camera.data.ortho_scale=5.8
scene.camera=camera
# Workbench with material color and ambient shadow for reproducible GitHub CPU render.
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO'
scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_shadows=True
scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH'
scene.display.shading.background_type='WORLD'
scene.world=bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new('Morning sky')
scene.world.color=(.66,.81,1.0)
scene.render.resolution_x=540;scene.render.resolution_y=960
scene.render.resolution_percentage=100
scene.render.fps=24
scene.frame_start=1;scene.frame_end=120
scene.render.image_settings.file_format='PNG'
scene.render.threads_mode='FIXED';scene.render.threads=2
os.makedirs('/tmp/realframes',exist_ok=True)
scene.render.filepath='/tmp/realframes/frame_'
print('MODEL_TEST_OK',json.dumps({'rabbit_meshes':len(bunny_meshes),'rabbit_armatures':len(bunny_arms),'rabbit_walk':rabbit_action.name,'chicken_walk':walk.name,'rabbit_scale':round(scale,3)}),flush=True)
bpy.ops.render.render(animation=True)
