#!/usr/bin/env python3
"""Report engine-exact type-1 reset placements for one PC level.

Answers two authoring questions offline, without launching the game:

- ``--query X Z``: if the engine's reset selector runs with the auxiliary
  coordinates X/Z (``0x0059D960``/``0x0059D968``), which type-1 row does it
  choose and exactly where does it put the actor?
- default: for every row, where would that row place the actor, and which
  rows can never be selected at all?

Both use :mod:`ablpc.type1_reset` (the ``0x00432930`` selector) composed with
:mod:`ablpc.terrain_height` (the ``0x004AC460``/``0x004ACA60`` height query).
PC world Y grows downward, and the reported Y is the value the selector
*writes*; an actor then settles deeper. ``settled_y_estimate`` reports the
observed extremes over the cited receipts, 121-129 units
(EXP-20260815-129/137, EXP-20260816-141/142/156) — a range of five samples,
not a guarantee.

The confirmed reset role is bounded to Level03/Tunnels
(EXP-20260815-116/117/129/131).  Type 1 has other PC consumers, so a
placement reported for another level says what *this* selector would do if
it ran there, not that the level uses it.

Read-only: this tool opens the given files, writes nothing, and never
touches ``originals/``.  Output is deterministic JSON.

Evidence: EXP-20260816-153.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))

from ablpc.level_dat import LevelDat  # noqa: E402
from ablpc.terrain_height import TerrainHeightModel  # noqa: E402
from ablpc.type1_reset import (  # noqa: E402
    HEIGHT_FAILURE_REST_Y,
    Type1ResetError,
    read_type1_table,
    resolve,
    row_placements,
    shadowed_rows,
)

# Observed extremes across the accepted receipts, not a modelled quantity:
# EXP-20260815-129 +123, EXP-20260815-137 +121/+126, EXP-20260816-156
# control +123 and candidate +129.
SETTLE_LOW = 121
SETTLE_HIGH = 129


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _placement_row(index: int, placement) -> dict[str, object]:
    row = placement.selection.row
    return {
        "row_index": index,
        "row_offset": row.offset,
        "row": {"x": row.x, "middle": row.middle, "z": row.z},
        "reset_x": placement.x,
        "reset_y": placement.y,
        "reset_z": placement.z,
        "height_failed": placement.height_failed,
        "height_ambiguous": placement.height_ambiguous,
        "terrain_descriptor": placement.descriptor_index,
        "settled_y_estimate": (
            None
            if placement.height_failed
            else [placement.y + SETTLE_LOW, placement.y + SETTLE_HIGH]
        ),
    }


def build_report(
    level_path: Path, terrain_path: Path | None, query: tuple[int, int] | None
) -> dict[str, object]:
    dat = LevelDat.from_path(level_path)
    table = read_type1_table(dat)
    model = (
        None if terrain_path is None else TerrainHeightModel.from_path(terrain_path)
    )

    report: dict[str, object] = {
        "level_dat": {
            "path": str(level_path),
            "sha256": _sha256(level_path),
            "record_index": table.record_index,
            "record_offset": table.offset,
            "row_count": table.count,
        },
        "terrain": (
            None
            if terrain_path is None
            else {"path": str(terrain_path), "sha256": _sha256(terrain_path)}
        ),
        "height_failure_rest_y": HEIGHT_FAILURE_REST_Y,
        "unreachable_rows": [
            {"row_index": later, "shadowed_by": earlier}
            for later, earlier in shadowed_rows(table)
        ],
    }

    if query is not None:
        placement = resolve(table, model, query[0], query[1])
        report["query"] = {
            "aux_x": query[0],
            "aux_z": query[1],
            "selected_row": placement.selection.index,
            "distance": placement.selection.distance,
            "tied_rows": list(placement.selection.tied_indices),
            "distance_overflowed": placement.selection.overflowed,
            "placement": _placement_row(placement.selection.index, placement),
        }
    else:
        report["rows"] = [
            _placement_row(index, placement)
            for index, placement in enumerate(row_placements(table, model))
        ]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Engine-exact type-1 reset placements for one PC level"
    )
    parser.add_argument("level_dat", type=Path, help="path to a LEVEL*.DAT copy")
    parser.add_argument(
        "--terrain",
        type=Path,
        default=None,
        help="matching TERRAIN.ALL/TERR1.ALL copy; omit to report X/Z only",
    )
    parser.add_argument(
        "--query",
        type=int,
        nargs=2,
        metavar=("X", "Z"),
        default=None,
        help="auxiliary/reset X and Z to resolve instead of listing every row",
    )
    args = parser.parse_args(argv)

    query = None if args.query is None else (args.query[0], args.query[1])
    try:
        report = build_report(args.level_dat, args.terrain, query)
    except (Type1ResetError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
