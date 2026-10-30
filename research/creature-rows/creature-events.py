#!/usr/bin/env python3
"""EXP-20261018-004: name the events that creature code plays.

Usage: .venv/bin/python research/creature-rows/creature-events.py [--out JSON]

0x004148A0(id, position) reads the 16-byte entry 0x004C6E08 + id*16 for
id >= 0. Its first word s selects the sample:

- s > 0: 0x00419950 / 0x00419990 receive s - 1 and add 1 back, so the
  sample id is s (0x00414A42, 0x00419966);
- s < 0: 0x00419B60 / 0x00419E00 receive -1 - s plus the entry's +2 word
  as a channel key, and add 1 back, so the sample id is -s on a keyed
  channel (0x00414A52, 0x00419BEB);
- s = 0: nothing plays (0x004149E0).

The bank loader 0x0049DF90 stores sample s at 0x007EDF08 + s*24, and the
player 0x0049D820 reads the same slot, so s is the bank sample id that
EXP-20260910-004's native census (reports/audio/EXP-20260910-004-native.json)
maps to a file. Only the event ids that creature code passes are listed.
"""
import argparse
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc import original_levels as ol  # noqa: E402

EXE = ROOT/'work/copies/BUGS_PC-disc/bugs.exe'
AUDIO = ROOT/'reports/audio/EXP-20260910-004-native.json'
TABLE = 0x004C6E08
SECTIONS = ((0x401000, 0xbe765, 0x400), (0x4c0000, 0xe88, 0xbec00), (0x4c1000, 0x2c400, 0xbfc00))
# Event id -> the creature code that passes it (EXP-20261018-004).
CALLERS = {
    0x07: 'badbug/weevil handler 0x0041BEF0, frame 0',
    0x14: 'op-11 subroutine 2 (wasp ring) 0x004287D0',
    0x18: 'op-11 subroutines 1 and 8 (emerge) 0x004288F0, 0x00428990',
    0x19: 'long-legged spider shot 0x0041C3B4',
    0x1A: 'Thumper/Hopper/Thud handler 0x0041C100; grasshopper handler group 1',
    0x26: 'grasshopper and Molt handlers, footstep frames',
    0x28: 'fly/wasp handler 0x0041C160',
    0x2A: 'mosquito handler 0x0041C190 (group 1); dragonfly handler 0x0041C210',
    0x66: 'op-11 subroutine 3 (Tunnels grasshopper) 0x00432A50',
    0x7D: 'acorn handler 0x0041C130',
}


def file_offset(va):
    for vma, size, fo in SECTIONS:
        if vma <= va < vma+size:
            return fo+(va-vma)
    raise ValueError(f'VA {va:#x} outside the mapped sections')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    exe = EXE.read_bytes()
    if ol.digest(exe) != ol.RETAIL_EXE:
        raise ValueError('Expected the exact retail PC executable')
    audio = json.loads(AUDIO.read_text())
    banks = {b['bank']: {f['sample_id']: f['path'] for f in b['files']} for b in audio['banks']}
    level_banks = sorted({b for level in audio['levels'] for b in level['bank']})
    events = []
    for event, caller in CALLERS.items():
        entry = struct.unpack_from('<8h', exe, file_offset(TABLE+event*16))
        word = entry[0]
        sample = word if word > 0 else -word if word < 0 else None
        files = sorted({banks[b].get(sample, '(none)') for b in level_banks}) if sample else []
        events.append(dict(event=f'0x{event:02X}', caller=caller, entry=list(entry),
                           path='keyed channel' if word < 0 else 'one-shot' if word > 0 else 'silent',
                           sample=sample, files_in_level_banks=files))
    report = dict(experiment='EXP-20261018-004', binary_sha256=ol.RETAIL_EXE, table=f'0x{TABLE:08X}',
                  level_banks=level_banks, events=events)
    text = json.dumps(report, indent=1)+'\n'
    if args.out:
        args.out.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
