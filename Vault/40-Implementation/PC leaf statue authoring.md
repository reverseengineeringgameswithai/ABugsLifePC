---
type: implementation
status: implemented-bounded
created: 2026-09-16
updated: 2026-10-29
evidence: [EXP-20260915-008, EXP-20260916-013, EXP-20260916-017]
tags: [terrain/scenery, re/pc]
---
# PC leaf statue authoring

The leaf structure in front of Flik is one original PC scene object: green leaf, two curling stems and yellow base. Its 317 vertices form 16 disconnected mesh components (70,57,57,49 and twelve7-vertex pieces), but they share one object/geometry stream. Nearby yellow upright leaves are separate scenes. EXP-20260915-008 owns source identification and bounded validation; no PS1 comparison was used.


## PC evidence and mechanism

Retail EXE SHA256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; original DAT `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`; original terrain `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`.

The original pose carries an intrinsic 8.6926° base tilt (plane fit in
`leaf_statue.py`; EXP-20260916-017). Source anchor (4392,−3862,−3563) is the
bottom central foot, rather than the lower curling side stem.

- **Confirmed object identity:** primary scene109, DAT7560, flags0x41;24-byte object20632;7014-byte geometry264144, SHA `e6cbc9a1f06f6e28bb93a4524c0bdb38385549a18f4fbdba1482a7f10106331a`. There are202 faces. The import-time original-game resident scene0064C63F/object0064F94F/geometry0068B087 match file bytes after relocation; screenshot and isolated textured render identify the structure (`resident.json`, `mesh-109.png`, `pair.json`). Original internal level1; supplied Flik world(47251,−115413,−52847).
- **Confirmed native representation:** `004498F0` cases0x41/0x49 both feed mesh renderer0045A7F0. `leaf_statue.visual` preserves the mesh and native control bytes, adds explicit4096 scales plus two zero padding bytes, and selects0x49. Nine original-x86 camera contexts produce identical matrix/translation inputs and mesh-renderer arguments (`normalize-probe.json`, `4498f0.json`). No decompiler source was copied into the implementation. Existing `PropVisual`, `append_visual` and `append_prop` paths are reused; distant geometry shares the same mesh.
- **Shell pairing:** original terrain source89, descriptor229340, payload7652..15020, tag6,226 triangles, SHA `98255d5975eb53c05720e40cf363ebc39b913438ebff9b685e6cf266422e2c37`. Independently rendered shell has the same leaf/base/curl outline; its expanded envelope surrounds the visual and native movement collides with it. Pairing is geometric/runtime evidence, not a discovered explicit DAT-to-terrain link. At heading0 with `level_base:false`, `append_shell` preserves the entire payload and descriptor except XYZ translation. EXP013 adds upright yaw of the original shell corners/normals, with rebuilt X/Z admission fields and unchanged grouping/opaque tail. No collision geometry is rebuilt from the render mesh.
- **Final preservation:** final primary549/object879500/geometry879532 and one shared secondary proxy retain the exact original mesh; all1588 pointer fields relocate correctly under original0044BB70. New collision source227 carries the exact original7368-byte shell. Removing that source reconstructs the entire EXP007 terrain file byte for byte.727 of729 CD files and all prior exported scene fields remain exact. The sole EXE change is an existing build patch's collision descriptor index240→241 at file0xBB610/VA004BC010; native loader maps descriptor241 to retained hazard source254 (`production.json`, `hazard-binding.json`). This is expected descriptor rebasing after a new collision source, not unrelated executable drift.

## Collision verification

Sixteen final-terrain movement/deletion comparisons using original004AB1A0 pass, including lateral blocking and top support. The native fixture terrain is byte-identical to final production.

The first plane criterion omitted the coordinator's0xC80 world/100 stored Y coordinate shift and marked six valid contacts as failures. Raw measurements remain in `collision-unadjusted-plane.json`. The corrected comparison subtracts100×normalY/16384 before comparing actor position to the shell plane, with32 units for native contact/sliding behavior; original004AB1A0 entry/exit confirms that shift (`4ab1a0.json`). This does not change terrain bytes. Claim sweeps record the anchor, collision-measurement and EXE expectation corrections.
