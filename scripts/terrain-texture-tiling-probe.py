#!/usr/bin/env python3
"""Run the original PC DAT relocator offline, without touching a live process."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.level_dat import LevelDat

EXE_SHA256 = "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
BASE = 0x10000000


def relocate(image, dat):
    import pefile
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP
    if hashlib.sha256(image).hexdigest() != EXE_SHA256:
        raise ValueError("Expected authoritative retail PC executable")
    pe = pefile.PE(data=image)
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    mapped = pe.get_memory_mapped_image()
    uc.mem_map(pe.OPTIONAL_HEADER.ImageBase, (pe.OPTIONAL_HEADER.SizeOfImage + 4095) & ~4095)
    uc.mem_write(pe.OPTIONAL_HEADER.ImageBase, mapped)
    uc.mem_map(BASE, (len(dat)+4095) & ~4095)
    uc.mem_write(BASE, dat)
    uc.mem_map(0x30000000, 0x10000)
    stack, stop = 0x3000ff00, 0x3000fff0
    uc.mem_write(stack, struct.pack("<3I", stop, 0, len(dat)))
    uc.reg_write(UC_X86_REG_ESP, stack)
    uc.mem_write(0x5ba240, struct.pack("<I", BASE))
    uc.mem_write(0x59f7f0, struct.pack("<H", 2))
    uc.emu_start(0x44bb70, stop, count=2_000_000)
    if uc.reg_read(UC_X86_REG_EIP) != stop:
        raise RuntimeError("Original relocator exceeded bounded instruction count")
    return bytes(uc.mem_read(BASE, len(dat))), {
        "trailing_data_pointer": struct.unpack("<I", uc.mem_read(0x5b7100, 4))[0],
        "trailing_plus_118_pointer": struct.unpack("<I", uc.mem_read(0x63e87c, 4))[0],
        "trailer_table_sha256": hashlib.sha256(uc.mem_read(0x5ba140, 256)).hexdigest(),
        "return_address": stop,
    }


def compare(image, source, candidate, geometry, stream_size):
    before, globals_before = relocate(image, source)
    after, globals_after = relocate(image, candidate)
    ref = LevelDat.parse(source).static_mesh_reference("primary", 160)
    pointer = ref.object_offset + 20
    checks = {
        "trailing_globals_identical": globals_before == globals_after,
        "old_prefix_before_pointer_identical": before[:pointer] == after[:pointer],
        "old_prefix_after_pointer_identical": before[pointer+4:-4] == after[pointer+4:len(source)-4],
        "new_geometry_pointer_correct": struct.unpack_from("<I", after, pointer)[0] == BASE + geometry,
        "new_mesh_loaded_exactly": after[geometry:geometry+stream_size] == candidate[geometry:geometry+stream_size],
        "trailing_data_pointer_correct": globals_after["trailing_data_pointer"] == BASE + len(source) - struct.unpack_from("<i", source, len(source)-4)[0],
    }
    return {"checks": checks, "passed": all(checks.values()), "source_globals": globals_before, "candidate_globals": globals_after,
            "pc_executable_sha256": EXE_SHA256, "entry": "0044bb70", "model": "Original x86 instructions under Unicorn; offline synthetic memory, no live process access",
            "source_dat_sha256": hashlib.sha256(source).hexdigest(), "candidate_dat_sha256": hashlib.sha256(candidate).hexdigest(),
            "limitations": "Proves bounded relocation, not cold file loading, visible textures, performance, movement or all-view occlusion."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    args = parser.parse_args()
    fixture = args.fixture.resolve()
    if not fixture.is_relative_to((ROOT / "work/copies").resolve()):
        parser.error("Fixture must be under work/copies")
    meta = json.loads((fixture / "fixture.json").read_text())
    source = (ROOT / "work/copies/EXP-20260905-005/material-fixture/LEVEL.DAT").read_bytes()
    candidate = (fixture / "LEVEL.DAT").read_bytes()
    image = (ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe").read_bytes()
    result = compare(image, source, candidate, meta["mesh160_geometry_offset"], meta["mesh160_replaced_prefix_bytes"])
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
