---
type: experiment
id: EXP-20260812-011
date: 2026-08-12
question: Do isolated +512 edits to Training record 126 fields +0x04 and +0x08 move its visible content, or do those fields act upstream of dispatch-0x49 render placement?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; ImageMagick 7
working_directory: /home/dev/ABLPC
configuration: Exact-hash Training control and record-126 +0x04/+0x08 candidates; Direct3D hardware 640x480x16 only
artifacts:
  - static/exports/BIN-97c95ba5572dce63/FUN_0044d430-record-field-reads.txt
  - dynamic/wine/EXP-20260812-011-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-105947
  - dynamic/wine/RUN-WINE-20260812-110202
  - dynamic/wine/RUN-WINE-20260812-110625
addresses:
  - 0x0044D59F
  - 0x0044D612
  - 0x0044D623
  - 0x0044D6AD
  - 0x00449B61
file_offsets:
  - 0x0E8C
  - 0x0E90
result: fields-are-upstream-center-candidates-not-dispatch-0x49-render-placement
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/rendering
  - re/file-format
---

# EXP-20260812-011 - Training record center candidates

## Question

Do isolated `+512` edits to Training record 126 fields `+0x04` and `+0x08`
move its visible content, or do those fields act upstream of dispatch-`0x49`
render placement?

## Inputs and procedure

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Primary record 126 at `0x0E88`, original tuple `(872, -757, 70)`.
- Candidate tuples `(872, -245, 70)` and `(872, -757, 582)`.
- Exact static reads were recorded before runtime interpretation.
- Each candidate and an unchanged control used the hardware renderer gate and
  a 15-frame native Gamescope sequence after the Training title pause.

No PS1 source was consulted.

## Static evidence

- `0x0044D59F` and `0x0044D6AD` read record `+0x08` as a dword for two
  center-distance candidate tests.
- `0x0044D612` reads record `+0x04` as a word and `0x0044D623` reads `+0x08`
  as a word for the camera-relative candidate transform.
- In the masked dispatch-`0x49` path, `0x00449B61` replaces the selected record
  pointer with record `+0x10`, the relocated payload. The path then consumes
  that payload's first three dwords for render placement and passes payload
  `+0x1C` onward at `0x00449E1A`.

Evidence:
`static/exports/BIN-97c95ba5572dce63/FUN_0044d430-record-field-reads.txt`
and the exact PC export for `0x004498F0`.

## Runtime result

Both candidates:

- changed one source byte inside only the selected four-byte field;
- passed `Screen mode 640x480x16 selected` and
  `Starting Direct3D renderer` without `INITSOFTRENDER`;
- loaded Training, completed `InitMainGame`, and entered `NextLife`;
- produced a frame-08 SHA-256 identical to the control:
  `bfece149ba83b20a632cd9dc4a88c0fa1c1581cb927f30a64a3147252ab0ae6f`.

Exact differing pixels for both comparisons at frame 08: zero. Full hashes,
receipts, and sequence reconciliation are in
`dynamic/wine/EXP-20260812-011-comparison.txt`.

## Confirmed

- The two `+512` edits do not move or otherwise change record 126's visible
  render output in the matched Training start phase.
- The fields feed upstream candidate selection in `0x0044D430`; dispatch
  `0x49` switches to relocated record `+0x10` before its render-placement math.
- The earlier `+0x00 = 50000` result demonstrates selection loss, not visible
  translation of the render content.

## Inferred

- Record `+0x00`, `+0x04`, and `+0x08` form a visibility-center tuple for the
  bounded dispatch path. Exact world-axis names and units remain unconfirmed.

## Unknown and limitations

- A center edit that crosses a candidate threshold at another camera position
  can still change visibility.
- Other scene dispatches may use the same record fields differently after
  selection.
- Wall-clock sequence phases are not deterministic; frame 08 is retained
  because all three image byte strings are identical.

## Contradictions and negative results

- Earlier notes called the tuple a position candidate and described the
  `+0x00 = 50000` experiment as moving a placement away. Static pointer flow
  plus the accepted no-movement candidates discriminate that interpretation
  for dispatch `0x49`: the tuple selects visibility while payload data places
  the rendered content.
- One preliminary `+0x08` run reached Direct3D but did not accept the Training
  menu input. It was rejected before capture and is not result evidence.

## Result and follow-up

Completed. Test positive record `+0x0C` as the statically observed visibility
bound, then reconcile `+0x0E` flags and relocated `+0x10` to close M1.3.
