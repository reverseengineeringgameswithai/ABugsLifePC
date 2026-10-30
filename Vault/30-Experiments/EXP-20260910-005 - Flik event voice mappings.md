---
type: experiment
id: EXP-20260910-005
date: 2026-09-10
environment: Fedora host, Tk/ffmpeg, offline Unicorn at two PE bases
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
question: Which native events trigger Flik's event voice lines on PC, under what conditions and repeat rules?
result: Nine recording/event bindings confirmed by native execution at two PE bases - grain-gate reminders (Tunnels 0043300D, City Entrance 00433833) with radius and cooldown rules, pickup cues through 004292C0 selectors, and a City Square Super Jump reminder (cue 79, sample 64) that is dormant because normal banks 9/21/22 do not load sample 64; hint helper 00414EE0 suppression guards apply
status: accepted-bounded
created: 2026-09-10
updated: 2026-10-29
tags: [experiment/audio, re/native]
---

# Flik event voice mappings

This experiment maps Flik's event-triggered voice lines, such as needing more
grain at a gate or needing Super Jump, to their native triggers, conditions,
repeat rules and sound-bank availability.

## Evidence method

Exact original PC executable SHA256 above is authoritative; no PS1 source used.
Static instruction windows at the addresses below were compared with original
x86 execution in `scripts/probe-flik-events.py`. The probe runs31 cases at each
of PE bases00400000/01000000 and requires identical results, retained in
`reports/audio/EXP-20260910-005-native.json`. Cases comprise12 grain-gate controls,
12 missing-Super-Jump/bank controls, and7 pickup handlers. Native bank0049E3E0
executes with its file loader0049DF90 intercepted to capture sample/path mappings.
Native speech helpers00414EE0/00414CC0 and0041A2B0 execute through the final
sample request0049D820, which is stubbed. Unrelated visual callbacks are stubbed.
These are event-request/path proofs, not real device playback or listening.

`scripts/transcribe-flik-candidates.py` used an already-installed external Python
environment and cached faster-whisper-small locally, offline, without modifying
that environment or installing/downloading anything. It transcribed39 candidate
private WAVs; metadata/hash/text results are in
`reports/audio/EXP-20260910-005-asr.json`. Automatic wording is a discovery aid,
not a certified transcript or speaker census. The nine curated display phrases
normalise punctuation and obvious berry-name transcription errors. Other
uncertain or empty transcriptions are not promoted into event labels.

## Confirmed native event bindings

All voice cues below map to sample ID `cue - 15` through0041A2B0/0049D820.
`config/audio/pc-flik-events.json` stores metadata only.

| Recording | Event | Native evidence |
| --- | --- | --- |
| USGN083, cue76/sample61 | Need more grain | Tunnels0043300D; City Entrance00433833 |
| USGN086, cue79/sample64 | Need Super Jump; normally dormant | City Square00434185 |
| USGN082, cue75/sample60 | Super Jump acquired | Pickup selector0F,0042944C |
| USGN081, cue65/sample50 | Invincibility acquired | Selector0C,0042942A |
| USGN050, cue62/sample47 | Health pickup | Selector09,004293FA |
| USGN031, cue53/sample38 | Super Berry | Selector23,004294CC; weapon1 |
| USGN032, cue54/sample39 | Homing Berry | Selector21,004294CC; weapon2 |
| USGN033, cue55/sample40 | Mega Homing Berry | Selector24,004294CC; weapon4 |
| USGN034, cue56/sample41 | Gold Berry | Selector22,004294CC; weapon3 |

**Tunnels grain gate:** the complete nine-row gate loop00432EF1–00433049 checks
closed state10C7, grain byte0059D9B1 below the row requirement at004DA9D0+20i,
and squared XZ distance after arithmetic shift8 below40². The gate-opening
radius is100, larger than the reminder radius. Shared cooldown0059EFDC must be
zero; the request resets it to60+random byte0–255. Enough grain enters the
opening branch instead. Native tests cover below/one-below/exact requirement,
just-inside/exact-radius exclusion and a nonzero cooldown. The loop slice does
not execute the outer updater's cooldown decrement; reset/radius/condition proof
must not be represented as a complete simulated level update.

**City Entrance grain gate:** actual function00433790 executes with native
proximity helper00416580. Gate state0059F020+4i must be-1, distance must be
inside the supplied radius, grain must be below10×(i+1), and shared cooldown
0059F018 must be zero. Native thresholds are10/20/30; reset is60+random byte.
The probe exercises gate0 with radius80; the index-dependent threshold expression
comes from the static instructions, not live testing of every gate. Enough grain
opens the gate without the missing-grain request. Cooldowns are game-update
counts, not a claimed wall-clock duration.

**Super Jump reminder:** native dispatcher00418780 with engine5 reaches City
Square00434170 via004187A5. Its prefix00434170–004341B0 requests cue79 when
timer0059F06C is zero and flag0059D9A0 bit20 is absent. Timer resets to600+random
byte even when Flik already has Super Jump; nonzero timers decrement once per
update. This is periodic missing-power-up logic, not a failed-jump input test.

**Important contradictory evidence:** the user recalls this line, and the PC
updater requests it, but normal City Square bank9 and later banks21/22 do not
load sample64. Startup bank1 does. Native bank loading0049E3E0 releases/clears
old samples rather than preserving a startup-bank copy. A separate regression
executes real0049D820 with unloaded sample64 and obtainsFFFFFFFF/no playback.
Therefore the event is **dormant** in normal play: replacing its WAV alone does
not activate it. This is not proof it can never play under
all device/reinitialisation paths. A future discriminating experiment should
observe sample64 ownership, active bank, flags and timer during ordinary City
Square entry and any audio-device reinitialisation, using read-only state. No
reactivation patch or live test occurred here.

**Pickups:** actual004292C0 executes one active overlapping56-byte effect row
and63 inactive rows. Super Jump sets flag20; health increments0059D9A4. The
invincibility request occurs only when0059D98E is below1; a pickup during active
invincibility refreshes the timer to400 without another quote. Berry selectors
set the weapon values above. A loaded clip does not prove that every level
contains the corresponding pickup.

Native hint helper00414EE0 can suppress requests during already tracked Flik
speech (0041A550), state2 at0059A5B0, flag04 at0059D9A0, or blockers00572C20/
00572C80. Regression negative controls exercise the four explicit state/flag/
blocker values; the tracked-speech guard also has static evidence. Pickup helper
00414CC0 retains its own native suppression. Nothing bypasses these guards.

`tests/test_flik_events.py` covers both-base native execution, unloaded sample
failure, suppression/repeat guards and catalogue/callsite correspondence. Final
focused `make check`:132 pass,6119 deselected; no full-suite or all-voice
listening claim. Originals remain untouched. Session:
[[2026-09-10 - Codex - Label Flik voice events]].
