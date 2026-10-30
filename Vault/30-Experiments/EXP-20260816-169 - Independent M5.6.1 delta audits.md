---
type: experiment
id: EXP-20260816-169
date: 2026-08-16
question: Does the M5.6.1 correction, including the last direct/static table-scope repair, survive wholly new path-bounded James audits?
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline path-bounded delta audits; no game, Wine, Gamescope, debugger, target write, originals access, or cross-port access
configuration: first audit subject 45cc15b8717fecfb0f383184e02746b0d6fb710c over 3504f6a; final audit subject dd034c9086c71bcd5cb0e4cbe08ae6c317739590 over 45cc15b; tracked files, exact named work copy, and explicit named logs only; no find or broad filesystem hashing
working_directory: /home/dev/ABLPC
artifacts:
  - work/copies/EXP-20260816-168-m56-correction/evidence/correction-focused-26.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/correction-make-check.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/correction-input-movie-isolated.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/correction-process-names.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/correction-final-vault-lint.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/correction-final-tracked.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/m561-delta2-vault-lint.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/m561-delta2-tracked.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/m561-acceptance-vault-lint.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/m561-acceptance-tracked.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/m561-acceptance-process-names.log
  - work/copies/EXP-20260816-168-m56-correction/evidence/m561-acceptance-sinks.log
addresses:
  - "0x004337EF"
  - "0x00433803"
  - "0x00433807"
  - "0x00436D50"
  - "0x00436D5F"
  - "0x00436D6F"
file_offsets:
  - "0x00032C07"
  - "0x00036150"
  - "0x0003615F"
  - "0x0003616F"
result: accept-m561-at-dd034c9-activate-m57
created: 2026-08-16T21:15:00-04:00
updated: 2026-08-16T21:15:00-04:00
tags: [re/experiment, re/audit, re/gameplay, milestone/m5]
---

# EXP-20260816-169 - Independent M5.6.1 delta audits

## Final verdict

**ACCEPT** exact clean commit
`dd034c9086c71bcd5cb0e4cbe08ae6c317739590`.

M5.6.1 is complete. The grain-gate opening resolver is admitted as M5's
second module only for the twelve confirmed Tunnels/City mechanisms at the
corrected contract in EXP-166/168. M5.7 is Active. This accepts no
implementation, global family exclusivity, meaning for `0x00599C69`, type-1
semantic name, runtime action, or broader trigger engine.

## First path-bounded delta audit — REJECT `45cc15b`

A wholly new verifier completed the mandatory startup sequence using explicit
tracked paths only. It rehashed the permitted work-copy executable to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
and independently reproduced:

- City state write `0x004337EF`, index test `0x00433803`, and gate-0 byte
  write `0x00433807` / file `0x00032C07`;
- one-row X/Y/Z loads `0x00436D50`/`5F`/`6F` at file
  `0x00036150`/`5F`/`6F`;
- helper/Tunnels arithmetic and every corrected contract boundary;
- all nine explicitly named EXP-168 evidence hashes and their 26/648/1/26/648,
  process, Vault 476/0/0, and tracked-0 contents.

It rejected one residual live site only. In
[[PC level roster and numbering]], corrected prose made global exclusivity
Inferred, but the table still used absolute column `Grain gates`, thirteen
`no` cells, and two `yes` cells. That table still asserted absence the direct-
reference evidence could not prove.

## Exact one-file correction

Commit `dd034c9086c71bcd5cb0e4cbe08ae6c317739590` changes only
[[PC level roster and numbering]]:

- column `Grain gates` becomes `Confirmed direct/static grain-gate family`;
- thirteen `no` cells become `none found`;
- Tunnels/City `yes` cells become `confirmed` with their existing 9/3 counts;
- the lead-in now says the column follows from direct/static evidence.

No other tracked file changed. Directly logged validation reports Vault
476/0/0 at SHA-256
`0a1a1730faa93704fa7c9b59b5c35a03832de688fb52365ea37e2b414ab20a51`
and tracked audit 0 at SHA-256
`341e3736a49a7e7722f7f5f57b7db2b03da46772492f3ecf3c2341ab8d5e30e4`.

## Second fresh path-bounded audit — ACCEPT `dd034c9`

A second wholly new verifier repeated the explicit startup and delta review,
confirmed the one-file/one-claim correction, checked table/prose consistency,
verified the two named delta logs and clean tree, and returned **ACCEPT**. It
also retained the already-audited M5.6.1 limits:

- twelve known mechanisms, not absence of indirect/aliased/cached families;
- City index-0 address-named `[0x00599C69] = 1`, semantics Unknown;
- rejected type-1 path reads one row; original runtime is its first failed
  criterion and other criteria remain unassessed;
- M5 had one accepted module until this verdict; M5.7 stayed blocked;
- KU-065 remains open and all passing denominators remain qualified.

Neither path-bounded audit accessed `originals/`, the external PS1 tree, or an
untracked broad filesystem surface. They used no `find`, game/runtime process,
debugger, or target write and made no repository edit.

## Consequence

The entry ratchet is closed at `dd034c9`. M5 now has two admitted modules.
M5.7 may implement the pure grain-gate resolver, but the implementation is a
new worker packet and must receive its own standing fresh-context hard-truth
audit.

After acceptance propagation, Vault lint reports `478 notes, 0 errors,
0 warnings` at SHA-256
`0871a6563bb699d7c8f25f5913333af9d966f688a636210a82113a6e037137e2`,
and tracked audit remains 0 at SHA-256
`341e3736a49a7e7722f7f5f57b7db2b03da46772492f3ecf3c2341ab8d5e30e4`.
Closure finds no game, Gamescope, Wine server/client, debugger, pytest, or
`rr`, and no private sink. The same 32 unowned `winedevice.exe` helpers remain
under user systemd PID `1927`, PIDs `68248`-`344284`; process-name log SHA-256
`d621dbeceef0808203ce1c6e7ea7a8e8dd893b180c323ed5eee63409cd59879c`.
