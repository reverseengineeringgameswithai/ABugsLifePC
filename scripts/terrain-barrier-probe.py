#!/usr/bin/env python3
"""EXP-20260904-003: barrier grammar and original grounded movement.

Reuse EXP-002 loading without changing its source or report. This extension
adds a read-only barrier parser, collector comparisons and landing-seeded
grounded cases. No collision writer or live game execution is provided.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_barriers import BarrierPayload, MAGIC, SENTINEL

spec = importlib.util.spec_from_file_location("retail_reference", ROOT / "scripts/terrain-retail-probe.py")
retail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retail)
p = retail.p
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESI, UC_X86_REG_ESP

COLLECTION_END = 0x004AB740
CONTACT = 0x007F3D68


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus() -> list[dict]:
    result = []
    for path in sorted((retail.SOURCE_ROOT / "CD").glob("LEVEL*/*.ALL")):
        if path.name not in ("TERRAIN.ALL", "TERR1.ALL"):
            continue
        terrain = TerrainAll.from_path(path)
        rows = []
        for record in terrain.records:
            if record.field_10 != 0x101:
                continue
            strip = BarrierPayload.from_terrain(terrain, record.index)
            rows.append({
                "source_record": record.index, "payload_offset": strip.offset,
                "payload_size": len(strip.raw), "segments": strip.segment_count,
                "unknown_06": strip.unknown_06, "trailer_size": len(strip.trailer),
                "bounded_blocks": sum(b.bounds is not None for b in strip.blocks),
                "sentinel_blocks": sum(b.bounds is None for b in strip.blocks),
                "bounds_cover_points": all(strip.bounds_cover_points(b) for b in strip.blocks),
            })
        result.append({"path": str(path.relative_to(ROOT)), "sha256": digest(path), "strips": rows})
    return result


def predicted_segments(strips: list[tuple[int, BarrierPayload]], x: int, z: int,
                       delta: tuple[int, int, int]) -> list[int]:
    """Bounded test oracle built from decoded geometry, not a movement solver.

    Strips are already in list order. Match the native padded query window,
    then intersect endpoint ranges and take the first sixteen passing segments.
    Fixed experiment coordinates keep all additions/products nonoverflowing.
    """
    p.require(sum(d*d for d in delta) <= 0x7FFFFFFF, "query velocity outside nonoverflowing oracle scope")
    radius = math.isqrt(sum(d*d for d in delta)) + 0x1880
    p.require(abs(x) + radius < 0x7FFFFFFF and abs(z) + radius < 0x7FFFFFFF,
              "query position outside nonoverflowing oracle scope")
    trunc32 = lambda value: value // 32 if value >= 0 else -((-value) // 32)
    low_x, high_x = trunc32(x-radius), trunc32(x+radius)
    low_z, high_z = trunc32(z-radius), trunc32(z+radius)
    padding = (radius+15)//16
    selected = []
    for base, strip in strips:
        for block in strip.blocks:
            if block.bounds is not None:
                minimum_x, span_x, minimum_z, span_z = block.bounds
                if not (minimum_x <= high_x < minimum_x+span_x+padding
                        and minimum_z <= high_z < minimum_z+span_z+padding):
                    continue
            for index in range(block.first_segment, block.first_segment+block.segment_count):
                a, b = strip.points[index:index+2]
                if (min(a.x,b.x) <= high_x and max(a.x,b.x) >= low_x
                        and min(a.z,b.z) <= high_z and max(a.z,b.z) >= low_z):
                    selected.append(base + a.offset)
                    if len(selected) == 16:
                        return selected
    return selected


class BarrierProbe:
    def __init__(self, level: str, text):
        self.ref = retail.RetailProbe(level, text)
        self.cpu = self.ref.cpu
        # Loader prepends each high-kind source; follow its actual linked list
        # and bind each head to a parsed source record. No guessed list order.
        self.strips = []
        pointer = p.get(self.cpu, 0x007F3D3C, "I")[0]
        seen = set()
        while pointer:
            p.require(pointer not in seen, "cyclic barrier list")
            seen.add(pointer)
            where = self.ref.locate(pointer)
            source_index = 0 if where["source"] == level else 1
            source = self.ref.sources[source_index]
            strip = BarrierPayload.from_terrain(source, where["source_record"])
            base = retail.SOURCE_BASES[source_index]
            p.require(pointer == base+strip.offset+4, "unexpected linked-list head offset")
            self.strips.append((base, strip))
            pointer = p.get(self.cpu, pointer-4, "I")[0]

    def reset(self):
        self.cpu.mem_write(retail.IMAGE[0], self.ref.baseline)
        for base, raw in self.ref.scratch_baseline.items():
            self.cpu.mem_write(base, raw)
        self.cpu.context_restore(self.ref.baseline_context)

    def clear_triangles(self):
        for index in range(self.ref.loaded_count):
            p.put(self.cpu, p.DESCRIPTORS + index*48 + 44, "H", 0)

    def collect(self, x: int, z: int, delta: tuple[int, int, int], *, synthetic=None) -> dict:
        self.reset()
        self.clear_triangles()  # isolate the segment collector; no response runs
        strips = self.strips
        if synthetic is not None:
            raw = synthetic
            strip = BarrierPayload.parse(raw)
            base = p.FIXTURE+0x1000
            p.require(len(raw) < 0xE000, "synthetic strip exceeds scratch capacity")
            self.cpu.mem_write(base, raw)
            p.put(self.cpu, base, "I", 0)  # explicitly seeded one-node runtime list
            p.put(self.cpu, 0x007F3D3C, "I", base+4)
            strips = [(base, strip)]
        predicted = predicted_segments(strips, x, z, delta)
        p.put(self.cpu, retail.POSITION, "4i", x, -2_000_000, z, 0)
        p.put(self.cpu, retail.VELOCITY, "4i", *delta, 0)
        p.put(self.cpu, retail.FLAGS, "I", 0)
        admitted = []

        def observe(cpu, address):
            if address == 0x004AB6CA:
                admitted.append(cpu.reg_read(UC_X86_REG_ECX)-8)

        stack = p.STACK+0x20000
        self.cpu.reg_write(UC_X86_REG_ESP, stack)
        p.put(self.cpu, stack, "5I", p.STOP, retail.POSITION, retail.VELOCITY, retail.FLAGS, 0)
        stats = self.ref.run(0x004AB1A0, COLLECTION_END, observe)
        vertex_count = p.get(self.cpu, 0x007FC8E8, "i")[0]
        p.require(admitted == predicted, "decoded barrier admission disagrees with original ordered collection")
        p.require(vertex_count == len(admitted)*2 <= 32, "segment capacity/count mismatch")
        for i, pointer in enumerate(admitted):
            p.require(bytes(self.cpu.mem_read(pointer,24)) == bytes(self.cpu.mem_read(0x007F2A28+i*24,24)),
                      "native candidate copy differs from its source")
        p.require(self.ref.source_hashes() == self.ref.loaded_source_hashes, "collector modified retail payloads")
        locators = ([{"synthetic_offset": ptr-(p.FIXTURE+0x1000)} for ptr in admitted]
                    if synthetic is not None else [self.ref.locate(ptr) for ptr in admitted])
        return {"x": x, "z": z, "delta": delta, "selected": locators,
                "ordered_admission_matches": True, "execution": stats}

    def state(self) -> dict:
        index, pointer = p.get(self.cpu, CONTACT, "2I")
        return {"position": list(p.get(self.cpu, retail.POSITION, "3i")),
                "velocity": list(p.get(self.cpu, retail.VELOCITY, "3i")),
                "flags": list(p.get(self.cpu, retail.FLAGS, "2B")),
                "contact_descriptor": index,
                "contact_cell": self.ref.locate(pointer) if pointer else None}

    def step(self, delta: tuple[int, int, int]) -> dict:
        before = self.state()
        p.put(self.cpu, retail.VELOCITY, "4i", *delta, 0)
        returns, triangle_updates, segment_updates = [], [], []

        def observe(cpu, address):
            if address in (0x004AB80D,0x004AB823,0x004AB843):
                returns.append({"return_site": f"0x{address:08x}", "eax": cpu.reg_read(UC_X86_REG_EAX)})
            elif address in (0x004AA715,0x004A9DF3):
                triangle_updates.append({"update_site":f"0x{address:08x}",
                                         **self.ref.locate(cpu.reg_read(UC_X86_REG_ESI))})
            elif address == 0x004A9787:
                segment_updates.append((cpu.reg_read(UC_X86_REG_ESI)-8-0x007F2A28)//24)

        stats = self.ref.call(0x004AB1A0,(retail.POSITION,retail.VELOCITY,retail.FLAGS,0),observe)
        p.require(self.ref.source_hashes() == self.ref.loaded_source_hashes, "movement modified retail payloads")
        return {"before": before, "requested_delta": delta, "after": self.state(),
                "returns": returns, "triangle_updates": triangle_updates,
                "segment_updates": segment_updates, "execution": stats}

    def grounded_case(self, surface: str, control: str) -> dict:
        p.require(self.ref.level == "level01", "grounded fixtures require Level01")
        starts = {
            "flat": (-176384, -83168+3200-1024, -342006),
            "barrier": (110544, -124140+3200-1024, -129568),
            "steep": (-9611, -91812+3200-1024, 251232),
        }
        deltas = {"flat": (256,0,0), "barrier": (0,0,-2048), "steep": (2048,0,0)}
        p.require(surface in starts, "unknown grounded surface")
        p.require(control in ("normal","without_obstacle","moving_away","normal_impulse","clear_ground_flag"),
                  "unknown grounded control")
        p.require(not (surface == "flat" and control == "without_obstacle"), "no obstacle in flat fixture")
        self.reset()
        p.put(self.cpu, retail.POSITION, "4i", *starts[surface],0)
        p.put(self.cpu, retail.FLAGS, "I", 0)
        landing = self.step((0,2048,0))
        p.require(landing["after"]["flags"] == [1,1], "original landing did not establish grounded state")
        delta = deltas[surface]
        if control == "without_obstacle":
            if surface == "barrier":
                p.put(self.cpu,0x007F3D3C,"I",0)
            else:
                p.put(self.cpu,p.DESCRIPTORS+87*48+44,"H",0)
        elif control == "moving_away":
            delta = tuple(-d for d in delta)
        elif control in ("normal_impulse","clear_ground_flag"):
            p.require(surface == "flat", "normal-impulse controls require flat floor")
            delta = (0,-2048,0)
            if control == "clear_ground_flag":
                p.put(self.cpu,retail.FLAGS+1,"B",0)
        movement = self.step(delta)
        return {"surface":surface,"control":control,"landing":landing,"movement":movement}


def fixed_strip(segment_count: int) -> bytes:
    """Hand-packed synthetic test strip; never emitted as a game file.

    All segments overlap the origin query, allowing block/remainder and
    sixteen-pair capacity tests. Only the fixed experiment sizes are allowed.
    """
    p.require(segment_count in (4,16,17,32,33), "unsupported synthetic fixture size")
    points = [[i%2,0,i%3] for i in range(segment_count+1)]
    for first in range(0,segment_count,16):
        if segment_count-first < 16:
            points[first][1] = SENTINEL
        else:
            for j,value in enumerate((0,1,0,2)):
                points[first+j][1] = value
    return struct.pack("<IHH",MAGIC,segment_count,0xBEEF)+b"".join(struct.pack("<3i",*v) for v in points)


def report() -> dict:
    text = p.load_text(p.DEFAULT_BINARY)
    probes = [BarrierProbe(level,text) for level in ("level01","level03")]
    queries = []
    for probe in probes:
        for _,strip in probe.strips:
            for index in sorted({0,strip.segment_count//2,strip.segment_count-1}):
                a,b = strip.points[index:index+2]
                for delta in ((0,0,0),(2048,0,0),(0,0,-16000)):
                    queries.append({"level":probe.ref.level,"strip_offset":strip.offset,"segment":index,
                                    **probe.collect((a.x+b.x)*16,(a.z+b.z)*16,delta)})
    synthetic = [{"segments":n,**probes[0].collect(0,0,(0,0,0),synthetic=fixed_strip(n))}
                 for n in (4,16,17,32,33)]
    movements = [probes[0].grounded_case(surface,control)
                 for surface,controls in (("flat",("normal","moving_away","normal_impulse","clear_ground_flag")),
                    ("barrier",("normal","without_obstacle","moving_away")),
                    ("steep",("normal","without_obstacle","moving_away"))) for control in controls]
    files = corpus()
    rows = [row for file in files for row in file["strips"]]
    return {
        "experiment":"EXP-20260904-003","binary_sha256":p.BINARY_SHA256,
        "unicorn_version":importlib.metadata.version("unicorn"),"python_version":sys.version,
        "provenance":{str(path.relative_to(ROOT)):digest(path) for path in
            (Path(__file__),Path(retail.__file__),Path(p.__file__),
             ROOT/"reimplementation/ablpc/terrain_barriers.py",ROOT/"reimplementation/ablpc/terrain_all.py",
             ROOT/"reports/terrain/EXP-20260904-002.json")},
        "scope":"offline original instructions; observed canonical barrier grammar; landing-seeded synthetic movement; no game or writer",
        "corpus":files,"totals":{"files":len(files),"strips":len(rows),
            "segments":sum(row["segments"] for row in rows),
            "bounded_blocks":sum(row["bounded_blocks"] for row in rows),
            "sentinel_blocks":sum(row["sentinel_blocks"] for row in rows)},
        "retail_collection":queries,"synthetic_collection":synthetic,"grounded_movement":movements,
    }


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(report(),indent=2,sort_keys=True))
