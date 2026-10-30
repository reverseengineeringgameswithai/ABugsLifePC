---
type: policy
status: active
updated: 2026-08-11
tags:
  - research/method
---

# Research Method

## Research loop

```text
Original behavior
      |
86Box observation
      |
Wine / debugger trace
      |
Ghidra static analysis
      |
bounded evidence packet
      |
Codex / Claude analysis
      |
hypothesis
      |
controlled experiment
      |
Vault evidence
      |
implementation + regression test
```

## Bounded questions

Each task should ask one question that available evidence can discriminate. Record the executable SHA-256, exact environment, configuration, working directory, procedure, expected result, observed result, artifacts, addresses, and offsets.

## Implementation-language selection

Follow [[Python and C reverse-engineering split]]. Python is the default
reference/controller for static parsing, orchestration, receipts, and
synthetic tests. Promote only a measured hot loop or intrinsically native ABI
boundary to C, retain a versioned interchange contract, and differentially
validate it against the Python reference. Language execution speed does not
change the evidence hierarchy.

## Evidence independence

Important conclusions should normally combine at least two evidence forms: cross-reference, breakpoint, Wine trace, Process Monitor trace, file offset, memory observation, comparison across files, or comparison across environments.

## Results

- **Confirmed:** directly demonstrated by cited static or runtime evidence.
- **Inferred:** supported interpretation not yet demonstrated.
- **Unknown:** meaning not established.

An experiment may be inconclusive. Preserve that result and design the smallest follow-up that distinguishes the leading interpretations.
