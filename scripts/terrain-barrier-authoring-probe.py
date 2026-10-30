#!/usr/bin/env python3
"""Reproduce EXP-20260904-004's fixed moved-barrier fixture offline.

Default output is an asset-free JSON measurement report. --write-terrain also
creates the fixed experimental terrain file at a new path under work/copies/.
This does not launch the game or implement general terrain authoring.
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
from ablpc.terrain_barrier_edit import translate_terrain_barrier

spec = importlib.util.spec_from_file_location("authoring_reference", ROOT / "scripts/terrain-barrier-probe.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
TRANSLATION = (2200, 19968)
MOVED_SHA256 = "7329b620ba5038be2ba3d94e1d08be68935e06c51ef03b5defb45737efeda0ac"


def fixture():
    source = b.retail.load_source("level01")
    strip = b.BarrierPayload.from_terrain(source, 179)
    b.p.require((strip.offset, strip.segment_count, len(strip.raw)) == (219632, 4, 68),
                "fixed barrier locator changed")
    modified = b.TerrainAll.parse(translate_terrain_barrier(source.data, 179, *TRANSLATION))
    b.p.require(hashlib.sha256(modified.data).hexdigest() == MOVED_SHA256,
                "authored fixture differs from live-tested file")
    return source, modified


def reference(terrain, text):
    # Reuse EXP-002 loading unchanged, supplying this experiment's explicit
    # source bytes. Scope the substitution to synchronous construction only.
    original = b.retail.load_source
    b.retail.load_source = lambda key: terrain if key == "level01" else original(key)
    try:
        return b.BarrierProbe("level01", text)
    finally:
        b.retail.load_source = original


def report():
    source, modified = fixture()
    text = b.p.load_text(b.p.DEFAULT_BINARY)
    arms = []
    for name, terrain in (("retail", source), ("moved", modified)):
        probe = reference(terrain, text)
        probe.reset()
        b.p.put(probe.cpu, b.retail.POSITION, "4i", 197091, 2734 - 1024, 492897, 0)
        b.p.put(probe.cpu, b.retail.FLAGS, "I", 0)
        landing = probe.step((0, 2048, 0))
        b.p.require(landing["after"]["flags"] == [1, 1], "spawn fixture did not land")
        steps = [probe.step((-900, 0, 700)) for _ in range(35)]
        arms.append({"arm": name, "landing": landing, "steps": steps,
                     "old_site": probe.grounded_case("barrier", "normal"),
                     "unrelated_floor": probe.grounded_case("flat", "normal")})
    return {
        "experiment": "EXP-20260904-004", "scope": "offline original instructions; synthetic motion, not a live input replay",
        "binary_sha256": b.p.BINARY_SHA256,
        "source_sha256": hashlib.sha256(source.data).hexdigest(), "modified_sha256": MOVED_SHA256,
        "translation_stored": list(TRANSLATION), "translation_world": [v * 32 for v in TRANSLATION],
        "source_record": 179, "payload_offset": 219632, "payload_size": 68,
        "provenance": {str(path.relative_to(ROOT)): b.digest(path) for path in
                       (Path(__file__), Path(b.__file__), Path(b.retail.__file__),
                        ROOT / "reimplementation/ablpc/terrain_barrier_edit.py")},
        "arms": arms,
    }


def write_fixture(path: Path) -> None:
    target = path.resolve()
    b.p.require(target.is_relative_to((ROOT / "work/copies").resolve()),
                "authored assets must stay under work/copies")
    # No overwrite: callers choose a new file in an existing work directory.
    raw = fixture()[1].data
    with target.open("xb") as output:
        output.write(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-terrain", type=Path)
    args = parser.parse_args()
    result = report()
    if args.write_terrain is not None:
        write_fixture(args.write_terrain)
    print(json.dumps(result, indent=2, sort_keys=True))
