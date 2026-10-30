---
type: session
date: 2026-08-16
agent: James
status: reject
tags: [session, re/audit, re/audio]
---

# Audio census audit

## Verdict

**REJECT** at `00c5ae5` — [[EXP-20260816-160 - Independent audio census audit]].

Anchors and most counts survived independent re-derivation. Six Confirmed
claims did not: two counts (37 not 38 `mmio` sites, 12 not 17 thunk-reachable
functions), a false "every caller outside the module", `0x0042C29F` treated as
a function start when it is a loop label, "a window class is registered"
describing an `UnregisterClassA` cleanup, and a "music" label the note's own
Inferred section contradicted.

Material miss: `0x0042BA60` has zero direct call sites and is dispatched from
the `"DIRECTX"` `.data` record at `0x004D81E8`, so the census's caller
completeness could not stand.

Judged **Bounded** correct for the audio row; declined the offered downgrade
to Touched. Input split verified and warranted.

## Boundary

Offline: nothing run, no debugger, no target write, nothing committed or
modified; tree clean.

## Next

Identify `0x0042B020` (34 call sites), the module's busiest entry point.
