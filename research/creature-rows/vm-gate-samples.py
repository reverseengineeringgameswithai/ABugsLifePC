#!/usr/bin/env python3
"""EXP-20261018-013 arm B: test the creature VM gate against live samples.

Usage: python3 research/creature-rows/vm-gate-samples.py PACKET [--out JSON]

Reads PACKET/drive.jsonl (read-only slot samples from drive.py). For each
pair of consecutive samples in one run (idle1..6, turned1..6), a slot is
"predicted frozen" when, in both samples, it is selected (flag 0x4000) and
off screen (flag 0x0001 clear), its source +0x11 is 100, its type is not 15
and flag 0x20 is clear. The gate at 0x0041EE89 then skips the interpreter,
and with it the tail that moves the slot and advances its animation phase
+0x40 (EXP-20261018-001, EXP-20261018-003). Every other selected slot is
"runs". The pre-registered falsifier is a predicted-frozen slot whose phase,
position, wait or program counter changes between the two samples.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def classify(a, b):
    both = (a['flags'] & b['flags'])
    if not both & 0x4000:
        return 'not selected'
    frozen = (not (a['flags'] | b['flags']) & 0x0001 and a['src11'] == 100 and a['type'] != 15
              and not a['flags'] & 0x20)
    return 'predicted frozen' if frozen else 'runs'


def changed(a, b):
    return [k for k in ('phase', 'pos', 'wait', 'pc') if a[k] != b[k]]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('packet', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in (args.packet/'drive.jsonl').read_text().splitlines()]
    runs = {'idle': [r for r in rows if r['label'].startswith('idle')],
            'turned': [r for r in rows if r['label'].startswith('turned')]}
    pairs, table = [], Counter()
    for name, seq in runs.items():
        for a, b in zip(seq, seq[1:]):
            sa = {s['slot']: s for s in a['sample']['slots']}
            sb = {s['slot']: s for s in b['sample']['slots']}
            for slot in sorted(sa.keys() & sb.keys()):
                cls = classify(sa[slot], sb[slot])
                diff = changed(sa[slot], sb[slot])
                table[(cls, bool(diff))] += 1
                pairs.append(dict(run=name, pair=[a['label'], b['label']], slot=slot, type=sa[slot]['type'],
                                  src11=sa[slot]['src11'], flags=[hex(sa[slot]['flags']), hex(sb[slot]['flags'])],
                                  cls=cls, changed=diff))
    falsifiers = [p for p in pairs if p['cls'] == 'predicted frozen' and p['changed']]
    report = dict(experiment='EXP-20261018-013', packet=str(args.packet), levels=sorted({r['sample']['level'] for r in rows}),
                  counts={f'{c} / {"changed" if d else "unchanged"}': n for (c, d), n in sorted(table.items())},
                  falsifiers=falsifiers,
                  frozen_slots=sorted({(p['slot'], p['type']) for p in pairs if p['cls'] == 'predicted frozen'}),
                  running_slots=sorted({(p['slot'], p['type'], p['src11']) for p in pairs if p['cls'] == 'runs'}),
                  pairs=pairs)
    text = json.dumps(report, indent=1)+'\n'
    if args.out:
        args.out.write_text(text)
    print(json.dumps({k: report[k] for k in ('levels', 'counts', 'falsifiers', 'frozen_slots', 'running_slots')}, indent=1))


if __name__ == '__main__':
    main()
