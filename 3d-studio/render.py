import bpy, math, os, random
from mathutils import Vector
random.seed(17)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.display.shading.light='STUDIO'
s.display.shading.color_type='MATERIAL'
s.display.shading.show_shadows=True
s.display.shading.show_cavity=True
s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=360;s.render.resolution_y=640
s.render.resolution_percentage=100;s.render.fps=12
s.render.image_settings.file_format='PNG'
s.frame_start=1;s.frame_end=144
s.view_settings.view_transform='Standard'
def mat(n,c,fuzz=False):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1)
 p.inputs['Roughness'].default_value=.65
 if fuzz:
  t=m.node_tree.nodes.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=90
  b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.16;b.inputs['Distance'].default_value=.025
  m.node_tree.links.new(t.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
blue=mat('mavi tuy',(.25,.55,.97),True); pale=mat('acik mavi',(.85,.95,1),True)
yellow=mat('sari tuy',(1,.75,.06),True);cream=mat('acik sari',(1,.91,.28),True)
pink=mat('pembe',(.98,.55,.7));orange=mat('turuncu',(1,.35,.04));eye=mat('goz',(.015,.03,.08))
white=mat('beyaz',(1,1,1));red=mat('balon kirmizi',(1,.05,.12));green=mat('cimen',(.24,.61,.23));brown=mat('agac',(.43,.22,.09));darkgreen=mat('yaprak',(.09,.39,.16))
def ball(n,xyz,scale,material,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=xyz)
 o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 if parent:o.parent=parent
 return o
def empty(n,pos):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=pos;return o
def rig(name,x,bodycolor,facecolor,chick=False):
 root=empty(name,(x,0,.08))
 ball(name+' govde',(0,0,.9),(.48,.4,.62),bodycolor,root)
 ball(name+' gogus',(0,-.34,.93),(.31,.1,.42),facecolor,root)
 head=1.66 if chick else 1.9
 ball(name+' kafa',(0,-.04,head),(.51,.47,.49),facecolor if chick else bodycolor,root)
 for side in (-1,1):
  ball('goz beyazi',(.22*side,-.455,head+.05),(.16,.09,.18),white,root)
  ball('goz pupili',(.22*side,-.525,head+.05),(.095,.04,.12),eye,root)
  ball('ayak',(.29*side,-.15,.20),(.20,.25,.14),orange if chick else pale,root)
  if not chick:
   ball('uzun kulak',(.29*side,0,2.61),(.16,.14,.53),bodycolor,root)
   ball('kulak ici',(.29*side,-.13,2.61),(.10,.035,.39),pink,root)
 if chick:
  ball('gaga',(0,-.54,head-.11),(.19,.18,.11),orange,root)
  for i in range(3):ball('tepe tuyu',((i-1)*.12,-.04,2.1),(.08,.09,.22),facecolor,root)
 else:
  ball('yanak sol',(-.28,-.42,1.75),(.25,.12,.19),pale,root)
  ball('yanak sag',(.28,-.42,1.75),(.25,.12,.19),pale,root)
  ball('burun',(0,-.57,1.8),(.11,.08,.08),pink,root)
 limbs=[]
 for side in (-1,1):
  arm=empty(name+' kol',(side*.41,0,1.30));arm.parent=root
  ball('hareketli kol',(side*.50,-.12,1.05),(.20,.2,.33),bodycolor,arm)
  limbs.append(arm)
 return root,limbs
rabbit,arms=rig('Mavi Tavsan',-2.1,blue,pale)
chick,wings=rig('Sari Civciv',2.1,yellow,cream,True)
# dekor
ball('yesil zemin',(0,0,-.35),(20,20,.25),green)
for x in (-3.5,3.5):
 ball('agac tac',(x,2.5,2.35),(1,1,1),darkgreen)
 ball('agac govde',(x,2.5,.95),(.17,.17,1.13),brown)
for i in range(24):
 x=random.uniform(-3.6,3.6);y=random.uniform(.25,3.5)
 if abs(x)<1.7:continue
 ball('kucuk cicek',(x,y,.13),(.10,.10,.12),pink if i%2 else cream)
balloon=empty('Balon', (1.30,.2,2.85))
ball('Kirmizi ucusan balon',(0,0,0),(.35,.30,.45),red,balloon)
ball('Balon dugum',(0,0,-.47),(.06,.06,.07),red,balloon)
# ip curve
cv=bpy.data.curves.new('ip','CURVE');cv.dimensions='3D';cv.bevel_depth=.008;cv.bevel_resolution=2
sp=cv.splines.new('POLY');sp.points.add(5)
for i,p in enumerate(sp.points):p.co=(math.sin(i*.7)*.025,0,-.52-i*.15,1)
ob=bpy.data.objects.new('Balon ipi',cv);bpy.context.collection.objects.link(ob);ob.parent=balloon
def key(o,f,loc=None,rot=None):
 if loc is not None:o.location=loc;o.keyframe_insert(data_path='location',frame=f)
 if rot is not None:o.rotation_euler=rot;o.keyframe_insert(data_path='rotation_euler',frame=f)
for f,x,z in [(1,-2.2,.05),(24,-1.8,.14),(48,-1.15,.05),(72,-1.0,.10),(90,-.78,.5),(105,-.7,.06),(120,-.7,.43),(144,-.7,.06)]:
 key(rabbit,f,(x,-.12,z))
for f,x,z in [(1,2.4,.05),(24,2.1,.24),(48,1.53,.05),(72,1.35,.3),(90,1.35,.05),(108,1.3,.3),(120,1.3,.05),(132,1.3,.28),(144,1.3,.05)]:
 key(chick,f,(x,-.12,z))
for f,ang in [(1,0),(48,.1),(70,-.25),(92,-.85),(103,-.12),(122,-.65),(144,0)]:
 for a in arms:key(a,f,rot=(0,ang,0))
for f,ang in [(1,0),(24,.35),(48,-.22),(72,.45),(96,-.3),(120,.35),(144,0)]:
 for w in wings:key(w,f,rot=(0,ang,0))
for f in (1,36,72,108,144):
 key(balloon,f,(1.30-.17*(f/144),.2,2.85+.12*math.sin(f*.08)))
# kamera
bpy.ops.object.camera_add(location=(0,-13,4.5))
cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,1.45))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=5.8;s.camera=cam
for f,dist in [(1,-13),(144,-12.3)]:key(cam,f,(0,dist,4.5))
world=bpy.data.worlds[0];world.use_nodes=True
world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.40,.7,1,1)
world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.9
def lamp(x,y,z,power):
 bpy.ops.object.light_add(type='AREA',location=(x,y,z))
 o=bpy.context.object;o.data.energy=power;o.data.size=6
 o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
lamp(-4,-4,7,900);lamp(4,-2,5,600)
os.makedirs('/tmp/frames',exist_ok=True)
if os.getenv('PREVIEW_ONLY')=='1':
 s.frame_set(72);s.render.filepath='/tmp/preview.png';bpy.ops.render.render(write_still=True)
else:
 s.render.filepath='/tmp/frames/frame_';bpy.ops.render.render(animation=True)
