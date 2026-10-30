"""Verify a saved private mapping scene and persist a landmark in a fresh copy."""
import json
from pathlib import Path
import sys

import bpy

project, output = map(Path, sys.argv[sys.argv.index('--')+1:])
if output.exists(): raise ValueError('Verification output must be fresh')
data = json.loads((project/'original-map.json').read_text())
checked_vertices = checked_uvs = 0
for source in data['objects']:
    obj = bpy.data.objects[source['id']+f' [0x{source["flags"]:04X}]']
    assert len(obj.data.vertices) == len(source['vertices'])
    assert len(obj.data.polygons) == len(source['faces'])
    for vertex, expected in zip(obj.data.vertices, source['vertices']):
        p = expected['position']; target = (p[0]/256,p[2]/256,-p[1]/256)
        assert max(abs(a-b) for a,b in zip(vertex.co,target)) < 1e-5
        checked_vertices += 1
    for polygon, face in zip(obj.data.polygons,source['faces']):
        assert list(polygon.vertices) == face['indices']
        assert obj.data.attributes['pc_face_tag'].data[polygon.index].value == face['tag']
        for loop, word in zip(polygon.loop_indices,face['uv']):
            actual = obj.data.uv_layers['PC UV'].data[loop].uv
            assert tuple(actual) == ((word & 255)/256,1-(word >> 8)/256)
            checked_uvs += 1
assert len([i for i in bpy.data.images if i.packed_file]) == 4
assert sum(len(o.data.polygons) for o in bpy.data.collections['Collision surfaces'].objects) == 1360
assert len(bpy.data.collections['Stored placements'].objects) == 78
sys.path.insert(0,str(Path(__file__).resolve().parent))
import original_map
original_map.register()
bpy.ops.ablpc.map_top()
bpy.context.scene.cursor.location = (1,2,3)
bpy.ops.ablpc.map_landmark(label='Verification landmark')
landmark = bpy.context.active_object
landmark['mapping_note'] = 'Saved annotation roundtrip'
assert tuple(landmark.location) == (1,2,3)
bpy.ops.wm.save_as_mainfile(filepath=str(output))
bpy.ops.wm.open_mainfile(filepath=str(output))
assert bpy.data.objects['Verification landmark']['mapping_note'] == 'Saved annotation roundtrip'
assert tuple(bpy.data.objects['Verification landmark'].location) == (1,2,3)
report = {'saved_scene_vertices_verified':checked_vertices,'saved_uv_corners_verified':checked_uvs,
          'collision_triangles_verified':1360,'packed_textures_verified':4,'placement_markers_verified':78,
          'landmark_add_save_reopen':'passed','blender_version':bpy.app.version_string}
output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
