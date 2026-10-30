---
type: implementation
status: bounded
created: 2026-09-10
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260910-002, EXP-20260910-006, EXP-20260910-007]
tags: [re/tutorial, modding/dialogue]
---

# PC Mr Soil lesson triggers

Native Training lesson advancement in retail `0043C340`, and the native
speech-completion and HUD behaviour that a change to lesson timing or counts
must respect.

## Native trigger census

**PC confirmed:** the following predicates execute in retail `0043C340`.
Original x86 is exercised offline at image bases00400000 and01000000
(EXP-20260910-002). The current actor
layout and some field meanings remain address-labelled. Topic descriptions are
the identification aids from [[PC Mr Soil dialogue replacement]], not a new
semantic naming pass. Lesson numbers below are zero-based.

| Stage / WAV | Advancement predicate | PC locator |
|---|---|---|
| 0 / LESS1 | Six samples of the throw countdown word `0059D996 ==17` | `0043C3B1–0043C3C9` |
| 1 / LESS2 | Six jump-word `0059D990 ==1` transitions whose prior sample `0059F6B4` was0 or3 | `0043C3F8–0043C469` |
| 2 / LESS3 | Three samples of bounce countdown `0059D994 ==9` | `0043C485–0043C49D` |
| 3 / LESS4 | Three `0059D9B3 ==9 &&0059D96C >0` samples, then `0059D96C ==0` and seed word `0059B70A !=0` | `0043C4FC–0043C58A` |
| 4 / LESS5 | Specific seed word `0059B79C ==1` | `0043C58F–0043C5D1` |
| 5 / LESS6 | Carried-object state `0059D96C <0`, subsequently0, then58 calls including release call | `0043C680–0043C6CA` |
| 6 / LESS7 | Particular first green-token row's Y is the consumed sentinel `80000000` | `0043C5D6–0043C610`, `0043C709` |
| 7 / LESS8 | Referenced actor2 seed colour byte `*(0059B7B0)+0E` nonzero on two update calls | `0043C615–0043C647` |
| 8 / LESS8A | Same seed word `0059B79C ==1`; clears `0059B792` | `0043C64C–0043C67B` |
| 9 / LESS9 | Particular second green-token row consumed | `0043C6CF–0043C71A` |
| 10 / LESS10 | Both timers `0059B816/0059B89A ==10000`, both words `0059B822/0059B8A6 ==0`, referenced colour bytes are0 and2 in either order | `0043C71F–0043C7B8` |
| 11 / LESS11 | Flik runtime Y `<-20000`, support word `0059D992 !=0`, `004ACEB0()==0` | `0043C7BD–0043C802` |
| 12 / LESS12 | Weapon byte `0059D9A7 !=0`; entry activates four spiders | `0043C807–0043C868` |
| 13 / LESS13 | No native next lesson; reveals four berry seed tokens, later proximity repeats alternate cues36/37 | `0043C86E–0043C8E6`, `0043C940–0043C980` |

The count starts at1 after entry, so comparisons `>6` mean six samples, not five.
The colour lesson is **not two button presses**: a single persistent colour change
satisfies two sampled updates. Discard's58 calls are not “60 actions.” The seed
pickup lesson has a release/state requirement in addition to its count. The ledge
is not an XYZ box or elapsed timer. `004ACEB0` only returns nonzero for its
support-word/descriptor branch; no broader semantic rename is implied.

The throw word is decremented in `00402DC0`; the native trigger is a countdown
sample, not “number of enemies hit.” Lesson entry effects are
seed activation, green-token reveal, spider activation and final berry-token
reveal. EXP-20260910-001 owns
the exact original token-row / blueberry-collection proof.

## Native lesson behaviour and change limits

A native lesson goal includes native early speech interruption, proximity
repeats and a30-update inter-lesson pause.
[[EXP-20260910-006 - First Soil throw count boundary proof]]: stock6 and every
adjusted target1–6 advance exactly at eventN in two-base original-x86 checks.
[[EXP-20260910-007 - Five-throw Training sign and native defaults]] shows that a
changed count also needs the initial sign at0043C250, not only the existing
countdown path.

Displayed counts are bounded: `00410A20` uses the third HUD argument
as an unchecked frame index. EXP007 matches the live pointer0076FA84's resource
with Training RAW type26/id33:32×32, six frames, no local palette entries.
Target7 would request frame6, beyond this bank. Larger counts need extended
number graphics and a safe HUD lookup. This is a display
limit, not a proven maximum of the native action counter.

The final lesson (stage13) is terminal and has no native final goal. A
lesson-timing change must not select an out-of-range stage14; staying at
stage13 leaves the original exit marker playable.

## Actual speech completion

`0042C110` merely returns `00596CEC`. Idle alone is insufficient: it also follows
stop/failure. The EXP-20260910-002 hook therefore invalidates completion when a
new valid stream starts at `0042BF48` and takes ownership only when its requested
cue matches the current lesson; disabled, failed or interrupted playback never
fabricates completion. Native proximity replay can retry an interrupted
instruction.

Native worker `00440F50` accounts DirectSound playback progress in `005966B0`.
At `004412CC–004412DA`, its stop allowance can accept `size-refill_block`.
The EXP-20260910-002 speech-waiting hook instead requires **played bytes ≥ full
data size** on the already-EOF drain branch and only marks natural completion at
`004412DC`. Ordinary streams retain their native stop logic.

Wall-clock timing is available through the imported `timeGetTime` at IAT
`00864884`; the native inter-lesson pause is counted in updates.
