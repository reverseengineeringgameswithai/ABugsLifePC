"""Execute PC terrain loader/movement/result reader with the exact exit build.

Private Unicorn fixtures only. No live process input, writes or execution control.
Normal actor animation/input and the completion UI are outside this probe.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import struct
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'reimplementation'))
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_floor_patch import floor_cells
from ablpc.terrain_isolated import pe_file_offset, isolate_collision


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    here=ROOT/'work/experiments/EXP-20260907-005'
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,default=here/'native.json')
    output=parser.parse_args().report.resolve()
    if not output.is_relative_to((ROOT/'work').resolve()):raise ValueError('Private work output required')
    if output.exists():raise ValueError('Refusing existing evidence receipt')
    clearance=module('exit_clearance',ROOT/'scripts/terrain-wall-clearance-probe.py')
    m=clearance.native_module()
    text=m.p.load_text(m.p.DEFAULT_BINARY)
    retail=m.load_source('level01')
    stage=ROOT/'work/copies/EXP-20260907-004/preview-03/game/PC/BUGS/CD'
    terrain=TerrainAll.from_path(stage/'LEVEL01/TERRAIN.ALL')
    plant=TerrainAll.from_path(stage/'BITS/PLANTTER.ALL')
    image=(ROOT/'work/copies/EXP-20260907-005/bugs.exe').read_bytes()
    build=json.loads((ROOT/'work/copies/EXP-20260907-005/bugs.exit.json').read_text())
    assert hashlib.sha256(image).hexdigest()==build['output_sha256']
    point=json.loads((here/'requested-exit-position.json').read_text())['first']['position']
    assert point==build['settings']['center_world']

    def make(ground,custom=False):
        original=m.load_source
        m.load_source=lambda key: plant if key=='plantter' and ground is terrain else original(key)
        try:s=clearance.Stepper(m,ground,text)
        finally:m.load_source=original
        p=s.probe
        if custom:
            for address,size in ((0x4bba00,256),(0x4408ac,5)):
                off=pe_file_offset(image,address,size)
                p.cpu.mem_write(address,image[off:off+size])
        m.p.put(p.cpu,0x861c84,'I',1)
        p.baseline=bytes(p.cpu.mem_read(*m.IMAGE))
        return s

    def result(s,custom=False):
        p=s.probe
        m.p.put(p.cpu,0x59d910,'3i',*s.state()['position'])
        p.cpu.mem_write(0x59d992,bytes(s.state()['flags']))
        return p.call(0x4bba24 if custom else 0x4acf90,(0,0x59d992))['eax_at_stop']

    # The first full-retail vertical drops hit source164, not177 (native.json).
    # Keep that negative control; isolate ONLY the original triangle stream to
    # discriminate its result. This does not claim a natural route to OG exit.
    isolated,_=isolate_collision(retail.data,{177:[g.offset for g in retail.collision_payload(177).groups]})
    original_exit=[]
    for scope,ground in (('full_retail_vertical_drop',retail),('isolated_original_exit',TerrainAll.parse(isolated))):
        og=make(ground)
        for cell in floor_cells(retail):
            if cell.source!=177:continue
            x,z=(sum(v[i] for v in cell.vertices)//3 for i in (0,2))
            y=min(v[1] for v in cell.vertices)*32-30000
            og.reset((x*32,y,z*32))
            samples=[]
            for _ in range(80):
                samples.append(og.step((0,1400,0)))
                if samples[-1]['flags'][1]:break
            value=result(og)
            original_exit.append({'scope':scope,'cell':cell.offset,'state':og.state(),'native_result':value,
                                  'accepted':value==(0 if ground is retail else 2),'movement_steps':len(samples)})

    pairs=[]
    # Saved point and a normal downward-ramp approach from beyond the new box.
    for label,start,steps in (
        ('saved_position',(point[0],point[1]-20000,point[2]),[(0,1400,0)]*36),
        ('walk_from_ramp',(point[0],-125000,point[2]+18000),[(0,1400,0)]*36+[(0,512,-512)]*48),
        ('jump_above_saved_point',(point[0],point[1]-20000,point[2]),[(0,-512,0)]*8),
    ):
        arms=[]
        for custom in (False,True):
            s=make(terrain,custom)
            s.reset(start)
            rows=[]
            for delta in steps:
                state=s.step(delta)
                rows.append({**state,'native_result':result(s,custom)})
            arms.append(rows)
        geometry_equal=all({k:v for k,v in a.items() if k!='native_result'}==
                           {k:v for k,v in b.items() if k!='native_result'}
                           for a,b in zip(*arms,strict=True))
        hits=[i for i,s in enumerate(arms[1]) if s['native_result']==2]
        expected=label!='jump_above_saved_point'
        assert geometry_equal and bool(hits)==expected
        assert all(s['native_result']==0 for s in arms[0])
        if label=='walk_from_ramp':
            assert hits and hits[0]>36
            for s in arms[1]:
                if s['native_result']==2:
                    assert s['flags']==[1,1] and all(abs(a-b)<=h for a,b,h in
                        zip(s['position'],point,build['settings']['half_extent_world'],strict=True))
        pairs.append({'case':label,'geometry_contact_equal':geometry_equal,'first_exit_sample':hits[0] if hits else None,
                      'accepted':True,'control':arms[0],'candidate':arms[1]})
    report={'experiment':'EXP-20260907-005','retail_sha256':m.p.BINARY_SHA256,
            'candidate_sha256':build['output_sha256'],'terrain_sha256':hashlib.sha256(terrain.data).hexdigest(),
            'plant_sha256':hashlib.sha256(plant.data).hexdigest(),'original_exit':original_exit,'pairs':pairs,
            'accepted':all(r['accepted'] for r in original_exit+pairs),'scope':__doc__}
    with output.open('x') as f:f.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'accepted':report['accepted'],'original_exit':original_exit,
                      'pairs':[{k:v for k,v in row.items() if k not in ('control','candidate')} for row in pairs]},indent=2))
    return 0 if report['accepted'] else 1


if __name__=='__main__':raise SystemExit(main())
