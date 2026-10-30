"""Stored PC scenery meshes, including the negative header in EXP-20260926-001.

0045A82E..0045A8B4 places negative-count commands after an auxiliary span.
Its semantics stay opaque. Keep the full stored bytes for native rendering;
the positive view exists only for topology validation and editor previews.
"""
from dataclasses import dataclass
import struct

from .terrain_scenery import read_mesh


@dataclass(frozen=True)
class StoredMesh:
    raw: bytes
    view: bytes
    auxiliary: bytes
    auxiliary_offset: int | None


def read_stored_mesh(data, offset):
    if type(data) is not bytes or type(offset) is not int or not 0 <= offset <= len(data)-4:
        raise ValueError('Invalid stored scenery mesh source/offset')
    signed = struct.unpack_from('<i', data, offset)[0]
    if signed >= 0:
        mesh = read_mesh(data, offset)
        return StoredMesh(mesh, mesh, b'', None)
    count = -signed
    if not 1 <= count <= 5462:
        raise ValueError('Expected bounded negative vertex count')
    vertices_end = offset+4+12*count
    commands = offset+8+18*count-2*(count & 1)
    if commands > len(data)-2:
        raise ValueError('Truncated negative mesh auxiliary span')
    view = read_mesh(struct.pack('<i', count)+data[offset+4:vertices_end]+data[commands:], 0)
    end = commands+len(view)-(4+12*count)
    return StoredMesh(data[offset:end], view, data[vertices_end:commands], vertices_end)
