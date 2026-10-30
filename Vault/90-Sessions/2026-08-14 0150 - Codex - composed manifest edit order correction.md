---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/manifest
---

# Composed manifest edit order correction

## Goal

Execute exact corrective packet M4.7 after independent M4.6 rejection, preserve
each input file entry's authored edit sequence under deterministic exactly-two-
input composition, retain all accepted baselines, and leave one clean worker
commit for fresh-context M4.8.

## Startup and boundary

After James's verdict, the complete required [[START HERE]] sequence was read
again: full [[Current State]], full [[Project Roadmap]], full
[[Environment Status]], full [[Decision Log]], full [[Known Unknowns]],
[[Implementation MOC]], and [[Experiments MOC]]. The complete
[[Agent Operating Manual]], [[Project Charter]], exact M4.7 packet,
`EXP-20260814-064/065`, [[M4 Exact Whole-file Replacement]],
[[M1 Tool Support Matrix]], and James's audit session were also read.

Work remained offline and PC-native at the existing manifest boundary. No
original, external PS1 repository, runtime state, executable, or user-owned
game byte was modified or added to Git.

## Work performed

- Changed `_composed_file_entry_from_ranked_claims` to sort by canonical input
  rank and original edit index instead of source byte span.
- Kept normalized destination-file sorting, cross-input exact-span conflict
  detection, deterministic earliest conflict, and combined existing-schema
  revalidation unchanged.
- Added the exact bounds-valid `0x98`/`0xA4`/`0x21C` regression with both
  inputs independently applied, both composition orders, saved apply/stage,
  ordinary receipt equality, independent expected bytes, and source
  preservation.
- Added regressions for descending offsets, same-span sequential guards,
  empty/unequal opaque behavior, and deterministic multiple-conflict
  selection.
- Corrected user and Vault documentation that promised byte-location-sorted
  edits; recorded `EXP-20260814-066`, `DEC-20260814-061`, `KU-047`, roadmap,
  state, MOCs, and this session.

## Evidence and validation

- Focused manifest/LEVEL suite: 63 passed.
- Complete canonical suite: 251 passed in 6.72 seconds before Vault closure.
- Final `make check`: 251 passed in 6.23 seconds; Vault lint 225 notes with
  zero errors/warnings; tracked-file audit zero violations; diff checks pass.
- Exact local same-DAT composed JSON/output hashes remain
  `b16a7cac...79faa` / `78cca99b...1d9a`.
- Exact local M1-plus-opaque composed JSON, DAT output, and opaque output
  hashes remain `de15f8e...b485` / `47b7f45e...7c00` /
  `6e5afb4f...079a4`.
- Source LEVEL DAT, opaque destination, and replacement-source hashes remain
  `494d2818...5a22`, `a2f23220...4ac6`, and `6e5afb4f...079a4`.
- Exact opaque recipe passes twice with byte-identical receipts/output and
  two-file sparse locality.
- No unscoped pytest command or external PS1 inspection was used.

Final `make check`, Vault lint, tracked-file audit, text-only diff audit, and
clean-tree checks are recorded in
[[EXP-20260814-066 - Preserve composed manifest edit sequences]].

## Conclusion

M4.7 is worker-complete, not independently accepted. The exact M4.6 defect is
closed without removing revalidation or widening to semantic ordering. M4
remains active on fresh-context hard-truth verifier packet M4.8.

## Exact next action

Give the immutable clean worker commit to a fresh James context. James must
attempt to falsify the order-preservation correction and all retained
conflict/topology/schema/receipt/local/asset-free gates, then return one exact
verdict and next/corrective packet under the serial ratchet.

## Git commit if applicable

`fix: preserve composed manifest edit order`
