---
type: experiment
id: EXP-20260812-012
date: 2026-08-12
question: Does reducing Training record 125 signed field +0x0C from 1259 to zero remove only its partially visible right-edge content as predicted by the PC candidate tests?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, Gamescope
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44; ImageMagick 7
working_directory: /home/dev/ABLPC
configuration: Exact-hash Training control and guarded record-125 +0x0C-zero candidate; Direct3D hardware 640x480x16 only
artifacts:
  - static/exports/BIN-97c95ba5572dce63/FUN_0044d430-record-field-reads.txt
  - dynamic/wine/EXP-20260812-012-comparison.txt
  - dynamic/wine/RUN-WINE-20260812-105947
  - dynamic/wine/RUN-WINE-20260812-111403
addresses:
  - 0x0044D5C4
  - 0x0044D63A
file_offsets:
  - 0x0E80
result: positive-field-0c-is-visibility-bound-for-tested-record
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/rendering
  - re/file-format
  - implementation/modding
---

# EXP-20260812-012 - Training record visibility bound

## Question

Does reducing Training record 125 signed field `+0x0C` from `1259` to zero
remove only its partially visible right-edge content as predicted by the PC
candidate tests?

## Inputs and procedure

- Exact PC executable and Training DAT hashes match `EXP-20260812-011`.
- Record 125 begins at `0x0E74`; field `+0x0C` is at `0x0E80`.
- `mods/training-primary-record-125-field-0c-zero.json` requires the original
  signed value `1259` and writes `0` through an offset-named guarded operation.
- The staged candidate was compared with the unchanged hardware control from
  `RUN-WINE-20260812-105947` using a freshly timed 15-frame candidate sequence.

No PS1 source was consulted.

## Static evidence

- `0x0044D5C4` sign-extends `+0x0C`, divides it by 16, squares it, and
  subtracts that value from the record-center distance before the coarse
  candidate comparison.
- `0x0044D63A` sign-extends it again and uses it as the near and horizontal/
  vertical margin after the center transform.

This confirms a visibility-bound use for positive values. It does not explain
negative values.

## Runtime result

- Output DAT SHA-256:
  `47b7f45e39137f7decdd4ca94db2ef663ee868e6d506bc88511569ded74d7c00`.
- Only bytes `0x0E80–0x0E81` differ from the exact input.
- The candidate passes the Direct3D hardware log gate, loads Training,
  completes `InitMainGame`, and enters `NextLife`.
- Phase-matched frame 02 differs in 756 pixels only within
  `25x109+615+158`, overlapping record 125's prior move-away region
  `24x99+616+124` from `EXP-20260812-008`.
- Frames in which the animated element is naturally outside the image are
  byte-identical. No content is repositioned.

Evidence: `RUN-WINE-20260812-111403` and
`dynamic/wine/EXP-20260812-012-comparison.txt`.

## Confirmed

- Positive record field `+0x0C` contributes the visibility margin for the
  tested record and camera.
- Reducing it to zero can exclude only the partially visible render content
  associated with that record while the remainder of the frame stays exact.
- The new manifest operation is expected-value guarded and edits only the
  selected signed word.

## Inferred

- A conservative current name is `visibility bound candidate`, not angle.
  Whether the numeric unit is a radius, extent, or another bound convention
  remains unconfirmed.

## Unknown and limitations

- The local corpus contains 508 records whose signed `+0x0C` is negative.
  Their meaning and the sign convention remain unknown.
- The result covers one positive value, one record, the Training start camera,
  and dispatch `0x49` only.

## Contradictions and negative results

- The prior `angle candidate` label is contradicted by exact PC use and this
  visibility-only result. It is retired from current dossiers but preserved in
  historical experiment wording where chronology matters.
- One sequence remained on the title because input was not accepted, and a
  second began too late for phase matching. Neither supports the conclusion;
  the retained rerun is `RUN-WINE-20260812-111403`.

## Result and follow-up

Completed. Together with existing `+0x0E` flag/sentinel and relocated `+0x10`
payload evidence, this closes M1.3. Begin M1.4 with a log-identified
non-Training PC scene and one guarded same-dispatch target rebind.
