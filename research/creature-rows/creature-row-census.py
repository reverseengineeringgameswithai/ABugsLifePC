#!/usr/bin/env python3
"""KU-069 census: the creature-row bytes the code uses as unbounded indexes.

Usage: .venv/bin/python research/creature-rows/creature-row-census.py [--cd DIR] [--exe EXE] [--out JSON]

Reads the hash-checked retail RAW and DAT of every engine (1..17) and the
retail executable, then reports, for each type-0x23 row, the bytes that
index a table without a bound check (EXP-20260816-172, KU-069):

- +0x0C type      -> byte [type+0x4C881F], byte [type*8+0x599CA8]  (0x0041C468/0x0041C476)
- +0x0D script    -> dword [script*4+0x4C83F0]                     (0x0041BD45)
- +0x0E/+0x0F     -> dword [byte*4+0x5C5860], picked by bit 3 of record +0x5C
                     (opcode 4 at 0x0041DDCD, opcode 10 at 0x0041DEDD)

For bit-0x20 rows the initializer first rewrites +0x0E = +0x0F & 0x0F
(0x0041BE1F-0x0041BE25). Opcode 10 with a nonzero operand seeds the list
index +0x5E from +0x0F (0x0041DEC1); opcode 4 wraps at the list count
(0x0041DDF7), opcode 10 does not check it.

The DAT side models 0x0044BB70: each top record writes slot |type|
(0x0044BCA9, negative types at 0x0044BC8B), a later record overwrites an
earlier one, and nothing bounds |type|.

The only call to the interpreter 0x0041DC60 is 0x0041EE9F (through thunk
0x004017F8), on the arm 0x0041EDA2 takes when bit 0x20 is clear, so a
bit-0x20 row never runs its script. With bit 0x20 clear, 0x0041EE89 runs it
when bit 0x0001 is set (on screen this frame, 0x00456640), when +0x11 is
not 0x64, or for type 15.

Static census only: opcode 12 can change +0x5C at run time, so the
selected byte is the one the initial flags pick unless a script toggles
bit 3 (reported per script; none does).
"""
import argparse
import json
import struct
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc import original_levels as ol  # noqa: E402
from ablpc.level_dat import LevelDat  # noqa: E402
from ablpc.level_raw import packets  # noqa: E402

SCRIPT_TABLE = 0x004C83F0
SCRIPT_COUNT = 40
POINTER_SLOTS = 64          # 0x00467207-0x00467215 zeroes 64 dwords
TYPE_TABLE = 0x004C881F     # boolean table indexed by the raw type byte
TYPE_TABLE_EXAMINED = 48    # EXP-20260816-172 3.3: extent not established
TYPE_DESTINATION_SLOTS = 64  # 0x200 bytes at 0x00599CA8, stride 8
# Instruction sizes (EXP-20260816-172 6.1); blocking opcodes take 2.
SIZE = {-1: 4, 0: 2, 1: 4, 2: 6, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 4, 9: 2,
        10: 4, 11: 4, 12: 6, 13: 6, 14: 4, 15: 4, 16: 4, 17: 2, 18: 2,
        19: 4, 20: 2, 21: 2, 22: 6, 23: 4, 24: 2}
DEFAULT_CD = ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD'
DEFAULT_EXE = ROOT/'work/copies/BUGS_PC-disc/bugs.exe'
SECTIONS = ((0x401000, 0xbe765, 0x400), (0x4c0000, 0xe88, 0xbec00), (0x4c1000, 0x2c400, 0xbfc00))


def file_offset(va):
    for vma, size, fo in SECTIONS:
        if vma <= va < vma+size:
            return fo+(va-vma)
    raise ValueError(f'VA {va:#x} outside the mapped sections')


def decode_scripts(exe):
    ptrs = struct.unpack_from('<40I', exe, file_offset(SCRIPT_TABLE))
    ends = ptrs[1:]+(SCRIPT_TABLE,)
    scripts = []
    for index, (start, end) in enumerate(zip(ptrs, ends)):
        va, ops = start, []
        while va < end:
            op = struct.unpack_from('<h', exe, file_offset(va))[0]
            if op not in SIZE:
                raise ValueError(f'script {index}: opcode {op} at {va:#x}')
            n = (SIZE[op]-2)//2
            ops.append((va, op, struct.unpack_from(f'<{n}h', exe, file_offset(va)+2) if n else ()))
            va += SIZE[op]
        if va != end:
            raise ValueError(f'script {index} misaligned at {va:#x}')
        bit3 = sorted({('clears' if not a & 8 else 'keeps') + ('+sets' if o & 8 else '')
                       for _, op, (a, o) in ((v, p, x) for v, p, x in ops if p == 12)})
        scripts.append(dict(index=index, va=f'0x{start:08X}', instructions=len(ops),
                            opcodes=sorted({op for _, op, _ in ops}),
                            op4=sum(op == 4 for _, op, _ in ops),
                            op10=[x[0] for _, op, x in ops if op == 10],
                            op12_bit3=bit3,
                            op13_sequences=sorted({x[1] for _, op, x in ops if op == 13})))
    return scripts


def pointer_table(dat):
    """Slot -> (record index, offset, count, type) after 0x0044BB70, last write wins."""
    slots = {}
    for record in dat.top_records:
        slot = abs(record.type_id)
        slots[slot] = dict(record=record.index, offset=record.offset, count=record.count,
                           type=record.type_id, form='relative-6' if record.type_id < 0 else
                           ('16-byte' if record.type_id == 0x3F else 'absolute-12'))
    return slots


def census(cd, exe_path):
    exe = exe_path.read_bytes()
    if ol.digest(exe) != ol.RETAIL_EXE:
        raise ValueError('Expected the exact retail PC executable')
    scripts = decode_scripts(exe)
    type_table = exe[file_offset(TYPE_TABLE):file_offset(TYPE_TABLE)+TYPE_TABLE_EXAMINED]
    engines, problems = [], []
    for engine in range(1, 18):
        inputs = ol.read_inputs(cd, engine)
        dat = LevelDat.parse(inputs['dat'])
        slots = pointer_table(dat)
        found = [p for _, _, p in packets(inputs['raw'])[0] if struct.unpack_from('<I', p)[0] == 0x23]
        if len(found) != 1:
            raise ValueError(f'engine {engine}: expected one type-0x23 packet')
        rows = []
        for row in ol.creature_rows(found[0]):
            raw = bytes.fromhex(row['raw_hex'])
            kind, script, e, f, count, x11 = raw[12], raw[13], raw[14], raw[15], raw[16], raw[17]
            flags = struct.unpack_from('<H', raw, 18)[0]
            effective_e = (f & 0x0F) if flags & 0x20 else e
            selector = f if flags & 0x08 else effective_e
            info = scripts[script] if script < SCRIPT_COUNT else None
            vm = ('never' if flags & 0x20 else
                  'on screen only' if x11 == 0x64 and kind != 15 else 'every active frame')
            walks = bool(info and (info['op4'] or info['op10'])) and vm != 'never'
            target = slots.get(selector) if walks else None
            seeded = bool(info and any(info['op10']))
            item = dict(slot=row['slot'], type=kind, script=script, b0e=e, b0f=f, b10=count, b11=x11,
                        flags=f'0x{flags:04X}', bit20=bool(flags & 0x20), bit08=bool(flags & 0x08),
                        vm=vm, selector=selector if walks else None, walks_list=walks)
            if walks:
                item['list'] = target
                if target is None:
                    problems.append(dict(engine=engine, slot=row['slot'], issue='list slot empty',
                                         selector=selector))
                elif seeded and not flags & 0x20 and f >= target['count']:
                    problems.append(dict(engine=engine, slot=row['slot'], issue='opcode 10 start >= count',
                                         start=f, count=target['count']))
            for name, value, limit in (('type', kind, TYPE_DESTINATION_SLOTS), ('script', script, SCRIPT_COUNT)):
                if value >= limit:
                    problems.append(dict(engine=engine, slot=row['slot'], issue=f'{name} {value} >= {limit}'))
            if walks and selector >= POINTER_SLOTS:
                problems.append(dict(engine=engine, slot=row['slot'], issue=f'selector {selector} >= 64'))
            rows.append(item)
        top_types = [r.type_id for r in dat.top_records]
        for t in top_types:
            if abs(t) >= POINTER_SLOTS:
                problems.append(dict(engine=engine, issue=f'DAT top type {t} outside 64 slots'))
        engines.append(dict(engine=engine, title=ol.LEVELS[engine][0], rows=len(rows),
                            dat_top_types=top_types,
                            pointer_slots={str(k): v for k, v in sorted(slots.items())},
                            max=dict(type=max(r['type'] for r in rows), script=max(r['script'] for r in rows),
                                     b0e=max(r['b0e'] for r in rows), b0f=max(r['b0f'] for r in rows)),
                            walkers=[r for r in rows if r['walks_list']],
                            rows_detail=rows))
    all_rows = [r for e in engines for r in e['rows_detail']]
    summary = dict(
        rows=len(all_rows),
        type_range=[min(r['type'] for r in all_rows), max(r['type'] for r in all_rows)],
        script_range=[min(r['script'] for r in all_rows), max(r['script'] for r in all_rows)],
        b0e_range=[min(r['b0e'] for r in all_rows), max(r['b0e'] for r in all_rows)],
        b0f_range=[min(r['b0f'] for r in all_rows), max(r['b0f'] for r in all_rows)],
        vm=dict(Counter(r['vm'] for r in all_rows)),
        walkers=sum(r['walks_list'] for r in all_rows),
        bit08_rows_without_bit20=sum(r['bit08'] and not r['bit20'] for r in all_rows),
        selectors=dict(sorted(Counter(r['selector'] for r in all_rows if r['walks_list']).items())),
        type_table_nonzero_below_48=[i for i, b in enumerate(type_table) if b],
        problems=problems)
    return dict(experiment='EXP-20261018-001', binary_sha256=ol.RETAIL_EXE,
                sources={e: ol.SOURCE_SHA256[e] for e in range(1, 18)},
                summary=summary, scripts=scripts, engines=engines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--cd', type=Path, default=DEFAULT_CD)
    parser.add_argument('--exe', type=Path, default=DEFAULT_EXE)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    report = census(args.cd, args.exe)
    text = json.dumps(report, indent=1)+'\n'
    if args.out:
        args.out.write_text(text)
    print(json.dumps(report['summary'], indent=1))


if __name__ == '__main__':
    main()
