---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/rendering
  - implementation/modding
---

# Hardware target rebind validation

## Agent

Codex

## Goal

Execute roadmap packet M1.2: run the prepared reciprocal Training target
rebinds against an unchanged PC Direct3D control, establish the smallest
visible conclusion supported by phase-matched evidence, and make hardware
renderer selection a durable RE gate.

## Files inspected

- Required system notes, roadmap, operating manual, decisions, unknowns, and
  reverse-engineering/file-format/implementation MOCs
- `EXP-20260812-008`, `EXP-20260812-009`, the positive-target structure and
  function dossiers, and prior hardware capture metadata
- Exact-hash executable and Training DAT work copies
- Both guarded target-rebind manifests and their staged receipts
- Native Gamescope captures and game logs under ignored work storage

No file under `originals/` was modified. No PS1 source was consulted.

## Experiments inspected

- [[EXP-20260812-008 - Training record watchpoints and individual roles]]
- [[EXP-20260812-009 - Training payload target structure and reuse census]]
- New packet: [[EXP-20260812-010 - Training target rebind visible substitution]]

## Changes made

- Staged both hash-locked reciprocal candidates and reconfirmed exact byte
  locality and output hashes.
- Ran an unchanged control and both candidates through log-proven Direct3D
  hardware initialization and Training `NextLife`.
- Replaced noisy fixed-delay screenshots with 15-frame native Gamescope
  sequences. Preserved capture hashes and logs without committing image bytes.
- Closed roadmap packet M1.2 and made a bounded record-126 `+0x04`/`+0x08`
  discriminator the sole active M1.3 packet.
- Promoted reusable positive-target render content to high-confidence
  supported status while keeping complete object semantics unknown.
- Added a hardware renderer evidence gate to [[START HERE]],
  [[Agent Operating Manual]], [[Wine Linux Play Baseline]], the environment
  handoff, and [[Decision Log]].

## Conclusions

- **Confirmed:** both guarded rebinds are accepted by the exact PC executable
  under Direct3D hardware at 640×480×16 and reach `NextLife`.
- **Confirmed:** phase-matched record-124 output differs only within
  `61x242+369+0`, and record-125 output differs only within
  `24x127+616+101`. These overlap the placement boxes independently isolated
  in `EXP-20260812-008`; outside each union, zero pixels differ.
- **Confirmed:** the positive target selected through the bounded `0x49` path
  contributes placement-local visible render content.
- **Unknown:** whether the target is a complete object definition and the exact
  meanings of its entry/command fields.

## New hypotheses

No new hypothesis. [[HYP-20260812-001 - shared payload targets identify reusable render content]] is now high-confidence supported within its stated PC boundary.

## Contradictions discovered

- The initial selector retained its default software choice during a
  preliminary control. Its 320×200 `INITSOFTRENDER` run was rejected.
- One fixed-delay record-124 screenshot contained broad animation-phase noise,
  while a repeat did not. The retained sequence resolves this: chosen frame 07
  is exactly identical outside the placement-local difference unions.

## Tests run

- Both manifests staged from Training SHA-256 `494d2818…d5a22` to the expected
  `b8012a95…f720e` and `b8ea00be…0ed9` outputs.
- `cmp -l` found changes only at `0x26F8–0x26F9` and `0x2718–0x2719`.
- Three accepted Wine/Gamescope runs passed the hardware log gate, loaded
  Training, completed `InitMainGame`, and entered `NextLife`.
- Forty-five native 640×480 screenshots were captured across the matched
  sequences; ImageMagick exact comparison produced 2,980 and 1,076 differing
  pixels, with zero differences outside the two placement unions.
- Final repository checks are recorded in the handoff response and commit.

## Unresolved questions

- Exact meanings of record fields `+0x04`, `+0x08`, `+0x0C`, `+0x0E`, and
  payload/target subfields.
- Whether positive-target reuse generalizes visibly to a non-Training scene.
- Negative-count target grammar and other scene dispatches.
- Complete object-definition, material, and animation boundaries.

## Recommended next action

Execute [[Project Roadmap#M1.3 — Record selection and payload discrimination]] with the
exact static field reads and the two planned record-126 `+512` candidates.

## Git commit if applicable

Bounded commit message: `research: validate hardware target rebinds`.
