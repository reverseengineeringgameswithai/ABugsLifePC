---
type: experiment
id: EXP-20260812-018
date: 2026-08-12
question: Does substituting PLANT10.ANM for PLANT04.ANM while retaining PLANT04.ALL remain loadable and visibly change the Training start camera?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; GStreamer 1.28.4; ImageMagick 7.1.2-13
working_directory: /home/dev/ABLPC
configuration: Exact same-size/same-first-level-layout PLANT10.ANM bytes at staged PLANT04.ANM; PLANT04.ALL unchanged; Direct3D hardware 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-018-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-134225
  - dynamic/wine/RUN-WINE-20260812-134512
addresses:
  - 0x00444CD8
  - 0x00444B70
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

# EXP-20260812-018 - Same-layout PC ANM replacement

## Question

Does replacing `PLANT04.ANM` with the exact existing `PLANT10.ANM` bytes in a
staged user-owned copy—while retaining `PLANT04.ALL`—remain loadable under the
exact PC executable, and does it visibly change the Training start camera?

## Inputs

- `bugs.exe` SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Control `PLANT04.ANM` SHA-256:
  `32dce9588272d4bd4d0b2054e58de2b9ca5ae563826d56f7cd12abe8b001e7ce`
- Replacement-source `PLANT10.ANM` SHA-256:
  `12d2550ea89b9156acd04ce403d1754aa244d1cedf8531eaca2c8e7bf22b5194`
- `PLANT04.ALL` SHA-256 in both arms:
  `486bd73c54b96f9b0ef41e2c9ccc6029c95772619feaacb8885f4f1cc424f14a`
- Static/format evidence: [[EXP-20260812-015 - Plant pair caller and consumer trace]]
  and [[EXP-20260812-017 - Bounded PC ANM inspector]].

No PS1 source or finding was consulted.

## Procedure

1. Create separate ignored control and replacement trees below
   `work/copies/EXP-20260812-018/` from the exact derived PC tree.
2. Prove the control tree is byte-identical to the source tree. Copy exact
   `PLANT10.ANM` bytes over replacement `PLANT04.ANM`; recursively verify that
   this is the only staged path difference and that `PLANT04.ALL` is unchanged.
3. Map control and replacement as `S:` and `T:` in the existing baseline Wine
   prefix. Launch both with `scripts/play-pristine.sh --research`.
4. At the initial selector, press Down to choose the second option. Reject a
   run without `Screen mode 640x480x16 selected` and `Starting Direct3D
   renderer`, or one containing `INITSOFTRENDER`.
5. Select Training, leave its natural title pause, require `End InitMainGame`
   and `NextLife`, and retain the game logs.
6. Capture 15 Gamescope PipeWire frames after `NextLife` at approximately
   0.2-second intervals. Normalize the centered 4:3 compositor image to
   640×480 with point sampling and compare all control/replacement pairings.
7. Repeat the control at the replacement arm's exact 2560×1440 compositor
   size. Compare closest frames and temporal medians, retaining only hashes and
   measurements in Git; keep screenshots with ignored user-owned work copies.

## Expected

- If the `.ANM` alone supplies visible resource identity compatible with the
  retained `.ALL`, the replacement should load and change a stable bounded
  region.
- If the files have a stricter pair contract, loading may fail.
- If `.ANM` is accepted but its effect is not visible at this camera, both runs
  should reach gameplay without a stable replacement-only visual difference.

## Observed

### Staging and byte locality

- Both `.ANM` inputs are exactly `0x70A` bytes and have the same M2.4
  first-level offsets/counts.
- Staged `PLANT04.ANM` is byte-identical to the exact `PLANT10.ANM` source.
- The control matches the source tree. The replacement differs from the source
  at exactly `CD/PLANTS/PLANT04.ANM` when generated `bugs.log` is excluded.
- Control and replacement ANM bytes differ at 884 positions from file offsets
  `0x26` through `0x708`. `PLANT04.ALL` is unchanged in both arms.

### Hardware-gated acceptance

Both `RUN-WINE-20260812-134512` (control) and
`RUN-WINE-20260812-134225` (replacement):

- contain exactly one `Screen mode 640x480x16 selected` marker;
- contain exactly one `Starting Direct3D renderer` marker;
- contain no `INITSOFTRENDER` marker;
- load `level07\level1.dat`, then both plant 04 and plant 10 `.ANM`/`.ALL`
  pairs;
- complete `InitMainGame` and reach `NextLife`.

After normalizing only the `S:`/`T:` drive label and removing the ten
diagnostic `->time[]` lines, the two 1,480-line logs are byte-identical with
SHA-256 `73a6a08e…25110`. Without removing timings, only indices 4 and 6 differ
by one timing unit.

### Visual comparison

The primary same-size arms each contain 15 2560×1440 compositor frames with a
centered 1920×1440 game image. After exact point-sampled normalization:

- closest pairing: control frame 01 versus replacement frame 15;
- differing pixels: 37,501 of 307,200 (12.2074%);
- normalized RMSE: `0.0390463`.

Visual inspection shows the same scene content. The remaining differences
follow moving characters, stems, flowers, and object edges rather than a stable
replacement-only region. The wall-clock sequence is not engine-frame locked.

Temporal-median comparison supplies a control-variance check:

| Comparison | Differing pixels | Normalized RMSE |
|---|---:|---:|
| Auxiliary control vs replacement | 36,045 | 0.0416820 |
| Auxiliary control vs primary control | 37,206 | 0.0416703 |
| Primary control vs replacement | 44,425 | 0.0532419 |

The replacement delta is comparable to ordinary control-to-control animation
variance. No stable visible change is discriminated at the tested start camera.
Exact set/frame/log hashes are preserved in
`dynamic/wine/EXP-20260812-018-comparison.txt` and the two run metadata files.

## Confirmed

- The exact PC executable accepts this same-size, same-first-level-layout
  `.ANM`-only substitution with the destination `.ALL` unchanged under the
  Direct3D hardware path.
- The replacement reaches Training gameplay through `NextLife`.
- Within the recorded start-camera procedure, no stable visible change is
  discriminated beyond measured control-to-control animation variance.

## Inferred

- Equal first-level layout is sufficient for acceptance in this exact pair and
  load path; it is not established as a general compatibility rule.
- A paired `.ANM`/`.ALL` replacement is now the sharper next discriminator for
  visible plant identity because `.ANM` alone did not supply a visible result
  here.

## Unknown and limitations

- Later gameplay, complete animation cycles, off-camera instances, other
  levels, and nonvisual behavior were not tested.
- The result does not show that `.ANM` is unused or interchangeable generally.
- The capture is wall-clock sampled, not tied to an internal frame counter.
- `.ALL` layout and complete pair semantics remain unknown.

## Result

Completed. M2.5 is classified
`accepted-no-visible-change-at-tested-start-camera`. This satisfies the
bounded replacement-acceptance result but not M2's visible asset-family exit
gate.

## Follow-up

Execute [[Project Roadmap#M2.6 — Same-size paired plant replacement]]: replace
both plant 04 files with the existing equal-size plant 10 pair in a new staged
copy and repeat the exact hardware/load/visual gates.
