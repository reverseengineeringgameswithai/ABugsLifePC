#!/usr/bin/env python3
"""Compute candidate teleport standoff coordinates for the 12 grain gates.

For every Tunnels row (internal Level03) and City Entrance gate (internal
Level04) this tool evaluates a fixed ring of 16 integer directions around
the static trigger center (EXP-20260815-136/139) using the engine-exact
plane enumeration in ``reimplementation/ablpc/terrain_height.py``
(EXP-20260816-141).  PC world Y grows downward.

Plane heights are engine-exact; the *selection policy* below is a
documented tool-level heuristic, not engine behavior:

- reference ground = the deepest result-0 plane at the gate center (the
  gate stands on the reachable path, so its own ground defines the local
  walking level);
- a candidate's standing plane = the result-0 plane closest to that
  reference; candidates with no result-0 plane, with a non-zero-result
  plane at or above the standing plane (a reset surface Flik would touch
  first), or with four 512-unit probes deviating more than 512 units are
  rejected;
- surviving candidates rank by closeness to the reference, then flatness,
  then the fixed direction order.

Standoff distances:
- Tunnels rows: 16000 units — outside the 10240-unit insufficient-grain
  message radius, inside the 25600-unit open radius (with grain 0 nothing
  can open; EXP-137 viewed the row-3 gate from about 18000 units).
- City gates: effective trigger radius (radius parameter << 8) + 1500 —
  just outside the trigger, matching how the proven approach point frames
  gate 0 without triggering it.

Outputs deterministic JSON.  Coordinates are *candidates for the guarded
teleport procedure* ([[PC Flik teleport procedure]]): live write/readback,
survival, and fresh-state checks remain mandatory, and observed standing Y
settles deeper than the computed rest Y (numerically larger; PC world Y grows
downward) by 121-129 units — the observed extremes over five cited receipts
(EXP-20260815-129/137, EXP-20260816-141/156), not a guarantee.
This tool is read-only and refuses unpinned terrain files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reimplementation"))

from ablpc.terrain_height import TerrainHeightModel  # noqa: E402

TERRAIN_PATHS = {
    3: "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL03/TERRAIN.ALL",
    4: "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL04/TERRAIN.ALL",
}
TERRAIN_SHA256 = {
    3: "b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c",
    4: "9cf8fb6990a955a808f2e4f2c22ffce3fe5d62136f4a9271bdc444a6dd7fc103",
}

# EXP-20260815-136 resident Tunnels rows: (row, retail requirement, x, z).
TUNNELS_GATES = (
    (0, 20, 193754, 131692),
    (1, 10, 505642, -451306),
    (2, 10, 832302, 291075),
    (3, 10, 509676, 510143),
    (4, 20, 833246, 612273),
    (5, 20, 1142934, 1308289),
    (6, 30, 1471643, 1410369),
    (7, 10, 1202034, 1986285),
    (8, 30, 1634925, 2534812),
)
# EXP-20260815-139 City Entrance call-site immediates:
# (gate, retail requirement, x, z, radius parameter).
CITY_GATES = (
    (0, 10, -71129, -184314, 80),
    (1, 20, 354031, 35256, 90),
    (2, 30, 582271, 310212, 100),
)

TUNNELS_STANDOFF = 16000
CITY_STANDOFF_MARGIN = 1500
PROBE_STEP = 512
MAX_SPREAD = 512

# 16 fixed integer directions, counterclockwise from +X.
DIRECTIONS = (
    (1, 0), (2, 1), (1, 1), (1, 2),
    (0, 1), (-1, 2), (-1, 1), (-2, 1),
    (-1, 0), (-2, -1), (-1, -1), (-1, -2),
    (0, -1), (1, -2), (1, -1), (2, -1),
)

# Independently accepted runtime coordinates (EXP-130/137/138); preferred
# over any computed candidate where they exist.
PROVEN_POINTS = {
    ("T", 3): {
        "label": "accepted walkable point (EXP-130, EXP-137)",
        "x": 501696,
        "y": 30092,
        "z": 494016,
    },
    ("C", 0): {
        "label": "accepted trigger point (EXP-137)",
        "x": -87622,
        "y": 917,
        "z": -182181,
    },
}


def _direction_offset(direction: tuple[int, int], distance: int) -> tuple[int, int]:
    """Deterministic integer offset of ~``distance`` along ``direction``."""

    a, b = direction
    scale = 10**6
    norm = isqrt((a * a + b * b) * scale * scale)
    return (a * distance * scale) // norm, (b * distance * scale) // norm


def _walkable_planes(model: TerrainHeightModel, x: int, z: int):
    hits = model.planes(x, z)
    ground = [hit for hit in hits if hit.result == 0]
    special = [hit for hit in hits if hit.result != 0]
    return hits, ground, special


def _reference_ground(
    model: TerrainHeightModel, center_x: int, center_z: int
) -> int | None:
    """Deepest result-0 plane at the gate center (Y grows downward)."""

    _, ground, _ = _walkable_planes(model, center_x, center_z)
    if not ground:
        return None
    return max(hit.plane_height for hit in ground)


def _evaluate_candidate(
    model: TerrainHeightModel, x: int, z: int, reference: int | None
) -> dict[str, object]:
    hits, ground, special = _walkable_planes(model, x, z)
    entry: dict[str, object] = {
        "x": x,
        "z": z,
        "planes": [
            {
                "rest_y": hit.rest_y,
                "result": hit.result,
                "descriptor": hit.descriptor_index,
                "mode": hit.mode,
            }
            for hit in hits
        ],
        "rest_y": None,
        "distance_to_reference": None,
        "spread": None,
        "valid": False,
        "reject_reason": None,
    }
    if reference is None:
        entry["reject_reason"] = "no reference ground at gate center"
        return entry
    if not ground:
        entry["reject_reason"] = "no result-0 plane"
        return entry
    chosen = min(
        ground,
        key=lambda hit: (abs(hit.plane_height - reference), -hit.plane_height),
    )
    entry["rest_y"] = chosen.rest_y
    entry["distance_to_reference"] = abs(chosen.plane_height - reference)
    if any(hit.plane_height <= chosen.plane_height for hit in special):
        entry["reject_reason"] = "reset-result plane at or above standing plane"
        return entry
    probe_heights = [chosen.plane_height]
    for px, pz in (
        (x + PROBE_STEP, z),
        (x - PROBE_STEP, z),
        (x, z + PROBE_STEP),
        (x, z - PROBE_STEP),
    ):
        _, probe_ground, probe_special = _walkable_planes(model, px, pz)
        near = [
            hit.plane_height
            for hit in probe_ground
            if abs(hit.plane_height - chosen.plane_height) <= MAX_SPREAD
        ]
        if not near:
            entry["reject_reason"] = f"probe ({px},{pz}) has no nearby ground"
            return entry
        probe_height = min(
            near, key=lambda height: abs(height - chosen.plane_height)
        )
        if any(
            hit.plane_height <= probe_height for hit in probe_special
        ):
            entry["reject_reason"] = (
                f"probe ({px},{pz}) has a reset-result plane at or above ground"
            )
            return entry
        probe_heights.append(probe_height)
    entry["spread"] = max(probe_heights) - min(probe_heights)
    entry["valid"] = True
    return entry


def _gate_entry(
    model: TerrainHeightModel,
    kind: str,
    index: int,
    requirement: int,
    center_x: int,
    center_z: int,
    distance: int,
    radius_note: str,
) -> dict[str, object]:
    reference = _reference_ground(model, center_x, center_z)
    candidates = []
    for direction_index, direction in enumerate(DIRECTIONS):
        off_x, off_z = _direction_offset(direction, distance)
        entry = _evaluate_candidate(
            model, center_x + off_x, center_z + off_z, reference
        )
        entry["direction"] = list(direction)
        entry["direction_index"] = direction_index
        candidates.append(entry)
    valid = [c for c in candidates if c["valid"]]
    chosen = min(
        valid,
        key=lambda c: (
            c["distance_to_reference"],
            c["spread"],
            c["direction_index"],
        ),
        default=None,
    )
    gate: dict[str, object] = {
        "mechanism": f"{kind}{index}",
        "retail_requirement": requirement,
        "center": {"x": center_x, "z": center_z},
        "reference_rest_y": (
            None
            if reference is None
            else reference + 0xC80 - 0x100
        ),
        "standoff_distance": distance,
        "radius_note": radius_note,
        "valid_candidates": len(valid),
        "chosen": chosen,
        "candidates": candidates,
    }
    proven = PROVEN_POINTS.get((kind, index))
    if proven is not None:
        gate["proven_point"] = proven
    return gate


def build_report(repo_root: Path) -> dict[str, object]:
    report: dict[str, object] = {
        "tool": "grain-gate-standoffs",
        "evidence": [
            "EXP-20260815-129",
            "EXP-20260815-136",
            "EXP-20260815-137",
            "EXP-20260815-139",
            "EXP-20260816-141",
            "EXP-20260816-156",
        ],
        "rest_y_note": (
            "rest_y = engine height result - 0x100 (0x004329F1); observed "
            "standing Y settles 121-129 units deeper (PC Y grows downward) - "
            "the observed extremes over five cited receipts, not a guarantee"
        ),
        "levels": {},
    }
    models: dict[int, TerrainHeightModel] = {}
    for level, relative in TERRAIN_PATHS.items():
        path = repo_root / relative
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != TERRAIN_SHA256[level]:
            raise SystemExit(
                f"refusing unpinned terrain file for level {level}: "
                f"sha256 {digest}"
            )
        models[level] = TerrainHeightModel.from_path(path)

    tunnels = [
        _gate_entry(
            models[3],
            "T",
            row,
            requirement,
            x,
            z,
            TUNNELS_STANDOFF,
            "16000 < open radius ~25600, > message radius ~10240",
        )
        for row, requirement, x, z in TUNNELS_GATES
    ]
    city = [
        _gate_entry(
            models[4],
            "C",
            gate,
            requirement,
            x,
            z,
            (radius << 8) + CITY_STANDOFF_MARGIN,
            f"trigger radius ~{radius << 8} + {CITY_STANDOFF_MARGIN} margin",
        )
        for gate, requirement, x, z, radius in CITY_GATES
    ]
    report["levels"]["3-tunnels"] = tunnels
    report["levels"]["4-city-entrance"] = city
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute grain-gate teleport standoff candidates."
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="print only the chosen standoff per gate",
    )
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    report = build_report(repo_root)
    if args.compact:
        for level_gates in report["levels"].values():
            for gate in level_gates:
                chosen = gate["chosen"]
                proven = gate.get("proven_point")
                line = f"{gate['mechanism']:>3} req {gate['retail_requirement']:>2}"
                if chosen is not None:
                    line += (
                        f"  standoff ({chosen['x']}, {chosen['rest_y']}, "
                        f"{chosen['z']}) spread {chosen['spread']}"
                    )
                else:
                    line += "  no valid computed candidate"
                if proven is not None:
                    line += (
                        f"  [proven: ({proven['x']}, {proven['y']}, "
                        f"{proven['z']})]"
                    )
                print(line)
        return 0
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
