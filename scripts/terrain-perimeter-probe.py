#!/usr/bin/env python3
"""EXP-006: discriminate both barrier windings around the isolated floor.

Collision-only offline arms. Foliage pairing and berry behavior remain separate
gates. Does not launch, control, read or write a live process.
"""

import importlib.util
import json
import math
from pathlib import Path
import time

from unicorn import UC_HOOK_CODE

from ablpc.terrain_all import TerrainAll
from ablpc.terrain_isolated import digest
from ablpc.terrain_perimeter import install_perimeter


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "work/copies/EXP-20260906-006"
OUTPUT = ROOT / "work/experiments/EXP-20260906-006/perimeter-native.json"
# Counterclockwise inset of the platform + access ramp union. No barrier across
# their shared internal seam. The 64 stored unit inset is a local trial only.
OUTLINE = ((4064, 13064), (5814, 13064), (5814, 10964), (6186, 10964),
           (6186, 13064), (8236, 13064), (8236, 18036), (4064, 18036), (4064, 13064))


def floor_contains(x, z):
    return ((4000 * 32 <= x <= 8300 * 32 and 13000 * 32 <= z <= 18100 * 32)
            or (5750 * 32 <= x <= 6250 * 32 and 10900 * 32 <= z <= 13000 * 32))


def normal(a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dz)
    return -dz / length, dx / length


def main():
    if DEST.exists() or OUTPUT.exists():
        raise ValueError("refusing to overwrite a perimeter experiment")
    control_path = ROOT / "work/copies/EXP-20260906-005/fixture"
    control = (control_path / "TERRAIN.ALL").read_bytes()
    dat = (control_path / "LEVEL.DAT").read_bytes()
    plant_bytes = (control_path / "PLANTTER.ALL").read_bytes()
    donor = TerrainAll.from_path(ROOT / "work/copies/EXP-20260906-004/fixture/TERRAIN.ALL")
    assert digest(control) == "961ff444fd875e80ce9e721e9f7fa264a7bea9059b54049d6145acc9154fb2db"
    assert digest(dat) == "3461dff75763670f54607efc6829c952158dc7876651c6a3f1088d0bcb0658af"
    assert digest(plant_bytes) == "c7fadbec78ac2c35f880c0dd5025e86a12604482c01dd93be38a90f6ad2d0cc9"
    assert digest(donor.data) == "26e7076fa4027e1a81a1c8d29260944c04e584486ef886d8ab85e1f5e5f8dfcc"
    r = donor.records[178]
    template = donor.data[r.payload_offset:r.payload_offset + r.payload_size]
    candidates = {name: install_perimeter(control, template, 178, points)
                  for name, points in (("positive", OUTLINE), ("negative", tuple(reversed(OUTLINE))))}
    for name, data in candidates.items():
        fixture = DEST / name / "fixture"
        fixture.mkdir(parents=True)
        for filename, contents in (("TERRAIN.ALL", data), ("LEVEL.DAT", dat), ("PLANTTER.ALL", plant_bytes)):
            (fixture / filename).write_bytes(contents)
    spec = importlib.util.spec_from_file_location("perimeter_clearance", ROOT / "scripts/terrain-wall-clearance-probe.py")
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    m = c.native_module()
    original_loader = m.load_source
    plant = TerrainAll.parse(plant_bytes)
    text = m.p.load_text(m.p.DEFAULT_BINARY)
    cases = []
    for i, (a, b) in enumerate(zip(OUTLINE, OUTLINE[1:])):
        nx, nz = normal(a, b)
        cases.append({"name": f"edge-{i}", "x": round((a[0] + b[0]) / 2 + nx * 128),
                      "z": round((a[1] + b[1]) / 2 + nz * 128), "nx": nx, "nz": nz})
    for i, point in enumerate(OUTLINE[:-1]):
        a = normal(OUTLINE[i - 1] if i else OUTLINE[-2], point)
        b = normal(point, OUTLINE[i + 1])
        length = math.hypot(a[0] + b[0], a[1] + b[1])
        nx, nz = (a[0] + b[0]) / length, (a[1] + b[1]) / length
        cases.append({"name": f"corner-{i}", "x": round(point[0] + nx * 128),
                      "z": round(point[1] + nz * 128), "nx": nx, "nz": nz})
    report = {"experiment": "EXP-20260906-006", "mode": "offline original PC instructions",
              "source": 178, "payload_offset": r.payload_offset, "payload_bytes": r.payload_size,
              "outline_stored_positive": OUTLINE, "inset_stored": 64, "arms": {},
              "foliage_paired": False, "berry_behavior_tested": False, "live_actions": []}
    started = time.monotonic()
    for name, data in {"unbarred_control": control, **candidates}.items():
        m.load_source = lambda key: plant if key == "plantter" else original_loader(key)
        try:
            stepper = c.Stepper(m, TerrainAll.parse(data), text)
        finally:
            m.load_source = original_loader
        results = []
        updates = []
        hook = stepper.probe.cpu.hook_add(UC_HOOK_CODE, lambda cpu, address, size, _: updates.append(address) if address == 0x004A9787 else None)
        try:
            for case in cases:
                for airborne in (False, True):
                    landing = stepper.land(case["x"], case["z"])
                    if airborne:
                        x, y, z = stepper.state()["position"]
                        stepper.reset((x, y - 12000, z))
                    initial = stepper.state()
                    dx, dz = round(-case["nx"] * 1200), round(-case["nz"] * 1200)
                    updates.clear()
                    trace = [stepper.step((dx, 0 if airborne else 512, dz)) for _ in range(24)]
                    push_updates = len(updates)
                    stayed_over_floor = all(floor_contains(s["position"][0], s["position"][2]) for s in trace)
                    outward = max((s["position"][0] - initial["position"][0]) * -case["nx"]
                                  + (s["position"][2] - initial["position"][2]) * -case["nz"] for s in trace)
                    final = trace[-1]
                    retreat = [stepper.step((-dx, 0 if airborne else 512, -dz)) for _ in range(8)]
                    accepted = stayed_over_floor and push_updates > 0 and outward <= 128 * 32 + 512
                    if not airborne:
                        accepted = accepted and final["flags"] == [1, 1]
                    results.append({"case": case, "airborne_setup": airborne, "accepted_containment": accepted,
                                    "landing": landing, "initial": initial, "push": trace,
                                    "segment_updates_during_push": push_updates, "stayed_over_authored_floor": stayed_over_floor,
                                    "maximum_outward_world": outward, "retreat": retreat})
        finally:
            stepper.probe.cpu.hook_del(hook)
        report["arms"][name] = {"terrain_sha256": digest(data), "accepted_cases": sum(r["accepted_containment"] for r in results),
                                "case_count": len(results), "all_contained": all(r["accepted_containment"] for r in results), "cases": results}
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({"arm": name, "accepted_cases": report["arms"][name]["accepted_cases"], "cases": len(results)}), flush=True)
    report["seconds"] = time.monotonic() - started
    report["accepted_windings"] = [name for name in candidates if report["arms"][name]["all_contained"]]
    report["control_has_no_segment_responses"] = all(r["segment_updates_during_push"] == 0 for r in report["arms"]["unbarred_control"]["cases"])
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"accepted_windings": report["accepted_windings"], "seconds": report["seconds"], "report": str(OUTPUT)}))


if __name__ == "__main__":
    main()
