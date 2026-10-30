"""Translation invariants and original-instruction authoring controls."""
import importlib.util
from pathlib import Path
import struct

import pytest

from reimplementation.ablpc.terrain_all import TerrainAll, TerrainFormatError
from reimplementation.ablpc.terrain_barriers import BarrierPayload, MAGIC, SENTINEL
from reimplementation.ablpc.terrain_barrier_edit import translate_payload, translate_terrain_barrier

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("authoring_probe", ROOT / "scripts/terrain-barrier-authoring-probe.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def synthetic(count):
    points = [[i, 1000 + i, -i] for i in range(count + 1)]
    for first in range(0, count, 16):
        if count - first < 16:
            points[first][1] = SENTINEL
        else:
            # Deliberately loose bounds, so tightening would violate preservation.
            for j, value in enumerate((first - 5, 26, -first - 21, 26)):
                points[first + j][1] = value
    return struct.pack("<IHH", MAGIC, count, 0x1234) + b"".join(struct.pack("<3i", *p) for p in points) + b"opaque"


@pytest.mark.parametrize("count", (0, 1, 4, 15, 16, 17, 32, 33))
def test_translation_moves_shared_endpoints_and_loose_bounds_but_preserves_unknowns(count):
    raw = synthetic(count)
    before = BarrierPayload.parse(raw)
    moved = translate_payload(raw, 71, -93)
    after = BarrierPayload.parse(moved)
    assert len(moved) == len(raw)
    assert moved[:8] == raw[:8]
    assert after.trailer == before.trailer == b"opaque"
    metadata = {block.metadata_offset + j for block in before.blocks if block.bounds is not None for j in (0, 24)}
    for a, b in zip(before.points, after.points, strict=True):
        assert (b.x - a.x, b.z - a.z) == (71, -93)
        if a.offset + 4 not in metadata:
            assert b.middle_dword == a.middle_dword
    for a, b in zip(before.blocks, after.blocks, strict=True):
        assert after.bounds_cover_points(b)
        if a.bounds is not None:
            assert b.bounds == (a.bounds[0] + 71, a.bounds[1], a.bounds[2] - 93, a.bounds[3])
        else:
            assert b.bounds is None
    assert translate_payload(moved, -71, 93) == raw
    assert translate_payload(raw, 0, 0) == raw


@pytest.mark.parametrize("delta", ((True, 0), (0, 1.5), (2**40, 0), (0, -(2**40)), (2**27, 0)))
def test_invalid_or_overflowing_translation_rejected_without_mutating_input(delta):
    raw = bytearray(synthetic(17))
    saved = bytes(raw)
    with pytest.raises(TerrainFormatError):
        translate_payload(raw, *delta)
    assert raw == saved


def test_bad_bounds_and_missing_tail_are_not_repaired_silently():
    raw = bytearray(synthetic(17))
    struct.pack_into("<i", raw, 24, 0)
    with pytest.raises(TerrainFormatError, match="cover"):
        translate_payload(raw, 1, 1)
    raw = bytearray(synthetic(4))
    struct.pack_into("<i", raw, 12, 0)
    with pytest.raises(TerrainFormatError, match="sentinel"):
        translate_payload(raw, 1, 1)


def test_container_edit_returns_immutable_bytes_and_rejects_wrong_kind_or_index():
    payload = synthetic(4)
    record = bytearray(76)
    struct.pack_into("<I", record, 0, len(payload) // 2)
    struct.pack_into("<i", record, 0x10, 0x101)
    raw = bytearray(struct.pack("<I", (4 + len(payload)) // 2) + payload + struct.pack("<I", 1) + record)
    assert isinstance(translate_terrain_barrier(raw, 0, 1, 1), bytes)
    for index in (-1, 1, True):
        with pytest.raises(TerrainFormatError, match="index"):
            translate_terrain_barrier(raw, index, 1, 1)
    struct.pack_into("<i", raw, 4 + len(payload) + 4 + 0x10, 6)
    with pytest.raises(TerrainFormatError, match="kind"):
        translate_terrain_barrier(raw, 0, 1, 1)
    with pytest.raises(TerrainFormatError, match="bytes"):
        translate_terrain_barrier(9999, 0, 1, 1)


def test_all_retail_strips_translate_and_reverse_without_other_file_changes():
    root = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD"
    paths = sorted(p for p in root.glob("LEVEL*/*.ALL") if p.name in ("TERRAIN.ALL", "TERR1.ALL"))
    if len(paths) != 18:
        pytest.skip("complete retail work-copy corpus unavailable")
    count = 0
    for path in paths:
        terrain = TerrainAll.from_path(path)
        for record in terrain.records:
            if record.field_10 != 0x101:
                continue
            moved = translate_terrain_barrier(terrain.data, record.index, 137, -251)
            end = record.payload_offset + record.payload_size
            assert moved[:record.payload_offset] == terrain.data[:record.payload_offset]
            assert moved[end:] == terrain.data[end:]
            assert translate_terrain_barrier(moved, record.index, -137, 251) == terrain.data
            count += 1
    assert count == 65


@pytest.fixture(scope="module")
def measured():
    if not probe.b.p.DEFAULT_BINARY.exists():
        pytest.skip("retail work-copy executable unavailable")
    return probe.report()


def test_authored_file_is_exactly_the_live_tested_fixture(measured):
    source, modified = probe.fixture()
    strip = BarrierPayload.from_terrain(source, 179)
    assert modified.data[:strip.offset] == source.data[:strip.offset]
    assert modified.data[strip.offset + 68:] == source.data[strip.offset + 68:]
    assert measured["modified_sha256"] == "7329b620ba5038be2ba3d94e1d08be68935e06c51ef03b5defb45737efeda0ac"


def test_original_instructions_respond_at_new_site_and_stop_responding_at_old_site(measured):
    retail, moved = measured["arms"]
    assert retail["landing"] == moved["landing"]
    assert retail["landing"]["after"]["flags"] == [1, 1]
    assert all(not step["segment_updates"] for step in retail["steps"])
    assert [i for i, step in enumerate(moved["steps"]) if step["segment_updates"]] == list(range(13, 22))
    # Nearby admission changes before impact, so execution traces may differ
    # while position/contact/response remain the same.
    for a, b in zip(retail["steps"][:13], moved["steps"][:13], strict=True):
        assert {k: v for k, v in a.items() if k != "execution"} == {k: v for k, v in b.items() if k != "execution"}
    assert retail["old_site"]["movement"]["segment_updates"]
    assert not moved["old_site"]["movement"]["segment_updates"]
    assert retail["unrelated_floor"] == moved["unrelated_floor"]


def test_fixture_writer_refuses_paths_outside_work_copies(tmp_path):
    with pytest.raises(probe.b.p.ProbeError, match="work/copies"):
        probe.write_fixture(tmp_path / "TERRAIN.ALL")
    assert not (tmp_path / "TERRAIN.ALL").exists()


def test_previous_experiment_remains_unchanged():
    assert probe.b.digest(ROOT / "scripts/terrain-barrier-probe.py") == "ede60a7dfe65faff8a778c8db5092d6ca657cfad25a64261fbe6ef5694fa7df8"
    assert probe.b.digest(ROOT / "reports/terrain/EXP-20260904-003.json") == "10ae67083823eec74f6fe5b8d4b08dce7af57d4da00e172b37c9349346eaf6e6"
