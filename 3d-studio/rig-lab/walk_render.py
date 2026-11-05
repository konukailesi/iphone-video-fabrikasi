import bpy, math, os
from mathutils import Vector
s=bpy.context.scene
rig=bpy.data.objects.get('AnimationRig')
mesh=bpy.data.objects.get('ChickenMesh')
assert rig is not None and mesh is not None, 'Model iskeleti veya mesh bulunamadi'
walk=bpy.data.actions.get('walk')
assert walk is not None, 'walk animasyonu bulunamadi'
for ob in list(bpy.data.objects):
    if ob.name.startswith('WGT-') or ob.name=='metarig':
        ob.hide_render=True
        # hide_render works for objects in excluded collections; hide_set requires view layer membership
# Rig'i NLA ile tekrar et; adim animasyonu + gercek konum degisimi
if rig.animation_data is None: rig.animation_data_create()
rig.animation_data.action=None
for tr in list(rig.animation_data.nla_tracks):
    rig.animation_data.nla_tracks.remove(tr)
track=rig.animation_data.nla_tracks.new()
track.name='Gercek Yuruyus'
strip=track.strips.new('Walk cycle', 1, walk)
strip.repeat=5
strip.extrapolation='HOLD_FORWARD'
# Animasyonun oldugu armature hiyerarsisi hareket etsin
rig.location=(0,0,0)
for fr,x in [(1,-.55),(60,0),(120,.55)]:
    rig.location.x=x
    rig.keyframe_insert(data_path='location',frame=fr)
# Hafif acili kamera, zemin
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015))
ground=bpy.context.object;ground.name='Yer'
gm=bpy.data.materials.new('Pastel cimen');gm.diffuse_color=(.29,.74,.36,1)
ground.data.materials.append(gm)
for ob in bpy.data.objects:
    if ob.type=='MESH':
        ob.hide_render=ob.name.startswith('WGT-')
bpy.ops.object.camera_add(location=(0,-6.6,2.4))
cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,1.04))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=6.2;s.camera=cam
for m in mesh.data.materials:
    if m:
        print('ORIGINAL_MATERIAL',m.name,flush=True)
        mn=m.name.lower()
        if 'eye' in mn or 'pupil' in mn:
            m.diffuse_color=(.035,.06,.10,1)
        elif 'beak' in mn or 'feet' in mn or 'leg' in mn:
            m.diffuse_color=(1,.40,.06,1)
        elif 'comb' in mn:
            m.diffuse_color=(.97,.18,.16,1)
        else:
            m.diffuse_color=(1,.78,.18,1)
world=bpy.data.worlds[0] if len(bpy.data.worlds) else bpy.data.worlds.new('Pastel sky')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.40,.72,1,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
s.render.engine='BLENDER_WORKBENCH'
s.display.shading.light='STUDIO'
s.display.shading.color_type='MATERIAL'
s.display.shading.show_shadows=True
s.display.shading.show_cavity=True
s.display.shading.background_type='VIEWPORT'
s.display.shading.background_color=(.64,.82,1)
s.render.resolution_x=540
s.render.resolution_y=960
s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
s.render.fps=24
s.frame_start=1
s.frame_end=120
s.render.threads_mode='FIXED';s.render.threads=2
os.makedirs('/tmp/rigframes',exist_ok=True)
s.render.filepath='/tmp/rigframes/frame_'
print('RIG_WALK_RENDER_START',rig.name,walk.name,flush=True)
bpy.ops.render.render(animation=True)
