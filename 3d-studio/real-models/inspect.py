import bpy,json,sys,os
from pathlib import Path
names=['plush','forest']
records={}
for nm in names:
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
 try:
  bpy.ops.import_scene.gltf(filepath='/tmp/models/'+nm+'.glb')
  objs=[o for o in bpy.context.scene.objects]
  meshes=[o for o in objs if o.type=='MESH']
  arm=[o for o in objs if o.type=='ARMATURE']
  actions=[a.name for a in bpy.data.actions]
  odata={'objects':len(objs),'meshes':len(meshes),'armatures':[(o.name,len(o.data.bones)) for o in arm], 'actions':actions,'animations':[(a.name,[float(x) for x in a.frame_range]) for a in bpy.data.actions],'bounds':[[*o.dimensions] for o in meshes[:5]], 'materials':[m.name for m in bpy.data.materials][:20],'names':[o.name for o in objs][:35]}
  records[nm]=odata
 except Exception as e:
  records[nm]={'error':str(e)}
print('MODEL_INSPECTION='+json.dumps(records,ensure_ascii=False),flush=True)
Path('outputs').mkdir(exist_ok=True)
Path('outputs/model_inventory.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
