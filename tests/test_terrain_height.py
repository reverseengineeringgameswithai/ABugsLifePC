"""Tests for the engine-faithful TERRAIN.ALL height query (EXP-20260816-141)."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import struct
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))

from ablpc.terrain_all import TerrainAll, TerrainFormatError  # noqa: E402
from ablpc.terrain_height import (  # noqa: E402
    HeightResult,
    TerrainHeightModel,
    _idiv,
    QUERY_SENTINEL_Y,
)

LEVEL03_TERRAIN = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL03/TERRAIN.ALL"
LEVEL04_TERRAIN = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL04/TERRAIN.ALL"
LEVEL03_SHA256 = "b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c"
LEVEL04_SHA256 = "9cf8fb6990a955a808f2e4f2c22ffce3fe5d62136f4a9271bdc444a6dd7fc103"


def _cell(
    *,
    slope_x: int = 0,
    divisor: int = -1,
    slope_z: int = 0,
    x0: int = 0,
    h0: int = 0,
    z0: int = 0,
    dx1: int = 64,
    dz1: int = 0,
    dx2: int = 0,
    dz2: int = -64,
    box_x_min: int = 0,
    box_x_span: int = 0x40,
    box_z_base: int = 0,
    box_z_span: int = 2,
) -> bytes:
    cell = bytearray(0x20)
    struct.pack_into("<h", cell, 0x00, slope_x)
    struct.pack_into("<h", cell, 0x02, divisor)
    struct.pack_into("<h", cell, 0x04, slope_z)
    struct.pack_into("<h", cell, 0x06, x0)
    struct.pack_into("<h", cell, 0x08, h0)
    struct.pack_into("<h", cell, 0x0A, z0)
    struct.pack_into("<h", cell, 0x0C, dx1)
    struct.pack_into("<h", cell, 0x10, dz1)
    struct.pack_into("<h", cell, 0x12, dx2)
    struct.pack_into("<h", cell, 0x16, dz2)
    struct.pack_into("<h", cell, 0x18, box_x_min)
    struct.pack_into("<h", cell, 0x1A, box_x_span)
    struct.pack_into("<b", cell, 0x1E, box_z_base)
    struct.pack_into("<b", cell, 0x1F, box_z_span)
    return bytes(cell)


def _payload(cells: tuple[bytes, ...]) -> bytes:
    payload = bytearray()
    payload.extend(struct.pack("<hhhhhh", 1, len(cells), 0, 0x40, 0, 0x40))
    for cell in cells:
        payload.extend(cell)
    payload.extend(struct.pack("<hh", -1, 0))
    return bytes(payload)


def _record(
    payload_word_count: int,
    base: tuple[int, int, int],
    *,
    tag: int = 6,
    result_word: int = 0,
    field_44: int = -1,
    field_46: int = 0,
) -> bytes:
    record = bytearray(0x4C)
    struct.pack_into("<Iiii", record, 0, payload_word_count, *base)
    struct.pack_into("<i", record, 0x10, tag)
    struct.pack_into("<h", record, 0x28, result_word)
    struct.pack_into("<hh", record, 0x44, field_44, field_46)
    return bytes(record)


def _terrain(records_and_payloads: list[tuple[bytes | None, bytes]]) -> bytes:
    payload_blob = bytearray()
    records = []
    for payload, record in records_and_payloads:
        if payload is None:
            payload = b""
        assert struct.unpack_from("<I", record, 0)[0] * 2 == len(payload)
        payload_blob.extend(payload)
        records.append(record)
    directory_offset = 4 + len(payload_blob)
    assert directory_offset % 2 == 0
    blob = bytearray(struct.pack("<I", directory_offset // 2))
    blob.extend(payload_blob)
    blob.extend(struct.pack("<I", len(records)))
    for record in records:
        blob.extend(record)
    return bytes(blob)


def _single_cell_model(cell: bytes, *cells: bytes, **record_kwargs) -> TerrainHeightModel:
    payload = _payload((cell, *cells))
    record = _record(len(payload) // 2, (0, 100, 0), **record_kwargs)
    return TerrainHeightModel(TerrainAll.parse(_terrain([(payload, record)])))


# The default triangle is V0=(0,0), V1=(64,0), V2=(0,-64) in cell units;
# local point (10,-10) — world (320,-320) — lies inside for divisor < 0.
INSIDE_X, INSIDE_Z = 320, -320


def test_idiv_truncates_toward_zero() -> None:
    assert _idiv(56, -16) == -3
    assert _idiv(-56, 16) == -3
    assert _idiv(-56, -16) == 3
    assert _idiv(56, 16) == 3


def test_flat_floor_plane_height_and_rest_y() -> None:
    model = _single_cell_model(_cell(h0=10))
    result = model.query(INSIDE_X, INSIDE_Z)
    assert result is not None
    # base_y = 100*32 = 3200; plane = 3200 + 4*(10<<3) = 3520.
    assert result.kind == "floor"
    assert result.plane_height == 3520
    assert result.height == 3520 + 0xC80
    assert result.rest_y == 3520 + 0xC80 - 0x100
    assert not result.ambiguous
    hits = model.planes(INSIDE_X, INSIDE_Z)
    assert len(hits) == 1 and hits[0].plane_height == 3520
    assert hits[0].mode == 1 and hits[0].result == 0


def test_sloped_plane_uses_toward_zero_division() -> None:
    # numerator = ((lx - x0) * slope_x) << 3 = (10*7)<<3 = 560 at lx=10;
    # idiv(560, -16) = -35 exactly; pick slope 5 for a non-exact case:
    # (10*5)<<3 = 400; idiv(400, -16) = -25; and at lx=-10 the numerator
    # is -400 with quotient 25 (toward zero, not floor).
    model = _single_cell_model(
        _cell(slope_x=5, divisor=-16, dx1=64, dz1=0, dx2=0, dz2=-64)
    )
    inside = model.query(INSIDE_X, INSIDE_Z)
    assert inside is not None
    assert inside.plane_height == 3200 + 4 * (0 - (-25))
    model_neg = _single_cell_model(
        _cell(slope_x=5, divisor=-16, dx1=0, dz1=-64, dx2=-64, dz2=0)
    )
    # Mirror triangle covering (-10,-10): V0=(0,0), V1=(0,-64), V2=(-64,0).
    result = model_neg.query(-320, -320)
    assert result is not None
    assert result.plane_height == 3200 + 4 * (0 - 25)


def test_positive_divisor_floor_never_returns() -> None:
    # Reversed winding triangle contains the point with divisor > 0; the
    # resolver tracks it as the best floor but discards a non-negative
    # divisor at the end (0x004ACD2E) and there is no ceiling candidate.
    model = _single_cell_model(
        _cell(divisor=1, dx1=0, dz1=-64, dx2=64, dz2=0)
    )
    hits = model.planes(INSIDE_X, INSIDE_Z)
    assert len(hits) == 1 and hits[0].mode == 2
    assert model.query(INSIDE_X, INSIDE_Z) is None


def test_ceiling_branch_returns_mode_one_plane_at_or_below_query() -> None:
    model = _single_cell_model(_cell(h0=10))
    result = model.query(INSIDE_X, INSIDE_Z, y=3520)
    assert result is not None
    # y_adj = 3520 - 0x600 < 3520, so the plane is not below the query and
    # resolves through the ceiling branch with the same +0xC80 offset.
    assert result.kind == "ceiling"
    assert result.height == 3520 + 0xC80


def test_floor_tie_prefers_greater_divisor_and_flags_ambiguity() -> None:
    model = _single_cell_model(
        _cell(h0=10, divisor=-16),
        _cell(h0=10, divisor=-1),
    )
    result = model.query(INSIDE_X, INSIDE_Z)
    assert result is not None
    assert result.plane_height == 3520
    assert result.cell_divisor == -1
    assert result.ambiguous is True


def test_cell_box_window_excludes_point() -> None:
    # cx_c = trunc((320+0x1000)/32) = 138; box_x_min=200 makes the unsigned
    # window test fail exactly as at 0x004AC606.
    model = _single_cell_model(_cell(box_x_min=200, box_x_span=10))
    assert model.planes(INSIDE_X, INSIDE_Z) == ()
    assert model.query(INSIDE_X, INSIDE_Z) is None


def test_clone_descriptor_shifts_planes_by_its_own_base() -> None:
    payload = _payload((_cell(h0=10),))
    template = _record(
        len(payload) // 2, (0, 100, 0), field_44=7, field_46=0
    )
    clone = _record(0, (1000, 200, 1000), field_44=7, field_46=1)
    model = TerrainHeightModel(
        TerrainAll.parse(_terrain([(payload, template), (None, clone)]))
    )
    original = model.query(INSIDE_X, INSIDE_Z)
    assert original is not None and original.plane_height == 3520
    moved = model.query(1000 * 32 + INSIDE_X, 1000 * 32 + INSIDE_Z)
    assert moved is not None
    assert moved.plane_height == 200 * 32 + 4 * (10 << 3)
    assert moved.descriptor_index == 1
    assert model.descriptors[1].clone_of == 0


def test_clone_with_unregistered_template_is_rejected() -> None:
    clone = _record(0, (0, 0, 0), field_44=9, field_46=1)
    with pytest.raises(TerrainFormatError, match="unregistered template"):
        TerrainHeightModel(TerrainAll.parse(_terrain([(None, clone)])))


def _retail_model(path: Path, sha256: str) -> TerrainHeightModel:
    if not path.is_file():
        pytest.skip("ignored retail-derived corpus is not present")
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == sha256
    return TerrainHeightModel(TerrainAll.parse(data))


def test_retail_receipt_points_reproduce_engine_heights() -> None:
    """Cross-check against independently accepted runtime receipts.

    The row-6 walkable point Y originates from the engine's own reset
    placement (EXP-129/130) and must reproduce exactly; the other three
    receipts are settled standing positions observed 121-126 units deeper
    (PC Y grows downward) than the reset placement.
    """

    level03 = _retail_model(LEVEL03_TERRAIN, LEVEL03_SHA256)
    level04 = _retail_model(LEVEL04_TERRAIN, LEVEL04_SHA256)

    exact = level03.query(501696, 494016)
    assert exact is not None and exact.kind == "floor"
    assert exact.rest_y == 30092  # EXP-130 accepted walkable point, exact
    assert exact.descriptor_index == 552

    for model, x, z, computed_rest, observed_standing in (
        (level03, 497247, 547255, 31176, 31299),  # EXP-129 endpoint
        (level04, -87622, -182181, 796, 917),  # EXP-137 trigger
        (level04, -92603, -181281, 972, 1098),  # EXP-137 approach
    ):
        result = model.query(x, z)
        assert result is not None and result.kind == "floor"
        assert result.rest_y == computed_rest
        assert 121 <= observed_standing - result.rest_y <= 126


def test_retail_descriptor_bounds_match_exp131_x_but_not_group_z() -> None:
    """Loader-literal bounds vs the EXP-131 group-header table.

    The runtime bounds recompute at 0x004A8A1A derives descriptor boxes
    from cell fields.  For Level03 descriptors 570-578 the X bounds agree
    exactly with EXP-131's group-header table while the Z bounds do not;
    the contradiction is recorded in the experiment note rather than
    silently normalized.  Pin one exact loader-literal Z value so any
    change in this derivation is caught.
    """

    level03 = _retail_model(LEVEL03_TERRAIN, LEVEL03_SHA256)
    exp131_x = {
        570: (176384, 236416),
        571: (470112, 528288),
        572: (471712, 529888),
        573: (1111712, 1169888),
        574: (1174272, 1203360),
        575: (1615456, 1674144),
        576: (816864, 875936),
        577: (1454496, 1515104),
        578: (811648, 880288),
    }
    for index, (x_low, x_high) in exp131_x.items():
        descriptor = level03.descriptors[index]
        assert descriptor.x_min == x_low
        assert descriptor.x_min + descriptor.x_span == x_high
    descriptor_570 = level03.descriptors[570]
    assert descriptor_570.z_min == 101632  # EXP-131 table records 98112
    assert descriptor_570.result == 1 and descriptor_570.tag == 6


def test_retail_pit_planes_show_downward_y_and_reset_surface() -> None:
    level03 = _retail_model(LEVEL03_TERRAIN, LEVEL03_SHA256)
    pit = level03.planes(500000, 522000)
    assert [hit.result for hit in pit] == [1]
    assert pit[0].descriptor_index == 572
    assert pit[0].rest_y == 64032  # deeper than the 30092 walkable ground
    walkable = level03.planes(501696, 494016)
    assert [hit.result for hit in walkable] == [0]


def _load_standoffs_module():
    script = ROOT / "scripts" / "grain-gate-standoffs.py"
    spec = importlib.util.spec_from_file_location("ablpc_standoffs", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_retail_standoff_report_is_deterministic_and_complete() -> None:
    if not (LEVEL03_TERRAIN.is_file() and LEVEL04_TERRAIN.is_file()):
        pytest.skip("ignored retail-derived corpus is not present")
    standoffs = _load_standoffs_module()
    report = standoffs.build_report(ROOT)
    tunnels = report["levels"]["3-tunnels"]
    city = report["levels"]["4-city-entrance"]
    assert [gate["mechanism"] for gate in tunnels] == [
        f"T{i}" for i in range(9)
    ]
    assert [gate["mechanism"] for gate in city] == ["C0", "C1", "C2"]
    for gate in (*tunnels, *city):
        assert gate["chosen"] is not None, gate["mechanism"]
        chosen = gate["chosen"]
        assert chosen["valid"] and chosen["spread"] <= standoffs.MAX_SPREAD
    assert tunnels[3]["proven_point"]["y"] == 30092
    assert city[0]["proven_point"]["y"] == 917
    # Determinism: a second build reproduces the identical report.
    assert standoffs.build_report(ROOT) == report


def test_query_sentinel_matches_helper_result_shape() -> None:
    model = _single_cell_model(_cell(h0=10))
    result = model.query(INSIDE_X, INSIDE_Z, y=QUERY_SENTINEL_Y)
    assert isinstance(result, HeightResult)
    assert result.matched_cells == 1
