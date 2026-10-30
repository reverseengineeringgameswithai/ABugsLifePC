#!/usr/bin/env python3
"""Build original grass reuse around the isolated area; no live operations."""
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_foliage import (append_blades, append_scene_mesh, blade_templates,
                                  decode_mesh, mesh_bytes, visible_floor_height)

OUTLINE = ((4064,13064),(5814,13064),(5814,10964),(6186,10964),
           (6186,13064),(8236,13064),(8236,18036),(4064,18036),(4064,13064))


def main():
    destination = ROOT / "work/copies/EXP-20260906-006/grass-fixture"
    report_path = ROOT / "work/experiments/EXP-20260906-006/grass-build.json"
    if destination.exists() or report_path.exists():
        raise ValueError("refusing an existing fixture/report")
    source = ROOT / "work/copies/EXP-20260906-005/fixture"
    original = ROOT / "work/copies/EXP-20260906-006/og-game/PC/BUGS/CD/LEVEL01"
    control = (source / "LEVEL.DAT").read_bytes()
    donor = (original / "LEVEL.DAT").read_bytes()
    digest = lambda b: hashlib.sha256(b).hexdigest()
    if digest(control) != "3461dff75763670f54607efc6829c952158dc7876651c6a3f1088d0bcb0658af" or digest(donor) != "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53":
        raise ValueError("exact control/donor hash mismatch")
    control_mesh, ref = mesh_bytes(control, 160)
    donor_mesh, donor_ref = mesh_bytes(donor, 388)
    origin = struct.unpack_from("<3i", control, ref.object_offset)
    placements = []
    for edge, (a, b) in enumerate(zip(OUTLINE, OUTLINE[1:])):
        dx, dz = b[0]-a[0], b[1]-a[1]
        length = abs(dx)+abs(dz)
        nx, nz = -dz//length, dx//length
        turns = 2 if dx > 0 else 0 if dx < 0 else 1 if dz > 0 else 3
        count = math.ceil(length / 88)
        for i in range(count):
            t = (i+.5)/count
            # Grass bases follow the actual outer visible edge,64 beyond barrier.
            x, z = round(a[0]+dx*t-nx*64), round(a[1]+dz*t-nz*64)
            # Height sampled just inside the surface to avoid boundary roundoff.
            y = visible_floor_height(control_mesh, origin, x+nx*2, z+nz*2)
            placements.append((x,y,z,turns))
    mesh = append_blades(control_mesh, donor_mesh, placements, origin)
    dat, allocation = append_scene_mesh(control, 160, mesh)
    terrain = (ROOT / "work/copies/EXP-20260906-006/positive/fixture/TERRAIN.ALL").read_bytes()
    plant = (source / "PLANTTER.ALL").read_bytes()
    vertices, groups = decode_mesh(mesh)
    report = {"experiment": "EXP-20260906-006", "status": "built; native/runtime gates pending",
              "donor_scene":388,"donor_object_offset":donor_ref.object_offset,
              "donor_geometry_offset":donor_ref.geometry_offset,
              "donor_blade_vertex_indices":[t["source_indices"] for t in blade_templates(donor_mesh)],
              "texture_dependency":"Original Level01 texture loading and page1; no new texture pixels",
              "original_level_raw_sha256":digest((original/'LEVEL.RAW').read_bytes()),
              "outline_stored":OUTLINE,"grass_barrier_offset_stored":64,
              "blade_count":len(placements),"placements":placements,
              "vertex_count":len(vertices),"face_count":sum(len(f) for _,f in groups),
              "groups":[{"tag":tag,"faces":len(f)} for tag,f in groups],
              "allocation":allocation,"fixture":str(destination.relative_to(ROOT)),
              "hashes":{n:digest(b) for n,b in (("TERRAIN.ALL",terrain),("LEVEL.DAT",dat),("PLANTTER.ALL",plant))}}
    destination.mkdir(parents=True)
    for name,data in (("TERRAIN.ALL",terrain),("LEVEL.DAT",dat),("PLANTTER.ALL",plant)):
        (destination/name).write_bytes(data)
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='placements'},indent=2))


if __name__ == "__main__":
    main()
