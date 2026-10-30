"""Augment, verify and save an existing original-map scene without rebuilding it."""
import hashlib
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'reimplementation'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ablpc.collectible_preview import preview as pickup_preview
from ablpc.enemy_preview import preview as enemy_preview
from ablpc.original_population import TOKEN_KINDS, BERRY_PICKUPS
from original_map import xyz, link, mesh, material, frame_level

LAYERS = ('Grain (50)', 'FLIK letters (4)', 'Seed tokens', 'Blueberries', 'Berry seed tokens', 'Distant pickups', 'Spiders (4)', 'Mr. Soil', 'Seeds (4)', 'Level ending marker', 'Map labels')


def fingerprint(obj):
    value = dict(name=obj.name, matrix=[list(r) for r in obj.matrix_world],
                 note=obj.get('mapping_note'), properties={k:obj[k].to_list() if hasattr(obj[k],'to_list') else obj[k] for k in obj.keys()})
    if obj.type=='MESH':
        value.update(vertices=[list(v.co) for v in obj.data.vertices],faces=[list(p.vertices) for p in obj.data.polygons],
                     materials=[m.name for m in obj.data.materials],
                     uv=[[list(v.uv) for v in layer.data] for layer in obj.data.uv_layers])
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def solid(name, rgba):
    m=bpy.data.materials.get(name)
    if m:return m
    m=bpy.data.materials.new(name);m.diffuse_color=rgba;m.use_nodes=True
    nodes=m.node_tree.nodes;nodes.clear()
    e=nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=rgba
    out=nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0])
    return m


def colored(name, source, layer):
    m=mesh(name,[v['position'] for v in source['vertices']],[f['indices'] for f in source['faces']])
    obj=link(name,m,layer)
    palette=list(dict.fromkeys(tuple(v['rgb']) for v in source['vertices']))
    for rgb in palette:m.materials.append(solid('Map RGB '+str(rgb),(*[c/255 for c in rgb],1)))
    for face,row in zip(m.polygons,source['faces']):face.material_index=palette.index(tuple(source['vertices'][row['indices'][0]]['rgb']))
    return obj


def voxel_letter(pixels):
    vertices=[];faces=[]
    for pixel in pixels:
        # Editable extrusion of original native frame-zero pixels, 432 units high.
        x,y=(pixel['x']-12)*18,(pixel['y']-12)*18;base=len(vertices)
        for a,b,c in ((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)):
            vertices.append(dict(position=[x+a*18,y+b*18,-24+c*48],rgb=pixel['rgb']))
        for face in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)):
            faces.append(dict(indices=[base+i for i in face]))
    return dict(vertices=vertices,faces=faces)


def label(body, obj, size=.8):
    t=bpy.data.curves.new(body+' label','FONT');t.body=body;t.align_x='CENTER';t.size=size;t.extrude=.005
    t.materials.append(solid('Map labels • cream',(1,.95,.55,1)))
    text=link(body+' • map label',t,'Map labels');text.parent=obj
    text.location=(0,-1.3,2.5);text.show_in_front=True
    text['mapping_note']='Editor annotation; lies in top-view plane, not game geometry'
    return text


def token_objects(rows):
    objects=[]
    for i,row in enumerate(rows,1):
        if row['selector'] not in TOKEN_KINDS:raise ValueError('Expected seed token selector')
        if any(o.get('pc_population_role')=='seed-token' and o.get('pc_source')==row['id'] for o in bpy.data.objects):
            raise ValueError('Seed token already present; preserve existing object')
        name=row['label']+' '+str(i)
        obj=colored(name,pickup_preview(TOKEN_KINDS[row['selector']]),'Seed tokens')
        obj.location=xyz(row['position']);obj['pc_source']=row['id'];obj['pc_record_offset']=f'0x{row["offset"]:X}'
        obj['pc_population_role']='seed-token';obj['pc_selector']=row['selector']
        obj['pc_raw_hex']=row['raw_hex'];obj['pc_initialized_hex']=row['initialized_hex']
        obj['pc_stored_origin']=row['stored_position'];obj['pc_initialized_position']=row['position']
        obj['mapping_note']='Editor seed-token mesh at original00456A90 initialized XYZ. Both lesson-gated tokens shown together; raw stored Y retained separately.'
        label('Green token '+str(i),obj,.65);objects.append(obj)
    return objects


def berry_objects(rows):
    objects=[];counts={0x23:0,0x2c:0};scene=bpy.context.scene
    low,high=scene['pc_map_bounds_min'],scene['pc_map_bounds_max']
    for row in rows:
        selector=row['selector'];counts[selector]+=1
        name=row['label']+' '+str(counts[selector]);berry=selector==0x23
        src=pickup_preview('berry-blue' if berry else 'token-green')
        if not berry:
            for v in src['vertices']:v['rgb']=[180,55,160]  # Editor colour, not native shaded pixels.
        p=xyz(row['position']);distant=any(p[k]<low[k] or p[k]>high[k] for k in (0,1))
        layer='Distant pickups' if distant else 'Blueberries' if berry else 'Berry seed tokens'
        obj=colored(name,src,layer);obj.location=p;obj['pc_source']=row['id']
        obj['pc_record_offset']=f'0x{row["offset"]:X}';obj['pc_selector']=selector
        obj['pc_population_role']='blueberry' if berry else 'berry-seed-token'
        obj['pc_raw_hex']=row['raw_hex'];obj['pc_initialized_hex']=row['initialized_hex']
        obj['pc_stored_origin']=row['stored_position'];obj['pc_initialized_position']=row['position']
        obj['mapping_note']='Editor preview at native initialized XYZ. '+row['availability']
        if distant:obj['mapping_note']+=' Outside mapped scenery; retained, not classified as unused.'
        lab=label(name,obj,.65)
        if distant:
            for c in list(lab.users_collection):c.objects.unlink(lab)
            bpy.data.collections[layer].objects.link(lab)
        objects.append(obj)
    bpy.data.collections['Distant pickups'].hide_viewport=True
    bpy.data.collections['Distant pickups'].hide_render=True
    return objects


def add_tokens(project, berry=False):
    scene=bpy.context.scene
    if not scene.get('pc_population'):raise ValueError('Expected populated original map')
    layers=('Blueberries','Berry seed tokens','Distant pickups') if berry else ('Seed tokens',)
    if any(n in bpy.data.collections for n in layers):raise ValueError('Pickup layer already exists')
    metadata='berry-pickups' if berry else 'seed-tokens'
    data=json.loads((project/(metadata+'.json')).read_text())
    previous={o.name:fingerprint(o) for o in bpy.data.objects}
    for n in layers:bpy.context.scene.collection.children.link(bpy.data.collections.new(n))
    names=[o.name for o in (berry_objects if berry else token_objects)(data['placements'])]
    scene['ablpc_map_project']=str(project);scene['pc_seed_tokens']=data['experiment']
    notes=bpy.data.texts.new('Training - '+metadata);notes.write('\n'.join(data['limits']))
    scene.render.filepath=str(project/'overview.png')
    saved=project/'level.blend';bpy.ops.wm.save_as_mainfile(filepath=str(saved))
    bpy.ops.wm.open_mainfile(filepath=str(saved))
    assert {name:fingerprint(bpy.data.objects[name]) for name in previous}==previous
    for name,row in zip(names,data['placements'],strict=True):
        obj=bpy.data.objects[name]
        assert tuple(obj.location)==xyz(row['position'])
        assert obj['pc_raw_hex']==row['raw_hex'] and obj['pc_initialized_hex']==row['initialized_hex']
    if berry:
        assert len(bpy.data.collections['Berry seed tokens'].objects)==4
        assert len(bpy.data.collections['Blueberries'].objects)==1
        assert bpy.data.collections['Distant pickups'].hide_viewport and bpy.data.collections['Distant pickups'].hide_render
    else:
        layer=bpy.data.collections['Seed tokens'];assert len(layer.objects)==2 and not layer.hide_viewport and not layer.hide_render
    receipt=dict(experiment=data['experiment'],preserved_objects=len(previous),original_objects_exact=True,
                 original_fingerprints=previous,token_objects=names,positions=[r['position'] for r in data['placements']],
                 save_reopen='passed',blend_sha256=hashlib.sha256(saved.read_bytes()).hexdigest(),
                 source_blend_sha256=data['source_blend_sha256'],blender_version=bpy.app.version_string)
    (project/('berry-pickup-check.json' if berry else 'seed-token-check.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    bpy.ops.render.render(write_still=True)
    print(json.dumps({k:v for k,v in receipt.items() if k!='original_fingerprints'}))


def populate(project):
    data=json.loads((project/'population.json').read_text())
    if not bpy.context.scene.get('ablpc_original_map'):raise ValueError('Expected original mapping scene')
    if bpy.context.scene.get('pc_population'):raise ValueError('Scene is already populated')
    previous={o.name:fingerprint(o) for o in bpy.data.objects}
    for layer in LAYERS:
        if layer in bpy.data.collections:raise ValueError('Population layer already exists')
        bpy.context.scene.collection.children.link(bpy.data.collections.new(layer))
    added=[]
    for row in data['placements']:
        if row['selector'] in TOKEN_KINDS or row['selector'] in BERRY_PICKUPS:continue
        grain=row['selector']==20
        src=pickup_preview('grain') if grain else voxel_letter(data['letters'][str(row['selector'])])
        name=('Grain '+str(len(added)+1).zfill(2)) if grain else row['label']
        obj=colored(name,src,'Grain (50)' if grain else 'FLIK letters (4)')
        obj.location=xyz(row['position']);obj['pc_source']=row['id'];obj['pc_record_offset']=f'0x{row["offset"]:X}'
        obj['pc_raw_hex']=row['raw_hex'];obj['pc_initialized_hex']=row['initialized_hex']
        obj['pc_stored_origin']=row['stored_position'];obj['pc_initialized_position']=row['position']
        obj['pc_population_role']='grain' if grain else 'letter'
        obj['mapping_note']='Editor mesh. Placement from original PC 00456A90 initialization; grain retains literal Y.'
        if not grain:label(row['label'][-1],obj,1.5)
        added.append(obj.name)
    added.extend(o.name for o in token_objects([r for r in data['placements'] if r['selector'] in TOKEN_KINDS]))
    added.extend(o.name for o in berry_objects([r for r in data['placements'] if r['selector'] in BERRY_PICKUPS]))
    images={}
    for page in data['pages']:
        image=bpy.data.images.load(str(project/'textures'/f'population-page-{int(page):02d}.png'))
        image.pack();image.filepath=f'//textures/population-page-{int(page):02d}.png';images[int(page)]=image
    for row in data['actors']:
        role=row['kind'];name=f'Spider {row["slot"]-4}' if role=='spider' else f'Seed {row["slot"]}' if role=='seed' else 'Mr. Soil'
        if role=='Mr. Soil':
            source=data['soil'];m=mesh(name,[v['position'] for v in source['vertices']],[f['indices'] for f in source['faces']])
            obj=link(name,m,'Mr. Soil');uv=m.uv_layers.new(name='PC UV')
            colors=m.color_attributes.new(name='PC vertex RGB',type='FLOAT_COLOR',domain='POINT')
            for dst,v in zip(colors.data,source['vertices']):dst.color_srgb=(*[c/255 for c in v['rgb']],1)
            tags=list(dict.fromkeys(f['tag'] for f in source['faces']))
            for tag in tags:m.materials.append(material(tag,images))
            for poly,face in zip(m.polygons,source['faces']):
                poly.material_index=tags.index(face['tag'])
                for loop,word in zip(poly.loop_indices,face['uv']):uv.data[loop].uv=((word&255)/256,1-(word>>8)/256)
            obj['pc_model_sha256']=data['soil_all_sha256']
            obj['mapping_note']='Original textured SOIL.ALL in stored pose; no animation matrices or tutorial movement. '+row['height_note']
        else:
            source=enemy_preview('spider') if role=='spider' else pickup_preview('grain')
            if role=='seed':
                for v in source['vertices']:
                    v['position']=[v['position'][0]*2,v['position'][1]-150,v['position'][2]*2]
                    v['rgb']=[150,98,44]
            obj=colored(name,source,'Spiders (4)' if role=='spider' else 'Seeds (4)')
            obj['mapping_note']='Editor placement silhouette, not native animated geometry. '+row['height_note']
            if role=='spider':obj['mapping_note']+=' Tutorial-gated spawn shown together with the other three.'
        obj.location=xyz(row['display_position']);obj['pc_source']=f'RAW actor slot {row["slot"]}'
        obj['pc_record_offset']=f'packet 0x{data["actor_packet_offset"]:X} decoded +0x{row["offset"]:X}'
        obj['pc_raw_hex']=row['raw_hex'];obj['pc_stored_origin']=row['position'];obj['pc_script_selector']=row['script']
        obj['pc_population_role']=role;added.append(obj.name);label(name,obj,.9 if role=='Mr. Soil' else .65)
    sign=next(o for o in bpy.data.objects if o.get('pc_source')==data['exit_object'])
    # Add a second collection link: preserve name, mesh, original layer, notes and properties.
    bpy.data.collections['Level ending marker'].objects.link(sign)
    label('EXIT',sign,1.5)
    source=bpy.data.objects['Collision 024'];zone=source.copy();zone.data=source.data.copy()
    zone.name='Exit contact area • source 24';bpy.data.collections['Level ending marker'].objects.link(zone)
    zone.hide_set(False);zone.hide_render=False;zone.display_type='WIRE';zone.show_in_front=True
    zone.data.materials.clear();zone.data.materials.append(solid('Exit area • lime',(.3,1,.2,1)))
    zone['mapping_note']='Original result-word 3 contact triangles; overlay only. Sign association is geometric inference.'
    wire=zone.modifiers.new('Contact outline','WIREFRAME');wire.thickness=.035
    bpy.data.collections['Level ending marker']['mapping_note']='Original sign primary.117 plus source24 contact-area overlay; hide scenery too to hide shared sign.'
    after={name:fingerprint(bpy.data.objects[name]) for name in previous}
    if after!=previous:raise ValueError('Population changed an existing object')
    scene=bpy.context.scene;scene['ablpc_map_project']=str(project);scene['pc_population']='EXP-20260909-013'
    scene['pc_population_limits']='\n'.join(data['limits'])
    notes=bpy.data.texts.new('Training - Population');notes.write('\n'.join(data['limits'])+'\n\n50 grains, F/L/I/K, four spiders, four seeds, Mr. Soil and exit overlay.\n')
    frame_level(bpy.context)
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.data.collections['Mr. Soil'].objects:o.select_set(True);bpy.context.view_layer.objects.active=o
    scene.render.filepath=str(project/'overview.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(project/'level.blend'))
    receipt=dict(experiment=data['experiment'],preserved_objects=len(previous),original_objects_exact=True,
                 source_blend_sha256=data['source_blend_sha256'],blend_sha256=hashlib.sha256((project/'level.blend').read_bytes()).hexdigest(),
                 layers={n:len(bpy.data.collections[n].objects) for n in LAYERS},added_placements=added,
                 original_fingerprints=previous,blender_version=bpy.app.version_string)
    (project/'population-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
    bpy.ops.render.render(write_still=True)


if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:]
    if '--berry-pickups-only' in args:add_tokens(Path(args[0]),True)
    else:(add_tokens if '--tokens-only' in args else populate)(Path(args[0]))
