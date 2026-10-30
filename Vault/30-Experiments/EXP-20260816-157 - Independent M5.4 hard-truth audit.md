---
type: experiment
id: EXP-20260816-157
date: 2026-08-16
question: 'Does independent fresh-context review support every M5.4 claim - the pre-registration integrity, the predicted triple, the runtime observation, the disclosed limits, the write and lifecycle boundary, and the gate-4 scoping?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit of retained artifacts and repository state; no game launch, debugger, or target write
environment_version: radare2 5.9.8; Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: audit at clean HEAD b861376 (prediction commit a58f962); read-only toward game media and originals; nothing committed, created, or modified
artifacts:
  - work/copies/EXP-20260816-156-evidence/candidate-trace.tsv
  - work/copies/EXP-20260816-156-evidence/control-trace.tsv
  - work/copies/EXP-20260816-156-helper/reset_probe.py
addresses:
  - "0x00432930"
  - "0x0059D910"
  - "0x0059D960"
  - "0x0059D9A0"
  - "0x0059A5B0"
file_offsets:
  - "0x4AD"
result: reject-two-unretained-quantitative-claims-runtime-result-and-boundaries-survive
created: 2026-08-16T19:15:00
updated: 2026-08-16T19:15:00
tags:
  - re/experiment
  - re/audit
  - milestone/m5
---

# EXP-20260816-157 - Independent M5.4 hard-truth audit

## Verdict

**REJECT**, narrowly, with the core result standing. The pre-registered
prediction is genuine, independently re-derivable, and was confirmed by an
unambiguous trace; the write boundary, lifecycle, and gate-4 scoping all
survive attack. Two quantitative claims in the completed note do not reproduce
from retained evidence, which is the same defect class this project rejected
in `EXP-20260816-145` and M5.2, held to the same bar.

No game process, debugger, or target write was used; nothing was committed,
created, or modified by the audit.

## Checks that passed

- **Pre-registration integrity.** `git show a58f962` contains the full
  prediction — the candidate row, `(501696, 31768, 502208)`, descriptor 552,
  the result-0/no-loop claim, the `+512` pit counterfactual, and the
  falsification conditions — committed at 16:41:46.
  `git diff a58f962 b861376` on the note touches only three frontmatter lines
  and appends the Observed section **below** the pre-registration rule.
  Nothing above it changed. The timeline coheres end to end: EXP-155 accept
  16:37:41, prediction 16:41:46, helper 16:46, control log 16:50, evidence
  16:54, `y:` restore 16:55, confirmation commit 16:57:00.
- **Prediction re-derived.** Rebuilding the candidate from the retail DAT with
  the guarded editor reproduces SHA-256 `91a27776...cb8965` with exactly one
  changed byte at `0x4AD` (`0x3C -> 0x3D`, Z `15438 -> 15694`). An independent
  resolver run gives control `(501696, 30092, 494016)` and candidate
  `(501696, 31768, 502208)`, both descriptor 552, floor, unambiguous, matching
  the registered table. The `+512` counterfactual reproduces
  `(501696, 64032, 510400)` on descriptor 572, the pit.
- **The terrain model is load-bearing.** Candidate shift and linear functions
  of the edited field (`15694 << 1 = 31388`, `30092 + 256 = 30348`,
  `30092 + 6*256 = 31628`, and others) all miss `31768`. The `+1676` delta is
  a plane recompute at the moved point, so the Y could not have been produced
  without the composed model.
- **The observation is unambiguous.** The candidate trace holds exactly one
  nonzero-`NextLife` row at `604.5 ms`; at `610.7 ms` — 6.2 ms later — the
  auxiliary triple becomes exactly the predicted value with `NextLife=0`. An
  adopted grounded value would carry current-position-like coordinates, and it
  does not: current had already advanced a frame. Internal level reads 3 in
  every row of both traces. The candidate log carries all six markers plus
  `Device has hardware acceleration`, zero `INITSOFTRENDER`, and the retained
  copy is byte-identical to the live file.
- **Write and lifecycle boundary.** Every helper subcommand runs the same
  preflight (executable SHA-256 pinned to retail or auto-hardware, cwd under
  `work/copies/`, non-`Z:` drive refusal); teleport is guarded on
  `NextLife == 0` and `level == 3`, trigger on `level == 3`; the sampler is
  strictly read-only; the writes are exactly one 24-byte
  `process_vm_writev` plus a byte and a word — 27 bytes in three calls per
  arm — with no ptrace attach, debugger, or breakpoint anywhere. Retail DAT,
  terrain, retail executable, and auto-hardware hashes are unchanged and `y:`
  is restored. The blind `0x18` byte is valid here because both traces show
  pre-trigger flags `0x0008`.
- **Gate-4 scoping.** "Supported for this module at its Level03 boundary" is
  exactly the scope the M5.4 packet specified, with the roadmap's guardrails
  intact.

## Defect 1 - an unretained no-loop window

The note claimed `NextLife` "stayed 0 for the remaining **7 seconds**". The
retained trace's final row is at `3076.1 ms`, so the retained post-reset
window is about **2.47 s**. The roughly 31/64 ms flag oscillation means a
longer silent tail is not possible — further state changes would have kept
printing rows. No retained artifact supports seven seconds.

## Defect 2 - a settle band the shipped tool contradicts

The packet widened the settle band to **121-129** in the experiment note,
[[Current State]], and the roadmap, but left `scripts/type1-reset.py`
(`SETTLE_LOW`/`SETTLE_HIGH` = 121/126) and
[[PC type-1 reset placement resolver]] publishing **121-126**. The tool's
`settled_y_estimate` for the accepted candidate row is `[31889, 31894]`, which
**excludes the observed 31897** — a live cross-artifact contradiction the
packet created and did not disclose.

## Retention gap

The evidence directory held no control-arm log. The claim that both arms
passed six markers was verifiable only from
`work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.log`, which the next launch
overwrites. Downgraded from a defect to a retention gap the correction must
close.

## Assessment of the disclosed limits

Both are honestly stated and correctly scoped. The control arm's
indistinguishability is not relied on anywhere else. The widened band is
reasonable **as a range of observed extremes across about five receipts**, and
is not too thin at that framing — provided it is stated as sample extremes
rather than a guarantee, which defect 2 prevented the tool from doing.

## Limitations

Nothing was run and no target memory was written, so the runtime story was
verified from retained artifacts plus live filesystem state, not by
reproduction. File and git times are consistent but not cryptographically
ordered. The helper's stderr receipts were not retained, so the exact
three-writes-per-arm count rests on the helper's code plus trace consistency.
Cleanup claims rest on the note; nothing contradicts them, and no game or
compositor processes exist now.

## Note on roadmap structure

Offered as observation only. The run of quick successes around Tunnels ground
is a consequence of **evidence density**: gates, terrain height, and reset
placement cross-validate each other, so packets there close fast and audits
are cheap. A first packet in an untouched subsystem will mostly be
corpus-building rather than code — the M5 entry gate made exactly that point
when it rejected `.ANM` for lacking a bounded contract (`KU-022`). Two cheap
bridges outward already sit in this audit trail: the type-1 table has at least
five unexamined consumers (`0x004317D0`, `0x004323A8`, `0x004369B0`,
`0x00436D25`, `0x0043CE60`) with index-ordered access, and `KU-064`'s
pointer-table lifecycle question is generic to all 64 record types. Nothing
structural failed — the milestone gates, entry gate, and packet discipline all
worked as designed — so the lever for breadth is which bounded unknown gets
the next packet, not a reorganisation.

## Corrective packet

M5.5 in [[Project Roadmap]]: restate the no-loop window from the retained
trace, retain and cite the control log, and make one settle-band statement
consistent across the note, the tool, the implementation note, and the tests.
