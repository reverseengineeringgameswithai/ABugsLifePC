#!/usr/bin/env python3
"""Stage a fresh EXP-009 successor with only its mesh visibility bound changed."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from ablpc.terrain_visibility import patch_scene_visibility


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", required=True)
    args = parser.parse_args()
    if not args.experiment.startswith("EXP-") or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in args.experiment):
        parser.error("invalid experiment ID")
    root = Path(__file__).resolve().parents[1]
    source = root / "work/copies/EXP-20260905-009/game"
    destination = root / "work/copies" / args.experiment
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise ValueError("destination exists; preserving existing copies")
    level = source / "PC/BUGS/CD/LEVEL01"
    terrain = (level / "TERRAIN.ALL").read_bytes()
    dat = (level / "LEVEL.DAT").read_bytes()
    digest = lambda data: hashlib.sha256(data).hexdigest()
    assert digest(terrain) == "77a77456c3b9a0f4db5e7b20d257a9772e04c0f0ed3d0812590943d630851698"
    assert digest(dat) == "24b8c345d82bb3489ab765d3ad24f917fcacf1da4d5a910e715b4daf84b071e8"
    candidate, bounds = patch_scene_visibility(dat, expected_bound=6047)
    destination.mkdir()
    fixture = destination / "fixture"
    fixture.mkdir()
    (fixture / "TERRAIN.ALL").write_bytes(terrain)
    (fixture / "LEVEL.DAT").write_bytes(candidate)
    subprocess.run(["cp", "-a", "--reflink=auto", str(source), str(destination / "game")], check=True)
    (destination / "game/PC/BUGS/CD/LEVEL01/LEVEL.DAT").write_bytes(candidate)
    report = {"experiment_id": args.experiment, "control": "EXP-20260905-009",
              "status": "staged-not-runtime-validated", "source_game": str(source.relative_to(root)),
              "candidate_game": str((destination / "game").relative_to(root)),
              "terrain_sha256": digest(terrain), "source_dat_sha256": digest(dat),
              "candidate_dat_sha256": digest(candidate), "bounds": bounds,
              "changed_dat_offsets": [i for i, (a, b) in enumerate(zip(dat, candidate)) if a != b],
              "dat_size_unchanged": len(dat) == len(candidate), "collision_unchanged": True,
              "unknown_fields_and_geometry_unchanged": True}
    (fixture / "build.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
