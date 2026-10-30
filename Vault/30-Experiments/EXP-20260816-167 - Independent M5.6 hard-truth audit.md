---
type: experiment
id: EXP-20260816-167
date: 2026-08-16
question: Does exact clean M5.6 subject 3504f6a survive a fresh-context adversarial audit of its native claims, six-criterion admission, and live propagation?
status: rejected
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static/documentation audit; no game, Wine, Gamescope, debugger, or target write
configuration: exact clean subject 3504f6a833306882532d8fce202517478a45d495 over parent 21c5e870d7c1d5c3470f9749f64a24a9cb1fc244; fresh James verifier; permitted exact-hash work copy; one disclosed accidental read-only originals traversal whose output was discarded
working_directory: /home/dev/ABLPC
artifacts: []
addresses:
  - "0x00416580"
  - "0x00432F0C"
  - "0x00432F49"
  - "0x00432F6A"
  - "0x00432F85"
  - "0x00432F9D"
  - "0x004337D6"
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
result: reject-m56-for-city-write-row-expression-criterion-and-exclusivity-overclaims
created: 2026-08-16T20:30:00-04:00
updated: 2026-08-16T20:45:00-04:00
tags: [re/experiment, re/audit, re/gameplay, milestone/m5]
---

# EXP-20260816-167 - Independent M5.6 hard-truth audit

## Verdict

**REJECT** exact clean subject
`3504f6a833306882532d8fce202517478a45d495` over parent
`21c5e870d7c1d5c3470f9749f64a24a9cb1fc244`.

The grain-gate candidate's core native arithmetic, accepted behavior receipts,
asset-free fixtures, distinct offline-preflight outcome, KU-063 correction,
auto-hardware MOC correction, and non-binding future-subsystem queue survive.
Four claim/contract defects prevent admission. M5.6.1 is the only correction;
M5.7 remains blocked.

## Confirmed surviving boundary

On exact retail SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:

- helper `0x00416580` uses wrapping `sub`, arithmetic `sar 8`, wrapping
  `imul`/`add`, and signed `<`;
- Tunnels checks closed type `0x10C7`, compares grain at `0x00432F0C`, uses
  signed proximity at `0x00432F49`, writes opening type `0x1068` at
  `0x00432F6A`, couples rows 0/4 at `0x00432F85`/`0x00432F9D`, and decays by
  140 while above `0x708`;
- City requires state `-1`, calls the proximity helper, compares grain at
  `0x004337D6`, writes state `0x20` at `0x004337EF`, then decrements positive
  state and applies call-site animation deltas;
- ten of twelve mechanisms have accepted exact `min-1`/`min` transitions;
  row 1's narrower receipt and row-0/4 non-separability are disclosed.

These facts come from independently reproduced disassembly of the permitted
work copy and EXP-137/138/144/145/148/149. No result of the accidental broad
search described below supports them.

## Rejection findings

### 1. Omitted City index-0 direct mutation

After City writes state `0x20`, `test esi,esi` at `0x00433803` selects gate
index 0 and `0x00433807` (file `0x00032C07`) executes
`mov byte [0x00599C69],1`. EXP-166 promised an immediate mutation plan but
omitted this direct branch-local write. Its semantics are Unknown. The bounded
repair is to include it by address without assigning a field or feature name.

### 2. False two-row type-1 description

EXP-166 said the later index-ordered path loads indexed and next rows. In fact,
with `i = [0x0059F4C4]`, `0x00436D50` loads X from
`[base + 12*i + 4]`, `0x00436D5F` loads Y from
`[base + 12*i + 8]`, and `0x00436D6F`, after incrementing the temporary,
loads Z from `[base + 12*(i+1)] = [base + 12*i + 12]`. All three components
belong to one indexed row.

### 3. Unsupported "single missing criterion"

Missing cited original runtime behavior is the decisive **first failed**
criterion for the index candidate. The packet did not establish that path's
complete state contract, edge behavior, or distinct modding outcome, so it
cannot state that runtime is the only missing criterion. The smallest runtime
discriminator survives, corrected to retain count, `0x0059F4C4`, the one
selected row, current triple `0x0059C184`/`88`/`8C`, candidate triple
`0x0059C1A8`/`AC`/`B0`, and before/after index state. A receipt triggers a
new six-criterion audit; it does not admit the path automatically.

### 4. EXP-146 authority promoted beyond its evidence

EXP-146 confirms 22 direct/static references to grain byte `0x0059D9B1`,
their classification, dispatcher routing, and known L3/L4 structure binding.
Reference enumeration does not prove absence of address-computed, aliased, or
cached consumers. Global gate-family exclusivity is therefore Inferred. The
candidate can remain bounded to the twelve confirmed mechanisms without that
stronger claim.

## KU-065 recurrence and evidence limit

The verifier ran unredirected `make check` and observed
`1 failed, 647 passed in 19.47s` at
`tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes`.
At `tests/test_input_movie.py:659`, the mismatched replay returned `3` with
`reason: "anchor_timeout"` and marker/detail `NextLife.` instead of expected
return `1`. The isolated node then passed `1 passed in 1.68s`; the focused
grain/coordinate pair passed `26 passed in 0.29s`.

None of those invocations was retained to a raw file, so their byte-exact
stdout/stderr and hashes are unavailable. This identifies one exact-signature
intermittent test, not the identity of the four earlier lost failures, and it
does not close KU-065. Every M5.6.1 validation invocation must use direct raw
redirection.

## Integrity disclosure

The verifier mistakenly ran:

```bash
find . -type f -not -path './.git/*' -print0 | xargs -0 sha256sum 2>/dev/null | rg '<three-worker-log-hashes>' || true
```

That broad read-only search could and did traverse `originals/`, contrary to
the audit's explicit no-access boundary. Its output was discarded and supports
no claim here; no file was modified. All rejection locators were obtained
earlier from the permitted exact-hash work copy and independently reproduced
there. Because of the breach, this audit can supply a rejection defect packet
but cannot serve as final acceptance. The correction requires a wholly new,
explicitly path-bounded verifier.

## Exactly one corrective packet

M5.6.1 changes documentation and evidence only: include the City byte write,
correct the type-1 row expression, use first-failed-criterion language, narrow
EXP-146, record the qualified KU-065 recurrence, preserve validation logs at
explicit ignored-work-copy paths, and propagate those boundaries. No M5.7
implementation, runtime, target write, cross-port consultation, semantic name
for `0x00599C69`, or expansion beyond the twelve confirmed mechanisms is in
scope. Stop after a clean commit and a new path-bounded James ACCEPT.
