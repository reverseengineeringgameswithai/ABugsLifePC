"""Engine-exact PC type-1 reset-placement resolver.

Reimplements, bit-exactly at the documented boundary, the exact retail
executable's reset-coordinate selector:

- the loader's type-indexed pointer table (``0x0044BB70``): a nonnegative
  top-record type writes ``0x005C5860 + type * 4`` at ``0x0044BCA9``, a
  negative type writes ``0x005C5860 - type * 4`` at ``0x0044BC8B-0x0044BC95``
  (so type ``-N`` aliases into slot ``+N``), and a later record of the same
  slot overwrites an earlier one.  Type 1 is slot ``0x005C5864``;
- the nearest-row scan (``0x00432930``, byte-identical variant
  ``0x00437A20``): gated on bit ``0x10`` of ``0x0059D9A0``, it reads the
  unsigned row count from ``word [record]``, reduces the query X/Z from the
  auxiliary/reset globals ``0x0059D960``/``0x0059D968`` with ``sar 5``,
  and compares ``((qx >> 5) - row_x) >> 3`` and ``((qz >> 5) - row_z) >> 3``
  squared and summed as wrapping signed 32-bit values, keeping a strictly
  smaller value (``cmp``/``jge`` at ``0x0043299A``), so the lowest index
  wins a tie;
- the placement write: selected row X and Z shifted left by five into
  ``0x0059D960``/``0x0059D968`` (``0x004329C6``/``0x004329E0``), the query Y
  set to sentinel ``0x7FFFFFFF`` (``0x004329D6``), the terrain height query
  through thunk ``0x00401659 -> 0x004AC460``, and finally
  ``aux_y = returned - 0x100`` (``0x004329F1``).

The height half is supplied by :mod:`ablpc.terrain_height` (EXP-20260816-141,
independently accepted in EXP-20260816-142); this module owns only the row
selection, the scaling, and the failure relation.  On a failed height query
``0x004ACDB2`` writes ``0x80000000`` into the query block and ``0x004AC6B8``
returns it, so the engine stores ``0x7FFFFF00``; :data:`HEIGHT_FAILURE_REST_Y`
models that exactly.

Two behaviours of the original are deliberately *not* reproduced:

- with a zero row count the original skips the loop (``0x0043295C``) and
  still reads its uninitialised best-index local ``[esp+0x18]``
  (``0x004329B0``), then indexes the record with that garbage value.  This
  module refuses instead of emulating undefined behaviour;
- the original reads the count as an unsigned word, so a raw count with the
  high bit set would mean up to 65535 rows.  :class:`~ablpc.level_dat.LevelDat`
  refuses such a file at parse time, so the divergence is unreachable here
  and is reported rather than silently reconciled.

The confirmed reset role is bounded to Level03/Tunnels (EXP-20260815-116,
EXP-20260815-117, EXP-20260815-129, EXP-20260815-131).  Type 1 has several
other PC consumers (``0x004317D0``, ``0x004323A8``, ``0x004369B0``,
``0x0043CE60``), so this module models one selector and does not name the
table a checkpoint or respawn table.

Evidence: EXP-20260816-153.
"""

from __future__ import annotations

from dataclasses import dataclass
import struct

from .level_dat import LevelDat, TopRecord
from .terrain_height import HeightResult, TerrainHeightModel

# Executable anchors (retail SHA-256 97c95ba5...a27b878).
POINTER_TABLE_ROOT = 0x005C5860
TYPE1_POINTER_SLOT = 0x005C5864
SELECTOR_ADDRESSES = (0x00432930, 0x00437A20)
STATE_WORD_ADDRESS = 0x0059D9A0
RESET_REQUEST_BIT = 0x10
AUX_X_ADDRESS = 0x0059D960
AUX_Y_ADDRESS = 0x0059D964
AUX_Z_ADDRESS = 0x0059D968

TYPE_ID = 1
ROW_STRIDE = 12
ROWS_OFFSET = 4
QUERY_SHIFT = 5
DISTANCE_SHIFT = 3
PLACEMENT_SHIFT = 5
INITIAL_BEST_DISTANCE = 0x7FFFFFFF
QUERY_SENTINEL_Y = 0x7FFFFFFF
REST_Y_OFFSET = 0x100
#: ``0x004ACDB2`` stores this in the query block when no plane is found.
HEIGHT_FAILURE_SENTINEL = -0x80000000


class Type1ResetError(ValueError):
    """Raised when the bounded type-1 reset contract cannot be modelled."""


def _i32(value: int) -> int:
    return (value + 0x80000000) % 0x100000000 - 0x80000000


#: What ``0x004329F1`` stores after a failed query: ``0x7FFFFF00``.
HEIGHT_FAILURE_REST_Y = _i32(HEIGHT_FAILURE_SENTINEL - REST_Y_OFFSET)


def _imul32(left: int, right: int) -> int:
    """32-bit ``imul``: the low half, interpreted signed."""

    return _i32(left * right)


@dataclass(frozen=True)
class Type1Row:
    """One 12-byte signed coordinate row.

    ``middle`` is the row's second dword.  This selector never reads it
    (``0x0043297D`` uses ``[edx-8]`` and ``0x00432984`` uses ``[edx]``), so
    it is preserved and reported rather than named.
    """

    index: int
    offset: int
    x: int
    middle: int
    z: int

    @property
    def placement_x(self) -> int:
        """``shl edx, 5`` at ``0x004329C6``."""

        return _i32(self.x << PLACEMENT_SHIFT)

    @property
    def placement_z(self) -> int:
        """``shl ecx, 5`` at ``0x004329E0``."""

        return _i32(self.z << PLACEMENT_SHIFT)


@dataclass(frozen=True)
class Type1Table:
    """The rows the engine's ``0x005C5864`` slot points at."""

    record_index: int
    offset: int
    count: int
    rows: tuple[Type1Row, ...]
    aliased_records: tuple[int, ...]

    def row(self, index: int) -> Type1Row:
        if index < 0 or index >= len(self.rows):
            raise Type1ResetError(
                f"type-1 row index {index} is outside 0..{len(self.rows) - 1}"
            )
        return self.rows[index]


@dataclass(frozen=True)
class RowSelection:
    """Outcome of the ``0x0043297D-0x004329AE`` scan."""

    index: int
    distance: int
    row: Type1Row
    tied_indices: tuple[int, ...]
    overflowed: bool

    @property
    def tied(self) -> bool:
        return bool(self.tied_indices)


@dataclass(frozen=True)
class ResetPlacement:
    """The complete triple the selector writes to ``0x0059D960``."""

    selection: RowSelection
    x: int
    y: int
    z: int
    height: int | None
    height_kind: str | None
    descriptor_index: int | None
    height_failed: bool
    height_ambiguous: bool

    @property
    def position(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)


def pointer_table_slot(type_id: int) -> int:
    """Address ``0x0044BB70`` writes for a top record of ``type_id``.

    ``0x0044BCA9`` for a nonnegative type, ``0x0044BC8B-0x0044BC95`` for a
    negative one; the negative form subtracts a negative product and so
    aliases type ``-N`` into slot ``+N``.
    """

    if type_id < 0:
        return POINTER_TABLE_ROOT - _i32(type_id * 4)
    return POINTER_TABLE_ROOT + type_id * 4


def engine_type1_record(dat: LevelDat) -> TopRecord:
    """The top record whose address ends up in ``0x005C5864``.

    Later records overwrite earlier ones, so the *last* record claiming the
    slot wins.  A winning negative-type record is refused: the loader stores
    it, but its element layout is the 6-byte/``0x10``-header form while this
    selector would read 12-byte rows from ``+4``.
    """

    claimants = [
        record
        for record in dat.top_records
        if pointer_table_slot(record.type_id) == TYPE1_POINTER_SLOT
    ]
    if not claimants:
        raise Type1ResetError(
            "no top record claims the type-1 pointer slot 0x005C5864, so the "
            "loader never writes it for this level; what the live slot then "
            "holds is unresolved (KU-064) and cannot be modelled"
        )
    winner = claimants[-1]
    if winner.type_id < 0:
        raise Type1ResetError(
            f"top record {winner.index} has type {winner.type_id} and aliases "
            "into slot 0x005C5864; its element layout is not the 12-byte row "
            "form this selector reads"
        )
    return winner


def read_type1_table(dat: LevelDat) -> Type1Table:
    """Bounds-checked rows for the engine-selected type-1 record."""

    record = engine_type1_record(dat)
    aliased = tuple(
        other.index
        for other in dat.top_records
        if pointer_table_slot(other.type_id) == TYPE1_POINTER_SLOT
        and other.index != record.index
    )

    if record.offset + 4 > len(dat.data):
        raise Type1ResetError("type-1 record header is outside the file")
    raw_count = struct.unpack_from("<H", dat.data, record.offset)[0]
    if raw_count != record.count:
        raise Type1ResetError(
            f"type-1 raw count word {raw_count} disagrees with the parsed "
            f"count {record.count}; the engine reads the unsigned word"
        )
    if raw_count == 0:
        raise Type1ResetError(
            "type-1 row count is zero; the original skips its scan at "
            "0x0043295C and then indexes the record with the uninitialised "
            "best-index local read at 0x004329B0, which is undefined"
        )

    rows_end = record.offset + ROWS_OFFSET + raw_count * ROW_STRIDE
    if rows_end > len(dat.data):
        raise Type1ResetError(
            f"type-1 rows end at 0x{rows_end:x}, beyond the {len(dat.data)}-byte file"
        )

    rows = []
    for index in range(raw_count):
        offset = record.offset + ROWS_OFFSET + index * ROW_STRIDE
        x, middle, z = struct.unpack_from("<iii", dat.data, offset)
        rows.append(Type1Row(index=index, offset=offset, x=x, middle=middle, z=z))
    return Type1Table(
        record_index=record.index,
        offset=record.offset,
        count=raw_count,
        rows=tuple(rows),
        aliased_records=aliased,
    )


def _row_deltas(row: Type1Row, query_x: int, query_z: int) -> tuple[int, int]:
    """``sar 5`` on the query, subtract the row, then ``sar 3`` on each."""

    dx = _i32(_i32(_i32(query_x) >> QUERY_SHIFT) - row.x) >> DISTANCE_SHIFT
    dz = _i32(_i32(_i32(query_z) >> QUERY_SHIFT) - row.z) >> DISTANCE_SHIFT
    return dx, dz


def row_distance(row: Type1Row, query_x: int, query_z: int) -> int:
    """One iteration of the scan body, exactly ``0x0043297D-0x00432998``."""

    dx, dz = _row_deltas(row, query_x, query_z)
    return _i32(_imul32(dx, dx) + _imul32(dz, dz))


def row_distance_wraps(row: Type1Row, query_x: int, query_z: int) -> bool:
    """Whether the 32-bit result differs from the mathematical one.

    The original has no overflow check, so a wrapped value competes on equal
    terms and can win.  Reporting it lets a caller distinguish a genuinely
    near row from an arithmetic artefact.
    """

    dx, dz = _row_deltas(row, query_x, query_z)
    return dx * dx + dz * dz != row_distance(row, query_x, query_z)


def select_row(table: Type1Table, query_x: int, query_z: int) -> RowSelection:
    """Engine-exact nearest-row scan.

    The comparison at ``0x0043299A`` keeps a strictly smaller distance, so
    the lowest index wins a tie; ties that lost are reported.  Squares and
    their sum wrap at 32 bits and are compared signed, so an extreme query
    can select a far row — that is reproduced, not corrected.
    """

    if not table.rows:
        raise Type1ResetError("type-1 table has no rows")

    best = INITIAL_BEST_DISTANCE
    best_index: int | None = None
    tied: list[int] = []
    overflowed = False
    for row in table.rows:
        distance = row_distance(row, query_x, query_z)
        if row_distance_wraps(row, query_x, query_z):
            overflowed = True
        if distance < best:
            best = distance
            best_index = row.index
            tied = []
        elif distance == best and best_index is not None:
            tied.append(row.index)

    if best_index is None:  # pragma: no cover - unreachable, see below
        # Defensive only.  Two squares sum to 0, 1 or 2 modulo 4, and 32-bit
        # truncation preserves that residue, so no distance can equal the
        # 0x7FFFFFFF seed (3 modulo 4) and nothing can exceed it.  A
        # non-empty table therefore always selects a row.
        raise Type1ResetError(
            "no row scored below the initial 0x7FFFFFFF best distance "
            "(0x00432953); the original would use an uninitialised index"
        )
    return RowSelection(
        index=best_index,
        distance=best,
        row=table.row(best_index),
        tied_indices=tuple(tied),
        overflowed=overflowed,
    )


def placement_for_row(
    row: Type1Row, height_model: TerrainHeightModel | None
) -> tuple[int, int, int, HeightResult | None]:
    """Scaled X/Z plus the reset Y the selector would store.

    ``height_model`` may be ``None`` to model a level whose terrain source
    is unavailable; the failure relation is the same one the engine takes
    when the query returns its ``0x80000000`` sentinel.
    """

    x = row.placement_x
    z = row.placement_z
    if height_model is None:
        return x, HEIGHT_FAILURE_REST_Y, z, None
    result = height_model.query(x, z, QUERY_SENTINEL_Y)
    if result is None:
        return x, HEIGHT_FAILURE_REST_Y, z, None
    return x, result.rest_y, z, result


def resolve(
    table: Type1Table,
    height_model: TerrainHeightModel | None,
    query_x: int,
    query_z: int,
) -> ResetPlacement:
    """Complete selector result for one query position.

    ``query_x``/``query_z`` are the auxiliary/reset globals the scan reads
    (``0x0059D960``/``0x0059D968``), not the live position triple at
    ``0x0059D910`` (EXP-20260815-128).
    """

    selection = select_row(table, query_x, query_z)
    x, y, z, result = placement_for_row(selection.row, height_model)
    return ResetPlacement(
        selection=selection,
        x=x,
        y=y,
        z=z,
        height=None if result is None else result.height,
        height_kind=None if result is None else result.kind,
        descriptor_index=None if result is None else result.descriptor_index,
        height_failed=result is None,
        height_ambiguous=False if result is None else result.ambiguous,
    )


def row_placements(
    table: Type1Table, height_model: TerrainHeightModel | None
) -> tuple[ResetPlacement, ...]:
    """Where each row would place the actor if it were selected.

    ``placement.height_failed`` marks a row whose scaled point has no
    terrain surface below it: the engine would store ``0x7FFFFF00`` as the
    actor Y there.  That is an authoring hazard, not engine intent.
    """

    return tuple(
        _placement(row, *placement_for_row(row, height_model))
        for row in table.rows
    )


def shadowed_rows(table: Type1Table) -> tuple[tuple[int, int], ...]:
    """``(shadowed_index, winner_index)`` for rows that can never be selected.

    The scan keeps a strictly smaller distance, so a row sharing its exact
    X and Z with a lower-index row is unreachable: every query scores both
    identically and the earlier index always wins.  This is an exact
    consequence of ``0x0043299A``, not a heuristic.

    Unreachable *for this selector* is not the same as unused.  Four retail
    files contain such rows, and in Level04's ``LEVEL1.DAT``/``LEVEL4.DAT``
    they mirror around one pivot into an out-and-back sequence — a shape
    that fits the index-ordered type-1 consumers (``0x004369B0``) rather
    than this one (EXP-20260816-153).
    """

    first_seen: dict[tuple[int, int], int] = {}
    shadowed: list[tuple[int, int]] = []
    for row in table.rows:
        key = (row.x, row.z)
        if key in first_seen:
            shadowed.append((row.index, first_seen[key]))
        else:
            first_seen[key] = row.index
    return tuple(shadowed)


def _placement(
    row: Type1Row, x: int, y: int, z: int, result: HeightResult | None
) -> ResetPlacement:
    selection = RowSelection(
        index=row.index,
        distance=row_distance(row, x, z),
        row=row,
        tied_indices=(),
        overflowed=False,
    )
    return ResetPlacement(
        selection=selection,
        x=x,
        y=y,
        z=z,
        height=None if result is None else result.height,
        height_kind=None if result is None else result.kind,
        descriptor_index=None if result is None else result.descriptor_index,
        height_failed=result is None,
        height_ambiguous=False if result is None else result.ambiguous,
    )


def summary(table: Type1Table) -> dict[str, object]:
    """Deterministic, asset-free description of one table."""

    return {
        "record_index": table.record_index,
        "record_offset": table.offset,
        "row_count": table.count,
        "rows_offset": table.offset + ROWS_OFFSET,
        "aliased_records": list(table.aliased_records),
        "rows": [
            {
                "index": row.index,
                "offset": row.offset,
                "x": row.x,
                "middle": row.middle,
                "z": row.z,
                "placement_x": row.placement_x,
                "placement_z": row.placement_z,
            }
            for row in table.rows
        ],
    }
