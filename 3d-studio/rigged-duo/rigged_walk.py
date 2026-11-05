# Minik Kasifler 3D Rig Walk - open and procedural, Blender 4
import bpy, math, os, random
from mathutils import Vector
random.seed(39)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO';sc.display.shading.color_type='MATERIAL'
sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True
sc.display.shading.cavity_type='BOTH';sc.display.shading.curvature_ridge_factor=1.2
sc.render.resolution_x=540;sc.render.resolution_y=960
sc.render.resolution_percentage=100;sc.render.fps=24;sc.frame_start=1;sc.frame_end=120
sc.render.image_settings.file_format='PNG';sc.render.threads_mode='FIXED';sc.render.threads=2
sc.world.color=(.52,.73,.95)
sc.display.shading.background_type='WORLD'

def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
mb=material('mavi tavsan tuy',(.30,.59,.91))
bl=material('acik tuy',(.88,.94,1))
pk=material('kulak pembe',(1,.55,.68))
yw=material('sari civciv tuy',(1,.76,.085))
yc=material('acik civciv tuy',(1,.91,.39))
orng=material('ayak ve gaga',(1,.40,.065))
eye=material('buyuk koyu goz',(.035,.08,.17))
wh=material('goz beyazi',(1,1,1))
red=material('kirmizi aksesuar',(.9,.06,.12))
green=material('cimen',(.29,.68,.29))
gold=material('parlak balon',(1,.15,.27))
brown=material('yol',(.82,.59,.36))

def mesh_ball(name,pos,size,mat,bone=None,rig=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=pos)
 ob=bpy.context.object;ob.name=name;ob.scale=size;ob.data.materials.append(mat)
 bpy.ops.object.transform_apply(location=True,rotation=False,scale=True)
 for poly in ob.data.polygons:poly.use_smooth=True
 if bone:
  vg=ob.vertex_groups.new(name=bone);vg.add(list(range(len(ob.data.vertices))),1.0,'REPLACE')
  ob.parent=rig
  ob.matrix_parent_inverse.identity()
  mod=ob.modifiers.new('Real armature deform','ARMATURE');mod.object=rig
 return ob

def make_rig(name,pos,chick=False):
 ar=bpy.data.armatures.new(name+' Armature');rig=bpy.data.objects.new(name+' rig',ar);bpy.context.collection.objects.link(rig)
 bpy.context.view_layer.objects.active=rig;rig.select_set(True)
 bpy.ops.object.mode_set(mode='EDIT')
 E=ar.edit_bones
 def b(n,head,tail,parent=None):
  x=E.new(n);x.head=head;x.tail=tail
  if parent:x.parent=E[parent]
  return x
 b('root',(0,0,.18),(0,0,.42))
 b('pelvis',(0,0,.42),(0,0,.81),'root')
 b('spine',(0,0,.81),(0,0,1.42),'pelvis')
 b('neck',(0,0,1.42),(0,0,1.55),'spine')
 b('head',(0,0,1.55),(0,0,2.09),'neck')
 for side in ['L','R']:
  sg=-1 if side=='L' else 1
  b('thigh.'+side,(.29*sg,0,.61),(.30*sg,0,.36),'pelvis')
  b('shin.'+side,(.30*sg,0,.36),(.31*sg,0,.17),'thigh.'+side)
  b('foot.'+side,(.31*sg,0,.17),(.31*sg,-.25,.14),'shin.'+side)
  b('upperarm.'+side,(.39*sg,0,1.35),(.57*sg,0,1.13),'spine')
  b('forearm.'+side,(.57*sg,0,1.13),(.57*sg,-.08,.92),'upperarm.'+side)
  if not chick:b('ear.'+side,(.29*sg,0,2.04),(.30*sg,0,2.65),'head')
 bpy.ops.object.mode_set(mode='OBJECT')
 rig.location=pos
 body_mat=yw if chick else mb
 head_mat=yc if chick else mb
 prefix='Sari Civciv' if chick else 'Mavi Tavsan'
 mesh_ball(prefix+' govde',(0,0,.97),(.47,.36,.61),body_mat,'spine',rig)
 mesh_ball(prefix+' karin',(0,-.30,.95),(.32,.10,.41),yc if chick else bl,'spine',rig)
 mesh_ball(prefix+' kafa',(0,-.02,1.79),(.53,.44,.50),head_mat,'head',rig)
 for side in ['L','R']:
  sg=-1 if side=='L' else 1
  mesh_ball('goz beyazi',(.23*sg,-.41,1.88),(.17,.12,.19),wh,'head',rig)
  mesh_ball('goz pupili',(.23*sg,-.518,1.87),(.106,.047,.128),eye,'head',rig)
  mesh_ball('goz pariltisi',(.23*sg-.03,-.558,1.92),(.04,.015,.04),wh,'head',rig)
  mesh_ball('ust bacak',(.30*sg,-.02,.47),(.17,.19,.27),body_mat,'thigh.'+side,rig)
  mesh_ball('alt bacak',(.31*sg,-.02,.23),(.16,.16,.23),body_mat,'shin.'+side,rig)
  mesh_ball('ayak',(.31*sg,-.24,.13),(.23,.33,.13),orng if chick else bl,'foot.'+side,rig)
  mesh_ball('kol',(.50*sg,-.01,1.22),(.19,.20,.26),body_mat,'upperarm.'+side,rig)
  mesh_ball('pati kanat',(.57*sg,-.10,1.02),(.19,.19,.23),body_mat,'forearm.'+side,rig)
  if not chick:
   mesh_ball('uzun kulak',(.30*sg,0,2.43),(.15,.12,.50),mb,'ear.'+side,rig)
   mesh_ball('pembe kulak',(.30*sg,-.115,2.43),(.093,.036,.38),pk,'ear.'+side,rig)
  # stylize fur along cheeks and torso
  for j in range(9):
   theta=j*2*math.pi/9
   mat=body_mat
   mesh_ball('minik tuy parcasi',(.38*math.cos(theta),.28*math.sin(theta),1.0+.11*math.sin(j)),(.095,.08,.15),mat,'spine',rig)
 if chick:
  mesh_ball('civciv gaga',(0,-.48,1.67),(.19,.20,.12),orng,'head',rig)
  for j in range(3):
   mesh_ball('tepe tuy',((j-1)*.14,-.03,2.25),(.08,.11,.22),yc,'head',rig)
  # red spotted bandana at chest
  mesh_ball('kirmizi bandana',(0,-.37,1.25),(.30,.07,.15),red,'spine',rig)
  for a,b in [(-.13,1.23),(.06,1.27),(.18,1.21)]:
   mesh_ball('beyaz benek',(a,-.43,b),(.035,.024,.035),wh,'spine',rig)
 else:
  mesh_ball('burun',(0,-.51,1.72),(.12,.065,.08),pk,'head',rig)
  mesh_ball('sol yanak',(-.28,-.36,1.71),(.22,.15,.16),bl,'head',rig)
  mesh_ball('sag yanak',(.28,-.36,1.71),(.22,.15,.16),bl,'head',rig)
  mesh_ball('kirmizi sirt cantasi',(0,.38,1.13),(.37,.20,.45),red,'spine',rig)
 return rig

rab=make_rig('Mavi Tavsan',(-1.18,0,0),False)
chi=make_rig('Sari Civciv',(1.08,0,0),True)
# Ground / garden: no external assets
mesh_ball('Yesil bahce zemini',(0,0,-.18),(16,16,.20),green)
mesh_ball('Toprak patika',(0,-.9,-.06),(3.0,1.20,.05),brown)
for x in (-2.7,2.7):
 mesh_ball('Yumusak calilar',(x,2.8,.45),(.65,.65,.57),green)
for i in range(20):
 x=random.uniform(-2.7,2.7); y=random.uniform(1.4,4)
 mesh_ball('Bahce cicegi',(x,y,.1),(.09,.09,.13),pk if i%2 else yc)
# Rig animation: real pose bones rotate at hip knee ankle shoulder elbow
def animate(rig,phaseoffset=0,speed=.014):
 for f in range(1,121,2):
  t=(f-1)/24.0
  cycle=t*2*math.pi*1.65+phaseoffset
  # actual world displacement proportional to number of steps
  rig.location=(rig.location.x if f==1 else 0,0,0) if False else rig.location
  # pelvis sways up and down, not full body sliding in isolation
  base_x=-1.18 if rig==rab else 1.08
  tx=base_x + speed*(f-1)
  rig.location=(tx,0,.055+max(0,.095*math.sin(2*cycle)))
  rig.keyframe_insert('location',frame=f)
  for side in ('L','R'):
   p=cycle+(math.pi if side=='R' else 0)
   thigh=rig.pose.bones['thigh.'+side]
   shin=rig.pose.bones['shin.'+side]
   foot=rig.pose.bones['foot.'+side]
   upper=rig.pose.bones['upperarm.'+side]
   lower=rig.pose.bones['forearm.'+side]
   for bone in (thigh,shin,foot,upper,lower):
    bone.rotation_mode='XYZ'
   thigh.rotation_euler=(.56*math.sin(p),0,.055*math.sin(p))
   shin.rotation_euler=(-.20-0.7*max(0,math.sin(p)),0,0)
   foot.rotation_euler=(.24*math.sin(p)+.23*max(0,math.sin(p)),0,0)
   upper.rotation_euler=(-.42*math.sin(p),0,0)
   lower.rotation_euler=(.15*math.sin(p)+.1,0,0)
   for bone in (thigh,shin,foot,upper,lower):bone.keyframe_insert('rotation_euler',frame=f)
  head=rig.pose.bones['head'];head.rotation_mode='XYZ'
  head.rotation_euler=(.03*math.sin(cycle*2),.04*math.sin(cycle),.04*math.sin(cycle))
  head.keyframe_insert('rotation_euler',frame=f)
  if rig==rab:
   for side in ('L','R'):
    e=rig.pose.bones['ear.'+side];e.rotation_mode='XYZ'
    e.rotation_euler=(.08*math.sin(cycle*2+(.5 if side=='L' else 0)),0,0)
    e.keyframe_insert('rotation_euler',frame=f)
animate(rab,.5,.0025)
animate(chi,2.2,.0025)
# Camera
bpy.ops.object.camera_add(location=(0,-11.5,3.4));cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,1.48))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=6.8;sc.camera=cam
os.makedirs('/tmp/rigged_duo_frames',exist_ok=True)
sc.render.filepath='/tmp/rigged_duo_frames/frame_'
print('RIGS',rab.name,chi.name,'BONES',len(rab.data.bones),len(chi.data.bones),flush=True)
bpy.ops.render.render(animation=True)
