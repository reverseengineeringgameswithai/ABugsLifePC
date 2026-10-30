"""EXP-009 bounded additive terrain composition, not a general level repacker.

Collision insertion retains original groups/terminator/trailer and changes only
the file's word-addressed directory locator and the selected payload word count.
Render growth retains original vertices and complete command groups, rebinding
one unique object through the established end-relative-footer append boundary.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import math
import struct

from .level_dat import LevelDat
from .terrain_all import TerrainAll
from .terrain_floor_patch import contains, floor_cells, mesh_groups
from .terrain_height import TerrainHeightModel
from .terrain_play_area import DECK, encode_group
from .terrain_texture_tiling import MAX_FACES, MAX_VERTICES, decode_mesh, tile_mesh

RETAIL_TERRAIN_SHA = "62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868"
RETAIL_DAT_SHA = "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"
AUTHORED_TERRAIN_SHA = "1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b"
AUTHORED_DAT_SHA = "99fbff1754fc43979542de40e56c04d10d7af4fccde8d13e919853b679429a21"
MAX_TERRAIN_BYTES = 0x100000  # Explicit experiment/harness budget, not a native format limit.
ACCESS_X = (5750, 6250)
ACCESS_FOOT_Z, ACCESS_DECK_Z = 10900, 13000
ACCESS_SOURCE_CELL = 44140


def digest(data):
    return hashlib.sha256(data).hexdigest()


def integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{label} outside supported integer bounds")
    return value


def immutable(data, label):
    if not isinstance(data, bytes):
        raise ValueError(f"{label} must be immutable bytes")


def append_collision_groups(data, addition, *, source_index):
    """Insert a complete, terminated local-coordinate stream before the old terminator.

    Only a unique active height source is supported. Original cells keep their
    fields and source indices; subsequent payload offsets increase by growth.
    """
    immutable(data, "terrain")
    immutable(addition, "addition")
    if not 4 <= len(data) <= MAX_TERRAIN_BYTES or len(data) % 2:
        raise ValueError("Terrain exceeds the bounded aligned input budget")
    if not 2 <= len(addition) <= MAX_TERRAIN_BYTES or len(addition) % 2:
        raise ValueError("Addition must be a bounded word-aligned stream")
    parsed = TerrainAll.parse(data)
    integer(source_index, 0, len(parsed.records)-1, "source index")
    record = parsed.records[source_index]
    if record.field_10 not in (6, 7, 8) or record.field_44 >= 0 or record.field_46 != 0:
        raise ValueError("Expected an active non-template, non-clone height source")
    users = [d.source_index for d in TerrainHeightModel(parsed).descriptors
             if d.payload_source_index == source_index]
    if users != [source_index]:
        raise ValueError("Cannot extend a shared collision payload")
    old = parsed.collision_payload(source_index)
    probe_record = bytearray(record.raw)
    struct.pack_into("<I", probe_record, 0, len(addition)//2)
    probe = (struct.pack("<I", (4+len(addition))//2) + addition
             + struct.pack("<I", 1) + bytes(probe_record))
    added = TerrainAll.parse(probe).collision_payload(0)
    if not added.groups or added.terminator_offset != 4+len(addition)-2 or added.trailer:
        raise ValueError("Addition must contain groups and exactly one final terminator")
    if any(g.cell_count <= 0 or g.span_x_units < 0 or g.span_z_units < 0 for g in added.groups):
        raise ValueError("Addition has an impossible count or group bound")
    prefix = addition[:-2]
    growth = len(prefix)
    if len(data)+growth > MAX_TERRAIN_BYTES:
        raise ValueError("Expanded terrain exceeds the experiment byte budget")
    insertion = old.terminator_offset
    new_directory = parsed.directory_offset+growth
    result = bytearray(data[:insertion] + prefix + data[insertion:])
    struct.pack_into("<I", result, 0, new_directory//2)
    new_record_offset = new_directory+4+source_index*76
    struct.pack_into("<I", result, new_record_offset, record.payload_word_count+growth//2)
    return bytes(result), {
        "source_index": source_index, "payload_offset": record.payload_offset,
        "insertion_offset": insertion, "growth_bytes": growth,
        "directory_offset_before": parsed.directory_offset, "directory_offset_after": new_directory,
        "record_offset_before": record.offset, "record_offset_after": new_record_offset,
        "payload_size_before": record.payload_size, "payload_size_after": record.payload_size+growth,
        "original_group_count": len(old.groups), "added_group_count": len(added.groups),
        "original_cell_count": sum(g.cell_count for g in old.groups),
        "added_cell_count": sum(g.cell_count for g in added.groups),
        "original_terminator_before": insertion, "original_terminator_after": insertion+growth,
        "original_trailer_sha256": digest(old.trailer),
        "preservation": "Original group/cell bytes, terminator, trailer, other payloads and unknown directory fields retained; only directory locator and this payload word count are rewritten.",
    }


def append_render_geometry(data, additions, *, record_index, neutral_depth=False):
    """Retain every original vertex/group and append translated 0x60/0x61 meshes.

    Center and flags are retained. The known signed +0x0c visibility bound can
    increase; optional known object +0x12 depth bias becomes the banked zero.
    """
    immutable(data, "DAT")
    if len(data) < 4 or len(data) % 4:
        raise ValueError("Expected a four-byte-aligned DAT")
    if type(neutral_depth) is not bool:
        raise ValueError("neutral_depth must be boolean")
    if not isinstance(additions, (list, tuple)) or not 1 <= len(additions) <= 8:
        raise ValueError("Expected one to eight additional meshes")
    parsed = LevelDat.parse(data)
    integer(record_index, 0, len(parsed.primary_records)-1, "record index")
    ref = parsed.static_mesh_reference("primary", record_index)
    footer_offset = len(data)-4
    if (ref.object_offset < parsed.parsed_prefix_end or ref.object_offset+24 > footer_offset
            or ref.geometry_offset < parsed.parsed_prefix_end):
        raise ValueError("Object/geometry lies outside established payload storage")
    aliases = [r for section in ("primary", "secondary") for r in parsed.records(section)
               if r.payload_offset_candidate == ref.object_offset]
    if len(aliases) != 1:
        raise ValueError("Cannot extend an aliased render object")
    if struct.unpack_from("<3h", data, ref.object_offset+12) != (0, 0, 0) or data[ref.object_offset+19] & 31:
        raise ValueError("Rotated/scaled render objects are outside this writer")
    groups, terminator = mesh_groups(data, ref)
    count = ref.payload.vertex_count
    integer(count, 1, MAX_VERTICES, "original vertex count")
    vertex_end = ref.geometry_offset+4+count*12
    if not vertex_end <= terminator <= footer_offset-2:
        raise ValueError("Original mesh stream exceeds its bounded storage")
    vertices = [data[ref.geometry_offset+4+i*12:ref.geometry_offset+16+i*12] for i in range(count)]
    original_groups = data[vertex_end:terminator]
    command_streams = [original_groups]
    origin = struct.unpack_from("<3i", data, ref.object_offset)
    original_faces = sum(len(g["faces"]) for g in groups)
    total_faces = original_faces
    additional_counts = []
    for mesh, mesh_origin in additions:
        immutable(mesh, "additional mesh")
        if not isinstance(mesh_origin, (tuple, list)) or len(mesh_origin) != 3:
            raise ValueError("Mesh origin requires three coordinates")
        for coordinate in mesh_origin:
            integer(coordinate, -(2**31), 2**31-1, "mesh origin")
        extra_vertices, extra_faces = decode_mesh(mesh)
        base = len(vertices)
        if base+len(extra_vertices) > MAX_VERTICES or total_faces+len(extra_faces) > MAX_FACES:
            raise ValueError("Combined mesh exceeds bounded vertex/face capacity")
        for vertex in extra_vertices:
            local = tuple(v+mesh_origin[i]-origin[i] for i, v in enumerate(struct.unpack_from("<3h", vertex)))
            for coordinate in local:
                integer(coordinate, -32768, 32767, "translated vertex")
            vertices.append(struct.pack("<3h", *local)+vertex[6:])
        runs = []
        for tag, indices, fields in extra_faces:
            if not runs or runs[-1][0] != tag:
                runs.append((tag, []))
            arity = len(indices)
            runs[-1][1].append(struct.pack("<"+"H"*(arity*2),
                                          *((i+base)*12 for i in indices), *fields))
        command_streams.extend(struct.pack("<Hh", tag, len(faces))+b"".join(faces) for tag, faces in runs)
        total_faces += len(extra_faces)
        additional_counts.append({"vertices": len(extra_vertices), "faces": len(extra_faces), "vertex_index_base": base})
    mesh = struct.pack("<i", len(vertices))+b"".join(vertices)+b"".join(command_streams)+b"\xff\xff"
    final_word = struct.unpack_from("<i", data, footer_offset)[0]
    if final_word != -1 and not 0x118+4 <= final_word <= len(data)-parsed.parsed_prefix_end:
        raise ValueError("Invalid end-relative trailing-data span")
    padding = (-len(mesh)) % 4
    growth = len(mesh)+padding
    if len(data)+growth >= 2**31 or final_word != -1 and final_word+growth >= 2**31:
        raise ValueError("Expanded DAT exceeds signed offset bounds")
    center = struct.unpack_from("<3i", data, ref.record_offset)
    previous_bound = struct.unpack_from("<h", data, ref.record_offset+12)[0]
    if previous_bound < 0:
        raise ValueError("Negative visibility bound is outside the extension contract")
    radius_squared = max(sum((struct.unpack_from("<3h", v)[i]+origin[i]-center[i])**2
                             for i in range(3)) for v in vertices)
    radius = math.isqrt(radius_squared)
    from .terrain_visibility import scene_visibility_radius
    new_bound = scene_visibility_radius(radius+(radius*radius != radius_squared), previous_bound)
    integer(new_bound, 0, 32767, "expanded visibility bound")
    result = bytearray(data[:-4]+mesh+bytes(padding)+struct.pack("<i", -1 if final_word == -1 else final_word+growth))
    struct.pack_into("<I", result, ref.object_offset+20, footer_offset)
    struct.pack_into("<h", result, ref.record_offset+12, new_bound)
    depth_before = data[ref.object_offset+18]
    if neutral_depth:
        result[ref.object_offset+18] = 0
    return bytes(result), {
        "record_index": record_index, "scene_record_offset": ref.record_offset,
        "object_offset": ref.object_offset, "pointer_field_offset": ref.object_offset+20,
        "previous_geometry_offset": ref.geometry_offset, "geometry_offset": footer_offset,
        "stream_bytes": len(mesh), "stream_sha256": digest(mesh), "growth_bytes": growth,
        "original_vertex_count": count, "original_face_count": original_faces,
        "vertex_count": len(vertices), "face_count": total_faces, "additions": additional_counts,
        "original_vertex_bytes_sha256": digest(data[ref.geometry_offset+4:vertex_end]),
        "original_command_bytes_sha256": digest(original_groups),
        "retained_commands_new_offset": footer_offset+4+len(vertices)*12,
        "retained_commands_size": len(original_groups),
        "visibility_bound_offset": ref.record_offset+12,
        "visibility_bound_before": previous_bound, "visibility_bound_after": new_bound,
        "scene_center_retained": center, "depth_bias_offset": ref.object_offset+18,
        "depth_bias_before": depth_before, "depth_bias_after": result[ref.object_offset+18],
        "footer_offset_before": footer_offset, "footer_offset_after": len(result)-4,
        "footer_word_before": final_word, "footer_word_after": -1 if final_word == -1 else final_word+growth,
        "trailing_data_offset": None if final_word == -1 else len(data)-final_word,
        "preservation": "All original vertices and full command groups remain active; old payload bytes remain in place. Only the known object pointer, conservative visibility bound, selected depth bias and displaced footer change.",
        "rendering_limit": "Zero depth bias is inherited from the banked authored area, not a pixel-identical retail sorting claim. Enlarged-batch visibility/performance still need runtime comparison.",
    }


def access_ramp(terrain, mesh_origin, vertex_suffix):
    """Small authored connection from preserved cell 44140 to the deck edge."""
    if not isinstance(vertex_suffix, bytes) or len(vertex_suffix) != 6:
        raise ValueError("Expected a preserved six-byte vertex suffix")
    source = terrain.records[99]
    origin = (source.component_x, source.component_y, source.component_z)
    original_cell = [c for c in floor_cells(terrain) if c.source == 99 and c.offset == ACCESS_SOURCE_CELL]
    if len(original_cell) != 1:
        raise ValueError("Pinned access landing cell missing")
    model = TerrainHeightModel(terrain)
    feet, errors, evidence = [], [], []
    for x in ACCESS_X:
        if not contains(original_cell[0].footprint, (x, ACCESS_FOOT_Z)):
            raise ValueError("Access foot escapes its preserved original triangle")
        planes = [p for p in model.planes(x*32, ACCESS_FOOT_Z*32) if p.descriptor_index == 99 and p.divisor < 0]
        if len(planes) != 1:
            raise ValueError("Access foot has ambiguous original source-99 height")
        exact = Fraction(planes[0].plane_height, 32)
        y = round(exact)
        feet.append((x, y, ACCESS_FOOT_Z))
        errors.append(abs(exact-y))
        evidence.append({"xz_stored": [x, ACCESS_FOOT_Z], "original_plane_y_world": planes[0].plane_height,
                         "authored_plane_y_stored": y, "rounding_error_stored": str(abs(exact-y))})
    collision = [feet[0], feet[1], (ACCESS_X[1], DECK[4]-96, ACCESS_DECK_Z),
                 (ACCESS_X[0], DECK[4]-96, ACCESS_DECK_Z)]
    groups = b"".join(encode_group([collision[i] for i in indices], origin)
                       for indices in ((0, 2, 1), (0, 3, 2)))
    visible = [(x, y+96, z) for x, y, z in collision]
    vertex_bytes = []
    for point in visible:
        local = tuple(point[i]-mesh_origin[i] for i in range(3))
        for v in local:
            integer(v, -32768, 32767, "access render coordinate")
        vertex_bytes.append(struct.pack("<3h", *local)+vertex_suffix)
    untiled = (struct.pack("<i", 4)+b"".join(vertex_bytes)
               +struct.pack("<2H8H", 0x60, 1, 0, 12, 24, 36, 0xc000, 0xc03f, 0xff3f, 0xff00)+b"\xff\xff")
    tiled, tiling = tile_mesh(untiled, mesh_origin, tile_size=512)
    return groups, tiled, {
        "source_record": 99, "original_cell_offset": ACCESS_SOURCE_CELL,
        "foot_z_stored": ACCESS_FOOT_Z, "deck_z_stored": ACCESS_DECK_Z,
        "x_span_stored": ACCESS_X, "collision_corners_stored": collision,
        "render_corners_stored": visible, "foot_heights": evidence,
        "max_foot_rounding_error_stored": str(max(errors)), "texture_tiling": tiling,
        "scope": "Authored 500-unit-wide connection; original terrain is unchanged. Seam/overlap behavior requires native movement proof.",
    }


def build_additive_pair(retail_terrain, retail_dat, authored_terrain, authored_dat):
    for label, raw, expected in (
        ("retail terrain", retail_terrain, RETAIL_TERRAIN_SHA),
        ("retail DAT", retail_dat, RETAIL_DAT_SHA),
        ("authored terrain", authored_terrain, AUTHORED_TERRAIN_SHA),
        ("authored DAT", authored_dat, AUTHORED_DAT_SHA),
    ):
        immutable(raw, label)
        if digest(raw) != expected:
            raise ValueError(f"Pinned {label} hash mismatch")
    original = TerrainAll.parse(retail_terrain)
    donor = TerrainAll.parse(authored_terrain)
    if original.records[99].world_base != donor.records[99].world_base:
        raise ValueError("Collision origins differ")
    donor_payload = donor.collision_payload(99)
    donor_prefix = authored_terrain[donor_payload.offset:donor_payload.terminator_offset]
    donor_dat = LevelDat.parse(authored_dat)
    donor_ref = donor_dat.static_mesh_reference("primary", 160)
    _, end = mesh_groups(authored_dat, donor_ref)
    donor_mesh = authored_dat[donor_ref.geometry_offset:end+2]
    vertices, _ = decode_mesh(donor_mesh)
    mesh_origin = struct.unpack_from("<3i", authored_dat, donor_ref.object_offset)
    bridge_groups, bridge_mesh, bridge = access_ramp(original, mesh_origin, vertices[0][6:])
    terrain, allocation = append_collision_groups(retail_terrain, donor_prefix+bridge_groups+b"\xff\xff", source_index=99)
    dat, render = append_render_geometry(retail_dat, [(donor_mesh, mesh_origin), (bridge_mesh, mesh_origin)],
                                        record_index=160, neutral_depth=True)
    return terrain, dat, {
        "experiment": "EXP-20260905-009", "arm": "additive-originals-retained",
        "terrain_sha256": digest(terrain), "level_dat_sha256": digest(dat),
        "source_hashes": {"retail_terrain": RETAIL_TERRAIN_SHA, "retail_dat": RETAIL_DAT_SHA,
                          "authored_terrain": AUTHORED_TERRAIN_SHA, "authored_dat": AUTHORED_DAT_SHA},
        "collision_allocation": allocation, "render_allocation": render, "access_ramp": bridge,
        "source99_payload_offset": allocation["payload_offset"],
        "mesh160_geometry_offset": render["geometry_offset"], "mesh160_stream_bytes": render["stream_bytes"],
        "acceptance": "Unvalidated candidate until regressions and original-PC loader/movement probes pass; runtime appearance remains separate.",
    }
