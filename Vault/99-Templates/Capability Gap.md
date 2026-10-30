---
type: capability-gap
id: CAP-NNN
status: observed
priority: medium
scope:
authority_required: none
evidence: []
tools: []
created:
updated:
tags:
  - implementation/tooling-gap
---

# Capability gap

## Need

State the concrete research operation that is difficult, unsafe, noisy, or
impossible. Do not describe a tool merely because it would be interesting.

## Confirmed limitation

Separate observed facts from inference. Cite an experiment, run ID, exact tool
version/output, address, or environment fact.

## Research impact

Name the current or likely roadmap packet affected. Explain what discriminator
is unavailable and what claims therefore remain bounded.

## Existing workaround

Record the current safe method, its coverage limits, and whether it has been
live-validated.

## Desired capability

Describe the smallest feature that closes the gap. Preserve read-only,
ownership, evidence, and artifact boundaries where applicable.

## Acceptance test

Give a reproducible pass/fail test with an exact target, expected receipt, and
cleanup or survival condition.

## Risks and authority boundary

State whether implementation needs user choice, root/sudo, external media,
network access, persistent configuration, target mutation, or broader capture.
The note records a need; it does not grant that authority.

## Alternatives considered

List bounded alternatives and why they do or do not discriminate the question.

## Status and revisit trigger

Use `observed`, `available`, `blocked`, `deferred`, or `resolved`. State the
event that should cause another review.

## Resolution evidence

Link the validation run, implementation note, environment update, and any
affected known unknown when resolved.
