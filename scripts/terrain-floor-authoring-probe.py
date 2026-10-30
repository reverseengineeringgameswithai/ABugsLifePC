#!/usr/bin/env python3
"""Reproduce EXP-20260904-005's six-cell raised floor with retail instructions.

Print asset-free measurements. Optional fixture output is restricted to a new
file under work/copies. Motion is synthetic, not a live input replay.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_floor_edit import translate_floor_group
from ablpc.terrain_height import TerrainHeightModel

spec = importlib.util.spec_from_file_location("floor_reference", ROOT / "scripts/terrain-barrier-authoring-probe.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
b = a.b
SOURCE_INDEX, GROUP_OFFSET, DY = 99, 47640, -64
RAISED_SHA256 = "0b808506390bed5ab3241e0a600a05a9df38726e18e38acd367323259fbc14a6"


def fixture():
    source = b.retail.load_source("level01")
    groups = source.collision_payload(SOURCE_INDEX).groups
    indices = [i for i, group in enumerate(groups) if group.offset == GROUP_OFFSET]
    b.p.require(len(indices) == 1, "fixed floor group locator changed")
    group = groups[indices[0]]
    b.p.require([c.offset for c in group.cells] == [47652, 47684, 47716, 47748, 47780, 47812],
                "fixed floor cell locators changed")
    modified = b.TerrainAll.parse(translate_floor_group(source.data, SOURCE_INDEX, indices[0], DY))
    b.p.require(hashlib.sha256(modified.data).hexdigest() == RAISED_SHA256,
                "authored floor differs from live-tested file")
    return source, modified


def report():
    source, modified = fixture()
    text = b.p.load_text(b.p.DEFAULT_BINARY)
    arms = []
    for name, terrain, dy in (("retail", source, 0), ("raised", modified, DY * 32)):
        probe = a.reference(terrain, text)
        probe.reset()
        b.p.put(probe.cpu, b.retail.POSITION, "4i", 197091, 2734 - 1024 + dy, 492897, 0)
        b.p.put(probe.cpu, b.retail.FLAGS, "I", 0)
        landing = probe.step((0, 2048, 0))
        b.p.require(landing["after"]["flags"] == [1, 1], "raised floor landing failed")
        steps = [probe.step((-900, 512, 700)) for _ in range(75)]
        arms.append({"arm": name, "landing": landing, "steps": steps,
                     "unrelated_floor": probe.grounded_case("flat", "normal"),
                     "spawn_plane_heights": [p.plane_height for p in TerrainHeightModel(terrain).planes(197091, 492897)]})
    return {"experiment": "EXP-20260904-005", "scope": "offline retail instructions; synthetic motion; rigid group translation only",
            "binary_sha256": b.p.BINARY_SHA256,
            "source_sha256": hashlib.sha256(source.data).hexdigest(), "modified_sha256": RAISED_SHA256,
            "source_record": SOURCE_INDEX, "group_offset": GROUP_OFFSET, "group_size": 204,
            "translation_stored_y": DY, "translation_world_y": DY * 32,
            "provenance": {str(p.relative_to(ROOT)): b.digest(p) for p in
                           (Path(__file__), Path(a.__file__), Path(b.__file__), Path(b.retail.__file__),
                            ROOT / "reimplementation/ablpc/terrain_floor_edit.py")},
            "arms": arms}


def write_fixture(path: Path) -> None:
    target = path.resolve()
    b.p.require(target.is_relative_to((ROOT / "work/copies").resolve()),
                "authored assets must stay under work/copies")
    with target.open("xb") as output:
        output.write(fixture()[1].data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-terrain", type=Path)
    args = parser.parse_args()
    result = report()
    if args.write_terrain is not None:
        write_fixture(args.write_terrain)
    print(json.dumps(result, indent=2, sort_keys=True))
