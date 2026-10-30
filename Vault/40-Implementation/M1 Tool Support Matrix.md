---
type: implementation
status: active
created: 2026-08-12
updated: 2026-10-02
tags:
  - implementation/modding
  - re/file-format
---

# M1 Tool Support Matrix

This matrix is the review boundary for M1 tooling. It describes what the tool
can safely do and keeps byte-operation support separate from semantic claims.
Evidence comes from `EXP-20260812-006` and `EXP-20260812-008` through
`EXP-20260812-013`.

## Supported inspection

| Surface | Accepted boundary | Evidence/status |
|---|---|---|
| Prefix parser | The bounded `LEVEL*.DAT` prefix in [[PC LEVEL DAT prefix]]; full input bytes and unknown suffix retained | 21 PC files, zero prefix failures (`EXP-20260812-006`) |
| Scene records | Primary or secondary 20-byte records through their signed `+0x0E` sentinel | Static PC walk plus GDB record access (`EXP-20260812-008`) |
| Candidate center | Signed dwords at `+0x00`, `+0x04`, `+0x08` | Upstream selection use; axis names/units unknown (`EXP-20260812-011`) |
| Field `+0x0C` | Signed word representation | Positive values have a demonstrated visibility-bound use; negative semantics unknown (`EXP-20260812-012`) |
| Payload targets | Only records satisfying `(flags & 0xBFEF) == 0x49`, and only their positive-count target layout | Static consumer and 990-reference corpus (`EXP-20260812-009`) |

`inspect --payload-targets` deliberately filters to the supported masked
dispatch class. It must not fail merely because the same file contains an
unrelated negative-count or other-dispatch payload. `EXP-20260812-013` made
this boundary material on the exact Level 01 DAT.

## Supported manifest operations

| Operation | Guards | Changed bytes | Semantic limit |
|---|---|---|---|
| `set-scene-record-position` | Exact input SHA, section/index, three signed dwords | Selected record `+0x00–+0x0B` only | Historical operation name; edits candidate-center inputs, not demonstrated render position |
| `set-scene-record-field-0c` | Exact input SHA, section/index, expected signed word | Selected record `+0x0C–+0x0D` only | Positive visibility-bound use demonstrated; negative values remain offset-named bytes |
| `set-scene-record-payload-target-offset` | Exact input SHA, section/index, masked dispatch `0x49`, expected old pointer, valid old/new positive blocks | Selected payload target dword only | Reusable visible content demonstrated in Training; complete object definition unknown |

Manifests have exactly `schema_version`, `name`, and `files` at the root.
Each file entry has exactly `path`, `sha256`, `format`, and `edits`. File paths
are safe relative POSIX paths and may occur only once, case-insensitively, to
avoid ambiguous Windows targets. Operation objects reject unknown fields.

These three operations remain manifest schema 1's complete surface. Schema 2
retains them unchanged and separately adds the opaque exact-hash whole-file
copy documented in [[M4 Exact Whole-file Replacement]]. That extension does
not widen the supported `LEVEL*.DAT` parser or edit boundary recorded here.

## Fail-closed rejection matrix

The tool rejects:

- malformed/truncated prefixes and impossible counts or offsets;
- unknown manifest versions, formats, root fields, operation names, or
  operation fields;
- duplicate file targets, traversal/absolute paths, wrong hashes, and unsafe
  `originals`/`media` roots;
- invalid section/index/range values;
- target rebinds outside masked dispatch `0x49`;
- target mismatches, negative-count target layouts, out-of-bounds tables,
  invalid command references, and invalid positive blocks.

The tool does not expose arbitrary byte patches, sentinel edits, negative-
count target writes, other-dispatch payload edits, unknown suffix editing, or
semantic names for unconfirmed fields.

## Preservation and acceptance gates

- Every edit starts from an exact source hash and writes to a distinct output.
- Sparse `apply` and full-tree `stage` leave the input unchanged and emit
  `.ablpc/receipt.json` with input/output hashes and normalized edit details.
- Synthetic tests assert locality and rejection behavior without game data.
- Corpus scans cover multiple PC files without committing their bytes.
- Training and Level 01 exact recipes have byte-local receipts and acceptance
  from the unchanged executable under the 640×480×16 Direct3D path
  (`EXP-20260812-010` through `EXP-20260812-013`).

`EXP-20260814-061` independently confirms that all three operations still
apply under schema 2 (3/3 synthetic cases) and that the schema-1 suite remains
green. It also finds one generic output-plan limitation shared by both schema
versions: the fixed receipt is not included in containment preflight, and
deterministic destination/receipt-parent blockers can fail after an earlier
write. This does not change the supported M1 byte-edit boundary.
`EXP-20260814-062` supplies the M4.3 worker correction: every destination and
the fixed receipt now share deterministic topology preflight, the four audit
reproductions fail before mutation, and the focused manifest/LEVEL suite passes
47 tests. Independent `EXP-20260814-063` accepts that correction after all
three M1 operations pass under both schema versions, 6/6 applications with
3/3 byte-identical cross-schema outputs. The correction adds no M1 operation
and is not a general rollback guarantee for unpredictable I/O.

`EXP-20260814-064` adds a worker-complete composition layer without widening
this matrix. For exactly two manifests, the three rows above claim their exact
parsed destination intervals—12 bytes, 2 bytes, or the 4-byte payload-target
field—and merge only when claims from different inputs are disjoint. The
emitted manifest still contains only the existing operations and is revalidated
through the same parser/application path. Synthetic apply/stage results and the
tracked target-record-124 plus field-record-125 pair pass; overlapping claims
fail with deterministic asset-free JSON before output. Independent M4.6 is
recorded in `EXP-20260814-065` with `REJECT`: exact claim/conflict behavior
survives, but global byte-span sorting can reverse edits inside one valid input
before combined revalidation. Exact M4.7 must preserve each input's authored
edit-index sequence without adding an M1 operation or widening this matrix.
N-way and cross-input semantic reconciliation remain unsupported.

`EXP-20260814-066` supplies that exact worker correction. Canonical input rank
now determines the inter-input grouping, while original edit index preserves
each input file entry's sequence. The rejected `0x98`/`0xA4`/`0x21C` case and
descending-offset/same-span guard regressions pass without changing any M1
operation, byte claim, schema, or receipt. Independent `EXP-20260814-067`
accepts the correction after both rank orientations, a longer authored chain,
the full conflict/collision matrix, 28/28 topology cases, and 6/6 schema
applications pass. A genuine cross-input guard dependency still fails closed;
no semantic ordering or new M1 operation is implied.

`EXP-20260814-068` adds only removal of a dedicated ordinary sparse overlay.
It recomputes the same existing-schema M1 output and unchanged ordinary receipt
from the supplied manifest/source, then requires byte-exact receipt, output
hash, regular-file, and exact-tree equality before deletion. Composed M1 and
exact local M1-plus-opaque overlays apply/remove successfully, while all
rejected cases preserve exact source/overlay snapshots. This adds no M1 edit,
field meaning, schema, or receipt. Independent `EXP-20260814-069` preserves
every ordinary M1 removal application but rejects complete preflight for a
bind-mounted overlay directory. Exact M4.11 adds only mount-topology refusal
before mutation; it does not add an M1 edit, field meaning, schema, or receipt.
`EXP-20260814-070` completes that correction at the worker boundary. Private
namespace bind mounts at the overlay root, an intermediate directory, recorded
M1 output, and receipt all refuse with exact source/overlay/independent-target
snapshots unchanged; ordinary composed M1 and M1-plus-opaque local cycles
remain byte/hash stable. Independent `EXP-20260814-071` preserves those M1 and
exact-path results but rejects M4.11 acceptance: a stable mount alias at a
proper parent traversed to reach the overlay root is absent from the exact
root/descendant plan, so cleanup can return success after removing the
independent overlay. Exact M4.13 adds only that traversed-ancestry preflight
correction. It does not add an M1 edit, field meaning, schema, receipt, or
deletion target. `EXP-20260814-072` completes M4.13 at the worker boundary:
the proper-parent alias now refuses with exact snapshots unchanged, ordinary
filesystem ancestry remains usable, and the composed M1 plus M1-plus-opaque
local families again pass twice with unchanged sources. Independent
`EXP-20260814-073` rejects M4.14 only because a hidden lower alias
covered by a distinct ordinary top filesystem still taints their shared
ancestry pathname. Exact M4.15 may only exclude that covered lower record while
retaining every M1 application/local hash and all prior mount refusals. No M1
surface is widened. `EXP-20260814-074` now completes that exact worker
correction: same-path parent-stack coverage filters hidden lower candidate and
source records, the visible ordinary-top overlay removes completely, and the
uncovered ancestor plus four exact planned-path mounts still refuse unchanged.
Both tracked M1 local families again apply/remove twice with exact prior hashes
and unchanged sources. That worker result changed no M1 operation, field
meaning, schema, receipt, or deletion target.

Independent `EXP-20260814-075` preserves every M1 application and local hash
but rejects M4.16 at the mount-classification boundary. A newer uncovered bind
alias reused a freed numerically lower mount ID than its still-mounted source;
numeric-ID ordering omitted it and removal changed the independent mounted
target. Exact corrective M4.17 changes no M1 edit, field meaning, schema,
receipt, destination, source preservation, or accepted composition behavior.
`EXP-20260814-076` completes only that worker correction through verified
current-Linux later-mount order. Both tracked M1 local families again apply/
remove twice with established hashes and unchanged sources; focused/full tests
pass 105/293. No M1 edit, field meaning, schema, receipt, destination,
composition, or source-preservation boundary changes. At that worker boundary,
M4.18 still had to audit the removal classifier independently.

Independent `EXP-20260814-077` now returns M4.18 `ACCEPT`. Position,
field-`0x0C`, and payload-target applications pass under schemas 1 and 2 at
6/6 with 3/3 cross-schema byte equality; both tracked M1 local families again
apply and remove twice with exact established receipt/output hashes and
unchanged sources. The complete focused/full suites remain 105/293. This
accepts only the current-Linux removal classifier around existing M1 outputs;
it changes no M1 parser, operation, field meaning, schema, receipt,
destination, composition, or source-preservation contract. Exact M4.19 may
describe these accepted hashes and limits in the versioned compatibility
statement but may not widen them.

`EXP-20260814-078` now completes that exact description at the M4.19 worker
boundary. The strict v0.1 statement names schemas 1/2,
`pc-level-dat-prefix-v0`, and exactly the three operations in this matrix; its
Training and Level 01 hashes are demonstrated anchors cross-checked against
the tracked manifests, not a global parser allowlist. Eighteen asset-free
drift tests and the 311-test canonical suite pass. No M1 parser, operation,
guard, field meaning, receipt, source-preservation, or runtime claim changes;
at that worker boundary, fresh-context M4.20 still had to audit the statement.

`EXP-20260814-079` rejects M4.20 only at the compatibility checker's authority-
alignment layer: an effective later launcher assignment survives the expected
substring, with adjacent receipt-constant and Environment contradictions in
the same class. Independent reconstruction still confirms schemas 1/2, all
three M1 operations, both demonstrated DAT anchors, 17/17 declaration-family
rejections, and 311 canonical tests. Exact M4.21 may change only asset-free
authority extraction/uniqueness and regressions. It grants no M1 parser,
operation, guard, field-meaning, hash-allowlist, receipt, source-preservation,
or runtime authority.

`EXP-20260814-080` completes that exact M4.21 worker correction with Python-AST
extraction of the unchanged schemas 1/2, `pc-level-dat-prefix-v0`, and the
three existing M1 operations. Duplicate/changed contract declarations now fail
closed; both demonstrated DAT manifests remain strict authority anchors rather
than a parser allowlist. The focused/full suites pass 36/329 after final docs,
and no M1 parser, operation, guard, field meaning, receipt, source-preservation,
hash, or runtime behavior changes. Exact M4.22 is only the required independent
audit of that compatibility-alignment layer.

`EXP-20260814-081` rejects M4.22 without changing any M1 conclusion. The exact
schemas, format, three operations, two DAT anchors, statement bytes, four
M4.20 regressions, focused/full 36/329 suites, and nine-read no-game boundary
survive. The defect is checker completeness: Python validator rebinding and
conflicting duplicate tracked-manifest keys can coexist with the checked AST/
effective-last value. Exact M4.23 may only byte-pin the manifest implementation
and three tracked manifest authorities, together with the launcher, from their
same existing reads. It grants no new M1 hash allowlist, parser, operation,
guard, field meaning, receipt, source-preservation, or runtime authority.

`EXP-20260814-082` completes only the M4.23 compatibility-alignment correction
at the worker boundary. The manifest implementation and three tracked manifest
evidence files are now exact same-read byte authorities for the v0.1 statement
checker. Five direct pins and the duplicate-key/validator-rebind regressions
pass; focused/full suites are 47/340 and the exact M1 statement fields survive.
This is not a manifest-loader hash allowlist and grants no new M1 parser,
operation, guard, field meaning, receipt, source-preservation, input-policy, or
runtime authority. At the worker boundary, exact M4.24 still had to audit the
immutable result.

`EXP-20260814-083` independently accepts that exact M4.23 boundary. The
statement, five pin hashes, schemas 1/2, both DAT recipes, all three M1
operations, guards, 10/10 predecessor rejections, 5/5 direct and missing-pin
failures, nine-read boundary, and 47/152/340 suites survive. M4.25 may reuse
existing M1 record/offset facts only to report deterministic write-free ranges
for one manifest; it may not change an M1 parser, manifest/receipt schema,
operation, guard, field meaning, input authority, source-preservation claim, or
runtime conclusion.

`EXP-20260814-084` completes that exact M4.25 report at the worker boundary.
All three operations in this matrix report their existing section/index/record
offsets and exact 12-/2-/4-byte destination spans under schemas 1 and 2, in
authored order, from ordinary prepared output. Exact source snapshots and
independently calculated output bytes/hashes pass; combined M4/M1/
compatibility tests are 161/161. No M1 parser, operation, guard, field meaning,
manifest/receipt schema, input authority, source-preservation, or runtime
conclusion changes. Exact M4.26 must independently audit these report claims.

`EXP-20260814-085` independently accepts those exact report claims. Direct
packed-byte expectations reproduce primary and secondary record locators,
12-/2-/4-byte spans, sequential same-span guards, no-op values, authored order,
and schema-1/schema-2 output hashes without trusting the report helper. The
combined M4/M1/compatibility suite remains 161/161; exact receipts, five pins,
nine reads, source preservation, and all M1 meanings remain unchanged. M4.27
is only a milestone-closure evidence audit and grants no new M1 parser,
operation, guard, field meaning, input authority, or runtime conclusion.

`EXP-20260814-086` completes that ledger and rejects M4 closure without
changing any M1 parser or byte conclusion. All three M1 operations remain
supported and exact current receipt bytes retain their accepted normalized
edit details. The open capability is operational: current replay/removal still
requires the original manifest, so the receipt is not yet sufficient authority
on its own. Exact M4.28 may reconstruct only the current existing-schema
manifest from strict ordinary receipt fields and reuse ordinary preparation;
it may not add an M1 operation, field meaning, schema, input authority, or
weaker guard. The separate clean-copy lifecycle exit gate also remains open.

`EXP-20260814-087` completes that exact M4.28 worker without changing an M1
parser, schema, operation, guard, byte locator, or field meaning. Strict
receipt reconstruction copies only the already normalized current M1 edit
fields into an equivalent existing-schema manifest, then ordinary M1
validation/preparation independently reruns every source hash, record/layout,
guard, authored-order, output-hash, and receipt check. Schema-1/schema-2
applications for all three M1 operations, no-op behavior, composition, exact
receipts, source preservation, and combined M4/M1/compatibility tests remain
green at 208/208. This worker result granted no new M1 semantic conclusion and
required exact M4.29 before `KU-051` could resolve.

[[EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit]]
retains that exact M1 boundary: independent current-format mapping is exact,
80/80 strict input cases reject, the combined M4/M1/compatibility suite remains
208/208, both tracked M1 local compositions replay/remove twice with their
prior hashes, and no M1 parser, schema, operation, guard, locator, or field
meaning is falsified. The `REJECT` is confined to external receipt parent
acquisition: a checked parent can change into a directory link before final
file acquisition while retaining the same accepted receipt inode. Exact M4.30
may correct only that component-stability boundary and grants no new M1
semantic conclusion.

[[EXP-20260814-089 - Component-stable external receipt acquisition]] completes
that exact M4.30 worker without changing an M1 parser, schema, operation,
guard, record locator, byte range, or field meaning. Receipt parents are now
opened relative to retained no-link directory descriptors and the complete
chain must reacquire identically before strict parsing. All three current M1
operations remain reconstructed through their existing normalized receipt
fields and ordinary preparation; combined M4/M1/compatibility tests pass
216/216, and both tracked M1 local families pass twice with prior hashes and
unchanged sources. At the worker boundary, exact M4.31 still had to audit only
the acquisition claim. No new M1 semantic or runtime conclusion followed.

[[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]]
retains that exact M1 boundary. The combined M4/M1/compatibility suite passes
216/216, both tracked M1 local compositions replay/remove twice with prior
receipt/output hashes and unchanged source, and the independent component/
final mapping cases do not falsify any M1 parser, schema, operation, guard,
locator, byte range, or field meaning. Its `REJECT` is confined to receipt-
chain descriptor cleanup: one close error skips later descriptors. Exact M4.32
may correct only exception-safe exhaustive release and grants no new M1
semantic or runtime conclusion.

[[EXP-20260814-091 - Exception-safe receipt-handle-chain closure]] completes
that exact M4.32 worker without changing an M1 parser, schema, operation,
guard, locator, byte range, or field meaning. Combined M4/M1/compatibility
tests pass 223/223; both tracked M1 local compositions retain prior hashes and
unchanged sources. Exact M4.33 must independently audit only descriptor
release/error propagation. No new M1 semantic or runtime conclusion follows.

[[EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit]]
accepts that release boundary without changing any M1 parser, schema,
operation, guard, locator, byte range, or field meaning. Twenty-eight fresh
indexed close cases pass; combined M4/M1/compatibility remains 223/223; both
tracked M1 local families replay and remove twice with prior exact hashes and
unchanged sources. `KU-051` resolves only for the existing strict receipt and
exact-source boundary. Exact M4.34 audits the separate same-tree clean-copy
lifecycle and grants no new M1 semantic or runtime conclusion.

[[EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit]] rejects
M4 completion without changing any M1 parser, schema, operation, guard,
locator, byte range, or field meaning. Complete staged/forced-copy trees cannot
use dedicated sparse removal, while removable apply/replay trees are not
complete launch inputs. Exact M4.35 may add only restoration of already
prepared M1 outputs inside an authenticated complete staged tree; every
schema-1/2 and cross-schema byte/receipt result remains an unchanged retained
gate.

Later the same day: [[EXP-20260814-094 - Manifest-driven clean-copy restoration]]
implements M4.35, which keeps the existing M1 behaviour, and
[[EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit]]
accepts M4 at the documented current-Linux, asset-free boundary.
[[M4 Exact Whole-file Replacement]] owns that chain. Manifest schemas 1/2 and
the three operations above remain the whole M1 surface
(`reimplementation/ablpc/manifest.py`).

[[EXP-20260814-094 - Manifest-driven clean-copy restoration]] completes that
worker boundary without changing an M1 parser, schema, operation, guard,
locator, byte range, receipt, or field meaning. All three M1 operations under
schemas 1/2 restore 6/6 to source content; a composed two-edit M1 tree also
restores. Combined M4/M1/compatibility tests pass 250/250 and retained M1 local
cycles preserve prior hashes. Exact M4.36 must audit only the surrounding
whole-tree authority/mutation boundary; no new M1 semantic or runtime claim
follows.

[[EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit]]
retains schemas 1/2 and all three M1 restoration operations 6/6, composed M1
restoration, both exact M1 local families, and 250 combined M4/M1/compatibility
tests. Its `REJECT` concerns only case-insensitive collisions among unrelated
complete-tree paths. Exact M4.37 changes no M1 parser, operation, guard,
locator, byte range, receipt, or field meaning; no M1 semantic or runtime claim
follows.

[[EXP-20260814-096 - Complete-tree case-insensitive path uniqueness]] supplies
only that surrounding full-tree admission correction. Combined M4/M1/
compatibility tests pass 260/260; the same-DAT and M1-plus-opaque local families
retain their exact receipt/output/source hashes. No M1 parser, schema,
operation, guard, locator, byte range, receipt, field meaning, or runtime claim
changes. Independent exact M4.38 must retain this boundary.

[[EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit]]
accepts that surrounding admission correction. All three M1 restoration
operations under schemas 1/2, composed same-DAT behavior, the exact same-DAT
and M1-plus-opaque local hashes, and 260 combined tests remain green. `KU-052`
resolves only at the joined current-Linux lifecycle; no M1 parser, schema,
operation, guard, locator, byte range, receipt, field meaning, or runtime claim
changes. Exact M4.39 may align only the versioned compatibility statement.

[[EXP-20260814-098 - Strict v0.2 restoration compatibility statement]] changes
no M1 parser, schema, operation, guard, locator, byte range, receipt, field
meaning, or runtime behavior. It preserves the three tracked recipes and five
machine pins, adds only the independently accepted surrounding restoration
scope to v0.2. Exact M4.40 later establishes the complete combined collection
is 271 rather than the worker's recorded 266.

[[EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit]]
changes no M1 conclusion and passes all 271 M4/M1/compatibility tests. Its
`REJECT` is confined to compatibility statement selected-version binding,
object-key order, and malformed-ID error normalization. Exact M4.41 may change
only that checker/test/documentation layer; it grants no M1 parser, schema,
operation, guard, locator, byte-range, receipt, field-meaning, or runtime claim.

[[EXP-20260814-100 - Version-bound canonical compatibility-statement strictness]]
changes only that checker/test/documentation layer. It rejects the exact
selected-version, recursive key-order, and typed-ID attacks and passes 284
combined M4/M1/compatibility tests. No M1 parser, schema, operation, guard,
locator, byte range, receipt, field meaning, local recipe hash, or runtime
claim changes. Exact M4.42 is audit/docs-only.

[[EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit]]
changes documentation only and retains all 284 combined M4/M1/compatibility
worker results. Its `REJECT` is confined to compatibility selected-path link
identity: the default active pathname can resolve to the historical selected
file and validate v0.1. Exact M4.43 may change only lexical selection and
regular non-link admission around the statements; it grants no M1 parser,
schema, operation, guard, locator, byte range, receipt, field meaning, local
recipe hash, or runtime claim.

[[EXP-20260814-102 - Lexical selected-statement identity and non-link admission]]
changes only that compatibility-checker boundary and passes 288 combined tests.
No M1 parser, schema, operation, guard, locator, byte range, receipt, field
meaning, local recipe, or runtime claim changes. M4.44 is audit/docs-only.

[[EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit]]
accepts that checker boundary and all 288 combined tests without changing any
M1 parser, schema, operation, guard, locator, byte range, receipt, field
meaning, local recipe, or runtime claim. Its M4 completion disposition is
limited to the documented asset-free current-Linux boundary and does not widen
this matrix.

[[EXP-20260814-104 - Second independent M4 post-closure verification]] retains
the 288 combined tests and returns a second bounded M4 `ACCEPT`. It changes no
M1 parser, schema, operation, guard, locator, byte range, receipt, field
meaning, local recipe, or runtime claim.

## Distribution boundary

Distribute independently authored manifests, receipts, documentation, and
tool code only. Never distribute the sparse overlay, staged tree, screenshots,
logs containing extracted assets, or any original game file as a mod package.
The recipient applies the manifest to their own exact-hash work copy and
checks the emitted receipt. The authoring commands and hardware validation gate
are in `reimplementation/README.md` and [[Wine Linux Play Baseline]].
