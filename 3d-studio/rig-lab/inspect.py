import bpy,json,os
out='/tmp/model_info.json'
data={
 'blender_version':bpy.app.version_string,
 'objects':[{'name':o.name,'type':o.type,'dimensions':list(o.dimensions),'location':list(o.location)} for o in bpy.data.objects],
 'actions':[{'name':a.name,'frame_range':[float(x) for x in a.frame_range]} for a in bpy.data.actions],
 'scenes':[s.name for s in bpy.data.scenes],
 'armatures':[{'name':o.name,'bones':[b.name for b in o.data.bones]} for o in bpy.data.objects if o.type=='ARMATURE'],
}
with open(out,'w') as f:json.dump(data,f,indent=2)
print('MODEL_REPORT='+json.dumps({'objects':len(data['objects']),'actions':len(data['actions']),'armatures':len(data['armatures'])}))
