#!/usr/bin/env python3
"""Fixed EXP-20260904-005 visual companion to the six-cell raised floor.

This maps 17 selected Level01 vertex Y fields, not arbitrary terrain. The
interior ground movement is live-tested; boundary stitching is unresolved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.level_dat import LevelDat, DatFormatError

SOURCE = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT"
SOURCE_SHA256 = "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"
MODIFIED_SHA256 = "6f36981636766ae6af52e65b13af53a862985d47dfce835c59a1a7ef351d93e9"
# Locators selected by spatial comparison, then validated in the live paired
# arm. Duplicate coordinates across these three meshes move together.
VERTICES = {160: (8, 9, 10, 11, 15, 23, 27, 36), 213: (107, 108),
            280: (26, 27, 28, 29, 96, 97, 103)}


def fixture(raw: bytes) -> tuple[bytes, list[dict]]:
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise DatFormatError("fixed visual fixture requires the pinned retail Level01 DAT")
    source = LevelDat.parse(raw)
    output = raw
    edits = []
    for index, indices in VERTICES.items():
        ref = source.static_mesh_reference("primary", index)
        if struct.unpack_from("<3h", raw, ref.object_offset + 12) != (0, 0, 0):
            raise DatFormatError("fixed visual fixture requires zero object rotation")
        origin = struct.unpack_from("<3i", raw, ref.object_offset)
        for i in indices:
            vertex = ref.payload.vertices[i]
            old = vertex.component_02
            output = LevelDat.parse(output).set_static_mesh_vertex_component("primary", index, i, 2, old, old - 64)
            edits.append({"section": "primary", "record": index, "vertex": i,
                          "field_offset": vertex.offset + 2, "old": old, "new": old - 64,
                          "object_plus_vertex_stored": [origin[0] + vertex.component_00,
                                                        origin[1] + old, origin[2] + vertex.component_04]})
    if hashlib.sha256(output).hexdigest() != MODIFIED_SHA256:
        raise DatFormatError("fixed visual fixture differs from live-tested bytes")
    return output, edits


def write_fixture(path: Path, raw: bytes) -> None:
    target = path.resolve()
    if not target.is_relative_to((ROOT / "work/copies").resolve()):
        raise DatFormatError("authored assets must stay under work/copies")
    data, _ = fixture(raw)
    with target.open("xb") as output:
        output.write(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-level", type=Path)
    args = parser.parse_args()
    raw = SOURCE.read_bytes()
    data, edits = fixture(raw)
    if args.write_level is not None:
        write_fixture(args.write_level, raw)
    print(json.dumps({"experiment": "EXP-20260904-005", "source_sha256": SOURCE_SHA256,
                      "modified_sha256": MODIFIED_SHA256, "edits": edits,
                      "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "scope": "fixed spatial mapping; boundary stitching unresolved"}, indent=2))
