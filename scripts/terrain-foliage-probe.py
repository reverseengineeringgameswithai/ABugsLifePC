#!/usr/bin/env python3
"""Original-PC acceptance arms for grass reuse, EXP-20260906-006.

Collision containment and release/return are separate from instantaneous flags.
The original grass-boundary control also reports [1,0] during blocked pushes.
All setup writes are to private Unicorn memory, never a running game.
"""
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys
import time

from unicorn import UC_HOOK_CODE

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_foliage import decode_mesh, mesh_bytes
from ablpc.terrain_isolated import digest

OUTLINE = ((4064,13064),(5814,13064),(5814,10964),(6186,10964),
           (6186,13064),(8236,13064),(8236,18036),(4064,18036),(4064,13064))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def over_floor(state):
    x, _, z = state['position']
    return ((128000 <= x <= 265600 and 416000 <= z <= 579200)
            or (184000 <= x <= 200000 and 348800 <= z <= 416000))


def normal(a, b):
    dx, dz = b[0]-a[0], b[1]-a[1]
    length = math.hypot(dx,dz)
    return -dz/length,dx/length


def main():
    output = ROOT / 'work/experiments/EXP-20260906-006/grass-native.json'
    if output.exists():
        raise ValueError('refusing to replace native evidence')
    fixture = ROOT / 'work/copies/EXP-20260906-006/grass-fixture'
    dat = (fixture/'LEVEL.DAT').read_bytes()
    terrain = TerrainAll.from_path(fixture/'TERRAIN.ALL')
    plant = TerrainAll.from_path(fixture/'PLANTTER.ALL')
    assert digest(dat) == '0cd3e85e5bc65c2791a05c5435c05ca194fb0d2508f45233bed325a5c3566b44'
    assert digest(terrain.data) == '56c167c1786b9fa3bf91963efd5334996a8e6a28d8ca633b66aefacdde9f02ba'
    c = module('grass_clearance', 'scripts/terrain-wall-clearance-probe.py')
    m = c.native_module()
    text = m.p.load_text(m.p.DEFAULT_BINARY)
    original = m.load_source
    m.load_source = lambda key: plant if key == 'plantter' else original(key)
    try:
        stepper = c.Stepper(m,terrain,text)
    finally:
        m.load_source = original
    report = {'experiment':'EXP-20260906-006','model':'original PC instructions, synthetic offline paths',
              'terrain_sha256':digest(terrain.data),'level_dat_sha256':digest(dat),
              'criteria':'Every push/idle/retreat sample remains over authored footprint; no unbounded descent; grounded retreat finishes [1,1]. Airborne arms retain independent height. Tangential sliding allowed; flags while pushing retained, not used alone as escape.',
              'cases':[],'live_actions':[]}
    started = time.monotonic()
    cases=[]
    for i,(a,b) in enumerate(zip(OUTLINE,OUTLINE[1:])):
        nx,nz=normal(a,b)
        cases.append((f'edge-{i}',round((a[0]+b[0])/2+nx*128),
                      round((a[1]+b[1])/2+nz*128),nx,nz))
    for i,point in enumerate(OUTLINE[:-1]):
        a=normal(OUTLINE[i-1] if i else OUTLINE[-2],point)
        b=normal(point,OUTLINE[i+1]);length=math.hypot(a[0]+b[0],a[1]+b[1])
        nx,nz=(a[0]+b[0])/length,(a[1]+b[1])/length
        cases.append((f'corner-{i}',round(point[0]+nx*128),round(point[1]+nz*128),nx,nz))
    updates=[]
    hook=stepper.probe.cpu.hook_add(UC_HOOK_CODE,lambda cpu,pc,size,data:updates.append(pc),
                                  begin=0x004A9787,end=0x004A9787)
    try:
        for name,x,z,nx,nz in cases:
            for air in (False,True):
                landing=stepper.land(x,z)
                if air:
                    p=stepper.state()['position'];stepper.reset((p[0],p[1]-12000,p[2]))
                initial=stepper.state()
                dx,dz=round(-nx*1200),round(-nz*1200)
                updates.clear()
                push=[stepper.step((dx,0 if air else 512,dz)) for _ in range(64)]
                count=len(updates)
                idle=[stepper.step((0,0 if air else 512,0)) for _ in range(8)]
                retreat=[stepper.step((-dx,0 if air else 512,-dz)) for _ in range(6)]
                settled=[stepper.step((0,0 if air else 512,0)) for _ in range(8)]
                trace=push+idle+retreat+settled
                contained=all(over_floor(s) for s in trace)
                # All authored floors lie above world Y=-93000; a fall through
                # that lower envelope rejects independently of cached contacts.
                no_descent=all(s['position'][1] < -92000 for s in trace)
                recovered=air or settled[-1]['flags']==[1,1]
                accepted=contained and no_descent and count>0 and recovered
                row={'name':name,'airborne_setup':air,'initial':initial,'landing':landing,
                     'push':push,'idle':idle,'retreat':retreat,'settled':settled,
                     'segment_updates':count,'over_floor':contained,
                     'above_lower_floor_envelope':no_descent,'settled_grounded_return':recovered,
                     'accepted':accepted}
                report['cases'].append(row)
                print(json.dumps({k:row[k] for k in ('name','airborne_setup','over_floor','above_lower_floor_envelope','settled_grounded_return','accepted')}),flush=True)
    finally:
        stepper.probe.cpu.hook_del(hook)
    report['ramp_routes']=[]
    for lane in (5850,6000,6150):
        landing=stepper.land(lane,14000)
        legs=[stepper.walk_z(target,lane) for target in (11200,14000,11200,14000)]
        report['ramp_routes'].append({'lane':lane,'landing':landing,'legs':legs,
                                     'accepted':all(r['accepted'] for r in legs)})
    relocate=module('grass_relocation','scripts/terrain-texture-tiling-probe.py')
    image=(ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe').read_bytes()
    relocated,globals_=relocate.relocate(image,dat)
    mesh,ref=mesh_bytes(dat,160)
    vertices,groups=decode_mesh(mesh)
    report['relocation']={'accepted':relocated[ref.geometry_offset:ref.geometry_offset+len(mesh)]==mesh
                        and struct.unpack_from('<I',relocated,ref.object_offset+20)[0]==relocate.BASE+ref.geometry_offset,
                        'globals':globals_,'vertex_count':len(vertices),
                        'groups':[(tag,len(faces)) for tag,faces in groups]}
    boundary=module('grass_stream','scripts/terrain-floor-boundary-probe.py')
    report['native_mesh_stream']=boundary.stream_instruction_audit(LevelDat.parse(dat),text)
    report['seconds']=time.monotonic()-started
    report['accepted']=all(r['accepted'] for r in report['cases']) and all(r['accepted'] for r in report['ramp_routes']) and report['relocation']['accepted']
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'accepted':report['accepted'],'cases_accepted':sum(r['accepted'] for r in report['cases']),
                      'ramp_routes':[r['accepted'] for r in report['ramp_routes']],
                      'native_mesh_stream':report['native_mesh_stream'],'seconds':report['seconds']}),flush=True)
    return 0 if report['accepted'] else 1


if __name__=='__main__':
    raise SystemExit(main())
