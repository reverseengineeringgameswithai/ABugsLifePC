#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pefile

parser = argparse.ArgumentParser()
parser.add_argument("executable", type=Path)
args = parser.parse_args()
pe = pefile.PE(str(args.executable), fast_load=False)

machine_names = {
    0x14C: "i386",
    0x8664: "AMD64",
    0x1C0: "ARM",
    0xAA64: "ARM64",
}
imports = []
for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []):
    imports.append({
        "dll": entry.dll.decode("utf-8", "replace"),
        "symbols": [
            {
                "name": symbol.name.decode("utf-8", "replace") if symbol.name else None,
                "ordinal": symbol.ordinal,
                "address": hex(symbol.address),
            }
            for symbol in entry.imports
        ],
    })
exports = []
if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
    for symbol in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        exports.append({
            "name": symbol.name.decode("utf-8", "replace") if symbol.name else None,
            "ordinal": symbol.ordinal,
            "rva": hex(symbol.address),
        })

resources = []
if hasattr(pe, "DIRECTORY_ENTRY_RESOURCE"):
    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if entry.name:
            name = str(entry.name)
        else:
            name = pefile.RESOURCE_TYPE.get(entry.struct.Id, str(entry.struct.Id))
        resources.append(name)

pdb_paths = []
for debug in getattr(pe, "DIRECTORY_ENTRY_DEBUG", []):
    try:
        data = pe.get_data(debug.struct.AddressOfRawData, debug.struct.SizeOfData)
        if data.startswith(b"RSDS") and b"\0" in data[24:]:
            pdb_paths.append(data[24:].split(b"\0", 1)[0].decode("utf-8", "replace"))
    except Exception:
        pass

report = {
    "path": str(args.executable.resolve()),
    "machine": {
        "value": hex(pe.FILE_HEADER.Machine),
        "name": machine_names.get(pe.FILE_HEADER.Machine, "unknown"),
    },
    "timestamp": pe.FILE_HEADER.TimeDateStamp,
    "characteristics": hex(pe.FILE_HEADER.Characteristics),
    "entry_point_rva": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
    "entry_point_va": hex(pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint),
    "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
    "subsystem": pe.OPTIONAL_HEADER.Subsystem,
    "linker_version": f"{pe.OPTIONAL_HEADER.MajorLinkerVersion}.{pe.OPTIONAL_HEADER.MinorLinkerVersion}",
    "sections": [
        {
            "name": section.Name.rstrip(b"\0").decode("ascii", "replace"),
            "virtual_address": hex(section.VirtualAddress),
            "virtual_size": section.Misc_VirtualSize,
            "raw_offset": hex(section.PointerToRawData),
            "raw_size": section.SizeOfRawData,
            "characteristics": hex(section.Characteristics),
        }
        for section in pe.sections
    ],
    "imports": imports,
    "exports": exports,
    "resource_types": resources,
    "pdb_paths": pdb_paths,
}
print(json.dumps(report, indent=2, sort_keys=True))
