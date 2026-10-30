#!/usr/bin/env python3
"""Build the private EXP-20260906-005 stripped landscape and platform spawn."""

import json
from pathlib import Path

from ablpc.terrain_isolated import digest, isolate_collision, isolate_render, platform_spawn


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "work/copies/EXP-20260906-005"


def main():
    control = ROOT / "work/copies/EXP-20260906-004/fixture"
    paths = {
        "TERRAIN.ALL": (control / "TERRAIN.ALL", "26e7076fa4027e1a81a1c8d29260944c04e584486ef886d8ab85e1f5e5f8dfcc"),
        "LEVEL.DAT": (control / "LEVEL.DAT", "f6cfa7883a902af5f43362356b7731adf9708ee5164c454b489e266867b048b2"),
        "PLANTTER.ALL": (ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/BITS/PLANTTER.ALL", "0a0cf7fa9e110eef8e2112760dcbefaa433b391ca613a3d673ee0327767eb468"),
        "bugs.exe": (ROOT / "work/copies/auto-hardware/bugs.exe", "1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f"),
    }
    if DEST.exists():
        raise ValueError("refusing to overwrite an experiment copy")
    inputs = {}
    for name, (path, sha) in paths.items():
        inputs[name] = path.read_bytes()
        if digest(inputs[name]) != sha:
            raise ValueError(f"control identity mismatch: {name}")
    terrain, tr = isolate_collision(inputs["TERRAIN.ALL"], {99: tuple(range(48380, 49964, 44))})
    plant, pr = isolate_collision(inputs["PLANTTER.ALL"], {})
    dat, dr = isolate_render(inputs["LEVEL.DAT"], record_index=160, first_group=5)
    executable, er = platform_spawn(inputs["bugs.exe"], x=192000, z=448000)
    fixture = DEST / "fixture"
    fixture.mkdir(parents=True)
    for name, data in (("TERRAIN.ALL", terrain), ("PLANTTER.ALL", plant), ("LEVEL.DAT", dat)):
        (fixture / name).write_bytes(data)
    (DEST / "auto-hardware").mkdir()
    (DEST / "auto-hardware/bugs.exe").write_bytes(executable)
    report = {"experiment": "EXP-20260906-005", "status": "built; native and runtime gates pending",
              "terrain": tr, "plantter": pr, "render": dr, "spawn": er,
              "scope": "Old scene draws and loaded terrain/template streams deactivated; actor logic, sky, texture assets and level scripts retained.",
              "limitations": ["Not a new level container or completed editor", "Raw retired bytes remain unreachable", "Ramp skirts retain their earlier ground-trim shape; outside the new terrain is intentionally void"],
              "live_memory_writes": []}
    evidence = ROOT / "work/experiments/EXP-20260906-005"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "build.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"fixture": str(fixture), "terrain": tr["after_sha256"], "plantter": pr["after_sha256"],
                      "dat": dr["after_sha256"], "exe": er["after_sha256"], "faces": dr["authored_faces"],
                      "muted_scenes": len(dr["muted_scenes"])}))


if __name__ == "__main__":
    main()
