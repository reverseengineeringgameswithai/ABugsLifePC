#!/usr/bin/env python3
"""EXP-20260905-003: shared-floor census, reverse failure and stitched control.

Original PC instructions, synthetic motion only. Optional paired assets are
created exclusively at a new directory under work/copies. Never starts a game.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_all import TerrainAll
from ablpc.level_dat import LevelDat
from ablpc.terrain_height import TerrainHeightModel
from ablpc.terrain_floor_patch import (boundary_census, digest, floor_cells, mesh_groups,
    normal, paired_visual, render_census, stitch_floor_vertex)
from unicorn.x86_const import UC_X86_REG_ESI, UC_X86_REG_EDI, UC_X86_REG_EBX, UC_X86_REG_ESP

spec = importlib.util.spec_from_file_location("floor_control", ROOT / "scripts/terrain-floor-authoring-probe.py")
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)
b = control.b
EXPERIMENT = "EXP-20260905-003"
VERTEX = (6103, 16, 16174)
DY = -64
LEVEL_SHA = "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"
EXPECTED = (47652, 47684, 47716, 47748, 47812, 48856)


def fixture():
    retail, rigid = control.fixture()
    raw = (b.retail.SOURCE_ROOT / "CD/LEVEL01/LEVEL.DAT").read_bytes()
    b.p.require(digest(raw) == LEVEL_SHA, "Level01 DAT hash mismatch")
    cells = floor_cells(retail)
    incident = [c for c in cells if VERTEX in c.vertices]
    b.p.require(tuple(c.offset for c in incident) == EXPECTED, "incident-corner census changed")
    terrain, edits = stitch_floor_vertex(retail.data, VERTEX, DY)
    dat, render_edits = paired_visual(raw, incident, VERTEX, DY)
    return retail, rigid, TerrainAll.parse(terrain), raw, dat, cells, edits, render_edits


class Probe:
    def __init__(self, terrain, text):
        self.terrain = terrain
        self.probe = control.a.reference(terrain, text)
        self.height = TerrainHeightModel(terrain)
        self.floor_only = False
        self.events = []
        original = self.probe.ref.run

        def run(entry, stop, observe=None, **kwargs):
            def hook(cpu, pc):
                if observe:
                    observe(cpu, pc)
                if pc in (0x004AA60B, 0x004AA646):
                    register = UC_X86_REG_EBX if pc == 0x004AA60B else UC_X86_REG_EDI
                    value = cpu.reg_read(register)
                    if value >= 2**31:
                        value -= 2**32
                    self.events.append({"pc": hex(pc), "signed_distance": value,
                                        **self.probe.ref.locate(cpu.reg_read(UC_X86_REG_ESI))})
            return original(entry, stop, hook, **kwargs)
        self.probe.ref.run = run

    def step(self, delta):
        self.events = []
        row = self.probe.step(tuple(delta))
        count = b.p.get(self.probe.cpu, 0x007FC8D4, "i")[0]
        b.p.require(0 <= count <= 400, "candidate capacity exceeded")
        row["admitted_cells"] = [self.probe.ref.locate(b.p.get(self.probe.cpu, 0x007F3F50+i*4, "I")[0]) for i in range(count)]
        row["plane_sign_tests"] = self.events
        return row

    def land(self, x, z, *, start_y=None):
        self.probe.reset()
        if self.floor_only:
            for i in range(self.probe.ref.loaded_count):
                if i not in (99, 100):
                    b.p.put(self.probe.cpu, b.p.DESCRIPTORS+i*48+44, "H", 0)
            b.p.put(self.probe.cpu, 0x007F3D3C, "I", 0)
        if start_y is None:
            hits = self.height.planes(x, z)
            b.p.require(bool(hits), "landing has no floor plane")
            start_y = min(h.plane_height for h in hits if h.divisor < 0)+3200-1024
        b.p.put(self.probe.cpu, b.retail.POSITION, "4i", x, start_y, z, 0)
        b.p.put(self.probe.cpu, b.retail.FLAGS, "I", 0)
        result = self.step((0, 2048, 0))
        b.p.require(result["after"]["flags"] == [1, 1], "original landing did not establish contact")
        return result


def summary(steps):
    transitions = []
    previous = None
    longest = current = 0
    for i, row in enumerate(steps):
        state = row["after"]
        cell = state["contact_cell"]
        key = (tuple(state["flags"]), state["contact_descriptor"], cell and cell["file_offset"])
        if key != previous:
            transitions.append({"step_zero_based": i, **state})
        previous = key
        current = current+1 if not state["flags"][1] else 0
        longest = max(longest, current)
    return {"transitions": transitions, "longest_airborne_run": longest,
            "final": steps[-1]["after"] if steps else None}


def return_route(probe, *, rigid=False):
    # Preserve the exact EXP-005 seed, then extend its unmodified forward path.
    landing = probe.land(197091, 492897, start_y=1710-(2048 if rigid else 0))
    legs = []
    for label, count, delta in (("forward", 35, (-900, 512, 700)),
                               ("return", 35, (900, 512, -700)),
                               ("settle", 15, (0, 512, 0))):
        steps = [probe.step(delta) for _ in range(count)]
        legs.append({"label": label, "steps": steps, **summary(steps)})
    return {"landing": landing, "legs": legs}


def cell_plane(cell, x, z):
    a = cell.vertices[0]
    nx, ny, nz = struct.unpack_from("<3h", cell.raw)
    return a[1]-(nx*(x-a[0])+nz*(z-a[2]))/ny


def crossing(probe, edge, owner, neighbor, direction):
    # Points 96 stored units to each side of the exact shared-edge midpoint.
    a, c = edge
    mx, mz = ((a[i]+c[i])/2 for i in range(2))
    dx, dz = c[0]-a[0], c[1]-a[1]
    length = math.hypot(dx, dz)
    nx, nz = -dz/length, dx/length
    centroid = tuple(sum(p[i] for p in owner.vertices)/3 for i in (0, 2))
    if (centroid[0]-mx)*nx+(centroid[1]-mz)*nz < 0:
        nx, nz = -nx, -nz
    sign = 1 if direction == "outward" else -1
    start = (round((mx+sign*96*nx)*32), round((mz+sign*96*nz)*32))
    end = (round((mx-sign*96*nx)*32), round((mz-sign*96*nz)*32))
    expected_start = owner if direction == "outward" else neighbor
    landing = probe.land(*start, start_y=round(cell_plane(expected_start, start[0]/32, start[1]/32)*32)+3200-1024)
    steps = []
    for _ in range(36):
        x, _, z = probe.probe.state()["position"]
        dx, dz = end[0]-x, end[1]-z
        distance = math.hypot(dx, dz)
        if distance < 256:
            break
        scale = min(384, distance)/distance
        steps.append(probe.step((round(dx*scale), 256, round(dz*scale))))
    settled = [probe.step((0, 256, 0)) for _ in range(4)]
    final = probe.probe.state()
    expected_end = neighbor if direction == "outward" else owner
    actual_start = landing["after"]["contact_cell"]
    actual_end = final["contact_cell"]
    result = {"edge_xz_stored": edge, "direction": direction,
              "control": "only_static_sources_99_100" if probe.floor_only else "complete_scene",
              "expected_start": [expected_start.source, expected_start.offset],
              "expected_end": [expected_end.source, expected_end.offset],
              "start_xz_world": start, "target_xz_world": end,
              "landing": landing, "steps": steps, "settling": settled,
              "start_contact_matches": actual_start is not None and
                  (actual_start["source_record"], actual_start["file_offset"]) == (expected_start.source, expected_start.offset),
              "end_contact_matches": actual_end is not None and
                  (actual_end["source_record"], actual_end["file_offset"]) == (expected_end.source, expected_end.offset),
              "reached_endpoint": math.hypot(final["position"][0]-end[0], final["position"][2]-end[1]) < 600,
              **summary(steps+settled)}
    result["accepted"] = (result["start_contact_matches"] and result["end_contact_matches"]
                          and result["reached_endpoint"] and final["flags"] == [1, 1]
                          and result["longest_airborne_run"] <= 2)
    return result


def stream_instruction_audit(dat, text):
    cpu = b.p.machine(text)
    base = 0x06000000
    cpu.mem_map(base, (len(dat.data)+4095)//4096*4096)
    cpu.mem_write(base, dat.data)
    # Use the existing original-instruction runner with a fresh synthetic image.
    runner = b.retail.RetailProbe.__new__(b.retail.RetailProbe)
    runner.cpu = cpu
    from unicorn.x86_const import UC_X86_REG_EIP
    rows = []
    for section in ("primary", "secondary"):
        for ref in dat.static_mesh_references(section):
            groups, terminator = mesh_groups(dat.data, ref)
            visited, faces = [], []
            cpu.reg_write(UC_X86_REG_ESI, base+ref.payload.vertices_offset+ref.payload.vertex_count*12)
            cpu.reg_write(UC_X86_REG_ESP, b.p.STACK+0x8000)
            cpu.reg_write(UC_X86_REG_EBX, 0)
            b.p.put(cpu, 0x0059F7F0, "h", 0)  # skip emission naturally; no draw claim
            def observe(machine, pc):
                if pc == 0x0045A8B0:
                    visited.append(machine.reg_read(UC_X86_REG_ESI)-base)
                elif pc in (0x0045C783, 0x0046024A):
                    faces.append(machine.reg_read(UC_X86_REG_ESI)-base)
            stats = runner.run(0x0045A8B0, 0x00460266, observe)
            expected = [g["offset"] for g in groups]+[terminator]
            expected_faces = [f["offset"] for g in groups for f in g["faces"]]
            b.p.require(visited == expected and faces == expected_faces, "mesh stream disagrees with original traversal")
            rows.append({"section": section, "record": ref.record_index, "groups": len(groups),
                         "faces": len(faces), "terminator": terminator, "execution": stats})
    return rows


def rotated_geometry(dat, text):
    """Use the original Euler builder and its pinned on-disc sine table.

    All matrix entries are signed shorts. Instances selecting another runtime
    matrix are excluded only when even the full signed-short bound misses the
    footprint. No camera/animation matrix is guessed.
    """
    import pefile
    raw = b.p.DEFAULT_BINARY.read_bytes()
    b.p.require(digest(raw) == b.p.BINARY_SHA256, "rotation executable hash mismatch")
    pe = pefile.PE(data=raw, fast_load=True)
    table = pe.get_data(0xC2100, 8192)
    b.p.require(len(table) == 8192 and struct.unpack_from("<h", table, 2048)[0] == 16384, "sine-table locator changed")
    cpu = b.p.machine(text)
    cpu.mem_write(0x004C2100, table)
    runner = b.retail.RetailProbe.__new__(b.retail.RetailProbe)
    runner.cpu = cpu
    transformed, excluded, receipts = {}, [], []
    for section in ("primary", "secondary"):
        for ref in dat.static_mesh_references(section):
            rotation = struct.unpack_from("<3h", dat.data, ref.object_offset+12)
            selector = dat.data[ref.object_offset+19] & 31
            if rotation == (0, 0, 0) and not selector:
                continue
            key = (section, ref.record_index)
            origin = struct.unpack_from("<3i", dat.data, ref.object_offset)
            local = [(v.component_00, v.component_02, v.component_04) for v in ref.payload.vertices]
            if selector:
                radius = 8*max(sum(map(abs, v)) for v in local)+2
                separated = (origin[0]+radius < 5511-32 or origin[0]-radius > 6893+32
                             or origin[2]+radius < 15109-32 or origin[2]-radius > 16494+32)
                b.p.require(separated, "runtime-selected matrix can reach the target footprint")
                excluded.append(key)
                receipts.append({"section": section, "record": ref.record_index, "runtime_matrix_selector": selector,
                                 "origin": origin, "signed_short_matrix_radius_bound": radius, "excluded": True})
                continue
            b.p.put(cpu, b.p.FIXTURE, "3h", *rotation)
            cpu.reg_write(UC_X86_REG_ESP, b.p.STACK+0x8000)
            b.p.put(cpu, b.p.STACK+0x8000, "3I", b.p.STOP, b.p.FIXTURE, b.p.FIXTURE+64)
            stats = runner.run(0x00463C80, b.p.STOP)
            matrix = b.p.get(cpu, b.p.FIXTURE+64, "9h")
            # Row layout is copied by 004636C0 and consumed at 00463F17..4B.
            # Integer truncation is at most one stored unit from the rational
            # product; the census also retains a 32-unit correspondence margin.
            def coordinate(i, v):
                value = sum(matrix[i*3+j]*v[j] for j in range(3))
                return origin[i]+(abs(value)//4096)*(1 if value >= 0 else -1)
            transformed[key] = [tuple(coordinate(i, v) for i in range(3)) for v in local]
            receipts.append({"section": section, "record": ref.record_index, "rotation": rotation,
                             "matrix": matrix, "origin": origin, "execution": stats})
    return transformed, excluded, {"table_address": "0x004c2100", "table_sha256": digest(table), "instances": receipts}


def report():
    retail, rigid, stitched, raw_dat, edited_dat, cells, edits, visual_edits = fixture()
    text = b.p.load_text(b.p.DEFAULT_BINARY)
    census = boundary_census(cells)
    target = [c for c in cells if c.source == 99 and c.group == 47640]
    transformed, excluded, rotation_receipts = rotated_geometry(LevelDat.parse(raw_dat), text)
    render = render_census(LevelDat.parse(raw_dat), [c.footprint for c in target], transformed=transformed, excluded=excluded)
    render["rotation_evidence"] = rotation_receipts
    b.p.require(not render["unresolved_rotated_references"], "rotated static geometry requires an explicit transform discriminator")
    streams = {}
    for level, dat in (("level01", LevelDat.parse(raw_dat)),
                       ("level03", LevelDat.from_path(b.retail.SOURCE_ROOT / "CD/LEVEL03/LEVEL.DAT"))):
        streams[level] = {"sha256": dat.sha256, "meshes": stream_instruction_audit(dat, text)}
    wide = bytearray(rigid.data)
    for cell in target:
        struct.pack_into("<2b", wide, cell.offset+28, -16, 32)
    arms = {}
    for name, terrain in (("retail", retail), ("rigid", rigid), ("rigid_wide_y_bounds", TerrainAll.parse(bytes(wide))), ("stitched", stitched)):
        print("measuring "+name, file=sys.stderr, flush=True)
        probe = Probe(terrain, text)
        # Candidate seed follows its actual surface, retaining the retail X/Z.
        if name == "stitched":
            landing = probe.land(197091, 492897)
            legs = []
            for label, count, delta in (("forward", 35, (-900, 512, 700)), ("return", 35, (900, 512, -700)), ("settle", 15, (0, 512, 0))):
                steps = [probe.step(delta) for _ in range(count)]
                legs.append({"label": label, "steps": steps, **summary(steps)})
            route = {"landing": landing, "legs": legs}
        else:
            route = return_route(probe, rigid=name.startswith("rigid"))
        crossings = []
        local = {(c.source, c.offset): c for c in floor_cells(terrain)}
        if name != "rigid_wide_y_bounds":
            for edge in census["boundaries"]:
                b.p.require(len(edge["full_edge_neighbors"]) == 1, "boundary lacks exactly one full-edge neighbor")
                own = edge["owner"]; nei = edge["full_edge_neighbors"][0]
                owner = local[(own["source_record"], own["file_offset"])]
                neighbor = local[(nei["source_record"], nei["file_offset"])]
                for isolated in (False, True):
                    probe.floor_only = isolated
                    for direction in ("outward", "inward"):
                        crossings.append(crossing(probe, edge["edge_xz_stored"], owner, neighbor, direction))
            probe.floor_only = False
        landing_cases = []
        if name == "stitched":
            for cell in local.values():
                if cell.offset not in EXPECTED:
                    continue
                x, z = (round(sum(v[i] for v in cell.vertices)*32/3) for i in (0, 2))
                landing = probe.land(x, z, start_y=round(cell_plane(cell, x/32, z/32)*32)+3200-1024)
                steps = [probe.step((0, -1800, 0))]+[probe.step((0, y, 0)) for y in (-1200, -600, 0, 600, 1200, 1800, 1200, 600)]+[probe.step((0, 256, 0)) for _ in range(12)]
                landing_cases.append({"cell": cell.offset, "landing": landing, "steps": steps,
                                      "scope": "landing and grounded normal-impulse control; not a jump-input model", **summary(steps)})
        arms[name] = {"terrain_sha256": digest(terrain.data), "return_route": route,
                      "boundary_crossings": crossings, "landing_and_departure": landing_cases}
    return {"experiment": EXPERIMENT, "scope": "offline original PC instructions, synthetic position/motion; runtime separate",
            "binary_sha256": b.p.BINARY_SHA256, "census": census, "render_census": render,
            "mesh_stream_original_instruction_audit": streams,
            "normal_reconstruction": [{"cell": c.offset, "original": struct.unpack_from("<3h", c.raw), "reconstructed": normal(c.vertices)} for c in cells if c.offset in EXPECTED or c.group == 47640],
            "fixture": {"corner_stored": VERTEX, "displacement_stored": DY, "collision_edits": edits,
                        "visual_edits": visual_edits, "terrain_sha256": digest(stitched.data), "level_dat_sha256": digest(edited_dat),
                        "retail_level_dat_sha256": digest(raw_dat)}, "arms": arms,
            "provenance": {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in
                (Path(__file__), ROOT / "reimplementation/ablpc/terrain_floor_patch.py", Path(control.__file__),
                 Path(control.a.__file__), Path(b.__file__), Path(b.retail.__file__))}}


def write_fixture(directory):
    target = Path(directory).resolve()
    if not target.is_relative_to((ROOT / "work/copies").resolve()):
        raise ValueError("authored assets must stay under work/copies")
    _, _, stitched, _, dat, _, _, _ = fixture()
    target.mkdir(parents=False, exist_ok=False)
    (target / "TERRAIN.ALL").write_bytes(stitched.data)
    (target / "LEVEL.DAT").write_bytes(dat)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = report()
    if args.write_fixture:
        write_fixture(args.write_fixture)
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.report:
        with args.report.open("x") as output:
            output.write(encoded)
    else:
        print(encoded, end="")
