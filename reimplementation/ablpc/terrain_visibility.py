"""Conservative type-0x41 scene bounds for the demonstrated PC camera profile.

EXP-20260905-009: the gate at 0x0044D63A uses unnormalised frustum
inequalities, so a geometric enclosing-sphere radius alone is insufficient.
This does not change collision, geometry, scene centres or unknown fields.
"""

import math
import struct

from .level_dat import LevelDat


def _integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{label} must be an integer in [{low}, {high}]")
    return value


def scene_visibility_radius(geometric_radius, previous_bound=0, *,
                            width=640, height=480, focal=320):
    """Scale a geometric radius for the PC's unnormalised side-plane tests.

    The eight stored-unit allowance covers strict comparisons and rounding
    for this bounded authoring profile. It is not an all-renderer proof.
    Reject overflow rather than silently clipping a required bound.
    """
    radius = _integer(geometric_radius, 0, 65535, "geometric radius")
    previous = _integer(previous_bound, 0, 32767, "previous bound")
    width = _integer(width, 2, 16384, "width")
    height = _integer(height, 2, 16384, "height")
    focal = _integer(focal, 1, 32767, "focal")
    half_extent = max(width // 2, height // 2)
    squared_numerator = radius * radius * (focal * focal + half_extent * half_extent)
    bound = math.isqrt(squared_numerator) // focal
    if bound * bound * focal * focal < squared_numerator:
        bound += 1
    bound = max(previous, bound + 8)
    return _integer(bound, 0, 32767, "required visibility bound")


def patch_scene_visibility(data, *, record_index=160, expected_bound=None,
                           width=640, height=480, focal=320):
    """Return a DAT differing only at one validated signed scene-bound word."""
    if type(data) is not bytes:
        raise ValueError("LEVEL.DAT must be immutable bytes")
    _integer(record_index, 0, 65535, "record index")
    parsed = LevelDat.parse(data)
    ref = parsed.static_mesh_reference("primary", record_index)

    def span(offset, size, label):
        if type(offset) is not int or type(size) is not int or offset < 0 or size < 0 or offset > len(data) - size:
            raise ValueError(f"{label} is outside LEVEL.DAT")
        return data[offset:offset + size]

    scene = span(ref.record_offset, 20, "scene")
    obj = span(ref.object_offset, 24, "object")
    count = _integer(ref.payload.vertex_count, 1, 65535, "vertex count")
    vertices = span(ref.payload.vertices_offset, count * 12, "vertices")
    if struct.unpack_from("<3h", obj, 12) != (0, 0, 0) or obj[19] & 0x1f:
        raise ValueError("only established untranslated-rotation mesh transforms are supported")
    center = struct.unpack_from("<3i", scene)
    origin = struct.unpack_from("<3i", obj)
    previous = struct.unpack_from("<h", scene, 12)[0]
    _integer(previous, 0, 32767, "previous bound")
    if expected_bound is not None:
        _integer(expected_bound, 0, 32767, "expected bound")
        if previous != expected_bound:
            raise ValueError("scene bound compare-before-write failed")
    squared_radius = 0
    for index in range(count):
        vertex = struct.unpack_from("<3h", vertices, index * 12)
        squared_radius = max(squared_radius, sum((vertex[i] + origin[i] - center[i]) ** 2 for i in range(3)))
    geometric_radius = math.isqrt(squared_radius)
    geometric_radius += geometric_radius * geometric_radius != squared_radius
    bound = scene_visibility_radius(geometric_radius, previous, width=width, height=height, focal=focal)
    offset = ref.record_offset + 12
    result = data[:offset] + struct.pack("<h", bound) + data[offset + 2:]
    return result, {
        "record_index": record_index,
        "scene_record_offset": ref.record_offset,
        "bound_offset": offset,
        "bound_before": previous,
        "bound_after": bound,
        "scene_center_retained": center,
        "object_origin_retained": origin,
        "vertex_count": count,
        "squared_geometric_radius": squared_radius,
        "geometric_radius": geometric_radius,
        "profile": {"width": width, "height": height, "focal": focal},
        "rounding_allowance_stored_units": 8,
        "formula": "ceil(R * sqrt(1 + (max(width//2,height//2)/focal)**2)) + 8",
        "preservation": "All bytes outside the signed scene-bound word are identical",
    }
