#!/usr/bin/env python3
"""Create a fresh EXP-006 tiled fixture and optionally an isolated game copy."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_texture_tiling import build_tiled_pair


def new_path(value):
    path = value.resolve()
    root = (ROOT / "work/copies").resolve()
    if path == root or not path.is_relative_to(root) or path.exists():
        raise ValueError("Output must be a fresh path strictly below work/copies")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage-game", type=Path)
    parser.add_argument("--tile-size", type=int, default=512)
    args = parser.parse_args()
    output = new_path(args.output)
    game = new_path(args.stage_game) if args.stage_game else None
    if game is not None and (game == output or game.is_relative_to(output) or output.is_relative_to(game)):
        parser.error("Fixture and game paths must not overlap")
    source = ROOT / "work/copies/EXP-20260905-005/material-fixture"
    terrain, dat, report = build_tiled_pair((source / "TERRAIN.ALL").read_bytes(),
                                           (source / "LEVEL.DAT").read_bytes(), tile_size=args.tile_size)
    baseline = json.loads((source / "fixture.json").read_text())
    retained = ("deck", "box", "ramp_foot_x", "ramp_run_stored", "ramp_rise_stored", "source99_payload_offset",
                "source99_replaced_prefix_bytes", "scene_record_offset", "object_offset", "mesh_origin", "depth_offset", "cells")
    fixture = {key: baseline[key] for key in retained}
    fixture.update({"experiment": report["experiment"], "source_fixture": str(source.relative_to(ROOT)),
                    "mesh160_geometry_offset": report["allocation"]["geometry_offset"],
                    "mesh160_replaced_prefix_bytes": report["tiling"]["stream_bytes"],
                    "known_mesh_capacity": report["allocation"]["growth_bytes"],
                    "vertex_count": report["tiling"]["vertex_count"], "face_count": report["tiling"]["face_count"],
                    "terrain_sha256": report["terrain_sha256"], "level_dat_sha256": report["candidate_dat_sha256"],
                    "texture_tiling": report})
    output.mkdir(parents=True, exist_ok=False)
    for name, data in (("TERRAIN.ALL", terrain), ("LEVEL.DAT", dat)):
        with (output / name).open("xb") as stream:
            stream.write(data)
    with (output / "fixture.json").open("x") as stream:
        json.dump(fixture, stream, indent=2)
        stream.write("\n")
    if game is not None:
        game.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-a", "--reflink=auto", "--", str(ROOT / "work/copies/EXP-20260905-004/game"), str(game)], check=True)
        for name, data in (("TERRAIN.ALL", terrain), ("LEVEL.DAT", dat)):
            (game / "PC/BUGS/CD/LEVEL01" / name).write_bytes(data)
        (game / "PC/BUGS/bugs.log").unlink(missing_ok=True)
        report["game_stage"] = str(game.relative_to(ROOT))
    report["fixture"] = str(output.relative_to(ROOT))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
