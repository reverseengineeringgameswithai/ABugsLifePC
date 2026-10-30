"""Blender reference-scene presentation; deliberately separate from mod Build."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
from bpy.props import StringProperty
from mathutils import Vector, Quaternion

LAYERS = ('Original scenery', 'Secondary scene', 'Collision surfaces', 'XZ barriers', 'Stored placements', 'Landmarks', 'Distant source objects')
POPULATION_LAYERS = ('Grain (50)', 'FLIK letters (4)', 'Seed tokens', 'Blueberries', 'Berry seed tokens', 'Distant pickups', 'Spiders (4)', 'Mr. Soil', 'Seeds (4)', 'Level ending marker', 'Map labels')


def xyz(p):
    return (p[0]/256, p[2]/256, -p[1]/256)


def link(name, data, layer):
    obj = bpy.data.objects.new(name, data)
    bpy.data.collections[layer].objects.link(obj)
    return obj


def mesh(name, vertices, faces=(), edges=()):
    data = bpy.data.meshes.new(name)
    data.from_pydata([xyz(p) for p in vertices], edges, faces); data.update()
    return data


def material(tag, images):
    name = f'PC page {(tag >> 8) & 31:02d} tag {tag:04X}'
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links; nodes.clear()
    tex = nodes.new('ShaderNodeTexImage'); tex.image = images[(tag >> 8) & 31]
    tex.interpolation = 'Closest'; tex.extension = 'EXTEND'
    color = nodes.new('ShaderNodeVertexColor'); color.layer_name = 'PC vertex RGB'
    multiply = nodes.new('ShaderNodeMixRGB'); multiply.blend_type = 'MULTIPLY'; multiply.inputs[0].default_value = 1
    links.new(tex.outputs['Color'], multiply.inputs[1]); links.new(color.outputs['Color'], multiply.inputs[2])
    emission = nodes.new('ShaderNodeEmission'); emission.inputs['Strength'].default_value = 2
    links.new(multiply.outputs[0], emission.inputs['Color'])
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    mix = nodes.new('ShaderNodeMixShader'); links.new(tex.outputs['Alpha'], mix.inputs[0])
    links.new(transparent.outputs[0], mix.inputs[1]); links.new(emission.outputs[0], mix.inputs[2])
    output = nodes.new('ShaderNodeOutputMaterial'); links.new(mix.outputs[0], output.inputs[0])
    mat['pc_tag'] = tag; mat['preview'] = 'Original textures and vertex colours; approximate brightness'
    return mat


def frame_level(context, top=False):
    low = Vector(context.scene['pc_map_bounds_min'])
    high = Vector(context.scene['pc_map_bounds_max'])
    center = (low+high)/2
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != 'VIEW_3D': continue
            space = area.spaces.active; space.clip_end = 3000
            space.region_3d.view_location = center
            space.region_3d.view_distance = max(high-low)*1.1
            space.region_3d.view_rotation = Quaternion((1,0,0,0)) if top else Quaternion((0.8805,0.3647,0.1159,0.2798)).normalized()
            space.region_3d.view_perspective = 'ORTHO'


def register():
    for cls in (ABLPC_OT_map_frame, ABLPC_OT_map_top, ABLPC_OT_landmark, ABLPC_PT_map):
        bpy.utils.register_class(cls)


class ABLPC_OT_map_frame(bpy.types.Operator):
    bl_idname = 'ablpc.map_frame'; bl_label = 'Frame level'
    def execute(self, context):
        frame_level(context); return {'FINISHED'}


class ABLPC_OT_map_top(bpy.types.Operator):
    bl_idname = 'ablpc.map_top'; bl_label = 'Top view'
    def execute(self, context):
        frame_level(context, True); return {'FINISHED'}


class ABLPC_OT_landmark(bpy.types.Operator):
    bl_idname = 'ablpc.map_landmark'; bl_label = 'Add named landmark at cursor'; bl_options = {'REGISTER','UNDO'}
    label: StringProperty(name='Name', default='Landmark')
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def execute(self, context):
        obj = link(self.label, None, 'Landmarks')
        obj.empty_display_type = 'ARROWS'; obj.empty_display_size = 1
        obj.location = context.scene.cursor.location; obj.show_name = True; obj.show_in_front = True
        obj['mapping_note'] = ''; bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
        context.view_layer.objects.active = obj
        return {'FINISHED'}


class ABLPC_PT_map(bpy.types.Panel):
    bl_label = 'Original PC map'; bl_idname = 'ABLPC_PT_original_map'
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = 'ABLPC Map'
    @classmethod
    def poll(cls, context):
        return context.scene.get('ablpc_original_map', False)
    def draw(self, context):
        layout = self.layout
        layout.label(text=context.scene.get('pc_map_name','LEVEL00 — Training'))
        row = layout.row(); row.operator('ablpc.map_frame'); row.operator('ablpc.map_top')
        # Complete maps (EXP-20260927-001) declare their own layer list.
        declared = context.scene.get('pc_map_layers')
        for layer in (declared.split('\n') if declared else (*POPULATION_LAYERS, *LAYERS)):
            if layer in bpy.data.collections:
                layout.prop(bpy.data.collections[layer], 'hide_viewport', text='Hide '+layer)
        layout.operator('ablpc.map_landmark')
        obj = context.active_object
        if obj:
            box = layout.box(); box.label(text=obj.name)
            p = obj.matrix_world.translation
            box.label(text=f'PC stored X {p.x*256:.1f}')
            box.label(text=f'Y {-p.z*256:.1f}  Z {p.y*256:.1f}')
            for key in ('pc_record_offset', 'pc_object_offset', 'pc_geometry_offset', 'pc_source'):
                if key in obj: box.label(text=f'{key[3:]}: {obj[key]}')
            if 'mapping_note' in obj: box.prop(obj, '["mapping_note"]', text='Note')
        layout.label(text='Reference scene • save notes with Ctrl+S')


def create(project, final):
    if (project/'population.json').exists():
        raise ValueError('Populated mapping scene must not be rebuilt as an empty base import')
    report_path = project/'import-report.json'
    report = json.loads(report_path.read_text())
    saved = project/'level.blend'
    if saved.exists() and hashlib.sha256(saved.read_bytes()).hexdigest() != report.get('blend_sha256'):
        raise ValueError('Saved mapping project has changed; preserve user edits')
    data = json.loads((project/'original-map.json').read_text())
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    context = bpy.context.scene; context['ablpc_original_map'] = True
    context['pc_map_name'] = data['name']
    context['ablpc_map_project'] = str(final); context['pc_coordinate_conversion'] = data['coordinate_system']['blender_xyz']
    for layer in LAYERS:
        context.collection.children.link(bpy.data.collections.new(layer))
    ground_points = [xyz(v) for group in data['collision'] for cell in group['cells'] for v in cell['vertices_stored']]
    low = Vector(tuple(min(p[k] for p in ground_points) for k in range(3)))
    high = Vector(tuple(max(p[k] for p in ground_points) for k in range(3)))
    context['pc_map_bounds_min'] = list(low); context['pc_map_bounds_max'] = list(high)
    images = {}
    for page in data['textures']:
        image = bpy.data.images.load(str(project/'textures'/f'page-{page["page"]:02d}.png'))
        image.pack(); image.filepath = f'//textures/page-{page["page"]:02d}.png'
        images[page['page']] = image
    for source in data['objects']:
        label = source['id']+f' [0x{source["flags"]:04X}]'
        m = mesh(label, [v['position'] for v in source['vertices']], [f['indices'] for f in source['faces']])
        world_points = [xyz([v['position'][k]+source['origin'][k] for k in range(3)]) for v in source['vertices']]
        outside = any(max(p[k] for p in world_points) < low[k]-1 or min(p[k] for p in world_points) > high[k]+1 for k in (0,1))
        layer = 'Secondary scene' if source['section'] == 'secondary' else ('Distant source objects' if outside else 'Original scenery')
        obj = link(label, m, layer); obj.location = xyz(source['origin'])
        obj['mapping_note'] = ''
        for field in ('record_offset','object_offset','geometry_offset'):
            obj['pc_'+field] = f'0x{source[field]:X}'
        obj['pc_source'] = source['id']; obj['pc_stored_origin'] = source['origin']
        obj['pc_angles'] = source['angles']; obj['pc_scale'] = source['scale']
        obj['pc_animation_selector'] = source['animation_selector']; obj['pc_object_hex'] = source['object_hex']
        uv = m.uv_layers.new(name='PC UV')
        colors = m.color_attributes.new(name='PC vertex RGB', type='FLOAT_COLOR', domain='POINT')
        for target, v in zip(colors.data, source['vertices']):
            target.color_srgb = (*[c/255 for c in v['rgb']], 1)
        # Preserve every source face tag, even when multiple tags use one page.
        tags = list(dict.fromkeys(f['tag'] for f in source['faces']))
        for tag in tags: m.materials.append(material(tag, images))
        attr = m.attributes.new(name='pc_face_tag', type='INT', domain='FACE')
        for polygon, face in zip(m.polygons, source['faces']):
            polygon.material_index = tags.index(face['tag']); attr.data[polygon.index].value = face['tag']
            for loop, word in zip(polygon.loop_indices, face['uv']):
                uv.data[loop].uv = ((word & 255)/256, 1-(word >> 8)/256)
    for group in data['collision']:
        cells = group['cells']; points = [v for cell in cells for v in cell['vertices_stored']]
        m = mesh(f'Collision {group["source"]:03d}', points, [(i*3,i*3+1,i*3+2) for i in range(len(cells))])
        obj = link(m.name,m,'Collision surfaces'); obj.display_type = 'WIRE'; obj.show_in_front = True
        obj.color = (0.1,0.9,1,1); obj['pc_source'] = group['source']; obj['mapping_note'] = ''
        a = m.attributes.new(name='pc_cell_offset', type='INT', domain='FACE')
        for p,c in zip(a.data,cells): p.value = c['file_offset']
    for barrier in data['barriers']:
        points = [(x,barrier['display_y'],z) for x,z in barrier['points_xz']]
        m = mesh(f'XZ barrier {barrier["source"]}',points,edges=[(i,i+1) for i in range(len(points)-1)])
        obj = link(m.name,m,'XZ barriers'); obj.show_in_front = True
        obj['mapping_note'] = barrier['note']; obj['pc_source'] = barrier['source']
    for row in data['placements']:
        obj = link(row['label']+' • '+row['id'],None,'Stored placements')
        obj.empty_display_type = 'SPHERE'; obj.empty_display_size = .35
        obj.location = xyz(row['position']); obj.show_in_front = True
        obj['pc_source'] = row['id']; obj['pc_record_offset'] = f'0x{row["offset"]:X}'
        obj['pc_raw_hex'] = row['raw_hex']; obj['mapping_note'] = row['note']
    for layer in (*LAYERS[1:5], 'Distant source objects'):
        bpy.data.collections[layer].hide_viewport = True
        bpy.data.collections[layer].hide_render = True
    text = bpy.data.texts.new(data['name']+' - Read me'); text.write((project/'README.md').read_text())
    context.render.engine = 'CYCLES'; context.cycles.samples = 16
    context.view_settings.view_transform = 'Standard'
    context.world.color = (.10,.10,.10)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active; space.shading.type = 'MATERIAL'
                space.overlay.show_floor = False; space.overlay.show_axis_x = False; space.overlay.show_axis_y = False
                space.show_region_ui = True
    context.view_layers[0].update()
    # Include the visible rim outside the collision envelope, after separating
    # distant records. This keeps the entire bowl in the saved overview.
    points = [o.matrix_world @ Vector(c) for o in bpy.data.collections[LAYERS[0]].objects for c in o.bound_box]
    low = Vector(tuple(min(p[k] for p in points) for k in range(3)))
    high = Vector(tuple(max(p[k] for p in points) for k in range(3)))
    context['pc_map_bounds_min'] = list(low); context['pc_map_bounds_max'] = list(high)
    frame_level(bpy.context)
    # A saved overview camera gives a reproducible standalone mapping image.
    camera = bpy.data.cameras.new('Level overview'); obj = link('Level overview',camera,'Landmarks')
    center = (low+high)/2; obj.location = center+Vector((0,0,150)); obj.rotation_euler = (0,0,0)
    camera.type = 'ORTHO'; camera.ortho_scale = max(high.x-low.x,high.y-low.y)*1.1
    context.camera = obj; context.render.resolution_x = 1400; context.render.resolution_y = 1400
    context.render.resolution_percentage = 100
    register()
    context.render.filepath = str(final/'overview.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(project/'level.blend'))
    report['blend_sha256'] = hashlib.sha256(saved.read_bytes()).hexdigest()
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    context.render.filepath = str(project/'overview.png'); bpy.ops.render.render(write_still=True)
    check = {'objects':len(data['objects']), 'mesh_faces':sum(len(bpy.data.objects[o['id']+f' [0x{o["flags"]:04X}]'].data.polygons) for o in data['objects']),
             'packed_textures':len(images), 'layers':{name:len(bpy.data.collections[name].objects) for name in LAYERS},
             'framing': 'Visible scenery touching the collision envelope; distant objects retained in a hidden collection',
             'blender_version':bpy.app.version_string}
    (project/'blender-check.json').write_text(json.dumps(check,indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('command',choices=['create','register'])
    parser.add_argument('project',nargs='?',type=Path); parser.add_argument('--project-path',type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.command == 'create': create(args.project,args.project_path or args.project)
    else: register()


if __name__ == '__main__': main()
