#!/usr/bin/env python3
"""Build EXP-20260905-009 without launching or changing a live process."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import time

from ablpc.terrain_additive import build_additive_pair, digest


ROOT = Path(__file__).resolve().parents[1]
RETAIL = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS"
DONOR = ROOT / "work/copies/EXP-20260905-006/fixture"
DESTINATION = ROOT / "work/copies/EXP-20260905-009"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="store_true", help="also make a fresh full game copy")
    args = parser.parse_args()
    started = time.monotonic()
    if DESTINATION.exists():
        raise ValueError(f"refusing to replace an existing experiment: {DESTINATION}")
    if not DESTINATION.resolve().is_relative_to((ROOT / "work/copies").resolve()):
        raise ValueError("output must stay under work/copies")
    original = RETAIL / "CD/LEVEL01"
    terrain, dat, receipt = build_additive_pair(
        (original / "TERRAIN.ALL").read_bytes(),
        (original / "LEVEL.DAT").read_bytes(),
        (DONOR / "TERRAIN.ALL").read_bytes(),
        (DONOR / "LEVEL.DAT").read_bytes(),
    )
    fixture = DESTINATION / "fixture"
    fixture.mkdir(parents=True)
    (fixture / "TERRAIN.ALL").write_bytes(terrain)
    (fixture / "LEVEL.DAT").write_bytes(dat)
    receipt.update({
        "experiment": "EXP-20260905-009",
        "fixture": str(fixture.relative_to(ROOT)),
        "build_seconds": round(time.monotonic() - started, 6),
        "runtime_tested": False,
        "live_process_actions": [],
    })
    if args.stage:
        game = DESTINATION / "game/PC/BUGS"
        shutil.copytree(RETAIL, game)
        log = game / "bugs.log"
        if log.exists():
            log.unlink()
        level = game / "CD/LEVEL01"
        (level / "TERRAIN.ALL").write_bytes(terrain)
        (level / "LEVEL.DAT").write_bytes(dat)
        receipt["staged_game"] = str(game.relative_to(ROOT))
        receipt["staged_level01_sha256"] = {
            "TERRAIN.ALL": digest(terrain), "LEVEL.DAT": digest(dat)
        }
    report = ROOT / "reports/terrain/EXP-20260905-009.json"
    if report.exists():
        raise ValueError(f"refusing to replace an existing report: {report}")
    report.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"report": str(report.relative_to(ROOT)), **receipt}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
