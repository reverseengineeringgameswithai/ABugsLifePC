---
type: experiment
id: EXP-20260816-147
date: 2026-08-16
question: Do the two committed level-analysis packets (EXP-146 grain-gate level exclusivity and the PC level roster / internal-index derivation) survive an independent offline hard-truth audit against the exact retail executable?
status: rejected-then-accepted-after-correction
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8; repository Python 3.14; no game/Wine/Gamescope launch, no target write
configuration: fresh-context adversarial audit at clean worker HEAD 5a265f15a133493363ea8929e5e18c4b37a1f4b9; read-only toward all game media and originals/; no launch, target write, commit, or staging
working_directory: /home/dev/ABLPC
artifacts: []
addresses:
  - "0x0041475F"
  - "0x00414766"
  - "0x00418780"
  - "0x00432B30"
  - "0x00432F0C"
  - "0x00433606"
  - "0x00433790"
  - "0x00433900"
  - "0x004337D6"
  - "0x004338B0"
  - "0x00436308"
  - "0x0043A911"
  - "0x004C6A30"
  - "0x004DA9C8"
  - "0x004DAA80"
  - "0x00599AF8"
  - "0x0059D9B1"
  - "0x0059F020"
  - "0x00861C84"
result: reject-for-incorrect-position-counter-address-then-accept-after-worker-corrected-0x00059AF8-to-0x00599AF8
created: 2026-08-16T13:03:00
updated: 2026-08-16T13:10:00
tags:
  - re/experiment
  - re/static
  - re/audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260816-147 - Independent level-analysis audit

> [!correction] Later scope rejection
> EXP-147 accepted the 22-reference census and known L3/L4 bindings correctly,
> but also repeated EXP-146's unsupported promotion from direct/static
> references to global family exclusivity. EXP-167 narrows the live authority:
> the census, classification, dispatcher, structures, and roster survive;
> absence of address-computed, aliased, or cached consumers is unproved.

## Verdict and authority

**Original verdict: REJECT. Final disposition: ACCEPT after the worker's
in-place correction** (see "Correction confirmed" below).

For a single specific, isolated, easily-fixable defect: the
carousel **position-counter address** cited in
[[PC level roster and numbering]] is wrong. The note states the counter is
`word [0x00059AF8]` (frontmatter `addresses`, and twice in body), but the
consumer instruction it points to (`0x00414766`) reads `word [0x00599AF8]`.
`0x00059AF8` is **below the image base** and unmapped (`.data` spans VA
`0x004C1000`–`0x00864000`), so the cited address cannot be reproduced or
disassembled — it breaks the note's own "Static derivation" reproduction
instruction. This is a dropped-hex-digit transcription error
(`0x00599AF8` → `0x00059AF8`).

This is not a rejection of the level-analysis science. The independently
verified direct grain-byte enumeration and gate classification, the 17-level
dispatcher routing, the gate-structure
L3/L4 binding, the roster table values, the progression→internal-index
mapping, the direction argument, the dispatcher-slot accounting, and the
overclaim caveats — verified cleanly and is recorded below. Per the same
scoping used in [[EXP-20260816-145 - Independent runtime gate mapping audit]],
the reject is narrow: the worker corrects the three occurrences of
`0x00059AF8` to `0x00599AF8` and resubmits.

This is an offline independent audit of committed PC-native static evidence.
No game, Wine, Gamescope, debugger, or helper was attached to a live target;
no game state or target byte was changed; nothing was committed or staged.

## Procedure

- Re-read the startup authority ([[START HERE]]), the two packets under
  audit ([[EXP-20260816-146 - Grain-gate level exclusivity static proof]],
  [[PC level roster and numbering]]), and the context notes
  [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]],
  [[EXP-20260815-139 - Static grain-gate trigger geometry]],
  [[EXP-20260816-144 - Runtime grain-gate visual mapping]], and
  [[PC autonomous game control]].
- Rehashed `bugs.exe` to
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
  (matches).
- Independently ran the two radare2 reference queries, disassembled every
  cited site in context, re-decoded the consumer's raw bytes, dumped the
  roster table, recomputed the mapping arithmetic, and ran the hygiene and
  `make check` gates. `.text` VA→file offset is `VA - 0x400C00`.

## Packet A — EXP-146 grain-gate level exclusivity

### Check A1 — grain-byte reference census (PASS)

`aar; axt @ 0x0059d9b1` returns exactly **22** code references. Each was
disassembled in context; the classification matches the note table exactly:

| # | Kind | Addresses | Verified |
| ---: | --- | --- | --- |
| 2 | positional grain-vs-requirement gate | `0x00432F0C`, `0x004337D6` | yes |
| 4 | pickup increment (read+store) | `0x00417D7B/8D`, `0x00418C40/52` | yes |
| 2 | Training completion (`cmp ==0x32`) | `0x00417DC2`, `0x00418C8A` | yes |
| 4 | clamp / reset (read+store) | `0x0043A0EB/F3`, `0x00442EC2/ED0` | yes |
| 3 | level non-gate grain events | `0x00436208/308`, `0x0043A911` | yes |
| 7 | HUD counter read / digit render | `0x00416BB7`, `0x00416C2C`, `0x0042E93C`, `0x0044341D`, `0x00443457`, `0x004434C5`, `0x0044358B` | yes |

2+4+2+4+3+7 = 22, fully accounting for every reference. The two positional
gates are the only ones feeding a barrier-open decision:

- `0x00432F0C` (in Tunnels `0x00432B30`): after the `0x10C7` closed-gate
  type check (`0x00432EF8`), `eax` is loaded from record `+0x08`
  (`[esi*4 + 0x4DA9D0]`, the requirement), grain (`cl`) is compared
  (`cmp ecx, eax`; `jl` skips), then proximity math (`sar 8`, squared sum vs
  `0x2710` = 100²) gates the open.
- `0x004337D6` (in City `0x00433790`): grain (`dl`) is compared to the
  inline `10*(index+1)` computed by `lea eax,[esi+1]; lea ecx,[eax+eax*4];
  shl ecx,1; cmp edx,ecx` (`0x004337D1`–`0x004337E3`); on pass, state is
  set to `0x20` at `0x004337EF`. The retail requirement is inline, not a
  table read.

The two claimed non-gate level readers were disassembled and are genuinely
not gates: `0x00436308` reads grain and compares it to the **previously
stored** value `[0x0059F404]` (`0x00436300` load, `cmp eax, ecx`,
`je`; on change writes `0x0059F400 = 0xE00` and updates `0x0059F404`) — a
counter-change detector; `0x0043A911` does `cmp al, 0x28` (40) with `jae`,
a grain-`<40` scripted event (`mov …, 0xA`), no requirement/proximity/
barrier. The direct/static census holds: all 22 references in that addressing
form are enumerated and only two are barrier gates. It does not prove that
every possible gate must reference the byte directly rather than through an
alias or cached value.

### Check A2 — level dispatcher routing (PASS)

`0x00418780` does `dec eax; cmp eax, 0x10; ja <ret>; jmp dword
[eax*4 + 0x4187E8]` — a 17-entry jump table (internal levels 1–17) on the
value at `0x00861C84`. The jump table (`0x004187E8`, 17 dwords) points to
5-byte thunks, each resolving to a real routine. All 17 match the note:

| L | routine | L | routine |
| ---: | --- | ---: | --- |
| 1 | `0x004317D0` | 10 | `0x00437B70` |
| 2 | `0x00431CB0` | 11 | `0x00438040` |
| **3** | **`0x00432B30`** | 12 | `0x00438A80` |
| **4** | **`0x00433900`** | 13 | `0x00439410` |
| 5 | `0x00434170` | 14 | `0x00439E90` |
| 6 | `0x00434620` | 15 | `0x0043AE00` |
| 7 | `0x00434E10` | 16 | `0x0043BD10` |
| 8 | `0x004362D0` | 17 | `0x0043C340` |
| 9 | `0x00436B40` | | |

Only L3 routes to `0x00432B30`; only L4 routes to `0x00433900`, which calls
thunk `0x00401D52` → `0x00433790` three times (`0x00433944/62/7F`).

### Check A3 — gate-structure L3/L4 binding (PASS)

Reference analysis binds every gate-specific structure to L3/L4 only
(note addresses cite the disp32/imm operand field; radare2 reports the
instruction start, a consistent +1..+3 offset):

- Tunnels gate table `0x004DA9C8`: 5 refs (`0x0043281D`, `0x00432EF1`,
  `0x00432F6A`, `0x00432F9D`, `0x00433024`) — all inside the Tunnels
  initializer/routine.
- Tunnels template `0x004DAA80`: 1 ref (`0x00432818`, the initializer
  `mov esi, 0x4DAA80`).
- City state array `0x0059F020`: initializer `0x00433606` (`or eax,-1` at
  `0x004335FE` then writes `-1` to `0x0059F020/024/028`, matching the live
  `(-1,-1,-1)`), plus 4 refs inside `0x00433790` (`0x00433798`,
  `0x004337EF`, `0x0043383B`, `0x0043384B`).
- City requirement lookup `0x004338B0`: **zero** refs; the 32 bytes there
  are all `0xCC` (INT3 padding), confirming retail uses the inline formula.
- Routine callers: `0x00432B30` is reached only by thunk `0x00401429`
  (dispatcher L3); `0x00433790` only by thunk `0x00401D52` (from L4's
  `0x00433900`).

**Packet A result: all checks PASS.**

## Packet B — level roster / internal-index derivation

### Check B1 — roster table dump (PASS)

`0x004C6A30` holds the 16 dwords
`[17,1,3,2,6,10,11,4,5,14,7,12,13,9,8,15]`, terminated by `0xFFFFFFFF` at
`0x004C6A70` — byte-exact to the note.

### Check B2 — consumer disassembly (DEFECT; sole reject cause)

Raw bytes at `0x0041475F` are `0f bf 05 f8 9a 59 00` =
`movsx eax, word [0x00599AF8]`, then `0x00414766`
`mov eax, dword [eax*4 + 0x004C6A30]`, then `0x0041476E`
`mov dword [0x00861C84], eax`. The mechanism (position counter → table
lookup → internal-level global) is exactly as described, **but the cited
counter address is wrong**: the instruction reads `0x00599AF8`, while the
note states `0x00059AF8` in three places (frontmatter `addresses` line, and
body lines describing the "carousel position counter" and
`word [0x00059AF8]`). `0x00059AF8` is below the image base and unmapped;
`0x00599AF8` is valid `.data`. **Fix:** replace all three occurrences of
`0x00059AF8` with `0x00599AF8`. (The same typo also propagated into the
worker session note
[[2026-08-16 1237 - Claude - grain gate level exclusivity]] line 38; the
worker should reconcile it there too.)

Table-base reference sites verify: radare2 reports instruction starts
`0x00410139`, `0x00414766`, `0x00414807`, `0x0043DD81`; the note cites the
disp32 operand field (`+3`): `0x0041013C`, `0x00414769`, `0x0041480A`,
`0x0043DD84`. All four sites are present and correctly attributed. Aside
from the counter address, the disassembly claims are accurate.

### Check B3 — mapping arithmetic and accounting (PASS)

The progression→internal table in the note is arithmetically exact from the
dumped values (pos 0→17, 1→1, 2→3, 3→2, 4→6, 5→10, 6→11, 7→4, 8→5, 9→14,
10→7, 11→12, 12→13, 13→9, 14→8, 15→15). **City Entrance (position 7) →
internal 4**, matching the live `0x00861C84 == 4` reads in EXP-136/144. The
direction is unambiguous: reading the table as internal→progression would
give internal 4 → `table[4]` = progression 6, contradicting City Entrance's
observed position 7. The carousel internal set is
`{17} ∪ {1..15}` (the 16 table values), so **internal 16** is the only
dispatcher slot (1–17) not reachable from the carousel — matching the note.

### Check B4 — overclaim / caveats (PASS, one clarification recommended)

- (b) The training slot's LEVELxx relationship (position 0 → internal 17)
  is explicitly flagged as table-derived and "not separately verified"; the
  note does **not** claim a `LEVEL17` folder. Present and honest.
- (c) Internal 16's identity was explicitly left "not determined here";
  uncertainty about whether it was used was honest at this audit date.
  **2026-09-11 correction:** it is outside the carousel but reached by a special initialization path.
  EXP-20260911-020
  confirms the route; the slot must not be allocated as free.
- (a) The internal indices are repeatedly and correctly presented as
  statically derived; the four live-loaded names (Anthill, Tunnels, Council
  Chamber, City Entrance) are the only ones evidence-backed, and the note
  never claims to derive level **names** from the binary (the table yields
  only numeric indices). This is honest. *Recommended clarification (not a
  reject cause):* add an explicit sentence stating the progression order /
  level names are researcher-provided from the carousel while only the
  internal indices are static, to remove any residual ambiguity from
  "The full progression→internal-index mapping is statically derived."

**Packet B result: B1/B3/B4 PASS; B2 carries the sole defect.**

## Hygiene (PASS)

- `git status --porcelain` clean at HEAD
  `5a265f15a133493363ea8929e5e18c4b37a1f4b9`;
  `git log --oneline -3` = `5a265f1` / `cf9d6b0` / `9ab38d2`.
- `originals/` tracks only `.gitkeep`.
- `make check`: Vault lint 424 notes / 0 errors / 0 warnings, M4 statement
  valid (5 hash anchors), **610 passed**, tracked-file audit 0 violations.

## Accepted boundary (upon fix)

On correction of the three `0x00059AF8` → `0x00599AF8` occurrences, the live
acceptable boundary is: for the exact retail executable
`97c95ba5…27b878`, the 22 direct/static grain-byte references contain only
two positional barrier comparisons, in internal level 3 (Tunnels,
`0x00432B30`) and internal level 4 (City Entrance, `0x00433900` →
`0x00433790`); the 17-entry dispatcher and known gate structures independently
bind those two families to L3/L4. Global absence of indirect/cached families
is Inferred. The full progression→internal-index roster is statically
derived from the `0x004C6A30` table read by the consumer at `0x00414766`
using the position counter at `0x00599AF8` and written to `0x00861C84`,
with City Entrance = progression 7 = internal 4, training = internal 17,
and internal 16 the sole non-carousel slot. Level names remain
researcher-provided/observational; only internal indices are static. No
grain, executable, asset, or `originals/` mutation occurred.

## Correction confirmed (2026-08-16, post-verdict)

The worker corrected [[PC level roster and numbering]] in place: all three
`0x00059AF8` occurrences (frontmatter `addresses` line and the two body
lines) now read `0x00599AF8`, and the propagated copy in
[[2026-08-16 1237 - Claude - grain gate level exclusivity]] is fixed. The
worker also added the recommended Check-B4(a) clarification — the level
names and play order are researcher-provided while the internal indices are
statically derived, cross-validated only at the four live-loaded levels.

Independently re-verified: `0x0041475F` decodes to
`movsx eax, word [0x00599AF8]` (raw bytes `0f bf 05 f8 9a 59 00`), which is
valid `.data`; the corrected note now matches the binary. A repo-wide grep
confirms the only remaining `0x00059AF8` strings are inside this audit
note, the James session note, and the MOC entry, where they correctly
describe the before→after. `vault-lint` reports 426 notes / 0 errors / 0
warnings. This resolves the sole defect. **Verdict upgraded to ACCEPT.**
The worker still reconciles Current State / Known Unknowns and commits.

## Result

**REJECT (original verdict), upgraded to ACCEPT after correction**, for the
incorrect carousel position-counter address
(`0x00059AF8` cited three times in [[PC level roster and numbering]]; the
binary reads `word [0x00599AF8]`, and `0x00059AF8` is unmapped). All other
claims in both packets — grain-byte census and gate classification,
dispatcher routing, gate-structure binding, roster table values, mapping
arithmetic, direction argument, slot accounting, and the caveats —
independently verified. The worker corrects the three occurrences (and the
propagated session-note copy) and reconciles Current State / Known Unknowns.

## Follow-up

- Worker corrects `0x00059AF8` → `0x00599AF8` and resubmits; a re-check of
  the single edit suffices.
- Optional: add the explicit researcher-provided-names clarification from
  Check B4(a).
