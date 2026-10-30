#!/usr/bin/env python3
"""Original-PC offline gates for the stripped EXP-20260906-005 fixture."""

import importlib.util
import json
from pathlib import Path
import struct
import time

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX

from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_isolated import pe_file_offset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "work/copies/EXP-20260906-005/fixture"
OUTPUT = ROOT / "work/experiments/EXP-20260906-005/native-validation-02.json"


def module(filename, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    if OUTPUT.exists():
        raise ValueError("refusing to replace a proof receipt")
    start = time.monotonic()
    clearance = module("terrain-wall-clearance-probe.py", "isolated_clearance")
    m = clearance.native_module()
    text = m.p.load_text(m.p.DEFAULT_BINARY)
    terrain = TerrainAll.from_path(FIXTURE / "TERRAIN.ALL")
    plant = TerrainAll.from_path(FIXTURE / "PLANTTER.ALL")
    original_loader = m.load_source
    m.load_source = lambda key: plant if key == "plantter" else original_loader(key)
    try:
        stepper = clearance.Stepper(m, terrain, text)
    finally:
        m.load_source = original_loader
    ref = stepper.probe
    report = {"experiment": "EXP-20260906-005", "kind": "offline original PC instructions",
              "live_process_actions": [], "arms": {},
              "limitation": "Finite synthetic movements, not a full actor/input replay or visual runtime acceptance."}

    def arm(name, function):
        before = time.monotonic()
        try:
            result = function()
            assert "accepted" in result
        except Exception as error:
            result = {"accepted": False, "error": f"{type(error).__name__}: {error}"}
        result["seconds"] = time.monotonic() - before
        report["arms"][name] = result
        OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({"arm": name, "accepted": result["accepted"], "error": result.get("error")}), flush=True)

    def census():
        counts = []
        total = 0
        for index in range(ref.loaded_count):
            descriptor = m.p.DESCRIPTORS + 48 * index
            kind = struct.unpack("<h", ref.cpu.mem_read(descriptor + 44, 2))[0]
            if kind not in (6, 7, 8):
                continue
            pointer = struct.unpack("<I", ref.cpu.mem_read(descriptor + 16, 4))[0]
            location = ref.locate(pointer)
            assert location is not None
            cursor = pointer
            cells = 0
            groups = []
            while struct.unpack("<h", ref.cpu.mem_read(cursor, 2))[0] >= 0:
                count = struct.unpack("<h", ref.cpu.mem_read(cursor + 2, 2))[0]
                assert 0 <= count <= 1000 and len(groups) < 1000
                groups.append(ref.locate(cursor))
                cells += count
                cursor += 12 + count * 32
            if cells:
                assert location["source"] == "level01" and location["source_record"] == 99
                assert cells == 36
            total += cells
            counts.append({"descriptor": index, "location": location, "cells": cells, "groups": groups})
        links = {hex(a): struct.unpack("<I", ref.cpu.mem_read(a, 4))[0] for a in (0x007F3D3C, 0x007F3D48)}
        assert all(v == 0 for v in links.values())
        return {"accepted": total == 36, "active_cell_instances": total,
                "loaded_descriptors": ref.loaded_count, "linked_heads": links, "descriptors": counts}

    arm("native_collision_census", census)

    def spawn():
        stepper.reset((0, 0, 0))
        image = (FIXTURE.parent / "auto-hardware/bugs.exe").read_bytes()
        row_offset = pe_file_offset(image, 0x004DC7F4, 12)
        row = image[row_offset:row_offset + 12]
        assert struct.unpack("<iii", row) == (192000, 448000, 3505)
        ref.cpu.mem_write(0x004DC7F4, row)
        stats = ref.call(0x0043E6B0, (0x0059D910, 1))
        position = struct.unpack("<3i", ref.cpu.mem_read(0x0059D910, 12))
        preceding = struct.unpack("<3i", ref.cpu.mem_read(0x0059D920, 12))
        auxiliary = struct.unpack("<3i", ref.cpu.mem_read(0x0059D960, 12))
        heading = struct.unpack("<i", ref.cpu.mem_read(0x0059D930, 4))[0]
        assert position == preceding == auxiliary
        assert (position[0], position[2], heading) == (192000, 448000, 3505)
        assert abs(position[1] + 102400) < 8192
        stepper.reset(position)
        settled = [stepper.step((0, 512, 0)) for _ in range(12)]
        final = stepper.state()
        return {"accepted": final["flags"] == [1, 1] and final["contact"]["source_record"] == 99,
                "initial": position, "preceding": preceding, "auxiliary": auxiliary,
                "heading": heading, "initializer": stats, "settling": settled,
                "final": final, "offline_table_setup": "complete file-backed Level01 X/Z/heading row; no live process"}

    arm("native_initial_spawn_and_settle", spawn)

    def relocate_and_mute():
        tiling = module("terrain-texture-tiling-probe.py", "isolated_tiling")
        dat_bytes = (FIXTURE / "LEVEL.DAT").read_bytes()
        relocated, globals_ = tiling.relocate(Path(m.p.DEFAULT_BINARY).read_bytes(), dat_bytes)
        dat = LevelDat.parse(dat_bytes)
        base = 0x10000000
        ref.cpu.mem_map(base, (len(relocated) + 4095) & ~4095)
        ref.cpu.mem_write(base, relocated)
        calls = []
        watched = {0x0045A7F0, 0x00454B70, 0x00453FF0, 0x00463770, 0x004636C0, 0x00463C80}
        hook = ref.cpu.hook_add(UC_HOOK_CODE, lambda cpu, address, size, _: calls.append(hex(address)) if address in watched else None)
        stats = []
        try:
            for section, records, entry in (("primary", dat.primary_records, 0x004498F0),
                                             ("secondary", dat.secondary_records, 0x00448D70)):
                pointers = [base + r.offset for r in records if not (section == "primary" and r.index == 160)]
                address = m.p.FIXTURE + 0x2000
                ref.cpu.mem_write(address, struct.pack("<" + "I" * len(pointers), *pointers))
                for draw_pass in ((0, 16) if section == "primary" else (0,)):
                    args = (address, len(pointers), 0, draw_pass) if section == "primary" else (address, len(pointers), 0)
                    stats.append({"section": section, "count": len(pointers), "pass": draw_pass,
                                  "execution": ref.call(entry, args)})
        finally:
            ref.cpu.hook_del(hook)
        boundary = module("terrain-floor-boundary-probe.py", "isolated_boundary")
        commands = boundary.stream_instruction_audit(dat, text)
        return {"accepted": not calls, "unexpected_draw_calls": calls, "dispatches": stats,
                "relocation": globals_, "new_command_stream": commands}

    arm("native_dat_relocation_old_draw_suppression_and_new_stream", relocate_and_mute)

    for lane in (5850, 6000, 6150):
        def ramp(lane=lane):
            landing = stepper.land(lane, 14000)
            down = stepper.walk_z(11100, lane)
            up = stepper.walk_z(14000, lane)
            return {"accepted": down["accepted"] and up["accepted"], "landing": landing,
                    "downhill": down, "uphill_return": up, "final": stepper.state()}
        arm(f"ramp_downhill_and_return_x{lane}", ramp)

    def walk_x(target, max_steps=180):
        sign = 1 if target * 32 > stepper.state()["position"][0] else -1
        trace = []
        for _ in range(max_steps):
            trace.append(stepper.step((sign * 900, 512, 0)))
            if sign * (trace[-1]["position"][0] - target * 32) >= 0:
                break
        return {"accepted": sign * (trace[-1]["position"][0] - target * 32) >= 0 and trace[-1]["flags"] == [1, 1], "trace": trace}

    def box():
        landing = stepper.land(7500, 15900)
        up = walk_x(5425)
        down = walk_x(7500)
        return {"accepted": up["accepted"] and down["accepted"], "landing": landing, "up": up, "return": down}
    arm("box_uphill_downhill_return", box)

    def step_off():
        landing = stepper.land(5250, 15900)
        off = walk_x(4700)
        return {"accepted": off["accepted"], "top_landing": landing, "step_off_to_new_deck": off}
    arm("box_top_landing_and_stepoff", step_off)

    def void():
        landing = stepper.land(8100, 14000)
        edge = [stepper.step((900, 512, 0)) for _ in range(20)]
        fall = [stepper.step((0, 1400, 0)) for _ in range(150)]
        return {"accepted": all(s["flags"] == [0, 0] for s in fall) and fall[-1]["position"][1] > 0,
                "landing": landing, "edge": edge, "fall": fall,
                "expected": "No original floor remains outside the authored platform"}
    arm("platform_edge_deliberate_void", void)

    def original_footprints():
        rows = []
        for x, z in ((124987, 328714), (191376, 348189), (249967, 371497), (222481, 383185), (320000, 500000)):
            stepper.reset((x, -180000, z))
            query = m.p.FIXTURE + 0x1000
            ref.cpu.mem_write(query, struct.pack("<4i", x, -0x80000000, z, 0))
            ref.call(0x004AC460, (query,))
            result = ref.cpu.reg_read(UC_X86_REG_EAX)
            rows.append({"x": x, "z": z, "result_u32": result})
        return {"accepted": all(r["result_u32"] == 0x80000000 for r in rows), "queries": rows}
    arm("removed_original_floor_negative_queries", original_footprints)
    report["seconds"] = time.monotonic() - start
    report["accepted"] = all(a["accepted"] for a in report["arms"].values())
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"accepted": report["accepted"], "seconds": report["seconds"], "report": str(OUTPUT)}))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
