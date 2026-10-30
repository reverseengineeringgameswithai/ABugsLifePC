#!/usr/bin/env python3
"""Fixed EXP-008 depth/subdivision variants, reusing the EXP-006 fixture.

This is a bounded experiment builder, not a general mesh writer. Assets may
only be written to a new directory under work/copies. The stationary variant
places the same box between the initial camera and Flik; its collision moves
with its visible geometry. Physics is identical among its rendering variants.
The compared object byte also adjusts a scene distance threshold; this is not
a recommendation to clear that byte throughout existing retail terrain.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
STATIONARY_BOX = (6275, 6925, 14800, 15500, -3392)


def reference():
    spec = importlib.util.spec_from_file_location(
        'fixed_deck_reference', ROOT / 'scripts/terrain-deck-probe.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def interpolate(corners, u, v):
    """Bilinear interpolation of one bounded quad's integer corner values."""
    weights = ((1-u)*(1-v), u*(1-v), u*v, (1-u)*v)
    return tuple(round(sum(w * corner[k] for w, corner in zip(weights, corners)))
                 for k in range(len(corners[0])))


def build(*, stationary=False, depth_offset=0, divisions=1):
    if type(depth_offset) is not int or depth_offset not in (0, 8):
        raise ValueError('only the compared depth offsets 0 and 8 are supported')
    if type(divisions) is not int or divisions not in (1, 2, 4):
        raise ValueError('only subdivisions 1, 2 and 4 fit this bounded fixture')
    base = reference()
    if stationary:
        base.BOX = STATIONARY_BOX
    terrain, original_dat, meta = base.build()
    dat = bytearray(original_dat)
    parsed = base.LevelDat.parse(original_dat)
    ref = parsed.static_mesh_reference('primary', 160)
    depth_at = ref.object_offset + 0x12
    assert (depth_at, dat[depth_at]) == (18690, 8)
    dat[depth_at] = depth_offset
    vertices = [v.to_bytes() for v in ref.payload.vertices]
    face_count = ref.payload.face_count
    if divisions != 1:
        # Keep the floor quad; divide top in both directions and each side
        # along its horizontal edge. Per-face suffix bytes remain local UVs.
        new_vertices, faces = [], []
        indices = {}
        for face_index, face in enumerate(ref.payload.faces):
            raw = [vertices[i // 12] for i in face.vertex_byte_offsets]
            xyz = [struct.unpack_from('<3h', row) for row in raw]
            attributes = raw[0][6:]
            assert all(row[6:] == attributes for row in raw)
            uv = [(word & 255, word >> 8) for word in face.field_words]
            nx, nz = ((1, 1) if face_index == 0 else
                      (divisions, divisions) if face_index == 1 else
                      (1, divisions))
            for z in range(nz):
                for x in range(nx):
                    parameters = ((x/nx, z/nz), ((x+1)/nx, z/nz),
                                  ((x+1)/nx, (z+1)/nz), (x/nx, (z+1)/nz))
                    offsets, fields = [], []
                    for u, v in parameters:
                        position = interpolate(xyz, u, v)
                        vertex = struct.pack('<3h', *position) + attributes
                        if vertex not in indices:
                            indices[vertex] = len(new_vertices)
                            new_vertices.append(vertex)
                        offsets.append(indices[vertex] * 12)
                        tx, ty = interpolate(uv, u, v)
                        assert 0 <= tx <= 255 and 0 <= ty <= 255
                        fields.append(tx | ty << 8)
                    faces.append(struct.pack('<8H', *offsets, *fields))
        mesh = (struct.pack('<i', len(new_vertices)) + b''.join(new_vertices)
                + struct.pack('<HH', ref.payload.tag, len(faces))
                + b''.join(faces) + b'\xff\xff')
        retail = base.LevelDat.from_path(base.SOURCE / 'LEVEL.DAT')
        original_ref = retail.static_mesh_reference('primary', 160)
        # Do not use unidentified trailing command groups as spare capacity.
        capacity = original_ref.payload.end_offset - original_ref.geometry_offset
        if len(mesh) > capacity:
            raise ValueError('subdivided stream exceeds the original known span')
        start = ref.geometry_offset
        assert start + len(mesh) <= len(dat)
        dat[start:start+len(mesh)] = mesh
        meta['mesh160_replaced_prefix_bytes'] = len(mesh)
        vertices, face_count = new_vertices, len(faces)
    reparsed = base.LevelDat.parse(bytes(dat)).static_mesh_reference('primary',160)
    assert reparsed.payload.vertex_count == len(vertices)
    assert reparsed.payload.face_count == face_count
    assert dat[reparsed.payload.end_offset:reparsed.payload.end_offset+2] == b'\xff\xff'
    meta.update(stationary=stationary, depth_offset=depth_offset, divisions=divisions,
                vertex_count=len(vertices), face_count=face_count,
                terrain_sha256=hashlib.sha256(terrain).hexdigest(),
                level_dat_sha256=hashlib.sha256(dat).hexdigest())
    return terrain, bytes(dat), meta


def write_fixture(directory, **options):
    target = Path(directory).resolve()
    if not target.is_relative_to((ROOT / 'work/copies').resolve()):
        raise ValueError('assets must stay under work/copies')
    if target.exists():
        raise FileExistsError('choose a new output directory')
    terrain, dat, metadata = build(**options)
    target.mkdir(parents=True)
    (target / 'TERRAIN.ALL').write_bytes(terrain)
    (target / 'LEVEL.DAT').write_bytes(dat)
    (target / 'fixture.json').write_text(json.dumps(metadata, indent=2)+'\n')
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stationary', action='store_true')
    parser.add_argument('--depth-offset', type=int, choices=(0,8), default=0)
    parser.add_argument('--divisions', type=int, choices=(1,2,4), default=1)
    parser.add_argument('--write-fixture', type=Path)
    args = parser.parse_args()
    options = dict(stationary=args.stationary, depth_offset=args.depth_offset,
                   divisions=args.divisions)
    metadata = (build(**options)[2] if args.write_fixture is None else
                write_fixture(args.write_fixture, **options))
    print(json.dumps(metadata, indent=2))
