#!/usr/bin/env python3
"""Build EXP-20260906-003 with independent collision-only and trim-only controls."""
from pathlib import Path
import hashlib,json,shutil,struct,time
from fractions import Fraction

from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_additive import append_collision_groups,append_render_geometry
from ablpc.terrain_ramp_solid import render_profile,trim_side_mesh,side_collision

ROOT=Path(__file__).resolve().parents[1]
EXP="EXP-20260906-003"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    if isinstance(value,Fraction):
        return {"numerator":value.numerator,"denominator":value.denominator}
    raise TypeError(type(value).__name__)


def main():
    start=time.monotonic();out=ROOT/"work/copies"/EXP;report=ROOT/"reports/terrain"/(EXP+".json")
    if out.exists() or report.exists():raise ValueError("fresh experiment output required")
    base=ROOT/"work/copies/EXP-20260906-001/fixture";control=ROOT/"work/copies/EXP-20260906-002/fixture"
    terrain=(base/"TERRAIN.ALL").read_bytes();dat=(base/"LEVEL.DAT").read_bytes();walls=(control/"side-faces.mesh").read_bytes();control_dat=(control/"LEVEL.DAT").read_bytes()
    original=(ROOT/"work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT").read_bytes()
    expected=["77a77456c3b9a0f4db5e7b20d257a9772e04c0f0ed3d0812590943d630851698","691674fdca9b87a95f477bfb144f9ff6d805fecc05785669c68162c8f4f17659","574a375fbc83d4757159f3c61672a7df8af9e209269e27420e19c18823a901be","8469172e17592544c75fc572b2dc99eb0729ee8f9edc20c6ecd64eab0ea517b0","786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"]
    if list(map(digest,(terrain,dat,walls,control_dat,original)))!=expected:raise ValueError("control provenance mismatch")
    ref=LevelDat.parse(dat).static_mesh_reference("primary",160);origin=struct.unpack_from("<3i",dat,ref.object_offset)
    points=[]
    for index in range(416,439):
        offset=ref.geometry_offset+4+index*12
        if offset+12>len(dat):raise ValueError("truncated ramp vertex")
        points.append(tuple(a+b for a,b in zip(struct.unpack_from("<3h",dat,offset),origin)))
    edges=[sorted((p for p in points if p[0]==x),key=lambda p:p[2]) for x in (5750,6250)]
    if list(map(len,edges))!=[6,6]:raise ValueError("unexpected ramp topology")
    profiles={x:render_profile(original,records=(124,128),x=x,z_start=10900,z_end=13000) for x in (5750,6250)}
    trimmed,trim_report=trim_side_mesh(walls,origin=origin,profiles=profiles)
    new_dat,render_allocation=append_render_geometry(dat,((trimmed,origin),),record_index=160)
    parsed=TerrainAll.parse(terrain);r=parsed.records[99]
    addition,cells=side_collision(*edges,origin=(r.component_x,r.component_y,r.component_z),bottom_y=-1168)
    new_terrain,collision_allocation=append_collision_groups(terrain,addition,source_index=99)
    insertion=parsed.collision_payload(99).terminator_offset
    for cell in cells:cell['file_offset']=insertion+cell['cell_relative_offset']
    for name,t,d in (("fixture",new_terrain,new_dat),("controls/collision-only",new_terrain,control_dat),("controls/trim-only",terrain,new_dat)):
        target=out/name;target.mkdir(parents=True);(target/"TERRAIN.ALL").write_bytes(t);(target/"LEVEL.DAT").write_bytes(d)
    (out/"fixture/side-faces.mesh").write_bytes(trimmed)
    shutil.copytree(ROOT/"work/copies/EXP-20260906-001/game",out/"game")
    game=out/"game/PC/BUGS";(game/"CD/LEVEL01/TERRAIN.ALL").write_bytes(new_terrain);(game/"CD/LEVEL01/LEVEL.DAT").write_bytes(new_dat)
    if (game/"bugs.log").exists():(game/"bugs.log").unlink()
    receipt=dict(experiment=EXP,status="built-offline-validation-pending",input_sha256=expected,terrain_sha256=digest(new_terrain),dat_sha256=digest(new_dat),
                 side_mesh_sha256=digest(trimmed),profiles=profiles,trim=trim_report,cells=cells,render_allocation=render_allocation,collision_allocation=collision_allocation,
                 controls=["EXP-20260906-002 visual-only buried skirts","controls/collision-only","controls/trim-only"],build_seconds=time.monotonic()-start,
                 root_cause_limit="Buried geometry removed as a bounded discriminator; exact screenshot pixels and full draw-order causality not established.",live_actions=[])
    report.write_text(json.dumps(receipt,indent=2,default=encode)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('profiles','cells','input_sha256')},indent=2))


if __name__=="__main__":main()
