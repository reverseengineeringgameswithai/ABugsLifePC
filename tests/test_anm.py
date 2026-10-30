from __future__ import annotations

import json
from pathlib import Path
import struct

import pytest

from reimplementation.ablpc.anm import AnmFile, AnmFormatError
from reimplementation.ablpc.cli import main as cli_main


def synthetic_anm(
    *,
    offsets: tuple[int, ...] = (0x14, 0, 0x50),
    item_values: tuple[int, ...] = (1, -2, 7),
    size: int = 0x60,
) -> bytes:
    source = bytearray(size)
    struct.pack_into("<HhHH", source, 0, 0x1111, len(offsets), 0x2222, 0x3333)
    for index, offset in enumerate(offsets):
        struct.pack_into("<I", source, 8 + index * 4, offset)
    first = next((offset for offset in offsets if offset), None)
    if first is not None and first + 12 + len(item_values) * 2 <= size:
        struct.pack_into(
            "<HHIHH",
            source,
            first,
            0x4444,
            0x5555,
            0x66666666,
            len(item_values),
            0x7777,
        )
        for index, value in enumerate(item_values):
            struct.pack_into("<h", source, first + 12 + index * 2, value)
    return bytes(source)


def test_parser_is_lossless_and_reports_only_bounded_fields() -> None:
    source = synthetic_anm()
    parsed = AnmFile.parse(source)

    assert parsed.data == source
    assert parsed.field_00 == 0x1111
    assert parsed.offset_count == 3
    assert parsed.field_04 == 0x2222
    assert parsed.field_06 == 0x3333
    assert parsed.offset_table_end == 0x14
    assert [item.relative_offset for item in parsed.offset_references] == [
        0x14,
        None,
        0x50,
    ]
    first = parsed.first_referenced_record
    assert first is not None
    assert first.offset == 0x14
    assert first.item_count == 3
    assert first.items_offset == 0x20
    assert first.items_end_offset == 0x26
    assert first.minus_two_indices == (1,)


def test_parser_accepts_zero_offsets_without_inventing_a_record() -> None:
    source = synthetic_anm(offsets=(0, 0), size=0x20)
    parsed = AnmFile.parse(source)

    assert parsed.data == source
    assert parsed.first_referenced_record is None
    assert all(item.relative_offset is None for item in parsed.offset_references)


@pytest.mark.parametrize("size", range(8))
def test_parser_rejects_truncated_header(size: int) -> None:
    with pytest.raises(AnmFormatError, match="ANM header"):
        AnmFile.parse(bytes(size))


def test_parser_rejects_negative_and_impossible_offset_counts() -> None:
    negative = bytearray(8)
    struct.pack_into("<h", negative, 2, -1)
    with pytest.raises(AnmFormatError, match="negative offset count"):
        AnmFile.parse(bytes(negative))

    impossible = bytearray(8)
    struct.pack_into("<h", impossible, 2, 1)
    with pytest.raises(AnmFormatError, match="impossible offset count"):
        AnmFile.parse(bytes(impossible))


def test_parser_rejects_out_of_range_first_level_offset() -> None:
    source = bytearray(synthetic_anm())
    struct.pack_into("<I", source, 8, len(source))
    with pytest.raises(AnmFormatError, match="outside file size"):
        AnmFile.parse(bytes(source))


def test_parser_rejects_truncated_first_referenced_header() -> None:
    source = synthetic_anm(offsets=(0x1C,), size=0x20)
    with pytest.raises(AnmFormatError, match="first referenced record header"):
        AnmFile.parse(source)


def test_parser_rejects_impossible_nested_item_count() -> None:
    source = bytearray(synthetic_anm())
    struct.pack_into("<H", source, 0x14 + 8, 0xFFFF)
    with pytest.raises(AnmFormatError, match="impossible first referenced"):
        AnmFile.parse(bytes(source))


def test_inspect_anm_cli_emits_metadata_only_json(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "fixture.anm"
    path.write_bytes(synthetic_anm())

    assert cli_main(["inspect-anm", str(path), "--json"]) == 0
    output = json.loads(capsys.readouterr().out)

    assert output["file_size"] == 0x60
    assert output["offset_count"] == 3
    assert output["offset_references"][0]["relative_offset"] == 0x14
    assert "data" not in output


def test_scan_anm_reports_each_file_and_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "valid.ANM").write_bytes(synthetic_anm())
    (tmp_path / "invalid.anm").write_bytes(bytes(4))
    (tmp_path / "ignored.ALL").write_bytes(bytes(4))

    assert cli_main(["scan-anm", str(tmp_path), "--json"]) == 1
    output = json.loads(capsys.readouterr().out)

    assert output["files_scanned"] == 2
    assert output["failures"] == 1
    assert [entry["path"] for entry in output["files"]] == [
        "invalid.anm",
        "valid.ANM",
    ]


# --- Per-slot records, as read by pose sampler 0x00445FF0 ---------------------


def synthetic_record(
    slot: int,
    *,
    frames: int = 2,
    part_offsets: tuple[int, ...] = (0, 6, -3, -2),
    words: int = 15,
    mask: bytes = b"\x02\x00",
    list_count: int | None = None,
) -> bytes:
    """One record: header, part list, mask, then ``frames`` frames of words."""
    count = len(part_offsets) if list_count is None else list_count
    head = struct.pack("<6H", slot, frames, len(part_offsets), words, count, len(mask))
    body = struct.pack(f"<{len(part_offsets)}h", *part_offsets)
    body += bytes(2 * (count - len(part_offsets))) + mask
    frame_data = b"".join(
        struct.pack(f"<{words}h", *(f * 100 + w for w in range(words)))
        for f in range(frames)
    )
    return head + body + frame_data


def synthetic_records_anm(records: tuple[bytes | None, ...]) -> bytes:
    table_end = 8 + 4 * len(records)
    offsets, blobs, cursor = [], b"", table_end
    for record in records:
        offsets.append(0 if record is None else cursor)
        if record is not None:
            blobs += record
            cursor += len(record)
    header = struct.pack("<HhHH", 0, len(records), 0, 0)
    return header + struct.pack(f"<{len(records)}I", *offsets) + blobs


def test_records_split_parts_by_sampler_classes_and_mask() -> None:
    source = synthetic_records_anm((synthetic_record(0), None, synthetic_record(2)))
    records = AnmFile.parse(source).records()

    assert records[1] is None
    record = records[0]
    assert record is not None
    assert (record.slot, record.frame_count, record.part_count) == (0, 2, 4)
    assert record.words_per_frame == 15 and record.mask == b"\x02\x00"
    assert record.driven_parts == (0, 1)
    assert record.inherited_parts == (2,)
    assert record.skipped_parts == (3,)
    assert record.trailing_bytes == 0
    assert record.part_width(0) == 6 and record.part_width(1) == 9
    pose = record.part_pose(1, 1)
    assert pose is not None
    assert pose.linear == (106, 107, 108)
    assert pose.angles == (109, 110, 111)
    assert pose.extra == (112, 113, 114)
    assert record.part_pose(0, 0).extra is None
    assert record.part_pose(0, 2) is None
    assert records[2].field_00 == 2


def test_records_keep_unknown_frame_flag_and_report_trailing_bytes() -> None:
    record = bytearray(synthetic_record(0))
    struct.pack_into("<H", record, 2, 0x8002)
    source = synthetic_records_anm((bytes(record) + b"\xAA\xBB",))
    parsed = AnmFile.parse(source).records()[0]

    assert parsed.flag_8000 and parsed.frame_count == 2
    assert parsed.trailing_bytes == 2
    assert AnmFile.parse(source).data == source


@pytest.mark.parametrize(
    ("record", "message"),
    [
        (synthetic_record(0)[:11], "header"),
        (synthetic_record(0)[:-1], "frame data"),
        (synthetic_record(0, part_offsets=(0, 6, -4, -2)), "unknown negative"),
        (synthetic_record(0, part_offsets=(0, 7, -3, -2)), "exceed"),
        (synthetic_record(0, mask=b""), "cannot cover"),
        (synthetic_record(0, list_count=3, part_offsets=(0, 6, -3)), None),
    ],
)
def test_records_reject_reads_outside_the_record(record: bytes, message: str | None) -> None:
    if message is None:  # part count above list count needs a hand-built header
        record = bytearray(record)
        struct.pack_into("<H", record, 4, 4)
        message = "exceeds its list count"
    source = synthetic_records_anm((bytes(record), synthetic_record(1)))
    with pytest.raises(AnmFormatError, match=message):
        AnmFile.parse(source).records()


def test_records_reject_frame_reads_past_the_record_end() -> None:
    record = synthetic_record(0)
    with pytest.raises(AnmFormatError, match="frame 2 outside"):
        AnmFile.parse(synthetic_records_anm((record,))).records()[0].frame_words(2)


def test_records_reject_an_offset_inside_the_offset_table() -> None:
    source = bytearray(synthetic_records_anm((synthetic_record(0),)))
    struct.pack_into("<I", source, 8, 4)
    with pytest.raises(AnmFormatError, match="inside the offset table"):
        AnmFile.parse(bytes(source)).records()
