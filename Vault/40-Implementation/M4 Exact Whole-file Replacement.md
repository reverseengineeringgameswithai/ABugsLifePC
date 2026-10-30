---
type: implementation
status: accepted
created: 2026-08-14
updated: 2026-08-14
tags:
  - implementation/modding
  - implementation/manifest
---

# M4 Exact Whole-file Replacement

## Purpose and evidence boundary

Manifest schema 2 adds one asset-free operation for copying an exact file
already present in a user's derived work copy over a different exact file in
that same work copy. The initial recipe is only the accepted Direct3D
replacement from `EXP-20260812-033`:

- destination `CD/CHARS/FLICK.ALL`, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- replacement source `CD/CHARS3/FLICKD.ALL`, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

`EXP-20260813-049` establishes that the paths, hashes, instructions, and
receipt can be distributed without either file. [[EXP-20260814-060 - Exact whole-file replacement manifest boundary]] validates the implementation. This
note does not claim a `.ALL` layout, identity, interchangeability rule, or
compatibility with any other pair.

## Schema 2 boundary

The destination remains a normal manifest file entry. `format` is
`opaque-file-v0`, deliberately stating that no parser or field semantics are
involved. Exactly one edit is permitted:

```json
{
  "operation": "replace-whole-file",
  "source_path": "CD/CHARS3/FLICKD.ALL",
  "source_sha256": "6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4"
}
```

The file entry's existing `path` and `sha256` fields name and hash-lock the
destination. Schema 1 remains accepted unchanged. Schema 2 also accepts every
existing `pc-level-dat-prefix-v0` M1 operation, including a manifest that mixes
an existing M1 edit with an independent whole-file replacement.

## Fail-closed behavior

The M4.3 worker correction preflights every manifest entry, computes every
result, and validates the deterministic planned-path/type topology for every
destination plus `.ablpc/receipt.json` before ordinary sparse output. For
staging it validates the topology that the source tree would reproduce at each
planned destination and receipt before `copytree`. At the tested manifest/
schema boundary it rejects:

- a wrong destination or replacement-source hash;
- a missing or non-file source;
- absolute, traversal, redundant, backslash, drive/colon, NUL, or internal
  `.ablpc` paths;
- a source path that escapes the source root through a symlink;
- case-insensitive same source/destination paths;
- a replacement source that is also any manifest destination;
- duplicate case-insensitive destinations, unsupported schema/format/
  operation fields, protected roots, and overlapping source/output roots; and
- existing sparse destinations without explicit `--force`.

It also rejects symlinks in the requested output-root path, symlinked or non-
directory planned ancestors, and symlinked/non-regular planned destinations.
`--force` permits replacement only of an existing regular file. These M4.3
claims are worker-complete in
[[EXP-20260814-062 - Complete planned-output containment preflight correction]]
and independently accepted in
[[EXP-20260814-063 - Independent M4.3 hard-truth audit]].

A later bad manifest hash or any of the four deterministic planned-topology
blockers from `EXP-20260814-061` cannot leave an earlier output written. Under
an ordinary new output root, sparse application writes only destination paths
plus `.ablpc/receipt.json`; full staging copies the user work tree to a new
path, then changes only each destination, while the replacement source remains
present and unchanged.

## Receipt

Schema-2 receipts retain manifest order and record:

- destination `input_sha256`;
- replacement `source_path` and `replacement_sha256`; and
- destination `output_sha256`.

The synthetic suite proves byte-identical receipt JSON across two independent
outputs. The demonstrated recipe's output hash equals the replacement-source
hash.

## Validation and distribution

`tests/test_manifest.py` covers sparse success, deterministic receipts,
destination/source hash failures, unsafe lexical paths, symlink escape,
same-path rejection, source/destination collision, whole-manifest preflight,
full staging, schema-1 rejection of the new format, schema-2 compatibility with
existing M1 edits, CLI application, all four M4.2 topology reproductions,
requested-output-root symlinks, and positive forced regular-file replacement.
Existing M1 tests remain unchanged.

The ignored local corpus check uses
`work/copies/BUGS_PC-full-disc/PC/BUGS` and resolves both expected hashes. Its
sparse result under `work/mod-builds/M4-1-local-check-overlay-20260814`
contains only the destination and receipt, while both source-tree hashes remain
unchanged.

Distribute only the manifest, tool, documentation, and optionally its receipt.
Never distribute the sparse overlay or staged tree because they contain
user-owned game bytes. The exact recipe is
`mods/chars-flick-all-from-chars3-flickd-all.json`; user commands and limits are
in `reimplementation/README.md`.

## Independent M4.2 result

[[EXP-20260814-061 - Independent M4.1 hard-truth audit]] returns `REJECT` at
one bounded output-plan boundary. The exact schema/hash, ordinary sparse/
staged, deterministic-receipt, M1-compatibility, local-recipe, and no-game-
bytes results survive. Complete preflight and containment do not:

- `_write_prepared` sends fixed `.ablpc/receipt.json` directly to
  `_atomic_write`, so an existing `output/.ablpc` symlink can receive the
  receipt outside the requested root while `apply` returns success;
- a later non-directory destination parent can fail after an earlier sparse
  destination was written; and
- a source `.ablpc` file can make `stage` fail only after the tree was copied
  and its destination changed; and
- `--force` accepts a directory destination, then fails after an earlier
  destination write.

M4.1 was therefore not independently accepted at M4.2. Exact corrective packet
M4.3 now preflights every planned destination plus the receipt and closes those
four reproductions without changing schema or replacement scope; M4.4 accepts
that correction at the deterministic planned-path/type boundary.

## M4.3 worker correction

`EXP-20260814-062` closes all four M4.2 reproductions at the deterministic
planned-path/type boundary:

- the fixed receipt is part of the same preflight plan as manifest
  destinations, so `output/.ablpc` symlinks fail before a destination write;
- every existing planned ancestor is inspected with `lstat`, so a later
  regular-file parent blocker fails before an earlier write;
- non-regular destinations fail even under `--force`, while existing regular
  files retain positive force behavior; and
- `stage` validates the source topology that its planned writes would inherit,
  so a source `.ablpc` file fails before the staged root is created.

The focused manifest/LEVEL suite passes 47 tests and the complete suite passes
235. The exact ignored local recipe retains its two input hashes, byte-exact
replacement output, two-file sparse locality, deterministic receipt, and
source preservation.

This is not a general transaction or rollback guarantee. Permission or storage
changes, unrelated `copytree` failures, hardware/I/O faults, and concurrent
filesystem races after preflight may still fail after mutation. No new schema,
operation, receipt field, `.ALL` meaning, compatibility rule, or runtime result
is introduced.

## Independent M4.4 acceptance

`EXP-20260814-063` accepts immutable worker commit `adcceda`. It reproduces the
four M4.2 cases and 22 adjacent topology cases with explicit complete
source/blocker snapshot equality and earlier/outside/receipt/staged-root
absence. The focused and complete suites pass 47/47 and 235/235; all three M1
operations pass under both schema versions, and two exact local-recipe outputs
retain byte equality, deterministic receipts, sparse locality, and source
hashes. The worker diff is text-only and the tracked-file audit has zero
violations.

This acceptance does not widen the limitation above. Exact M4.5 subsequently
addresses only composition of two existing manifests or a deterministic byte-
range/opaque-file conflict report; it does not change this replacement
contract.

## M4.5 exact two-manifest composition

`EXP-20260814-064` is worker-complete; independent M4.6 later rejects its
complete done claim as recorded below. The new
`compose LEFT RIGHT --source-root ROOT` command accepts exactly two existing
schema-1/schema-2 manifests, independently executes their existing guards in
memory, and emits another existing-schema manifest only for disjoint cross-
manifest destination-byte claims. It adds no operation or receipt field.

The byte claims are offset-derived, not semantic guesses: existing position,
field-`0x0C`, and payload-target operations claim 12, 2, and 4 bytes at their
exact parsed PC offsets. `replace-whole-file` claims the complete original
destination interval, and any opaque claim sharing that destination conflicts.
Same-file entries also require exact path spelling, normalized source-hash
agreement, and format agreement. A replacement source may not become a
combined destination.

Inputs are ordered by validated canonical-JSON digest. Files are sorted by
normalized Windows path; M4.7 supersedes the initial edit ordering with
canonical-input grouping and original per-input edit index. Schema 2 is
selected iff either input uses it, and the combined name derives from the
ordered input digests. Reversing CLI arguments produces byte-identical success
output. On a conflict, stdout is empty and stderr receives compact
deterministic JSON containing canonical input names/digests, normalized
Windows destination, conflict kind, and exact half-open overlap when
applicable. No source or output bytes enter that report.

Synthetic same-file/different-file apply and stage outputs match independently
calculated results with ordinary receipts and source preservation. Exact M1
overlap, opaque collision, case/hash/format/path mismatch, and cross-manifest
replacement-source/destination fixtures fail before filesystem output. The
focused suite passes 58 tests and the complete suite 246. The tracked local
same-DAT pair and M1-plus-exact-opaque pair are order-independent and preserve
all source hashes; exact hashes are in `EXP-20260814-064`.

This is not N-way dependency or semantic intent resolution, a general dry-run,
removal, launch, compatibility, `.ALL` parsing, or a schema/receipt redesign.
The accepted M4.3 limitation for unpredictable I/O/races remains unchanged.
Fresh-context M4.6 independently rejects this worker result at the intra-input
ordering boundary below.

## Independent M4.6 rejection

`EXP-20260814-065` rejects immutable M4.5 commit `8419402` at one exact
existing-schema ordering boundary. `_prepare_manifest` accepts each input in
its authored sequence, but `_composed_file_entry_from_ranked_claims` then sorts
all claims for a destination by source byte span before combined revalidation.
That can reverse two edits inside one input.

The synthetic falsification is bounds-valid and contains no game bytes. Its
left manifest edits the payload-target field `[0x21C,0x220)` before position
`[0x98,0xA4)`; its right manifest claims only disjoint field-`0x0C` bytes
`[0xA4,0xA6)`. Both inputs apply independently. Forward and reverse compose
both fail after span sorting moves the position write first and invalidates the
pending payload-target guard's formerly valid old block. This does not require
semantic reconciliation: it requires preserving an existing input's
sequential edit contract.

The exact single-edit conflict detector, canonical identities, schemas,
receipts, M4.4 topology behavior, tracked local pairs, exact opaque recipe, and
asset-free boundary survive the audit. M4.7 corrects only deterministic
intra-input order preservation for exactly two inputs and must update the
current byte-location-sorted-edit documentation. N-way solving, cross-input
semantic dependency reconciliation, schema/receipt changes, `.ALL` parsing,
compatibility, dry-run, removal, launch, and general rollback remain outside
scope.

## M4.7 worker correction

`EXP-20260814-066` closes the exact M4.6 order reversal at the worker boundary.
`_composed_file_entry_from_ranked_claims` now orders claims first by canonical
input rank and then by that file entry's original edit index. Destination files
remain normalized-path sorted, while exact conflict selection still compares
byte claims only across the two inputs and chooses the earliest overlap
deterministically.

The bounds-valid `0x98`/`0xA4`/`0x21C` pair now applies independently,
composes byte-identically in both CLI argument orders, and produces saved
sparse/staged bytes equal to the authored payload-target-then-position sequence
plus the independent field edit. Adjacent regressions preserve descending-
offset and same-span sequential-guard order, retain empty opaque collision and
unequal distinct opaque behavior, and select the same earliest conflict when
multiple overlaps exist. The focused suite passes 63 tests and the complete
canonical suite 251; both tracked local composition hashes and output hashes
remain unchanged from M4.5.

Independent `EXP-20260814-067` now accepts the clean immutable correction. It
reproduces the exact pair, canonicalizes the order-sensitive input at either
rank, retains a three-edit authored chain plus a fourth shared-destination
edit, and passes the complete conflict/collision matrix. A genuine disjoint
cross-input guard dependency still fails closed during combined revalidation
in both argument orders. The focused/full suites pass 63/251, accepted
topology/schema matrices pass 28/28 and 6/6, both tracked local pairs and the
exact opaque recipe retain their hashes, and source/asset-free gates pass. The
two-input, existing-schema, no-semantic-reconciliation, and non-transactional
limitations above remain unchanged.

## M4.9 receipt-validated sparse-overlay removal worker

`EXP-20260814-068` adds `remove MANIFEST --source-root SOURCE --overlay-root
ROOT` only for dedicated sparse overlays produced by ordinary current-version
`apply`. It reuses `_prepare_manifest` and the unchanged receipt construction
to recompute every expected output and the ordinary receipt from the supplied
manifest and exact source root.

Before any unlink it requires:

- safe distinct source/overlay roots under the accepted protected-root and
  output-symlink rules;
- every recorded output and `.ablpc/receipt.json` present as single-link regular
  files below directory-only, non-symlink ancestors;
- strict UTF-8 JSON receipt parsing with no duplicate keys or non-JSON numeric
  constants;
- exact recomputed receipt data and the byte-exact deterministic ordinary
  `apply` encoding;
- every recorded output's recomputed SHA-256; and
- a no-follow complete tree walk containing exactly those files and their
  necessary directories, with no other file, directory, symlink, or FIFO.

After complete preflight it unlinks only the recorded sparse outputs and fixed
receipt, then prunes the authenticated empty directories deepest-first and the
empty overlay root. It returns the same recomputed receipt and has no source-
tree deletion target. A staged full tree necessarily contains extra copied
content and is rejected before deletion.

Thirty-two parameter-expanded cases raise the focused/full suites to 95/283
before documentation. They cover single/multi/composed and empty-output
success; source, output, and receipt drift; missing/symlink/FIFO/hard-link
topology; exact receipt field/JSON/encoding mismatches; every extra-content
type; staged-tree/root-safety
refusal; exact failure snapshots; and CLI behavior. Exact opaque, same-DAT
composed, and M1-plus-opaque user-owned local families each apply/remove twice
with deterministic receipts, absent overlay roots, and unchanged source hashes.

This worker boundary is not independently accepted. Fresh-context
`EXP-20260814-069` passes the ordinary success/refusal and local-recipe matrices
but rejects the complete-preflight claim. A pre-existing bind-mounted
intermediate overlay directory passes the current type/tree checks; removal
deletes the recorded file through that mount and the receipt before directory
pruning fails `EBUSY`. Both reproductions changed the overlay and independent
mounted target snapshots. It is not a staged-tree remover, source restoration
mechanism, trash/backup/package manager, receipt migration, or general
transaction.

## M4.11 mounted deletion-plan refusal worker

[[EXP-20260814-070 - Mounted sparse-overlay deletion-plan path refusal]] closes
the exact M4.10 falsification at the worker boundary. `remove_manifest` now
constructs its complete relative file/directory plan, reads Linux
`/proc/self/mountinfo` as bytes, decodes the kernel's octal path escapes, and
compares the overlay root plus every planned directory, output, and receipt
against the current mountpoint set before overlay traversal, receipt reads, or
the first unlink. Missing, malformed, or empty mount topology fails closed with
`ManifestError`; no fallback silently relies on `lstat` or device numbers,
which cannot identify same-filesystem bind aliases.

Asset-free private user/mount-namespace cases bind an independently snapshotted
ordinary overlay at the root, at intermediate `D`, at the recorded output, and
at `.ablpc/receipt.json`. All four refuse with byte/type/link-complete overlay,
source, and independent-target snapshots unchanged. Their paths contain an
embedded space, so the live cases also exercise mountinfo `\040` decoding.
Ordinary manifest tests pass 84/84; focused manifest/LEVEL and complete suites
pass 99/287 before documentation. The exact opaque, same-DAT composed, and
M1-plus-opaque local families each apply/remove twice with their established
deterministic receipt/output hashes, absent roots, and unchanged three source
hashes.

The guard is intentionally Linux removal-only and requires readable trustworthy
`/proc/self/mountinfo`; a broader portability/compatibility statement remains a
written M4 exit-gate issue. Concurrent topology/I/O changes after preflight
remain outside the non-transactional boundary. No schema, receipt, operation,
staged/source deletion, unmount, backup/trash/package/rollback, `.ALL`, runtime,
M2, or PS1 claim changes.

## Independent M4.12 rejection

[[EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit]]
returns `REJECT` without weakening the exact-root/descendant worker evidence.
The permitted non-mount focused/full suites pass 95/283, the removal,
composition, and topology/schema/receipt selectors pass 32/17/28, 12/12 pure-
function mountinfo parser/failure checks pass, and all six ordinary local
cycles retain the exact M4.11 hashes and unchanged sources.

The complete mounted-plan-path claim nevertheless fails for one omitted
topology. A disposable James QA case and Root's independent repeat place an
otherwise exact overlay below a proper-parent alias to an independent parent.
The exact overlay root and expected descendants are not mountpoints. Cleanup
returns success and removes the independent overlay; the source stays unchanged
while both visible-overlay and independent-target snapshots change. This is a
stable pre-existing layout, not a concurrent change.

The implementation agrees with the result. `_resolved_root` resolves the
supplied overlay, but `_validate_unmounted_deletion_plan` compares only that
exact root and its expected descendant directories/files with mountinfo. It
does not include the proper parent directories traversed to reach the root.
M4.11 therefore remains worker-complete but is not independently accepted.

## M4.13 traversed-ancestry worker correction

[[EXP-20260814-072 - Traversed overlay-root ancestry mount-alias refusal]]
retains mount ID, device, filesystem root, and mountpoint from the same trusted
Linux mountinfo input. Exact overlay-root and descendant-plan mountpoints keep
M4.11's unconditional refusal. For proper ancestry only, a newer mount is an
alias when its filesystem root is already reachable through an older same-
device mount record at a different visible path.

The exact M4.12 reproduction now refuses before overlay content traversal or
unlink: the supplied overlay root and descendants are unmounted, its proper
parent aliases an independent parent, and complete visible-overlay/source/
independent-target snapshots remain unchanged. A pure regression retains
ordinary root, `/home`, `/tmp`, and same-path nested filesystem mount records
while classifying subdirectory and whole-filesystem-root aliases. All five
private namespace mount cases, 101 focused and 289 full tests, and all six
tracked local apply/remove cycles pass with the established hashes.

This worker correction does not create a general mount-ownership or
portability policy. It changes no schema, receipt, operation, deletion target,
staged/source behavior, transaction boundary, or accepted M4.3/M4.7 claim.

## Independent M4.14 rejection

Independent
[[EXP-20260814-073 - Independent M4.13 traversed-ancestry hard-truth audit]]
returns M4.14 `REJECT`. The exact uncovered proper-parent alias refuses before
traversal/unlink with complete snapshots unchanged, all retained matrices and
six local cycles pass, and the canonical suites remain 101/289. One stable
stacked topology falsifies the ordinary-filesystem classification: a lower bind
alias covered at the identical parent pathname by a distinct ordinary top
filesystem still contributes that shared pathname to `_mount_alias_points`, so
valid removal on the visible ordinary filesystem refuses unchanged.

## M4.15 covered lower-record worker correction

[[EXP-20260814-074 - Covered lower mount record exclusion]] uses the retained
mountinfo stack relation without changing alias semantics otherwise. A record
is covered only when another retained entry names it as `parent_id` at the
same normalized mountpoint. `_mount_alias_points` removes those covered records
before both candidate and source comparison; the remaining mount ID/device/
filesystem-root/path test is unchanged.

The exact M4.14 lower-bind/upper-`tmpfs` case now succeeds. Removal authenticates
and deletes the overlay from the visible ordinary top filesystem, returns that
top parent to its exact empty pre-overlay snapshot, and leaves the source and
hidden independent target exact. The M4.12 uncovered proper-parent alias and
M4.11 exact root/intermediate/output/receipt mounts still refuse before
mutation. Pure controls include both a covered alias candidate and a covered
source path, ordinary filesystem/subvolume/same-path/different-device records,
and uncovered subdirectory/whole-root aliases. All six namespace cases, 102
focused and 290 full tests, and all six local cycles pass with established
hashes.

This remains a Linux removal-only worker correction. It adds no general mount
ownership or portability policy and changes no schema, receipt, operation,
deletion target, staged/source behavior, transaction boundary, or accepted
M4.3/M4.7 claim. It entered exact fresh-context M4.16 independent audit before
another capability could be selected.

## Independent M4.16 rejection

[[EXP-20260814-075 - Independent M4.15 covered-stack hard-truth audit]] returns
M4.16 `REJECT` without weakening M4.15's covered-stack result. The exact lower-
bind/ordinary-top and three-level stack cases remove completely with sources
and hidden targets exact; hidden candidate/source, visible top alias, all six
namespace cases, parser/failure matrices, 102/290 suites, and six local cycles
survive.

One uncovered alias escapes preflight when mount IDs are reused. A disposable
scratch `tmpfs` held ID 1081, the independent source then held ID 1082, and
after only the scratch was unmounted a newer bind alias to that source reused
ID 1081. The remaining M4.13 comparison interprets numeric ID order as mount
age and skips the lower-numbered candidate. Removal succeeds through the alias,
preserves the work-copy source, and changes the independent mounted target,
alias view, and overlay. Exact M4.17 may correct only that numeric-ID-reuse
classification defect or fail closed on its exact ambiguity while retaining
M4.15 and every accepted boundary.

## M4.17 mount generation-order worker correction

[[EXP-20260814-076 - Mount generation order for ancestry aliases]] retains
legacy mountinfo IDs for identity, parent-stack coverage, and device/root/path
classification but removes them from age decisions. Current Linux
`listmount(2)` with `LISTMOUNT_REVERSE` enumerates later mounts first under
unique non-reused IDs; `statmount(2)` maps each unique ID back to the legacy ID,
legacy parent, and device. The implementation bounds both syscall interfaces,
requires valid order/masks/IDs, cross-checks the complete old-ID set plus
parent/device metadata, and rereads mountinfo byte-exact before using the
snapshot. Every disagreement fails before overlay traversal.

`_mount_alias_points` now compares verified `mount_order`; M4.15 same-path
parent-stack visibility remains unchanged. In the tracked private namespace,
the newer alias is required to reuse the released lower legacy ID beneath its
still-mounted source, yet removal refuses before traversal/unlink with complete
source, independent-target, alias, and overlay snapshots exact. Covered
ordinary-top removal and all prior mounted refusals survive. Targeted/focused/
full tests pass 10/105/293 and all six local cycles retain exact hashes.

At its worker boundary this was a current-Linux removal-only correction pending
exact independent M4.18. It added no general mount ownership/portability,
schema, receipt, operation, deletion-target/order, staged/source, transaction,
runtime, M2, or PS1 authority.

## M4.18 independent acceptance

[[EXP-20260814-077 - Independent M4.17 mount-order hard-truth audit]] returns
`ACCEPT` against immutable commit
`67ea1618a7d3ad741c81d3eaaa1d32d99874631b`. Independent current-x86_64 UAPI
and Linux v7.0 source review confirms the v0 request layout, syscall numbers,
result offsets, reverse later-first order, and last-ID pagination. Injected
syscall, sequence, stat-result, mapping, parent/device, read, byte-change, and
parser failures all refuse before traversal.

A separately authored private namespace reproduces legacy old IDs
1081/1082/1081 for scratch/source/later alias. Independent batch-2 reverse
enumeration places the alias before its source; removal raises the ancestry-
alias refusal before an overlay traversal guard and preserves complete source,
independent-target, alias, and overlay snapshots. M4.15 covered-stack behavior,
all seven tracked namespaces, 120 tuple permutations, ordinary removal 32/32,
composition 17/17, broad topology/schema/receipt 37/37, explicit M1 6/6,
focused/full 105/293, and six exact local cycles survive.

This accepts authenticated ordinary sparse-overlay removal only under the
stated current-Linux prerequisites. It remains non-transactional after
preflight and does not establish general mount ownership, other platforms,
staged/source removal, restoration, package management, launch, dry-run,
compatibility, `.ALL`, runtime, M2, or PS1 behavior. Exact M4.19 now addresses
only the still-unmet versioned compatibility statement exit gate.

## M4.19 versioned compatibility statement worker

[[EXP-20260814-078 - Versioned exact M4 compatibility statement]] publishes
canonical asset-free `reimplementation/compatibility/m4-v0.1.json` and a
strict checker. The statement identifies five demonstrated executable/input
hash anchors, schemas 1/2, the two existing formats and four existing
operations, exact two-input composition, existing apply/stage/remove
workflows, the tested Fedora/Python/Wine/Gamescope versions, and explicit
unsupported surfaces. An unlisted hash is outside the demonstrated v0.1
anchor set; it is not automatically rejected by the manifest parser.

Removal is separately and exactly labeled current-x86_64-Linux-only with
readable, cross-checked mountinfo/listmount/statmount prerequisites, fail-
closed topology failure, and the accepted non-transactional-after-preflight
limit. The Wine/Gamescope fields record the accepted launcher and four
positive Direct3D log markers plus `INITSOFTRENDER` rejection, not broad
platform compatibility or launch automation.

The checker validates canonical strict JSON, the launcher, three tracked
manifests, Environment Status, Wine baseline, and README without opening game
files. Eighteen focused drift tests and 311 canonical tests pass. No manifest
schema, receipt, operation, apply/stage/compose/remove, `.ALL`, runtime, M2,
PS1, mount-policy, or transaction behavior changed. This is worker evidence
that was pending exact fresh-context M4.20.

## M4.20 hard-truth disposition and exact M4.21 correction

[[EXP-20260814-079 - Independent M4.19 compatibility-statement hard-truth audit]]
returns **REJECT**. Independent reconstruction confirms exact canonical bytes,
five evidence/tracked-authority anchors, the existing schema/format/operation/
workflow and receipt/removal boundaries, exact current host/Wine/Gamescope
claims, 17/17 declaration-family rejections, focused 18/18, canonical 311/311,
and exactly nine tracked asset-free reads with no game-root access.

The failure is confined to authority alignment. In a disposable source copy,
`OUTPUT_WIDTH=1` immediately after checked `OUTPUT_WIDTH=2560` changes the
effective launcher value but still passes `_require_fragments`. Effective
filter and `_RECEIPT_RELATIVE` overrides and a contradictory Environment
kernel row also pass. The present checked-in authorities are consistent; the
checker nevertheless does not reject the representative drift class claimed
by M4.19.

Exact M4.21 may change only compatibility-checker extraction/alignment and its
asset-free regressions. Every already-claimed scalar must resolve to one
unambiguous/effective declaration. The statement, manifests, authority values,
schema, receipt path, operations, workflows, apply/stage/compose/remove,
launcher behavior, assets, runtime, M2, mount policy, and transaction boundary
must remain unchanged.

## M4.21 source-aware authority extraction worker

[[EXP-20260814-080 - Unambiguous effective compatibility-authority declarations]]
completes the exact correction at the worker boundary. Launcher declarations
are now checked as ordered assignments plus one command-array surface/scaler,
one derived-copy guard, and one renderer instruction. The manifest contract is
read from Python AST assignments and validator structure rather than unrelated
string literals. Environment facts come only from one generated doctor block,
and Wine/README declarations come from unique keyed lines or phrases inside
their exact Markdown sections.

The four M4.20 attacks now reject: later width, filter, and receipt assignments
and a second kernel row. Adjacent assignment, indirect-write, command/guard,
constant/format, Environment, Wine, and README ambiguity cases also reject.
Focused/full suites pass 36/329 after documentation closure, the checker
still reads exactly nine tracked asset-free inputs, and the 6,177-byte
statement/authorities/game-facing behavior remain unchanged. Exact M4.22 must
independently audit the immutable worker; this does not itself complete M4 or
widen any compatibility, removal, launch, mount, or transaction boundary.

## M4.22 hard-truth disposition and exact M4.23 correction

[[EXP-20260814-081 - Independent M4.21 authority-extraction hard-truth audit]]
returns **REJECT**. Independent reconstruction preserves the canonical
6,177-byte statement, 126 scalar leaves, five anchors, every checked-in
authority value, the four exact M4.20 rejections, 36/329 focused/full tests,
and exactly nine asset-free reads. Direct/generated/scoped Markdown mutations
also reject.

The accepted counterexamples are confined to the machine authority sources.
After the checked initial syntax, standard Bash indexed/compound/array writes
can change output size, command arguments, and the game directory after its
guard. Python global and function-name rebinding can replace the receipt or
validators while leaving the checked AST nodes. Conflicting duplicate tracked-
manifest keys pass when the expected value is last. Separate Bash/Python
semantic checks confirm those effective changes; the checker still returns
success on the disposable authority copies.

Exact M4.23 adds one closed-world correction: compute and require exact
SHA-256 from the already-read bytes of only `scripts/play-pristine.sh`,
`reimplementation/ablpc/manifest.py`, and the three tracked manifests before
retaining current semantic/scoped checks. It may change only checker alignment,
synthetic regressions, and documentation. It may not change the statement,
authority sources or values, general manifest input policy, schema, receipt,
operations, workflows, apply/stage/compose/remove, assets, runtime, M2, mount,
transaction, prose scope, or the exactly-nine-read boundary.

## M4.23 worker result and exact M4.24 audit

[[EXP-20260814-082 - Closed-world machine-authority byte pins]] completes that
exact correction at the worker boundary. The checker pins only the launcher,
manifest implementation, and three tracked manifests to their evidence-listed
SHA-256 values. It hashes each raw byte sequence from the same read already
required for alignment, fails on mismatch before semantic checks, and reuses
the accepted bytes for strict manifest parsing and source-aware inspection.

Five direct pin tests and six exact M4.22 regressions pass. Indexed scalar,
command-array append, post-guard game-directory, Python `globals()` receipt,
validator-name rebind, and conflicting duplicate-manifest-key copies now all
reject by digest. The four predecessor attacks and scoped human-authority
checks survive. Focused/full suites pass 47/340; the canonical statement and
all five authority files remain byte-exact; tracing remains nine unique asset-
free reads with no protected path.

At the worker boundary, exact M4.24 was only the required fresh-context hard-
truth audit of that immutable result. These pins are a compatibility-evidence
contract, not a general manifest allowlist, input policy, schema/operation
expansion, or claim about unsupported hashes, hosts, runtime behavior,
rollback, or transactions.

## M4.24 acceptance and exact M4.25 dry-run boundary

[[EXP-20260814-083 - Independent M4.23 machine-authority-pin hard-truth audit]]
returns `ACCEPT`. Independent reconstruction confirms the canonical 6,177-byte
statement and all five authority hashes; the mapping contains exactly those
five paths and no extras. All six M4.22 and four M4.20 attacks reject, direct
drift and missing-file cases fail 5/5 before recipe semantic alignment, scoped
human-source drift rejects 3/3, and tracing remains nine unique asset-free
reads with one read per pin. Focused/combined/canonical tests pass 47/152/340
and every hygiene gate survives.

This closes only compatibility alignment. M4 remains active because the written
dry-run/report capability is still absent. Exact M4.25 adds only a deterministic
write-free report for one existing manifest: affected paths, input/output
hashes and sizes, authored operations, LEVEL DAT record locators and half-open
byte ranges, or exact whole-file input/output extents. It must reuse existing
validation/preparation, mutate no filesystem, keep the compatibility statement
and general dry-run unsupported boundary intact, and leave apply/stage/compose/
remove, schema, receipt, operations, launch, mount, runtime, and input policy
unchanged.

## M4.25 worker result and exact M4.26 audit

[[EXP-20260814-084 - Deterministic single-manifest dry-run report]] completes
that exact worker boundary. `dry_run_manifest` and the `ablpc-mod dry-run`
command reuse `_prepare_manifest`; no separately weakened validation path or
output root exists. Report schema 1 retains canonical manifest identity and
authored file/edit order, derives hashes from prepared bytes, records LEVEL
section/index/record-offset plus half-open destination spans, and gives opaque
replacement distinct input/output extents.

Nine new focused cases cover all four existing operations under schemas 1/2,
authored order, deterministic repeated stdout, unequal extents, later/input-
hash/record-guard/protected failures, empty failure stdout, and exact complete
filesystem snapshots. Manifest/combined/canonical suites pass 99/161/349.
Receipts and accepted apply/stage/compose/remove behavior remain on their prior
paths. Only the manifest implementation authority pin is refreshed, to
`ce66bd048e505546c002ebe8a1fdc4477822363cce8e4631618dd157a9c3d243`;
exact five-pin membership, other values, nine reads, and statement survive.

Exact M4.26 is only the required fresh-context hard-truth audit. M4.25 does not
authorize composed/N-way dry-run, semantic diff, output simulation, persisted
reports, packaging, rollback, transactions, general launch automation, or a
broader compatibility/input claim.

## M4.26 acceptance and exact M4.27 closure audit

[[EXP-20260814-085 - Independent M4.25 single-manifest dry-run hard-truth audit]]
returns `ACCEPT` for exact worker
`58b01d4c415d45ce98952ef0492fbdc51fe9888d` over direct parent
`7a07f55782bec77e25ac9af1c8aeea4e0b3d244b`. Independent packed-byte
expectations cover schemas 1/2, primary/secondary records, same-span sequential
guards, no-ops, multi-file/multi-edit authored order, and empty/shorter/longer
opaque outputs. Ninety-one assertions across 20 cases pass; broad write traps
observe zero mutation, complete no-follow snapshots remain exact on success
and ten failure families, and retained failure stdout is empty.

Ordinary receipt objects/bytes, apply, stage, compose, and remove remain exact.
Thirty-eight independent compatibility assertions reproduce exactly five pins,
the manifest digest
`ce66bd048e505546c002ebe8a1fdc4477822363cce8e4631618dd157a9c3d243`,
the other four values, pre-semantic failure, same-read reuse, nine unique asset-
free reads, and the exact statement. Focused/combined/canonical tests pass
99/161/349 and every hygiene gate survives.

This accepts only the existing single-manifest report. Exact M4.27 is one
bounded milestone-closure evidence audit: it must map every written M4
capability and exit gate to independently accepted evidence, a current command/
test, user documentation, and exact limitation before M4 may be marked
complete. No implementation, game-byte, runtime, or broader dry-run work is
authorized by that audit.

## M4.27 rejection and exact M4.28 receipt boundary

[[EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit]] maps all nine
required capabilities and five exit gates to evidence, a current command/test,
user documentation, and exact limits. Eight capability rows and four exit-
gate rows survive. M4 closure is rejected for two explicit gaps.

First, the written receipt capability says receipts must be sufficient to
reproduce and remove a mod, while current `remove` requires the original
manifest and this note deliberately tells users to preserve it. The receipt is
deterministic and already records normalized current-operation details, but no
supported loader reconstructs an existing-schema manifest from it. Second,
separate evidence for staging/application, validation, runtime launch, and
sparse removal does not join one tool-created clean-copy lifecycle: staged
trees are complete launch inputs but deliberately non-removable, while sparse
overlays are removable but not complete game roots.

Exact M4.28 selects only the smaller receipt contradiction. It may strictly
load byte-exact ordinary receipts, reconstruct only current schema-1/schema-2
manifests from the uniquely mapped current operation families, and reuse
ordinary preparation/writing/removal for sparse replay and receipt-driven
removal. Receipt bytes, schemas, formats, operations, hashes, guards, paths,
topology checks, and manifest-driven workflows must remain exact. It is not a
receipt migration, embedded-output, staged-tree removal, launcher, package,
backup, rollback, transaction, or M4-completion packet. The clean-copy
lifecycle gate remains open after M4.28.

## M4.28 worker result and exact M4.29 audit

[[EXP-20260814-087 - Strict receipt reconstruction for replay and removal]]
completes the bounded worker implementation. `replay_receipt` and CLI `replay`
load one external ordinary receipt, reconstruct the unique current schema/
format/operation mapping, rerun ordinary manifest validation/preparation, and
require the fully recomputed receipt to match byte-for-byte before creating a
new dedicated sparse output root. `remove_receipt` and CLI `remove-receipt`
perform the same authority reconstruction before entering the shared exact-
tree, output-hash, current-Linux mount, and deletion implementation used by
manifest-driven `remove`.

External receipt acquisition rejects protected/source/output placement,
symlinked ancestors, nonregular or multi-link files, descriptor identity/type
swaps, and metadata/content changes across the no-follow nonblocking read.
Only strict ordinary UTF-8 JSON bytes with exact root/file/edit keys,
integer-not-boolean current schemas/indices, contiguous authored edit indices,
lowercase exact hashes, safe unique paths, and current operation families are
accepted. Duplicate keys, invalid constants, deep recursion, alternate
encodings, and unknown/missing fields fail before source preparation.

Forty-seven new focused cases cover schemas 1/2, all four operations, no-op,
empty/shorter/longer opaque output, composition, malformed/mismatched
authority, nonregular/race inputs, later failure, replay topology, removal
drift, exact snapshots, and CLI behavior. Focused/combined/canonical suites
pass 146/208/396. The manifest pin is
`59c275c5a6d7f539b4664130102035d90ecc6c0d587a09e90688115268e0e240`;
the exact statement, five-pin membership, other four hashes, and nine reads
remain. All three established local families replay/remove twice from
external receipts with prior deterministic receipt/output hashes and unchanged
sources.

This makes the receipt a bounded operational authority under the exact-source
model, not a signature, author/provenance proof, original-manifest recovery,
or universal reorder detector. Post-preflight sequential I/O remains non-
transactional. Staged-tree/source removal and the clean-derived-copy lifecycle
are unchanged. Exact M4.29 is documentation-only independent falsification of
the immutable worker; no M4 completion follows from the worker result.

## M4.29 rejection and exact M4.30 acquisition boundary

[[EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit]]
returns `REJECT` on one exact external-input consistency claim. The current
loader checks each lexical component and resolved placement, then opens the
final receipt with `O_NOFOLLOW` and compares only the final file identity and
metadata. In 2/2 deterministic synthetic repetitions, one already checked
parent changes into a directory link immediately before final `open` and
reaches the same single-link receipt inode below a changed disallowed
location. Final-file checks remain exact, so replay accepts and creates output.
Final-component `O_NOFOLLOW` does not stabilize parent components.

The receipt mapping itself survives independent reconstruction. Two exact
format mappings, 80/80 strict authority variants, 146 focused tests, 208
combined tests, 37 removal/mount/topology cases, 396 canonical tests, six
local cycles, exact five pins, and nine reads pass. Source, output, ordinary
receipt bytes, current schemas/operations, replacement extents, composition,
authenticated removal, mount handling, compatibility, and every retained
manifest workflow remain supported. `KU-051` nevertheless remains open because
the strict external path/placement claim is incomplete; `KU-052` and M4 also
remain open.

Exact M4.30 is the sole successor. It must acquire and validate every parent
component and the final receipt through stable directory/file handles, or the
smallest equivalent component-by-component no-link mechanism; bind component
type/device/inode and placement checks to that acquired chain; reject the exact
parent change before source preparation, output creation, or removal; and
retain exact before/after snapshots plus every green gate above. It may change
only external receipt acquisition, exact synthetic regressions, one resulting
pin if required, and documentation. No receipt/schema/mapping, output/removal/
mount, staged-tree, launcher, asset, runtime, M2, PS1, transaction, or clean-
copy lifecycle change is selected.

## M4.30 worker result and exact M4.31 audit

[[EXP-20260814-089 - Component-stable external receipt acquisition]] completes
the exact correction at the worker boundary. `_open_external_receipt_chain`
retains descriptors for the filesystem root and every lexical parent, opens
each next component relative to that parent without following links, compares
directory type/device/inode across inspection and open, and applies complete
single-link final-file metadata checks before and after reading. Placement is
revalidated, then the entire visible lexical chain is independently reacquired
and must equal the retained chain before receipt parsing.

The exact M4.29 rename/link substitution now rejects for replay and receipt-
driven removal before source preparation or mutation. Different parent inode,
inspection/open replacement, final hard-link or metadata change, and CLI
failure cases also reject with exact snapshots. Seven new cases raise focused/
combined/canonical totals to 154/216/404. All three local families pass two
ordinary apply, external-receipt replay, exact-tree comparison, and removal
cycles with their established hashes and unchanged sources.

Only the manifest implementation pin changes, to
`091a0431c24637fd8e4618bd09b208ac856c3312c3ebe5f1fb6ba7dcdff0f503`.
Receipt/manifest bytes and schemas, four operations, reconstruction, guards,
source/hash/output authority, new-root replay, removal/mount behavior, the
exact statement, five-pin membership, other four pins, and nine reads remain.
This was not an acceptance verdict, filesystem transaction, post-preflight
concurrency guarantee, or clean-derived-copy lifecycle result. Exact M4.31 was
the required documentation-only fresh-context audit; M4, `KU-051`, and
`KU-052` remained open.

## M4.31 rejection and exact M4.32 closure boundary

[[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]]
independently retains the corrected acceptance boundary. The exact M4.29
parent rename/protected-directory-link attacks reject for replay and removal
with complete no-follow source/parent/moved-target/overlay/output snapshots;
28/28 adjacent absolute/relative/deep/component/final/parse/error cases and
three reacquisition changes retain exact accept/refuse and no-mutation results.
The focused/combined/canonical suites pass 154/216/404, all six local cycles
retain their hashes, and the exact statement/five pins/nine reads survive.

The verifier nevertheless returns `REJECT` on one exact descriptor-ownership
claim. `_close_receipt_handle_chain` stops if one `os.close` reports an error,
so it does not attempt the remaining directory closes. First-close injection
reproducibly retains seven descriptors; next-close injection retains six.
This directly contradicts the worker experiment's claim that every acquired
descriptor closes on success and failure, while leaving source/overlay exact
and output absent.

Exact M4.32 is the sole successor. It may change only receipt-chain release and
error propagation, exact synthetic tests, the manifest implementation pin if
required, and documentation. Every owned descriptor must receive one close
attempt despite an earlier close error; primary acquisition/read/reacquisition
errors remain primary, and cleanup-only errors fail deterministically before
parsing or mutation. Receipt/manifest bytes, schemas, operations, mapping,
guards, source/hash/output authority, component acceptance, replay/removal/
mount behavior, statement membership, launcher, staged trees, assets, runtime,
M2, PS1, transactions, and the clean-copy lifecycle remain unchanged. M4,
`KU-051`, and `KU-052` remain open.

## M4.32 worker result and exact M4.33 audit

[[EXP-20260814-091 - Exception-safe receipt-handle-chain closure]] corrects
only the M4.31 cleanup failure. One release helper attempts the owned file and
every reverse directory descriptor exactly once despite earlier `OSError`,
retains the first cleanup error, and never retries. Partial acquisition and
both nested managed chains preserve an existing primary error with secondary
cleanup notes; cleanup-only failure becomes `ManifestError` before parsing.

Seven indexed tests cover first/second/last close positions across reacquired
and acquired chains, partial final-`fstat` failure, errors in both nested
closures, exact close identity/multiplicity, real descriptor deltas, snapshots,
parse exclusion, and CLI silence. Focused/combined/canonical suites pass
161/223/411, and all six local cycles retain prior hashes. The manifest pin is
`f7fd01144b99f4b93cbbb05faa382c53279114bb60b1a71b0793a755279ad111`;
the exact statement, five-pin membership, other four pins, and nine reads
remain unchanged.

This is an exhaustive owned-handle worker boundary, not retry, rollback,
transaction, or post-preflight concurrency protection. Exact M4.33 must audit
the immutable result before `KU-051` can resolve or the separate lifecycle can
be selected. M4 and both unknowns remain open.

## Independent M4.33 closure acceptance and exact M4.34

[[EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit]]
returns `ACCEPT`. The direct parent reproduces +7/+6 retained descriptors.
Twenty-eight fresh worker cases then cover every position across partial
acquisition, cleanup-only errors in both managed chains, and a custom body
error plus errors in both nested closures. Observed file-first/reverse-directory
and reacquired-before-acquired order is exact, every descriptor receives one
attempt, every `/proc/self/fd` delta returns to zero, primary type/message and
ordered cleanup notes survive, and cleanup-only failure precedes parsing and
source preparation. CLI failure is status 2 with empty stdout.

The parent/adjacent acquisition selector passes 15/15, focused/combined/
canonical totals remain 161/223/411, all six exact local cycles retain prior
receipt/output/source hashes, and the compatibility statement/five pins/nine
reads remain exact. `KU-051` is resolved only at this strict current-receipt,
exact-source, component-stable, exhaustive-closure boundary. No retry,
transaction, concurrency, provenance, staged-tree removal, runtime automation,
M2, or PS1 claim follows.

M4 remains active because `KU-052` is open. Exact M4.34 is the audit-only
clean-derived-copy lifecycle feasibility packet. It must build a same-tree
four-verb ledger for current staged, sparse, in-place-force, receipt, launcher-
readiness, and removal surfaces; it may not combine evidence from separate
trees or weaken an accepted safety boundary.

## M4.34 lifecycle rejection and exact M4.35 restoration boundary

[[EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit]] returns
`REJECT` for M4 completion. On one fresh complete synthetic source, `stage`,
sparse `apply`, `apply --force` into a clean full copy, and strict receipt
replay all emit equal ordinary receipts and exact recorded output hashes.
Staged and forced-copy outputs retain unrelated game content and the
executable; below `work/copies/` they reach the launcher's deliberate
synthetic-executable hash rejection. Their supported `remove` attempts fail at
status 2 with empty stdout on exact extra content and leave complete no-follow
snapshots unchanged. Sparse apply and replay remove completely, but contain no
executable or full game tree. The documented `work/mod-builds/` stage path is
also outside the launcher boundary, though `stage` can already target a new
path below `work/copies/`.

The accepted dedicated-sparse removal contract is therefore correct and must
not be relaxed. Its action unlinks recorded outputs; on a complete tree that
would remove required game files, not remove the mod. Exact M4.35 adds one
separate manifest-driven `restore` path for an exact `stage`-produced complete
tree. It must authenticate whole-tree equivalence to the exact source except
for recorded outputs and the ordinary receipt before mutation, then restore
only those destinations from source and remove the receipt/empty `.ablpc`.
Sparse removal, external-receipt behavior, receipt/manifest bytes and schemas,
launcher policy, package/rollback/transaction scope, and game behavior remain
unchanged. M4 and `KU-052` stay open until fresh-context M4.36 accepts the
worker and the joined same-tree lifecycle.

## M4.35 worker result and exact M4.36 audit

[[EXP-20260814-094 - Manifest-driven clean-copy restoration]] adds one distinct
`restore MANIFEST --source-root SOURCE --game-root ROOT` worker path. It
recomputes the ordinary receipt and prepared outputs, inventories complete
source/game trees without following links, requires regular single-link files,
rejects reserved source `.ablpc`, and authenticates every path/type/content
pair except exact recorded outputs and the ordinary receipt. Mount/alias
preflight covers the full expected game tree before any write or unlink.

Success writes only exact clean-source bytes for recorded destinations and
removes receipt/empty `.ablpc`; it does not delete the game root or mutate
source. Twenty-seven focused instances cover schemas 1/2, all four operations,
opaque/multi/composed trees, unrelated and authority drift, nonordinary source/
game paths, CLI behavior, and four private mountpoints. Focused/combined/
canonical totals are 188/250/438. All six sparse local cycles retain prior
hashes. One exact 722-file tree below `work/copies/` passes `stage`, the pinned
launcher dry run, restoration to source content, source preservation, and
cleanup without game execution.

The new manifest pin is
`4707c93e5d57b7d8b833547bb3c5d7e5c0b735ba1c772ceb3e43a5546e2b004d`;
the other four machine pins and nine-read membership remain exact. Existing
sparse deletion, receipts/schemas/operations, launcher behavior, and statement
membership do not change. The statement remains deliberately conservative at
this unverified worker edge. Exact M4.36 must independently audit the full-tree
boundary; M4 and `KU-052` remain open.

## M4.36 rejection and exact M4.37 boundary

[[EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit]]
retains M4.35's ordinary restoration and refusal behavior, five deterministic
stable-read identity traps, eight namespace cases, exact 722-file local
lifecycle, six sparse cycles, exact five pins/nine reads, and 188/250/438
tests. It nevertheless returns `REJECT`: `_regular_tree_inventory` and the
complete-tree comparison key entries only by exact Linux spelling, so a source
and staged game containing both `Case.bin` and `case.bin` restore successfully.

Exact M4.37 may add only case-insensitive uniqueness across complete source and
game file/directory paths before restoration mount traversal or mutation. It
must cover file/file, directory/directory, file/directory, and nested ancestor
collisions with exact snapshots and retain every M4.36 gate. It does not own
general Windows reserved-name policy, manifest/receipt/schema changes, sparse
behavior, mount-policy changes, launcher/statement alignment, assets, runtime,
M2, or PS1. M4 and `KU-052` remain open.

## M4.37 worker result and exact M4.38 audit

[[EXP-20260814-096 - Complete-tree case-insensitive path uniqueness]] closes
the exact admission gap at the worker boundary. `_regular_tree_inventory`
records one `relative.as_posix().casefold()` key for every file and directory
and raises on a second distinct entry. Source inventory and reserved metadata
validation now precede manifest preparation, so a source collision cannot
reach manifest-source content reads or mount planning. The staged-game
inventory applies the same key after the retained mount/alias safety gate and
before stable content reads or restoration mutation.

Eight parameterized cases cover source and staged-game file/file,
directory/directory, file/directory, and nested ancestor collisions. All
refuse with exact source/game snapshots; explicit traps exclude preparation,
content reads, atomic writes, and unlink at their applicable boundaries. The
ordinary `.ablpc` refusal remains unchanged. Focused/combined/canonical totals
are 198/260/448; two uppercase-first directory cases also prove neither
ambiguous branch is descended. The tracked mount/order selector is 6/6, the
exact 722-file/26-directory launcher-dry-run lifecycle passes, and all six
sparse local cycles retain prior hashes. Only the manifest pin changes to
`b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75`;
the statement remains byte-exact and conservative.

This uses the repository's established case-fold model only. It adds no
Windows reserved-device-name or other canonicalization policy, manifest/
receipt change, mount-policy change, sparse behavior, transaction, provenance,
or post-preflight concurrency guarantee. M4 and `KU-052` remain open on exact
fresh-context audit/docs M4.38. Statement alignment is not selected at the
worker edge.

## M4.38 independent acceptance and exact M4.39 alignment

[[EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit]]
returns `ACCEPT` for immutable worker
`8e73a7f5d513bb2534ed16b74ce1027e2d643039` above exact parent
`7180e4a7d41e125307a2b32a3f1f6cb726d20b3d`. A separate no-follow oracle
reproduces parent `Case.bin`/`case.bin` acceptance, then verifies 36 current
source/game collision cases across path types, nesting, both orientations,
and Unicode casefold. Four additional bind-mounted colliding-directory cases
place the independent tree in both lexical positions; every sibling key is
validated before either ambiguous branch is descended. Timing traps and
complete source/game/external snapshots retain the exact source-before-
preparation and game-before-stable-read/mutation boundaries.

All eight M4.36 namespace families pass, including hidden-stack success and
reused IDs `1185/1186/1185`. Five stable-identity swaps, root overlaps,
ordinary type/drift/CLI cases, two mounted character-device cases, the exact
722-file/26-directory launcher-dry-run lifecycle, all six sparse cycles, five
pins, nine reads, and 198/260/448 tests also pass. Unmounted `mknod` remains
environment-denied and is not claimed. No game was executed.

`KU-052` is resolved only for exact-source manifest-driven `stage`, pinned
launcher `--dry-run`, and exact-manifest/source `restore` of the same complete
derived tree on the declared current-x86_64-Linux boundary. M4 is not complete:
v0.1 remains 6,177 bytes at
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`
and still declares restoration unsupported. Only exact M4.39 may publish a
strict v0.2 statement aligned to this accepted boundary while preserving v0.1
and every unsupported deletion/transaction/automation limit.

## M4.39 strict v0.2 statement worker and exact M4.40 audit

[[EXP-20260814-098 - Strict v0.2 restoration compatibility statement]] keeps
historical v0.1 byte-identical at 6,177 bytes/SHA-256 `c3427d44...af0` and
adds canonical 7,677-byte v0.2 at SHA-256 `dacfcab8...ccb2`. The same five
hash anchors, schemas, formats, operations, recipes, machine pins, tested
environment, sparse-removal boundary, and Wine/Gamescope scope remain exact.
Only one `restore` workflow and one evidence-cited current-Linux restoration
boundary are added.

The v0.2 boundary requires an existing-schema manifest plus exact source,
complete regular single-link source/game trees, exact path/type/content except
for recomputed outputs and receipt, project casefold uniqueness, retained
mount/alias preflight, exact output hashes, and exact receipt bytes. It keeps
post-preflight I/O non-transactional. External-receipt full-tree restoration,
whole staged-tree/source deletion, untested platforms/filesystems, provenance,
POSIX metadata equality, backup/rollback/package/transaction, general launch/
runtime automation, general Windows path policy, and concurrency guarantees
remain unsupported.

The checker defaults to v0.2 and still validates exact historical v0.1. It
rejects drift at all 151 v0.2 scalar values plus retained structural,
duplicate, unknown-version, and noncanonical mutations. Each check reads one
statement plus the same eight enumerated tracked asset-free authorities. The
worker recorded 58/266/459; exact M4.40 later corrects the combined collection
to 271. No manifest implementation or pin, manifest/receipt/schema/operation,
behavior, launcher, asset, runtime, M2, or PS1 surface changes. M4.39 is worker-
complete, not independently accepted; exact audit/docs-only M4.40 owns the
final hard-truth and milestone disposition.

## M4.40 rejection and exact M4.41 strictness boundary

[[EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit]]
independently reconstructs v0.1/v0.2 at exact 6,177/7,677 bytes and
`c3427d44...af0`/`dacfcab8...ccb2`, confirms 126/151 scalar leaves, only the
accepted restoration semantic delta, five pins, and exactly nine asset-free
reads for each normal version check. The restoration boundary remains exact
against `EXP-094/097` and manifest pin `b3480761...6d75`; no unsupported
deletion, platform, metadata, transaction, automation, path-policy, or
concurrency claim is weakened.

M4.40 nevertheless returns `REJECT`. The loader accepts attacker-ordered
object fields when those bytes are indented in that order. The default v0.2
path accepts complete v0.1 bytes and the explicit historical path accepts
complete v0.2 bytes, both with status 0. An object/array statement ID escapes
as `TypeError`. All 151 scalar-value attacks and retained authority/scope tests
reject normally; focused/combined/canonical suites pass 58/271/459, proving
the worker's 266 combined count stale.

Only exact M4.41 follows. It may bind selected paths to exact version IDs,
require expected object-key order recursively, normalize malformed IDs to the
ordinary compatibility error path, add exact regressions, and correct counts.
It may not change either statement, a pin/authority, manifest behavior,
launcher, game-facing surface, restoration scope, or unsupported declaration.
M4 remains active and no second successor is selected.

## M4.41 worker correction and exact M4.42 audit boundary

[[EXP-20260814-100 - Version-bound canonical compatibility-statement strictness]]
closes only the independent M4.40 checker failures. The repository-selected
historical and active paths require exact v0.1/v0.2 IDs; every expected JSON
object key sequence is checked recursively; and every non-string ID fails as
`CompatibilityError` before version lookup. Full opposite-version replacement,
top/nested key reorder, list/object/integer ID, and CLI status/no-traceback
regressions all pass.

The exact statements remain 6,177/7,677 bytes at `c3427d44...af0` and
`dacfcab8...ccb2`; all five machine pins, the launcher, manifest authority,
one-statement-plus-eight-authority reads, restoration scope, and unsupported
boundaries remain unchanged. All 151 scalar value and 151 scalar type attacks
reject; focused/combined/canonical suites pass 71/284/472.

This is worker evidence, not milestone acceptance. Exact M4.42 must audit the
immutable correction and reconcile the complete M4.27 capability/exit ledger.
It may change documentation only, and only its clean fresh-context verdict may
mark M4 complete or select one smallest corrective packet.

## M4.42 rejection and exact M4.43 selected-path boundary

[[EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit]]
independently retains both exact statement bytes/hashes, their 19/21 ordered
objects and 126/151 leaves, only the accepted restoration semantic delta, all
five pins, normal one-statement-plus-eight-authority behavior, and the worker's
71/284/472 suites. Accepted M4.33 and M4.38 still close receipt sufficiency and
the exact current-Linux same-tree lifecycle; `KU-051` and `KU-052` do not
reopen.

M4.42 nevertheless returns `REJECT`. In a tracked-only disposable export, the
default active statement pathname was a relative symbolic link to the
historical selected file. Because expected-version selection compares resolved
targets and takes the first match, both selected entries collapse to the
historical path, v0.1 is selected, and the default checker reports valid v0.1
with status 0 and empty stderr. The compatibility publication capability and
exit gate remain open; the ledger stands at eight of nine and four of five.

Only exact M4.43 follows. Determine expected v0.1/v0.2 identity from the
normalized lexical repository pathname before following file content, and
require each selected statement itself to be a regular non-link file. Add both
selected-link directions and normal-path regressions. Preserve statement
bytes, five pins, normal nine reads, arbitrary otherwise-valid unselected paths,
manifest/receipt/restoration behavior, unsupported limits, and every game-
facing boundary. M4 remains active and no second successor is selected.

## M4.43 worker correction and M4.44 audit boundary

[[EXP-20260814-102 - Lexical selected-statement identity and non-link admission]]
uses lexical normalized repository paths for version selection and `lstat`
regular-file admission for selected final entries before content reads. Both
selected link directions refuse through library/CLI with read traps; arbitrary
unselected exact v0.1/v0.2 links retain prior behavior. Exact suites pass
75/288/476; statements, five pins, normal nine reads, authorities, restoration
scope, unsupported declarations, and all game-facing behavior remain exact.
M4.44 is audit/docs-only and owns final milestone disposition.

## M4.44 acceptance and final M4 boundary

[[EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit]]
reproduces the direct parent's active-to-historical selected-link acceptance,
then accepts immutable M4.43. Both selected link directions, dangling links,
directories, FIFOs, and Unix sockets reject before content reads; normal and
dot/dot-dot lexical aliases bind to the required version; arbitrary unselected
exact v0.1/v0.2 regular files and links retain acceptance. Both statements,
their 19/21 recursive object orders and 126/151 scalar leaves, exact semantic
delta, five anchors/pins, and normal one-statement-plus-eight-authority reads
remain exact. Focused/combined/canonical suites pass 75/288/476.

The complete M4.27 ledger, including accepted M4.33 receipt sufficiency and
M4.38 same-tree lifecycle evidence, is now 9/9 required capabilities and 5/5
exit gates. M4 is Complete only for the asset-free, exact-hash, manifest/source-
authenticated current-x86_64-Linux workflow documented by v0.2. Unlisted
hashes, untested systems, N-way composition, general dry-run/launch/runtime
automation, whole staged-tree/source deletion, external-receipt full-tree
restoration, provenance, POSIX metadata equality, backup, rollback, packaging,
transactions, general Windows path policy, and post-preflight concurrency
remain unsupported. No successor milestone is activated by this disposition.

## Second independent post-closure confirmation

[[EXP-20260814-104 - Second independent M4 post-closure verification]] returns
a fresh `ACCEPT` at exact post-closure HEAD. Its independent 663-assertion
matrix confirms normal/alias paths, selected link/nonregular no-read refusals,
cross-version regular and hard-linked content, accepted same-version hard
links, parent-link behavior at the explicit final-entry boundary, arbitrary
unselected exact regular/links, recursive statement order/leaves, strict JSON,
five pins, and nine ordered reads. Exact suites remain 75/288/476.

This second verdict does not add a general parent-filesystem policy or post-
`lstat` race/concurrency protection and does not change any M4 capability,
exit-gate evidence boundary, statement, authority, behavior, unsupported item,
or milestone activation.
