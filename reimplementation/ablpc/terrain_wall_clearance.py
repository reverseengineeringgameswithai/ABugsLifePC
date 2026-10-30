"""Bounded X-wall clearance authoring, EXP-20260906-004.

Translate explicitly selected one-cell, axis-aligned wall groups outward.
This is an authoring offset, not a PC collider-radius setting. Group X minimum,
cell origin X and cell X-window minimum move together. Relative extents, edges,
normals, unknown bytes, directory records and all other payloads are preserved.
The original loader recomputes its derived descriptor/bucket bounds on load.
"""
from __future__ import annotations

import hashlib
import struct
from collections.abc import Sequence

from .terrain_all import TerrainAll


def offset_x_wall_groups(
    data: bytes,
    *,
    source_index: int,
    group_offsets: Sequence[int],
    outward_stored: int,
) -> tuple[bytes, dict]:
    """Return a size-preserving copy; refuse unsupported or overflowing edits."""
    if type(outward_stored) is not int or not 0 <= outward_stored <= 32767:
        raise ValueError("clearance must be an integer in 0..32767 stored units")
    terrain = TerrainAll.parse(data)
    if type(source_index) is not int or not 0 <= source_index < len(terrain.records):
        raise ValueError("source index outside directory")
    record = terrain.records[source_index]
    if record.field_10 not in (6, 7, 8) or record.field_46 == 1:
        raise ValueError("requires an explicit non-clone triangle payload")
    offsets = tuple(group_offsets)
    if not offsets or any(type(o) is not int for o in offsets):
        raise ValueError("nonempty integer group offsets required")
    if len(set(offsets)) != len(offsets):
        raise ValueError("duplicate group offset")
    groups = {g.offset: g for g in terrain.collision_payload(source_index).groups}
    end = record.payload_offset + record.payload_size
    writes: list[tuple[int, int]] = []
    rows = []
    for offset in offsets:
        if offset not in groups:
            raise ValueError("offset does not identify a group in the selected source")
        group = groups[offset]
        if not record.payload_offset <= offset <= end - 44 or end > len(data):
            raise ValueError("wall group outside payload")
        marker, count, xmin, xspan, _, zspan = struct.unpack_from("<6h", data, offset)
        if marker != 1 or count != 1 or len(group.cells) != 1:
            raise ValueError("only the banked marker-1, one-cell group is supported")
        cell = group.cells[0]
        if cell.offset != offset + 12 or cell.offset + 32 > end:
            raise ValueError("cell layout outside selected group")
        w = cell.words
        if w[:3] not in ((-16384, 0, 0), (16384, 0, 0)):
            raise ValueError("requires an exact axis-aligned X-wall normal")
        if w[6] or w[9]:
            raise ValueError("wall edges are not coplanar at constant X")
        if xspan < 0 or zspan < 0 or w[13] < 0:
            raise ValueError("negative admission span")
        delta = outward_stored if w[0] > 0 else -outward_stored
        fields = ((offset + 4, xmin), (cell.offset + 6, w[3]), (cell.offset + 24, w[12]))
        changed = []
        for address, before in fields:
            after = before + delta
            if not -32768 <= after <= 32767:
                raise ValueError("translated X field exceeds signed 16-bit storage")
            writes.append((address, after))
            changed.append({"offset": address, "before": before, "after": after})
        rows.append({
            "group_offset": offset, "cell_offset": cell.offset,
            "normal": list(w[:3]), "delta_stored": delta,
            "plane_x_world_before": record.world_base[0] + w[3] * 32,
            "plane_x_world_after": record.world_base[0] + (w[3] + delta) * 32,
            "fields": changed,
        })
    output = bytearray(data)
    for address, value in writes:
        struct.pack_into("<h", output, address, value)
    result = bytes(output)
    return result, {
        "source_index": source_index, "outward_stored": outward_stored,
        "outward_world": outward_stored * 32, "groups": rows,
        "size": len(result), "directory_offset": terrain.directory_offset,
        "before_sha256": hashlib.sha256(data).hexdigest(),
        "after_sha256": hashlib.sha256(result).hexdigest(),
        "scope": "only three established X words per selected group; no render edit or PC-radius claim",
    }
