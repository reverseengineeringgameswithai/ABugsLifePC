#!/usr/bin/env python3
"""EXP-20260910-009: offline PC grain, shared-pickup and nonfatal-hurt voices.

Executes original x86 and native bank selection, never a live game. Geometry,
visual feedback and the final sound-device callback are explicitly stubbed.
"""
import hashlib
import json
from pathlib import Path
import runpy
import struct

ROOT = Path(__file__).resolve().parents[1]
prior = runpy.run_path(str(ROOT/'scripts/probe-flik-events.py'))
Events, STOP, SCRATCH = (prior[k] for k in ('Events', 'STOP', 'SCRATCH'))
RETAIL = prior['baseline']['RETAIL']
PICKUP = [62, 63, 66, 52, 58, 62, 63, 66, 62]
HURT = [67, 68, 77, 78, 81, 67, 68, 77, 67]


class Actions(Events):
    def __init__(self, image, base, random=(0, 0), engine=1):
        super().__init__(image, base, 2)  # Anthill native bank; not Training's bank.
        self.put(self.va(0x861c84), engine)
        self.u.mem_write(SCRATCH, bytes(random))
        self.hook(self.va(0x41a2b0), lambda: self.requests.append(dict(
            cue=self.arg(1)+16, via=0x41a2b0, callsite=self.arg(-1)-self.delta-5)))
        # Visual/HUD feedback only; selection/guards/health and cue translation run.
        for pc in (0x428590, 0x403a10, 0x4039d0, 0x4595e0,
                   0x4a59c0, 0x464be0, 0x43e820):
            self.hook(self.va(pc), self.ret)

    def result(self):
        trace = self.trace()
        trace['requests'] = [dict(q, callsite=None) if q['callsite'] == STOP-self.delta-5 else q
                             for q in trace['requests']]
        return dict(**trace, random_bytes=self.get(self.va(0x599c60))-SCRATCH,
            grain=self.get(self.va(0x59d9b1)) & 255,
            health=struct.unpack('<h', self.u.mem_read(self.va(0x59d9a4), 2))[0],
            last_cue=self.get(self.va(0x572c24)))

    def stored(self, selector, active=True, distance=0):
        table = SCRATCH+0x10000
        self.put(self.va(0x5c595c), table)
        self.u.mem_write(table, struct.pack('<HHiiiBBh', 1, 0, distance, -230, 0,
                                           selector, int(active), 0))
        self.byte(0x599aac, 254)  # Avoid unrelated sparkle RNG consumption.
        assert self.call(0x417720) == STOP
        return self.result()

    def grain(self):
        assert self.call(0x418b90) == STOP
        return self.result()

    def hurt(self, health=2, invulnerability=0, invincibility=0):
        self.word(0x59d9a4, health)
        self.word(0x59d9a2, invulnerability)
        self.word(0x59d98e, invincibility)
        assert self.call(0x41c6c0, 0, 0, SCRATCH+0x20000, 0) == STOP
        return self.result()


def proof(image, base):
    rows = []
    for path in ('helper', 'stored', 'effect'):
        for random in range(16):
            for variant in range(2):
                n = Actions(image, base, (random, variant))
                if path == 'helper': r = n.grain()
                elif path == 'stored': r = n.stored(0x14)
                else: n.pickup(0x14); r = n.result()
                assert r['grain'] == 1, (path, r)
                assert [s['sample_id'] for s in r['samples']] == ([33+variant] if random == 0 else [])
                assert r['random_bytes'] == (2 if random == 0 else 1), (path, r)
                rows.append(dict(event='grain', path=path, random=random, variant=variant, **r))
        for guard in ('training', 'busy', 'state2', 'flag04', 'blocker'):
            n = Actions(image, base)
            if guard == 'training': n.put(n.va(0x861c84), 17)
            elif guard == 'busy': n.hook(n.va(0x41a550), lambda: n.ret(value=1))
            elif guard == 'state2': n.word(0x59a5b0, 2)
            elif guard == 'flag04': n.byte(0x59d9a0, 4)
            else: n.put(n.va(0x572c20), 1)
            if path == 'helper': r = n.grain()
            elif path == 'stored': r = n.stored(0x14)
            else: n.pickup(0x14); r = n.result()
            assert r['grain'] == 1 and not r['samples'], (path, guard, r)
            rows.append(dict(event='grain_guard', path=path, guard=guard, **r))
    # Native stored-record action -> random pool -> filename, not inferred wording.
    for selector in (0x10, 0x11, 0x12, 0x13, 0x20, 0x29, 0x2a, 0x2b):
        for choice in range(8):
            n = Actions(image, base, (choice, 0)); r = n.stored(selector)
            assert [s['sample_id'] for s in r['samples']] == [PICKUP[choice]-15], (selector, choice, r)
            rows.append(dict(event='shared_pickup', selector=selector, choice=choice, **r))
        n = Actions(image, base, engine=17); r = n.stored(selector)
        assert not r['samples'] and r['random_bytes'] == 0, (selector, r)
        rows.append(dict(event='shared_pickup_training', selector=selector, **r))
    for selector in (0x14, 0x10, 0x20, 0x29):
        for guard, kwargs in (('inactive', dict(active=False)), ('distant', dict(distance=100000))):
            n = Actions(image, base); r = n.stored(selector, **kwargs)
            assert not r['samples'] and r['grain'] == 0
            rows.append(dict(event='pickup_overlap_guard', selector=selector, guard=guard, **r))
    for choice in range(8):
        n = Actions(image, base, (choice, 0)); r = n.hurt()
        assert r['health'] == 1 and [s['sample_id'] for s in r['samples']] == [HURT[choice]-15], r
        rows.append(dict(event='nonfatal_hurt', choice=choice, **r))
    for guard, kwargs in (('invulnerability', dict(invulnerability=1)), ('invincibility', dict(invincibility=10)),
                          ('fatal', dict(health=0))):
        n = Actions(image, base); r = n.hurt(**kwargs)
        assert [s['sample_id'] for s in r['samples']] == ([58] if guard == 'fatal' else []), r
        rows.append(dict(event='hurt_guard', guard=guard, **r))
    # Native table bytes plus exact fallback state on an immediate repeated cue.
    for selector, table, va in ((-3, PICKUP, 0x4c7678), (-1, HURT, 0x4c7638)):
        n = Actions(image, base)
        assert list(n.u.mem_read(n.va(va), 9)) == table
        slot = -1-selector
        n.put(n.va(0x572c24), table[0]); n.put(n.va(0x572c08+slot*4), table[2])
        assert n.call(0x414cc0, selector & 0xffffffff) == STOP
        r = n.result()
        assert r['last_cue'] == table[2] and n.get(n.va(0x572c08+slot*4)) == table[0]
        rows.append(dict(event='repeat_fallback', selector=selector, **r))
    return rows


def main():
    image = (ROOT/'work/copies/BUGS_PC-disc/bugs.exe').read_bytes()
    assert hashlib.sha256(image).hexdigest() == RETAIL
    first, second = proof(image, 0x400000), proof(image, 0x1000000)
    assert first == second
    out = ROOT/'reports/audio/EXP-20260910-009-native.json'
    report = dict(experiment='EXP-20260910-009', retail_sha256=RETAIL,
        evidence='Offline original x86, device/visual/geometry stubs; not live listening',
        bases=['0x400000', '0x1000000'], cases=first)
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(report=str(out), cases=len(first), both_bases_equal=True)))


if __name__ == '__main__': main()
