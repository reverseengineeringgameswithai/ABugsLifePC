#!/usr/bin/env python3
"""Add Training pickups/actors to a fresh successor of a saved mapping project.

No live memory, original assets or source Blender file are changed.
"""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import shutil
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc.original_level import TRAINING, RETAIL_EXE, digest, texture_page, png_rgba
from ablpc.original_population import actors, stored_model, letter_pixels, initialized_placements, TOKEN_KINDS, BERRY_PICKUPS, MAPPED_PICKUPS
from ablpc.level_dat import LevelDat
from ablpc.level_raw import packets
from ablpc.terrain_all import TerrainAll


def native_pickups(dat, terrain, exe):
    """Execute original terrain load and pickup initialization, without a game."""
    spec = importlib.util.spec_from_file_location('training_native',ROOT/'scripts/terrain-retail-probe.py')
    native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
    original_loader = native.load_source
    native.load_source = lambda key: TerrainAll.parse(terrain) if key=='level01' else original_loader(key)
    try: ref = native.RetailProbe('level01',native.p.load_text(exe))
    finally: native.load_source = original_loader
    top = next(r for r in LevelDat.parse(dat).top_records if r.type_id == 0x3f)
    table = dat[top.offset:top.offset+4+top.count*16]
    ptr = native.p.FIXTURE+0x4000
    ref.cpu.mem_write(ptr,table); native.p.put(ref.cpu,0x5c595c,'I',ptr)
    import pefile
    pe = pefile.PE(data=exe.read_bytes())
    ref.cpu.mem_write(0x4c6a88,pe.get_data(0xc6a88,64))
    init = ref.call(0x456a90,())
    return native,ref,top,bytes(ref.cpu.mem_read(ptr,len(table))),init


def populate(source, target, *, tokens_only=False, berries_only=False, open_editor=False):
    source, target = source.resolve(), target.resolve()
    if not source.is_relative_to(ROOT/'work/level-projects') or not target.is_relative_to(ROOT/'work/level-projects'):
        raise ValueError('Mapping projects must remain under work/level-projects')
    if target.exists():
        raise ValueError('Population requires a fresh destination; never overwrite annotations')
    incremental=tokens_only or berries_only
    selectors=BERRY_PICKUPS if berries_only else TOKEN_KINDS
    metadata='berry-pickups' if berries_only else 'seed-tokens'
    if incremental and not (source/'population.json').exists():
        raise ValueError('Incremental addition requires an already populated source')
    if incremental and (source/(metadata+'.json')).exists():
        raise ValueError('Source already has this pickup addition')
    if incremental and any(r['selector'] in selectors for r in json.loads((source/'population.json').read_text())['placements']):
        raise ValueError('Source population already includes these pickups')
    data = json.loads((source/'original-map.json').read_text())
    report = json.loads((source/'import-report.json').read_text())
    inputs = {key:(source/'inputs'/Path(row[0]).name).read_bytes() for key,row in TRAINING.items()}
    for key,row in TRAINING.items():
        if digest(inputs[key]) != row[1]: raise ValueError(f'Training {key} hash mismatch')
    exe = source/'inputs/bugs.exe'
    if digest(exe.read_bytes()) != RETAIL_EXE: raise ValueError('Retail EXE mismatch')
    source_sha = digest((source/'level.blend').read_bytes())
    native,ref,top,initialized,init = native_pickups(inputs['dat'],inputs['terrain'],exe)
    rows = initialized_placements(data['placements'],top.offset,initialized,
                                  selectors if incremental else MAPPED_PICKUPS)
    tokens = [r for r in rows if r['selector'] in TOKEN_KINDS]
    if not berries_only and [r['selector'] for r in tokens] != [0x2b,0x2b]:
        raise ValueError('Training seed-token census changed')
    if berries_only and [r['selector'] for r in rows] != [0x23,0x23,0x2c,0x2c,0x2c,0x2c]:
        raise ValueError('Training blueberry/berry-token census changed')
    blender = runpy.run_path(str(ROOT/'scripts/original-map.py'))['blender_command']()
    if incremental:
        result = dict(experiment='EXP-20260910-001',source_project=str(source),source_blend_sha256=source_sha,
                      placements=rows,native=dict(loader=ref.loader,initializer=ref.initializer,pickup_initializer=init),
                      limits=['Editor pickup meshes at native initialized XYZ; lesson-gated tokens shown together.'])
        if berries_only:
            result['lesson_proof']=runpy.run_path(str(ROOT/'scripts/training-berry-token-probe.py'))['proof'](source)
        shutil.copytree(source,target)
        (target/(metadata+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        subprocess.run(blender+['--background','--disable-autoexec',str(target/'level.blend'),
                       '--python-exit-code','1','--python',str(ROOT/'tools/blender/populate_original.py'),
                       '--',str(target),'--berry-pickups-only' if berries_only else '--tokens-only'],check=True)
        report['pre_'+metadata+'_blend_sha256']=report.pop('blend_sha256',None)
        report['blend_sha256']=digest((target/'level.blend').read_bytes())
        report[metadata]=metadata+'.json'
        (target/'import-report.json').write_text(json.dumps(report,indent=2)+'\n')
        with (target/'README.md').open('a') as output:
            output.write('\n## '+metadata+'\n\nAdded '+str(len(rows))+' pickups (EXP-20260910-001); '
                         'N > ABLPC Map for layers. Lesson-gated tokens are shown together. '
                         +metadata+'.json supplements the earlier population report.\n')
        if digest((source/'level.blend').read_bytes())!=source_sha:raise ValueError('Source changed during addition')
        if open_editor:
            subprocess.Popen(blender+['--disable-autoexec',str(target/'level.blend'),'--python',
                             str(ROOT/'tools/blender/original_map.py'),'--','register'],start_new_session=True)
        print(json.dumps(dict(project=str(target),added_pickups=len(rows),source_preserved=True)))
        return
    chunks, _ = packets(inputs['raw'])
    def packet(tag, ident=None):
        found = [(off,p) for off,_,p in chunks if struct.unpack_from('<I',p)[0] == tag
                 and (ident is None or len(p)>=8 and struct.unpack_from('<I',p,4)[0] == ident)]
        if len(found)!=1: raise ValueError(f'Expected unique packet {tag:#x}/{ident}')
        return found[0]
    actor_offset, actor_data = packet(0x23)
    actor_rows = actors(actor_data)
    if Counter(r['type'] for r in actor_rows) != {38:1,11:4,9:4}:
        raise ValueError('Training actor census changed')
    height_calls = []
    for row in actor_rows:
        x,y,z = row['position']; point = native.p.FIXTURE+0x3000
        native.p.put(ref.cpu,point,'3i',x*32,-0x2000000,z*32)
        call = ref.call(0x4abe00,(point,0)); value=call['eax_at_stop']
        if value>=2**31: value-=2**32
        if abs(value)>10000000: raise ValueError('Actor mapping height has no floor')
        row['display_position'] = [x,value/32,z]
        row['height_note'] = 'Editor feet snapped with native floor query; not a running actor simulation'
        height_calls.append(dict(slot=row['slot'],height_runtime=value,execution=call))
    soil_offset,soil_packet = packet(0x102,38)
    soil = stored_model(soil_packet[8:])
    pages = {}
    for page in {(f['tag']>>8)&31 for f in soil['faces']} | {29}:
        off,payload = packet(page)
        _,_,palette,rgba = texture_page(payload)
        pages[page] = dict(offset=off,sha256=digest(payload),png=png_rgba(rgba))
        if page==29: pickup_palette=palette
    letters = {str(tile):letter_pixels(packet(0x22,tile)[1],pickup_palette) for tile in range(16,20)}
    exit_object = next(o for o in data['objects'] if o['id']=='primary.117')
    if exit_object['geometry_offset']!=90780 or exit_object['origin']!=[416,-651,8915]:
        raise ValueError('Exit-side sign locator changed')
    terrain = TerrainAll.parse(inputs['terrain'])
    exit_sources = [r.index for r in terrain.records if r.result_word==3 and r.field_10==6]
    if exit_sources != [24]: raise ValueError('Training result-3 terrain census changed')
    result = dict(experiment='EXP-20260909-013',source_project=str(source),source_blend_sha256=source_sha,
                  placements=rows,actors=actor_rows,actor_packet_offset=actor_offset,
                  actor_packet_sha256=digest(actor_data),soil=soil,soil_packet_offset=soil_offset,
                  soil_all_sha256=digest(soil_packet[8:]),letters=letters,
                  pages={str(k):{n:v for n,v in p.items() if n!='png'} for k,p in pages.items()},
                  exit_object='primary.117',exit_collision_source=24,
                  native=dict(loader=ref.loader,initializer=ref.initializer,pickup_initializer=init,actor_heights=height_calls),
                  limits=['Mr. Soil uses original textured stored pose, not an animated rig.',
                          'Grain, letters, spiders and seeds are editor meshes; letters use original frame-zero pixels.',
                          'Actor feet use native floor queries; headings, script movement and tutorial visibility are not simulated.',
                          'All four spider spawns are shown together although tutorial-gated in game.',
                          'Exit-side sign identity inferred from geometry and proximity to confirmed result-3 terrain.'])
    shutil.copytree(source,target)
    for page,p in pages.items(): (target/'textures'/f'population-page-{page:02d}.png').write_bytes(p['png'])
    (target/'population.json').write_text(json.dumps(result,indent=2)+'\n')
    subprocess.run(blender+['--background','--disable-autoexec',str(target/'level.blend'),
                    '--python-exit-code','1','--python',str(ROOT/'tools/blender/populate_original.py'),'--',str(target)],check=True)
    report['base_import_blend_sha256']=report.pop('blend_sha256',None)
    report['blend_sha256']=digest((target/'level.blend').read_bytes())
    report['population']='population.json'
    report['population_experiment']=result['experiment']
    (target/'import-report.json').write_text(json.dumps(report,indent=2)+'\n')
    (target/'README.md').write_text('# Populated original Training mapping scene\n\n'
        '50 grains, F/L/I/K, two green and four berry seed tokens, two blueberry records (one distant), four spiders, four seeds, Mr. Soil and exit overlay.\n'
        'Use N > ABLPC Map for individual layers. Population provenance: population.json; '
        'saved-file checks: population-check.json. original-map.json and the base counts/limits '
        'in import-report.json describe the unchanged scenery extraction, supplemented here.\n\n'
        +'\n'.join('- '+s for s in result['limits'])+'\n\n'
        +'Source saved project preserved at '+str(source)+'.\n')
    if digest((source/'level.blend').read_bytes())!=source_sha: raise ValueError('Source changed during population')
    if open_editor:
        subprocess.Popen(blender+['--disable-autoexec',str(target/'level.blend'),'--python',
                         str(ROOT/'tools/blender/original_map.py'),'--','register'],start_new_session=True)
    print(json.dumps(dict(project=str(target),counts=dict(grain=50,letters=4,seed_tokens=2,berry_seed_tokens=4,blueberry_records=2,spiders=4,seeds=4,mr_soil=1,exit_sign=1),source_preserved=True)))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('target',type=Path)
    mode=p.add_mutually_exclusive_group()
    mode.add_argument('--tokens-only',action='store_true',help='Add green tokens to an already populated map')
    mode.add_argument('--berry-pickups-only',action='store_true',help='Add blueberries and lesson-gated berry seed tokens to a populated map')
    p.add_argument('--open',action='store_true',help='Open the successor after verification')
    a=p.parse_args();populate(a.source,a.target,tokens_only=a.tokens_only,berries_only=a.berry_pickups_only,open_editor=a.open)
