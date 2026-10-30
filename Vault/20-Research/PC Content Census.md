---
type: research
status: active
created: 2026-08-12
updated: 2026-10-02
tags:
  - re/resources
  - re/file-access
---

# PC Content Census

[[EXP-20260812-014 - PC content census and loader context]] is the canonical
metadata census for the current derived PC game tree.

## Reproduce

```bash
./scripts/census-pc-content.py \
  work/copies/BUGS_PC-full-disc/PC/BUGS \
  --log training=dynamic/wine/RUN-WINE-20260812-000634/bugs.log \
  --log level01=dynamic/wine/RUN-WINE-20260812-114514/bugs.log \
  --json-output reports/content/pc-content-census.json \
  --summary-output reports/content/pc-content-census.md
```

The command refuses `originals` and `media`, symlinks, and case-insensitive
path collisions. It excludes only the runtime-generated root `bugs.log` by
default. The report contains path/size/hash and derived grouping metadata, not
game-file payload bytes.

## Confirmed snapshot

- Fingerprint: `b145e2aa5fbf7e3350cf437985bbc76c764c36f2d954105d5282af4831738986`.
- Files/bytes: 721 / 460,306,509.
- Training explicit loads: 25/25 matched.
- Level 01 explicit loads: 45/45 matched.
- Unique observed union: 51 files; common intersection: 19.
- Duplicate byte groups: five groups / 26 files, including 18 empty
  placeholders and four non-empty pairs.

## Candidate subfamilies and current selection

The first bounded trace used the 11 basename-matched pairs under `CD/PLANTS`.
Nine pairs occur in the retained loader logs; four occur in both scenes.
`EXP-20260812-032` completes that route with a fixed-trajectory negative for
the exact plant-04-to-10 pair and retires it as the direct visible-outcome
candidate. This does not prove that the plant files are unused.

M2.20 selected a different census-local family. The accepted Training log
explicitly loads `CD/CHARS/FLICK.ANM/.ALL`. PC files
`CD/CHARS/FLICK.ANM` and `CD/CHARS3/FLICKD.ANM` are byte-identical, while the
corresponding `.ALL` files are equal-size (`0x34EC`) but differ at 2,115 byte
positions. `EXP-20260812-033` accepts that exact one-path `.ALL` replacement
and finds a repeated local difference on the input-controlled central figure
along all four bounded anchors. This confirms the exact loaded-file-to-render
link, not file semantics, filename identity, general replacement
compatibility, or an M1 placement dependency. `EXP-20260812-034` now binds
that exact selected path to the ID-zero request and retained shared-entry
range `[0x005A9660, 0x005A9DE0)`; this narrows the dependency without changing
the census or establishing identity/layout semantics.

## Evidence boundary

- Explicit load-line producer: `0x004AE240`, string `0x004E93AC`.
- Training runtime: `RUN-WINE-20260812-000634`.
- Level 01 runtime: `RUN-WINE-20260812-114514`.
- Full metadata: `reports/content/pc-content-census.json`.
- Compact generated summary: `reports/content/pc-content-census.md`.

## Static follow-up

[[EXP-20260812-015 - Plant pair caller and consumer trace]] confirms that the
selected basename pairs share a PC coordinator but diverge immediately after
loading: `.ANM` reaches `0x00444B70`, while `.ALL` is interpreted within
`0x00448010`. This resolves the caller/consumer question without changing the
census evidence boundary; an M1-to-file dependency remains unproven.

[[EXP-20260812-032 - Fixed trajectory paired plant replacement]] closes the
plant-04/10 direct visible route.
[[EXP-20260812-033 - Character ALL replacement visible outcome]] supplies the
positive character-family render anchor.
[[EXP-20260812-034 - Character request and first consumer trace]] supplies its
exact request/load/retained-range boundary. The next contract is
[[Project Roadmap#M2.22 — Character retained-range first-use bridge]].
*Update (2026-10-02 audit):* M2.22 completed in
[[EXP-20260813-035 - Character retained-range first-use bridge]], and
[[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]] later
left M2 deferred. No census follow-up is queued.
