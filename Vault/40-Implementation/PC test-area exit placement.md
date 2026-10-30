---
type: implementation
status: implemented
created: 2026-09-07
updated: 2026-10-29
evidence: [EXP-20260907-005]
tags: [implementation/modding, terrain/authoring, gameplay/progression]
---

# PC test-area exit placement

EXP-20260907-005 finishes Level01 when grounded Flik enters a configured
region of a test-area build, by wrapping Flik's native post-movement contact
query. A live walk into the region finished the stage, and the guarded game log
independently records native `Level done variable is 1` and complete
`LEVELDONE` cycles. The region test requires exact grounded contact flags
`0x0101` on its floor descriptor, so jumping over the spot does not finish until
supported contact is established. Stored terrain units are world units divided
by32, and Y grows downward.

## PC mechanism

Retail executable SHA256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:

- Source descriptor177 in original Level01 `TERRAIN.ALL` has result2 at record
  `0x399FC+0x28`, with two sloped collision triangles at payload `0x357D0`.
  Loader0x004A8410 copies source+0x28 to runtime descriptor+0x2E.
- Native0x004ACF90 returns the selected contact's result when its state byte is1.
  Flik's post-movement query is the call at0x004408AC. Result2 reaches0x004408FC,
  setting done word0x0059A5B0 to1 and countdown0x0059D9B8 to23, then normal audio,
  fade and completion flow. This branch has no grain check.

The EXP-005 wrapper uses guarded original call bytes at file0x3FCAC and
256 bytes of original `CC` linker padding at VA0x004BBA00/file0xBAE00. It verifies
no relocation overlaps the padding. The helper uses relative calls and computed
image base; native-reader/dispatch tests pass at bases0x400000 and0x1000000.
No new section, relocation, asset, floor geometry or live-memory patch is needed.
The code-padding slot is also used by the separate Training FLIKFLIK experiment;
patches that use it are not silently composable.

## Evidence and limits

36 exit regressions pass. Original PC loader/movement
on the test-area terrain gives identical position/contact traces for control and
candidate in three paired cases: landing at the configured point, walking down
the ramp into the region, and an airborne control. Full resident helper/call,
terrain, perimeter and plant data match files. The native probe is
`research/level-exit/probe-native.py`.

An initial full-retail vertical-drop probe hits nearby source164, not the exit.
The retained discriminator isolates only the original exit stream and obtains
native result2. This establishes that stream's behavior; it is not a natural OG
route demonstration or proof of contact with both original triangles. Exact live
boundary coordinates, all movement speeds and other levels remain outside this
acceptance.
