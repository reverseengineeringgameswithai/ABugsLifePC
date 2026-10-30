#!/usr/bin/env python3
"""Map original PC levels as complete Blender reference scenes (EXP-20260927-001).

Each level gets a fresh folder: exact-source inputs, decoded pages, one
original-map.json (version 2), import-report.json, README.md, level.blend,
overview.png and blender-check.json. Pickup Y comes from original 00456A90
and creature/start floor heights from 004ABE00, both executed offline in
Unicorn on the hash-locked retail executable. No game runs; no original or
existing project is modified.
"""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import runpy
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc import original_levels as ol  # noqa: E402
from ablpc.level_dat import LevelDat  # noqa: E402
from ablpc.level_raw import packets  # noqa: E402
from ablpc.original_level import NativeMatrices, RETAIL_EXE  # noqa: E402
from ablpc.original_population import letter_pixels  # noqa: E402
from ablpc.terrain_all import TerrainAll  # noqa: E402

EXPERIMENT = 'EXP-20260927-001'
DEFAULT_CD = ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD'
DEFAULT_EXE = ROOT/'work/copies/BUGS_PC-disc/bugs.exe'
DEFAULT_OUT = ROOT/'work/level-projects/original-levels'
LIMITS = [
    'Reference map only: nothing here is compiled back into a game file.',
    'Scenery uses stored poses; native animation selectors are recorded, not played.',
    'Sprite batches (fences, berries, billboards) are drawn as crossed planes; the game turns them to face the camera.',
    'Pickups sit at original 00456A90 initialized XYZ; stored rows are kept on each object.',
    'Creatures use their original RAW 0x102 models in stored pose at literal stored XYZ; every slot is shown, '
    'including spawns the game gates by script or lesson. Headings and movement are not simulated.',
    'Creature names come only from earlier Anthill/Training evidence; other types keep numeric names. '
    '"Looks like" hints describe model appearance only, not identity or behaviour.',
    'Trailing per-corner normal tables in creature models are recorded as metadata; lighting is not reproduced.',
    'Texture/vertex-colour preview is not a reproduction of the native renderer or lighting.',
]


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def folder_name(engine):
    name, progression = ol.LEVELS[engine]
    return f'{progression:02d}-{slug(name)}' if progression is not None else f'engine{engine}-special-stage'


def native_probe(terrain, exe):
    spec = importlib.util.spec_from_file_location('retail_probe', ROOT/'scripts/terrain-retail-probe.py')
    native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
    original = native.load_source
    native.load_source = lambda key: TerrainAll.parse(terrain) if key == 'level01' else original(key)
    try:
        ref = native.RetailProbe('level01', native.p.load_text(exe))
    finally:
        native.load_source = original
    return native, ref


def signed(value):
    return value-2**32 if value >= 2**31 else value


def floor(native, ref, x, y, z):
    """Original 004ABE00 floor below the runtime point, as 0041C420 calls it; stored units."""
    point = native.p.FIXTURE+0x3000
    native.p.put(ref.cpu, point, '3i', x, y, z)
    call = ref.call(0x4abe00, (point, 0))
    value = signed(call['eax_at_stop'])
    return (None if abs(value) > 10_000_000 else value/32), call['instruction_count']


def start_height(native, ref, x, z):
    """0043E6B0: Y=0x80000000, 004AC460 floor, minus 0x100; stored units."""
    point = native.p.FIXTURE+0x3000
    native.p.put(ref.cpu, point, '3I', x & 0xffffffff, 0x80000000, z & 0xffffffff)
    call = ref.call(0x4ac460, (point,))
    value = signed(call['eax_at_stop'])
    if abs(value) > 10_000_000:
        raise ValueError('Flik start has no native floor')
    return (value-0x100)/32, call['instruction_count']


def populate(engine, inputs, scene, exe_path, image, pe):
    native, ref = native_probe(inputs['terrain'], exe_path)
    dat = inputs['dat']
    top = next(r for r in LevelDat.parse(dat).top_records if r.type_id == 0x3f)
    table = dat[top.offset:top.offset+4+top.count*16]
    pointer = native.p.FIXTURE+0x4000
    ref.cpu.mem_write(pointer, table); native.p.put(ref.cpu, 0x5c595c, 'I', pointer)
    ref.cpu.mem_write(0x4c6a88, pe.get_data(0xc6a88, 64))
    init = ref.call(0x456a90, ())
    ol.initialized_pickups(scene['pickups'], top.offset, bytes(ref.cpu.mem_read(pointer, len(table))))
    heights = []
    for row in scene['creatures']:
        x, y, z = row['position']
        row['native_floor_y'], count = floor(native, ref, x*32, y*32, z*32)
        heights.append(dict(slot=row['slot'], floor_y=row['native_floor_y'], instructions=count))
    start = ol.spawn(image, pe, engine)
    start['native_start_y'], count = start_height(native, ref, *start['runtime_xz'])
    start['height_rule'] = '0043E6B0: Y=0x80000000 through 004AC460, minus 0x100'
    scene['spawn'] = start
    return dict(loader=ref.loader, initializer=ref.initializer, pickup_initializer=init,
                creature_floor_queries=heights, start_floor_instructions=count)


def letters(raw):
    """Native frame-zero FLIK pixels (packet 0x22 tiles 16..19, page 29 palette bank 7)."""
    rows, _ = packets(raw)
    def find(tag, ident=None):
        found = [p for _, _, p in rows if struct.unpack_from('<I', p)[0] == tag
                 and (ident is None or len(p) >= 8 and struct.unpack_from('<I', p, 4)[0] == ident)]
        return found[0] if len(found) == 1 else None
    page = find(29)
    if page is None:
        return {}
    try:
        _, _, _, palette, _ = ol.texture_image(page)
    except ValueError:
        return {}
    result = {}
    for tile in range(16, 20):
        strip = find(0x22, tile)
        if strip is not None:
            try:
                result[str(tile)] = letter_pixels(strip, palette)
            except ValueError:
                pass
    return result


def title(engine):
    name, progression = ol.LEVELS[engine]
    _, dat, _, _ = ol.sources(engine)
    where = f'progression {progression}' if progression is not None else 'no carousel position'
    return f'{name} • {where} • engine {engine} • {dat}'


def readme(scene, report):
    c = scene['counts']
    creature_lines = '\n'.join(f'- {n}: {k}' for k, n in report['creature_census'].items())
    pickup_lines = '\n'.join(f'- {n}: {k}' for k, n in sorted(report['pickup_census'].items()))
    return (f'# {scene["title"]}\n\nOriginal PC reference map ({EXPERIMENT}). Open level.blend, or run\n'
            f'`.venv/bin/python scripts/original-map.py edit <this folder>` for the N → ABLPC Map sidebar.\n\n'
            f'Sources: {", ".join(report["sources"].values())} (SHA-256 in import-report.json).\n\n'
            f'## Contents\n\n- {c["drawn_objects"]} scene records drawn ({c["mesh_objects"]} meshes, '
            f'{c["sprite_objects"]} sprite batches with {c["sprite_quads"]} quads), '
            f'{c["undispatched_records"]} undispatched record(s) kept as markers\n'
            f'- {c["pickups"]} pickups at native-initialized positions\n'
            f'- {c["creatures"]} creature slots with original models ({c["creature_types"]} types)\n'
            f'- Flik start from the executable spawn table\n'
            f'- {c["collision_triangles"]} collision triangles, {c["barrier_segments"]} XZ barrier segments, '
            f'{c["other_rows"]} other stored rows (hidden layers)\n\n'
            f'### Pickups\n\n{pickup_lines}\n\n### Creatures\n\n{creature_lines}\n\n'
            f'## Limits\n\n'+'\n'.join('- '+s for s in LIMITS)+'\n')


def map_level(engine, out, cd, exe_path, blender):
    image = exe_path.read_bytes()
    if ol.digest(image) != RETAIL_EXE:
        raise ValueError('Expected the exact retail PC executable')
    import pefile
    pe = pefile.PE(data=image)
    final = out/folder_name(engine)
    if final.exists() or final.is_symlink():
        raise ValueError(f'Refusing to overwrite existing mapping project {final}')
    inputs = ol.read_inputs(cd, engine)
    matrices = NativeMatrices(image)
    scene, textures = ol.extract(engine, inputs, matrices)
    native = populate(engine, inputs, scene, exe_path, image, pe)
    scene.update(experiment=EXPERIMENT, title=title(engine), letters=letters(inputs['raw']),
                 preview_kinds={str(k): v for k, v in ol.PREVIEW_KINDS.items()},
                 creature_packet_offset=next(o for o, _, p in packets(inputs['raw'])[0]
                                             if struct.unpack_from('<I', p)[0] == 0x23), limits=LIMITS)
    _, *paths = ol.sources(engine)
    report = dict(format='ablpc.original-map-report', version=2, experiment=EXPERIMENT, engine=engine,
                  title=scene['title'], sources=dict(zip(('dat', 'raw', 'terrain'), paths)),
                  hashes=dict(zip(('dat', 'raw', 'terrain'), ol.SOURCE_SHA256[engine])),
                  executable_sha256=RETAIL_EXE, native_matrix_function='0x00463C80',
                  native_matrix_cases=len(matrices.cache), native=native, spawn=scene['spawn'],
                  counts=scene['counts'], dispatches=scene['dispatches'], textures=scene['textures'],
                  unavailable_pages=scene['unavailable_pages'],
                  pickup_census={f'0x{s:02X} {label}': n for (s, label), n in sorted(
                      Counter((p['selector'], p['label']) for p in scene['pickups']).items())},
                  creature_census={f'type {t} {name or ("(looks like: "+hint+")" if hint else "(unnamed)")}': n
                                   for (t, name, hint), n in sorted(Counter(
                                       (c['type'], c['name'], c['appearance']) for c in scene['creatures']).items(),
                                       key=lambda item: item[0][0])},
                  creature_models={k: dict(packet_offset=m['packet_offset'], payload_sha256=m['payload_sha256'],
                                           vertices=len(m['vertices']), faces=len(m['faces']),
                                           normal_tables=[p['normal_table'] for p in m['parts'] if p['normal_table']],
                                           opaque=m['opaque'])
                                   for k, m in scene['creature_models'].items()},
                  undispatched=[{k: v for k, v in r.items()} for r in scene['undispatched']],
                  terrain_other=scene['terrain_other'], dat_structure=scene['dat_structure'],
                  raw_structure=scene['raw_structure'], letters=sorted(scene['letters']), limits=LIMITS)
    out.mkdir(parents=True, exist_ok=True)
    staging = out/f'.{final.name}.partial'
    if staging.exists():
        shutil.rmtree(staging)
    (staging/'inputs').mkdir(parents=True); (staging/'textures').mkdir()
    for key, relative in zip(('dat', 'raw', 'terrain'), paths):
        (staging/'inputs'/Path(relative).name).write_bytes(inputs[key])
    for page, content in textures.items():
        (staging/'textures'/f'page-{page:02d}.png').write_bytes(content)
    (staging/'original-map.json').write_text(json.dumps(scene, separators=(',', ':'))+'\n')
    (staging/'import-report.json').write_text(json.dumps(report, indent=2)+'\n')
    (staging/'README.md').write_text(readme(scene, report))
    command = blender+['--background', '--factory-startup', '--disable-autoexec', '--python-exit-code', '1',
                       '--python', str(ROOT/'tools/blender/original_level_map.py'), '--', str(staging)]
    subprocess.run(command, check=True, timeout=3600, stdout=subprocess.DEVNULL if not VERBOSE else None)
    check = json.loads((staging/'blender-check.json').read_text())
    report['blend_sha256'] = check['blend_sha256']
    (staging/'import-report.json').write_text(json.dumps(report, indent=2)+'\n')
    staging.rename(final)
    print(json.dumps(dict(engine=engine, project=str(final), **{k: check[k] for k in (
        'saved_objects', 'source_objects_verified', 'pickups_and_creatures_verified', 'collision_triangles_verified')})),
        flush=True)
    return final


VERBOSE = False


def publish(out, report_path):
    """Asset-free metadata for every mapped level: hashes, counts and native receipts."""
    levels = []
    for engine in sorted(ol.LEVELS):
        project = out/folder_name(engine)
        if not (project/'import-report.json').exists():
            continue
        report = json.loads((project/'import-report.json').read_text())
        check = json.loads((project/'blender-check.json').read_text())
        levels.append(dict(
            engine=engine, folder=f'work/level-projects/{out.name}/{project.name}', title=report['title'],
            sources=report['sources'], hashes=report['hashes'], counts=report['counts'],
            dispatches=report['dispatches'], pickup_census=report['pickup_census'],
            creature_census=report['creature_census'], unavailable_pages=report['unavailable_pages'],
            undispatched=[{k: r[k] for k in ('id', 'flags', 'record_offset', 'object_offset', 'geometry_offset')}
                          for r in report['undispatched']],
            spawn=report['spawn'], textures=[{k: t[k] for k in ('page', 'width', 'packet_offset', 'packet_sha256')}
                                             for t in report['textures']],
            creature_models={k: {n: m[n] for n in ('packet_offset', 'payload_sha256', 'vertices', 'faces')}
                             | dict(normal_tables=len(m['normal_tables']),
                                    opaque_kinds=dict(Counter(str(o['kind']) for o in m['opaque'])))
                             for k, m in report['creature_models'].items()},
            native=dict(pickup_initializer=report['native']['pickup_initializer'],
                        start_floor_instructions=report['native']['start_floor_instructions'],
                        creature_floor_queries=len(report['native']['creature_floor_queries'])),
            blender={k: check[k] for k in ('blend_sha256', 'saved_objects', 'source_objects_verified',
                                            'source_vertices_verified', 'polygons_verified',
                                            'pickups_and_creatures_verified', 'collision_triangles_verified',
                                            'packed_textures', 'degenerate_faces_dropped', 'hidden_layers',
                                            'blender_version', 'save_reopen')}))
    totals = {key: sum(level['counts'][key] for level in levels)
              for key in ('scene_records', 'drawn_objects', 'undispatched_records', 'pickups', 'creatures',
                          'other_rows', 'collision_triangles')}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(dict(experiment=EXPERIMENT, executable_sha256=RETAIL_EXE,
                                           file_rule='004671D0: engine 1..10 LEVELnn/LEVEL.*+TERRAIN.ALL; '
                                                     '11..17 LEVEL(n-10)/LEVEL1.*+TERR1.ALL',
                                           appearance_hints=ol.APPEARANCE, names=ol.CREATURES,
                                           limits=LIMITS, totals=totals, levels=levels), indent=1)+'\n')
    print(json.dumps(dict(report=str(report_path), levels=len(levels), **totals)))


def main():
    global VERBOSE
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--engines', default=','.join(str(n) for n in range(1, 17)),
                        help='comma-separated engine indices (default 1..16; Training 17 has its own map)')
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--cd', type=Path, default=DEFAULT_CD)
    parser.add_argument('--exe', type=Path, default=DEFAULT_EXE)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--publish-report', type=Path,
                        help='only summarize existing projects into this asset-free JSON under reports/')
    args = parser.parse_args()
    VERBOSE = args.verbose
    private = (ROOT/'work').resolve()
    for path in (args.out, args.cd, args.exe):
        if not path.resolve().is_relative_to(private):
            raise ValueError('Inputs and outputs must stay under work/')
    if not args.out.resolve().is_relative_to((ROOT/'work/level-projects').resolve()):
        raise ValueError('Mapping projects must be written under work/level-projects/')
    if args.publish_report:
        if not args.publish_report.resolve().is_relative_to((ROOT/'reports').resolve()):
            raise ValueError('Published metadata belongs under reports/')
        return publish(args.out.resolve(), args.publish_report.resolve())
    blender = runpy.run_path(str(ROOT/'scripts/original-map.py'))['blender_command']()
    engines = [int(n) for n in args.engines.split(',')]
    for engine in engines:
        map_level(engine, args.out.resolve(), args.cd.resolve(), args.exe.resolve(), blender)


if __name__ == '__main__':
    main()
