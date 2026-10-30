"""Conservative parser for the confirmed prefix of PC LEVEL*.DAT files.

The names in this module describe byte layout, not game semantics. Unknown data is
retained in the original byte string; edits patch only explicitly selected fields.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct
from pathlib import Path
from typing import Literal


SCENE_RECORD_SIZE = 20
FIXED_RECORD_SIZE = 128
PAYLOAD_TARGET_ENTRY_SIZE = 12
SUPPORTED_SCENE_DISPATCH_MASK = 0xBFEF
SUPPORTED_SCENE_DISPATCH_VALUE = 0x49
STATIC_MESH_SCENE_DISPATCH_VALUE = 0x41
STATIC_MESH_VERTEX_SIZE = 12


class DatFormatError(ValueError):
    """Raised when a file cannot satisfy the bounded LEVEL*.DAT layout."""


@dataclass(frozen=True)
class TopRecord:
    index: int
    offset: int
    count: int
    type_id: int
    size: int


@dataclass(frozen=True)
class SceneRecord:
    index: int
    offset: int
    center_component_00: int
    center_component_04: int
    center_component_08: int
    field_0c_signed: int
    flags: int
    payload_offset_candidate: int


@dataclass(frozen=True)
class PayloadTargetReference:
    record_index: int
    record_offset: int
    payload_offset: int
    target_field_offset: int
    target_offset: int


@dataclass(frozen=True)
class PayloadTargetCommandGroup:
    index: int
    offset: int
    mode: int
    item_count: int
    item_size: int
    items_offset: int
    end_offset: int


@dataclass(frozen=True)
class PositivePayloadTargetBlock:
    offset: int
    entry_count: int
    entries_offset: int
    command_stream_offset: int
    command_groups: tuple[PayloadTargetCommandGroup, ...]
    terminator_offset: int
    end_offset: int


@dataclass(frozen=True)
class StaticMeshVertex:
    index: int
    offset: int
    component_00: int
    component_02: int
    component_04: int
    field_06: int
    field_08: int
    field_09: int
    field_0a: int
    field_0b: int

    def to_bytes(self) -> bytes:
        return struct.pack(
            "<hhhhBBBB",
            self.component_00,
            self.component_02,
            self.component_04,
            self.field_06,
            self.field_08,
            self.field_09,
            self.field_0a,
            self.field_0b,
        )


@dataclass(frozen=True)
class StaticMeshFace:
    index: int
    offset: int
    vertex_byte_offsets: tuple[int, ...]
    field_words: tuple[int, ...]


@dataclass(frozen=True)
class StaticMeshPayload:
    offset: int
    vertex_count: int
    vertices_offset: int
    vertices: tuple[StaticMeshVertex, ...]
    tag: int
    face_count: int
    faces_offset: int
    faces: tuple[StaticMeshFace, ...]
    end_offset: int

    @property
    def is_triangle(self) -> bool:
        return bool(self.tag & 1)

    @property
    def tag_low_5(self) -> int:
        return self.tag & 0x1F

    @property
    def tag_bits_5_6(self) -> int:
        return self.tag & 0x60

    @property
    def tag_upper_index(self) -> int:
        return (self.tag >> 8) & 0x1F

    @classmethod
    def parse(cls, data: bytes, offset: int) -> "StaticMeshPayload":
        reader = _Reader(data)
        vertex_count = reader.i32(offset, "static-mesh vertex count")
        if vertex_count < 0:
            raise DatFormatError(
                f"negative static-mesh vertex count {vertex_count} at 0x{offset:x} "
                "uses an unsupported layout"
            )

        vertices_offset = offset + 4
        vertex_bytes = vertex_count * STATIC_MESH_VERTEX_SIZE
        reader.require(
            vertices_offset,
            vertex_bytes + 4,
            "static-mesh vertices and face header",
        )
        vertices = tuple(
            StaticMeshVertex(
                index=index,
                offset=vertex_offset,
                component_00=reader.i16(
                    vertex_offset, f"static-mesh vertex {index} component +0x00"
                ),
                component_02=reader.i16(
                    vertex_offset + 2,
                    f"static-mesh vertex {index} component +0x02",
                ),
                component_04=reader.i16(
                    vertex_offset + 4,
                    f"static-mesh vertex {index} component +0x04",
                ),
                field_06=reader.i16(
                    vertex_offset + 6, f"static-mesh vertex {index} field +0x06"
                ),
                field_08=data[vertex_offset + 8],
                field_09=data[vertex_offset + 9],
                field_0a=data[vertex_offset + 10],
                field_0b=data[vertex_offset + 11],
            )
            for index in range(vertex_count)
            for vertex_offset in (vertices_offset + index * STATIC_MESH_VERTEX_SIZE,)
        )

        face_header_offset = vertices_offset + vertex_bytes
        tag = reader.u16(face_header_offset, "static-mesh tag")
        face_count = reader.u16(face_header_offset + 2, "static-mesh face count")
        face_vertex_count = 3 if tag & 1 else 4
        face_size = face_vertex_count * 4
        faces_offset = face_header_offset + 4
        reader.require(
            faces_offset, face_count * face_size, "static-mesh face records"
        )

        faces: list[StaticMeshFace] = []
        for face_index in range(face_count):
            face_offset = faces_offset + face_index * face_size
            vertex_byte_offsets = tuple(
                reader.u16(
                    face_offset + item_index * 2,
                    f"static-mesh face {face_index} vertex byte offset {item_index}",
                )
                for item_index in range(face_vertex_count)
            )
            for item_index, vertex_byte_offset in enumerate(vertex_byte_offsets):
                if (
                    vertex_byte_offset % STATIC_MESH_VERTEX_SIZE != 0
                    or vertex_byte_offset >= vertex_bytes
                ):
                    raise DatFormatError(
                        f"static-mesh face {face_index} vertex byte offset "
                        f"0x{vertex_byte_offset:x} at 0x{face_offset + item_index * 2:x} "
                        f"does not select one of {vertex_count} {STATIC_MESH_VERTEX_SIZE}-byte vertices"
                    )
            field_words = tuple(
                reader.u16(
                    face_offset + face_vertex_count * 2 + item_index * 2,
                    f"static-mesh face {face_index} field word {item_index}",
                )
                for item_index in range(face_vertex_count)
            )
            faces.append(
                StaticMeshFace(
                    index=face_index,
                    offset=face_offset,
                    vertex_byte_offsets=vertex_byte_offsets,
                    field_words=field_words,
                )
            )

        return cls(
            offset=offset,
            vertex_count=vertex_count,
            vertices_offset=vertices_offset,
            vertices=vertices,
            tag=tag,
            face_count=face_count,
            faces_offset=faces_offset,
            faces=tuple(faces),
            end_offset=faces_offset + face_count * face_size,
        )

    def to_bytes(self) -> bytes:
        if len(self.vertices) != self.vertex_count:
            raise DatFormatError("static-mesh vertex count does not match vertices")
        if len(self.faces) != self.face_count:
            raise DatFormatError("static-mesh face count does not match faces")
        face_vertex_count = 3 if self.is_triangle else 4
        encoded = bytearray(struct.pack("<i", self.vertex_count))
        for vertex in self.vertices:
            encoded.extend(vertex.to_bytes())
        encoded.extend(struct.pack("<HH", self.tag, self.face_count))
        for face in self.faces:
            if (
                len(face.vertex_byte_offsets) != face_vertex_count
                or len(face.field_words) != face_vertex_count
            ):
                raise DatFormatError(
                    f"static-mesh face {face.index} does not match tag arity"
                )
            encoded.extend(
                struct.pack(
                    "<" + "H" * (face_vertex_count * 2),
                    *face.vertex_byte_offsets,
                    *face.field_words,
                )
            )
        return bytes(encoded)


@dataclass(frozen=True)
class StaticMeshReference:
    section: Literal["primary", "secondary"]
    record_index: int
    record_offset: int
    object_offset: int
    geometry_offset: int
    payload: StaticMeshPayload


@dataclass(frozen=True)
class LevelDat:
    """Parsed offsets plus the complete, unchanged source bytes."""

    data: bytes
    top_records: tuple[TopRecord, ...]
    fixed_records_offset: int
    fixed_record_count: int
    primary_records_offset: int
    primary_records: tuple[SceneRecord, ...]
    primary_sentinel_offset: int
    index_table_offset: int
    index_table_max: int
    index_table_values: tuple[int, ...]
    secondary_records_offset: int
    secondary_records: tuple[SceneRecord, ...]
    secondary_sentinel_offset: int
    parsed_prefix_end: int
    final_dword: int

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()

    @classmethod
    def from_path(cls, path: Path | str) -> "LevelDat":
        return cls.parse(Path(path).read_bytes())

    @classmethod
    def parse(cls, data: bytes) -> "LevelDat":
        reader = _Reader(data)
        top_count = reader.i32(0, "top-record count")
        if top_count < 0 or top_count > (reader.size - 4) // 4:
            raise DatFormatError(f"impossible top-record count: {top_count}")

        cursor = 4
        top_records: list[TopRecord] = []
        for index in range(top_count):
            count = reader.i16(cursor, f"top record {index} count")
            type_id = reader.i16(cursor + 2, f"top record {index} type")
            if count < 0:
                raise DatFormatError(
                    f"negative top-record element count {count} at 0x{cursor:x}"
                )
            if type_id < 0:
                size = 16 + _align_up(count * 6, 4)
            elif type_id == 0x3F:
                size = 4 + count * 16
            else:
                size = 4 + count * 12
            reader.require(cursor, size, f"top record {index}")
            top_records.append(TopRecord(index, cursor, count, type_id, size))
            cursor += size

        fixed_records_offset = cursor
        fixed_record_count = reader.i32(cursor, "fixed-record count")
        if fixed_record_count < 0:
            raise DatFormatError(
                f"negative fixed-record count {fixed_record_count} at 0x{cursor:x}"
            )
        fixed_size = fixed_record_count * FIXED_RECORD_SIZE
        reader.require(cursor + 4, fixed_size, "fixed-record section")
        cursor += 4 + fixed_size

        primary_records_offset = cursor
        primary_records, primary_sentinel_offset = _read_scene_records(
            reader, cursor, "primary"
        )
        cursor = primary_sentinel_offset + SCENE_RECORD_SIZE

        index_table_offset = cursor
        index_table_max = reader.i32(cursor, "index-table maximum")
        if index_table_max < -1:
            raise DatFormatError(
                f"impossible index-table maximum {index_table_max} at 0x{cursor:x}"
            )
        index_count = index_table_max + 1
        reader.require(cursor + 4, index_count * 4, "index table")
        index_table_values = tuple(
            reader.i32(cursor + 4 + index * 4, f"index-table entry {index}")
            for index in range(index_count)
        )
        cursor += 4 + index_count * 4

        secondary_records_offset = cursor
        secondary_records, secondary_sentinel_offset = _read_scene_records(
            reader, cursor, "secondary"
        )
        parsed_prefix_end = secondary_sentinel_offset + SCENE_RECORD_SIZE
        final_dword = reader.i32(reader.size - 4, "final dword")

        return cls(
            data=data,
            top_records=tuple(top_records),
            fixed_records_offset=fixed_records_offset,
            fixed_record_count=fixed_record_count,
            primary_records_offset=primary_records_offset,
            primary_records=primary_records,
            primary_sentinel_offset=primary_sentinel_offset,
            index_table_offset=index_table_offset,
            index_table_max=index_table_max,
            index_table_values=index_table_values,
            secondary_records_offset=secondary_records_offset,
            secondary_records=secondary_records,
            secondary_sentinel_offset=secondary_sentinel_offset,
            parsed_prefix_end=parsed_prefix_end,
            final_dword=final_dword,
        )

    def records(
        self, section: Literal["primary", "secondary"]
    ) -> tuple[SceneRecord, ...]:
        if section == "primary":
            return self.primary_records
        if section == "secondary":
            return self.secondary_records
        raise ValueError(f"unknown scene-record section: {section!r}")

    def payload_target_reference(
        self, section: Literal["primary", "secondary"], index: int
    ) -> PayloadTargetReference:
        records = self.records(section)
        if index < 0 or index >= len(records):
            raise IndexError(
                f"{section} scene-record index {index} is outside 0..{len(records) - 1}"
            )
        record = records[index]
        target_field_offset = 0x1C if record.flags & 0x08 else 0x14
        reader = _Reader(self.data)
        target_offset = reader.u32(
            record.payload_offset_candidate + target_field_offset,
            f"{section} scene-record {index} payload target",
        )
        reader.require(target_offset, 4, f"{section} scene-record {index} target block")
        return PayloadTargetReference(
            record_index=index,
            record_offset=record.offset,
            payload_offset=record.payload_offset_candidate,
            target_field_offset=target_field_offset,
            target_offset=target_offset,
        )

    def payload_target_references(
        self, section: Literal["primary", "secondary"]
    ) -> tuple[PayloadTargetReference, ...]:
        return tuple(
            self.payload_target_reference(section, index)
            for index in range(len(self.records(section)))
        )

    def supported_payload_target_references(
        self, section: Literal["primary", "secondary"]
    ) -> tuple[PayloadTargetReference, ...]:
        """Return references only for the evidenced PC dispatch-0x49 class."""

        return tuple(
            self.payload_target_reference(section, record.index)
            for record in self.records(section)
            if (record.flags & SUPPORTED_SCENE_DISPATCH_MASK)
            == SUPPORTED_SCENE_DISPATCH_VALUE
        )

    def static_mesh_reference(
        self, section: Literal["primary", "secondary"], index: int
    ) -> StaticMeshReference:
        records = self.records(section)
        if index < 0 or index >= len(records):
            raise IndexError(
                f"{section} scene-record index {index} is outside 0..{len(records) - 1}"
            )
        record = records[index]
        dispatch = record.flags & SUPPORTED_SCENE_DISPATCH_MASK
        if dispatch != STATIC_MESH_SCENE_DISPATCH_VALUE:
            raise DatFormatError(
                f"{section} scene-record {index} flags 0x{record.flags:04x} "
                "do not select the supported PC static-mesh dispatch 0x41"
            )

        reader = _Reader(self.data)
        object_offset = record.payload_offset_candidate
        reader.require(object_offset, 24, f"{section} static-mesh object")
        geometry_offset = reader.u32(
            object_offset + 0x14, f"{section} static-mesh object geometry offset"
        )
        return StaticMeshReference(
            section=section,
            record_index=index,
            record_offset=record.offset,
            object_offset=object_offset,
            geometry_offset=geometry_offset,
            payload=StaticMeshPayload.parse(self.data, geometry_offset),
        )

    def static_mesh_references(
        self, section: Literal["primary", "secondary"]
    ) -> tuple[StaticMeshReference, ...]:
        return tuple(
            self.static_mesh_reference(section, record.index)
            for record in self.records(section)
            if (record.flags & SUPPORTED_SCENE_DISPATCH_MASK)
            == STATIC_MESH_SCENE_DISPATCH_VALUE
        )

    def set_static_mesh_vertex_component(
        self,
        section: Literal["primary", "secondary"],
        record_index: int,
        vertex_index: int,
        component_offset: Literal[0, 2, 4],
        expected_value: int,
        value: int,
    ) -> bytes:
        if component_offset not in (0, 2, 4):
            raise ValueError("static-mesh component offset must be 0, 2, or 4")
        for label, candidate in (("expected value", expected_value), ("value", value)):
            if not isinstance(candidate, int) or isinstance(candidate, bool):
                raise TypeError(f"static-mesh {label} must be an integer")
            if candidate < -(2**15) or candidate > 2**15 - 1:
                raise ValueError(
                    f"static-mesh {label} is outside signed 16-bit range: {candidate}"
                )

        reference = self.static_mesh_reference(section, record_index)
        if vertex_index < 0 or vertex_index >= reference.payload.vertex_count:
            raise IndexError(
                f"static-mesh vertex index {vertex_index} is outside "
                f"0..{reference.payload.vertex_count - 1}"
            )
        field_offset = (
            reference.payload.vertices_offset
            + vertex_index * STATIC_MESH_VERTEX_SIZE
            + component_offset
        )
        current = _Reader(self.data).i16(
            field_offset,
            f"static-mesh vertex {vertex_index} component +0x{component_offset:02x}",
        )
        if current != expected_value:
            raise DatFormatError(
                f"static-mesh vertex {vertex_index} component +0x{component_offset:02x} "
                f"mismatch: expected {expected_value}, found {current}"
            )

        changed = bytearray(self.data)
        struct.pack_into("<h", changed, field_offset, value)
        return bytes(changed)

    def set_static_mesh_face_vertex_byte_offsets(
        self,
        section: Literal["primary", "secondary"],
        record_index: int,
        face_index: int,
        *,
        expected_object_offset: int,
        expected_geometry_offset: int,
        expected_offsets: tuple[int, ...],
        offsets: tuple[int, ...],
    ) -> bytes:
        """Guardedly replace one static-mesh face's vertex byte offsets."""

        reference = self.static_mesh_reference(section, record_index)
        for label, expected, current in (
            ("object", expected_object_offset, reference.object_offset),
            ("geometry", expected_geometry_offset, reference.geometry_offset),
        ):
            if not isinstance(expected, int) or isinstance(expected, bool):
                raise TypeError(f"expected static-mesh {label} offset must be an integer")
            if expected != current:
                raise DatFormatError(
                    f"static-mesh {label} offset mismatch: expected 0x{expected:x}, "
                    f"found 0x{current:x}"
                )

        payload = reference.payload
        if face_index < 0 or face_index >= payload.face_count:
            raise IndexError(
                f"static-mesh face index {face_index} is outside "
                f"0..{payload.face_count - 1}"
            )
        face = payload.faces[face_index]
        arity = 3 if payload.is_triangle else 4

        def validate_offsets(label: str, candidate: tuple[int, ...]) -> None:
            if not isinstance(candidate, tuple):
                raise TypeError(f"static-mesh {label} must be a tuple")
            if len(candidate) != arity:
                raise ValueError(
                    f"static-mesh {label} arity must be {arity}, found {len(candidate)}"
                )
            vertex_bytes = payload.vertex_count * STATIC_MESH_VERTEX_SIZE
            for item_index, item in enumerate(candidate):
                if not isinstance(item, int) or isinstance(item, bool):
                    raise TypeError(
                        f"static-mesh {label}[{item_index}] must be an integer"
                    )
                if item % STATIC_MESH_VERTEX_SIZE:
                    raise ValueError(
                        f"static-mesh {label}[{item_index}] 0x{item:x} is not "
                        f"{STATIC_MESH_VERTEX_SIZE}-byte aligned"
                    )
                if item < 0 or item >= vertex_bytes:
                    raise ValueError(
                        f"static-mesh {label}[{item_index}] 0x{item:x} is outside "
                        f"0..0x{vertex_bytes - STATIC_MESH_VERTEX_SIZE:x}"
                    )

        validate_offsets("expected face offsets", expected_offsets)
        validate_offsets("replacement face offsets", offsets)
        if face.vertex_byte_offsets != expected_offsets:
            raise DatFormatError(
                f"static-mesh face {face_index} offsets mismatch: expected "
                f"{expected_offsets}, found {face.vertex_byte_offsets}"
            )

        changed = bytearray(self.data)
        for item_index, item in enumerate(offsets):
            struct.pack_into("<H", changed, face.offset + item_index * 2, item)

        reparsed = LevelDat.parse(bytes(changed)).static_mesh_reference(
            section, record_index
        )
        if (
            reparsed.object_offset != expected_object_offset
            or reparsed.geometry_offset != expected_geometry_offset
            or reparsed.payload.faces[face_index].vertex_byte_offsets != offsets
        ):
            raise DatFormatError("static-mesh face edit failed reconstructive reparse")
        return bytes(changed)

    def positive_payload_target_block(self, offset: int) -> PositivePayloadTargetBlock:
        """Parse the positive-count target layout consumed at PC VA 0x0045A7F0.

        The negative-count branch has a different layout and remains unsupported.
        Names intentionally describe the demonstrated byte walk rather than model
        or object semantics.
        """

        reader = _Reader(self.data)
        entry_count = reader.i32(offset, "payload-target entry count")
        if entry_count < 0:
            raise DatFormatError(
                f"negative payload-target entry count {entry_count} at 0x{offset:x} "
                "uses an unsupported layout"
            )
        entries_offset = offset + 4
        entries_size = entry_count * PAYLOAD_TARGET_ENTRY_SIZE
        reader.require(entries_offset, entries_size, "payload-target entry table")
        command_stream_offset = entries_offset + entries_size
        cursor = command_stream_offset
        groups: list[PayloadTargetCommandGroup] = []

        while True:
            mode = reader.u16(cursor, "payload-target command mode or terminator")
            if mode == 0xFFFF:
                end_offset = _align_up(cursor + 2, 4)
                reader.require(cursor, end_offset - cursor, "payload-target terminator")
                return PositivePayloadTargetBlock(
                    offset=offset,
                    entry_count=entry_count,
                    entries_offset=entries_offset,
                    command_stream_offset=command_stream_offset,
                    command_groups=tuple(groups),
                    terminator_offset=cursor,
                    end_offset=end_offset,
                )

            item_count = reader.i16(cursor + 2, "payload-target command item count")
            if item_count < 0:
                raise DatFormatError(
                    f"negative payload-target command item count {item_count} "
                    f"at 0x{cursor:x}"
                )
            item_size = 12 if mode & 1 else 16
            items_offset = cursor + 4
            reader.require(
                items_offset,
                item_count * item_size,
                f"payload-target command group {len(groups)} items",
            )
            referenced_entry_count = 3 if mode & 1 else 4
            for item_index in range(item_count):
                item_offset = items_offset + item_index * item_size
                for reference_index in range(referenced_entry_count):
                    relative_offset = reader.u16(
                        item_offset + reference_index * 2,
                        "payload-target entry-table reference",
                    )
                    if (
                        relative_offset % PAYLOAD_TARGET_ENTRY_SIZE != 0
                        or relative_offset + PAYLOAD_TARGET_ENTRY_SIZE > entries_size
                    ):
                        raise DatFormatError(
                            f"payload-target command reference 0x{relative_offset:x} "
                            f"at 0x{item_offset + reference_index * 2:x} is outside "
                            f"the {entries_size}-byte entry table"
                        )
            end_offset = items_offset + item_count * item_size
            groups.append(
                PayloadTargetCommandGroup(
                    index=len(groups),
                    offset=cursor,
                    mode=mode,
                    item_count=item_count,
                    item_size=item_size,
                    items_offset=items_offset,
                    end_offset=end_offset,
                )
            )
            cursor = end_offset

    def set_record_payload_target_offset(
        self,
        section: Literal["primary", "secondary"],
        index: int,
        expected_target_offset: int,
        target_offset: int,
    ) -> bytes:
        records = self.records(section)
        if index < 0 or index >= len(records):
            raise IndexError(
                f"{section} scene-record index {index} is outside 0..{len(records) - 1}"
            )
        record = records[index]
        if (
            record.flags & SUPPORTED_SCENE_DISPATCH_MASK
        ) != SUPPORTED_SCENE_DISPATCH_VALUE:
            raise DatFormatError(
                f"{section} scene-record {index} flags 0x{record.flags:04x} "
                "do not select the supported PC 0x49 dispatch"
            )
        reference = self.payload_target_reference(section, index)
        if reference.target_offset != expected_target_offset:
            raise DatFormatError(
                f"{section} scene-record {index} target mismatch: expected "
                f"0x{expected_target_offset:x}, found 0x{reference.target_offset:x}"
            )
        self.positive_payload_target_block(reference.target_offset)
        self.positive_payload_target_block(target_offset)

        changed = bytearray(self.data)
        struct.pack_into(
            "<I",
            changed,
            reference.payload_offset + reference.target_field_offset,
            target_offset,
        )
        return bytes(changed)

    def set_record_position(
        self,
        section: Literal["primary", "secondary"],
        index: int,
        position: tuple[int, int, int],
    ) -> bytes:
        records = self.records(section)
        if index < 0 or index >= len(records):
            raise IndexError(
                f"{section} scene-record index {index} is outside 0..{len(records) - 1}"
            )
        if len(position) != 3:
            raise ValueError("position must contain exactly three integers")
        for value in position:
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError("position values must be integers")
            if value < -(2**31) or value > 2**31 - 1:
                raise ValueError(f"position value outside signed 32-bit range: {value}")

        changed = bytearray(self.data)
        struct.pack_into("<iii", changed, records[index].offset, *position)
        return bytes(changed)

    def set_record_field_0c(
        self,
        section: Literal["primary", "secondary"],
        index: int,
        expected_value: int,
        value: int,
    ) -> bytes:
        """Guard and replace the signed word at scene-record offset +0x0C.

        Static use bounds this field as a signed spatial/culling scalar, but its
        complete semantics are not established. Keep the operation offset-named
        until a discriminating original-executable experiment supports more.
        """

        records = self.records(section)
        if index < 0 or index >= len(records):
            raise IndexError(
                f"{section} scene-record index {index} is outside 0..{len(records) - 1}"
            )
        for label, candidate in (("expected value", expected_value), ("value", value)):
            if not isinstance(candidate, int) or isinstance(candidate, bool):
                raise TypeError(f"field +0x0c {label} must be an integer")
            if candidate < -(2**15) or candidate > 2**15 - 1:
                raise ValueError(
                    f"field +0x0c {label} is outside signed 16-bit range: {candidate}"
                )

        field_offset = records[index].offset + 0x0C
        current = _Reader(self.data).i16(
            field_offset, f"{section} scene-record {index} field +0x0c"
        )
        if current != expected_value:
            raise DatFormatError(
                f"{section} scene-record {index} field +0x0c mismatch: "
                f"expected {expected_value}, found {current}"
            )

        changed = bytearray(self.data)
        struct.pack_into("<h", changed, field_offset, value)
        return bytes(changed)

    def summary(self) -> dict[str, object]:
        return {
            "sha256": self.sha256,
            "size": len(self.data),
            "top_records": [
                {
                    "index": record.index,
                    "offset": record.offset,
                    "count": record.count,
                    "type_id": record.type_id,
                    "size": record.size,
                }
                for record in self.top_records
            ],
            "fixed_record_count": self.fixed_record_count,
            "primary_record_count": len(self.primary_records),
            "primary_records_offset": self.primary_records_offset,
            "primary_sentinel_offset": self.primary_sentinel_offset,
            "index_table_offset": self.index_table_offset,
            "index_table_max": self.index_table_max,
            "secondary_record_count": len(self.secondary_records),
            "secondary_records_offset": self.secondary_records_offset,
            "secondary_sentinel_offset": self.secondary_sentinel_offset,
            "parsed_prefix_end": self.parsed_prefix_end,
            "unparsed_byte_count": len(self.data) - self.parsed_prefix_end,
            "final_dword": self.final_dword,
        }


class _Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.size = len(data)
        if self.size < 4:
            raise DatFormatError("file is shorter than four bytes")

    def require(self, offset: int, size: int, description: str) -> None:
        if offset < 0 or size < 0 or offset > self.size or size > self.size - offset:
            raise DatFormatError(
                f"{description} at 0x{offset:x} needs {size} bytes; file size is {self.size}"
            )

    def i16(self, offset: int, description: str) -> int:
        self.require(offset, 2, description)
        return struct.unpack_from("<h", self.data, offset)[0]

    def u16(self, offset: int, description: str) -> int:
        self.require(offset, 2, description)
        return struct.unpack_from("<H", self.data, offset)[0]

    def u32(self, offset: int, description: str) -> int:
        self.require(offset, 4, description)
        return struct.unpack_from("<I", self.data, offset)[0]

    def i32(self, offset: int, description: str) -> int:
        self.require(offset, 4, description)
        return struct.unpack_from("<i", self.data, offset)[0]


def _read_scene_records(
    reader: _Reader, offset: int, label: str
) -> tuple[tuple[SceneRecord, ...], int]:
    records: list[SceneRecord] = []
    cursor = offset
    while True:
        reader.require(cursor, SCENE_RECORD_SIZE, f"{label} scene record or sentinel")
        if reader.i16(cursor + 14, f"{label} scene-record flags") < 0:
            return tuple(records), cursor
        records.append(
            SceneRecord(
                index=len(records),
                offset=cursor,
                center_component_00=reader.i32(
                    cursor, f"{label} scene-record center component +0x00"
                ),
                center_component_04=reader.i32(
                    cursor + 4, f"{label} scene-record center component +0x04"
                ),
                center_component_08=reader.i32(
                    cursor + 8, f"{label} scene-record center component +0x08"
                ),
                field_0c_signed=reader.i16(
                    cursor + 12, f"{label} scene-record field +0x0c"
                ),
                flags=reader.u16(cursor + 14, f"{label} scene-record flags"),
                payload_offset_candidate=reader.i32(
                    cursor + 16, f"{label} scene-record payload-offset candidate"
                ),
            )
        )
        cursor += SCENE_RECORD_SIZE


def _align_up(value: int, alignment: int) -> int:
    return (value + alignment - 1) // alignment * alignment
