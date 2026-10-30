---
type: experiment
id: EXP-20260812-020
date: 2026-08-12
question: Does suppressing only the second Training 0x2B selector omit plant 10 requests, preserve initialization, and expose a stable M1-correlated visual mask?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; GStreamer 1.28.4; ImageMagick 7.1.2-13
working_directory: /home/dev/ABLPC
configuration: Training LEVEL1.DAT 0x3A4 changed from 0x2B to 0x00; Direct3D hardware 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-020-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-150528
  - dynamic/wine/RUN-WINE-20260812-150805
addresses:
  - 0x004161EA
  - 0x004161FA
  - 0x00445020
  - 0x00444C40
file_offsets:
  - 0x394
  - 0x3A4
result: plant10-request-omission-confirmed-no-stable-start-mask
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - re/file-format
---

# EXP-20260812-020 - Training plant10 request suppression

## Question

Does changing only the exact second Training type-`0x3F` selector at DAT
offset `0x3A4` from `0x2B` to a value outside the evidenced collector dispatch
range omit the plant 10 `.ANM`/`.ALL` request, preserve gameplay
initialization, and produce a stable visible mask that can be compared with
the independent M1 placements?

## Preflight correction and contradiction

The roadmap originally proposed changing `0x394` to suppress plant 04. Before
staging, exact instruction review at `0x004161EA–0x004161FA` showed that every
`0x2B` occurrence consumes and then advances one shared class-specific cursor
rooted at `0x004DEA10`. If the first `0x2B` at `0x394` were removed, the
second at `0x3A4` would consume the first constant, ID 4. That edit would
therefore remove plant 10 rather than plant 04.

This contradiction was not silently normalized. M2.7 was narrowed to the
clean one-byte discriminator at the second `0x2B`, `0x3A4`, which can omit ID
10 without shifting a later same-class selector. Direct plant-04 suppression
remains untested. No PS1 source or finding was consulted.

## Inputs and staging

- `bugs.exe` SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact control Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Suppression DAT SHA-256:
  `bcf6b8390f8ddcfebeb3411807f60f2dee0fc73a6cbd9d63a9daa1a3c7f1370e`
- Exact receipt: zero-based `0x3A4`, expected `0x2B`, replacement `0x00`.
  `cmp -l` reports only one-based byte 933, octal `053 → 000`.
- The control tree matched the exact source; excluding generated `bugs.log`,
  the suppression tree differed only at `CD/LEVEL07/LEVEL1.DAT`.
- Plant 04 and plant 10 `.ANM`/`.ALL` hashes were unchanged in both arms. Full
  hashes are retained in `EXP-20260812-020-comparison.txt`.

All game bytes and screenshots remained in ignored user-owned work copies.
No file below `originals/` was modified.

## Procedure

1. Map the control and suppression arms as `W:` and `X:` in the existing Wine
   prefix and launch each with `scripts/play-pristine.sh --research`.
2. At the opening selector, send Down once to the exact `Bugs` Xwayland
   window, then confirm. Reject any run without `Screen mode 640x480x16
   selected` and `Starting Direct3D renderer`, or with `INITSOFTRENDER`.
3. Select Training, leave its natural title pause, require `End InitMainGame`
   and `NextLife`, then capture 15 Gamescope PipeWire frames per arm.
4. Normalize only the drive label and ten `->time[]` diagnostics in logs.
   Crop each 2560×1440 capture to centered 1920×1440 gameplay and point-
   sample to 640×480. Compare all pairs, temporal medians, and three retained
   independent control medians from M2.5/M2.6.

## Observed

### Hardware-gated request result

Both `RUN-WINE-20260812-150528` (control) and
`RUN-WINE-20260812-150805` (suppression):

- contain exactly one required 640×480×16 marker and one Direct3D-start
  marker;
- contain no `INITSOFTRENDER` marker;
- complete `InitMainGame` and reach `NextLife`;
- retain plant 04 `.ANM` and `.ALL` requests.

The control contains 1,480 log lines and both plant 10 request lines. The
suppression arm contains 1,478 lines and neither plant 10 request. After
normalizing only drive labels and diagnostic timings, deletion of
`plant10.anm` and `plant10.all` is the entire diff. Plant 05, 04, and 06
requests and the surrounding initialization trace remain unchanged.

This runtime result independently confirms the class-cursor static model and
the exact `0x3A4` level-byte-to-plant-10 request dependency.

### Visual result and M1 gate

The closest all-pairs match is control frame 02 versus suppression frame 10:
28,279 of 307,200 pixels differ (9.2054%), normalized RMSE `0.0318984`.
Temporal medians differ by 36,487 pixels, RMSE `0.0419452`.

Three independent prior control medians compared with the current control at
RMSE `0.0422443`, `0.0437912`, and `0.0373585`. Their comparisons with the
suppression median are `0.0344740`, `0.0363679`, and `0.0366375`. The current
arm-to-arm delta lies inside ordinary independently measured control variance.
Residuals follow animated characters, stems, flowers, and object edges rather
than a stable suppression-only region.

Therefore no stable mask exists to compare meaningfully with the disjoint M1
record 124–126 masks. Pixel overlap in a temporally unstable residual is not
promoted to candidate placement/resource correspondence.

## Confirmed

- Training DAT byte `0x3A4 == 0x2B` is necessary for the plant 10 pair request
  in this exact scene state, given the unchanged earlier selector sequence.
- Changing only that byte to `0x00` removes both plant 10 load requests while
  retaining plant 04 and the remainder of the normalized initialization log.
- The exact PC executable accepts the suppressed arm under the required
  Direct3D hardware path and reaches Training `NextLife`.
- No stable start-camera visual mask is discriminated by the recorded
  wall-clock capture procedure.

## Inferred

- Plant 10 is either not represented by a stable uniquely visible start-camera
  element, shares/caches render content through another path, affects a later
  or off-camera state, or produces an effect hidden by uncontrolled animation.
  This experiment does not discriminate among those possibilities.

## Unknown and limitations

- Plant 04 cannot be cleanly suppressed by simply changing `0x394`, because
  that shifts the next `0x2B` to ID 4. A different guarded intervention is
  required.
- The direct M1 placement-to-resource identity (`KU-023`) remains open.
- Later gameplay, other cameras, deterministic internal-frame capture, and
  nonvisual effects were not tested.
- This one-byte dependency is evidence, not a public selector-editing API.
