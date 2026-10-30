#!/usr/bin/env python3
"""Build EXP-20260906-002 decorative ramp side faces, without runtime actions."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import struct
import time

from ablpc.level_dat import LevelDat
from ablpc.terrain_additive import append_render_geometry
from ablpc.terrain_ramp_sides import buried_base, ground_boundary_spans, side_face_mesh
from ablpc.terrain_wall_material import native_wall_profile


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = "EXP-20260906-002"
DAT_SHA = "691674fdca9b87a95f477bfb144f9ff6d805fecc05785669c68162c8f4f17659"
TERRAIN_SHA = "77a77456c3b9a0f4db5e7b20d257a9772e04c0f0ed3d0812590943d630851698"
ORIGINAL_TERRAIN_SHA = "62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_value(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="store_true")
    args = parser.parse_args()
    start = time.monotonic()
    source = ROOT / "work/copies/EXP-20260906-001"
    original = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01"
    destination = ROOT / "work/copies" / EXPERIMENT
    report_path = ROOT / "reports/terrain" / f"{EXPERIMENT}.json"
    if destination.exists() or report_path.exists():
        raise ValueError("refusing to replace an experiment or report")
    dat = (source / "fixture/LEVEL.DAT").read_bytes()
    terrain = (source / "fixture/TERRAIN.ALL").read_bytes()
    original_terrain = (original / "TERRAIN.ALL").read_bytes()
    if (digest(dat), digest(terrain), digest(original_terrain)) != (DAT_SHA, TERRAIN_SHA, ORIGINAL_TERRAIN_SHA):
        raise ValueError("control or original terrain provenance mismatch")
    donor = native_wall_profile((original / "LEVEL.DAT").read_bytes())
    reference = LevelDat.parse(dat).static_mesh_reference("primary", 160)
    if (reference.record_offset, reference.object_offset, reference.geometry_offset) != (8580, 18672, 332820):
        raise ValueError("unexpected control mesh locations")
    origin = struct.unpack_from("<3i", dat, reference.object_offset)
    ramp = []
    for index in range(416, 439):
        offset = reference.geometry_offset + 4 + index * 12
        if offset + 12 > len(dat) - 4:
            raise ValueError("truncated ramp vertex")
        raw = dat[offset:offset + 12]
        xyz = tuple(a + b for a, b in zip(struct.unpack_from("<3h", raw), origin))
        ramp.append((index, offset, xyz, raw[6:]))
    if len({entry[3] for entry in ramp}) != 1:
        raise ValueError("ramp suffix disagreement")
    left, right = (sorted((entry for entry in ramp if entry[2][0] == x), key=lambda entry: entry[2][2])
                   for x in (5750, 6250))
    if len(left) != 6 or len(right) != 6:
        raise ValueError("unexpected ramp edge topology")
    spans = {str(x): ground_boundary_spans(original_terrain, source_index=99, x=x, z_start=10900, z_end=13000)
             for x in (5750, 6250)}
    bottom = buried_base([span for side in spans.values() for span in side], burial=256)
    addition, walls = side_face_mesh(
        tuple(entry[2] for entry in left), tuple(entry[2] for entry in right),
        origin=origin, bottom_y=bottom, vertex_suffix=ramp[0][3],
        top_channels=donor["top_channels"], bottom_channels=donor["bottom_channels"],
    )
    candidate, allocation = append_render_geometry(dat, ((addition, origin),), record_index=160)
    fixture = destination / "fixture"
    fixture.mkdir(parents=True)
    (fixture / "LEVEL.DAT").write_bytes(candidate)
    (fixture / "TERRAIN.ALL").write_bytes(terrain)
    (fixture / "side-faces.mesh").write_bytes(addition)
    if args.stage:
        # Full independent game tree. Never edit the currently running copy.
        shutil.copytree(source / "game", destination / "game")
        game = destination / "game/PC/BUGS"
        (game / "CD/LEVEL01/LEVEL.DAT").write_bytes(candidate)
        log = game / "bugs.log"
        if log.exists():
            log.unlink()
    receipt = {
        "experiment": EXPERIMENT, "status": "built-not-launched", "fixture": str(fixture.relative_to(ROOT)),
        "staged": args.stage, "build_seconds": time.monotonic() - start,
        "control_dat_sha256": DAT_SHA, "candidate_dat_sha256": digest(candidate),
        "terrain_sha256_unchanged": digest(terrain), "side_mesh_sha256": digest(addition),
        "original_terrain_sha256": ORIGINAL_TERRAIN_SHA,
        "control_size": len(dat), "candidate_size": len(candidate), "donor": donor,
        "walls": walls, "allocation": allocation, "ground_spans": spans,
        "edge_vertex_indices": [[entry[0] for entry in edge] for edge in (left, right)],
        "edge_vertex_offsets": [[entry[1] for entry in edge] for edge in (left, right)],
        "base_choice": "ceil(maximum original triangle-plane boundary height) + 256 stored units; buried overlap, not welded ground",
        "user_request": "Side faces down to the ground, not guardrails",
        "control_feedback": "User: I think this works now. Manual report, not instrumented all-angle acceptance.",
        "limits": ["No new collision walls or barriers", "No bottom, foot or deck-end cap",
                   "Original PC loader path reused, not newly instrumented for this candidate",
                   "Ground-boundary planes are geometric bounds, not PC contact trajectories",
                   "New side-face appearance and sorting await a fresh file-loaded preview"],
        "live_process_actions": [], "full_suite_or_r2q": False,
    }
    report_path.write_text(json.dumps(receipt, indent=2, default=json_value) + "\n")
    print(json.dumps({"report": str(report_path.relative_to(ROOT)), "candidate_dat_sha256": digest(candidate),
                      "walls": walls, "allocation": allocation, "build_seconds": receipt["build_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
