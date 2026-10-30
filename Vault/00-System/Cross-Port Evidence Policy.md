---
type: policy
status: active
updated: 2026-08-11
tags:
  - research/cross-port
  - system/policy
---

# Cross-Port Evidence Policy

The PlayStation reverse-engineering project can accelerate PC research, but it is a different binary, platform, toolchain, data layout, and runtime environment. It is **comparative evidence**, not authority for the PC port.

## Repository boundary

- Keep the PS1 repository outside ABLPC at the path recorded in [[External Source Registry]].
- Treat it as read-only while performing ABLPC work. Do not modify, clean, reformat, commit, branch, or generate artifacts inside it.
- Do not vendor it, add it as a Git submodule/subtree, create a symlink into ABLPC, or copy its vault wholesale.
- Never copy PS1 disc images, binaries, assets, save states, dumps, generated images, Ghidra databases, or emulator state into ABLPC.
- Do not depend on an uncommitted PS1 working-tree state. Durable citations use a commit object plus a repository-relative path.

These rules prevent ABLPC history and search results from being polluted by unrelated generated state or copyrighted material.

## Epistemic boundary

A PS1 observation may:

- suggest search terms, signatures, constants, control-flow shapes, resource relationships, or experiments;
- identify a candidate concept to test in the PC port;
- provide a second implementation for structural comparison.

A PS1 observation may not, by itself:

- confirm a PC function name, address, field, structure, subsystem, format, constant, behavior, or bug;
- justify copying PS1 addresses or layouts into PC notes or code;
- increase confidence merely because multiple PS1 notes or agents repeat it.

Until PC evidence exists, use **Inferred** or **Unknown** and explicit qualifiers such as `ps1_candidate_...`. Promotion to **Confirmed** requires PC evidence under [[Evidence Standard]].

## What may enter ABLPC

Only bounded, reviewable material needed to support a specific comparison:

- a citation containing source ID, commit, repository-relative path, and relevant address/offset;
- a short text excerpt or independently written summary within copyright limits;
- hashes and metadata;
- a minimal hexdump or structural measurement when legally appropriate;
- an ABLPC-authored comparison table or experiment design.

Do not copy whole PS1 notes, source trees, decompiler exports, or artifact directories for convenience. Prefer citations over duplication.

## Required comparison record

Use [[Cross-Port Comparison]] and record:

1. The bounded question.
2. PS1 source ID, commit, path, and locator.
3. PC binary/disc hash and PC locator, if known.
4. Directly observed similarities.
5. Directly observed differences.
6. What remains unknown.
7. The smallest PC experiment that would discriminate the hypothesis.

Cross-port comparison notes live in `Vault/20-Research/Cross-Port/`. Task artifacts live in `research/cross-port/`. Neither location is a mirror of the external repository.

## Conflict rule

When PS1 and PC evidence disagree, preserve both observations. The PC executable under a controlled PC environment is authoritative only for claims about the PC port; the PS1 evidence remains authoritative only for its own observed build and environment.
