#!/usr/bin/env python3
"""Bounded conforming rectangular grids for the EXP-011 box comparison.

Reuses EXP-008's fixed dimensions, collision, fields and original mesh capacity.
This does not choose a general level-authoring rule. Outputs stay under work/copies.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, struct

ROOT = Path(__file__).resolve().parents[1]
GRIDS = ((4, 4), (4, 5), (5, 4), (3, 6), (6, 3))


def reference():
    spec = importlib.util.spec_from_file_location(
        "fixed_visual_reference", ROOT / "scripts/terrain-deck-visual-probe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(nx=4, nz=5, *, flip_top=False):
    if type(nx) is not int or type(nz) is not int or (nx, nz) not in GRIDS:
        raise ValueError("unsupported bounded grid")
    if type(flip_top) is not bool:
        raise ValueError("flip_top must be boolean")
    visual = reference()
    terrain, original, meta = visual.build(divisions=1, depth_offset=0)
    base = visual.reference()
    ref = base.LevelDat.parse(original).static_mesh_reference("primary", 160)
    retail = base.LevelDat.from_path(base.SOURCE / "LEVEL.DAT").static_mesh_reference("primary", 160)
    capacity = retail.payload.end_offset - retail.geometry_offset
    assert ref.geometry_offset == retail.geometry_offset == 113136
    vertices, faces, lookup, provenance = [], [], {}, []
    for face_index, face in enumerate(ref.payload.faces):
        raw = [ref.payload.vertices[i // 12].to_bytes() for i in face.vertex_byte_offsets]
        xyz = [struct.unpack_from("<3h", row) for row in raw]
        attributes = raw[0][6:]
        assert all(row[6:] == attributes for row in raw)
        uv = [(word & 255, word >> 8) for word in face.field_words]
        columns, rows = ((1, 1) if face_index == 0 else
                         (nx, nz) if face_index == 1 else
                         (1, nx if face_index in (2, 4) else nz))
        for row in range(rows):
            for col in range(columns):
                parameters = ((col / columns, row / rows),
                              ((col + 1) / columns, row / rows),
                              ((col + 1) / columns, (row + 1) / rows),
                              (col / columns, (row + 1) / rows))
                offsets, fields = [], []
                for u, v in parameters:
                    vertex = struct.pack("<3h", *visual.interpolate(xyz, u, v)) + attributes
                    if vertex not in lookup:
                        lookup[vertex] = len(vertices)
                        vertices.append(vertex)
                    offsets.append(lookup[vertex] * 12)
                    tx, ty = visual.interpolate(uv, u, v)
                    assert 0 <= tx <= 255 and 0 <= ty <= 255
                    fields.append(tx | ty << 8)
                if face_index == 1 and flip_top:
                    offsets = offsets[1:] + offsets[:1]
                    fields = fields[1:] + fields[:1]
                faces.append(struct.pack("<8H", *offsets, *fields))
                provenance.append({"source_face": face_index, "cell": [col, row]})
    mesh = (struct.pack("<i", len(vertices)) + b"".join(vertices)
            + struct.pack("<HH", ref.payload.tag, len(faces)) + b"".join(faces) + b"\xff\xff")
    if len(mesh) > capacity:
        raise ValueError("grid exceeds original known mesh span")
    start = ref.geometry_offset
    assert start + len(mesh) <= len(original)
    dat = original[:start] + mesh + original[start + len(mesh):]
    check = base.LevelDat.parse(dat).static_mesh_reference("primary", 160)
    assert check.payload.vertex_count == len(vertices) and check.payload.face_count == len(faces)
    assert dat[check.payload.end_offset:check.payload.end_offset + 2] == b"\xff\xff"
    meta.update(nx=nx, nz=nz, flip_top=flip_top, divisions=None,
                vertex_count=len(vertices), face_count=len(faces),
                mesh160_replaced_prefix_bytes=len(mesh), known_capacity=capacity,
                source_faces=provenance, terrain_sha256=hashlib.sha256(terrain).hexdigest(),
                level_dat_sha256=hashlib.sha256(dat).hexdigest())
    return terrain, dat, meta


def write_fixture(directory, **options):
    target = Path(directory).resolve()
    if not target.is_relative_to((ROOT / "work/copies").resolve()):
        raise ValueError("assets must stay under work/copies")
    if target.exists():
        raise FileExistsError("choose a new output directory")
    terrain, dat, meta = build(**options)
    target.mkdir(parents=True)
    (target / "TERRAIN.ALL").write_bytes(terrain)
    (target / "LEVEL.DAT").write_bytes(dat)
    (target / "fixture.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nx", type=int, default=4)
    parser.add_argument("--nz", type=int, default=5)
    parser.add_argument("--flip-top", action="store_true")
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    options = dict(nx=args.nx, nz=args.nz, flip_top=args.flip_top)
    result = build(**options)[2] if args.write_fixture is None else write_fixture(args.write_fixture, **options)
    print(json.dumps(result, indent=2))
