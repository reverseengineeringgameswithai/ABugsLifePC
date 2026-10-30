#!/usr/bin/env python3
"""EXP-005: read-only PC Level01 face/attribute census; no game control."""

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.level_dat import LevelDat

ORIGINAL_SHA = "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"
AUTHORED_SHA = "54d1ae4d96a4d926b806584cc669e791c3f6565688ec4aa491a987b0c2f56aab"


def census(data):
    level = LevelDat.parse(data)
    rows = []
    skipped_rotated = []
    for ref in level.static_mesh_references("primary"):
        origin = struct.unpack_from("<3i", data, ref.object_offset)
        if struct.unpack_from("<3h", data, ref.object_offset + 12) != (0, 0, 0):
            skipped_rotated.append(ref.record_index)
            continue
        payload = ref.payload
        vertices = payload.vertices
        cursor = payload.vertices_offset + 12 * payload.vertex_count
        group = 0
        while True:
            if cursor + 2 > len(data):
                raise ValueError("Group header outside file")
            tag = struct.unpack_from("<H", data, cursor)[0]
            if tag == 0xffff:
                break
            if cursor + 4 > len(data):
                raise ValueError("Group count outside file")
            count = struct.unpack_from("<h", data, cursor + 2)[0]
            arity = 3 if tag & 1 else 4
            end = cursor + 4 + count * arity * 4
            if count < 0 or end > len(data):
                raise ValueError("Impossible primitive count")
            for index in range(count):
                offset = cursor + 4 + index * arity * 4
                refs = struct.unpack_from("<" + "H" * arity, data, offset)
                if any(ref % 12 or ref // 12 >= len(vertices) for ref in refs):
                    raise ValueError("Misaligned or out-of-range vertex reference")
                selected = [vertices[ref // 12] for ref in refs]
                points = [(v.component_00 + origin[0], v.component_02 + origin[1],
                           v.component_04 + origin[2]) for v in selected]
                center = tuple(sum(p[axis] for p in points) / arity for axis in range(3))
                if abs(center[0] - 6160) > 4200 or abs(center[2] - 15400) > 4200:
                    continue
                a = [points[1][i] - points[0][i] for i in range(3)]
                b = [points[2][i] - points[0][i] for i in range(3)]
                normal = (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
                length = math.sqrt(sum(value * value for value in normal))
                ratio = abs(normal[1]) / length if length else None
                kind = "degenerate" if ratio is None else "steep" if ratio < .4 else "floor" if ratio > .85 else "slope"
                words = struct.unpack_from("<" + "H" * arity, data, offset + arity * 2)
                uv = [(word & 255, word >> 8) for word in words]
                rows.append({
                    "record": ref.record_index, "geometry": ref.geometry_offset,
                    "group": group, "face": index, "face_offset": offset,
                    "tag": tag, "page_index": (tag >> 8) & 31,
                    "uv_bytes": uv,
                    "uv64_bin": [min(u for u,v in uv)//64, min(v for u,v in uv)//64,
                                 max(u for u,v in uv)//64, max(v for u,v in uv)//64],
                    "center": center, "geometric_class": kind,
                    "normal_y_fraction": ratio, "points": points,
                    "vertex_offsets": [v.offset for v in selected],
                    "field_08_09_0a": [(v.field_08, v.field_09, v.field_0a) for v in selected],
                })
            cursor = end
            group += 1
            if group > 1000:
                raise ValueError("Unbounded group chain")
    return rows, skipped_rotated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        parser.error("Refusing to overwrite an existing report")
    source_path = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT"
    source = source_path.read_bytes()
    authored_path = ROOT / "work/copies/EXP-20260905-004/fixture/LEVEL.DAT"
    authored = authored_path.read_bytes()
    if hashlib.sha256(source).hexdigest() != ORIGINAL_SHA or hashlib.sha256(authored).hexdigest() != AUTHORED_SHA:
        raise ValueError("Exact original/authored source pair guard failed")
    rows, skipped = census(source)
    authored_rows, _ = census(authored)
    authored_rows = [row for row in authored_rows if row["record"] == 160]
    histogram = Counter((row["geometric_class"], row["page_index"], tuple(row["uv64_bin"])) for row in rows)
    examples = [row for row in rows if (row["record"], row["group"], row["face"]) in [(160, 0, 2), (128, 0, 13)]]
    report = {
        "experiment": "EXP-20260905-005", "status": "static census; exact screenshot identity open",
        "original_dat": {"path": str(source_path.relative_to(ROOT)), "sha256": ORIGINAL_SHA},
        "authored_dat": {"path": str(authored_path.relative_to(ROOT)), "sha256": AUTHORED_SHA},
        "pc_executable_sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
        "selection": {"center_xz_stored": [6160, 15400], "centroid_half_extent": 4200,
                      "steep_abs_normal_y_fraction_below": .4, "floor_fraction_above": .85,
                      "quad_normal": "First three referenced vertices only", "skipped_rotated_records": skipped},
        "original_class_counts": dict(Counter(row["geometric_class"] for row in rows)),
        "page_uv64_histogram": [{"class": key[0], "page": key[1], "uv64_bin": key[2], "count": value}
                                for key, value in sorted(histogram.items())],
        "same_tag_examples": examples,
        "original_faces": rows, "authored_primary160_faces": authored_rows,
        "native_instruction_anchors": {
            "quad_uv_bytes_to_output_uv": ["0x0045D38C", "0x0045D3A7", "0x0045D3A4", "0x0045D3B9"],
            "vertex_plus_8_load": "0x0045D474",
            "three_channel_global_multipliers": ["0x0045D462", "0x0045D49D", "0x0045D4A7"],
            "source_consumer": "FUN_0045A7F0",
        },
        "conclusion": "Selected original steep faces use other page-0 coordinate regions plus varying warm vertex colours; the authored box uses the floor region and uniform neutral channels.",
        "limits": [
            "64-pixel bins are a census grouping, not a claimed native tile metadata structure.",
            "Texture-page pixels have not been extracted or compared; distinct coordinate regions are confirmed, distinct artwork is not yet independently visualized.",
            "Geometric classes are offline selections, not collision classifications or live visibility proofs.",
            "The cropped user screenshot has not been matched to an exact PC mesh face.",
            "No universal wall material or fixed brightness ratio follows.",
        ],
        "next_discriminator": "Identify the original screenshot-facing wall, then compare baseline / original wall UV region only / donor colours only / both in separate file-loaded copies.",
        "pending_candidate": "terrain_wall_shading.py is unapplied and untested; uniform 3/5 shading is not accepted as OG matching.",
        "runtime": "No launch, close, input, memory operation or session modification in this census; user's EXP-004 session preserved.",
        "tests": "No pytest, R2q or full-suite run for this read-only investigation.",
    }
    with args.report.open("x") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps({"report": str(args.report), "original_class_counts": report["original_class_counts"],
                      "same_tag_examples": examples, "authored_face_count": len(authored_rows)}, indent=2))


if __name__ == "__main__":
    main()
