#!/usr/bin/env python3
"""Build and probe a bounded ground-ramp-box area using the banked PC pieces."""
from pathlib import Path
import argparse
import importlib.util
import json
import math
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reimplementation'))
from ablpc.terrain_all import TerrainAll
from ablpc.level_dat import LevelDat
from ablpc import terrain_play_area as area


def reference(filename,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/filename)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def build():
    grid=reference('terrain-deck-grid-probe.py','area_banked_grid')
    terrain,dat,_=grid.build(4,4,flip_top=True)
    return area.build(terrain,dat)


def walk_to(probe,target,speed,*,max_steps=300,allowed_airborne=2):
    steps=[];outcome='step-limit';best=float('inf');stalled=0
    state=probe.step((0,512,0))['after']
    for _ in range(max_steps):
        x,_,z=state['position'];dx,dz=target[0]-x,target[1]-z
        distance=math.hypot(dx,dz)
        if distance<=128:
            outcome='target-reached';break
        stalled=stalled+1 if distance>=best-16 else 0
        best=min(best,distance)
        if stalled>=20:
            outcome='blocked';break
        scale=min(1,speed/distance)
        row=probe.step((round(dx*scale),512,round(dz*scale)))
        steps.append(row);state=row['after']
    steps.extend(probe.step((0,512,0)) for _ in range(16))
    summary=reference('terrain-floor-boundary-probe.py','area_summary').summary(steps)
    summary.update(target_xz=target,speed=speed,outcome=outcome,steps=steps,
                   accepted=outcome=='target-reached' and steps[-1]['after']['flags']==[1,1]
                   and summary['longest_airborne_run']<=allowed_airborne)
    return summary


def report():
    terrain,dat,meta=build()
    boundary=reference('terrain-floor-boundary-probe.py','area_original_instructions')
    text=boundary.b.p.load_text(boundary.b.p.DEFAULT_BINARY)
    source=TerrainAll.parse(terrain)
    routes=[]
    for z in (15675,15900,16125):
        for speed in (512,900):
            probe=boundary.Probe(source,text)
            landing=probe.land(7500*32,z*32,start_y=area.DECK[4]*32-1024)
            uphill=walk_to(probe,(5425*32,z*32),speed)
            downhill=walk_to(probe,(7500*32,z*32),speed)
            routes.append({'z_stored':z,'speed':speed,'landing':landing,
                           'uphill':uphill,'downhill':downhill})
    probe=boundary.Probe(source,text)
    spawn=probe.land(197091,492897,start_y=area.DECK[4]*32-1024)
    approach=[walk_to(probe,target,900) for target in
              ((197091,15000*32),(7500*32,15000*32),(7500*32,15900*32))]
    landings=[]
    for name,x,y in (('ramp',6450,-3296),('top',5425,area.BOX[4])):
        probe=boundary.Probe(source,text)
        row=probe.land(x*32,15900*32,start_y=y*32-1024)
        landings.append({'surface':name,'landing':row,'settle':[probe.step((0,512,0)) for _ in range(12)]})
    probe=boundary.Probe(source,text)
    step_off_landing=probe.land(5250*32,15900*32,start_y=area.BOX[4]*32-1024)
    step_off=walk_to(probe,(4700*32,15900*32),900,allowed_airborne=30)
    banked=reference('terrain-deck-grid-probe.py','area_control').build(4,4,flip_top=True)[0]
    control=boundary.Probe(TerrainAll.parse(banked),text)
    control.land(7500*32,15900*32,start_y=area.DECK[4]*32-1024)
    closed_wall=walk_to(control,(5425*32,15900*32),900)
    stream=boundary.stream_instruction_audit(LevelDat.parse(dat),text)
    accepted=all(r[k]['accepted'] for r in routes for k in ('uphill','downhill'))
    accepted=accepted and all(r['accepted'] for r in approach) and step_off['accepted']
    accepted=accepted and not closed_wall['accepted']
    return {'experiment':'EXP-20260905-004','scope':'Offline original PC instructions and synthetic motion; no runtime input claim.',
            'binary_sha256':boundary.b.p.BINARY_SHA256,'fixture':meta,'accepted':accepted,
            'routes':routes,'natural_spawn_approach':{'landing':spawn,'legs':approach},
            'landings':landings,'step_off':{'landing':step_off_landing,'route':step_off},
            'banked_closed_wall_control':closed_wall,'mesh_stream_instruction_audit':stream}


def work_target(path):
    path=Path(path).resolve()
    if not path.is_relative_to((ROOT/'work/copies').resolve()):
        raise ValueError('assets must stay under work/copies')
    if path.exists():
        raise FileExistsError('choose a fresh destination')
    return path


def write_fixture(path):
    path=work_target(path);terrain,dat,meta=build();path.mkdir(parents=True)
    (path/'TERRAIN.ALL').write_bytes(terrain);(path/'LEVEL.DAT').write_bytes(dat)
    (path/'fixture.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta


def stage_game(path):
    path=work_target(path);terrain,dat,meta=build();path.mkdir(parents=True)
    source=ROOT/'work/copies/BUGS_PC-full-disc'
    subprocess.run(['cp','-a','--reflink=auto',str(source)+'/.',str(path)],check=True)
    level=path/'PC/BUGS/CD/LEVEL01'
    (level/'TERRAIN.ALL').write_bytes(terrain);(level/'LEVEL.DAT').write_bytes(dat)
    log=path/'PC/BUGS/bugs.log'
    if log.exists():log.unlink()
    rows=[]
    for original in sorted(source.rglob('*')):
        if not original.is_file():continue
        rel=original.relative_to(source)
        if str(rel).lower()=='pc/bugs/bugs.log':continue
        staged=path/rel;before=area.digest(original.read_bytes());after=area.digest(staged.read_bytes())
        if before!=after and str(rel) not in ('PC/BUGS/CD/LEVEL01/TERRAIN.ALL','PC/BUGS/CD/LEVEL01/LEVEL.DAT'):
            raise ValueError('unexpected staged file difference: '+str(rel))
        rows.append({'path':str(rel),'source_sha256':before,'staged_sha256':after})
    return {'fixture':meta,'stage':str(path),'files':rows}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-fixture',type=Path)
    parser.add_argument('--stage-game',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    result={}
    if args.report:
        measured=report()
        with args.report.open('x') as f:json.dump(measured,f,indent=2);f.write('\n')
        if not measured['accepted']:raise SystemExit('offline route gate failed; no assets staged')
        result['offline_accepted']=True
    if args.write_fixture:result['fixture']=write_fixture(args.write_fixture)
    if args.stage_game:result['staging']=stage_game(args.stage_game)
    if not result:result['fixture']=build()[2]
    print(json.dumps(result,indent=2))
