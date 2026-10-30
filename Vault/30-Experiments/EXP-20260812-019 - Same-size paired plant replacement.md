---
type: experiment
id: EXP-20260812-019
date: 2026-08-12
question: Does replacing both PLANT04.ANM and PLANT04.ALL with the exact equal-size plant 10 pair remain loadable and visibly change the Training start camera?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; GStreamer 1.28.4; ImageMagick 7.1.2-13
working_directory: /home/dev/ABLPC
configuration: Exact equal-size PLANT10.ANM and PLANT10.ALL bytes at the two staged PLANT04 paths; Direct3D hardware 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-019-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-140325
  - dynamic/wine/RUN-WINE-20260812-141020
addresses:
  - 0x00444C40
  - 0x00444CD8
  - 0x00444B70
  - 0x00448079
  - 0x00448010
file_offsets: []
result: accepted-no-visible-change-at-tested-start-camera
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - implementation/modding
---

# EXP-20260812-019 - Same-size paired plant replacement

## Question

Does replacing both `PLANT04.ANM` and `PLANT04.ALL` with the exact existing
plant 10 pair in a staged user-owned copy remain loadable under the exact PC
executable, and does it produce a stable visible change at the Training start
camera?

## Inputs

- `bugs.exe` SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Control `PLANT04.ANM`, size `0x70A`, SHA-256:
  `32dce9588272d4bd4d0b2054e58de2b9ca5ae563826d56f7cd12abe8b001e7ce`
- Replacement-source `PLANT10.ANM`, size `0x70A`, SHA-256:
  `12d2550ea89b9156acd04ce403d1754aa244d1cedf8531eaca2c8e7bf22b5194`
- Control `PLANT04.ALL`, size `0xE08`, SHA-256:
  `486bd73c54b96f9b0ef41e2c9ccc6029c95772619feaacb8885f4f1cc424f14a`
- Replacement-source `PLANT10.ALL`, size `0xE08`, SHA-256:
  `0c0f244b5bef3b5a3f7148744aad9ac223b7fdeaeb0eecaa561193e7a30bf714`
- Static/runtime boundaries: [[EXP-20260812-015 - Plant pair caller and consumer trace]],
  [[EXP-20260812-017 - Bounded PC ANM inspector]], and
  [[EXP-20260812-018 - Same-layout PC ANM replacement]].

No PS1 source or finding was consulted.

## Procedure

1. Create separate ignored control and replacement trees below
   `work/copies/EXP-20260812-019/` from the exact derived PC tree.
2. Verify the executable and all four exact plant input hashes. Prove the
   control is byte-identical to the source. Copy exact plant 10 `.ANM` and
   `.ALL` bytes over the two replacement plant 04 paths.
3. Prove that the two destinations equal their exact sources and that those
   are the only staged path differences, both before execution and afterward
   when generated `bugs.log` is excluded.
4. Map the arms as `U:` and `V:` in the existing baseline Wine prefix and
   launch each with `scripts/play-pristine.sh --research`.
5. At the initial selector choose the second option. Reject a run without
   `Screen mode 640x480x16 selected` and `Starting Direct3D renderer`, or one
   containing `INITSOFTRENDER`.
6. Select Training, leave its natural title pause, require `End InitMainGame`
   and `NextLife`, and retain the accepted game logs.
7. Capture 15 2560×1440 Gamescope PipeWire frames per accepted arm after
   `NextLife`, crop the centered 1920×1440 game image, point-sample it to
   640×480, and compare all frame pairs and temporal medians.
8. Compare the current median delta with the two independent control medians
   retained by `EXP-20260812-018`.

## Expected discriminator

- If the exact pair has a stricter incompatibility, the substituted arm may
  reject, fault, or fail to reach gameplay.
- If the pair supplies visible plant identity at this camera, a stable bounded
  replacement-only region should exceed control animation variance.
- If the pair is accepted but its role is off-camera, nonvisual, or selected
  elsewhere, both arms should reach gameplay without such a stable region.

## Observed

### Staging and byte locality

- The control recursively matched the exact source tree before execution.
- The replacement differed at exactly
  `CD/PLANTS/PLANT04.ANM` and `CD/PLANTS/PLANT04.ALL`.
- Each staged destination was byte-identical to its exact plant 10 source.
- The ANM inputs differ at 884 byte positions from zero-based offsets `0x26`
  through `0x708`. The ALL inputs differ at 3,087 positions from `0x4`
  through `0xDEF`.
- Post-run locality is unchanged when generated `bugs.log` is excluded.

Equal sizes constrain this exact staging experiment. They do not establish
equal `.ALL` layout, semantic compatibility, or a public replacement rule.

### Hardware-gated acceptance

Both `RUN-WINE-20260812-140325` (control) and
`RUN-WINE-20260812-141020` (replacement):

- contain exactly one `Screen mode 640x480x16 selected` marker;
- contain exactly one `Starting Direct3D renderer` marker;
- contain no `INITSOFTRENDER` marker;
- load `level07\level1.dat`, then plant 04 and plant 10 `.ANM`/`.ALL` paths;
- complete `InitMainGame` and reach `NextLife`.

One preceding replacement launch entered `INITSOFTRENDER` because the opening
selector retained the default software path. It was rejected before capture,
and its log was replaced by the accepted rerun. It contributes no result.

After normalizing only the `U:`/`V:` drive label and removing the ten
diagnostic `->time[]` lines, the two 1,480-line accepted logs are byte-identical
with SHA-256 `73a6a08e…25110`—the same normalized trace hash retained for
M2.5. The substituted pair therefore does not alter the game's emitted load
and initialization trace at this boundary.

### Visual comparison

Both arms contain 15 2560×1440 compositor frames with the same centered
1920×1440 game presentation. After exact point-sampled normalization:

- closest all-pairs match: control frame 12 versus replacement frame 06;
- differing pixels: 22,627 of 307,200 (7.36556%);
- normalized RMSE: `0.0272229`.

The current temporal medians differ by 33,485 pixels with normalized RMSE
`0.0357224`. The prior M2.5 primary-control versus current-control median is
`0.0267928` RMSE; the prior control-rerun versus current-control median is
`0.0387554`. The paired replacement delta lies inside that independent
control-to-control range.

Visual inspection shows the same scene content. Residuals follow moving
characters, stems, flowers, and object edges rather than a stable
replacement-only region. The capture is wall-clock sampled rather than tied
to an internal engine frame.

Exact hashes and measurements are retained in
`dynamic/wine/EXP-20260812-019-comparison.txt`; screenshots remain ignored
with the user-owned work copies.

## Confirmed

- The exact PC executable accepts the equal-size plant 10 `.ANM`/`.ALL` pair
  at the two plant 04 request paths under the Direct3D hardware path.
- The substituted pair reaches Training gameplay through `NextLife`.
- Within the recorded start-camera procedure, no stable visible change is
  discriminated beyond independently measured control animation variance.

## Inferred

- This exact whole-pair substitution satisfies the immediate consumers well
  enough to reach gameplay. It does not establish a general pair-compatibility
  rule.
- Further blind plant 04/10 whole-file swapping is unlikely to resolve the
  missing placement-to-resource identity at this camera. Suppressing the
  exact level-derived plant 04 request is a sharper next discriminator because
  it predicts a load-log change and can be compared with retained M1 masks.

## Unknown and limitations

- Later gameplay, complete animation cycles, off-camera instances, other
  levels, and nonvisual effects were not tested.
- Complete `.ANM` and `.ALL` semantics remain unknown.
- The result does not show that either file is unused or generally
  interchangeable.
- Which M1 20-byte placement or positive target, if any, consumes plant 04
  remains unresolved (`KU-023`).

## Result

Completed. M2.6 is classified
`accepted-no-visible-change-at-tested-start-camera`. It proves an exact
pair-acceptance boundary but not a visible asset mod or safe editing surface.

## Follow-up

Historical recommendation superseded by
[[EXP-20260812-020 - Training plant10 request suppression]]. Exact preflight
review showed that `0x394` and `0x3A4` share an occurrence cursor; the clean
one-byte discriminator suppressed plant 10 at `0x3A4`. Continue with
[[Project Roadmap#M2.8 — Plant 10 runtime consumer-to-placement bridge]].
