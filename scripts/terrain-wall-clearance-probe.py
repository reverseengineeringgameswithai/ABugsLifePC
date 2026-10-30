#!/usr/bin/env python3
"""EXP-20260906-004: isolated clearance build and original-PC offline gates.

No live game access. Coordinate/velocity writes below are to private Unicorn
fixtures only. Renderer/body-envelope acceptance still needs a live comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_wall_clearance import offset_x_wall_groups

CONTROL = ROOT / "work/copies/EXP-20260906-003/fixture"
TERRAIN_SHA = "288d57396d6de67db0df7904567c2bf2a0a40e4309fff490f9343928dc1075b7"
DAT_SHA = "f6cfa7883a902af5f43362356b7731adf9708ee5164c454b489e266867b048b2"
GROUPS = tuple(range(49084, 49964, 44))


def native_module():
    spec = importlib.util.spec_from_file_location("wall_clearance_retail", ROOT / "scripts/terrain-retail-probe.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Stepper:
    def __init__(self, module, terrain, text):
        self.m = module
        original = module.load_source
        module.load_source = lambda key: terrain if key == "level01" else original(key)
        try:
            self.probe = module.RetailProbe("level01", text)
        finally:
            module.load_source = original

    def reset(self, position):
        m, p = self.m, self.probe
        p.cpu.mem_write(m.IMAGE[0], p.baseline)
        for base, data in p.scratch_baseline.items():
            p.cpu.mem_write(base, data)
        p.cpu.context_restore(p.baseline_context)
        m.p.put(p.cpu, m.POSITION, "4i", *position, 0)
        m.p.put(p.cpu, m.FLAGS, "I", 0)

    def state(self):
        m, p = self.m, self.probe
        pointer = m.p.get(p.cpu, 0x007F3D6C, "I")[0]
        return {
            "position": list(m.p.get(p.cpu, m.POSITION, "3i")),
            "flags": list(m.p.get(p.cpu, m.FLAGS, "2B")),
            "contact": p.locate(pointer) if pointer else None,
        }

    def step(self, delta):
        m, p = self.m, self.probe
        m.p.put(p.cpu, m.VELOCITY, "4i", *delta, 0)
        stats = p.call(0x004AB1A0, (m.POSITION, m.VELOCITY, m.FLAGS, 0))
        return {**self.state(), "requested_delta": list(delta),
                "instruction_count": stats["instruction_count"]}

    def land(self, x, z):
        self.reset((x * 32, -180000, z * 32))
        samples = []
        for _ in range(240):
            sample = self.step((0, 1400, 0))
            samples.append(sample)
            if sample["flags"][1]:
                for _ in range(4):
                    samples.append(self.step((0, 512, 0)))
                return samples
        raise RuntimeError(f"bounded landing failed at {x},{z}")

    def walk_z(self, target, lane):
        samples = []
        direction = 1 if self.state()["position"][2] < target * 32 else -1
        for _ in range(180):
            state = self.state()
            if direction * (state["position"][2] - target * 32) >= 0:
                break
            correction = max(-384, min(384, lane * 32 - state["position"][0]))
            samples.append(self.step((correction, 512, direction * 900)))
        final = self.state()
        reached = direction * (final["position"][2] - target * 32) >= 0
        return {"target_z": target, "lane_x": lane, "samples": samples,
                "final": final, "accepted": reached and bool(final["flags"][1])}


def clearance_cases(stepper, terrain, margin):
    result = []
    for side, cell_offset, plane, sign in (("west", 49272, 184000, -1), ("east", 49712, 200000, 1)):
        cell = next(c for g in terrain.collision_payload(99).groups for c in g.cells if c.offset == cell_offset)
        w, base = cell.words, terrain.records[99].world_base
        center = [base[i] + (3 * w[3+i] + w[6+i] + w[9+i]) * 32 // 3 for i in range(3)]
        center[0] = plane + sign * 3072
        center[1] += 3200
        for speed in (256, 512, 900):
            stepper.reset(center)
            samples = [stepper.step((-sign * speed, 0, 0)) for _ in range(28)]
            distances = [sign * (s["position"][0] - plane) for s in samples]
            result.append({"side": side, "speed": speed, "start": center[:],
                "minimum_visible_plane_distance": min(distances), "expected_minimum": margin * 32,
                "accepted": min(distances) >= margin * 32, "samples": samples})
    return result


def grounded_sides(stepper, margin):
    result = []
    for side, x, plane, sign in (("west", 5450, 184000, -1), ("east", 6550, 200000, 1)):
        for z in (11700, 12300):
            landing = stepper.land(x, z)
            samples = [stepper.step((-sign * 900, 512, 0)) for _ in range(55)]
            distances = [sign * (s["position"][0] - plane) for s in samples]
            result.append({"side": side, "z": z, "landing": landing, "samples": samples,
                "minimum_visible_plane_distance": min(distances),
                "accepted": min(distances) >= margin * 32,
                "criterion": "blocking/clearance only; report flags, do not require continuously settled actor behavior"})
    return result


def ramp_routes(stepper):
    result = []
    for lane in (5850, 6000, 6150):
        landing = stepper.land(lane, 10800)
        legs = [stepper.walk_z(target, lane) for target in (13200, 10800, 13200)]
        result.append({"lane": lane, "landing": landing, "legs": legs,
            "accepted": all(leg["accepted"] for leg in legs),
            "controller": "bounded X correction +/-384 toward lane; Z +/-900; Y +512; no leg reset"})
    return result


def step_off_return(stepper):
    result = []
    for side, lane, outside, sign in (("west", 5850, 5450, -1), ("east", 6150, 6550, 1)):
        initial_landing = stepper.land(lane, 12200)
        departure = []
        for _ in range(50):
            if sign * (stepper.state()["position"][0] - outside * 32) >= 0:
                break
            departure.append(stepper.step((sign * 900, 512, 0)))
        settling = []
        for _ in range(160):
            sample = stepper.step((0, 1200, 0))
            settling.append(sample)
            if sample["flags"][1]:
                break
        landed = bool(stepper.state()["flags"][1])
        foot = stepper.walk_z(10800, outside)
        across = []
        for _ in range(80):
            state = stepper.state(); dx = lane * 32 - state["position"][0]
            if abs(dx) <= 64:
                break
            dz = max(-384, min(384, 10800 * 32 - state["position"][2]))
            across.append(stepper.step((max(-900, min(900, dx)), 512, dz)))
        returned = stepper.walk_z(12200, lane)
        result.append({"side": side, "initial_landing": initial_landing, "departure": departure,
            "settling": settling, "landed": landed, "open_foot": foot,
            "across_foot": across, "return": returned,
            "accepted": landed and foot["accepted"] and returned["accepted"]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--clearance", type=int, default=48)
    args = parser.parse_args()
    destination = args.fixture.resolve()
    if not destination.is_relative_to((ROOT / "work/copies").resolve()) or destination.exists():
        parser.error("fixture must be a fresh directory under work/copies")
    if args.report.exists():
        parser.error("report already exists")
    terrain_bytes = (CONTROL / "TERRAIN.ALL").read_bytes()
    dat_bytes = (CONTROL / "LEVEL.DAT").read_bytes()
    if hashlib.sha256(terrain_bytes).hexdigest() != TERRAIN_SHA or hashlib.sha256(dat_bytes).hexdigest() != DAT_SHA:
        raise ValueError("control asset SHA-256 mismatch")
    candidate_bytes, edit = offset_x_wall_groups(terrain_bytes, source_index=99,
        group_offsets=GROUPS, outward_stored=args.clearance)
    destination.mkdir(parents=True)
    for name, data in (("TERRAIN.ALL", candidate_bytes), ("LEVEL.DAT", dat_bytes)):
        with (destination / name).open("xb") as output:
            output.write(data)
    started = time.monotonic()
    module = native_module(); text = module.p.load_text(module.p.DEFAULT_BINARY)
    arms = []
    for name, data, margin in (("control", terrain_bytes, 0), ("clearance", candidate_bytes, args.clearance)):
        terrain = TerrainAll.parse(data); stepper = Stepper(module, terrain, text)
        clearance = clearance_cases(stepper, terrain, margin)
        sides = grounded_sides(stepper, margin)
        routes = ramp_routes(stepper)
        returns = step_off_return(stepper)
        arms.append({"name": name, "clearance": clearance, "grounded_sides": sides,
            "ramp_routes": routes, "step_off_return": returns,
            "accepted": all(row["accepted"] for rows in (clearance, sides, routes, returns) for row in rows)})
    report = {"experiment": "EXP-20260906-004", "kind": "offline original-PC instruction validation",
        "binary_sha256": module.p.BINARY_SHA256, "edit": edit,
        "dat_sha256": DAT_SHA, "dat_unchanged": True,
        "seconds": time.monotonic() - started, "arms": arms,
        "accepted": all(arm["accepted"] for arm in arms),
        "limits": ["No live renderer or actor-envelope acceptance.",
                   "Horizontal synthetic clearance cases start nongrounded; grounded approaches are separate.",
                   "Steered route criterion is separate from the retained failed EXP-003 fixed-axis route.",
                   "Only selected X-aligned ramp walls are offset; no universal wall or PC-radius rule."]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("x") as output:
        json.dump(report, output, indent=2); output.write("\n")
    print(json.dumps({"accepted": report["accepted"], "seconds": report["seconds"],
        "terrain_sha256": edit["after_sha256"], "dat_sha256": DAT_SHA,
        "arms": [{"name": a["name"], "accepted": a["accepted"],
                  "counts": {key: {"passed": sum(r["accepted"] for r in a[key]), "total": len(a[key])}
                             for key in ("clearance", "grounded_sides", "ramp_routes", "step_off_return")}}
                 for a in arms]}, indent=2))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
