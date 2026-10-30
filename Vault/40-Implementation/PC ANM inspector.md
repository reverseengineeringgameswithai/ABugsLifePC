---
type: implementation
status: active
created: 2026-08-12
updated: 2026-10-01
evidence:
  - EXP-20260812-015
  - EXP-20260812-017
  - EXP-20260812-018
  - EXP-20260812-019
  - EXP-20261001-002
tags:
  - implementation/parser
  - implementation/resources
---

# PC ANM inspector

## Supported boundary

The implementation mirrors only the first-level reads demonstrated at PC
address `0x00444B70` and documented in [[PC ANM first-level]]. It retains the
complete input bytes, reports offset-named metadata, and performs no edits.

Supported checks:

- 8-byte header presence;
- nonnegative signed offset count and complete dword offset table;
- every nonzero offset inside the exact file;
- complete 12-byte header at the first nonzero reference;
- complete signed-word list selected by its unsigned count;
- indices whose signed value is `-2`, the only value distinguished by the
  evidenced consumer.

## Commands

Inspect one user-owned work-copy file:

```bash
./scripts/ablpc-mod inspect-anm \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/PLANTS/PLANT04.ANM --json
```

Validate a user-owned directory without emitting payload bytes:

```bash
./scripts/ablpc-mod scan-anm \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/PLANTS --json
```

## Safety properties

- `AnmFile.data` is the exact immutable input byte string.
- Every read is checked against exact file size.
- Output contains paths, hashes, sizes, counts, offsets, and `-2` indices only.
- No serializer, relocation writer, resource editor, or generic byte-patch
  operation is exposed.
- Tests use synthetic fixtures; no game bytes are tracked.

## Unsupported

- geometry, material or object field names, and meanings for the linear,
  angle and extra words (slot records themselves are parsed by
  `AnmFile.records()` since EXP-20261001-002; the CLI still reports only the
  first-level layout);
- `.ALL` parsing;
- malformed-file compatibility with the original unchecked routine;
- any resource replacement or edit in the public CLI. `EXP-20260812-018`
  performs an external whole-file copy between exact user-owned staged files;
  `EXP-20260812-019` repeats that boundary for an exact two-file pair. Neither
  adds a serializer or manifest operation.

## Validation

`EXP-20260812-017` records 16 synthetic ANM tests, 38 complete repository
tests, and zero failures across all 11 exact PC plant `.ANM` files.

`EXP-20260812-018` separately confirms that one exact whole-file substitution
is accepted through Direct3D Training gameplay with the destination `.ALL`
unchanged. Because no stable start-camera change is visible, the operation is
not promoted as a useful public mod class.

`EXP-20260812-019` separately confirms the equal-size whole pair is accepted
with the same no-stable-start-camera classification. This does not widen the
read-only tooling surface.
