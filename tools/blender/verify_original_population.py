"""Independent saved-file census, preservation and annotation roundtrip."""
from collections import Counter
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from populate_original import fingerprint
from original_map import xyz, register

project, out = map(Path,sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True,exist_ok=True)
saved=out/'annotation-check.blend'
if saved.exists():raise ValueError('Verification output must be fresh')
data=json.loads((project/'population.json').read_text())
receipt=json.loads((project/'population-check.json').read_text())
assert {name:fingerprint(bpy.data.objects[name]) for name in receipt['original_fingerprints']}==receipt['original_fingerprints']
objects=[o for o in bpy.data.objects if 'pc_population_role' in o]
placements=list(data['placements'])
expected=dict(grain=50,letter=4,spider=4,seed=4,**{'Mr. Soil':1})
if (project/'seed-tokens.json').exists():
    placements.extend(json.loads((project/'seed-tokens.json').read_text())['placements'])
    token_receipt=json.loads((project/'seed-token-check.json').read_text())
    assert {n:fingerprint(bpy.data.objects[n]) for n in token_receipt['original_fingerprints']}==token_receipt['original_fingerprints']
    receipt=token_receipt
if (project/'berry-pickups.json').exists():
    placements.extend(json.loads((project/'berry-pickups.json').read_text())['placements'])
    berry_receipt=json.loads((project/'berry-pickup-check.json').read_text())
    assert {n:fingerprint(bpy.data.objects[n]) for n in berry_receipt['original_fingerprints']}==berry_receipt['original_fingerprints']
    receipt=berry_receipt
if any(r['selector'] in (0x29,0x2a,0x2b) for r in placements):expected['seed-token']=2
if any(r['selector']==0x23 for r in placements):expected['blueberry']=2
if any(r['selector']==0x2c for r in placements):expected['berry-seed-token']=4
assert Counter(o['pc_population_role'] for o in objects)==expected
for row in placements:
    obj=next(o for o in objects if o.get('pc_source')==row['id'])
    assert max(abs(a-b) for a,b in zip(obj.location,xyz(row['position'])))<1e-5
    assert obj['pc_raw_hex']==row['raw_hex'] and obj['pc_initialized_hex']==row['initialized_hex']
for row in data['actors']:
    obj=next(o for o in objects if o.get('pc_source')==f'RAW actor slot {row["slot"]}')
    assert max(abs(a-b) for a,b in zip(obj.location,xyz(row['display_position'])))<1e-5
    assert obj['pc_raw_hex']==row['raw_hex']
soil=bpy.data.objects['Mr. Soil']
assert len(soil.data.vertices)==778 and len(soil.data.polygons)==207
assert sum(len(o.data.polygons) for o in bpy.data.collections['Collision surfaces'].objects)==1360
assert len(bpy.data.collections['Stored placements'].objects)==78
assert len([i for i in bpy.data.images if i.packed_file])==7  # Four scenery + three Soil; page29 supplies voxel RGB only.
register();bpy.ops.ablpc.map_top()
bpy.context.scene.cursor.location=(1,2,3);bpy.ops.ablpc.map_landmark(label='Population verification landmark')
bpy.context.active_object['mapping_note']='Population annotation survives reopen'
bpy.ops.wm.save_as_mainfile(filepath=str(saved));bpy.ops.wm.open_mainfile(filepath=str(saved))
assert bpy.data.objects['Population verification landmark']['mapping_note']=='Population annotation survives reopen'
# Unsaved inspection cameras do not change either deliverable or roundtrip file.
scene=bpy.context.scene;camera=scene.camera;scene.render.resolution_x=1000;scene.render.resolution_y=1000
for name,target,distance,scale in [('soil-closeup','Mr. Soil',(0,-8,4),4),
                                   ('exit-closeup','primary.117 [0x0049]',(0,-18,15),15)]:
    obj=bpy.data.objects.get(target)
    if obj is None and name.startswith('exit'):obj=next(o for o in bpy.data.objects if o.get('pc_source')=='primary.117')
    center=obj.matrix_world.translation+Vector((0,0,1))
    camera.location=center+Vector(distance);camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=scale;scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
report=dict(roles=dict(Counter(o['pc_population_role'] for o in bpy.data.objects if 'pc_population_role' in o)),
            original_objects_exact=len(receipt['original_fingerprints']),all_population_positions_verified=True,
            stored_markers=78,collision_triangles=1360,packed_textures=7,soil_vertices=778,soil_faces=207,
            annotation_add_save_reopen='passed',blender_version=bpy.app.version_string)
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
