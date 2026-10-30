"""Complete original-level reference scene, EXP-20260927-001; never exported.

Builds scenery (meshes and sprite batches), pickups at native-initialized
positions, creatures with their stored RAW models, Flik's start, collision,
barriers and remaining stored rows from one original-map.json (version 2).
Reuses the Training map's coordinate conversion, materials and sidebar.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]/'reimplementation'))
from original_map import xyz, frame_level, register  # noqa: E402
from ablpc.collectible_preview import preview as pickup_preview  # noqa: E402

SCENERY = ('Original scenery', 'Secondary scene', 'Distant source objects', 'Undispatched records')
PICKUP_LAYERS = ('Grain', 'FLIK letters', 'Berries', 'Seed tokens', 'Telescopes', 'Other pickups')
REFERENCE = ('Flik start', 'Creature offset model parts', 'Collision surfaces', 'Collision • special results', 'XZ barriers',
             'Other stored rows', 'Landmarks')
HIDDEN = {'Secondary scene', 'Distant source objects', 'Undispatched records', 'Creature offset model parts',
          'Collision surfaces',
          'Collision • special results', 'XZ barriers', 'Other stored rows'}
PICKUP_COLOURS = {0x20: (.85, .85, .85), 0x2c: (.75, .25, .70), 0x2d: (.20, .80, .80),
                  0x30: (.55, .40, .20), 0x31: (1, .45, .10)}
RESULT_COLOURS = {1: (1, .15, .1, 1), 2: (1, .8, .1, 1), 3: (.3, 1, .2, 1), 4: (.7, .3, 1, 1)}


def collection(name):
    if name not in bpy.data.collections:
        bpy.context.scene.collection.children.link(bpy.data.collections.new(name))
    return bpy.data.collections[name]


def add(name, data, layer):
    obj = bpy.data.objects.new(name, data)
    collection(layer).objects.link(obj)
    return obj


def solid(name, rgba):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name); mat.diffuse_color = rgba; mat.use_nodes = True
    nodes = mat.node_tree.nodes; nodes.clear()
    emission = nodes.new('ShaderNodeEmission'); emission.inputs['Color'].default_value = rgba
    output = nodes.new('ShaderNodeOutputMaterial'); mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    return mat


def textured(name, image):
    """Original page times PC vertex RGB, colour-keyed alpha; same graph as original_map.material."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links; nodes.clear()
    tex = nodes.new('ShaderNodeTexImage'); tex.image = image
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
    mat['preview'] = 'Original textures and vertex colours; approximate brightness'
    return mat


def vertex_colour_only():
    name = 'PC vertex RGB only (page unavailable)'
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links; nodes.clear()
    color = nodes.new('ShaderNodeVertexColor'); color.layer_name = 'PC vertex RGB'
    emission = nodes.new('ShaderNodeEmission'); links.new(color.outputs['Color'], emission.inputs['Color'])
    output = nodes.new('ShaderNodeOutputMaterial'); links.new(emission.outputs[0], output.inputs[0])
    return mat


class Builder:
    """Accumulates one Blender mesh from stored-unit points and tagged faces."""

    def __init__(self):
        self.points, self.colours, self.faces, self.uvs, self.materials, self.tags = [], [], [], [], [], []
        self.dropped = 0

    def vertex(self, point, rgb):
        self.points.append(point); self.colours.append(rgb)
        return len(self.points)-1

    def face(self, indices, uv, material, tag=-1):
        # Blender needs distinct polygon corners; drop repeated source corners with their UV.
        seen, keep = set(), []
        for position, index in enumerate(indices):
            if index not in seen:
                seen.add(index); keep.append(position)
        if len(keep) < 3:
            self.dropped += 1
            return
        self.faces.append([indices[i] for i in keep]); self.uvs.append([uv[i] for i in keep] if uv else None)
        self.materials.append(material); self.tags.append(tag)

    def build(self, name, layer, location):
        data = bpy.data.meshes.new(name)
        data.from_pydata([xyz(p) for p in self.points], [], self.faces); data.update()
        order = list(dict.fromkeys(self.materials))
        for mat in order:
            data.materials.append(mat)
        colours = data.color_attributes.new(name='PC vertex RGB', type='FLOAT_COLOR', domain='POINT')
        for target, rgb in zip(colours.data, self.colours):
            target.color_srgb = (*[c/255 for c in rgb], 1)
        uv_layer = data.uv_layers.new(name='PC UV')
        tag_attr = data.attributes.new(name='pc_face_tag', type='INT', domain='FACE')
        for polygon, mat, uv, tag in zip(data.polygons, self.materials, self.uvs, self.tags):
            polygon.material_index = order.index(mat); tag_attr.data[polygon.index].value = tag
            if uv:
                for loop, value in zip(polygon.loop_indices, uv):
                    uv_layer.data[loop].uv = value
        obj = add(name, data, layer); obj.location = xyz(location)
        obj['pc_dropped_degenerate_faces'] = self.dropped
        return obj


class Scene:
    def __init__(self, project, data):
        self.project, self.data = project, data
        self.images, self.widths = {}, {}
        for page in data['textures']:
            image = bpy.data.images.load(str(project/'textures'/f'page-{page["page"]:02d}.png'))
            image.pack(); image.filepath = f'//textures/page-{page["page"]:02d}.png'
            self.images[page['page']] = image; self.widths[page['page']] = page['width']

    def page_material(self, page, label):
        if page not in self.images:
            return vertex_colour_only()
        return textured(f'PC page {page:02d} {label}', self.images[page])

    def uv(self, word, page):
        width = self.widths.get(page, 256)
        return ((word & 255)/width, 1-(word >> 8)/width)

    def mesh_faces(self, builder, vertices, faces, base=0):
        for face in faces:
            page = (face['tag'] >> 8) & 31
            builder.face([base+i for i in face['indices']], [self.uv(w, page) for w in face['uv']],
                         self.page_material(page, f'tag {face["tag"]:04X}'), face['tag'])


def stamp(obj, **properties):
    obj['mapping_note'] = properties.pop('note', '')
    for key, value in properties.items():
        obj['pc_'+key] = value


def build_scenery(scene, low, high):
    counts = {name: 0 for name in SCENERY}; dropped = 0
    for source in scene.data['objects']:
        builder = Builder()
        if source['kind'] in ('mesh', 'mesh-4'):
            for v in source['vertices']:
                builder.vertex(v['position'], v['rgb'])
            scene.mesh_faces(builder, source['vertices'], source['faces'])
            points = [v['position'] for v in source['vertices']]
        else:
            # Screen-aligned native quads: two crossed vertical planes in the editor.
            for quad in source['sprites']:
                c = quad['center']; mat = scene.page_material(quad['page'], f'sprite {quad["tag"]:04X}')
                uv = [scene.uv(w, quad['page']) for w in quad['uv']]
                for plane in (0, 2):
                    ids = []
                    for (qx, qy), rgb in zip(quad['corners'], quad['rgb']):
                        offset = [0, qy, 0]; offset[plane] = qx
                        ids.append(builder.vertex([c[k]+offset[k] for k in range(3)], rgb))
                    builder.face(ids, uv, mat, quad['tag'])
            points = builder.points or [[0, 0, 0]]
        world = [xyz([p[k]+source['origin'][k] for k in range(3)]) for p in points]
        outside = any(max(p[k] for p in world) < low[k]-1 or min(p[k] for p in world) > high[k]+1 for k in (0, 1))
        layer = ('Secondary scene' if source['section'] == 'secondary'
                 else 'Distant source objects' if outside else 'Original scenery')
        name = f'{source["id"]} [0x{source["flags"]:04X}]'+('' if source['kind'] in ('mesh', 'mesh-4') else ' sprites')
        obj = builder.build(name, layer, source['origin'])
        dropped += builder.dropped; counts[layer] += 1
        stamp(obj, source=source['id'], record_offset=f'0x{source["record_offset"]:X}',
              object_offset=f'0x{source["object_offset"]:X}', geometry_offset=f'0x{source["geometry_offset"]:X}',
              flags=f'0x{source["flags"]:04X}', dispatch=f'0x{source["dispatch"]:02X}', kind=source['kind'],
              stored_origin=source['origin'], angles=source['angles'], scale=source['scale'],
              animation_selector=source['animation_selector'], object_hex=source['object_hex'],
              geometry_sha256=source['geometry_sha256'],
              note=source.get('preview', '')+(f' {source["mesh_format"]}.' if 'mesh_format' in source else ''))
    for row in scene.data['undispatched']:
        obj = add(f'{row["id"]} [0x{row["flags"]:04X}] undispatched', None, 'Undispatched records')
        obj.empty_display_type = 'CUBE'; obj.empty_display_size = .4; obj.location = xyz(row['origin'])
        stamp(obj, source=row['id'], record_offset=f'0x{row["record_offset"]:X}',
              object_offset=f'0x{row["object_offset"]:X}', geometry_offset=f'0x{row["geometry_offset"]:X}',
              object_hex=row['object_hex'], note=row['note'])
        counts['Undispatched records'] += 1
    return counts, dropped


def coloured_preview(name, source, layer, rgb=None):
    builder = Builder()
    for v in source['vertices']:
        builder.vertex(v['position'], rgb or v['rgb'])
    for face in source['faces']:
        colour = rgb or source['vertices'][face['indices'][0]]['rgb']
        builder.face(face['indices'], None, solid(f'Map RGB {tuple(colour)}', (*[c/255 for c in colour], 1)))
    return builder, builder.build


def marker_mesh(radius, height):
    """Editor octahedron in stored units (Y down)."""
    points = [(0, -height, 0), (radius, 0, 0), (0, 0, radius), (-radius, 0, 0), (0, 0, -radius), (0, height, 0)]
    faces = [(0, 2, 1), (0, 3, 2), (0, 4, 3), (0, 1, 4), (5, 1, 2), (5, 2, 3), (5, 3, 4), (5, 4, 1)]
    return dict(vertices=[dict(position=list(p), rgb=[255, 255, 255]) for p in points],
                faces=[dict(indices=list(f)) for f in faces])


def letter_mesh(pixels):
    vertices, faces = [], []
    for pixel in pixels:
        x, y = (pixel['x']-12)*18, (pixel['y']-12)*18; base = len(vertices)
        for a, b, c in ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)):
            vertices.append(dict(position=[x+a*18, y+b*18, -24+c*48], rgb=pixel['rgb']))
        for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (3, 7, 6, 2), (0, 4, 7, 3), (1, 2, 6, 5)):
            faces.append(dict(indices=[base+i for i in f]))
    return dict(vertices=vertices, faces=faces)


def build_pickups(scene):
    counts = {}
    for row in scene.data['pickups']:
        selector = row['selector']; layer = row['layer']
        if selector in (0x10, 0x11, 0x12, 0x13) and str(selector) in scene.data.get('letters', {}):
            source, rgb = letter_mesh(scene.data['letters'][str(selector)]), None
        elif str(selector) in scene.data['preview_kinds']:
            source, rgb = pickup_preview(scene.data['preview_kinds'][str(selector)]), None
        else:
            source = marker_mesh(140, 200)
            rgb = [round(c*255) for c in PICKUP_COLOURS.get(selector, (1, 0, 1))]
        counts[layer] = counts.get(layer, 0)+1
        name = f'{row["label"]} {counts[layer]:02d} • {row["id"]}'
        _, build = coloured_preview(name, source, layer, rgb)
        obj = build(name, layer, row['position'])
        stamp(obj, source=row['id'], record_offset=f'0x{row["offset"]:X}', selector=f'0x{selector:02X}',
              raw_hex=row['raw_hex'], initialized_hex=row['initialized_hex'], stored_origin=row['stored_position'],
              initialized_position=row['position'], population_role='pickup',
              note='Editor preview at original 00456A90 initialized XYZ; stored row retained in pc_raw_hex.')
    return counts


def build_creatures(scene):
    counts = {}; dropped = 0
    for row in scene.data['creatures']:
        model = scene.data['creature_models'][str(row['type'])]
        if row['name']:
            layer = f'Creatures • {row["name"]} (type {row["type"]})'
            label = row['name'][0].upper()+row['name'][1:]
        else:
            hint = f' (looks like: {row["appearance"]})' if row.get('appearance') else ''
            layer, label = f'Creatures • type {row["type"]}{hint}', f'Creature type {row["type"]}'
        counts[layer] = counts.get(layer, 0)+1
        offset = {p['index'] for p in model['parts'] if p['offset_part']}
        name = f'{label} {counts[layer]:02d} • slot {row["slot"]}'
        for extra in (False, True):
            faces = [f for f in model['faces'] if (f['part'] in offset) == extra]
            if not faces:
                continue
            builder = Builder()
            for v in model['vertices']:
                builder.vertex(v['position'], v['rgb'])
            scene.mesh_faces(builder, model['vertices'], faces)
            if extra:
                part = builder.build(name+' • offset parts', 'Creature offset model parts', row['position'])
                stamp(part, source=f'RAW creature slot {row["slot"]}', population_role='creature offset parts',
                      offset_parts=sorted(offset), note='Model parts stored far from the model origin; '
                      'shown separately because their role (alternate/helper) is not established.')
                dropped += builder.dropped
                continue
            obj = builder.build(name, layer, row['position'])
            dropped += builder.dropped
        stamp(obj, source=f'RAW creature slot {row["slot"]}', record_offset=f'packet 0x{scene.data["creature_packet_offset"]:X} +0x{row["offset"]:X}',
              creature_type=row['type'], script_selector=row['script'], raw_hex=row['raw_hex'],
              appearance_hint=row.get('appearance') or 'none',
              stored_origin=row['position'], native_floor_below=row['native_floor_y'] if row.get('native_floor_y') is not None else 'none',
              model_packet_offset=f'0x{model["packet_offset"]:X}', population_role='creature',
              note='Original RAW 0x102 model in stored pose at the literal stored XYZ; no animation, '
                   'heading or script movement. Every slot is shown, including gated spawns.')
    return counts, dropped


def build_reference(scene):
    start = scene.data['spawn']
    source = marker_mesh(160, 320)
    _, build = coloured_preview('Flik start', source, 'Flik start', [40, 255, 90])
    obj = build('Flik start', 'Flik start', [start['stored_xz'][0], start['native_start_y'], start['stored_xz'][1]])
    stamp(obj, source=f'spawn table {start["va"]}', heading=start['heading'], runtime_xz=start['runtime_xz'],
          note='X/Z/heading from the executable per-engine table; Y follows 0043E6B0 (004AC460 from the top, minus 0x100), run offline.')
    text = bpy.data.curves.new('START label', 'FONT'); text.body = 'START'; text.align_x = 'CENTER'; text.size = 1.2
    text.materials.append(solid('Map labels • cream', (1, .95, .55, 1)))
    label = add('START • map label', text, 'Flik start'); label.parent = obj
    label.location = (0, -1.5, 3); label.show_in_front = True
    for group in scene.data['collision']:
        cells = group['cells']; points = [v for cell in cells for v in cell['vertices_stored']]
        data = bpy.data.meshes.new(f'Collision {group["source"]:03d}')
        data.from_pydata([xyz(p) for p in points], [], [(i*3, i*3+1, i*3+2) for i in range(len(cells))]); data.update()
        special = group['result_word'] != 0
        layer = 'Collision • special results' if special else 'Collision surfaces'
        name = f'Collision {group["source"]:03d}'+(f' • result {group["result_word"]}' if special else '')
        obj = add(name, data, layer); obj.display_type = 'WIRE' if not special else 'SOLID'; obj.show_in_front = True
        if special:
            data.materials.append(solid(f'Collision result {group["result_word"]}',
                                        RESULT_COLOURS.get(group['result_word'], (1, 0, 1, 1))))
        attr = data.attributes.new(name='pc_cell_offset', type='INT', domain='FACE')
        for polygon, cell in zip(attr.data, cells):
            polygon.value = cell['file_offset']
        stamp(obj, source=group['source'], result_word=group['result_word'], descriptor_kind=group['kind'],
              note='Native floor/collision triangles; result word from the source descriptor +0x28.')
    for barrier in scene.data['barriers']:
        points = [(x, barrier['display_y'], z) for x, z in barrier['points_xz']]
        data = bpy.data.meshes.new(f'XZ barrier {barrier["source"]}')
        data.from_pydata([xyz(p) for p in points], [(i, i+1) for i in range(len(points)-1)], []); data.update()
        obj = add(data.name, data, 'XZ barriers'); obj.show_in_front = True
        stamp(obj, source=barrier['source'], note=barrier['note'])
    for row in scene.data['other_rows']:
        obj = add(f'Type 0x{row["type"]:02X} row • {row["id"]}', None, 'Other stored rows')
        obj.empty_display_type = 'PLAIN_AXES'; obj.empty_display_size = .5; obj.location = xyz(row['position'])
        stamp(obj, source=row['id'], record_offset=f'0x{row["offset"]:X}', raw_hex=row['raw_hex'],
              note='Stored 12-byte top-record row; role varies by type and is not claimed here.')


def create(project):
    data = json.loads((project/'original-map.json').read_text())
    if (project/'level.blend').exists():
        raise ValueError('Mapping project already has a saved Blender file; preserve user edits')
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.collections):
        bpy.data.collections.remove(block)
    context = bpy.context.scene; context['ablpc_original_map'] = True
    context['pc_map_name'] = data['title']; context['ablpc_map_project'] = str(project)
    context['pc_coordinate_conversion'] = data['coordinate_system']['blender_xyz']
    scene = Scene(project, data)
    ground = [xyz(v) for g in data['collision'] for c in g['cells'] for v in c['vertices_stored']]
    low = Vector(tuple(min(p[k] for p in ground) for k in range(3)))
    high = Vector(tuple(max(p[k] for p in ground) for k in range(3)))
    for name in (*SCENERY, *PICKUP_LAYERS, *REFERENCE):
        collection(name)
    scenery, dropped = build_scenery(scene, low, high)
    pickups = build_pickups(scene)
    creatures, creature_dropped = build_creatures(scene)
    build_reference(scene)
    for name in list(bpy.data.collections.keys()):
        if not bpy.data.collections[name].objects and name not in ('Landmarks',):
            bpy.data.collections.remove(bpy.data.collections[name])
    present = [c.name for c in context.collection.children]
    creatures = sorted((n for n in present if n.startswith('Creatures • ')),
                       key=lambda n: int(n.split('type ')[1].split(')')[0].split(' ')[0]))
    layers = [n for n in (*SCENERY, *PICKUP_LAYERS, *creatures, *REFERENCE) if n in present]
    for name in layers:  # Outliner order follows the sidebar order.
        context.collection.children.unlink(bpy.data.collections[name])
        context.collection.children.link(bpy.data.collections[name])
    context['pc_map_layers'] = '\n'.join(layers)
    for name in HIDDEN & set(layers):
        bpy.data.collections[name].hide_viewport = True; bpy.data.collections[name].hide_render = True
    text = bpy.data.texts.new(data['title']+' - Read me'); text.write((project/'README.md').read_text())
    context.render.engine = 'CYCLES'; context.cycles.samples = 16
    context.view_settings.view_transform = 'Standard'; context.world.color = (.10, .10, .10)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active; space.shading.type = 'MATERIAL'
                space.overlay.show_floor = False; space.overlay.show_axis_x = False; space.overlay.show_axis_y = False
                space.show_region_ui = True
    context.view_layers[0].update()
    visible = [o for o in bpy.data.collections['Original scenery'].objects] or list(bpy.data.objects)
    points = [o.matrix_world @ Vector(c) for o in visible for c in o.bound_box]
    points += [Vector(p) for p in ground]
    low = Vector(tuple(min(p[k] for p in points) for k in range(3)))
    high = Vector(tuple(max(p[k] for p in points) for k in range(3)))
    context['pc_map_bounds_min'] = list(low); context['pc_map_bounds_max'] = list(high)
    frame_level(bpy.context)
    camera = bpy.data.cameras.new('Level overview'); obj = add('Level overview', camera, 'Landmarks')
    center = (low+high)/2; obj.location = center+Vector((0, 0, max(150, high.z-center.z+50)))
    camera.type = 'ORTHO'; camera.ortho_scale = max(high.x-low.x, high.y-low.y)*1.05; camera.clip_end = 5000
    context.camera = obj; context.render.resolution_x = 1600; context.render.resolution_y = 1600
    context.render.resolution_percentage = 100
    register()
    context.render.filepath = str(project/'overview.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(project/'level.blend'))
    bpy.ops.render.render(write_still=True)
    # Unsaved second image: clip everything more than 2048 stored units above
    # Flik's start so roofs and canopies do not hide interiors.
    cut = xyz([0, data['spawn']['native_start_y']-2048, 0])[2]
    camera.clip_start = max(.01, obj.location.z-cut)
    context.render.filepath = str(project/'overview-cutaway.png')
    bpy.ops.render.render(write_still=True)
    return dict(scenery_layers=scenery, pickup_layers=pickups, creature_layers=creatures,
                degenerate_faces_dropped=dict(scenery=dropped, creatures=creature_dropped))


def verify(project, built):
    """Reopen the saved file and check every source object, placement and layer."""
    data = json.loads((project/'original-map.json').read_text())
    bpy.ops.wm.open_mainfile(filepath=str(project/'level.blend'))
    checked = dict(vertices=0, faces=0, placements=0)
    for source in data['objects']:
        name = f'{source["id"]} [0x{source["flags"]:04X}]'+('' if source['kind'] in ('mesh', 'mesh-4') else ' sprites')
        obj = bpy.data.objects[name]
        assert tuple(obj.location) == xyz(source['origin'])
        expected = len(source['faces']) if source['kind'] in ('mesh', 'mesh-4') else 2*len(source['sprites'])
        assert len(obj.data.polygons)+obj['pc_dropped_degenerate_faces'] == expected
        if source['kind'] in ('mesh', 'mesh-4'):
            assert len(obj.data.vertices) == len(source['vertices'])
            for vertex, expected in zip(obj.data.vertices, source['vertices']):
                assert max(abs(a-b) for a, b in zip(vertex.co, xyz(expected['position']))) < 1e-4
            checked['vertices'] += len(source['vertices'])
        checked['faces'] += len(obj.data.polygons)
    for row in data['pickups']:
        obj = next(o for o in bpy.data.objects if o.get('pc_source') == row['id'])
        assert tuple(obj.location) == xyz(row['position']) and obj['pc_raw_hex'] == row['raw_hex']
        checked['placements'] += 1
    for row in data['creatures']:
        obj = next(o for o in bpy.data.objects if o.get('pc_source') == f'RAW creature slot {row["slot"]}'
                   and o.get('pc_population_role') == 'creature')
        assert tuple(obj.location) == xyz(row['position']) and obj['pc_raw_hex'] == row['raw_hex']
        checked['placements'] += 1
    cells = sum(len(g['cells']) for g in data['collision'])
    assert sum(len(o.data.polygons) for name in ('Collision surfaces', 'Collision • special results')
               if name in bpy.data.collections for o in bpy.data.collections[name].objects) == cells
    assert len([i for i in bpy.data.images if i.packed_file]) == len(data['textures'])
    assert bpy.context.scene.get('ablpc_original_map')
    report = dict(experiment=data['experiment'], engine=data['engine'], title=data['title'],
                  saved_objects=len(bpy.data.objects), source_objects_verified=len(data['objects']),
                  source_vertices_verified=checked['vertices'], polygons_verified=checked['faces'],
                  pickups_and_creatures_verified=checked['placements'], collision_triangles_verified=cells,
                  packed_textures=len(data['textures']),
                  layers={c.name: len(c.objects) for c in bpy.context.scene.collection.children},
                  hidden_layers=sorted(c.name for c in bpy.context.scene.collection.children if c.hide_viewport),
                  blend_sha256=hashlib.sha256((project/'level.blend').read_bytes()).hexdigest(),
                  save_reopen='passed', blender_version=bpy.app.version_string, **built)
    (project/'blender-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'layers'}))


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('project', type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    built = create(args.project)
    verify(args.project, built)


if __name__ == '__main__':
    main()
