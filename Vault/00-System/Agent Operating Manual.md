---
type: policy
status: active
updated: 2026-10-02
tags:
  - system/policy
---

# Agent Operating Manual

This is the canonical operating policy for Codex and Claude. Root instruction files summarize it but must not diverge from it.

## Durable memory

Follow the startup sequence in [[START HERE]]. Treat the vault as the authoritative handoff surface. Keep [[Current State]] concise; chronology belongs in session notes indexed by [[Session Index]].

## Evidence discipline

- Mark claims **Confirmed**, **Inferred**, or **Unknown**.
- Cite an address, offset, artifact path, binary hash, experiment ID, or run ID.
- Seek two independent evidence forms for important conclusions.
- AI output and decompiler output are not ground truth.
- Never promote an interpretation because it sounds plausible or has been repeated.
- Record contradictions rather than silently selecting a preferred story.

## Original material

- Never modify `originals/`.
- Never commit originals, game assets, disc images, ROMs, Windows media, dumps, or virtual disks.
- Hash and inventory source material before analysis.
- Conduct experiments on explicit copies under `work/copies/`.
- Store generated evidence in `static/`, `dynamic/`, `reports/`, or a bounded task packet.

## Naming

Use the rules in [[Naming Conventions]]. Unknown semantics must remain visibly unknown. A stable address-based name is better than a confident fiction.

## Static analysis

Ghidra databases are working state, not the review surface. Export function metadata, references, decompiler text, strings, imports, and call relationships into reviewable text or JSON under `static/exports/`. Decompiler output is evidence, not source code.

## Dynamic analysis

Record binary hash, OS, environment version, configuration, working directory, steps, expected result, observed result, artifacts, and addresses/offsets. Debugger/control services must bind to localhost or host-only networking. Start debugger automation read-only; changes to memory, registers, code, execution, or breakpoints require explicit approval.

Renderer-facing Wine experiments use the game's hardware-acceleration path
unless the bounded question explicitly compares renderers. At the initial
selector do not assume a default or infer selection from chooser pixels.
Pre-register the exact no-direction/Up/Down and confirmation sequence for the
experiment, then require the complete game log to pass all six hardware
markers. Reject a hardware arm that enters `INITSOFTRENDER`, `SYSTEM MEMORY
ONLY`, or selected 320x200 mode; UI input intent or a screenshot alone is not
proof of the selected code path. The historical R2c retail calibration used
RC0 with no direction before Return and permitted one fresh RC1 with exactly
one Down only if RC0's complete log proved software. On 2026-08-19 R2c moved to
the auto-hardware build instead
([[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]).

## Runtime instance lifecycle

- Before launching a game, emulator, compatibility layer, debugger, capture
  process, or private audio sink, audit for instances left by earlier work.
- Keep one active experiment instance unless a bounded comparison explicitly
  requires parallel arms. Close and verify each arm before starting the next.
- Record the exact owned process IDs and private sink/module IDs at launch.
  Cleanup may target only those identities: request graceful termination,
  wait for a bounded interval, recheck identity, and use forced termination
  only on the same still-owned processes when needed.
- Unload private audio sinks and close agent/sub-agent instances as soon as
  their bounded task is finished. Completed, errored, or superseded workers
  must not be left running merely because their result may still be useful.
- At session closure, audit the process table and audio sinks again. Record any
  instance that cannot be closed and do not start a replacement that would
  obscure ownership.

## Implementation

Independent implementations must follow demonstrated behavior rather than pseudocode aesthetics. Parsers must bounds-check every read, preserve unknown fields, reject impossible offsets/counts, test multiple files, and use synthetic fixtures where possible.

## Agent task sizing

Use bounded evidence packets. Good tasks compare related functions, categorize imports, identify repeated offsets, export references, write a parser, or propose one discriminating experiment. Never use "reverse engineer the entire game" as a unit of work.

## Cross-port evidence

Follow [[Cross-Port Evidence Policy]]. Treat the PS1 project as an external comparative source, never as PC ground truth. Do not vendor, symlink, submodule, or broadly copy it into ABLPC. A PS1 name, field, format, behavior, or interpretation may seed a PC hypothesis, but it remains unconfirmed until cited PC static or runtime evidence supports it. Every cross-port claim must record the external repository commit, source path, platform, comparable PC locator, similarities, differences, and a discriminating PC experiment.

## Session closure

Complete every item in the end-of-session sequence in [[START HERE]]. Include tests actually run, unresolved questions, and the exact next action.
