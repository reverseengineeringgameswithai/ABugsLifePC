"""Conservative reader for the bounded PC ``TERRAIN.ALL`` descriptor layout.

Names in this module describe the demonstrated byte walk.  The complete input,
record bytes, collision payload bytes, and unparsed trailer bytes are retained;
no game-facing semantic name is assigned to the descriptor result word.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
import struct
from typing import Sequence


SOURCE_RECORD_SIZE = 0x4C
GROUP_HEADER_SIZE = 0x0C
CELL_SIZE = 0x20
WORLD_SCALE = 0x20


class TerrainFormatError(ValueError):
    """Raised when bytes cannot satisfy the bounded ``TERRAIN.ALL`` layout."""


@dataclass(frozen=True)
class CollisionCell:
    offset: int
    words: tuple[int, ...]
    raw: bytes


@dataclass(frozen=True)
class CollisionGroup:
    offset: int
    marker: int
    cell_count: int
    minimum_x_units: int
    span_x_units: int
    minimum_z_units: int
    span_z_units: int
    cells: tuple[CollisionCell, ...]
    raw: bytes


@dataclass(frozen=True)
class CollisionPayload:
    offset: int
    size: int
    groups: tuple[CollisionGroup, ...]
    terminator_offset: int
    trailer: bytes
    raw: bytes


@dataclass(frozen=True)
class TerrainSourceRecord:
    index: int
    offset: int
    payload_offset: int
    payload_word_count: int
    component_x: int
    component_y: int
    component_z: int
    field_10: int
    result_word: int
    field_44: int
    field_46: int
    raw: bytes

    @property
    def payload_size(self) -> int:
        return self.payload_word_count * 2

    @property
    def world_base(self) -> tuple[int, int, int]:
        return (
            self.component_x * WORLD_SCALE,
            self.component_y * WORLD_SCALE,
            self.component_z * WORLD_SCALE,
        )


@dataclass(frozen=True)
class TerrainAll:
    """Parsed offsets plus the complete unchanged source bytes."""

    data: bytes
    directory_offset: int
    records: tuple[TerrainSourceRecord, ...]
    suffix: bytes

    @classmethod
    def from_path(cls, path: Path | str) -> "TerrainAll":
        return cls.parse(Path(path).read_bytes())

    @classmethod
    def parse(cls, data: bytes) -> "TerrainAll":
        reader = _Reader(data)
        directory_word_offset = reader.u32(0, "directory word offset")
        directory_offset = directory_word_offset * 2
        if directory_offset < 4:
            raise TerrainFormatError(
                f"impossible directory offset: 0x{directory_offset:x}"
            )
        record_count = reader.u32(directory_offset, "source-record count")
        maximum_count = (reader.size - directory_offset - 4) // SOURCE_RECORD_SIZE
        if record_count > maximum_count:
            raise TerrainFormatError(
                f"impossible source-record count {record_count} at "
                f"0x{directory_offset:x}"
            )
        directory_end = directory_offset + 4 + record_count * SOURCE_RECORD_SIZE
        reader.require(directory_offset, directory_end - directory_offset, "directory")

        payload_offset = 4
        records: list[TerrainSourceRecord] = []
        for index in range(record_count):
            offset = directory_offset + 4 + index * SOURCE_RECORD_SIZE
            payload_word_count = reader.u32(
                offset, f"source record {index} payload-word count"
            )
            payload_size = payload_word_count * 2
            if payload_size > directory_offset - payload_offset:
                raise TerrainFormatError(
                    f"source record {index} payload overruns directory: "
                    f"0x{payload_offset:x} + 0x{payload_size:x}"
                )
            reader.require(payload_offset, payload_size, f"source record {index} payload")
            records.append(
                TerrainSourceRecord(
                    index=index,
                    offset=offset,
                    payload_offset=payload_offset,
                    payload_word_count=payload_word_count,
                    component_x=reader.i32(offset + 0x04, f"source record {index} +0x04"),
                    component_y=reader.i32(offset + 0x08, f"source record {index} +0x08"),
                    component_z=reader.i32(offset + 0x0C, f"source record {index} +0x0c"),
                    field_10=reader.i32(offset + 0x10, f"source record {index} +0x10"),
                    result_word=reader.i16(offset + 0x28, f"source record {index} +0x28"),
                    field_44=reader.i16(offset + 0x44, f"source record {index} +0x44"),
                    field_46=reader.i16(offset + 0x46, f"source record {index} +0x46"),
                    raw=data[offset : offset + SOURCE_RECORD_SIZE],
                )
            )
            payload_offset += payload_size

        if payload_offset != directory_offset:
            raise TerrainFormatError(
                f"payload chain ends at 0x{payload_offset:x}, not directory "
                f"0x{directory_offset:x}"
            )
        return cls(
            data=data,
            directory_offset=directory_offset,
            records=tuple(records),
            suffix=data[directory_end:],
        )

    def collision_payload(self, index: int) -> CollisionPayload:
        if index < 0 or index >= len(self.records):
            raise IndexError(
                f"source-record index {index} is outside 0..{len(self.records) - 1}"
            )
        record = self.records[index]
        if record.payload_size == 0:
            raise TerrainFormatError(f"source record {index} has no collision payload")

        reader = _Reader(self.data)
        start = record.payload_offset
        end = start + record.payload_size
        cursor = start
        groups: list[CollisionGroup] = []
        while cursor < end:
            marker = reader.i16(cursor, f"source record {index} group marker")
            if marker < 0:
                trailer_start = cursor + 2
                return CollisionPayload(
                    offset=start,
                    size=record.payload_size,
                    groups=tuple(groups),
                    terminator_offset=cursor,
                    trailer=self.data[trailer_start:end],
                    raw=self.data[start:end],
                )

            reader.require(cursor, GROUP_HEADER_SIZE, f"source record {index} group header")
            cell_count = reader.i16(cursor + 0x02, "collision-group cell count")
            if cell_count < 0:
                raise TerrainFormatError(
                    f"negative collision-group cell count {cell_count} at 0x{cursor:x}"
                )
            group_size = GROUP_HEADER_SIZE + cell_count * CELL_SIZE
            if group_size > end - cursor:
                raise TerrainFormatError(
                    f"collision group at 0x{cursor:x} overruns source record {index} payload"
                )
            cells: list[CollisionCell] = []
            for cell_index in range(cell_count):
                cell_offset = cursor + GROUP_HEADER_SIZE + cell_index * CELL_SIZE
                raw = self.data[cell_offset : cell_offset + CELL_SIZE]
                cells.append(
                    CollisionCell(
                        offset=cell_offset,
                        words=struct.unpack("<16h", raw),
                        raw=raw,
                    )
                )
            groups.append(
                CollisionGroup(
                    offset=cursor,
                    marker=marker,
                    cell_count=cell_count,
                    minimum_x_units=reader.i16(cursor + 0x04, "collision-group minimum X"),
                    span_x_units=reader.i16(cursor + 0x06, "collision-group X span"),
                    minimum_z_units=reader.i16(cursor + 0x08, "collision-group minimum Z"),
                    span_z_units=reader.i16(cursor + 0x0A, "collision-group Z span"),
                    cells=tuple(cells),
                    raw=self.data[cursor : cursor + group_size],
                )
            )
            cursor += group_size

        raise TerrainFormatError(
            f"source record {index} collision payload has no negative terminator"
        )

    def world_xz_bounds(self, index: int) -> tuple[int, int, int, int]:
        record = self.records[index]
        payload = self.collision_payload(index)
        if not payload.groups:
            raise TerrainFormatError(
                f"source record {index} collision payload contains no groups"
            )
        for group in payload.groups:
            if group.span_x_units < 0 or group.span_z_units < 0:
                raise TerrainFormatError(
                    f"source record {index} has a negative collision-group span"
                )
        base_x, _, base_z = record.world_base
        minimum_x = base_x + min(group.minimum_x_units for group in payload.groups) * WORLD_SCALE
        maximum_x = base_x + max(
            group.minimum_x_units + group.span_x_units for group in payload.groups
        ) * WORLD_SCALE
        minimum_z = base_z + min(group.minimum_z_units for group in payload.groups) * WORLD_SCALE
        maximum_z = base_z + max(
            group.minimum_z_units + group.span_z_units for group in payload.groups
        ) * WORLD_SCALE
        return minimum_x, maximum_x, minimum_z, maximum_z


class _Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.size = len(data)

    def require(self, offset: int, size: int, label: str) -> None:
        if offset < 0 or size < 0 or offset > self.size - size:
            raise TerrainFormatError(
                f"{label} exceeds file bounds: offset=0x{offset:x}, size=0x{size:x}, "
                f"file=0x{self.size:x}"
            )

    def u32(self, offset: int, label: str) -> int:
        self.require(offset, 4, label)
        return struct.unpack_from("<I", self.data, offset)[0]

    def i32(self, offset: int, label: str) -> int:
        self.require(offset, 4, label)
        return struct.unpack_from("<i", self.data, offset)[0]

    def i16(self, offset: int, label: str) -> int:
        self.require(offset, 2, label)
        return struct.unpack_from("<h", self.data, offset)[0]


def _record_summary(terrain: TerrainAll, record: TerrainSourceRecord) -> dict[str, object]:
    summary: dict[str, object] = {
        "index": record.index,
        "record_offset": record.offset,
        "payload_offset": record.payload_offset,
        "payload_size": record.payload_size,
        "base": record.world_base,
        "field_10": record.field_10,
        "result_word": record.result_word,
        "field_44": record.field_44,
        "field_46": record.field_46,
    }
    if record.payload_size:
        try:
            summary["world_xz_bounds"] = terrain.world_xz_bounds(record.index)
        except TerrainFormatError as error:
            summary["world_xz_bounds"] = None
            summary["world_xz_bounds_error"] = str(error)
    else:
        summary["world_xz_bounds"] = None
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect the bounded PC TERRAIN.ALL source-descriptor layout."
    )
    parser.add_argument("path", type=Path)
    parser.add_argument("--result-word", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    terrain = TerrainAll.from_path(args.path)
    records = [
        record
        for record in terrain.records
        if args.result_word is None or record.result_word == args.result_word
    ]
    summaries = [_record_summary(terrain, record) for record in records]
    if args.json:
        print(
            json.dumps(
                {
                    "path": str(args.path),
                    "size": len(terrain.data),
                    "directory_offset": terrain.directory_offset,
                    "record_count": len(terrain.records),
                    "suffix_size": len(terrain.suffix),
                    "records": summaries,
                },
                indent=2,
            )
        )
        return 0

    print(
        "index\trecord_offset\tpayload_offset\tpayload_size\tbase_x\tbase_y\tbase_z"
        "\tfield_10\tresult_word\tmin_x\tmax_x\tmin_z\tmax_z"
    )
    for summary in summaries:
        base_x, base_y, base_z = summary["base"]
        bounds = summary["world_xz_bounds"]
        if bounds is None:
            bounds = ("", "", "", "")
        print(
            "\t".join(
                str(value)
                for value in (
                    summary["index"],
                    f"0x{summary['record_offset']:x}",
                    f"0x{summary['payload_offset']:x}",
                    summary["payload_size"],
                    base_x,
                    base_y,
                    base_z,
                    summary["field_10"],
                    summary["result_word"],
                    *bounds,
                )
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
