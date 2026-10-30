# Bounded PC update/render probe

Independently authored diagnostic assembly for EXP-20260907-028, pinned to the
four-chunk control and visual-detail fixtures. It is not installed by the level
compiler or included in the playable handoff. All executable/data copies and
live experiment helpers remain under ignored `work/experiments/EXP-20260907-028`.

`measure.asm` and `scene-offsets.inc` match the tested private sources. Build with
NASM `-f bin` from this directory. The output is a private binary, not a tracked
asset. `build-probe.py` in the experiment applies exact byte guards, preserves an
inverse, removes the overwritten HIGHLOW relocation at preferred VA 00405C08,
and checks the original 4096-byte CC cave at 004BBC00. Source EXE SHA-256:
`431ec953b67bd3233f8fa58e7a22edbfabaeb153e3ee322d760c45f2a44c7d8f`.
Do not apply this fixture-specific recipe to other builds or arena loads.

The eight entry RVAs follow a 20-byte header. Preferred hook VAs:

| Hook | Role |
| --- | --- |
| 0040FFCA | Start before the native gameplay update; replay call 00401E79 |
| 00405C07 | Preserve native millisecond timestamp, start render interval |
| 00405B63 | End both intervals after present, before deliberate pacing |
| 004AB756 | Completed collision-collector calls and candidate maxima |
| 00405816 / 0040598B | Submitted batch vertex/index totals and maxima |
| 0044D6FA / 0044D712 | Primary scene admissions and four terrain chunk bits |

The upper arena range preferred VA 01000000..010600FF holds a 256-byte header
and 2048 records of 192 bytes. The exact fixtures retain less than 1.5 MiB from
0087B000. This is diagnostic scratch for that finite load, not a general arena
reservation protocol. QPC/QPF resolve through existing kernel32 IAT entries;
there is no external live memory write or changed frame pacing. Level and cursor
checks gate initialization. Register/flags preservation and displaced operations
pass 50 offline checks across two image bases, including stdcall argument order,
API failure, counter borrow, inactive hooks and ring wrap. API internals,
LastError and arbitrary complete engine state are outside that equivalence check.

Each record publishes matching sequence words at offsets 0 and 188 after its
payload. The reader rejects incomplete/overwritten slots and records dropped
frames separately. Core payload: native render milliseconds +4, whole interval
QPC ticks +8, render ticks +16, start/end ticks +24/+32, level/input +40/+44,
position +48, heading +60, camera matrix +64, translation +84, twelve collection/
batch/admission counters +96, error bits +144, moving-plant count/type mask
+148/+152, seed count +156, contact +160, flags/lives +164/+166, cursor +168,
native timestamp +172, transition/damage +176/+178, renderer flags +180 and
back-to-back QPC-call gap +184. Reserved bytes are zero. Counter frequency is
at header +16. Consult the tested assembly and experiment reader for the full ABI.

Timing includes probe overhead, Wine and host scheduling. End-record copying and
native pacing are outside the intervals. Present can submit asynchronously;
these are not isolated GPU execution/completion times. Route repetitions use
camera feedback and recorded contexts, not identical per-frame input movies.
EXP-026's old coarse probe covered render/present only: 0040FFC0 calls gameplay
004144C0 before renderer 0044D430, which starts the old timestamp. The new probe
separates both boundaries explicitly.

Evidence and acceptance limits:
`Vault/30-Experiments/EXP-20260907-028 - Representative update and render headroom.md`
and `reports/terrain/EXP-20260907-028.json`.
