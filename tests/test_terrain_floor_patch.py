"""Shared-corner preservation, complete face streams and original trajectories."""
import importlib.util
from pathlib import Path
import struct
from types import SimpleNamespace

import pytest

from ablpc.terrain_all import TerrainAll, TerrainFormatError
from ablpc.level_dat import LevelDat, DatFormatError
from ablpc.terrain_floor_patch import (boundary_census, contains, displacement_at,
    floor_cells, mesh_groups, normal, polygons_touch, stitch_floor_vertex)

ROOT = Path(__file__).resolve().parents[1]


def synthetic():
    center = (0, 0, 0)
    corners = ((100, 0, 0), (0, 0, -100), (-100, 0, 0), (0, 0, 100))
    payloads = []
    for first in (0, 2):
        cells = []
        for i in range(first, first+2):
            a, b, c = center, corners[i], corners[(i+1) % 4]
            cells.append(struct.pack("<14h4b", *normal((a, b, c)), *a, *b, *c,
                                     -100, 200, -2, 4, -2, 4))
        payloads.append(struct.pack("<6h", 0x1234, 2, -100, 200, -100, 200)
                        + b"".join(cells) + b"\xff\xffopaque")
    records = []
    for payload in payloads:
        record = bytearray(b"\x55"*76)
        struct.pack_into("<I4i", record, 0, len(payload)//2, 0, 0, 0, 6)
        struct.pack_into("<2h", record, 68, -1, 0)
        records.append(record)
    directory = 4+sum(map(len, payloads))
    return (struct.pack("<I", directory//2)+b"".join(payloads)
            +struct.pack("<I", 2)+b"".join(records)+b"opaque suffix")


@pytest.mark.parametrize("dy", (-64, -1, 0, 97, 900))
def test_shared_corner_crosses_sources_and_preserves_unselected_fields(dy):
    raw = synthetic()
    changed, edits = stitch_floor_vertex(raw, (0, 0, 0), dy)
    if dy == 0:
        assert changed == raw and not edits
        return
    assert len(edits) == 4
    cells = floor_cells(TerrainAll.parse(changed))
    assert {c.source for c in cells} == {0, 1}
    assert all((0, dy, 0) in c.vertices for c in cells)
    allowed = {c.offset+i for c in cells for i in (*range(6), 8, 9, 14, 15, 20, 21, 28, 29)}
    assert len(changed) == len(raw)
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(raw, changed, strict=True)))
    for cell in cells:
        low, span = struct.unpack_from("<2b", cell.raw, 28)
        y = cell.vertices[0][1]
        assert all(y+low*64 <= v[1] <= y+(low+span)*64 for v in cell.vertices)
        assert struct.unpack_from("<3h", cell.raw) == normal(cell.vertices)


@pytest.mark.parametrize("vertex,dy", (((1, 2), 1), ((True, 0, 0), 1), ((0, 0, 0), True),
                                      ((0, 0, 0), 1.5), ((99, 99, 99), 1),
                                      ((0, 0, 0), 40000), ((0, 0, 0), 9000)))
def test_invalid_and_unrepresentable_edits_leave_caller_bytes_unchanged(vertex, dy):
    source = bytearray(synthetic())
    before = bytes(source)
    with pytest.raises(TerrainFormatError):
        stitch_floor_vertex(source, vertex, dy)
    assert bytes(source) == before


def test_truncated_sources_and_unsupported_incident_kind_reject():
    for raw in (b"", synthetic()[:28], 123):
        with pytest.raises(TerrainFormatError):
            stitch_floor_vertex(raw, (0, 0, 0), -64)
    raw = bytearray(synthetic())
    t = TerrainAll.parse(raw)
    struct.pack_into("<i", raw, t.records[1].offset+16, 7)
    with pytest.raises(TerrainFormatError, match="unsupported"):
        stitch_floor_vertex(raw, (0, 0, 0), -64)


def test_geometry_detects_containment_crossings_and_vertical_projection():
    tri = ((0, 0), (100, 0), (0, 100))
    assert contains(tri, (20, 20))
    assert not contains(tri, (80, 80))
    assert polygons_touch(tri, ((10, 10), (20, 10), (10, 20)))
    assert polygons_touch(tri, ((-20, 30), (120, 30)))
    assert polygons_touch(tri, ((0, 0), (0, 0), (0, 0)))
    assert not polygons_touch(tri, ((101, 101), (120, 120)))


def test_continuous_displacement_agrees_at_shared_edges_and_zero_boundary():
    cells = floor_cells(TerrainAll.parse(synthetic()))
    assert displacement_at((0, 0), cells, (0, 0, 0), -64) == -64
    assert displacement_at((50, 0), cells, (0, 0, 0), -64) == -32
    assert displacement_at((100, 0), cells, (0, 0, 0), -64) == 0
    assert displacement_at((101, 0), cells, (0, 0, 0), -64) == 0


def stream_fixture():
    raw = (struct.pack("<i", 4)+bytes(48)+struct.pack("<HH8H", 0x8064, 1, 0, 12, 24, 36, 11, 22, 33, 44)
           +struct.pack("<HH6H", 0x8061, 1, 0, 12, 24, 55, 66, 77)
           +struct.pack("<HHH", 0x160, 0, 0xffff)+b"opaque tail")
    ref = SimpleNamespace(payload=SimpleNamespace(vertices_offset=4, vertex_count=4))
    return raw, ref


def test_all_mesh_groups_keep_offsets_tags_and_unknown_face_words():
    raw, ref = stream_fixture()
    groups, end = mesh_groups(raw, ref)
    assert [g["tag"] for g in groups] == [0x8064, 0x8061, 0x160]
    assert [g["offset"] for g in groups] == [52, 72, 88]
    assert groups[0]["faces"][0]["field_words"] == (11, 22, 33, 44)
    assert groups[1]["faces"][0]["vertex_indices"] == (0, 1, 2)
    assert end == 92 and raw[end+2:] == b"opaque tail"


@pytest.mark.parametrize("kind", ("negative", "count", "misaligned", "out_of_range", "truncated", "no_terminator"))
def test_mesh_stream_bounds_and_references(kind):
    raw, ref = stream_fixture()
    data = bytearray(raw)
    if kind == "negative":
        struct.pack_into("<h", data, 74, -1)
    elif kind == "count":
        struct.pack_into("<h", data, 74, 32767)
    elif kind in ("misaligned", "out_of_range"):
        struct.pack_into("<H", data, 76, 1 if kind == "misaligned" else 48)
    elif kind == "truncated":
        data = data[:74]
    else:
        data = data[:92]
    with pytest.raises(DatFormatError):
        mesh_groups(bytes(data), ref)


@pytest.fixture(scope="module")
def probe():
    spec = importlib.util.spec_from_file_location("boundary_probe", ROOT / "scripts/terrain-floor-boundary-probe.py")
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    return p


def test_fixed_corner_and_visual_edit_preservation(probe):
    if not probe.b.p.DEFAULT_BINARY.exists():
        pytest.skip("private PC work copies unavailable")
    retail, rigid, stitched, raw_dat, dat, cells, edits, visual = probe.fixture()
    assert tuple(e["file_offset"] for e in edits) == probe.EXPECTED
    assert probe.digest(rigid.data) == probe.control.RAISED_SHA256
    assert len(dat) == len(raw_dat)
    allowed = {e["field_offset"]+i for e in visual for i in (0, 1)}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(raw_dat, dat, strict=True)))
    original = {(c.source, c.offset): c for c in cells}
    updated = {(c.source, c.offset): c for c in floor_cells(stitched)}
    census = boundary_census(cells)
    assert len(census["boundaries"]) == 8
    for edge in census["boundaries"]:
        owner = edge["owner"]
        assert len(edge["full_edge_neighbors"]) == 1
        neighbor = edge["full_edge_neighbors"][0]
        a = updated[(owner["source_record"], owner["file_offset"])]
        b = updated[(neighbor["source_record"], neighbor["file_offset"])]
        for xz in edge["edge_xz_stored"]:
            assert next(v for v in a.vertices if (v[0], v[2]) == tuple(xz)) == next(v for v in b.vertices if (v[0], v[2]) == tuple(xz))


def test_original_stream_walk_on_two_pc_files(probe):
    if not probe.b.p.DEFAULT_BINARY.exists():
        pytest.skip("private PC work copies unavailable")
    text = probe.b.p.load_text(probe.b.p.DEFAULT_BINARY)
    for level in ("LEVEL01", "LEVEL03"):
        dat = LevelDat.from_path(probe.b.retail.SOURCE_ROOT / "CD" / level / "LEVEL.DAT")
        rows = probe.stream_instruction_audit(dat, text)
        assert len(rows) == sum(len(dat.static_mesh_references(section)) for section in ("primary", "secondary"))
        assert len(rows) > 0
        assert sum(r["groups"] for r in rows) > len(rows)


def test_assets_cannot_escape_work_copies(probe, tmp_path):
    with pytest.raises(ValueError, match="work/copies"):
        probe.write_fixture(tmp_path / "fixture")


@pytest.fixture(scope="module")
def original_cases(probe):
    if not probe.b.p.DEFAULT_BINARY.exists():
        pytest.skip("private PC work copies unavailable")
    retail, rigid, stitched, *_ = probe.fixture()
    text = probe.b.p.load_text(probe.b.p.DEFAULT_BINARY)
    result = {}
    for name, terrain in (("retail", retail), ("rigid", rigid), ("stitched", stitched)):
        original = probe.Probe(terrain, text)
        route = probe.return_route(original, rigid=name == "rigid")
        result[name] = {"route": route}
        if name == "stitched":
            original.floor_only = True
            cells = floor_cells(terrain)
            lookup = {(c.source, c.offset): c for c in cells}
            crossings = []
            for edge in boundary_census(cells)["boundaries"]:
                own, neighbor = edge["owner"], edge["full_edge_neighbors"][0]
                a = lookup[(own["source_record"], own["file_offset"])]
                b = lookup[(neighbor["source_record"], neighbor["file_offset"])]
                for direction in ("outward", "inward"):
                    crossings.append(probe.crossing(original, edge["edge_xz_stored"], a, b, direction))
            result[name]["crossings"] = crossings
    return result


def test_original_return_failure_and_stitched_recovery(original_cases):
    retail = original_cases["retail"]["route"]["legs"]
    rigid = original_cases["rigid"]["route"]["legs"]
    stitched = original_cases["stitched"]["route"]["legs"]
    assert rigid[1]["longest_airborne_run"] == 26
    assert rigid[2]["final"]["flags"] == [0, 0]
    assert retail[2]["final"]["flags"] == stitched[2]["final"]["flags"] == [1, 1]
    assert max(x["longest_airborne_run"] for x in stitched) <= 2
    step = rigid[1]["steps"][10]
    assert any(c["file_offset"] == 47652 for c in step["admitted_cells"])
    assert any(c["pc"] == "0x4aa646" and c["file_offset"] == 47652 and c["signed_distance"] < 0 for c in step["plane_sign_tests"])


def test_all_eight_stitched_edges_cross_in_both_directions_in_original_floor_control(original_cases):
    rows = original_cases["stitched"]["crossings"]
    assert len(rows) == 16
    assert all(row["accepted"] for row in rows)
