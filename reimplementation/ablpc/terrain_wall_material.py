"""EXP-005 wall material arm, pinned to the accepted EXP-004 geometry.

The vertical colour gradient is an authoring choice derived from one original
same-tag wall face, not an inferred universal PC lighting rule.
"""

import hashlib
import struct

from .level_dat import LevelDat
from .terrain_wall_shading import (
    CAPACITY, GEOMETRY_OFFSET, SOURCE_SHA256, SOURCE_SIZE, decode, shade_quad_stream,
)

ORIGINAL_DAT_SHA256 = "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"
TERRAIN_SHA256 = "1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b"


def native_wall_profile(original):
    if not isinstance(original, bytes) or hashlib.sha256(original).hexdigest() != ORIGINAL_DAT_SHA256:
        raise ValueError("Expected the pinned original PC Level01 DAT")
    reference = LevelDat.parse(original).static_mesh_reference("primary", 128)
    face = reference.payload.faces[13]
    if (face.offset, reference.payload.tag, face.field_words) != (
            221788, 0x60, (0xff7f, 0xc07f, 0xc040, 0xff40)):
        raise ValueError("Original donor face identity changed")
    vertices = [reference.payload.vertices[offset // 12] for offset in face.vertex_byte_offsets]
    channels = [(v.field_08, v.field_09, v.field_0a) for v in vertices]
    top = tuple((channels[0][axis] + channels[1][axis]) // 2 for axis in range(3))
    bottom = tuple((channels[2][axis] + channels[3][axis]) // 2 for axis in range(3))
    return {
        "original_dat_sha256": ORIGINAL_DAT_SHA256,
        "record": 128, "group": 0, "face": 13, "face_offset": face.offset,
        "vertex_offsets": [v.offset for v in vertices], "donor_channels": channels,
        "donor_uv": [(word & 255, word >> 8) for word in face.field_words],
        "top_channels": top, "bottom_channels": bottom,
        "choice": "Average each donor height edge, then interpolate vertically; retain continuity between authored walls",
    }


def match_wall_stream(source, top_channels, bottom_channels, *, texture=True, tint=True):
    """Keep all face positions; edit wall UVs and optionally wall-only channels."""
    if type(texture) is not bool or type(tint) is not bool:
        raise ValueError("Material switches must be bools")
    for channels in (top_channels, bottom_channels):
        if not isinstance(channels, (tuple, list)) or len(channels) != 3:
            raise ValueError("Expected three channel values")
        if any(type(value) is not int or not 0 <= value <= 255 for value in channels):
            raise ValueError("Colour channels must be integers in 0..255")
    # Unit scale duplicates wall/non-wall boundaries without applying the old
    # uniform darkening candidate. Its original control remains reproducible.
    separated, report = shade_quad_stream(source, 1, 1)
    vertices, faces = decode(separated)
    output = bytearray(separated)
    group = 4 + len(vertices) * 12
    assigned = {}
    changes = []
    for face_index, (refs, fields) in enumerate(faces):
        points = [struct.unpack_from("<3h", vertices[index]) for index in refs]
        wall = (len({p[1] for p in points}) > 1
                and (len({p[0] for p in points}) == 1 or len({p[2] for p in points}) == 1))
        if not wall:
            continue
        before_uv = [(word & 255, word >> 8) for word in struct.unpack("<4H", fields)]
        if any(not (0 <= u <= 63 and 192 <= v <= 255) for u, v in before_uv):
            raise ValueError("Wall is outside the pinned floor texture region")
        for corner, (index, (u, _)) in enumerate(zip(refs, before_uv)):
            if texture:
                output[group + 4 + face_index * 16 + 8 + corner * 2] = u + 64
            if tint:
                channels = bytes((bottom_channels[i] * (63 - u) + top_channels[i] * u + 31) // 63
                                 for i in range(3))
                if index in assigned and assigned[index] != channels:
                    raise ValueError("Shared wall vertex has inconsistent height coordinates")
                assigned[index] = channels
                offset = 4 + index * 12 + 8
                output[offset:offset + 3] = channels
        changes.append({"face": face_index, "uv_before": before_uv,
                        "uv_after": [(u + 64 if texture else u, v) for u, v in before_uv]})
    report.update({
        "texture_enabled": texture, "tint_enabled": tint,
        "texture_page_index": 0, "wall_region": {"u": [64, 127], "v": [192, 255]},
        "wall_uv_operation": "Add 64 to U only; existing vertical-U orientation and all V bytes preserved",
        "top_channels": list(top_channels), "bottom_channels": list(bottom_channels),
        "field_08_09_0a_scale": "Not a uniform scale in this arm; donor-derived vertical gradient",
        "wall_face_edits": changes,
    })
    return bytes(output), report


def build_material_pair(terrain, dat, original, *, texture=True, tint=True):
    if not isinstance(terrain, bytes) or hashlib.sha256(terrain).hexdigest() != TERRAIN_SHA256:
        raise ValueError("Expected the banked EXP-004 collision bytes")
    if not isinstance(dat, bytes) or hashlib.sha256(dat).hexdigest() != SOURCE_SHA256:
        raise ValueError("Expected the banked EXP-004 render bytes")
    if GEOMETRY_OFFSET + CAPACITY > len(dat):
        raise ValueError("Mesh allocation outside DAT bounds")
    profile = native_wall_profile(original)
    mesh, report = match_wall_stream(dat[GEOMETRY_OFFSET:GEOMETRY_OFFSET + SOURCE_SIZE],
                                    profile["top_channels"], profile["bottom_channels"],
                                    texture=texture, tint=tint)
    if len(mesh) > CAPACITY:
        raise ValueError("Material stream exceeds known allocation")
    result = dat[:GEOMETRY_OFFSET] + mesh + dat[GEOMETRY_OFFSET + len(mesh):]
    report.update({
        "experiment": "EXP-20260905-005", "arm": "wall-material",
        "donor": profile, "terrain_sha256": TERRAIN_SHA256,
        "source_dat_sha256": SOURCE_SHA256, "candidate_dat_sha256": hashlib.sha256(result).hexdigest(),
        "mesh160_geometry_offset": GEOMETRY_OFFSET, "mesh160_replaced_prefix_bytes": len(mesh),
        "allocation_bytes": CAPACITY,
        "preservation": "Identical TERRAIN.ALL and per-face XYZ; original tag/UV corner order, unknown vertex fields, top/deck/ramp appearance and bytes outside the new prefix retained",
    })
    return terrain, result, report
