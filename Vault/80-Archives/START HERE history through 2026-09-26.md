---
type: archive
status: historical
created: 2026-09-26
tags: [archive/project-review]
---

# START HERE history through 2026-09-26

Historical snapshot of [[START HERE]] before the September 26 review. The body
below is preserved, including superseded claims, old process IDs and
consumed permissions. It is evidence of earlier notes, **not a current work
queue or runtime binding**. Use [[Current State#Current task handoff]] and
[[Environment Status#Current runtime handoff]] for current instructions.
2026-09-26 - Codex - Project review and Vault cleanup records the review.

<!-- preserved-body:start -->


# START HERE


Latest active correction is [[EXP-20260916-011 - Terrain camera range guard for horizontal bands]]: intermittent eastern-path horizontal bands come from signed16 camera-coordinate wrap in admitted western terrain. An opt-in native visual guard clears the checked replay and92 final hardware captures while all assets/source/collision/placements stay exact to EXP010.


This vault is the durable shared memory for the researcher, Codex, and Claude. Conversation history is disposable. Do not begin substantive work from memory alone.

## Required startup sequence

1. Read `Vault/00-System/START HERE.md` (this note).
2. Read `Vault/00-System/Current State.md`.
3. Read `Vault/00-System/Project Roadmap.md`.
4. Read `Vault/00-System/Environment Status.md`.
5. Read `Vault/50-Decisions/Decision Log.md`.
6. Read `Vault/70-Known-Unknowns/Known Unknowns.md`.
7. Read whichever MOC relates to the current task.

Start from [[Reverse Engineering MOC]] when the relevant MOC is unclear. Detailed agent policy is in [[Agent Operating Manual]].


Maintain the two stable handoff sections, [[Current State#Current task handoff]]
and [[Environment Status#Current runtime handoff]], **in place**, ahead of chronology.
Keep their adjacent `<!-- briefing: ... -->` markers: `make briefing` requires
one nonempty H2 for each marked handoff and preserves the entire section under
budget pressure. Do not put the only current instructions in a newly dated
banner while leaving these sections stale. Old dated entries and old next-agent
directives are history, not an automatically authorized work queue. The briefing
also recognizes date-named decision headings (`YYYY-MM-DD: Title`) alongside
older `DEC-YYYYMMDD-NNN` entries.

`make briefing` prints a generated, bounded orientation (about 4,600 tokens)
drawn from the notes above, with pointers back to each. It exists because the
mandated set measures far more than a session can hold. It **does not replace
the sequence above and is not authoritative**: anything you rely on must be
verified in the note it cites. `make budget` reports the current sizes.
The Sep10 hygiene check retains these budget warnings: several historical
registers remain oversized. Passing link/frontmatter checks is not a claim that
the mandated reading set is within budget; use the bounded current handoffs.
Before any runtime launch, follow
[[Agent Operating Manual#Runtime instance lifecycle]]; close obsolete runtime
and agent instances promptly and prove the final process/sink audit is clear.
`make session-audit` classifies every runtime process and audio sink as owned
by a recorded session or unattributed.

The session-control tools in [[Session control plane]] automate the launch
recipe and record an ownership ledger, but they are **fixture-validated only
and have never run against the game**. Until CAP-010's acceptance arm passes,
[[PC autonomous game control]] remains the authoritative procedure and no tool
output may be cited as runtime evidence.

[[Project Charter]] defines why and within what authority the project operates.
[[Project Roadmap]] defines milestone order and gates. [[Current State]] records
where the project is now, while [[Known Unknowns]] records unresolved questions.
Do not create competing plans in session notes or MOCs.

When a task uses the PS1 reverse-engineering project or any other external project, also read [[Cross-Port Evidence Policy]] and [[External Source Registry]] before inspecting that source.

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
<!-- preserved-body:end -->
