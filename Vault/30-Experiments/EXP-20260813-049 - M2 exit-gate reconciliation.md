---
type: experiment
id: EXP-20260813-049
date: 2026-08-13
question: Do the accumulated PC-native M2 results satisfy all four written exit gates, and if not, what one exact evidence edge remains unsupported?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline evidence and repository audit
environment_version: Git 2.54.0; existing PC static, Wine, GDB, parser, and fixture evidence only
working_directory: /home/dev/ABLPC
configuration: Four-gate M2 reconciliation; no runtime, target/source edit, parser/tool change, semantic promotion, other family, or cross-port evidence
artifacts:
  - Vault/00-System/Project Roadmap.md
  - Vault/40-Implementation/PC ANM inspector.md
  - Vault/40-Implementation/M1 Tool Support Matrix.md
addresses:
  - 0x00448079
  - 0x00448010
  - 0x0044C898
  - 0x0044F8E0
  - 0x00449E20
  - 0x0045A7F0
  - 0x005A9660
  - 0x005B18E0
file_offsets:
  - 0x0A6C
  - 0x111E4
  - 0x1319C
result: three-exit-gates-supported-one-record-to-resource-edge-open
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/milestone-audit
---

# EXP-20260813-049 - M2 exit-gate reconciliation

## Question

Do the accumulated PC-native M2 results satisfy all four written exit gates,
and if not, what one exact evidence edge remains unsupported?

## Scope and procedure

This packet reviewed only existing evidence for executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
It reconciled:

- M1's exact Training scene-record/positive-target path and visible rebinds;
- M2's PC `.ANM` first-level inspector, synthetic fixtures, and exact
  whole-file replacement evidence;
- the exact `CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL` accepted visible result and
  its request, loader, retained-entry, and Direct3D paths;
- the M2.25/M2.26 correction that reclassified the shared `0x80`-stride arena
  as selector-1 native-software output; and
- `KU-023`, the still-unresolved M1 placement/payload-to-resource identity.

No game was launched or instrumented. No executable, work-copy asset, source
file, parser, manifest, or runtime schema was changed. No other record or
resource family was inspected, and no PS1 evidence was consulted.

## Four-gate matrix

| M2 exit gate | Status | Exact evidence and limit |
|---|---|---|
| A reviewable dependency path links a level record/payload, PC file path, loader, runtime consumer, and outcome | **Not satisfied; sole M2 blocker** | `EXP-20260812-009/010` prove the M1 record/payload-to-`0x0045A7F0`-to-visible path. `EXP-20260812-033/034` and `EXP-20260813-039/040` separately prove `CHARS/FLICK.ALL` through loader call `0x00448079`, first consumer `0x00448010`, retained range `[0x005A9660,0x005A9DE0)`, `0x0044F8E0`, selected Direct3D batches, and a bounded rendered result. `EXP-20260813-035/036` find no direct input edge between those sources. Their shared `0x80`-stride arena cannot close the gate because `EXP-20260813-039` proves it is the selector-1 software path, not the accepted Direct3D path. No exact PC edge makes an M1 record or positive target select the ID-zero resource path. |
| The selected format is tested across multiple files plus synthetic invalid inputs | **Satisfied at the selected `.ANM` first-level boundary** | `EXP-20260812-017` validates all 11 exact PC plant `.ANM` files with zero failures and 16 synthetic tests covering truncation, impossible counts, zero/out-of-range offsets, nested bounds, byte preservation, and metadata-only output. This does **not** transfer to `.ALL`: [[File Formats MOC]] and [[PC ANM inspector]] continue to reject any `.ALL` parser/layout claim. |
| One replacement or parameter edit is accepted and distributable without bundled assets | **Satisfied as exact whole-file instructions** | `EXP-20260812-033` gives the exact executable, destination, and replacement-source hashes; requires a separate ignored staged copy; copies only user-owned `CHARS3/FLICKD.ALL` over `CHARS/FLICK.ALL`; verifies the destination hash and one-path locality; and records unchanged-executable Direct3D acceptance plus a repeated rendered difference. The distributable unit is those paths, hashes, checks, and instructions—not either `.ALL` file. A repository audit found no tracked `.ALL` or `.ANM` files, and `work/copies/` is ignored. This is an exact recipe, not a generic `.ALL` compatibility or editing claim. |
| Unknown sections remain preserved and visibly labeled unknown | **Satisfied at the supported format/tool boundary** | `EXP-20260812-017`, [[PC ANM first-level]], and [[PC ANM inspector]] retain the exact immutable `.ANM` byte string, expose no writer, use offset names, and label uncharacterized header/nested sections unknown. `.ALL` remains whole-file-only and unparsed; `EXP-20260813-043` explicitly does not promote its exact byte spans into safe fields or semantics. The software-arena correction remains visible in `EXP-20260813-036/039` rather than being silently normalized. |

## Asset-free replacement-instruction audit

The exact M2.20 recipe is sufficient as distributable instructions because a
recipient can perform every material check against files already present in
their own derived work copy:

1. Require `bugs.exe` SHA-256
   `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
2. Require destination `CD/CHARS/FLICK.ALL` size `0x34EC` and SHA-256
   `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`.
3. Require replacement source `CD/CHARS3/FLICKD.ALL` size `0x34EC` and
   SHA-256
   `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
4. Create a separate staged tree under ignored `work/copies/`, copy only the
   verified replacement source over the verified destination, require the
   destination to acquire the replacement hash, and require a recursive
   comparison to report only that path.
5. Launch through the existing hash-checked work-copy launcher and accept only
   the four positive Direct3D markers, no `INITSOFTRENDER`, the exact selected
   load, `End InitMainGame`, and `NextLife`.

These instructions contain no source bytes and require no distributable patch
payload. They reproduce only the demonstrated exact-pair experiment. They do
not authorize a public `.ALL` editor, arbitrary source selection, or a claim
that the filenames identify a semantic asset.

## Confirmed

- The selected PC `.ANM` first-level format satisfies the written multi-file,
  synthetic-invalid-input, and unknown-preservation gates at its documented
  read-only boundary (`EXP-20260812-017`).
- The exact M2.20 `.ALL` whole-file replacement is accepted by the unchanged
  executable, has a bounded rendered result, and can be distributed as
  hash-guarded instructions without either game file (`EXP-20260812-033`).
- The M1 level record/payload path and selected M2 resource path are separately
  reviewable and renderer-facing, but no cited PC evidence makes the former
  select the latter (`EXP-20260812-010`, `EXP-20260812-033` through
  `EXP-20260813-040`).
- The conditional shared arena from M2.23 is selector-1 software output and is
  not valid Direct3D bridge evidence (`EXP-20260813-039`).

## Inferred

The M1 positive-target and ID-zero `.ALL` paths are parallel renderer inputs
under the reviewed Direct3D update. Their convergence on renderer machinery
does not establish a dependency or resource-selection identity.

## Unknown and contradiction preserved

- **Unknown:** which, if any, exact M1 scene record or positive target selects
  the ID-zero `CHARS/FLICK.ALL` resource path or one retained entry.
- **Unknown:** general `.ALL` layout, invalid-input behavior, field semantics,
  and safe partial editing. `.ANM` coverage is not `.ALL` coverage.
- **Contradiction resolved without promotion:** M2.23's historical hardware-
  arena label is superseded by M2.26's exact software ownership proof. Shared
  output topology remains true only on that corrected branch.

## Result and follow-up

M2.34 is complete, but M2 remains active. Three written gates are supported
at their exact boundaries; the sole unsupported gate is the missing PC-native
M1 record/positive-target-to-ID-zero-resource selection edge preserved by
`KU-023`.

The smallest next discriminator is an offline selector-2 slice inside exact
M1 consumer `0x0045A7F0`: trace only the values used to choose and parameterize
its Direct3D builders and test whether any is derived from ID-zero header
`0x005B18E0`, retained range `[0x005A9660,0x005A9DE0)`, or the exact selected
resource state. A positive exact data-flow edge can supply the missing bridge;
a complete negative must retain the gate rather than treating shared batches
or pixels as identity.
