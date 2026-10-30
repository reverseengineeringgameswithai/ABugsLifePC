---
type: system
status: active
updated: 2026-10-29
tags: [system/start]
---

# START HERE

This Obsidian vault is the durable shared memory for the researcher and agents.
Conversation history is disposable. [[Agent Operating Manual]] is the canonical
policy; [[Project Charter]] defines the PC-first mission and evidence hierarchy.

**Scope.** This vault holds the reverse-engineering research on the Windows PC
release of *A Bug's Life*: how the original executable and its data work, and
what the original engine requires, permits or limits when its files or code are
changed. The author's own modding project is maintained separately, so some
experiment IDs cited in plain text, without a link, are not part of this
repository.

## Required startup sequence

1. Read `Vault/00-System/START HERE.md`.
2. Read `Vault/00-System/Current State.md`.
3. Read `Vault/00-System/Project Roadmap.md`.
4. Read `Vault/00-System/Environment Status.md`.
5. Read `Vault/50-Decisions/Decision Log.md`.
6. Read `Vault/70-Known-Unknowns/Known Unknowns.md`.
7. Read the task MOC; default to [[Reverse Engineering MOC]].

## Current orientation

[[Current State]] (2026-10-29) summarises where the research stands, subsystem
by subsystem, with links to the notes and evidence. [[Next Tasks]] (2026-10-29)
lists the open research tasks in a proposed order; it authorizes nothing.
[[Project Roadmap]] owns milestones and gates; [[Known Unknowns]] owns
unresolved questions, not an automatic work queue. [[Subsystem Coverage Map]]
shows which subsystems have PC evidence and which are still blank.

The latest research results (2026-10-18) read the creature subsystem end to
end apart from the level routines. The creature script VM is confirmed running
in saved hardware samples, and no retail creature row drives its unbounded
indexes out of range ([[EXP-20261018-002 - Creature script counter in saved runtime samples]],
[[EXP-20261018-001 - Creature row index census]]). The same session closed the
event callbacks, the controls screen, the frame cap and the default depth rule;
[[2026-10-18 - Claude - Static research on creature rows and the script VM]]
lists every result.

Every original level has a Blender reference map: [[PC original level Blender maps]]
(Training: [[PC original Training Blender mapping]]). Cross-port work requires
[[Cross-Port Evidence Policy]] and [[External Source Registry]] first.

Older “OPEN” claims are dated history, not instructions to target those IDs.
Keep the two stable handoff H2 sections and their adjacent `<!-- briefing: ... -->`
markers in place: [[Current State#Current task handoff]] and
[[Environment Status#Current runtime handoff]]. Update them instead of adding
dated banners above them. `make briefing` is a generated map; verify relied-on
claims in the cited notes. `make budget` measures the required reading set.
Old chronological registers are linked under [[Project history MOC]], outside
required startup reading.

Before any runtime launch and after any close, run `make session-audit` with
host visibility and account for every process and sink. Follow
[[Agent Operating Manual#Runtime instance lifecycle]]. The session-control tools
are fixture-validated only, except `game-memory`'s read, snapshot and restore
verbs, which [[EXP-20260817-188 - Live game-memory read save restore validation]]
ran against the live game. Until CAP-010 passes against the real game,
[[PC autonomous game control]] remains authoritative and their output is not
gameplay evidence. Every live-memory write requires fresh explicit permission,
a compare-before-write guard and a receipt.

## Before touching evidence

- Identify the executable SHA-256 or state explicitly that no binary is available.
- Work only on copies under `work/`; never modify `originals/`.
- For renderer-facing runtime work, select **hardware acceleration**, the
  second initial option reached with Down, wait for its highlight, then
  confirm. Do not accept the early selection summary alone. An accepted arm
  must positively prove all six markers in the same log:
  `Native software render mode is FALSE`, `RenderMode set to Direct3d render
  mode`, `Screen mode 640x480x16 selected`, `OnlySystemMemory status VIDEO
  MEMORY ONLY`, `D3DAPPCREATE : Mode set to 640x480`, and
  `INIT : Starting Direct3D renderer`. Reject the arm if any is absent, if it
  instead records `SYSTEM MEMORY ONLY`, 320x200, or `INITSOFTRENDER`, or if
  the gameplay surface occupies only 320x200. A software-renderer run is a
  separate experiment and cannot serve as a hardware control. EXP-137 caught
  one false-looking selection this way before any target write.
- Retail `bugs.exe` has **no** native hardware/Direct3D command-line argument
  (static audit [[EXP-20260816-143 - Automatic Direct3D startup static audit]]),
  so for the **retail hash** the manual hardware-selection procedure above and
  the full six-marker log gate remain authoritative. Do not pass guessed
  renderer arguments or skip the chooser on the retail exe.
- A guarded **auto-hardware build** now exists and is runtime-accepted at its
  own derived build hash: `scripts/make-auto-hardware` applies the exact paired
  code+relocation transform to a derived copy under `work/`, and
  [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] /
  [[EXP-20260816-151 - Independent auto-hardware runtime audit]] confirm it
  boots straight into renderer-level hardware Direct3D with no chooser input.
  Use it only through that builder on a derived copy — never by hand-editing,
  applying one of the two edits, or claiming a native retail argument. See
  [[PC automatic Direct3D startup candidate]].
- Frame a bounded question.
- Assign or cite an evidence ID.
- Record exact environment, path, procedure, expected result, and observed result.
- Separate **Confirmed**, **Inferred**, and **Unknown**.

## End-of-session sequence

1. Update [[Current State]].
2. Add or update relevant research notes.
3. Update [[Known Unknowns]].
4. Record significant architectural or research decisions in [[Decision Log]].
5. Write a session note using [[Session]].
6. Update relevant MOCs.
7. Ensure every new conclusion points to its evidence.

A repeated claim is not evidence. The original executable running under controlled conditions remains the behavioral reference.

## Project charter

The required startup sequence above remains the routine handoff. On a first session, before changing scope, or before consulting another port, also read [[Project Charter]]. It defines the durable mission, evidence hierarchy, and the gate for bounded PS1 comparisons.

## Historical record

[[START HERE history through 2026-09-26]] preserves the previous note verbatim. [[Session Index]] indexes the original session records. Historical permissions and process IDs do not carry forward.
