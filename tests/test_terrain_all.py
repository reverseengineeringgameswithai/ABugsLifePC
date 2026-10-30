from __future__ import annotations

from pathlib import Path
import struct

import pytest

from reimplementation.ablpc.terrain_all import TerrainAll, TerrainFormatError, main


def _source_record(
    payload_word_count: int,
    xyz: tuple[int, int, int],
    *,
    field_10: int = 6,
    result_word: int = 0,
    field_44: int = -1,
    field_46: int = 0,
) -> bytes:
    record = bytearray(0x4C)
    struct.pack_into("<Iiii", record, 0, payload_word_count, *xyz)
    struct.pack_into("<i", record, 0x10, field_10)
    struct.pack_into("<h", record, 0x28, result_word)
    struct.pack_into("<hh", record, 0x44, field_44, field_46)
    return bytes(record)


def _collision_payload(
    groups: tuple[tuple[int, int, int, int], ...],
) -> bytes:
    payload = bytearray()
    for minimum_x, span_x, minimum_z, span_z in groups:
        payload.extend(
            struct.pack(
                "<hhhhhh16h",
                1,
                1,
                minimum_x,
                span_x,
                minimum_z,
                span_z,
                *range(16),
            )
        )
    payload.extend(struct.pack("<hh", -1, 0x1234))
    return bytes(payload)


def synthetic_terrain(*, two_groups: bool = False) -> bytes:
    groups = ((-2, 10, 3, 5), (8, 4, -6, 2)) if two_groups else ((-2, 10, 3, 5),)
    payload = _collision_payload(groups)
    directory_offset = 4 + len(payload)
    source = bytearray(struct.pack("<I", directory_offset // 2))
    source.extend(payload)
    source.extend(struct.pack("<I", 2))
    source.extend(
        _source_record(
            len(payload) // 2,
            (100, 200, -300),
            result_word=1,
        )
    )
    source.extend(
        _source_record(
            0,
            (400, 500, 600),
            result_word=3,
            field_44=7,
            field_46=1,
        )
    )
    source.extend(b"UNKNOWN-SUFFIX")
    return bytes(source)


@pytest.mark.parametrize("two_groups", [False, True])
def test_parser_is_lossless_and_preserves_unknown_bytes(two_groups: bool) -> None:
    source = synthetic_terrain(two_groups=two_groups)
    terrain = TerrainAll.parse(source)

    assert terrain.data == source
    assert len(terrain.records) == 2
    assert terrain.records[0].raw == source[
        terrain.records[0].offset : terrain.records[0].offset + 0x4C
    ]
    assert terrain.records[0].world_base == (3200, 6400, -9600)
    assert terrain.records[0].result_word == 1
    assert terrain.records[1].field_44 == 7
    assert terrain.records[1].field_46 == 1
    assert terrain.suffix == b"UNKNOWN-SUFFIX"

    payload = terrain.collision_payload(0)
    assert payload.raw == source[payload.offset : payload.offset + payload.size]
    assert len(payload.groups) == (2 if two_groups else 1)
    assert payload.groups[0].cells[0].words == tuple(range(16))
    assert payload.trailer == struct.pack("<h", 0x1234)
    expected = (3136, 3584, -9792, -9344) if two_groups else (3136, 3456, -9504, -9344)
    assert terrain.world_xz_bounds(0) == expected


def test_parser_rejects_invalid_offsets_counts_and_payload_chains() -> None:
    with pytest.raises(TerrainFormatError, match="directory word offset"):
        TerrainAll.parse(b"\x00\x00")
    with pytest.raises(TerrainFormatError, match="directory offset"):
        TerrainAll.parse(struct.pack("<I", 1) + bytes(8))

    source = bytearray(synthetic_terrain())
    directory = struct.unpack_from("<I", source, 0)[0] * 2
    struct.pack_into("<I", source, directory, 2**31)
    with pytest.raises(TerrainFormatError, match="source-record count"):
        TerrainAll.parse(bytes(source))

    source = bytearray(synthetic_terrain())
    directory = struct.unpack_from("<I", source, 0)[0] * 2
    struct.pack_into("<I", source, directory + 4, 1)
    with pytest.raises(TerrainFormatError, match="payload chain ends"):
        TerrainAll.parse(bytes(source))


def test_collision_payload_rejects_truncation_and_missing_terminator() -> None:
    source = bytearray(synthetic_terrain())
    terrain = TerrainAll.parse(bytes(source))
    source[terrain.records[0].payload_offset + 2 : terrain.records[0].payload_offset + 4] = struct.pack("<h", 100)
    corrupt = TerrainAll.parse(bytes(source))
    with pytest.raises(TerrainFormatError, match="overruns"):
        corrupt.collision_payload(0)

    source = bytearray(synthetic_terrain())
    terrain = TerrainAll.parse(bytes(source))
    terminator = terrain.collision_payload(0).terminator_offset
    struct.pack_into("<h", source, terminator, 0)
    corrupt = TerrainAll.parse(bytes(source))
    with pytest.raises(
        TerrainFormatError, match="group header|collision group|no negative terminator"
    ):
        corrupt.collision_payload(0)

    with pytest.raises(TerrainFormatError, match="no collision payload"):
        terrain.collision_payload(1)


def test_json_cli_filters_result_word(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "TERRAIN.ALL"
    path.write_bytes(synthetic_terrain(two_groups=True))

    assert main([str(path), "--result-word", "1", "--json"]) == 0
    output = capsys.readouterr().out
    assert '"record_count": 2' in output
    assert '"index": 0' in output
    assert '"index": 1' not in output


def test_cli_retains_unparsed_bounds_as_an_explicit_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = bytearray(synthetic_terrain())
    terrain = TerrainAll.parse(bytes(source))
    struct.pack_into("<h", source, terrain.records[0].payload_offset + 6, -1)
    path = tmp_path / "TERRAIN.ALL"
    path.write_bytes(source)

    assert main([str(path), "--json"]) == 0
    output = capsys.readouterr().out
    assert '"world_xz_bounds": null' in output
    assert '"world_xz_bounds_error": "source record 0 has a negative collision-group span"' in output


@pytest.mark.parametrize(
    ("relative_path", "expected_count", "expected_directory"),
    [
        ("LEVEL00/TERRAIN.ALL", 74, 0x2E120),
        ("LEVEL03/TERRAIN.ALL", 592, 0x3688C),
        ("LEVEL10/TERRAIN.ALL", 301, 0x1D2A8),
    ],
)
def test_local_retail_corpus_when_available(
    relative_path: str, expected_count: int, expected_directory: int
) -> None:
    path = Path("work/copies/BUGS_PC-full-disc/PC/BUGS/CD") / relative_path
    if not path.exists():
        pytest.skip("ignored retail-derived corpus is not present")
    terrain = TerrainAll.from_path(path)
    assert len(terrain.records) == expected_count
    assert terrain.directory_offset == expected_directory
    assert terrain.suffix == b""
