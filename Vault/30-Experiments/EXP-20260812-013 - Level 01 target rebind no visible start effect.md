---
type: experiment
id: EXP-20260812-013
date: 2026-08-12
question: In the log-identified non-Training Level 01 scene, does a guarded positive dispatch-0x49 target rebind reproduce Training's placement-local visible substitution at the starting camera?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; ImageMagick 7
working_directory: /home/dev/ABLPC
configuration: Exact-hash Level 01 control, record-261 center candidate, and guarded target rebind; Direct3D hardware 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-013-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-114514
  - dynamic/wine/RUN-WINE-20260812-120021
  - dynamic/wine/RUN-WINE-20260812-121042
addresses:
  - 0x0044D430
  - 0x00449B61
  - 0x00449E1A
  - 0x0045A7F0
file_offsets:
  - 0x2968
  - 0x4E00
  - 0x4E1C
  - 0x3459C
  - 0x3703C
result: accepted-no-visible-change-at-level01-start-camera
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/rendering
  - re/file-format
  - implementation/modding
---

# EXP-20260812-013 - Level 01 target rebind no visible start effect

## Question

In one log-identified non-Training PC scene, does a guarded positive
dispatch-`0x49` target rebind reproduce Training's placement-local visible
substitution at the starting camera?

## Inputs and procedure

- The unchanged executable SHA-256 is
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- A hardware-gated unchanged menu run selected `ant hill`; its log, rather
  than the menu label, identifies `R:\PC\BUGS\cd\level01\level.dat`.
- The exact work-copy DAT SHA-256 is
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- The bounded scanner finds nine valid positive masked dispatch-`0x49`
  references to four unique targets with zero validation errors.
- Candidate-center discovery covered every matching record at the tested
  start camera. Record 261 was retained for a byte-local center control and a
  guarded rebind from its unique positive target `0x3703C` to contrasting
  same-file target `0x3459C`, which is shared by three records.
- Each retained arm used a fresh launch, explicit hardware log gate, accepted
  Level One title input, and a 15-frame native 640×480 capture sequence.

No PS1 source was consulted.

## File evidence

Primary record 261 begins at `0x2968`:

- candidate center `(4685, -4948, -762)`;
- positive signed `+0x0C` value `954`;
- flags `0x0049`;
- payload offset `0x4E00`;
- target pointer field at payload `+0x1C`, file offset `0x4E1C`;
- original target `0x3703C`, positive count `32`;
- replacement target `0x3459C`, positive count `131`.

`mods/level01-primary-record-261-candidate-far.json` changes component 0 from
`4685` to `50000`. Its output SHA-256 is
`ef43ee54e9283bac7280251dad9ad664b35ec02aa63ef9494bd36037f5b10384`,
and only bytes `0x2968–0x2969` differ.

`mods/level01-primary-record-261-target-3459c.json` requires old target
`0x3703C` and writes `0x3459C`. Its output SHA-256 is
`80649462f3e5e4010218ba04a20e2356ea981b5e29b651dacd7ecf4bff39965b`,
and only bytes `0x4E1C–0x4E1D` differ. Both receipts validate the complete old
and new positive blocks before editing.

## Runtime result

All three accepted logs contain:

- `Screen mode 640x480x16 selected`;
- `Starting Direct3D renderer`;
- the Level 01 DAT load;
- `End InitMainGame` and `NextLife`;
- no `INITSOFTRENDER`.

Frame 03 is byte-identical across the unchanged, center, and rebind arms with
SHA-256
`e79c0a1cac5eb7632c4f14fb4d74afc2d2cf078ebdd20fed355f8962545e77da`.
The center arm has eleven same-index exact frames; the rebind arm has four.
Other frames contain ordinary idle character and particle-animation phase
differences. Evidence: `RUN-WINE-20260812-114514`,
`RUN-WINE-20260812-120021`, `RUN-WINE-20260812-121042`, and
`dynamic/wine/EXP-20260812-013-comparison.txt`.

## Confirmed

- The `ant hill` selection loads the second exact PC DAT hash above.
- The supported center edit and guarded target rebind are byte-local and are
  accepted by the unchanged executable under the Direct3D hardware path.
- Neither edit has a visible effect at the tested Level 01 starting camera.
- Supported edits have now been accepted by the original executable against
  both the Training DAT and Level 01 DAT.

## Inferred

- The nine matching Level 01 records are outside selection or otherwise
  visually inactive at this specific camera. This is consistent with every
  discovery arm retaining exact control frames, but their later in-level
  positions are not identified.

## Unknown and limitations

- Whether record 261 becomes selected later in Level 01, and whether the same
  target rebind then changes visible content, remain unknown.
- No visible Level 01 placement is assigned to any of the nine records.
- This no-change result does not weaken Training's visible substitution; it
  bounds runtime observability to a different file and camera.

## Contradictions and negative results

- The first-pass expectation that one eligible record would be visible at the
  non-Training start camera was not met. This difference is retained rather
  than normalized to the Training result.
- Runs that stayed on a menu/title, began at a mismatched idle phase, or
  entered `INITSOFTRENDER` were rejected. Sent input alone was not accepted as
  evidence; each retained arm is gated by its game log.

## Result and follow-up

Completed with a bounded no-visible-change result. This closes M1.4: the
format/tool boundary validates across the corpus, and exact guarded edits are
accepted by the original executable on a second level file. M1.5 should audit
and promote only this demonstrated boundary into the user-facing tool and
regression surface.
