---
type: experiment
id: EXP-20260909-004
date: 2026-09-09
status: bounded; live launches observed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Original PC data, built PC instructions in Unicorn, guarded Wine observation and authorized intervention
question: Why does a grown cannon plant whose PLANTTER template payload was emptied not accept and launch Flik, and what must a repair restore?
result: An emptied template payload gives the plant descriptor empty bounds, so reader 004ACEB0 never reports the plant and activation 00468010 case 2 cannot run; restoring the original low-kind payloads recovers contact and state 17 offline; for an already registered plant 0044CA7F skips re-registration on an unchanged type/tag, so cached template and descriptor bounds persist until also updated; two live launches observed after both updates
tags: [re/experiment, terrain/collision]
---


# EXP-20260909-004 - Restore native plant collision

A grown cannon plant in an authored level whose PLANTTER template payloads had
been emptied would not accept Flik. A passive 40-second run collected1591
user-controlled samples while the cannon was approached; each reported ground
descriptor99, never cannon233. Movement and Shift jump inputs were observed; Y
ranged from-202188 to-182375. This establishes failed contact during those
attempts, not the full cause of perceived lateral blocking. No agent gameplay
input or live memory write was used in this capture.

Read-only census identifies the visible cannon as plant slot3/type2, animation1,
flags7, world(779964,-184673,667694), selecting template descriptor223 and
dynamic descriptor233/tag105. Its payload10271559 begins with-1, giving empty
bounds(779932,667662,32,32). PC source record6 is at PLANTTER offset6708.
Original payload length1540,16 groups/42 cells. The old isolation replaced only
its initial marker, and EXP20260906-007 restored only the separate mushroom.

Independent evidence forms:

- Original allocation/directory comparison: all13 low-kind payloads preserve
  original bytes after their initial marker. Record8 is already restored. The
  current input SHA c8251790…a762 is the prior mushroom-repaired profile;
  original PC PLANTTER SHA0a0cf7fa…b468. Full hashes/offsets are in the report.
- Native loader004A8410 maps source+0x1a to plant type+33. Constructor00467E60
  selects type2 from the white tier4 preset; growth00468BF0 reaches settled
  animation1. Native registration0044CA19–0044D20B uses record6 for this plant.
- Reader004ACEB0 returns the dynamic plant slot+1 only after an appropriate
  grounded tagged contact. Activation00468010 case2 requires matching slot,
  animation1 and flags; then it stores17 at0059D98C and switches plant animation.
  Missing template contact prevents this condition.
- Paired original-instruction trials use the same banked executable and terrain,
  the observed cannon position, and a downward approach from40000 world units
  above. The empty control ends100 ticks with contact99/state0. Cannon-only and
  all-low restoration both reach contact233/reader4/state17 at tick35,
  world(779868,-188003,667701). Both copied-live-structure and native-constructor
  probes agree. Unit variants pass at image deltas0 and0x10000000.

Renderer-resource presence is supplied and the renderer block excluded; feedback
callbacks are stubbed. Native collision/constructor/growth/contact instructions
execute unchanged. This proves offline cannon activation, not an observed full
live cannon flight. The constructor fixture must wait for animation1 as well as
the settled bit; the timer alone expires earlier and is not a growth-ready test.

The repaired build restores12 two-byte markers (24 bytes), leaving the existing
mushroom repair, high-kind stream, unknown tails, directory and authored terrain
exact. All low-kind allocations then equal the original PC data. Restored
PLANTTER SHA 03d2a8c3fedef819f828f701e50e47df72f30aec12e3a9afe63f60305c433bc9.
The whole-source hash guard rejects altered/truncated/unknown profiles. Focused
make check577 passes.

Private evidence: `work/experiments/EXP-20260909-004/` contains the initial census,
`user-cannon-approach.json`, original static queries, `plant-census.json`,
`native-cannon.json`, `native-cannon-constructor.json` and `build-preservation.json`.
Public metadata/hashes: `reports/terrain/EXP-20260909-004.json`.
Runtime directory bytes are not retained after the loaded payload prefix;
the read-only preflight matches the first16692 bytes exactly, not the full file.
No claim is based on bytes beyond that prefix.

With fresh explicit user authorization, the same game26160/start672985 was
identity/content/code guarded and briefly stopped for a 24-byte payload repair.
All16692 payload-prefix bytes matched the control; all template pointers and
twelve markers matched before writing. Twelve two-byte writes were read back;
the entire resulting prefix equals the repaired file prefix. Flik state before
and after the stopped write is identical, and the process resumed. Receipt:
`live-write.json`, with approval in `live-write-authorization.json`.

This runtime intervention revealed a missed condition in the original plan:
the active cannon still has the empty bounds despite its restored payload.
Both the source template bounds and current plant descriptor bounds are cached.
Static instruction0044CA7F skips registration on an unchanged type/tag; the
copy at0044CABF–0044CB02 only runs when registration proceeds. Read-only census
after the write still shows descriptor233 bounds(779932,667662,32,32).
This contradicts the initial expectation that a24-byte live edit alone would
make the already grown cannon testable; the fresh-file build result still holds.

`probe-cached-bounds.py` reproduces the payload-only edit after native loading:
bounds stay old. It derives each changed cache word from native fresh control
versus repaired loading, including the observed three active plant instances.
Applying those60 words offline (240 written bytes,127 differing byte values)
matches fresh cannon bounds(770652,660526,18752,272256) and reaches
contact4/state17 at tick35. Every proposed current live word is compared read-only
against its control. `cached-bounds-plan.json` and `registration.asm` own this
new evidence. No guessed bounds or geometry changes are involved.

A separately authorized 240-byte cache update (receipt `cache-write.json`)
verifies all60 before-words against the native plan, every four-byte
write/readback, unchanged Flik state while stopped, unchanged repaired payload
prefix and successful process resume. The settled live cannon then has the exact
fresh-build bounds(770652,660526,18752,272256). No restart occurred; both
authorized operations are complete and must not be repeated.

A bounded300-second passive observer (`user-cannon-fixed-02.json`, 11897 samples,
no agent keys, no further writes) records Flik contacting233 at214.8799s and
242.5636s; cannon state17 and animation2 follow, then upward velocity reaches
-7936 and Y reaches-314339/-313997. These are two observed launches. An earlier
55-second recording (`user-cannon-fixed-01.json`, 2181 samples) had no input and
is not a failed approach.

The user reported that the restored cannon works but acts like a complete wall.
Whether that wall-like behavior matches the original is not established.
Exhaustive behaviors, all landing routes and distant no-ground plants remain
unverified.
