#!/usr/bin/env python3
"""KU-068: check saved live samples of creature slot +0x70 against the decoded scripts.

Usage: .venv/bin/python research/creature-rows/script-counter-samples.py [--out JSON]

No game is launched. The samples come from two earlier hardware arms:

- EXP-20260913-002 (Dot, Anthill slot 25, script 7): play/, ready/ and
  summit/ dot-*.json, 100 read-only samples each of +0x70 ("script"),
  +0x5E ("cursor") and +0x5C ("flags").
- EXP-20261005-002 (moved taxi bug, Moonlit slot 14, script 23): each
  tough-regulars*/*.jsonl sample whose "boss" is type 18 carries the whole
  0x84-byte slot.

Both arms ran derived executables. The script bodies and table, the
interpreter, the pool initializer, the builder, thunk 0x004017F8 and the
visibility pass are compared byte for byte with retail; the per-frame update
is compared too and its only difference is reported.

Checks: every sampled +0x70 is a decoded instruction start of a shipped
script; for the taxi bug, op4's target +0x34/+0x38/+0x3C equals the image's
list-1 entry at +0x5E shifted left 5 (0x0041DE62-0x0041DE8D).

EXP-20261018-003 adds the taxi bug's motion: horizontal speed |+0x1C, +0x24|
against the cap source +0x1B << 4 (0x0041E458-0x0041E475), vertical
velocity +0x20, and the XZ distance to the target (>> 5, as 0x0041E1AF-
0x0041E1DE computes it) at op 9 and at op 9 + 2, against the arrival
radius source +0x14 << 4. Op 4 copies the old target into home +0x28/+0x30
(0x0041DE09-0x0041DE12), so home should be the previous list row, and the
leash (0x0041E519-0x0041E536) should keep the slot within source +0x16 << 4
of it.
"""
import argparse
import glob
import hashlib
import importlib.util
import json
import math
import struct
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc.level_dat import LevelDat  # noqa: E402

spec = importlib.util.spec_from_file_location('census', Path(__file__).with_name('creature-row-census.py'))
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)

RETAIL = ROOT/'work/copies/BUGS_PC-disc/bugs.exe'
REGIONS = {'scripts and table': (0x4C7D00, 0x4C8490), 'interpreter and dispatch': (0x41DC60, 0x41E914),
           'initializer 0x0041BD10': (0x41BD10, 0x41BE83), 'builder 0x0041C420': (0x41C420, 0x41C5A0),
           'frame update 0x0041EC40': (0x41EC40, 0x41EF00), 'thunk 0x004017F8': (0x4017F8, 0x4017FD),
           'visibility 0x00456640': (0x456640, 0x4567B0), 'sequence table 0x004C8754': (0x4C8754, 0x4C87C4)}
DOT = ROOT/'work/experiments/EXP-20260913-002'
DOT_EXES = {'play': ROOT/'work/copies/EXP-20260913-002-play/bugs.exe',
            'ready': ROOT/'work/copies/EXP-20260913-002-ready/bugs.exe',
            'summit': ROOT/'work/copies/EXP-20260913-002-summit/bugs.exe'}
TAXI = ROOT/'work/experiments/EXP-20261005-002'
TAXI_IMAGE = ROOT/'work/copies/EXP-20261005-002-tough-regulars'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mapped(path):
    """VA -> byte reader over the PE sections (no pefile needed)."""
    data = path.read_bytes()
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    count, opt = struct.unpack_from('<H', data, pe+6)[0], struct.unpack_from('<H', data, pe+20)[0]
    base = struct.unpack_from('<I', data, pe+24+28)[0]
    sections = []
    for i in range(count):
        s = pe+24+opt+40*i
        vsize, rva, rsize, raw = struct.unpack_from('<4I', data, s+8)
        sections.append((base+rva, max(vsize, rsize), raw, rsize))

    def read(start, end):
        out = bytearray()
        for va in range(start, end):
            for vma, size, raw, rsize in sections:
                if vma <= va < vma+size:
                    out.append(data[raw+va-vma] if va-vma < rsize else 0)
                    break
            else:
                raise ValueError(f'VA {va:#x} unmapped in {path}')
        return bytes(out)
    return read


def compare(path):
    retail, derived = mapped(RETAIL), mapped(path)
    out = {}
    for name, (start, end) in REGIONS.items():
        a, b = retail(start, end), derived(start, end)
        out[name] = [f'0x{start+i:08X}' for i in range(end-start) if a[i] != b[i]]
    return out


def starts(scripts, exe):
    """Instruction-start VA -> (script, offset)."""
    found = {}
    ptrs = struct.unpack_from('<40I', exe, census.file_offset(census.SCRIPT_TABLE))
    for index, (start, end) in enumerate(zip(ptrs, ptrs[1:]+(census.SCRIPT_TABLE,))):
        va = start
        while va < end:
            found[va] = (index, va-start)
            va += census.SIZE[struct.unpack_from('<h', exe, census.file_offset(va))[0]]
    return found


def taxi_row():
    """Retail City Entrance slot 0, the taxi bug's donor row (make-boss-test)."""
    inputs = census.ol.read_inputs(census.DEFAULT_CD, 4)
    found = [p for _, _, p in census.packets(inputs['raw'])[0] if struct.unpack_from('<I', p)[0] == 0x23]
    row = found[0][4:4+28]
    return {'+0x14': struct.unpack_from('<h', row, 0x14)[0], '+0x16': struct.unpack_from('<h', row, 0x16)[0],
            '+0x18': row[0x18], '+0x19': row[0x19], '+0x1A': row[0x1A], '+0x1B': row[0x1B],
            'arrival_radius': struct.unpack_from('<h', row, 0x14)[0] << 4, 'speed_cap': row[0x1B] << 4}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    exe = RETAIL.read_bytes()
    if hashlib.sha256(exe).hexdigest() != census.ol.RETAIL_EXE:
        raise ValueError('Expected the exact retail PC executable')
    pcs = starts(census.decode_scripts(exe), exe)
    report = dict(experiment='EXP-20261018-002', binary_sha256=census.ol.RETAIL_EXE, builds={}, dot={}, taxi={})
    for arm, path in DOT_EXES.items():
        report['builds'][f'EXP-20260913-002 {arm}'] = dict(sha256=sha(path), differs=compare(path))
    for arm in ('play', 'ready', 'summit'):
        rows, runs = [], []
        for f in sorted(glob.glob(str(DOT/arm/'dot-*.json'))):
            for s in json.loads(Path(f).read_text()):
                pc = int(s['script'], 16)
                rows.append((pc, s['cursor'], s['flags']))
                key = (f'0x{pc:08X}', s['cursor'], s['flags'])
                if not runs or runs[-1][0] != list(key):
                    runs.append([list(key), 0])
                runs[-1][1] += 1
        report['dot'][arm] = dict(samples=len(rows),
                                  pcs={f'0x{pc:08X}': dict(count=n, script=pcs.get(pc)) for pc, n in
                                       sorted(Counter(r[0] for r in rows).items())},
                                  all_instruction_starts=all(r[0] in pcs for r in rows),
                                  cursors=sorted({r[1] for r in rows}), runs=runs)
    image_exe = TAXI_IMAGE/'bugs.exe'
    report['builds']['EXP-20261005-002 tough-regulars'] = dict(sha256=sha(image_exe), differs=compare(image_exe))
    dat_path = TAXI_IMAGE/'game/PC/BUGS/CD/LEVEL01/LEVEL.DAT'
    dat = dat_path.read_bytes()
    record = [r for r in LevelDat.parse(dat).top_records if r.type_id == 1][-1]
    points = [struct.unpack_from('<3i', dat, record.offset+4+12*i) for i in range(record.count)]
    samples, matches, by_pc, cursors = 0, 0, Counter(), set()
    speeds, vertical, distance = [], Counter(), {'op9': [], 'op9+2': []}
    from_home, home_is_previous = [], 0
    for f in sorted(glob.glob(str(TAXI/'tough-regulars*/*.jsonl'))):
        for line in Path(f).read_text().splitlines():
            boss = (json.loads(line).get('sample') or {}).get('boss')
            if not boss or boss.get('type') != 18:
                continue
            slot = bytes.fromhex(boss['record'])
            pc, cursor = struct.unpack_from('<I', slot, 0x70)[0], struct.unpack_from('<h', slot, 0x5E)[0]
            target = struct.unpack_from('<3i', slot, 0x34)
            samples += 1
            by_pc[pc] += 1
            cursors.add(cursor)
            if 0 <= cursor < len(points) and target == tuple(c << 5 for c in points[cursor]):
                matches += 1
            if boss.get('health', 1) > 0:
                vx, vy, vz = struct.unpack_from('<3i', slot, 0x1C)
                speeds.append(math.hypot(vx, vz))
                vertical[vy] += 1
                pos = struct.unpack_from('<3i', slot, 4)
                gap = math.hypot((pos[0]-target[0]) >> 5, (pos[2]-target[2]) >> 5)
                home = struct.unpack_from('<3i', slot, 0x28)
                from_home.append(math.hypot((pos[0]-home[0]) >> 5, (pos[2]-home[2]) >> 5))
                if 0 < cursor <= len(points) and home[0] == points[cursor-1][0] << 5 and \
                        home[2] == points[cursor-1][2] << 5:
                    home_is_previous += 1
                key = {0x4C80FA: 'op9', 0x4C80FC: 'op9+2'}.get(pc)
                if key:
                    distance[key].append(gap)
    report['taxi'] = dict(samples=samples, dat_sha256=hashlib.sha256(dat).hexdigest(),
                          list1=dict(offset=record.offset, count=record.count),
                          pcs={f'0x{pc:08X}': dict(count=n, script=pcs.get(pc)) for pc, n in sorted(by_pc.items())},
                          all_instruction_starts=all(pc in pcs for pc in by_pc),
                          target_is_list1_at_cursor=matches, cursor_range=[min(cursors), max(cursors)],
                          motion=dict(source_row=taxi_row(), live_samples=len(speeds),
                                      speed=[round(min(speeds)), round(max(speeds))],
                                      vertical_velocity=dict(vertical),
                                      distance_at_op9=[round(min(distance['op9'])), round(max(distance['op9']))],
                                      distance_at_op9_plus_2=[round(min(distance['op9+2'])),
                                                              round(max(distance['op9+2']))],
                                      home_is_previous_row=home_is_previous,
                                      max_distance_from_home=round(max(from_home))))
    text = json.dumps(report, indent=1)+'\n'
    if args.out:
        args.out.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
