---
type: experiment
id: EXP-20260812-010
date: 2026-08-12
question: Do reciprocal guarded Training target rebinds change only the selected placement's visible render content under the PC Direct3D path?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; ImageMagick 7
working_directory: /home/dev/ABLPC
configuration: Exact-hash Training control and reciprocal record-124/125 guarded candidates; Direct3D hardware 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-010-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-102953
  - dynamic/wine/RUN-WINE-20260812-103136
  - dynamic/wine/RUN-WINE-20260812-103354
addresses:
  - 0x0044BD4A
  - 0x00449E1A
  - 0x0045A7F0
file_offsets:
  - 0x26F8
  - 0x2718
  - 0x111E4
  - 0x1319C
result: selected-positive-target-controls-placement-local-visible-render-content
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/rendering
  - implementation/modding
---

# EXP-20260812-010 - Training target rebind visible substitution

## Question

Do reciprocal guarded Training target rebinds change only the selected
placement's visible render content under the PC Direct3D path?

## Inputs

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Record 124 manifest: `mods/training-primary-record-124-target-111e4.json`
- Record 125 manifest: `mods/training-primary-record-125-target-1319c.json`
- Static/file evidence: [[EXP-20260812-009 - Training payload target structure and reuse census]]
- Prior placement-local visual evidence:
  [[EXP-20260812-008 - Training record watchpoints and individual roles]]

No PS1 source was consulted.

## Procedure

1. Stage each manifest from the exact source hash and confirm the output hash,
   receipt, and byte locality.
2. Launch an unchanged control and both candidates through `R:\PC\BUGS` or the
   equivalent `S:\PC\BUGS` work-copy shape.
3. At the initial selector, press Down to select the second option. Accept a
   run only if its log contains `Screen mode 640x480x16 selected` and
   `Starting Direct3D renderer`, and does not enter `INITSOFTRENDER`.
4. Select Training, stop at the natural title pause, press a key, and request
   15 native 640×480 Gamescope screenshots at approximately 0.2-second
   intervals.
5. Compare same-index frames. Select the first phase where both candidate
   comparisons are exactly identical to the control outside the affected
   placement boxes.
6. Preserve captures only under ignored work storage. Commit hashes, logs,
   receipts, measurements, and reproduction metadata.

## Expected

If the positive target supplies reusable render content, changing only the
guarded target field should alter the selected placement's visible geometry.
If it is unrelated, the placement should remain unchanged or another bounded
effect should appear. Any crash, load rejection, software-renderer run, or
uncontrolled animation difference must remain distinct from a content result.

## Observed

### Staging and acceptance

- Record 124 output SHA-256:
  `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`.
  Only target field `0x26F8–0x26FB` was selected; for these values only bytes
  `0x26F8–0x26F9` differ.
- Record 125 output SHA-256:
  `b8ea00be86de53a9b659a20f8b0023369e687c9309b61dd61fe8496393d90ed9`.
  Only target field `0x2718–0x271B` was selected; for these values only bytes
  `0x2718–0x2719` differ.
- Control and candidates all selected Direct3D hardware at 640×480×16, loaded
  `level07\level1.dat`, completed `InitMainGame`, and entered `NextLife`.

### Phase-matched visual result

Frame 07 was the first same-index phase in which both candidate comparisons
were pixel-identical to the control outside their affected placement boxes.

| Rebind | Differing pixels | Exact difference union | Outside-union differences | Prior move-away box |
|---|---:|---:|---:|---:|
| Record 124, `0x1319C → 0x111E4` | 2,980 | `61x242+369+0` | 0 | `52x241+369+0` |
| Record 125, `0x111E4 → 0x1319C` | 1,076 | `24x127+616+101` | 0 | `24x99+616+124` |

The rebind boxes occupy the same screen locations independently isolated by
forcing records 124 and 125 outside selection in `EXP-20260812-008` (the
center/placement distinction was resolved by `EXP-20260812-011`). The selected target
therefore changes visible render content at the selected placement while the
matched remainder of the frame stays byte-identical.

Evidence: `RUN-WINE-20260812-102953`, `RUN-WINE-20260812-103136`,
`RUN-WINE-20260812-103354`, and
`dynamic/wine/EXP-20260812-010-comparison.txt`.

## Confirmed

- Both guarded target rebinds are accepted by the exact PC executable under
  the hardware Direct3D path.
- For the tested masked-dispatch-`0x49` records, the positive target selected
  through payload `+0x1C` controls placement-local visible render content.
- The narrow target-rebind tool changes no bytes outside its selected
  four-byte field, and each phase-matched visual difference stays within the
  independently established placement region.

## Inferred

- Positive targets are reusable render-content inputs. Records that share one
  target can reuse that content under their own placement transforms.
- Other payload or record fields may still affect material, animation,
  transform, or final identity; the target is not proven to be a complete
  object definition.

## Unknown and limitations

- Exact meanings of the 12-byte entries, command modes, and item suffixes.
- Whether animation or other payload fields select variants within one target.
- Negative-count blocks, other dispatch classes, and non-Training runtime
  behavior.
- The capture sequence is wall-clock sampled rather than tied to an internal
  engine frame counter. Exact outside-region identity establishes the selected
  comparison phase; it does not make the full sequence deterministic.

## Contradictions and negative results

- A preliminary control accepted the default software option and entered the
  320×200 software path. It was rejected and is not evidence for this result.
- One fixed-delay record-124 screenshot contained broad animation-phase noise,
  while a repeat did not. The retained 15-frame sequences discriminate this:
  frame 07 has zero differences outside the placement-local unions. The noisy
  single capture is excluded from the conclusion.

## Result

Completed. Roadmap packet M1.2 is closed. Reciprocal PC-native runtime edits
confirm that the bounded positive target contributes reusable visible render
content at an independently identified placement.

## Follow-up

Begin [[Project Roadmap#M1.3 — Record selection and payload discrimination]] with isolated
record-126 edits to `+0x04` and `+0x08` under the same hardware renderer gate.
