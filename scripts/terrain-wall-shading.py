#!/usr/bin/env python3
"""Write a fresh EXP-005 fixture without touching the running EXP-004 game."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))

from ablpc.terrain_wall_shading import shade_level_dat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    copies = (ROOT / "work/copies").resolve()
    if not output.is_relative_to(copies) or output == copies or output.exists():
        parser.error("Output must be a new directory strictly beneath work/copies")
    source = ROOT / "work/copies/EXP-20260905-004/fixture"
    terrain = (source / "TERRAIN.ALL").read_bytes()
    terrain_sha = hashlib.sha256(terrain).hexdigest()
    if terrain_sha != "1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b":
        raise ValueError("Banked EXP-004 collision guard failed")
    dat, report = shade_level_dat((source / "LEVEL.DAT").read_bytes())
    report.update({
        "experiment": "EXP-20260905-005",
        "terrain_sha256": terrain_sha,
        "source_fixture": str(source.relative_to(ROOT)),
        "output_fixture": str(output.relative_to(ROOT)),
        "runtime": "Not launched; user's EXP-004 session left untouched",
    })
    output.mkdir(parents=True, exist_ok=False)
    for name, data in (("LEVEL.DAT", dat), ("TERRAIN.ALL", terrain)):
        with (output / name).open("xb") as stream:
            stream.write(data)
    with (output / "fixture.json").open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
