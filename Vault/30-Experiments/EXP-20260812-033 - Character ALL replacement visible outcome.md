---
type: experiment
id: EXP-20260812-033
date: 2026-08-12
question: Does exact equal-size CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL produce an accepted repeated stable local rendered difference along the fixed Training trajectory?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, windowed muted Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; ImageMagick 7.1.2-13
working_directory: /home/dev/ABLPC
configuration: Fresh unchanged/replacement/unchanged arms; exact one-path equal-size ALL replacement; fixed Training trajectory; Direct3D 640x480x16 only
artifacts:
  - dynamic/wine/EXP-20260812-033-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-230859
  - dynamic/wine/RUN-WINE-20260812-231216
  - dynamic/wine/RUN-WINE-20260812-231403
addresses:
  - 0x004AE240
file_offsets:
  - 0x4
  - 0x34D2
result: positive-bounded-one-path-character-render-link
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - implementation/modding
---

# EXP-20260812-033 - Character ALL replacement visible outcome

## Question

Does exact equal-size `CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL` produce an
accepted, repeated stable local rendered difference along the fixed Training
trajectory?

This is roadmap packet M2.20. It tests a second PC-only content family after
[[EXP-20260812-032 - Fixed trajectory paired plant replacement]] retired the
plant-04/10 visible route.

## Inputs and authority

- Exact unchanged PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact Training `LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Both companion `.ANM` files are byte-identical, size `0x2C83E`, SHA-256
  `1743b26a13770b6453dfcf900d9f02a515e52a1b04e5679149c06ec77e5e8ab1`.
- Unchanged `CHARS/FLICK.ALL` is `0x34EC` bytes, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`.
- Replacement `CHARS3/FLICKD.ALL` is also `0x34EC` bytes, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- The `.ALL` files differ at 2,115 byte positions from zero-based `0x4`
  through `0x34D2`.
- [[PC Content Census]] and retained accepted Training logs supply the exact
  PC path/load anchor. `0x004AE240` produces the recorded load lines, but this
  experiment does not assign the selected file's first format consumer.

No PS1 source or finding was consulted. No executable, memory, DAT, or `.ANM`
was modified. The only changed game path was an exact copy inside ignored
`work/copies/EXP-20260812-033/replacement/`.

## Procedure

1. Reflink-copy three fresh trees from the exact derived PC source. Prove both
   controls recursively identical to it, excluding generated `bugs.log`.
2. In only the replacement tree, copy exact `CHARS3/FLICKD.ALL` bytes over
   `CHARS/FLICK.ALL`. Verify the destination source hash and prove that no
   other staged path differs.
3. Map each arm in turn as Wine drive `R:` and launch
   `scripts/play-pristine.sh --research --windowed --mute`.
4. Send Down and Return separately to exact isolated Xwayland window
   `14680071`. Accept only a complete log containing the 640x480x16 and
   Direct3D markers and no `INITSOFTRENDER`.
5. Select Training, retain the natural title boundary, send one title Return,
   and require both selected path loads, `End InitMainGame`, and `NextLife`.
6. Record three 640x480 game-surface samples at each fixed anchor: start;
   after Up held three seconds; after Right held two seconds; and after a
   second Up held three seconds. Preserve exact key/capture timestamps and
   hashes.
7. Compare raw and clock-normalized logs, same-index frames, temporal medians,
   and local masks. At each anchor, compare all three replacement frames with
   all six control frames and intersect the resulting 18 masks at 2%, 5%, and
   10% grayscale thresholds.
8. Visually inspect representative direct frames and intersection masks. Stop
   after this exact one-path discriminator; do not parse or edit unknown
   `.ALL` fields.

Every screenshot targeted only the isolated 640x480 Gamescope game surface,
never the desktop or whole screen. PNGs and generated masks remain ignored in
the experiment work tree; only logs, receipts, hashes, metrics, and metadata
are curated.

## Expected discriminator

- A repeated solid local region that survives both fresh controls and all
  sampled phases would link the exact loaded path to rendered content.
- Rejection, a crash, or only ordinary background/camera/animation residuals
  would leave the character-family route unresolved or close it negatively.

## Observed

### Hardware, load, and acceptance gates

Accepted runs are `RUN-WINE-20260812-230859` (control A),
`RUN-WINE-20260812-231216` (replacement), and
`RUN-WINE-20260812-231403` (control B). Every 1,480-line log records hardware
mode at line 76, Direct3D at line 127, `CHARS/FLICK.ANM/.ALL` loads at lines
1459–1460, `End InitMainGame` at line 1476, and `NextLife` at line 1478. None
contains `INITSOFTRENDER`.

After removing only the ten clock timing lines, all three logs are
byte-identical with SHA-256
`f47d9d3d648f0d9c3a951ea0135fa4fed29a91089ba653e0dcaf13fbc97cad18`.
The replacement therefore changes no emitted load/init line at this boundary.

### Repeated rendered region

The unchanged controls are byte-identical at start samples 1 and 3. Later
same-index control RMSE ranges from `0.0508476` to `0.0720664`, so global
trajectory metrics are not independently discriminating there.

The stricter 18-way intersection is local and repeated. At a 5% grayscale
threshold it retains:

- start: 689 pixels in `41x195+302+190`;
- after first Up: 466 pixels in `44x202+319+195`;
- after Right: 89 pixels in `20x64+341+230`;
- after second Up: 532 pixels in `41x195+304+189`.

Visual review confirms that every surviving box lies on the input-controlled
central on-screen figure and follows it along the trajectory. No stable
intersection pixel lies outside those local boxes. At 2%, 1,498, 1,667, 352,
and 2,348 pixels survive in the same moving region. At 10%, only one start
pixel survives and the other anchors are empty; the demonstrated difference
is therefore repeated but moderate in color/intensity.

Exact per-run hashes, global metrics, intersection construction, component
sizes, and bounding boxes are retained in
`dynamic/wine/EXP-20260812-033-comparison.txt`.

### Rejection and corrected classification

One control-A retry stayed at the previously observed 954-line pre-resource
boundary. It did not load the tested path and contributes no substitution
evidence.

An earlier control-A attempt reached line 1474 and was initially stopped as a
suspected post-load stall. Isolated surface inspection on the accepted retry
shows that this is the natural Training title waiting for its start key;
`End ClearLoadScreen`, `End InitMainGame`, and `NextLife` follow that key. The
first attempt is therefore an incomplete operator rejection, not a game fault.
Both ignored hashes are retained in the curated comparison.

## Confirmed

- The exact one-path equal-size replacement is accepted by the unchanged
  executable under hardware Direct3D and completes the fixed trajectory.
- All accepted arms explicitly load the selected `CHARS/FLICK.ANM/.ALL`
  paths, emit byte-identical normalized logs, and reach `NextLife`.
- A repeated local rendered difference survives every replacement-to-control
  frame pairing at all four anchors and follows the input-controlled central
  figure.
- The exact staged path is causally linked to that bounded rendered region in
  this experiment.

## Inferred

The changed bytes likely alter some resource data used to draw the central
figure. That is intentionally weaker than assigning `.ALL` structure, model,
texture, animation, or filename identity.

## Unknown and limitations

- `.ALL` layout, fields, and first character-specific consumer remain unknown.
- The filenames and visible figure do not by themselves prove resource or
  character identity.
- Input is timestamped but not synchronized to an internal engine frame; the
  later controls demonstrate camera/trajectory phase divergence.
- General cross-file compatibility, later behavior, an M1 payload dependency,
  and the complete level-to-runtime-object chain remain unknown.

## Result and follow-up

M2.20 is complete with a positive bounded loaded-file-to-render link. Keep M2
active: the result supplies a safe visible anchor but does not yet connect that
path through its PC request origin, first consumer/runtime object, and a level
record or payload.

The next packet should trace the exact `CHARS/FLICK.ALL` request backward to
its PC caller/origin and forward only to its first bounded consumer/runtime
destination, using the visible region from this experiment as the acceptance
anchor. Do not infer `.ALL` semantics or reuse plant-specific identities.
