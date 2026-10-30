#!/usr/bin/env python3
"""Bounded original-PC instruction proofs for additive EXP-009 assets.

All emulated state setup is inside offline Unicorn instances. This script
does not connect to a game, inject input, or read/write any live process.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import struct
import time

from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_additive import digest


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01"
FIXTURE = ROOT / "work/copies/EXP-20260905-009/fixture"
REPLACEMENT = ROOT / "work/copies/EXP-20260905-006/fixture"


def reference(filename: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "work/experiments/EXP-20260905-009/offline-proof.json")
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to((ROOT / "work").resolve()) or output.exists():
        raise ValueError("proof output must be a fresh path under work/")
    output.parent.mkdir(parents=True, exist_ok=True)
    boundary = reference("terrain-floor-boundary-probe.py", "additive_boundary")
    play = reference("terrain-play-area.py", "additive_play")
    tiling = reference("terrain-texture-tiling-probe.py", "additive_tiling")
    text = boundary.b.p.load_text(boundary.b.p.DEFAULT_BINARY)
    retail_bytes = (ORIGINAL / "TERRAIN.ALL").read_bytes()
    added_bytes = (FIXTURE / "TERRAIN.ALL").read_bytes()
    retail_dat = (ORIGINAL / "LEVEL.DAT").read_bytes()
    added_dat = (FIXTURE / "LEVEL.DAT").read_bytes()
    terrains = {
        "retail": TerrainAll.parse(retail_bytes),
        "additive": TerrainAll.parse(added_bytes),
        "replacement_control": TerrainAll.from_path(REPLACEMENT / "TERRAIN.ALL"),
    }
    started = time.monotonic()
    report = {
        "experiment": "EXP-20260905-009",
        "kind": "offline-original-PC-instruction-proof",
        "live_process_actions": [],
        "full_actor_or_keyboard_replay": False,
        "limitation": "Finite synthetic displacements through the native collision coordinator, not a replay of the complete retail actor/input loop or runtime rendering acceptance.",
        "input_sha256": {
            "retail_terrain": digest(retail_bytes), "additive_terrain": digest(added_bytes),
            "retail_dat": digest(retail_dat), "additive_dat": digest(added_dat),
        },
        "arms": {},
    }

    def arm(name, function):
        start = time.monotonic()
        try:
            result = function()
            if "accepted" not in result:
                raise ValueError("arm must explicitly state acceptance")
        except Exception as error:
            result = {"accepted": False, "error": f"{type(error).__name__}: {error}"}
        result["seconds"] = round(time.monotonic() - start, 6)
        report["arms"][name] = result
        output.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({"arm": name, "accepted": result["accepted"], "seconds": result["seconds"], "error": result.get("error")}), flush=True)

    probes = {}

    def load_and_preserve():
        for name, terrain in terrains.items():
            probes[name] = boundary.Probe(terrain, text)
        old, new = probes["retail"].probe.ref, probes["additive"].probe.ref
        p = boundary.b.p
        assert old.loaded_count == new.loaded_count
        assert old.loaded_tags == new.loaded_tags
        assert old.initialized_tags == new.initialized_tags
        original_cells, reached_cells = 0, 0
        records = []
        for index in range(old.loaded_count):
            descriptor = p.DESCRIPTORS + index * 48
            tag = struct.unpack("<h", old.cpu.mem_read(descriptor + 44, 2))[0]
            if tag not in (6, 7, 8):
                continue
            old_pointer = struct.unpack("<I", old.cpu.mem_read(descriptor + 16, 4))[0]
            new_pointer = struct.unpack("<I", new.cpu.mem_read(descriptor + 16, 4))[0]
            old_location, new_location = old.locate(old_pointer), new.locate(new_pointer)
            assert old_location is not None and new_location is not None
            assert old_location["source"] == new_location["source"]
            assert old_location["source_record"] == new_location["source_record"]
            source = terrains["retail"] if old_location["source"] == "level01" else old.sources[1]
            payload = source.collision_payload(old_location["source_record"])
            count = 0
            for group in payload.groups:
                for cell in group.cells:
                    relative = cell.offset - old_location["file_offset"]
                    original_cells += 1
                    assert bytes(new.cpu.mem_read(new_pointer + relative, 32)) == cell.raw
                    reached_cells += 1
                    count += 1
            records.append({"runtime_descriptor": index, "original": old_location, "additive": new_location, "preserved_original_cells": count})
        return {
            "accepted": original_cells == reached_cells and original_cells > 0,
            "preserved_runtime_cell_instances": reached_cells,
            "descriptor_payloads": records,
            "retail_initialization": old.initialization_report(),
            "additive_initialization": new.initialization_report(),
            "evidence": ["004A8410", "004A89F8..004A908F"],
        }

    arm("native_loader_and_original_cell_reachability", load_and_preserve)

    def dat_relocation():
        image = Path(boundary.b.p.DEFAULT_BINARY).read_bytes()
        before, old_globals = tiling.relocate(image, retail_dat)
        after, new_globals = tiling.relocate(image, added_dat)
        old_ref = LevelDat.parse(retail_dat).static_mesh_reference("primary", 160)
        new_ref = LevelDat.parse(added_dat).static_mesh_reference("primary", 160)
        allowed = set(range(old_ref.object_offset + 20, old_ref.object_offset + 24)) | {old_ref.object_offset + 18, old_ref.record_offset + 12, old_ref.record_offset + 13}
        differences = [i for i, (a, b) in enumerate(zip(before[:-4], after)) if a != b]
        assert set(differences) <= allowed
        assert struct.unpack_from("<I", after, new_ref.object_offset + 20)[0] == 0x10000000 + new_ref.geometry_offset
        assert after[new_ref.geometry_offset:-4] == added_dat[new_ref.geometry_offset:-4]
        for key in ("trailing_data_pointer", "trailing_plus_118_pointer", "trailer_table_sha256"):
            assert old_globals[key] == new_globals[key]
        return {
            "accepted": True, "retail_globals": old_globals, "additive_globals": new_globals,
            "changed_relocated_prefix_byte_offsets": differences,
            "geometry_offset": new_ref.geometry_offset,
            "evidence": ["0044BB70", "0044BD13..0044BD22", "0044BEC4..0044BF25"],
        }

    arm("native_dat_relocation", dat_relocation)

    def command_stream():
        result = boundary.stream_instruction_audit(LevelDat.parse(added_dat), text)
        return {"accepted": True, "native_stream_audit": result, "limitation": "Command traversal acceptance is not a rendered-image comparison."}

    arm("native_dat_command_stream", command_stream)

    def traverse(x, z_from, z_to):
        probe = probes["additive"]
        probe.land(x * 32, z_from * 32, start_y=-3200 * 32 - 1024)
        initial = probe.probe.state()
        outward = play.walk_to(probe, (x * 32, z_to * 32), 900)
        foot = probe.probe.state()
        backward = play.walk_to(probe, (x * 32, z_from * 32), 900)
        return {
            "accepted": bool(outward["accepted"] and backward["accepted"]),
            "initial": initial, "foot": foot, "returned": probe.probe.state(),
            "outward": outward, "return": backward,
            "intended_contact_order": "appended deck -> appended connector -> preserved original floor -> connector -> deck",
        }

    for lane in (5850, 6000, 6150):
        arm(f"connector_downhill_uphill_x{lane}", lambda lane=lane: traverse(lane, 13200, 10800))

    def box_return():
        probe = probes["additive"]
        probe.land(7500 * 32, 15900 * 32, start_y=-3200 * 32 - 1024)
        uphill = play.walk_to(probe, (5425 * 32, 15900 * 32), 900)
        top = probe.probe.state()
        downhill = play.walk_to(probe, (7500 * 32, 15900 * 32), 900)
        return {"accepted": bool(uphill["accepted"] and downhill["accepted"]), "uphill": uphill, "top": top, "downhill": downhill}

    arm("banked_box_uphill_downhill_in_additive_context", box_return)

    def landing_stepoff():
        probe = probes["additive"]
        probe.land(5250 * 32, 15900 * 32, start_y=-3392 * 32 - 1024)
        steps = []
        for _ in range(16):
            steps.append(probe.step((0, 2048, 0)))
            if steps[-1]["after"]["flags"] == [1, 1]:
                break
        top = probe.probe.state()
        crossing = play.walk_to(probe, (4700 * 32, 15900 * 32), 900, allowed_airborne=30)
        return {"accepted": top["flags"] == [1, 1] and bool(crossing["accepted"]), "landing": steps, "top": top, "step_off": crossing}

    arm("top_landing_and_stepoff", landing_stepoff)

    def fall(name):
        probe = probes[name]
        probe.land(220590, 435460, start_y=-3200 * 32 - 1024)
        initial = probe.probe.state()
        steps = [probe.step((33, 512, -900)) for _ in range(58)]
        steps.extend(probe.step((0, 512, 0)) for _ in range(120))
        final = probe.probe.state()
        expected = [0, 0] if name == "replacement_control" else [1, 1]
        return {
            "accepted": final["flags"] == expected,
            "initial": initial, "final": final, "summary": boundary.summary(steps), "steps": steps,
            "comparison": "Identical finite synthetic route near the recorded fall, not exact actor-input replay.",
            "expected": "remains airborne" if name == "replacement_control" else "lands on preserved original collision",
        }

    arm("replacing_fixture_fall_control", lambda: fall("replacement_control"))
    arm("additive_same_synthetic_fall", lambda: fall("additive"))

    def ground_return():
        probe = probes["additive"]
        initial = probe.probe.state()
        to_foot = play.walk_to(probe, (6000 * 32, 10800 * 32), 900, max_steps=500)
        uphill = play.walk_to(probe, (6000 * 32, 13200 * 32), 900)
        return {"accepted": bool(to_foot["accepted"] and uphill["accepted"]), "initial": initial, "to_foot": to_foot, "uphill": uphill, "returned": probe.probe.state()}

    arm("return_from_restored_landing_to_deck", ground_return)
    report["seconds"] = round(time.monotonic() - started, 6)
    report["accepted"] = all(row["accepted"] for row in report["arms"].values())
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"accepted": report["accepted"], "seconds": report["seconds"], "report": str(output.relative_to(ROOT))}))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
