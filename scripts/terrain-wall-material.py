#!/usr/bin/env python3
"""Build separate texture-only, tint-only and combined EXP-005 file arms."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_wall_material import build_material_pair


def new_copy_path(value):
    path = value.resolve()
    copies = (ROOT / "work/copies").resolve()
    if path == copies or not path.is_relative_to(copies) or path.exists():
        raise ValueError("Expected a new path strictly beneath work/copies")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage-game", type=Path)
    parser.add_argument("--mode", choices=["combined", "texture-only", "tint-only"], default="combined")
    args = parser.parse_args()
    output = new_copy_path(args.output)
    game = new_copy_path(args.stage_game) if args.stage_game else None
    if game is not None and (game == output or game.is_relative_to(output) or output.is_relative_to(game)):
        parser.error("Fixture and game paths must not overlap")
    base = ROOT / "work/copies/EXP-20260905-004/fixture"
    original = (ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT").read_bytes()
    terrain, dat, material = build_material_pair((base / "TERRAIN.ALL").read_bytes(),
                                                (base / "LEVEL.DAT").read_bytes(), original,
                                                texture=args.mode != "tint-only", tint=args.mode != "texture-only")
    fixture = json.loads((base / "fixture.json").read_text())
    fixture.update({"mesh160_replaced_prefix_bytes": material["mesh160_replaced_prefix_bytes"],
                    "wall_material": material, "material_mode": args.mode})
    output.mkdir(parents=True, exist_ok=False)
    for name, data in [("TERRAIN.ALL", terrain), ("LEVEL.DAT", dat)]:
        with (output / name).open("xb") as stream:
            stream.write(data)
    with (output / "fixture.json").open("x") as stream:
        json.dump(fixture, stream, indent=2)
        stream.write("\n")
    if game is not None:
        game.parent.mkdir(parents=True, exist_ok=True)
        source_game = ROOT / "work/copies/EXP-20260905-004/game"
        subprocess.run(["cp", "-a", "--reflink=auto", "--", str(source_game), str(game)], check=True)
        (game / "PC/BUGS/CD/LEVEL01/LEVEL.DAT").write_bytes(dat)
        (game / "PC/BUGS/bugs.log").unlink(missing_ok=True)
        material["game_stage"] = str(game.relative_to(ROOT))
        material["stage_method"] = "Reflink-capable copy of closed EXP-004 game; only LEVEL.DAT replaced and copied bugs.log removed"
    print(json.dumps({"fixture": str(output.relative_to(ROOT)), "material": material}, indent=2))


if __name__ == "__main__":
    main()
