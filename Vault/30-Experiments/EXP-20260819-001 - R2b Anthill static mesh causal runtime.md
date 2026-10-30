---
type: experiment
id: EXP-20260819-001
date: 2026-08-19
status: complete-inconclusive
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Wine 11 staging under Gamescope/Wayland; unchanged retail executable; hardware Direct3D
question: Does the guarded Anthill Level01 type-0x41 vertex edit produce the preregistered localized visible change under matched hardware-Direct3D A1/B/A2 runs?
result: The three arms were procedurally valid, but the 0.75 control-agreement gate failed at 108 of 307200 pixels; causal effect classification is therefore inconclusive.
tags:
  - re/experiment
  - re/level-format
  - re/runtime
---

# EXP-20260819-001 - R2b Anthill static mesh causal runtime

## Result

The authorized A1/B/A2 run set is procedurally valid and the retained lifecycle,
identity, level, renderer, capture, and close gates pass. The causal result is
**inconclusive**: only `108 / 307200` pixels (`0.0003515625`, or
`0.03515625%`) were identical across all 30 control frames, far below the
preregistered `0.75` control-agreement threshold. Effect classification stops
at that failed gate.

This is not a candidate rejection, a no-effect result, or confirmation that the
edited mesh is visible ground. R1 remains complete and R2 remains open.

## Authorization and write boundary

The user explicitly authorized R2b to create the EXP-008 one-byte Anthill
Level01 work-copy candidate and run the exact A1/B/A2 Direct3D experiment. The
authorization expressly excluded runtime memory and debugger writes. No runtime
memory or debugger write was performed. The only process-memory access was a
read-only four-byte level-index read at `0x00861c84` in each accepted arm.

## Frozen candidate receipt

| Item | Value |
|---|---|
| retail executable SHA-256 | `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` |
| retail Level01 DAT SHA-256 | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` |
| candidate Level01 DAT SHA-256 | `c76586991cb4cede5d58a3cae8278aca80ba2082130dcf33062b698334db0a4c` |
| scene/object/geometry chain | primary record 81 at `0x1b58` -> object `0x4860` -> geometry `0x188cc` |
| face/vertex | face 8 -> vertex 25 at `0x189fc` |
| edited component | bytes at `0x189fe`: `7b 13` (`4987`) -> `7b 1b` (`7035`) |
| sole physical byte edit | file offset `0x189ff`: `0x13` -> `0x1b` |
| proven numeric effect | `+2048` in the second stored vertex component |

The object and geometry each have one Level01 scene reference, and vertex 25 is
used by face 8 only within that payload. Component-axis identity, world scale,
and exact screen location remain unknown.

## Renderer calibration

The chooser did not expose a visually discriminating selection state. Two
separate non-arm calibration runs therefore established the input-to-renderer
mapping through the complete log gate:

- C0: no direction input, then Return, selected the software path.
- C1: Down keydown -> requested host sleep `0.180` -> keyup, then Return by the
  same mechanism, selected hardware Direct3D.

The requested sleep is not claimed as the delivered key-hold duration. C1's
measured wall intervals were `0.238507618 s` for Down and `0.239506415 s` for
Return. Every accepted arm used the same XTEST mechanism and retained its own
keydown/key-up timestamps.

## Accepted arms

| Arm | Run ID | DAT | Level-index read | Frames | Maximum absolute deadline error |
|---|---|---|---|---:|---:|
| A1 | `R2B-A1-005` | retail | `01 00 00 00` | 15 | `0.00007450397242791951 s` |
| B | `R2B-B-001` | candidate | `01 00 00 00` | 15 | `0.0000710780150257051 s` |
| A2 | `R2B-A2-001` | retail | `01 00 00 00` | 15 | `0.00007385597564280033 s` |

Each arm used the unchanged retail executable, passed the full six-marker
hardware-Direct3D log gate with no software rejection marker, navigated
Training -> Anthill -> Level01, captured the natural `Level One: Welcome to Ant
Island` title/index boundary before Return, then retained 15 native `640x480`
frames at the frozen cadence. Each arm also retained a clean immediate
pre-launch audit and clean post-close audit. Post-title logs contain
`End ClearLoadScreen`, `End InitMainGame`, and `NextLife`.

The discarded setup and A1 attempts remain rejected evidence and are not in the
accepted namespace. They do not contribute frames to this result.

## Frozen comparison and observed result

The comparison decoded all 45 retained PNGs to RGB and applied the preregistered
rules in order:

1. A control-stable pixel must be byte-identical in every A1 and A2 frame.
2. At least `75%` of the `307200` pixels must be control-stable, and at least one
   of the 225 A1/A2 cross-pairs must be byte-identical.
3. Candidate-stable-changed classification is permitted only after that gate.

Observed:

| Measure | Result |
|---|---:|
| control-stable pixels | `108 / 307200` |
| control-stable fraction | `0.0003515625` |
| candidate-stable-changed pixels | `0` |

Eight corresponding A1/A2 frame pairs were decoded- and PNG-identical:
`1, 2, 5, 6, 9, 10, 13, 14`. All 15 corresponding B/A2 frame pairs were also
decoded- and PNG-identical. Those observations do not override the ordered
acceptance rule: the global control-agreement gate failed before causal effect
classification. There is also no independent proof that face 8 was in view.

## Interpretation and next experiment

The run demonstrates that the frozen lifecycle and retail/candidate substitution
can be executed reproducibly on the hardware path. It does not join the static
decode to a visible runtime effect.

Before another causal inference, commit and preregister a new stable-camera or
steady-state packet that:

- produces control agreement above its frozen threshold;
- independently localizes face 8 in view;
- preserves the retail-executable, one-byte candidate, renderer, level, audit,
  capture, and fail-closed identity gates;
- defines the effect and competing outcomes before launch.

That successor is now frozen offline as
[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]. It
first calibrates a retail-only `SIGSTOP` freeze and then runs an orthogonal
face-index localizer. The one-byte candidate remains out of scope until that
localizer is separately accepted.

## Evidence and hygiene

Raw receipts, logs, captures, masks, and `comparison.json` are retained under
the ignored work-copy evidence root
`work/copies/EXP-20260819-009/evidence/`. The accepted namespace contains only
`A1-005`, `B-001`, and `A2-001`. The Wine `R:` mapping was restored after A2.
All six retained lifecycle audits were clear, the final audit was clear, and no
runtime processes, capture sinks, or open sessions remained.

James independently reproduced the `108 / 307200` control mask and zero
candidate-stable-changed mask, verified the lifecycle and arm evidence, and
accepted this interpretation as an inconclusive R2 run rather than roadmap
closure.

## Links

- [[EXP-20260818-008 - R2a Anthill static mesh causal candidate]]
- [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
- [[PC LEVEL DAT static mesh]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[2026-08-19 0135 - Codex - Anthill R2b inconclusive causal runtime]]
