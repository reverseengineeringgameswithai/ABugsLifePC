---
type: experiment
id: EXP-20260907-010
date: 2026-09-07
updated: 2026-10-29
status: accepted-bounded
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Derived PC executable in isolated Wine hardware session; original instructions under Unicorn; Blender 5.2.0 LTS
question: Can terrain and scenery draw farther by scaling the two original render-distance groups through guarded executable immediates, within native batch and index capacities?
result: Yes at 1.5x (1152/1664 to 1728/2496); native initializer cases and eight primary-frame arms pass with maximum batch 498 of capacity 500 and index capacities 1000/4800; far also affects secondary/background admission in 0x0044D430; resident lookup words match live
tags: [re/experiment, re/rendering]
---

# EXP-20260907-010 - General render distance preview

Terrain disappears at distance as well as scenery, so a general change was
tested instead of a mushroom-only one. Following
[[EXP-20260907-009 - Mushroom render distance diagnosis]], both original
groups scale from 1152/1664 to 1728/2496 through three guarded executable
immediates. [[PC general render distance]] documents exact addresses, tuning,
restoration and bounds. The 1.5× setting passes the native initializer and
primary-frame checks below and looked correct in a live run.

## Build and tests

48 focused tests pass in 9.92s, covering settings rejection before staging,
initializer identity/truncation/double-application, exact inverse and unchanged
data files. Six native initializer cases execute real PC code under both renderer
selections at original/1.5×/2×. Write bounds, table canaries and all 4095 words
match. Installed transition end index is 2240; table runs are 1728 zeros,
256 × 0x600, 256 × 0x400 and 1855 × 0x200.

The derived executable `80999c8e...0752e` differs from its base
`e4ff4340...ab2c` only at the three immediate fields; the data files are
unchanged. Full hashes and sites are in
`reports/render-distance/EXP-20260907-010.json`.

Eight native primary frame arms (four EXP-009 cameras, stock and 1.5× each)
execute all 29 active terrain/mushroom objects, original admission, projection,
emission, automatic packet flush and counter reset. Terrain output changes
1997/1991/1938/1895 → 3122/3073/3038/2996 vertices across the four cameras;
combined totals change 2433/2475/2554/2511 → 4286/4273/4214/4068.
Maximum batches are 499 stock and 498 installed, within capacity 500. Index
capacities 1000/4800, finite XYZW, triangle multiples and every referenced index
are checked. Accepted arm takes 14.69s. Six Direct3D COM sites return HRESULT 0
in the private fixture, with texture upload assumed complete. This does not
execute a GPU, dynamic actors or secondary/background passes, or benchmark FPS.

## Resident check

In a file-loaded run of the derived executable, hardware log markers, the full
resident initializer, near/far globals and all 4095 lookup words matched the
stage. Two captures show terrain and blue mushrooms; player movement prevented a
matched-pose pixel A/B. No RAM writes, debugger, pause or teleport were used.
No originals or external PS1 material touched.

## Retained corrections and limits

A first direct-global fixture passed; strengthening it to execute the initializer
in a reused CPU failed on the second arm. The failed log is retained. Stale
translated-code reuse is a possible explanation, not confirmed. Using a fresh
CPU per executable arm yields the accepted eight-frame result; independent
initializer unit cases already used fresh CPUs. This was fixture work, not a
production renderer fix.

Initial generated receipts claimed unchanged background behavior. That wording
was too broad: far also affects the original secondary/background admission
inside `0x0044D430`. Receipt source now says original geometry, object bias and
render code retained. Original generated receipts remain intact, with
`receipt-scope-correction.json` recording the correction; executable unchanged.

The bounded native checks and one live appearance check do not prove every
camera, occlusion case or performance level. 2× has only initializer/selected
mushroom offline evidence. Private evidence root
`work/experiments/EXP-20260907-010`; `reports/render-distance/EXP-20260907-010.json`
contains receipt hashes, native counts and build identities.
