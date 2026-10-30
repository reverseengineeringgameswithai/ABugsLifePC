---
type: experiment
id: EXP-20260812-032
date: 2026-08-12
question: Does the accepted plant-04-to-plant-10 pair replacement produce a stable replacement-local rendered difference along one fixed Training trajectory?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, windowed muted Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; ImageMagick 7.1.2-13
working_directory: /home/dev/ABLPC
configuration: Fresh unchanged/replacement/unchanged arms; exact paired PLANT04-to-PLANT10 replacement; fixed timestamped Training trajectory; Direct3D 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-032-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-223223
  - dynamic/wine/RUN-WINE-20260812-223921
  - dynamic/wine/RUN-WINE-20260812-224252
addresses:
  - 0x00416100
  - 0x00444C40
  - 0x00444CD8
  - 0x00448010
  - 0x00448079
file_offsets:
  - 0x394
result: bounded-negative-plant04-plant10-visible-route-retired
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - implementation/modding
---

# EXP-20260812-032 - Fixed trajectory paired plant replacement

## Question

Does the already accepted exact `PLANT04.ANM/.ALL <- PLANT10.ANM/.ALL`
replacement produce a stable, replacement-local rendered difference along one
fixed Training camera trajectory beyond matched control variance?

This is roadmap packet M2.19. It directly tests M2's rendered-outcome gate and
does not extend the unsafe caller-gate breakpoint work.

## Inputs and authority

- Exact unchanged PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact Training `LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Control plant 04 `.ANM/.ALL` hashes:
  `32dce9588272d4bd4d0b2054e58de2b9ca5ae563826d56f7cd12abe8b001e7ce`
  and
  `486bd73c54b96f9b0ef41e2c9ccc6029c95772619feaacb8885f4f1cc424f14a`.
- Replacement plant 10 `.ANM/.ALL` hashes:
  `12d2550ea89b9156acd04ce403d1754aa244d1cedf8531eaca2c8e7bf22b5194`
  and
  `0c0f244b5bef3b5a3f7148744aad9ac223b7fdeaeb0eecaa561193e7a30bf714`.
- The request origin, loader/consumer addresses, and earlier start-camera
  acceptance come from [[EXP-20260812-016 - Plant request origin and separate DAT table]],
  [[EXP-20260812-015 - Plant pair caller and consumer trace]], and
  [[EXP-20260812-019 - Same-size paired plant replacement]].

No PS1 source or finding was consulted. No executable or memory was modified.
All game-file changes were exact copies inside ignored trees under
`work/copies/EXP-20260812-032/`.

## Procedure

1. Reflink-copy three fresh trees from the exact derived PC source. Prove both
   controls recursively identical to it, excluding generated `bugs.log`.
2. In only the replacement tree, copy the exact plant 10 pair over the two
   plant 04 paths. Verify the two destinations against their source hashes and
   prove that no other staged path differs.
3. Map each arm in turn as Wine drive `R:` and launch
   `scripts/play-pristine.sh --research --windowed --mute`.
4. Send Down and Return separately to exact isolated Xwayland window
   `14680071`. Accept only a complete log containing the 640x480x16 and
   Direct3D markers and no `INITSOFTRENDER`.
5. Select Training and require `End InitMainGame`, `NextLife`, and the four
   plant 04/10 request lines. From the same natural title, send one Return.
6. Record three 640x480 game-surface samples at each of four anchors: start;
   after Up held three seconds; after Right held two seconds; and after a
   second Up held three seconds. Wait one second before each post-input sample
   group and approximately 0.4 seconds between samples.
7. Preserve exact key/capture timestamps and hashes. Compare same-index
   frames, all-pair phase proximity, three-sample temporal medians, and the
   intersection of per-sample difference masks at several thresholds.
8. Visually inspect representative direct, median, and intersection
   differences. Stop after the two replacement-to-control comparisons; do not
   widen the trajectory after a negative.

Every screenshot targeted only the isolated 640x480 Gamescope game surface,
never the desktop or whole screen. PNGs and generated masks remain ignored in
the experiment work tree; only logs and text receipts are curated.

## Expected discriminator

- A stable solid region that repeats in both replacement comparisons and
  exceeds the unchanged controls would link the exact plant paths to rendered
  content along this trajectory.
- Residuals confined to ordinary moving/camera edges, with no stable local
  region across both comparisons, would complete the bounded negative and
  retire this plant-04/10 visible route.

## Observed

### Hardware and load gates

Accepted runs are `RUN-WINE-20260812-223223` (control A),
`RUN-WINE-20260812-223921` (replacement), and
`RUN-WINE-20260812-224252` (control B). Each 1,480-line log records hardware
mode at line 76, Direct3D at line 127, plant 04/10 `.ANM/.ALL` loads at lines
1468–1471, `End InitMainGame` at line 1476, and `NextLife` at line 1478. None
contains `INITSOFTRENDER`.

After removing only the ten clock-calibration lines, all three logs are
byte-identical with SHA-256
`f47d9d3d648f0d9c3a951ea0135fa4fed29a91089ba653e0dcaf13fbc97cad18`.
The tested replacement therefore does not change the emitted load/init trace
at this boundary.

### Control repeatability and visual result

The fresh controls are byte-identical at 11 of 12 same-index trajectory
samples. All samples after the first start frame match exactly. The replacement
also exactly matches a control at three samples: start 1, start 3, and
after-up2 1.

At the remaining samples, low differences follow the player, stems, flowers,
ground texture, and camera-motion edges. The largest same-index delta occurs
at after-right sample 2 (`0.0792866` normalized RMSE) when the camera transition
is at a different phase; the adjacent samples are only `0.0110342` and
`0.0128991`. Three-sample temporal-median replacement-to-control RMSE is
`0.0221729`, `0.0165925`, `0.0491928`, and `0.0127760` at start, after-up1,
after-right, and after-up2 respectively.

The intersection of all three replacement difference masks at each anchor
contains zero pixels at start and after-up2. At after-up1 and after-right it
contains only 8 and 13 pixels at a 5% channel threshold, and 3 and 0 pixels at
10%. Visual review shows sparse thin animated/transition edges, not a solid
replacement-local region. Exact sample metrics and hashes are retained in
`dynamic/wine/EXP-20260812-032-comparison.txt`.

### Rejections and contradiction

The first control-A preflight used a staged physical path while `R:` still
resolved to the pristine tree; it failed the CD-path gate before renderer
selection and contributes no evidence.

One replacement attempt and the first control-B attempt reached the Training
loading screen but stalled at the same 954-line pre-resource boundary with
high CPU. Their ignored log SHA-256 values are
`c853ebb70ec8700d92cd2edef384fc2ee11723ce3d4068c61044dd604a998abf`
and `ce0f292cf10302e3fc473b588bca84f1f423021b3c6210103c88efc2c570d4ca`.
Because the same stall occurred before resource loading in replacement and
unchanged arms, it is not evidence about the substituted plant pair. Each was
rejected and followed by a clean prefix restart and accepted run.

## Confirmed

- The exact paired replacement is accepted under hardware Direct3D and the
  complete fixed trajectory in a fresh staged tree.
- The accepted arms emit byte-identical normalized load/init logs and all
  reach `NextLife`.
- The controls reproduce exactly at 11 of 12 same-index frames.
- No stable replacement-local visual region is discriminated in either
  replacement comparison along this bounded trajectory.

## Inferred

The non-exact replacement frames are best explained by ordinary animation and
camera phase because their residuals follow moving/transition edges, exact
matches recur, and no stable solid region survives the repeated masks. This is
an inference from the matched capture evidence, not a semantic claim about
either file format.

## Unknown and limitations

- The result does not prove that plant 04/10 files are unused, invisible in
  every camera/event, or generally interchangeable.
- Input is timestamped and control-repeatable but is not synchronized to an
  internal engine frame. Game-surface capture is asynchronous.
- Complete `.ALL` layout, nested `.ANM` meaning, and the M1 placement-to-file
  dependency remain unknown.
- The cause of the two pre-resource loading stalls is unknown and is not
  assigned to the replacement.

## Result and follow-up

M2.19 is complete under its bounded-negative condition. Retire the
plant-04/10 direct visible-outcome route rather than expanding its camera path
or returning to the unsafe caller gate.

The next M2 packet should test a different PC-native, Training-loaded content
family with a safer visible discriminator. The exact character candidates
`CD/CHARS/FLICK.ANM/.ALL` and `CD/CHARS3/FLICKD.ANM/.ALL` provide a bounded
one-file opportunity: their `.ANM` files are byte-identical, while their
equal-size `.ALL` files differ. This candidate selection is based only on the
PC census and Training log and does not yet assign character/model semantics.
