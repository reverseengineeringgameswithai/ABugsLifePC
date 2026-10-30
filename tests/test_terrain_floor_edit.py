"""Bounded rigid floor edits, preservation, and original-instruction behavior."""
import importlib.util
from pathlib import Path
import struct

import pytest

from reimplementation.ablpc.terrain_all import TerrainAll, TerrainFormatError
from reimplementation.ablpc.terrain_floor_edit import translate_floor_group

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("floor_probe", ROOT / "scripts/terrain-floor-authoring-probe.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def synthetic(*, height=100, normal=-16384, kind=6, template=-1, clone=0, base_y=20):
    cell = struct.pack("<16h", 0, normal, 0, 10, height, 30, 40, 0, 50, 60, 0, 70, -5, 100, 0x04ff, 0x07fe)
    payload = struct.pack("<6h", 1, 1, -100, 400, -100, 400) + cell
    payload += struct.pack("<6h", 1, 1, -100, 400, -100, 400) + cell
    payload += struct.pack("<h", -1) + b"opaque"
    directory = 4 + len(payload)
    record = bytearray(76)
    struct.pack_into("<I3ii", record, 0, len(payload) // 2, 10, base_y, 30, kind)
    struct.pack_into("<hh", record, 0x44, template, clone)
    return struct.pack("<I", directory // 2) + payload + struct.pack("<I", 1) + record + b"unknown suffix"


@pytest.mark.parametrize("dy", (-32768, -64, 0, 97, 32000))
def test_rigid_translation_preserves_all_other_bytes_and_reverses(dy):
    raw = synthetic(); t = TerrainAll.parse(raw)
    c = t.collision_payload(0).groups[0].cells[0]
    changed = translate_floor_group(raw, 0, 0, dy)
    assert len(changed) == len(raw)
    assert changed[:c.offset + 8] == raw[:c.offset + 8]
    assert changed[c.offset + 10:] == raw[c.offset + 10:]
    assert struct.unpack_from("<h", changed, c.offset + 8)[0] == 100 + dy
    assert translate_floor_group(changed, 0, 0, -dy) == raw


@pytest.mark.parametrize("args", ((-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 2, 1), (True, 0, 1), (0, 0, 1.5), (0, 0, True), (0, 0, 32768), (0, 0, -40000)))
def test_bad_indices_types_and_overflow_leave_input_unchanged(args):
    raw = bytearray(synthetic()); before = bytes(raw)
    with pytest.raises(TerrainFormatError):
        translate_floor_group(raw, *args)
    assert raw == before


@pytest.mark.parametrize("kwargs", ({"kind": 0x101}, {"template": 0}, {"clone": 1}, {"normal": 0}, {"normal": 16384}, {"base_y": 2**30}))
def test_unsupported_sources_and_wrapping_world_coordinates_are_rejected(kwargs):
    with pytest.raises(TerrainFormatError):
        translate_floor_group(synthetic(**kwargs), 0, 0, -64)


def test_malformed_inputs_are_rejected():
    for raw in (b"", b"\0" * 4, synthetic()[:30], 123):
        with pytest.raises(TerrainFormatError):
            translate_floor_group(raw, 0, 0, 1)
    raw = bytearray(synthetic()); struct.pack_into("<h", raw, 6, 32767)
    with pytest.raises(TerrainFormatError):
        translate_floor_group(raw, 0, 0, 1)


def test_multiple_retail_files_roundtrip_each_supported_group():
    root = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD"
    paths = [root / f"LEVEL{i:02d}/TERRAIN.ALL" for i in (1, 3)]
    if not all(p.exists() for p in paths):
        pytest.skip("retail work copies unavailable")
    counts = []
    for path in paths:
        t = TerrainAll.from_path(path); count = 0
        for r in t.records:
            if (r.field_10, r.field_44, r.field_46) != (6, -1, 0):
                continue
            for i, g in enumerate(t.collision_payload(r.index).groups):
                if not g.cells or any(c.words[1] >= 0 for c in g.cells):
                    continue
                changed = translate_floor_group(t.data, r.index, i, -1)
                assert translate_floor_group(changed, r.index, i, 1) == t.data
                allowed = {c.offset + d for c in g.cells for d in (8, 9)}
                assert all(a == b or j in allowed for j, (a, b) in enumerate(zip(t.data, changed, strict=True)))
                count += 1
        counts.append(count)
    assert all(count > 100 for count in counts)


@pytest.fixture(scope="module")
def measured():
    if not probe.b.p.DEFAULT_BINARY.exists():
        pytest.skip("retail work-copy executable unavailable")
    return probe.report()


def test_original_landing_and_grounded_walk_translate_exactly(measured):
    a, b = measured["arms"]
    assert a["spawn_plane_heights"] == [-336]
    assert b["spawn_plane_heights"] == [-2384]
    for aa, bb in [(a["landing"], b["landing"]), *zip(a["steps"][:23], b["steps"][:23], strict=True)]:
        x, y, z = aa["after"]["position"]
        assert bb["after"]["position"] == [x, y - 2048, z]
        assert aa["after"]["flags"] == bb["after"]["flags"]
        assert aa["after"]["contact_cell"] == bb["after"]["contact_cell"]
    assert a["landing"]["after"]["flags"] == b["landing"]["after"]["flags"] == [1, 1]


def test_leaving_edge_causes_extra_fall_then_landing_on_unchanged_floor(measured):
    a, b = measured["arms"]
    assert a["steps"][22]["after"]["flags"] == b["steps"][22]["after"]["flags"] == [0, 0]
    assert a["steps"][23]["after"]["flags"] == [1, 1]
    assert b["steps"][23]["after"]["flags"] == b["steps"][24]["after"]["flags"] == [0, 0]
    assert b["steps"][25]["after"]["flags"] == [1, 1]
    assert a["steps"][23]["after"]["contact_cell"] == b["steps"][25]["after"]["contact_cell"] == {"source": "level01", "source_record": 99, "file_offset": 47544}
    assert a["unrelated_floor"] == b["unrelated_floor"]


def test_fixture_refuses_output_outside_work_copies(tmp_path):
    with pytest.raises(probe.b.p.ProbeError, match="work/copies"):
        probe.write_fixture(tmp_path / "TERRAIN.ALL")
