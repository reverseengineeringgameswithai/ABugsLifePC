---
type: experiment
id: EXP-20260813-052
date: 2026-08-13
question: Can M2 close by revising its dependency-path gate without weakening the milestone outcome, and if not, what one finite PC-native candidate remains?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline evidence reconciliation and native instruction verification
environment_version: GNU objdump 2.44; Git 2.54.0; existing PC static and runtime evidence only
working_directory: /home/dev/ABLPC
configuration: M2 gate disposition plus one finite signed-selector candidate; no runtime, mutation, parser/schema, semantic promotion, new xref family, other resource family, or cross-port evidence
artifacts:
  - Vault/00-System/Project Roadmap.md
  - Vault/50-Decisions/Decision Log.md
  - Vault/70-Known-Unknowns/Known Unknowns.md
addresses:
  - 0x0044CA1F
  - 0x0044CA24
  - 0x0044CE0D
  - 0x0044CE11
  - 0x0044D1F7
  - 0x0044D1FB
  - 0x0044D205
  - 0x0044D7A4
  - 0x0059D9C0
  - 0x0059DD50
  - 0x0059DD58
  - 0x005B18E0
  - 0x005B1A7C
file_offsets: []
result: gate-retained-one-signed-selector-candidate-selected
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/milestone-audit
  - re/static
---

# EXP-20260813-052 - M2 dependency-gate disposition

## Question

Can M2 close by revising its dependency-path gate without weakening the
milestone outcome, and if not, what one finite PC-native candidate remains?

## Scope and procedure

This packet reviewed only existing evidence for executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:

- `EXP-20260813-049`'s four-gate reconciliation;
- `EXP-20260813-050`'s complete negative for exact M1 positive-target
  selector-2 inputs;
- `EXP-20260813-051`'s complete current-invocation census of the eight generic
  header readers;
- M1's positive level-record/target-to-rendered result in
  `EXP-20260812-009/010`; and
- the exact ID-zero `CHARS/FLICK.ALL` request, load, retained range, Direct3D
  consumer, and rendered result in `EXP-20260812-033/034` and
  `EXP-20260813-039/040`.

The literal M2 outcome, roadmap summary, and first exit gate were compared
with `DEC-20260813-044` through `DEC-20260813-046`. The exact existing native
instructions in `0x0044CA00` were then rechecked only far enough to bound one
candidate left by the disposition:

```text
sha256sum work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -Mintel -d --start-address=0x44ca00 --stop-address=0x44d210 work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -Mintel -d --start-address=0x44d760 --stop-address=0x44d7c0 work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
```

The inspected copy at
`/home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe` matched the
canonical executable SHA-256. No game was launched or instrumented. No
executable, asset, parser, schema, source, or target was modified. No new xref
family, other resource family, semantic name, or PS1 evidence was introduced.

## Gate disposition

M2 cannot close by combining the two existing renderer-facing chains:

- the M1 chain proves a level placement/positive target reaches
  `0x0045A7F0` and changes a bounded rendered region; and
- the ID-zero chain proves `CHARS/FLICK.ALL` reaches loader call
  `0x00448079`, first consumer `0x00448010`, retained header
  `0x005B18E0`, selected Direct3D consumers, and a bounded rendered result.

`EXP-20260813-035/036/050/051` prove no selection edge at their declared
direct, renderer-input, or generic-reader boundaries. Rewording the gate so
that two parallel chains count as one dependency would remove the causal
requirement that the level placement select or cause the external resource
path. That would weaken both the detailed M2 outcome and the roadmap summary
"Trace one level placement through loaded resources to rendered content."

The same evidence also cannot support a lifetime-independence claim. Persistent
or copied state remains outside the completed negative windows, so M2 remains
active rather than closing negatively.

## One finite PC-native candidate

Exact native instructions bound one signed-selector candidate inside existing
function `0x0044CA00`:

- `0x0044D7A4` calls the function from M1 coordinator `0x0044D430` after the
  record-processing portion of the coordinator.
- `0x0044CA1F` initializes `EDI = 0x0059D9C8`.
- `0x0044CA24` and `0x0044CE0D` sign-extend selector word `[EDI-0x08]`.
- `0x0044CE11` reads header pointer
  `*(0x005B1A7C + sign_extend16(selector) * 4)`.
- The exact ID-zero header is selected only when the signed selector is
  `-103` (encoded word `0xFF99`), because
  `0x005B1A7C + (-103 * 4) == 0x005B18E0`.
- `0x0044D1F7` advances `EDI` by `0x30`; the comparison at
  `0x0044D1FB-0x0044D205` bounds at most 20 source records. The candidate
  selector words are therefore exactly
  `0x0059D9C0 + i * 0x30` for `0 <= i < 20`, ending at `0x0059DD50`.

This arithmetic proves only an addressable candidate. It does not prove that
any selector contains `-103`, that an M1 record or positive target produces
one of the 20 words, that the path executes for ID zero, or that the selected
header contributes to the M2.20 visible result.

## Confirmed

- The existing M1 and ID-zero resource chains are separately reviewable and
  renderer-facing, but no cited PC evidence makes the former select the latter.
- Revising the first gate to accept those parallel chains would remove a
  causal dependency required by the current milestone outcome.
- The signed-selector surface in `0x0044CA00` is finite: at most 20 words,
  one exact header-address formula, and one exact value (`-103`) that would
  address ID-zero header `0x005B18E0`.

## Inferred

The signed-selector surface is the best remaining PC-native candidate because
it is inside the M1 coordinator, runs after its record-processing portion,
and can address the already selected ID-zero header by exact arithmetic. That
ranking is not evidence that the M1 record path populates the source records.

## Unknown and limitations

- The producer and file/runtime provenance of the 20 selector words remain
  unknown.
- It is unknown whether any word can equal signed `-103` at the consumer.
- The relationship between the `0x0059D9C0` source-record array and M1's
  20-byte records or positive targets is not established.
- Persistent/copied wider-lifetime paths and indirect calls remain outside
  the completed negative evidence, but they are not selected for the next
  packet.

## Result and follow-up

M2.37 is complete with option (b): the dependency gate is retained, and M2
stays active. Exactly one next candidate is selected.

M2.38 must remain offline and inspect only the 20 selector words
`0x0059D9C0 + i * 0x30` and their exact native producers. Its first
discriminator is whether the established M1 record/positive-target route can
produce one of those words and whether that word can be signed `-103` at
`0x0044CE0D`. A positive exact lineage supplies the missing ID-zero selection
edge; a complete negative retires this candidate. Do not widen to another
index family, launch or instrument the game, mutate state, assign semantics,
or consult PS1 in that packet.
