---
type: research
status: confirmed-bounded
created: 2026-09-06
updated: 2026-10-02
tags: [re/collision, re/gameplay, terrain/authoring]
---

> Current actor-distance repair: [[EXP-20260907-014 - Cliff seam and phantom seed collision repair]] reproduces phantom seed pushes at
> 0041CD5B/60 from extreme-position type11 actors. A guarded64-bit broad phase
> prevents those contacts while the native nearby VX-512, stomp countdown10
> and type5 constructor controls pass. How the retained seeds reached their
> extreme coordinates remains untraced. This does not alter PLANTTER support.


# PC seed and mushroom collision state

## Confirmed boundary

[[EXP-20260906-007 - Plant-state collision regression]] resolves the isolated Level01 seed/opened-mushroom regression for the observed **type 5 plant / PLANTTER record 8**. The Windows PC executable is authoritative: SHA-256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`. No PS1 evidence is used. Function labels below describe demonstrated bounded paths; no unidentified functions or fields were renamed.

| Stage | PC evidence | Consequence |
| --- | --- | --- |
| Unopened seed | General actor array `0x0059B628`, stride `0x84`, type11; contact `0x0041C9B0`, shape pointer `+0x74` | Seed collision is separate from PLANTTER triangles. Native present/absent controls yield lateral velocity -512/0. |
| Stomp and countdown | `0x0041C9B0` writes countdown10 at seed `+0x6c`; slice `0x0041ED9A` reaches call `0x0041EDF8` on tenth tick, thunk `0x00401488` -> `0x00467E60` | Working seed contact can initiate a plant whose triangle template is nevertheless empty. Slice excludes final seed-list removal. |
| Type selection | `0x00467E60` reads placement `+0x0e/+0x0f`, selectors `0x0059D9A8`, table `0x004DE9F0`; selection `0x00467ECC`, type store `0x00467EE9` | Observed selectors `(0,0)` and global bytes `(17,0,0,0,0,0)` produce plant type5, not type7. |
| Opening animation | Plant array `0x0059D9C0`, stride48; `0x00468BF0` decrements actor `+0x26` from15 and sets flag bit2 at zero | Native original code establishes the tested open state. |
| Dynamic registration | Loader `0x004A858D` uses source `+0x1a`; registration `0x0044CA00` with slice `0x0044CA19..0x0044CB5D` and epilogue `0x0044D1F3..0x0044D20B` | Type5 -> template descriptor186 -> PLANTTER source8. Slot2 -> descriptor `N+2=193` with `N=191`, tag `type+0x67=108`, actor origin. Both failing and repaired runtime agree. |
| Landing/contact | Original coordinator `0x004AB1A0`; contact selector `0x004ACEB0` checks flags `0x0059D992 > 255` and descriptor tag `>0x67`, returns descriptor-N+1 | Active mushroom triangles supply the matching plant contact; an empty template cannot. |
| Bounce | Type5 case in `0x00468010` checks matching contact and plant flag bits2/4; store `0x00468406` writes `-0xD00` at `0x0059D940` and contact flags clear | Ordinary upward velocity is -3328. Effect dispatch call `0x004684CA` targets `0x004148A0`; audiovisual execution excluded from the native probe. |

## Causal evidence

The original PLANTTER record8 allocation starts at file offset9808 (`0x2650`), size964, kind8, source `+0x1a=38`, non-clone. Isolation replaced its first group marker `01 00` with `ff ff`, leaving all later payload bytes intact. The correct descriptor/origin still registers, but its parsed groups/cells are empty and bounds collapse to32x32. A bounds-checked two-byte restoration reactivates the original16 groups/24 triangles without changing terrain, other plant templates, high0x104, directory or unknown bytes.

Independent evidence forms:

- Static original-PC addresses above plus original/stripped file census, full allocation comparisons and exact hashes in the experiment/report.
- `work/experiments/EXP-20260906-007/native-03.json`: same modeled inputs, stripped/restored only; four lateral approaches change from penetration to exclusion; landing changes0->6 bounce-store events; continuous floor departure and jump-return changes0->1 bounce. Original `0x00467D70` reset is executed to initialize bounce history; omitting it was a rejected harness setup.
- Read-only live census `control-01/receipt-1788739476760182883.json` establishes type5/source8 even in the failing control. Fresh repaired file loading plus normal-input `repaired-variety-01/receipt-1788739935331279279.json` records descriptor193 contacts and five -3328 bounce onsets. User also confirms mushroom contact/jumping. Complete paths/hashes and asynchronous-capture limits are in the experiment.

The seed's surviving collision is therefore not contradictory to losing the mushroom template: the two states use different collision data. The bounce code was not separately disabled; its contact prerequisite was missing.

## Remaining unknowns and implementation scope

`terrain_plant_templates.py` restores only explicitly selected marker-only allocations after complete identity checks. It is not a generic semantic classifier or an all-plant isolation policy. Other emptied templates and high0x104 remain untouched. Type7 -> source10 remains a separate loader mapping, not the observed mushroom's identity.

Native tests supply synthetic cadence, gravity, visible flag and jump impulse, omit rendering/input interpretation/effect dispatch, and do not establish every upgrade, mushroom colour or level. Runtime samples are asynchronous and finite. Full PLANTTER directory bytes must not be compared against its retained payload arena: `0x004A8800..0x004A880A` advances the loader cursor by payload words*2, and the directory area is reused/not retained. Only the full prefix through16691 was verified resident; the later directory-area writer is not identified.

Next use the repaired varied-grass preview for user feedback. Map any additional broken plant independently before restoring its template.
(2026-10-02 audit: that preview step is historical; [[Current State]] owns current work. The rule to map each broken plant before restoring it still applies.)
