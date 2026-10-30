---
type: implementation
status: implemented
created: 2026-09-09
updated: 2026-10-29
evidence: [EXP-20260909-003, EXP-20260916-004, EXP-20260928-001]
tags: [implementation/modding]
---

# PC fixed growable seed authoring

## Forced plant bytes (EXP-20260928-001)

Placement `+0x0E` is the seed colour and `+0x0F` an optional forced plant: a
nonzero value selects table `004DE9F0` entry `(b>>4)+(b&15)*4`. Brown `0/0x10`
grows the type 3 propeller and green `2/0x32` the type 1 tall leaf plant. Native
constructor runs and hardware confirm both. The
resource collector requests a forced model only for state 1/4 seeds, so fixed
seeds need retired token rows as model requests.

## Original seed slots

The original Anthill has nine seed slots, 19/20/21/22/23/24/26/27/28: five
state3 seeds and four state0 seeds. EXP-20260916-004 moves them and shows their
native configuration after XYZ stays exact, so each retains its source
behavior. A slot must stay unique. Original-PC offline collision support checks
show seeds can rest on terrain, the existing paired structures and solid
authored scenery.

## Additional fixed seeds

EXP-20260909-003 records original
PC evidence and the extended-path build. An additional fixed seed copies
original Anthill donor19's opaque configuration into an available actor slot,
changing only XYZ (stored PC units). Enemies and
new seeds share the64-slot native pool; slot0 is excluded for new seeds because
its held-actor byte offset would equal the empty sentinel. At most52 additional
seeds fit with no authored enemies, fewer with enemies.

Native0041C420 resolves terrain height and unique contact selectors. Donor19's
state3 and short range1 retain native stationary interaction; movable donor26
has state0. Growth, plant selection and the20-plant pool remain native. This
adds no executable patch or streaming adapter. Leave sufficient safe ground around fixed seeds:
their native release animation propels Flik backward. EXP003 enlarged this
landing to2048 stored units after the first1024-unit landing failed that check.

Original/relocated native fixed-vs-movable interaction and native stomp/growth
are covered by EXP003.
