"""Lossless inspector for the PC .ANM layout.

Field names remain offset-based where the original executable's semantics are
unknown. ``AnmFile.parse`` mirrors only the first-level reads demonstrated at PC
address 0x00444B70. ``AnmFile.records`` adds the per-slot record reads of the
pose sampler 0x00445FF0 (see Vault ``PC Flik animation catalog``). Both add
explicit file-size checks that the original routines do not receive.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import struct


ANM_HEADER_SIZE = 8
ANM_OFFSET_SIZE = 4
ANM_REFERENCED_HEADER_SIZE = 12

# Part-list values 0x00445FF0 treats specially; any other value is a word
# offset into one frame.
ANM_PART_SKIP_VALUES = (-1, -2)  # skipped; no destination entry consumed
ANM_PART_INHERIT = -3  # skipped; destination entry consumed (left as posed)
ANM_PART_BASE_WORDS = 6  # three linear words, then three 12-bit angles
ANM_PART_EXTRA_WORDS = 3  # three more linear words when the mask bit is set
ANM_FRAME_COUNT_MASK = 0x7FFF


class AnmFormatError(ValueError):
    """Raised when bytes cannot satisfy the bounded PC .ANM layout."""


@dataclass(frozen=True)
class AnmOffsetReference:
    """One file-relative dword from the first-level offset table."""

    index: int
    field_offset: int
    relative_offset: int | None


@dataclass(frozen=True)
class AnmFirstReferencedRecord:
    """The only referenced record inspected further by 0x00444B70."""

    offset: int
    item_count: int
    items_offset: int
    items_end_offset: int
    minus_two_indices: tuple[int, ...]


@dataclass(frozen=True)
class AnmPartPose:
    """One part's words in one frame, split the way 0x00445FF0 consumes them."""

    linear: tuple[int, int, int]
    angles: tuple[int, int, int]
    extra: tuple[int, int, int] | None


@dataclass(frozen=True)
class AnmRecord:
    """One slot's record as read by pose sampler 0x00445FF0.

    ``field_00`` is not read by the sampler; across the retail corpus it equals
    the slot index. ``frame_word`` bit 0x8000 selects a sampler branch that no
    retail record uses.
    """

    data: bytes
    slot: int
    offset: int
    field_00: int
    frame_word: int
    part_count: int
    words_per_frame: int
    list_count: int
    mask_length: int
    part_offsets: tuple[int, ...]
    mask: bytes
    frames_offset: int
    trailing_bytes: int

    @property
    def frame_count(self) -> int:
        return self.frame_word & ANM_FRAME_COUNT_MASK

    @property
    def flag_8000(self) -> bool:
        return bool(self.frame_word & 0x8000)

    @property
    def frames_end_offset(self) -> int:
        return self.frames_offset + self.frame_count * self.words_per_frame * 2

    def part_has_extra(self, part: int) -> bool:
        return bool(self.mask[part >> 3] >> (part & 7) & 1)

    def part_width(self, part: int) -> int:
        return ANM_PART_BASE_WORDS + (
            ANM_PART_EXTRA_WORDS if self.part_has_extra(part) else 0
        )

    @property
    def driven_parts(self) -> tuple[int, ...]:
        return tuple(p for p, v in enumerate(self.part_offsets) if v >= 0)

    @property
    def inherited_parts(self) -> tuple[int, ...]:
        return tuple(
            p for p, v in enumerate(self.part_offsets) if v == ANM_PART_INHERIT
        )

    @property
    def skipped_parts(self) -> tuple[int, ...]:
        return tuple(
            p for p, v in enumerate(self.part_offsets) if v in ANM_PART_SKIP_VALUES
        )

    def frame_words(self, frame: int) -> tuple[int, ...]:
        if not 0 <= frame < self.frame_count:
            raise AnmFormatError(
                f"slot {self.slot} frame {frame} outside 0..{self.frame_count - 1}"
            )
        start = self.frames_offset + frame * self.words_per_frame * 2
        return struct.unpack_from(f"<{self.words_per_frame}h", self.data, start)

    def part_pose(self, frame: int, part: int) -> AnmPartPose | None:
        """Return ``part``'s words in ``frame``, or None when it is not driven."""
        if not 0 <= part < self.part_count:
            raise AnmFormatError(f"slot {self.slot} part {part} outside record")
        offset = self.part_offsets[part]
        if offset < 0:
            return None
        words = self.frame_words(frame)[offset : offset + self.part_width(part)]
        return AnmPartPose(
            linear=tuple(words[0:3]),
            angles=tuple(words[3:6]),
            extra=tuple(words[6:9]) if self.part_has_extra(part) else None,
        )

    @classmethod
    def parse(
        cls, data: bytes, slot: int, offset: int, limit: int
    ) -> "AnmRecord":
        """Parse the record at ``offset``; it must end at or before ``limit``.

        ``limit`` is the next record's offset or the file size. The original
        sampler has no record bound; this parser rejects any record whose
        reads would leave ``[offset, limit)``.
        """
        reader = _Reader(data[:limit])
        label = f"slot {slot} record"
        reader.require(offset, ANM_REFERENCED_HEADER_SIZE, f"{label} header")
        field_00, frame_word, part_count, words_per_frame, list_count, mask_length = (
            struct.unpack_from("<6H", data, offset)
        )
        if part_count > list_count:
            raise AnmFormatError(
                f"{label} part count {part_count} exceeds its list count {list_count}"
            )
        if mask_length * 8 < part_count:
            raise AnmFormatError(
                f"{label} mask of {mask_length} bytes cannot cover {part_count} parts"
            )
        list_offset = offset + ANM_REFERENCED_HEADER_SIZE
        reader.require(list_offset, list_count * 2, f"{label} part list")
        part_offsets = struct.unpack_from(f"<{list_count}h", data, list_offset)
        mask_offset = list_offset + list_count * 2
        reader.require(mask_offset, mask_length, f"{label} part mask")
        mask = data[mask_offset : mask_offset + mask_length]
        frames_offset = mask_offset + mask_length
        frame_count = frame_word & ANM_FRAME_COUNT_MASK
        frames_size = frame_count * words_per_frame * 2
        reader.require(frames_offset, frames_size, f"{label} frame data")

        record = cls(
            data=data,
            slot=slot,
            offset=offset,
            field_00=field_00,
            frame_word=frame_word,
            part_count=part_count,
            words_per_frame=words_per_frame,
            list_count=list_count,
            mask_length=mask_length,
            part_offsets=part_offsets[:part_count],
            mask=mask,
            frames_offset=frames_offset,
            trailing_bytes=limit - (frames_offset + frames_size),
        )
        for part, value in enumerate(record.part_offsets):
            if value < 0:
                if value not in ANM_PART_SKIP_VALUES and value != ANM_PART_INHERIT:
                    raise AnmFormatError(
                        f"{label} part {part} has unknown negative value {value}"
                    )
            elif value + record.part_width(part) > words_per_frame:
                raise AnmFormatError(
                    f"{label} part {part} words {value}+{record.part_width(part)} "
                    f"exceed the {words_per_frame}-word frame"
                )
        return record


@dataclass(frozen=True)
class AnmFile:
    """Parsed first-level offsets plus the complete, unchanged source bytes."""

    data: bytes
    field_00: int
    offset_count: int
    field_04: int
    field_06: int
    offset_references: tuple[AnmOffsetReference, ...]
    first_referenced_record: AnmFirstReferencedRecord | None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()

    @property
    def offset_table_end(self) -> int:
        return ANM_HEADER_SIZE + self.offset_count * ANM_OFFSET_SIZE

    @classmethod
    def from_path(cls, path: Path | str) -> "AnmFile":
        return cls.parse(Path(path).read_bytes())

    @classmethod
    def parse(cls, data: bytes) -> "AnmFile":
        reader = _Reader(data)
        reader.require(0, ANM_HEADER_SIZE, "ANM header")

        field_00 = reader.u16(0, "field +0x00")
        offset_count = reader.i16(2, "offset count at +0x02")
        field_04 = reader.u16(4, "field +0x04")
        field_06 = reader.u16(6, "field +0x06")
        if offset_count < 0:
            raise AnmFormatError(f"negative offset count: {offset_count}")
        if offset_count > (reader.size - ANM_HEADER_SIZE) // ANM_OFFSET_SIZE:
            raise AnmFormatError(
                f"impossible offset count {offset_count} for file size "
                f"0x{reader.size:x}"
            )

        references: list[AnmOffsetReference] = []
        first_nonzero: int | None = None
        for index in range(offset_count):
            field_offset = ANM_HEADER_SIZE + index * ANM_OFFSET_SIZE
            relative_offset = reader.u32(
                field_offset, f"offset-table entry {index}"
            )
            if relative_offset == 0:
                references.append(AnmOffsetReference(index, field_offset, None))
                continue
            if relative_offset >= reader.size:
                raise AnmFormatError(
                    f"offset-table entry {index} value 0x{relative_offset:x} "
                    f"is outside file size 0x{reader.size:x}"
                )
            references.append(
                AnmOffsetReference(index, field_offset, relative_offset)
            )
            if first_nonzero is None:
                first_nonzero = relative_offset

        first_record = None
        if first_nonzero is not None:
            reader.require(
                first_nonzero,
                ANM_REFERENCED_HEADER_SIZE,
                "first referenced record header",
            )
            item_count = reader.u16(
                first_nonzero + 8, "first referenced record item count at +0x08"
            )
            items_offset = first_nonzero + ANM_REFERENCED_HEADER_SIZE
            if item_count > (reader.size - items_offset) // 2:
                raise AnmFormatError(
                    f"impossible first referenced record item count {item_count} "
                    f"at 0x{first_nonzero + 8:x}"
                )
            items_end_offset = items_offset + item_count * 2
            minus_two_indices = tuple(
                index
                for index in range(item_count)
                if reader.i16(
                    items_offset + index * 2,
                    f"first referenced record item {index}",
                )
                == -2
            )
            first_record = AnmFirstReferencedRecord(
                offset=first_nonzero,
                item_count=item_count,
                items_offset=items_offset,
                items_end_offset=items_end_offset,
                minus_two_indices=minus_two_indices,
            )

        return cls(
            data=data,
            field_00=field_00,
            offset_count=offset_count,
            field_04=field_04,
            field_06=field_06,
            offset_references=tuple(references),
            first_referenced_record=first_record,
        )

    def records(self) -> tuple[AnmRecord | None, ...]:
        """Parse every slot's record; absent (zero) slots are None.

        Each record is bounded by the next-higher record offset or the file
        end, so overlapping records are rejected rather than reinterpreted.
        """
        starts = sorted(
            {r.relative_offset for r in self.offset_references if r.relative_offset}
        )
        if starts and starts[0] < self.offset_table_end:
            raise AnmFormatError(
                f"record offset 0x{starts[0]:x} lies inside the offset table"
            )
        limits = dict(zip(starts, starts[1:] + [len(self.data)]))
        return tuple(
            None
            if r.relative_offset is None
            else AnmRecord.parse(
                self.data, r.index, r.relative_offset, limits[r.relative_offset]
            )
            for r in self.offset_references
        )

    def summary(self) -> dict[str, object]:
        first = self.first_referenced_record
        return {
            "sha256": self.sha256,
            "file_size": len(self.data),
            "field_00": self.field_00,
            "offset_count": self.offset_count,
            "field_04": self.field_04,
            "field_06": self.field_06,
            "offset_table_offset": ANM_HEADER_SIZE,
            "offset_table_end": self.offset_table_end,
            "offset_references": [
                {
                    "index": reference.index,
                    "field_offset": reference.field_offset,
                    "relative_offset": reference.relative_offset,
                }
                for reference in self.offset_references
            ],
            "first_referenced_record": (
                None
                if first is None
                else {
                    "offset": first.offset,
                    "item_count": first.item_count,
                    "items_offset": first.items_offset,
                    "items_end_offset": first.items_end_offset,
                    "minus_two_indices": list(first.minus_two_indices),
                }
            ),
        }


class _Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.size = len(data)

    def require(self, offset: int, size: int, label: str) -> None:
        if offset < 0 or size < 0 or offset > self.size - size:
            raise AnmFormatError(
                f"{label} at 0x{offset:x} needs {size} bytes; "
                f"file size is 0x{self.size:x}"
            )

    def u16(self, offset: int, label: str) -> int:
        self.require(offset, 2, label)
        return struct.unpack_from("<H", self.data, offset)[0]

    def i16(self, offset: int, label: str) -> int:
        self.require(offset, 2, label)
        return struct.unpack_from("<h", self.data, offset)[0]

    def u32(self, offset: int, label: str) -> int:
        self.require(offset, 4, label)
        return struct.unpack_from("<I", self.data, offset)[0]
