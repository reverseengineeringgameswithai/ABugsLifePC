#!/usr/bin/env python3
"""Original-PC offline loading, landing and side-contact gates for EXP-014.

Only private emulated memory is modified. Synthetic cadence/displacements are
not input, animation, bounce or an end-to-end game replay. No live access.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_scenery import digest, scene_pointer_fields, read_mesh


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--experiment', default='EXP-20260906-014')
    args = parser.parse_args()
    if args.report.exists() or not args.report.resolve().is_relative_to((ROOT/'work').resolve()):
        parser.error('report must be fresh under work')
    started = time.monotonic(); build = json.loads(args.build.read_text())
    files = {n: (args.fixture/n).read_bytes() for n in build['hashes']}
    assert all(digest(files[n]) == h for n, h in build['hashes'].items())
    old_path = ROOT/'work/copies/EXP-20260906-012/fixture'
    old_files = {n: (old_path/n).read_bytes() for n in build['base_hashes']}
    assert all(digest(old_files[n]) == h for n, h in build['base_hashes'].items())
    native = module('scenery_clearance', 'terrain-wall-clearance-probe.py')
    m = native.native_module(); text = m.p.load_text(m.p.DEFAULT_BINARY)
    original = m.load_source('level01'); terrain = TerrainAll.parse(files['TERRAIN.ALL'])
    plant = TerrainAll.parse(files['PLANTTER.ALL'])
    retail = native.Stepper(m, original, text)
    loader = m.load_source
    m.load_source = lambda key: plant if key == 'plantter' else loader(key)
    try:
        added = native.Stepper(m, terrain, text)
    finally:
        m.load_source = loader
    rows = []
    result = {'experiment': args.experiment, 'binary_sha256': m.p.BINARY_SHA256,
              'hashes': build['hashes'], 'arms': rows,
              'scope': 'original PC instructions in offline synthetic memory; no live writes/input; not GPU or end-to-end gameplay acceptance'}

    def arm(name, function, *, required=True):
        try:
            value = function()
            assert type(value['accepted']) is bool
        except Exception as error:
            value = {'accepted': False, 'error': f'{type(error).__name__}: {error}'}
        rows.append({'name': name, 'required': required, **value})
        print(json.dumps({'name': name, 'accepted': value['accepted'], 'error': value.get('error')}), flush=True)

    def preservation():
        old = TerrainAll.parse(old_files['TERRAIN.ALL'])
        assert len(terrain.records) == len(old.records)+len(build['additions'])
        for r in old.records:
            new = terrain.records[r.index]
            assert r.raw == new.raw
            assert old.data[r.payload_offset:r.payload_offset+r.payload_size] == terrain.data[new.payload_offset:new.payload_offset+new.payload_size]
        assert terrain.suffix == old.suffix
        assert files['PLANTTER.ALL'] == old_files['PLANTTER.ALL']
        p = added.probe
        pointers = []
        for row in build['additions']:
            index = row['source_indices'][0]; r = terrain.records[index]
            matching = [i for i in range(p.loaded_count)
                        if m.p.get(p.cpu, m.p.DESCRIPTORS+48*i+16, 'I')[0] == m.SOURCE_BASES[0]+r.payload_offset]
            assert len(matching) == 1
            i = matching[0]; ptr = m.p.get(p.cpu, m.p.DESCRIPTORS+48*i+16, 'I')[0]
            assert p.tags()[i] == 6
            assert bytes(p.cpu.mem_read(ptr, r.payload_size)) == terrain.collision_payload(index).raw
            pointers.append({'source': index, 'runtime_descriptor': i, 'tag': 6})
        return {'accepted': True, 'loaded_count': p.loaded_count, 'boundary': p.boundary,
                'new_descriptors': pointers, 'old_payloads_records_plant_file_preserved': True}
    arm('collision_loader_and_preservation', preservation)

    def render_relocation():
        rel = module('scenery_relocate', 'terrain-texture-tiling-probe.py')
        image = m.p.DEFAULT_BINARY.read_bytes(); old = old_files['LEVEL.DAT']; new = files['LEVEL.DAT']
        d, fields = scene_pointer_fields(old); delta = 20*len(build['additions'])
        before, bg = rel.relocate(image, old); after, ag = rel.relocate(image, new)
        out = bytearray(after[:d.primary_sentinel_offset]+after[d.primary_sentinel_offset+delta:len(old)-4+delta])
        for f in fields:
            struct.pack_into('<I', out, f, struct.unpack_from('<I', out, f)[0]-delta)
        assert bytes(out) == before[:-4]
        assert ag['trailing_data_pointer'] == bg['trailing_data_pointer']+delta
        assert ag['trailer_table_sha256'] == bg['trailer_table_sha256']
        parsed = LevelDat.parse(new); meshes=[]
        for row in build['additions']:
            r = parsed.primary_records[row['scene_indices'][0]]; o = r.payload_offset_candidate
            geo = struct.unpack_from('<I', new, o+28)[0]; mesh = read_mesh(new, geo)
            assert struct.unpack_from('<I', after, r.offset+16)[0] == rel.BASE+o
            assert struct.unpack_from('<I', after, o+28)[0] == rel.BASE+geo
            assert after[geo:geo+len(mesh)] == mesh and digest(mesh) == row['mesh_sha256']
            assert new[r.offset+14:r.offset+16] == b'\x19\x00'
            meshes.append({'scene': r.index, 'object': o, 'mesh': geo, 'bytes': len(mesh)})
        return {'accepted': True, 'new_meshes': meshes, 'original_relocated_bytes_preserved_modulo_rebase': True}
    arm('render_relocation_and_preservation', render_relocation)

    for row in build['additions']:
        source, target = row['donor_source'], row['source_indices'][0]
        delta = tuple(v*32 for v in row['translations_stored'][0])
        r = original.records[source]
        def landing(row=row, source=source, target=target, delta=delta):
            # Center of the source render bound, above cap; new start translates
            # the complete original start so the comparison includes identical cadence.
            dat = LevelDat.from_path(m.SOURCE_ROOT/'CD/LEVEL01/LEVEL.DAT')
            scene = dat.primary_records[row['donor_scene']]
            x, z = scene.center_component_00*32, scene.center_component_08*32
            start = (x, -180000, z); traces=[]
            for stepper, offset in ((retail, (0,0,0)), (added, delta)):
                stepper.reset(tuple(start[k]+offset[k] for k in range(3))); samples=[]
                for _ in range(240):
                    s = stepper.step((0,1400,0)); samples.append(s)
                    if s['flags'][1]:break
                samples += [stepper.step((0,512,0)) for _ in range(4)]
                traces.append(samples)
            a,b = traces
            assert a[-1]['contact']['source_record'] == source, a[-1]
            assert b[-1]['contact']['source_record'] == target, b[-1]
            assert len(a)==len(b)
            errors=[max(abs(bi['position'][k]-delta[k]-ai['position'][k]) for k in range(3)) for ai,bi in zip(a,b)]
            assert max(errors)==0 and all(ai['flags']==bi['flags'] for ai,bi in zip(a,b))
            return {'accepted': True, 'source': source, 'target': target, 'maximum_world_error': max(errors), 'control': a, 'new': b}
        arm(f'landing-{target}', landing)

        def sides(control=retail, source=source, target=target, delta=delta, r=r):
            cases=[]
            cells=[c for g in original.collision_payload(source).groups for c in g.cells
                   if max(abs(c.words[0]),abs(c.words[2])) > abs(c.words[1])]
            # Four most lateral-facing cells, distinct normal quadrants where available.
            for axis, sign in ((0,1),(0,-1),(2,1),(2,-1)):
                c=max(cells,key=lambda c:sign*c.words[axis])
                w=c.words; normal=(w[0],w[2]); length=math.hypot(*normal)
                if not length:continue
                outward=(round(normal[0]/length*4096),round(normal[1]/length*4096))
                start=[r.world_base[k]+(3*w[3+k]+w[6+k]+w[9+k])*32//3 for k in range(3)]
                start[0]+=outward[0];start[1]+=3200;start[2]+=outward[1]
                move=(-round(normal[0]/length*512),0,-round(normal[1]/length*512))
                traces=[]
                for stepper, offset in ((control,(0,0,0)),(added,delta)):
                    stepper.reset(tuple(start[k]+offset[k] for k in range(3)))
                    traces.append([stepper.step(move) for _ in range(18)])
                a,b=traces
                errors=[max(abs(bi['position'][k]-delta[k]-ai['position'][k]) for k in range(3)) for ai,bi in zip(a,b)]
                response=max(abs(a[-1]['position'][k]-start[k]-18*move[k]) for k in range(3))
                cases.append({'axis':axis,'sign':sign,'cell':c.offset,'maximum_world_error':max(errors),
                              'response_from_free_motion':response,'control':a,'new':b,
                              'accepted':max(errors)==0 and response>0})
            return {'accepted':len(cases)==4 and all(c['accepted'] for c in cases), 'cases':cases}
        arm(f'sides-{target}', sides, required=source != 146)
        if source == 146:
            # native-02 retains the complete-scene counterexample: its west
            # approach also contacts source108 floor at file82120. Remove only
            # that floor's first marker in a private control, keeping the donor
            # and candidate byte-identical. This does not change either fixture.
            stripped=bytearray(original.data)
            struct.pack_into('<h', stripped, original.records[108].payload_offset, -1)
            isolated=native.Stepper(m, TerrainAll.parse(bytes(stripped)), text)
            arm(f'sides-{target}-control-without-floor108', lambda: sides(control=isolated))
        def grounded(row=row, target=target):
            # Same authored floor and other props, remove only this new shell.
            missing=bytearray(terrain.data)
            struct.pack_into('<h', missing, terrain.records[target].payload_offset, -1)
            saved=m.load_source
            m.load_source=lambda key: plant if key == 'plantter' else saved(key)
            try:
                absent=native.Stepper(m,TerrainAll.parse(bytes(missing)),text)
            finally:
                m.load_source=saved
            scene=LevelDat.parse(files['LEVEL.DAT']).primary_records[row['scene_indices'][0]]
            center=(scene.center_component_00, scene.center_component_08)
            cases=[]
            for axis,sign in ((0,1),(0,-1),(2,1),(2,-1)):
                x,z=center
                if axis==0:x+=sign*1100
                else:z+=sign*1100
                traces=[]
                move=(-sign*512,512,0) if axis==0 else (0,512,-sign*512)
                for stepper in (added,absent):
                    land=stepper.land(x,z)
                    push=[stepper.step(move) for _ in range(70)]
                    retreat=[stepper.step((-move[0],512,-move[2])) for _ in range(24)]
                    settle=[stepper.step((0,512,0)) for _ in range(6)]
                    traces.append({'landing':land,'push':push,'retreat':retreat,'settle':settle})
                a,b=traces
                separation=max(abs(a['push'][-1]['position'][k]-b['push'][-1]['position'][k]) for k in (0,2))
                returned=a['settle'][-1]['contact']
                okay=separation>1024 and returned is not None and returned['source_record']==99
                cases.append({'axis':axis,'sign':sign,'accepted':okay,'xz_separation_from_no_prop':separation,
                              'candidate':a,'same_floor_without_prop':b})
            return {'accepted':all(c['accepted'] for c in cases),'cases':cases}
        arm(f'grounded-push-return-{target}',grounded)
    result['known_complete_scene_difference']='Small donor west approach in original world also contacts source108 floor (82120), absent from isolated mod. Complete-scene mismatch is retained as non-required observation; the explicit floor108-removal discriminator is required.'
    result['seconds']=time.monotonic()-started;result['accepted']=all(r['accepted'] for r in rows if r['required'])
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.report.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'accepted':result['accepted'],'seconds':result['seconds']}))
    return 0 if result['accepted'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
