"""Tests for the engine-exact type-1 reset resolver (EXP-20260816-153).

Synthetic fixtures cover the selector contract, its wrapping arithmetic, and
the boundaries where this module deliberately refuses instead of emulating
undefined original behaviour.  The retail-derived cases are hash-pinned and
skip when the ignored work copy is absent; they are the differential test
against independently accepted PC runtime receipts.
"""

from __future__ import annotations

import hashlib
from math import isqrt
from pathlib import Path
import struct
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))

from ablpc.level03_type1_row_mod import (  # noqa: E402
    _edit_exact_type1_row,
    build_level03_type1_row6_x_plus_128,
)
from ablpc.level_dat import LevelDat  # noqa: E402
from ablpc.terrain_height import HeightResult, TerrainHeightModel  # noqa: E402
from ablpc.type1_reset import (  # noqa: E402
    HEIGHT_FAILURE_REST_Y,
    POINTER_TABLE_ROOT,
    TYPE1_POINTER_SLOT,
    Type1ResetError,
    Type1Row,
    engine_type1_record,
    pointer_table_slot,
    read_type1_table,
    resolve,
    row_distance,
    row_distance_wraps,
    row_placements,
    select_row,
    shadowed_rows,
    summary,
)

CD = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD"
LEVEL03_DAT = CD / "LEVEL03/LEVEL.DAT"
LEVEL03_TERRAIN = CD / "LEVEL03/TERRAIN.ALL"
LEVEL03_DAT_SHA256 = "bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b"
LEVEL03_TERRAIN_SHA256 = (
    "b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c"
)


# --------------------------------------------------------------------------
# synthetic fixtures
# --------------------------------------------------------------------------


def _top_record(count: int, type_id: int, elements: bytes) -> bytes:
    return struct.pack("<hh", count, type_id) + elements


def _rows_blob(rows: list[tuple[int, int, int]]) -> bytes:
    return b"".join(struct.pack("<iii", *row) for row in rows)


def _synthetic_dat(records: list[bytes]) -> bytes:
    """Minimal parseable LEVEL*.DAT prefix wrapping the given top records."""

    body = struct.pack("<i", len(records)) + b"".join(records)
    sentinel = bytearray(20)
    struct.pack_into("<h", sentinel, 0x0E, -1)
    tail = (
        struct.pack("<i", 0)  # fixed-record count
        + bytes(sentinel)  # empty primary section
        + struct.pack("<i", -1)  # index-table maximum
        + bytes(sentinel)  # empty secondary section
    )
    data = bytearray(body + tail)
    struct.pack_into("<i", data, len(data) - 4, -1)
    return bytes(data)


def _dat_with_rows(rows: list[tuple[int, int, int]], type_id: int = 1) -> LevelDat:
    return LevelDat.parse(
        _synthetic_dat([_top_record(len(rows), type_id, _rows_blob(rows))])
    )


class _StubHeightModel:
    """Duck-typed stand-in; terrain maths is covered by test_terrain_height."""

    def __init__(self, heights: dict[tuple[int, int], int]) -> None:
        self.heights = heights
        self.queries: list[tuple[int, int, int]] = []

    def query(self, x: int, z: int, y: int) -> HeightResult | None:
        self.queries.append((x, z, y))
        height = self.heights.get((x, z))
        if height is None:
            return None
        return HeightResult(
            height=height,
            kind="floor",
            plane_height=height - 0xC80,
            descriptor_index=7,
            cell_divisor=-1,
            matched_cells=1,
            ambiguous=False,
        )


# --------------------------------------------------------------------------
# loader pointer table (0x0044BB70)
# --------------------------------------------------------------------------


def test_pointer_slot_matches_loader_arithmetic() -> None:
    assert pointer_table_slot(0) == POINTER_TABLE_ROOT
    assert pointer_table_slot(1) == TYPE1_POINTER_SLOT
    assert pointer_table_slot(0x3F) == 0x005C595C
    # 0x0044BC8B subtracts a negative product, so -N aliases into slot +N.
    assert pointer_table_slot(-1) == TYPE1_POINTER_SLOT
    assert pointer_table_slot(-7) == pointer_table_slot(7)


def test_last_record_claiming_the_slot_wins() -> None:
    first = _top_record(1, 1, _rows_blob([(10, 0, 20)]))
    second = _top_record(1, 1, _rows_blob([(30, 0, 40)]))
    dat = LevelDat.parse(_synthetic_dat([first, second]))
    assert engine_type1_record(dat).index == 1
    table = read_type1_table(dat)
    assert [(row.x, row.z) for row in table.rows] == [(30, 40)]
    assert table.aliased_records == (0,)


def test_negative_type_alias_is_refused() -> None:
    # A type -1 record claims slot 0x005C5864 but uses the 6-byte element form.
    negative = struct.pack("<hh", 1, -1) + bytes(12 + 6 + 2)
    dat = LevelDat.parse(_synthetic_dat([negative]))
    with pytest.raises(Type1ResetError, match="aliases into slot"):
        read_type1_table(dat)


def test_file_without_a_type1_record_is_refused() -> None:
    dat = LevelDat.parse(_synthetic_dat([_top_record(0, 0x3F, b"")]))
    with pytest.raises(Type1ResetError, match="no top record claims"):
        read_type1_table(dat)


def test_zero_row_count_is_refused_instead_of_emulated() -> None:
    dat = _dat_with_rows([])
    with pytest.raises(Type1ResetError, match="uninitialised best-index"):
        read_type1_table(dat)


def test_truncated_rows_are_refused() -> None:
    dat = _dat_with_rows([(1, 0, 2)])
    truncated = LevelDat.parse(dat.data)
    object.__setattr__(truncated, "data", dat.data[: dat.top_records[0].offset + 8])
    with pytest.raises(Type1ResetError, match="beyond the"):
        read_type1_table(truncated)


# --------------------------------------------------------------------------
# scan arithmetic (0x0043297D-0x004329AE)
# --------------------------------------------------------------------------


def test_row_distance_uses_arithmetic_shifts_not_division() -> None:
    row = Type1Row(index=0, offset=0, x=0, middle=0, z=0)
    # sar rounds toward -inf: (-33 >> 5) == -2, then (-2 >> 3) == -1.
    assert row_distance(row, -33, 0) == 1
    # truncating division would give 0 for both steps.
    assert row_distance(row, -1, 0) == 1
    assert row_distance(row, 0, 0) == 0
    # positive side: 33 >> 5 == 1, 1 >> 3 == 0.
    assert row_distance(row, 33, 0) == 0


def test_row_distance_matches_hand_computed_engine_values() -> None:
    row = Type1Row(index=0, offset=0, x=15539, middle=0, z=17102)
    # EXP-20260815-129 fall 1 contact position, engine-exact:
    # (494438 >> 5) - 15539 = -88 -> -11; (526143 >> 5) - 17102 = -661 -> -83.
    assert row_distance(row, 494438, 526143) == 11 * 11 + 83 * 83


def test_lowest_index_wins_a_tie() -> None:
    # -8 >> 3 and 8 >> 3 both have magnitude 1, so the two rows tie exactly.
    table = read_type1_table(_dat_with_rows([(8, 0, 0), (-8, 0, 0)]))
    selection = select_row(table, 0, 0)
    assert selection.index == 0
    assert selection.distance == 1
    assert selection.tied_indices == (1,)


def test_distance_overflow_wraps_and_can_select_a_far_row() -> None:
    """The engine compares wrapped signed sums; a far row can win."""

    near = (0, 0, 0)
    # dz >> 3 == 0xC000; 0xC000 ** 2 == 0x90000000, negative when truncated.
    far = (0, 0, -0xC000 * 8)
    table = read_type1_table(_dat_with_rows([near, far]))
    selection = select_row(table, 0, 0)
    assert row_distance(table.rows[1], 0, 0) == -0x70000000
    assert row_distance_wraps(table.rows[1], 0, 0) is True
    assert row_distance_wraps(table.rows[0], 0, 0) is False
    assert selection.index == 1
    assert selection.distance < 0
    assert selection.overflowed is True


def test_distance_can_never_equal_the_initial_best_value() -> None:
    """``0x00432953`` seeds the best distance with ``0x7FFFFFFF``.

    A row can only lose to that seed by scoring ``0x7FFFFFFF`` or more, and
    after 32-bit truncation nothing exceeds it.  Two squares sum to 0, 1 or
    2 modulo 4, truncation by 2**32 preserves that residue, and
    ``0x7FFFFFFF`` is 3 modulo 4 — so the seed is always beaten and the
    original's uninitialised-index path is reachable only through a zero row
    count.  The refusal below is defensive, not observed.
    """

    for x in range(-40, 41):
        for z in range(-40, 41):
            row = Type1Row(index=0, offset=0, x=x, middle=0, z=z)
            for query in (-1234, -33, 0, 7, 4096, 1 << 20):
                assert row_distance(row, query, query) % 4 != 3


# --------------------------------------------------------------------------
# placement (0x004329B0-0x004329F6)
# --------------------------------------------------------------------------


def test_placement_scales_by_thirty_two_and_wraps_at_32_bits() -> None:
    table = read_type1_table(_dat_with_rows([(3, 0, -5), (1 << 27, 0, 0)]))
    assert (table.rows[0].placement_x, table.rows[0].placement_z) == (96, -160)
    # shl truncates: (1 << 27) << 5 == 1 << 32 -> 0.
    assert table.rows[1].placement_x == 0


def test_resolve_uses_the_sentinel_query_and_rest_y_relation() -> None:
    table = read_type1_table(_dat_with_rows([(10, 0, 20)]))
    model = _StubHeightModel({(320, 640): 5000})
    placement = resolve(table, model, 320, 640)
    assert model.queries == [(320, 640, 0x7FFFFFFF)]
    assert placement.position == (320, 5000 - 0x100, 640)
    assert placement.height_failed is False
    assert placement.descriptor_index == 7


def test_failed_height_query_reproduces_the_engine_sentinel_relation() -> None:
    table = read_type1_table(_dat_with_rows([(10, 0, 20)]))
    placement = resolve(table, _StubHeightModel({}), 0, 0)
    assert placement.height_failed is True
    # 0x004ACDB2 stores 0x80000000; 0x004329F1 subtracts 0x100 with wrap.
    assert placement.y == HEIGHT_FAILURE_REST_Y == 0x7FFFFF00
    assert resolve(table, None, 0, 0).y == HEIGHT_FAILURE_REST_Y


def test_row_placements_and_shadowed_rows_report_authoring_hazards() -> None:
    table = read_type1_table(
        _dat_with_rows([(10, 0, 20), (99, 0, 99), (10, 0, 20)])
    )
    model = _StubHeightModel({(320, 640): 5000})
    placements = row_placements(table, model)
    assert [placement.height_failed for placement in placements] == [
        False,
        True,
        False,
    ]
    assert placements[1].y == HEIGHT_FAILURE_REST_Y
    # Row 2 duplicates row 0, so the strict comparison can never reach it.
    assert shadowed_rows(table) == ((2, 0),)


def test_summary_preserves_the_unread_middle_field() -> None:
    table = read_type1_table(_dat_with_rows([(10, 1234, 20)]))
    report = summary(table)
    assert report["row_count"] == 1
    assert report["rows"][0]["middle"] == 1234
    assert report["rows"][0]["placement_x"] == 320


# --------------------------------------------------------------------------
# differential tests against retained PC runtime receipts
# --------------------------------------------------------------------------


def _retail(path: Path, sha256: str) -> bytes:
    if not path.is_file():
        pytest.skip("ignored retail-derived corpus is not present")
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == sha256
    return data


def test_level03_natural_pit_falls_reproduce_the_observed_row7_reset() -> None:
    """EXP-20260815-129: two natural pit falls, one repeated endpoint.

    Both observed post-reset samples were (497247, 31299, 547255).  The
    selector writes the scaled row exactly; the observed sample is the first
    *settled* position, deeper (PC world Y grows downward).  This receipt's
    +123 sits inside the band EXP-20260816-141/142 accepted from three
    standing receipts; EXP-20260816-156 later widened the observed extremes
    to 121-129.
    """

    table = read_type1_table(LevelDat.parse(_retail(LEVEL03_DAT, LEVEL03_DAT_SHA256)))
    model = TerrainHeightModel.from_path(
        _retail_path(LEVEL03_TERRAIN, LEVEL03_TERRAIN_SHA256)
    )
    assert table.count == 18
    assert (table.rows[7].x, table.rows[7].z) == (15539, 17102)
    assert table.rows[7].offset == 0x4B0

    for query_x, query_z in ((494438, 526143), (505717, 526449), (501522, 540782)):
        placement = resolve(table, model, query_x, query_z)
        assert placement.selection.index == 7
        assert (placement.x, placement.z) == (497248, 547264)
        assert placement.height_failed is False
        assert 121 <= 31299 - placement.y <= 126
        # The trace sampled collision 543/0 right after the reset; the
        # terrain model reaches the same descriptor from the file bytes.
        assert placement.descriptor_index == 543


def test_level03_row6_walkable_point_is_its_own_reset_fixed_point() -> None:
    """EXP-20260815-130/141: the accepted walkable point reproduces exactly.

    Its Y originated from this engine path, so the computed rest Y must
    match the observed value with zero delta.
    """

    table = read_type1_table(LevelDat.parse(_retail(LEVEL03_DAT, LEVEL03_DAT_SHA256)))
    model = TerrainHeightModel.from_path(
        _retail_path(LEVEL03_TERRAIN, LEVEL03_TERRAIN_SHA256)
    )
    placement = resolve(table, model, 501696, 494016)
    assert placement.selection.index == 6
    assert placement.selection.distance == 0
    assert placement.position == (501696, 30092, 494016)
    assert placement.descriptor_index == 552


def test_level03_candidate_row6_reproduces_the_exp116_runtime_delta() -> None:
    """EXP-20260815-116/117: row-6 X 15678 -> 15806 moved runtime X by +4096."""

    source = _retail(LEVEL03_DAT, LEVEL03_DAT_SHA256)
    control = read_type1_table(LevelDat.parse(source))
    candidate = read_type1_table(
        LevelDat.parse(build_level03_type1_row6_x_plus_128(source).output_bytes)
    )
    query = (501696, 494016)

    control_selection = select_row(control, *query)
    candidate_selection = select_row(candidate, *query)
    assert control_selection.index == candidate_selection.index == 6
    assert control.rows[6].placement_x == 501696
    assert candidate.rows[6].placement_x == 505792
    assert candidate.rows[6].placement_x - control.rows[6].placement_x == 4096
    assert control.rows[6].placement_z == candidate.rows[6].placement_z == 494016


def test_retail_corpus_type1_tables_are_bounded_and_consistent() -> None:
    """Metadata-only census over the 21 retail-derived ``LEVEL*.DAT`` files.

    Seven files carry no type-1 record at all, so the loader never writes the
    slot for them and the module refuses rather than guessing what the live
    slot holds (unresolved, KU-064).  Four files contain rows this selector
    can never reach
    because a lower index shares their exact X/Z — in Level04 and Level08
    those duplicates form out-and-back sequences, which is consistent with
    the separate index-ordered type-1 consumers (``0x004369B0``) and is one
    more reason not to call type 1 a respawn table.
    """

    if not CD.is_dir():
        pytest.skip("ignored retail-derived corpus is not present")
    files = sorted(CD.rglob("LEVEL*.DAT"))
    assert len(files) == 21

    counts: dict[str, int] = {}
    shadowed: dict[str, int] = {}
    for path in files:
        key = str(path.relative_to(CD))
        dat = LevelDat.from_path(path)
        try:
            table = read_type1_table(dat)
        except Type1ResetError as error:
            assert "no top record claims" in str(error), key
            continue
        counts[key] = table.count
        assert table.count > 0
        assert table.aliased_records == ()
        assert table.offset + 4 + table.count * 12 <= len(dat.data)
        for row in table.rows:
            # Every retail row scales without wrapping.
            assert row.placement_x == row.x * 32
            assert row.placement_z == row.z * 32
        if shadowed_rows(table):
            shadowed[key] = len(shadowed_rows(table))

    assert len(counts) == 14
    assert counts["LEVEL03/LEVEL.DAT"] == 18
    assert shadowed == {
        "LEVEL02/LEVEL1.DAT": 1,
        "LEVEL04/LEVEL1.DAT": 28,
        "LEVEL04/LEVEL4.DAT": 28,
        "LEVEL08/LEVEL1.DAT": 233,
    }


def test_level04_secondary_type1_rows_form_an_out_and_back_sequence() -> None:
    """The duplicates are mirrored around one pivot, not scattered."""

    path = CD / "LEVEL04/LEVEL1.DAT"
    if not path.is_file():
        pytest.skip("ignored retail-derived corpus is not present")
    table = read_type1_table(LevelDat.from_path(path))
    assert shadowed_rows(table) == tuple(
        (30 + step, 28 - step) for step in range(28)
    )
    # The mirrored rows repeat the full triple, so even a three-coordinate
    # consumer sees the same point twice; only row order separates them.
    for later, earlier in shadowed_rows(table):
        assert table.rows[later].middle == table.rows[earlier].middle


def test_level03_rows_pair_one_to_one_with_the_nine_grain_gates() -> None:
    """Structural cross-check against independently accepted gate geometry.

    EXP-20260815-136/139 fixed the nine Tunnels gate centres from executable
    immediates; this table comes from level data.  Rows 2n and 2n+1 are the
    two rows nearest gate n for every gate, one at 13.7k-18.0k units and one
    at 37.2k-39.4k, while the next-nearest gate is 284k or more away.  The
    numbers are confirmed; reading authoring intent into the pairing is
    inference, and this module still does not name type 1 a respawn table.
    """

    table = read_type1_table(LevelDat.parse(_retail(LEVEL03_DAT, LEVEL03_DAT_SHA256)))
    gates = _load_standoffs_module().TUNNELS_GATES
    assert len(gates) == 9 and table.count == 18

    assignment: dict[int, list[int]] = {}
    distances: dict[int, list[int]] = {}
    second: list[int] = []
    for row in table.rows:
        ranked = sorted(
            (
                isqrt((row.placement_x - x) ** 2 + (row.placement_z - z) ** 2),
                gate,
            )
            for gate, _requirement, x, z in gates
        )
        nearest, gate = ranked[0]
        assignment.setdefault(gate, []).append(row.index)
        distances.setdefault(gate, []).append(nearest)
        second.append(ranked[1][0])

    assert assignment == {gate: [2 * gate, 2 * gate + 1] for gate in range(9)}
    # Which member of a pair is nearer is not fixed by index parity: at gate 1
    # the odd row is the near one.  Classify within each pair instead.
    near = [min(pair) for pair in distances.values()]
    far = [max(pair) for pair in distances.values()]
    # Exact recorded extremes, as integer square roots of exact squares.
    assert (min(near), max(near)) == (13_729, 17_993)
    assert (min(far), max(far)) == (37_231, 39_316)
    assert min(second) == 303_653


def _load_standoffs_module():
    import importlib.util

    script = ROOT / "scripts" / "grain-gate-standoffs.py"
    spec = importlib.util.spec_from_file_location("ablpc_standoffs_t1", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_report_module():
    import importlib.util

    script = ROOT / "scripts" / "type1-reset.py"
    spec = importlib.util.spec_from_file_location("ablpc_type1_reset_cli", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_report_tool_is_deterministic_and_matches_the_receipts() -> None:
    if not (LEVEL03_DAT.is_file() and LEVEL03_TERRAIN.is_file()):
        pytest.skip("ignored retail-derived corpus is not present")
    tool = _load_report_module()

    query = tool.build_report(LEVEL03_DAT, LEVEL03_TERRAIN, (494438, 526143))
    assert query == tool.build_report(LEVEL03_DAT, LEVEL03_TERRAIN, (494438, 526143))
    assert query["query"]["selected_row"] == 7
    placement = query["query"]["placement"]
    assert (placement["reset_x"], placement["reset_y"], placement["reset_z"]) == (
        497248,
        31176,
        547264,
    )
    low, high = placement["settled_y_estimate"]
    assert low <= 31299 <= high  # EXP-20260815-129 observed settled Y
    assert query["level_dat"]["sha256"] == LEVEL03_DAT_SHA256
    assert query["unreachable_rows"] == []

    # The band must cover every accepted settle receipt, including the
    # EXP-20260816-156 control arm at +123 from the row-6 placement.
    control = tool.build_report(LEVEL03_DAT, LEVEL03_TERRAIN, (501696, 494016))
    control_low, control_high = control["query"]["placement"]["settled_y_estimate"]
    assert control_low <= 30215 <= control_high

    listing = tool.build_report(LEVEL03_DAT, LEVEL03_TERRAIN, None)
    assert len(listing["rows"]) == 18
    assert not any(row["height_failed"] for row in listing["rows"])


def test_settle_band_covers_the_exp156_candidate_receipt() -> None:
    """The +129 receipt that widened the band must fall inside it.

    EXP-20260816-156 edited row 6's Z to 15694, the engine wrote reset Y
    31768, and Flik settled at 31897.  A band that excluded 31897 would be
    contradicted by the packet that produced it.
    """

    source = _retail(LEVEL03_DAT, LEVEL03_DAT_SHA256)
    _retail(LEVEL03_TERRAIN, LEVEL03_TERRAIN_SHA256)
    candidate = _edit_exact_type1_row(
        source,
        expected_source_sha256=LEVEL03_DAT_SHA256,
        expected_table_index=1,
        expected_table_offset=0x458,
        expected_count=18,
        row_index=6,
        expected_position=(15678, 0, 15438),
        output_position=(15678, 0, 15694),
    ).output_bytes
    assert (
        hashlib.sha256(candidate).hexdigest()
        == "91a27776b84626ba400817cb5968699f685a3b9fbbeb63bff101e5d514cb8965"
    )

    table = read_type1_table(LevelDat.parse(candidate))
    model = TerrainHeightModel.from_path(LEVEL03_TERRAIN)
    placement = resolve(table, model, 501696, 494016)
    assert placement.position == (501696, 31768, 502208)  # observed exactly

    tool = _load_report_module()
    assert placement.y + tool.SETTLE_LOW <= 31897 <= placement.y + tool.SETTLE_HIGH


def test_report_tool_without_terrain_reports_the_failure_sentinel() -> None:
    if not LEVEL03_DAT.is_file():
        pytest.skip("ignored retail-derived corpus is not present")
    tool = _load_report_module()
    listing = tool.build_report(LEVEL03_DAT, None, None)
    assert listing["terrain"] is None
    assert all(row["height_failed"] for row in listing["rows"])
    assert {row["reset_y"] for row in listing["rows"]} == {HEIGHT_FAILURE_REST_Y}
    assert listing["rows"][6]["reset_x"] == 501696


def _retail_path(path: Path, sha256: str) -> Path:
    _retail(path, sha256)
    return path
