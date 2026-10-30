"""Engine-faithful PC ``TERRAIN.ALL`` ground-height query.

Reimplements, bit-exactly at the documented boundary, the exact retail
executable's terrain height pipeline:

- runtime-descriptor construction from source records, including the clone
  branch (``0x004A8410``; clone copy at ``0x004A850A-0x004A857D``, template
  registration at ``0x004A85DF``);
- the cell-derived descriptor X/Z bounds recompute for tag-6/7/8
  descriptors (``0x004A8A1A-0x004A8B60``);
- the candidate cell collector (``0x004AC460``), iterating descriptors in
  index order instead of the runtime zone-bucket order.  Each descriptor
  belongs to exactly one zone; the bucket unions derive from group-header
  extents while the phase-2 boxes are cell-derived, and EXP-20260816-142's
  exhaustive scan of both modeled retail files shows no cell window
  protrudes below its group extent, so the accepted cell set is identical
  for these exact files; only tie ordering could differ, and height ties
  resolve to the same height (ambiguities are reported);
- the height resolver (``0x004ACA60``) with its exact plane formula,
  floor/ceiling selection, tie-breaks, and the ``+ 0xC80`` output offset;
- the half-plane edge test (``0x004A9290`` via thunk ``0x00401500``).

The reset consumer ``0x00432930`` derives the actor Y as ``result - 0x100``
(``0x004329F1``); :func:`rest_y` mirrors that relation.

All arithmetic wraps at 32 bits exactly as the x86 code does; ``idiv``
truncates toward zero; ``sar`` is an arithmetic shift.  This module models
only descriptors sourced from one ``TERRAIN.ALL``/``TERR1.ALL`` file.  The
live table may append a second source family (``plantter.all``); that
family is explicitly out of scope and results are terrain-surface heights.
The loader's ``+0x10 >= 0x100`` branch (``0x004A84EB``) appends no
descriptor, whereas this model builds a height-ineligible descriptor;
both modeled retail files carry such records only after every tag-6/7/8
record, so indices and query results are unchanged (EXP-20260816-142).

Evidence: EXP-20260816-141 (static extraction and receipts cross-check),
building on EXP-20260815-131 and [[PC TERRAIN ALL collision descriptor
source]].
"""

from __future__ import annotations

from dataclasses import dataclass
import struct

from .terrain_all import (
    CollisionPayload,
    TerrainAll,
    TerrainFormatError,
)

HEIGHT_TAGS = (6, 7, 8)
QUERY_SENTINEL_Y = 0x7FFFFFFF
RESULT_OFFSET = 0xC80
REST_Y_OFFSET = 0x100
_BOUNDS_MIN_INIT = 0x7FFFFFFF
_BOUNDS_MAX_INIT = -0x80000000


def _i32(value: int) -> int:
    return (value + 0x80000000) % 0x100000000 - 0x80000000


def _u32(value: int) -> int:
    return value % 0x100000000


def _idiv(numerator: int, denominator: int) -> int:
    """x86 ``idiv``: 32-bit operands, quotient truncated toward zero."""

    if denominator == 0:
        raise TerrainFormatError("cell divisor word is zero in a tested cell")
    quotient = abs(numerator) // abs(denominator)
    if (numerator < 0) != (denominator < 0):
        quotient = -quotient
    return quotient


def _trunc_div32(value: int) -> int:
    """``cdq; and edx, 0x1f; add eax, edx; sar eax, 5`` — /32 toward zero."""

    adjust = 0x1F if value < 0 else 0
    return _i32(value + adjust) >> 5


@dataclass(frozen=True)
class RuntimeDescriptor:
    """One ``0x30``-byte runtime descriptor rebuilt from file bytes."""

    index: int
    source_index: int
    clone_of: int | None
    base_x: int
    base_y: int
    base_z: int
    tag: int
    result: int
    payload_source_index: int | None
    x_min: int
    z_min: int
    x_span: int
    z_span: int
    height_eligible: bool


@dataclass(frozen=True)
class CellWords:
    """Signed views of one 0x20-byte collision cell used by the query."""

    slope_x: int  # +0x00, B
    divisor: int  # +0x02, C; sign selects winding
    slope_z: int  # +0x04, A
    x0: int  # +0x06
    h0: int  # +0x08
    z0: int  # +0x0A
    dx1: int  # +0x0C
    dz1: int  # +0x10
    dx2: int  # +0x12
    dz2: int  # +0x16
    box_x_min: int  # +0x18
    box_x_span: int  # +0x1A
    box_z_base: int  # byte +0x1E
    box_z_span: int  # byte +0x1F

    @classmethod
    def parse(cls, raw: bytes) -> "CellWords":
        if len(raw) != 0x20:
            raise TerrainFormatError(f"cell raw size {len(raw)} != 0x20")
        words = struct.unpack("<16h", raw)
        return cls(
            slope_x=words[0x00 // 2],
            divisor=words[0x02 // 2],
            slope_z=words[0x04 // 2],
            x0=words[0x06 // 2],
            h0=words[0x08 // 2],
            z0=words[0x0A // 2],
            dx1=words[0x0C // 2],
            dz1=words[0x10 // 2],
            dx2=words[0x12 // 2],
            dz2=words[0x16 // 2],
            box_x_min=words[0x18 // 2],
            box_x_span=words[0x1A // 2],
            box_z_base=struct.unpack_from("<b", raw, 0x1E)[0],
            box_z_span=struct.unpack_from("<b", raw, 0x1F)[0],
        )


@dataclass(frozen=True)
class HeightResult:
    """One resolved height query."""

    height: int  # selected plane height + 0xC80, exactly as returned live
    kind: str  # "floor" or "ceiling"
    plane_height: int
    descriptor_index: int
    cell_divisor: int
    matched_cells: int
    ambiguous: bool  # a distinct cell tied the winning plane height

    @property
    def rest_y(self) -> int:
        """Actor Y as the reset consumer derives it (``0x004329F1``)."""

        return _i32(self.height - REST_Y_OFFSET)


@dataclass(frozen=True)
class PlaneHit:
    """One triangle-containing cell with its engine-exact plane height.

    ``mode`` is the resolver's winding result (1 or 2); Y grows downward in
    PC world space, so a numerically smaller ``plane_height`` is physically
    higher.
    """

    plane_height: int
    mode: int
    divisor: int
    descriptor_index: int
    tag: int
    result: int
    clone_of: int | None

    @property
    def rest_y(self) -> int:
        """Reset-consumer actor Y if this plane were the selected floor."""

        return _i32(self.plane_height + RESULT_OFFSET - REST_Y_OFFSET)


class TerrainHeightModel:
    """Descriptor table plus height queries for one parsed terrain file."""

    def __init__(self, terrain: TerrainAll) -> None:
        self.terrain = terrain
        self.descriptors = _build_descriptors(terrain)
        self._payloads: dict[int, CollisionPayload] = {}
        self._cells: dict[int, tuple[tuple["CellWords", ...], ...]] = {}
        for descriptor in self.descriptors:
            if not descriptor.height_eligible:
                continue
            source = descriptor.payload_source_index
            if source is not None and source not in self._cells:
                payload = terrain.collision_payload(source)
                self._payloads[source] = payload
                self._cells[source] = tuple(
                    tuple(CellWords.parse(cell.raw) for cell in group.cells)
                    for group in payload.groups
                )

    @classmethod
    def from_path(cls, path) -> "TerrainHeightModel":
        return cls(TerrainAll.from_path(path))

    def _collect(
        self, x: int, z: int
    ) -> list[tuple[RuntimeDescriptor, CellWords]]:
        """Candidate cell collection, exactly ``0x004AC460``.

        Descriptors are visited in index order instead of the runtime
        zone-bucket order; see the module docstring for the equivalence
        argument.
        """

        x_biased = _i32(x + 0x1000)
        z_biased = _i32(z + 0x1000)
        collected: list[tuple[RuntimeDescriptor, CellWords]] = []
        for descriptor in self.descriptors:
            if not descriptor.height_eligible:
                continue
            if descriptor.tag == 0:
                continue
            if not _u32(x_biased - descriptor.x_min) < _u32(
                descriptor.x_span + 0x2000
            ):
                continue
            if not _u32(z_biased - descriptor.z_min) < _u32(
                descriptor.z_span + 0x2000
            ):
                continue
            source = descriptor.payload_source_index
            if source is None:
                continue
            payload = self._payloads[source]
            if not payload.groups:
                continue
            cell_x = _trunc_div32(_i32(x_biased - descriptor.base_x))
            cell_z = _trunc_div32(_i32(z_biased - descriptor.base_z))
            for group, cells in zip(
                payload.groups, self._cells[source], strict=True
            ):
                if not _u32(cell_x - group.minimum_x_units) < _u32(
                    group.span_x_units + 0x100
                ):
                    continue
                if not _u32(cell_z - group.minimum_z_units) < _u32(
                    group.span_z_units + 0x100
                ):
                    continue
                for cell in cells:
                    if not _u32(cell_x - cell.box_x_min) < _u32(
                        cell.box_x_span + 0x100
                    ):
                        continue
                    if not _u32(
                        cell_z - (cell.box_z_base << 6) - cell.z0
                    ) < _u32((cell.box_z_span + 4) << 6):
                        continue
                    collected.append((descriptor, cell))
        return collected

    def planes(self, x: int, z: int) -> tuple[PlaneHit, ...]:
        """Engine-exact plane heights of every triangle containing (x, z).

        Each hit's ``plane_height`` is exactly the resolver's per-cell value
        (``0x004ACC3E-0x004ACC7D``); the ordering is the collection order.
        """

        x = _i32(x)
        z = _i32(z)
        hits: list[PlaneHit] = []
        for descriptor, cell in self._collect(x, z):
            local_x = _i32(x - descriptor.base_x) >> 5
            local_z = _i32(z - descriptor.base_z) >> 5
            mode = _cell_mode(cell, local_x, local_z)
            if mode == 0:
                continue
            hits.append(
                PlaneHit(
                    plane_height=_plane_height(
                        descriptor, cell, local_x, local_z
                    ),
                    mode=mode,
                    divisor=cell.divisor,
                    descriptor_index=descriptor.index,
                    tag=descriptor.tag,
                    result=descriptor.result,
                    clone_of=descriptor.clone_of,
                )
            )
        return tuple(hits)

    def query(
        self, x: int, z: int, y: int = QUERY_SENTINEL_Y
    ) -> HeightResult | None:
        """Exact ``0x004AC460`` + ``0x004ACA60`` height query.

        Returns ``None`` where the live routine writes the ``0x80000000``
        failure sentinel into the query block.
        """

        x = _i32(x)
        z = _i32(z)
        y_adjusted = _i32(y - 0x600)
        collected = self._collect(x, z)

        floor_best: int | None = None
        floor_cell: CellWords | None = None
        floor_descriptor: RuntimeDescriptor | None = None
        floor_ambiguous = False
        ceiling_best: int | None = None
        ceiling_cell: CellWords | None = None
        ceiling_descriptor: RuntimeDescriptor | None = None
        ceiling_ambiguous = False

        for descriptor, cell in collected:
            local_x = _i32(x - descriptor.base_x) >> 5
            local_z = _i32(z - descriptor.base_z) >> 5
            mode = _cell_mode(cell, local_x, local_z)
            if mode == 0:
                continue
            height = _plane_height(descriptor, cell, local_x, local_z)
            if height < y_adjusted:
                if floor_best is None or height > floor_best:
                    floor_best = height
                    floor_cell = cell
                    floor_descriptor = descriptor
                    floor_ambiguous = False
                elif height == floor_best:
                    assert floor_cell is not None
                    floor_ambiguous = True
                    if cell.divisor > floor_cell.divisor:
                        floor_cell = cell
                        floor_descriptor = descriptor
            else:
                if mode == 1 and (
                    ceiling_best is None or height < ceiling_best
                ):
                    ceiling_best = height
                    ceiling_cell = cell
                    ceiling_descriptor = descriptor
                    ceiling_ambiguous = False
                elif mode == 1 and height == ceiling_best:
                    ceiling_ambiguous = True

        if (
            floor_best is not None
            and floor_cell is not None
            and floor_descriptor is not None
            and floor_cell.divisor < 0
        ):
            return HeightResult(
                height=_i32(floor_best + RESULT_OFFSET),
                kind="floor",
                plane_height=floor_best,
                descriptor_index=floor_descriptor.index,
                cell_divisor=floor_cell.divisor,
                matched_cells=len(collected),
                ambiguous=floor_ambiguous,
            )
        if ceiling_best is not None:
            assert ceiling_cell is not None and ceiling_descriptor is not None
            return HeightResult(
                height=_i32(ceiling_best + RESULT_OFFSET),
                kind="ceiling",
                plane_height=ceiling_best,
                descriptor_index=ceiling_descriptor.index,
                cell_divisor=ceiling_cell.divisor,
                matched_cells=len(collected),
                ambiguous=ceiling_ambiguous,
            )
        return None


def rest_y(height_result: HeightResult) -> int:
    return height_result.rest_y


def _build_descriptors(terrain: TerrainAll) -> tuple[RuntimeDescriptor, ...]:
    template_map: dict[int, int] = {}
    built: list[RuntimeDescriptor] = []
    for record in terrain.records:
        index = record.index
        if record.field_46 == 1:
            if record.field_44 not in template_map:
                raise TerrainFormatError(
                    f"clone record {index} references unregistered template "
                    f"id {record.field_44}"
                )
            reference = built[template_map[record.field_44]]
            base_x, base_y, base_z = record.world_base
            built.append(
                RuntimeDescriptor(
                    index=index,
                    source_index=index,
                    clone_of=reference.index,
                    base_x=_i32(base_x),
                    base_y=_i32(base_y),
                    base_z=_i32(base_z),
                    tag=reference.tag,
                    result=reference.result,
                    payload_source_index=reference.payload_source_index,
                    x_min=0,
                    z_min=0,
                    x_span=0,
                    z_span=0,
                    height_eligible=reference.tag in HEIGHT_TAGS,
                )
            )
            continue
        tag = struct.unpack_from("<h", record.raw, 0x10)[0]
        base_x, base_y, base_z = record.world_base
        built.append(
            RuntimeDescriptor(
                index=index,
                source_index=index,
                clone_of=None,
                base_x=_i32(base_x),
                base_y=_i32(base_y),
                base_z=_i32(base_z),
                tag=tag,
                result=record.result_word,
                payload_source_index=(
                    index if record.payload_word_count > 0 else None
                ),
                x_min=0,
                z_min=0,
                x_span=0,
                z_span=0,
                height_eligible=tag in HEIGHT_TAGS,
            )
        )
        if record.field_44 >= 0:
            template_map[record.field_44] = index

    return tuple(
        _recompute_bounds(terrain, descriptor) for descriptor in built
    )


def _recompute_bounds(
    terrain: TerrainAll, descriptor: RuntimeDescriptor
) -> RuntimeDescriptor:
    """Cell-derived bounds recompute, ``0x004A8A1A-0x004A8B60``."""

    if not descriptor.height_eligible:
        return descriptor
    x_min = _BOUNDS_MIN_INIT
    z_min = _BOUNDS_MIN_INIT
    x_max = _BOUNDS_MAX_INIT
    z_max = _BOUNDS_MAX_INIT
    source = descriptor.payload_source_index
    if source is not None:
        payload = terrain.collision_payload(source)
        for group in payload.groups:
            for raw_cell in group.cells:
                cell = CellWords.parse(raw_cell.raw)
                x_min = min(x_min, cell.box_x_min)
                x_max = max(x_max, _i32(cell.box_x_min + cell.box_x_span))
                z_min = min(z_min, _i32((cell.box_z_base << 6) + cell.z0))
                z_max = max(
                    z_max,
                    _i32(
                        (cell.box_z_span << 12)
                        + (cell.box_z_base << 6)
                        + cell.z0
                    ),
                )
    bound_x_min = _i32(descriptor.base_x + _i32(x_min << 5))
    bound_z_min = _i32(descriptor.base_z + _i32(z_min << 5))
    return RuntimeDescriptor(
        index=descriptor.index,
        source_index=descriptor.source_index,
        clone_of=descriptor.clone_of,
        base_x=descriptor.base_x,
        base_y=descriptor.base_y,
        base_z=descriptor.base_z,
        tag=descriptor.tag,
        result=descriptor.result,
        payload_source_index=descriptor.payload_source_index,
        x_min=bound_x_min,
        z_min=bound_z_min,
        x_span=_i32(_i32(x_max << 5) - bound_x_min + descriptor.base_x),
        z_span=_i32(_i32(z_max << 5) - bound_z_min + descriptor.base_z),
        height_eligible=True,
    )


def _plane_height(
    descriptor: RuntimeDescriptor, cell: CellWords, local_x: int, local_z: int
) -> int:
    """Per-cell plane height, exactly ``0x004ACC3E-0x004ACC7D``."""

    numerator = _i32(
        _i32(
            _i32(local_z - cell.z0) * cell.slope_z
            + _i32(local_x - cell.x0) * cell.slope_x
        )
        << 3
    )
    quotient = _idiv(numerator, cell.divisor)
    return _i32(descriptor.base_y + 4 * _i32((cell.h0 << 3) - quotient))


def _cell_mode(cell: CellWords, px: int, pz: int) -> int:
    """Triangle containment, ``0x004ACAEC-0x004ACC32``; 0 = outside."""

    x0, z0 = cell.x0, cell.z0
    x1, z1 = _i32(x0 + cell.dx1), _i32(z0 + cell.dz1)
    x2, z2 = _i32(x0 + cell.dx2), _i32(z0 + cell.dz2)
    if cell.divisor < 0:
        if (
            _edge_test(px, pz, x0, z0, x1, z1)
            and _edge_test(px, pz, x2, z2, x0, z0)
            and _edge_test(px, pz, x1, z1, x2, z2)
        ):
            return 1
        return 0
    if cell.divisor > 0:
        if (
            _edge_test(px, pz, x1, z1, x0, z0)
            and _edge_test(px, pz, x0, z0, x2, z2)
            and _edge_test(px, pz, x2, z2, x1, z1)
        ):
            return 2
        return 0
    return 0


def _edge_test(
    px: int, pz: int, x1: int, z1: int, x2: int, z2: int
) -> bool:
    """Half-plane side test, exactly ``0x004A9290``."""

    if z1 == z2:
        if x1 <= x2:
            return pz <= z1
        return pz >= z1
    if x1 == x2:
        if z1 <= z2:
            return px >= x1
        return px <= x1
    edge_dx = _i32(x1 - x2)
    edge_dz = _i32(z1 - z2)
    if abs(edge_dz) > abs(edge_dx):
        if z1 < z2:
            quotient = _idiv(
                _i32(_i32(x2 - x1) * _i32(pz - z1)), _i32(z2 - z1)
            )
            return _i32(px - x1) >= quotient
        quotient = _idiv(_i32(_i32(pz - z2) * edge_dx), edge_dz)
        return _i32(px - x2) <= quotient
    if x1 < x2:
        quotient = _idiv(
            _i32(_i32(px - x1) * _i32(z2 - z1)), _i32(x2 - x1)
        )
        return _i32(pz - z1) <= quotient
    quotient = _idiv(_i32(_i32(px - x2) * edge_dz), edge_dx)
    return _i32(pz - z2) >= quotient
