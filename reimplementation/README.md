# ABLPC modding tools

This directory contains independently written tools for the PC game. It does not
contain game files. The current vertical slice parses a confirmed prefix of
`LEVEL*.DAT`, reports candidate spatial records and structurally bounded positive
payload-target blocks, applies guarded field edits, and emits either a sparse
overlay or a complete staged work tree.

M2 adds a read-only, lossless inspector for the first-level PC `.ANM` layout
consumed at executable address `0x00444B70`. It reports metadata only and does
not expose resource editing.

M4 schema 2 adds one opaque `replace-whole-file` operation. It copies bytes
between two exact-hash files already present in the user's work copy; it does
not parse the replacement format or include either file in the repository.
M4 adds independently accepted composition of exactly two existing schema-1/
schema-2 manifests against one exact source tree. Canonical input identity
determines whole-input grouping per destination, while each input's authored
edit sequence is preserved. Combined existing-schema revalidation remains
fail-closed for cross-input guard dependencies. M4.9 adds removal of dedicated
ordinary sparse overlays after exact manifest/source, receipt, output-hash,
and complete-tree validation. Independent M4.10 rejects its complete-preflight
claim for a pre-existing bind-mounted overlay directory. M4.11 adds a worker-
complete Linux mountinfo preflight guard for the exact root and descendants.
Independent M4.12 rejects acceptance because a proper-parent mount alias is
omitted. M4.13 adds the exact traversed-ancestry correction at the worker
boundary, but independent M4.14 rejects its ordinary-filesystem claim for a
hidden lower stacked alias. M4.15 now excludes only same-path parent-stack-
covered lower records and passes the exact visible ordinary-top case at the
worker boundary. Independent M4.16 preserves that correction but rejects
acceptance because a newly created uncovered alias can reuse a numerically
lower freed mount ID than its still-mounted source and bypass the current
numeric-ID ordering. M4.17 now replaces only that age decision with verified
current-Linux later-mount order and passes the exact reused-ID regression at
the worker boundary. Exact independent M4.18 accepts that correction after a
separate namespace reproduction and adversarial fail-closed audit. M4.19 is
worker-complete on one strict, asset-free versioned compatibility statement,
but independent M4.20 rejects its substring-only authority alignment. M4.21's
source-aware declaration correction is worker-complete, but independent M4.22
rejects residual post-declaration shell/Python and duplicate-manifest-key
bypasses. M4.23 pins exactly those five machine authority files from their
same existing reads and rejects all six observed families. Independent M4.24
accepts that correction after the full adversarial, read-boundary, and retained-
gate audit. M4.25 adds a deterministic write-free report for one existing
manifest, and exact M4.26 independently accepts that boundary. M4.27's 14-row
evidence ledger rejects milestone closure: receipts remain insufficient
without the original manifest, and no accepted evidence joins one tool-created
clean-copy install through validation, launch, and removal. M4.28 is now
worker-complete on strict current-receipt sparse replay/removal. Exact M4.29
preserves its receipt mapping and retained behavior but rejects acceptance at
one parent-component consistency boundary. M4.30 closes that acceptance bypass
at the worker boundary, but exact M4.31 rejects its descriptor-release claim:
one close error skips the remaining chain. M4.32 corrects exception-safe
exhaustive receipt-chain closure, and exact M4.33 independently accepts it
after 28/28 fresh indexed close cases. `KU-051` is resolved only at that strict
boundary. M4.34 then rejects milestone closure after a same-tree four-route
audit: complete outputs are not dedicated sparse-removal targets, while
removable sparse outputs are not launch inputs. M4.35 adds a distinct
authenticated full-tree restore path; independent M4.36 retains its ordinary
behavior but rejects Windows-case-equivalent complete-tree paths. M4.37 now
supplies the bounded case-fold uniqueness correction, and independent M4.38
accepts it after stronger collision/order/mount attacks. `KU-052` resolves only
for the demonstrated manifest-driven current-Linux lifecycle. M4.39 publishes
the strict v0.2 statement at the worker boundary. Independent M4.40 retains its
bytes, restoration truth, five pins, nine reads, and 58/271/459 suites but
rejects selected-path cross-version acceptance, reordered object fields, and a
malformed-ID error leak. M4.41 closes only those strictness failures at the
worker boundary with 71/284/472 suites. Exact M4.42 retains those results but
rejects selected-path identity because the default active pathname can link to
the historical selected file and validate v0.1. M4.43 closes that exact worker
boundary with 75/288/476 suites. Exact independent M4.44 accepts that
correction and closes the final ledger at 9/9 required capabilities and 5/5
exit gates. M4 is Complete only at the documented asset-free, current-x86_64-
Linux, explicit-unsupported boundary; that closure itself activated no
successor milestone.

`EXP-20260814-104` independently rechecks that completed state with a separate
663-assertion matrix, including same/opposite-version hard links and parent-
directory links at the explicit selected-final-entry boundary. It returns a
second `ACCEPT`, keeps 75/288/476 suites green, and does not add parent-
filesystem or post-`lstat` concurrency guarantees or activate a successor.

## M6 asset-free release layer

M6 packages the independently authored tools, exact recipes, compatibility
metadata, and bounded documentation as `ablpc-toolkit-v1.0.0`. Its strict
contract is `reimplementation/release/m6-v1.0.0.json`; detailed build,
verification, install, rollback, smoke, and compatibility instructions are in
`reimplementation/M6-RELEASE.md`.

The deterministic tar builder accepts only its clean tracked allowlist and
fixes member order, epoch, ownership, mode, and canonical inventory. The
installer verifies every archived path/type/size/mode/hash before creating a
new immutable version. Toolkit migration preserves the prior selected version,
and rollback verifies and atomically reselects it without touching game data.
All packaged Python entry points suppress bytecode generation, preserving the
complete installed inventory during ordinary use. Lifecycle commands admit
`state.json`, `releases/`, and selected version entries without following the
final entry and reject links or incompatible types before state mutation.
State, manifests, and package files must be canonical single-link regular
files; implicit package directories and their modes must be exact. Every
installed version is revalidated, including inactive retained versions, and
missing state cannot silently adopt a populated release directory.
Canonical install-state schema 2 stores the verified archive, manifest, and
source-tree hashes for every retained version; installed content and its local
manifest therefore cannot be rebaselined without contradicting the state lock.

The primary Linux smoke matrix validates the supported executable/data hashes,
the M4 v0.2 statement, and all 21 `LEVEL*.DAT` files. It stages, launcher-dry-
runs, and exactly restores Training, Level 01, and schema-2 character cases on
disposable complete work copies. This does not automate gameplay or establish
a rendered result. Renderer, menu, level, and gameplay input remain manual;
Windows 98 and every unlisted environment remain untested.

## Exact M4 compatibility statements

`reimplementation/compatibility/m4-v0.1.json` is preserved byte-for-byte as the
historical M4 v0.1 statement. v0.1 remains immutable historical evidence.
`reimplementation/compatibility/m4-v0.2.json` is the active machine-checkable
statement. v0.2 adds only the independently accepted manifest/source-authenticated
complete-tree restoration boundary on current x86_64 Linux.
Both versions name the same five demonstrated hash anchors, exact schema/
format/operation surface, tested tool host, current-Linux topology
prerequisites, and tested Wine/Gamescope presentation. Their `demonstrated`,
`fail-closed`, and `unsupported` labels are evidence boundaries; they are not
claims about unlisted hashes or untested systems.

Validate the statement without reading any game file:

```bash
./scripts/check-m4-compatibility.py
# or: make m4-compatibility
```

The checker defaults to v0.2 and accepts v0.1 as its separate exact historical
contract. M4.41 binds regular files at those two selected paths to their
declared versions, requires canonical strict JSON with the declared recursive
object-key order, rejects
unknown or changed fields, and cross-checks the five hashes against the hash-
checked launcher and three tracked manifests. It also checks the recorded
Fedora/Python/Wine/Gamescope
versions and the launcher/renderer guidance in tracked text. Each invocation
reads exactly one selected statement plus the same eight enumerated tracked
asset-free authorities: three manifests, the launcher, manifest implementation,
Environment Status, Wine baseline, and this README. `make check` runs this
asset-free consistency gate automatically. M4.20 confirms those current
sources agree and the checker reads no game files, but rejects the drift claim:
an expected assignment followed by an effective competing assignment can pass
while the checked substring remains. M4.21 now extracts the already-claimed
shell, Python, generated-row, and scoped documentation declarations
and rejects that exact attack class. Independent M4.22 nevertheless finds
effective post-declaration Bash/Python changes and conflicting duplicate
tracked-manifest keys that still pass. M4.23 now requires exact same-read
SHA-256 for the launcher, manifest implementation, and three manifests before
semantic alignment. All six observed bypass families reject; the statement,
authority behavior, and exactly-nine-read boundary remain unchanged.
Independent M4.24 accepts this exact alignment boundary. The pins remain a
compatibility evidence contract, not a general input allowlist. M4.25
refreshed only the manifest implementation pin for its worker. M4.28 refreshed
that same pin to
`59c275c5a6d7f539b4664130102035d90ecc6c0d587a09e90688115268e0e240`;
M4.30 refreshes it again to
`091a0431c24637fd8e4618bd09b208ac856c3312c3ebe5f1fb6ba7dcdff0f503`;
M4.32 refreshes it to
`f7fd01144b99f4b93cbbb05faa382c53279114bb60b1a71b0793a755279ad111`
and M4.35 refreshes it to
`4707c93e5d57b7d8b833547bb3c5d7e5c0b735ba1c772ceb3e43a5546e2b004d`.
M4.37 refreshes only that pin again to
`b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75`.
Neither broadens the statement; the receipt workflow leaves general dry-
run automation unsupported. Exact M4.26 independently accepts the prior
report. Exact M4.29 rejects only M4.28's parent-component acquisition claim;
the exact statement, five pins, and nine reads remain green.
M4.27's evidence ledger in `EXP-20260814-086` supports eight of nine
capabilities and four of five exit gates but rejects closure. M4.28 addresses
only receipt sufficiency at the worker boundary; M4.30 completes its stable
component-acquisition correction only at the worker boundary. Exact M4.31
retains that behavior but rejects exception-unsafe descriptor closure. Exact
M4.32 corrects only that boundary, and independent M4.33 accepts it after the
parent +7/+6 reproduction, 28/28 indexed cases, and every retained gate.
M4.34 independently rejects the separate clean-derived-copy lifecycle gate.
M4.35's bounded restore command survives its ordinary audit, but independent
M4.36 rejects case-colliding complete-tree admission. M4.37 supplies only that
worker correction; independent M4.38 accepts it. M4.39 publishes the strict
v0.2 alignment without changing the historical v0.1 bytes, five pins, nine-
read boundary, or any game-facing behavior.

Independent M4.40 preserves those facts but rejects complete checker
strictness. A canonically indented object with reordered fields is accepted;
the default v0.2 selected path accepts the complete valid v0.1 contract and
the explicit historical path accepts complete v0.2; an object/array statement
ID can escape as `TypeError`. Exact compatibility/manifest/LEVEL collection is
271, correcting the worker's stale 266 count. Only M4.41 may correct selected-
version binding, recursive object-key order, and malformed-ID error handling;
neither statement, the five pins, nor any behavior is selected to change.

M4.41 now binds the repository-selected historical/active paths to exact
v0.1/v0.2 IDs, requires the expected key order in every JSON object, and
normalizes all non-string IDs into the ordinary compatibility error path.
Complete cross-version swaps, top/nested reordered objects, and list/object/
integer IDs reject; both normal versions retain exactly nine reads. All 151
v0.2 scalar value and 151 scalar type attacks reject, and exact suites pass
71/284/472. Both statement bytes, five pins, authorities, scopes, unsupported
declarations, and game-facing behavior remain unchanged. Exact independent
M4.42 owned final acceptance and milestone disposition.

M4.42 returns `REJECT` on one selected-path identity case. When the canonical
active pathname is a relative symbolic link to the canonical historical
statement, both selected paths resolve to the historical target; first-match
selection assigns v0.1 and the default checker reports valid v0.1 with status
0. Regular-file cross-version replacements, recursive key order, typed IDs,
canonical bytes, five pins, and normal nine-read behavior remain retained.
Exact M4.43 may only derive selected identity from the lexical repository path
before following content, require both selected statements themselves to be
regular non-link files, and add link/normal-path regressions. Statement bytes,
authorities, arbitrary otherwise-valid unselected paths, unsupported limits,
and game-facing behavior remain unchanged.

M4.43 now selects v0.1/v0.2 from normalized lexical repository paths and
requires each selected final entry to be a regular non-link before content
reads. Both selected link directions refuse through library and CLI contracts;
arbitrary unselected exact v0.1/v0.2 links retain prior behavior. Normal checks
retain nine reads and exact suites pass 75/288/476. Exact M4.44 independently
accepts this boundary after selected nonregular/read-timing, lexical-alias,
unselected-path, exact-contract, and authority attacks. The compatibility row
closes without broadening arbitrary-path or filesystem policy.

The demonstrated v0.2 restoration authority is one existing-schema manifest
plus its exact source root. It applies only to a complete stage-produced tree
whose source and game inventories contain directories and regular single-link
files, are unique under the repository's relative-path `casefold()` model, and
match path/type/content except for the exact recomputed outputs and ordinary
receipt. The accepted mount/alias preflight remains mandatory and fails closed
when current-Linux topology cannot be trusted. Restoration writes only exact
source bytes to recorded destinations and removes receipt metadata after full
deterministic preflight; later I/O is non-transactional.

External-receipt full-tree restoration, whole staged-tree or source deletion,
provenance, POSIX metadata equality, backup, rollback, packaging, transactions,
general launch/runtime automation, and post-preflight concurrency guarantees
remain unsupported. Untested platforms/filesystems and general Windows path
policy beyond the established casefold uniqueness rule also remain unsupported.

Apply and stage retain their existing exact-hash manifest behavior. `remove`
is demonstrated only for receipt-validated dedicated sparse `apply` overlays
on the declared current x86_64 Linux environment, with readable and internally
consistent `/proc/self/mountinfo`, `listmount(2)`, and `statmount(2)` results.
Topology enumeration or cross-check failure is fail-closed. Removal remains
non-transactional after preflight and is not supported for staged trees or
source restoration.

M4.34's exact four-route ledger explains that last limitation. A complete
`stage` tree or full clean copy modified with `apply --force` retains the
executable and can be placed below `work/copies/`, but `remove` correctly
rejects its unrelated game files before mutation. An ordinary `apply` or
receipt replay tree removes exactly, but contains no executable or complete
game content. Do not combine those different trees into one lifecycle claim or
use sparse removal on a full tree. Exact M4.35 adds a distinct manifest/source-
authenticated restore path at the worker boundary.

The tested Wine/Gamescope scope is the unchanged executable under Wine 11.0
(Staging), Gamescope 3.16.25-1.fc44.x86_64, a 640x480 game surface, `fit`
scaling, and the default `nearest` filter. Hardware selection remains manual:
press Down, then confirm. Accept the Direct3D path only when the complete new
log contains all four markers:

- `Native software render mode is FALSE`
- `RenderMode set to Direct3d render mode`
- `Screen mode 640x480x16 selected`
- `Starting Direct3D renderer`

Reject a run containing `INITSOFTRENDER`. This scope does not establish other
Wine, Windows, kernel, architecture, filesystem, or period-hardware behavior.

## Restore one exact complete staged copy

> **Audit status:** M4.36 rejected Windows-case-equivalent complete-tree
> admission; M4.37 now supplies only that correction in `EXP-20260814-096`.
> Independent exact M4.38 accepts the correction in `EXP-20260814-097`.
> `KU-052` resolves only at the demonstrated current-Linux lifecycle. M4.39
> aligns strict v0.2 while preserving historical v0.1. Exact M4.40 retains the
> restoration boundary but rejects checker strictness; M4.41 closes that exact
> regular-file worker boundary. Exact M4.42 rejects selected-path link identity
> and M4.43 closes that worker boundary. Independent M4.44 accepts it and marks
> M4 Complete only at the documented current-Linux, asset-free boundary.

Create the complete modded tree directly below the launcher's existing
`work/copies/` boundary, validate launcher readiness without running the game,
and later restore the same tree:

```bash
./scripts/ablpc-mod stage \
  mods/chars-flick-all-from-chars3-flickd-all.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --game-root work/copies/chars-flick-all/PC/BUGS

./scripts/play-pristine.sh --dry-run \
  --game-dir work/copies/chars-flick-all/PC/BUGS

./scripts/ablpc-mod restore \
  mods/chars-flick-all-from-chars3-flickd-all.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --game-root work/copies/chars-flick-all/PC/BUGS
```

`restore` recomputes the ordinary manifest preparation and receipt. Before
writing, it requires both trees to contain only directories and regular
single-link files; the source may not contain `.ablpc`; and every game path,
type, and file byte must equal source except the recorded outputs and ordinary
receipt. Those outputs and receipt must match their recomputed hashes/bytes.
On the declared Linux boundary, every expected game path also receives the
accepted mount/alias preflight.

Every source and staged-game file/directory path must also be unique under the
repository's case-folded Windows-path model. Distinct paths such as
`Case.bin` and `case.bin` fail before content reads or restoration mutation.
This is not a broader Windows reserved-device-name or path-canonicalization
policy.

Success restores only recorded destinations from source, removes
`.ablpc/receipt.json` and the now-empty `.ablpc`, preserves the source, and
leaves the complete game tree content-equivalent to source. It does not prove
POSIX permission/time metadata equality or provenance. It is non-transactional
after deterministic preflight and is not external-receipt restoration,
staged-tree deletion, source deletion, backup, rollback, package, or launch
automation. Existing `remove` and `remove-receipt` remain dedicated sparse-
tree deletion and must not be used on a full game tree.

Run the test suite and inspect a work-copy file:

```bash
make check
./scripts/ablpc-mod inspect work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL07/LEVEL1.DAT
./scripts/ablpc-mod inspect \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL07/LEVEL1.DAT \
  --payload-targets primary --json
./scripts/ablpc-mod scan work/copies/BUGS_PC-full-disc/PC/BUGS/CD
./scripts/ablpc-mod scan-payload-targets \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD --json
./scripts/ablpc-mod inspect-anm \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/PLANTS/PLANT04.ANM --json
./scripts/ablpc-mod scan-anm \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/PLANTS --json
```

The `.ANM` inspector checks the 8-byte header, signed first-level count,
file-relative offset table, first nonzero referenced header, and the exact
signed-word list read by `0x00444B70`. It preserves the complete source bytes,
rejects out-of-file reads/offsets, and leaves every unsupported field unknown.
See `Vault/40-Implementation/PC ANM inspector.md`.

Build the example as a complete, ignored game tree:

```bash
./scripts/ablpc-mod stage mods/training-central-flower-cluster-candidate-far.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --game-root work/mod-builds/training-flower-cluster/PC/BUGS
```

Map `work/mod-builds/training-flower-cluster` as a temporary Wine drive
and launch from that drive's `PC/BUGS` directory. The original game faulted in
the downstream loader when run through a direct absolute `Z:` path, even with an
unmodified control file; see `EXP-20260812-006`.

`stage` refuses an existing destination so it cannot silently overwrite a prior
experiment. `apply` builds a sparse overlay by default and requires `--force` to
replace an existing output file. Both commands validate the input SHA-256, reject
unsafe paths, and refuse roots containing `originals` or `media`.

For schema 2 whole-file replacements, both the destination and replacement
source hashes are checked before any output is written. Source and destination
must be distinct safe relative POSIX paths, and a replacement source may not
also be a manifest destination. A sparse overlay contains only the replaced
destination and `.ablpc/receipt.json`; a staged tree retains the source path
unchanged and changes only the destination. The receipt records the input,
replacement, and output hashes.

M4.3 now preflights the deterministic path/type topology of every manifest
destination and `.ablpc/receipt.json` before sparse output, and preflights the
topology that `stage` will copy for those planned writes. Symlinked or non-
directory ancestors and symlinked/non-regular destinations fail before output;
`--force` permits only existing regular files. Independent M4.4 accepts this
correction at that exact boundary (`EXP-20260814-063`). It is not a transaction
or rollback system: unexpected permission, storage, unrelated copy/I/O, or
concurrent-race failures can still leave partial output. Prefer a new output
path and inspect the receipt before use.

## Dry-run one manifest

M4.25 adds a write-free report for exactly one existing schema-1 or schema-2
manifest. It runs the same exact-hash preparation and edit guards used by
ordinary application, but creates no output directory or receipt:

```bash
./scripts/ablpc-mod dry-run \
  mods/training-primary-record-124-target-111e4.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS
```

The deterministic JSON identifies the canonical manifest and lists files and
edits in authored order. Every file includes its format, input/output SHA-256,
and input/output byte size. LEVEL DAT edits include section, record index,
record file offset, and an exact half-open `start`/`end` destination range.
Whole-file replacement instead reports distinct half-open input and output
extents, which may have different sizes.

The command prints no success JSON if any file, input/replacement hash, format,
record guard, operation, or protected source fails. It does not simulate an
overlay, persist its report, compose or order multiple manifests, create a
receipt, or change apply/stage/compose/remove. M4.25 is worker-complete in
`EXP-20260814-084`; independent `EXP-20260814-085` accepts the exact boundary
after direct byte reconstruction, broad write traps, complete no-follow
snapshots, retained ordinary receipt/workflow checks, exact five-pin/nine-read
compatibility, and 99/161/349 tests. General dry-run remains unsupported.

## Compose exactly two manifests

> **Independent audit status:** M4.8 `EXP-20260814-067` accepts the M4.7
> authored-sequence correction at the exact canonical two-input boundary.

`compose` validates both manifests independently against the same source tree,
then writes one deterministic existing-schema manifest to stdout. Save it and
use the ordinary accepted `apply` or `stage` path:

```bash
./scripts/ablpc-mod compose \
  mods/training-primary-record-124-target-111e4.json \
  mods/training-primary-record-125-field-0c-zero.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  > work/mod-builds/training-124-target-plus-125-field.json

./scripts/ablpc-mod apply \
  work/mod-builds/training-124-target-plus-125-field.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --output-root work/mod-builds/training-124-target-plus-125-field-overlay
```

Only the existing byte-located operations participate. Candidate-center edits
claim 12 bytes, field-`0x0C` edits claim 2 bytes, payload-target edits claim the
exact 4-byte target field, and an opaque replacement claims its entire
destination. Same-file entries merge only when their exact path, input hash,
and format agree and every cross-manifest byte span is disjoint. Any opaque
replacement sharing a destination conflicts, even if both replacements name
the same bytes. A replacement source may not become a destination through the
combined manifest.

CLI argument order does not affect successful output or conflict output. A
conflict exits with status 2, leaves stdout empty, and writes one compact JSON
object to stderr. That asset-free report contains canonical input manifest
names/digests, the normalized Windows destination, the conflict kind, and the
exact half-open overlap when one exists. The combined manifest uses schema 2
iff either input uses schema 2. Files are sorted by normalized Windows path.
Within a shared destination, canonical input identity determines the two-input
interleaving and each input file entry retains its authored edit-index order.
The name derives from the two validated canonical input digests.

This command accepts exactly two manifests. It does not reconcile semantic
intent, order N inputs, perform a dry run, remove a mod, change receipts, or
establish resource-format compatibility. The emitted manifest contains no game
bytes, but applying or staging it creates user-owned game-byte output that must
remain untracked and undistributed.

## Remove an exact sparse overlay

> **Audit status:** M4.10 `EXP-20260814-069` rejects M4.9 acceptance. M4.11
> `EXP-20260814-070` rejects exact root/descendant plan mountpoints at the
> worker boundary, but M4.12 `EXP-20260814-071` rejects acceptance because a
> proper parent traversed to reach the overlay root can be a mount alias.
> M4.13 `EXP-20260814-072` rejects that exact uncovered proper-parent alias at
> the worker boundary. Independent M4.14 `EXP-20260814-073` preserves that
> refusal but finds that a hidden lower alias covered by a distinct ordinary
> top filesystem still falsely taints their shared pathname. M4.15
> `EXP-20260814-074` closes that exact worker reproduction through retained
> same-path parent stacking. Independent M4.16 `EXP-20260814-075` rejects
> acceptance because Linux mount-ID reuse can place a newer uncovered alias
> below its source numerically and the classifier then omits it. M4.17
> `EXP-20260814-076` now uses cross-checked current-Linux later-mount order and
> rejects that exact reused-ID case at the worker boundary. M4.18
> `EXP-20260814-077` independently accepts the current-Linux correction after
> ABI/kernel review, adversarial injection, and a separate ID-reuse namespace
> reproduction. M4.19's strict asset-free compatibility statement/checker is
> worker-complete in `EXP-20260814-078`; independent `EXP-20260814-079`
> rejects substring-only authority alignment. M4.21's exact source-aware
> correction is worker-complete in `EXP-20260814-080`, but independent
> `EXP-20260814-081` rejects its residual executable-authority bypasses and
> activates only the five-file same-read pin correction M4.23.
> `EXP-20260814-082` completes that correction and independent
> `EXP-20260814-083` accepts its exact boundary. M4.25's bounded dry-run report
> is worker-complete in `EXP-20260814-084`, and independent
> `EXP-20260814-085` accepts it. `EXP-20260814-086` then rejects milestone
> closure on receipt sufficiency and the unjoined clean-copy lifecycle. Exact
> M4.28 is worker-complete on strict current-receipt replay/removal. Exact
> M4.29 rejects its parent-component consistency claim. M4.30 is worker-
> complete on component-stable acquisition, but exact M4.31 rejects skipped
> descriptor closes after one close error. M4.32 corrects exhaustive one-
> attempt cleanup; exact M4.33 independently accepts it. M4.34 rejects the
> same-tree lifecycle at the full-tree restoration join. M4.35 supplies the
> restore path; exact M4.36 rejects case-colliding complete trees, M4.37
> supplies the correction, and independent M4.38 accepts it. Only M4.39 strict
> v0.2 statement alignment is active.

M4.28 adds a bounded receipt-only sparse workflow. First preserve an ordinary
receipt outside both the source and overlay roots. It must be the exact
single-link regular UTF-8 JSON file emitted by the current tool:

```bash
cp work/mod-builds/chars-flick-all-overlay/.ablpc/receipt.json \
  work/mod-builds/chars-flick-all-receipt.json

./scripts/ablpc-mod replay \
  work/mod-builds/chars-flick-all-receipt.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --output-root work/mod-builds/chars-flick-all-replayed

./scripts/ablpc-mod remove-receipt \
  work/mod-builds/chars-flick-all-receipt.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --overlay-root work/mod-builds/chars-flick-all-replayed
```

`replay` requires a new output root. The loader rejects symlinked ancestors,
nonregular or multi-link inputs, descriptor identity/type/content changes,
protected or in-root placement, duplicate/unknown/missing fields, nonordinary
encoding, unsafe paths, noncontiguous indices, and non-lowercase hashes. It
reconstructs only the current schemas and four operation families, reruns
ordinary source/hash/layout/guard preparation, and requires the fully
recomputed receipt to match byte-for-byte before creating output.

M4.29 identifies one exact limitation in that strict input claim: final-file
`O_NOFOLLOW` does not stabilize already checked parents. M4.30 now retains
directory descriptors from the filesystem root through every lexical parent,
opens each next component relative to the retained parent without following
links, checks type/device/inode and complete final-file metadata, revalidates
placement, and requires an equal second whole-chain acquisition before parsing.
The exact rename/link bypass and adjacent changes reject in the worker and in
independent M4.31. M4.31 nevertheless finds that one close error skips every
remaining descriptor in the chain, retaining seven or six descriptors in the
exact injections. M4.32 now attempts every owned descriptor once, preserves an
existing primary error, and turns cleanup-only error into deterministic failure
before parsing. Exact M4.33 independently accepts that boundary after 28/28
fresh indexed partial/nested cases, zero real descriptor deltas, exact primary
errors, 161/223/411 tests, six local cycles, five pins, and nine reads.
`KU-051` is resolved. M4.34 rejects M4 completion at the full-tree restoration
join; M4.35 supplies the worker path, M4.36 rejects its admission of distinct
Windows-case-equivalent complete-tree paths, and M4.37 supplies the bounded
correction. Independent M4.38 accepts it and resolves `KU-052` only for the
demonstrated current-Linux lifecycle. M4.39 supplies strict v0.2 while
preserving v0.1; exact M4.40 rejects only compatibility checker strictness,
M4.41 closes its regular-file cases, exact M4.42 rejects selected-path link
identity, M4.43 closes that worker boundary, and exact M4.44 independently
accepts the final 9/9-capability, 5/5-exit-gate ledger at the explicit bounded
scope. M4 is Complete and this statement creates no broader M4 claim; M6's
asset-free package/smoke/install layer is documented separately above.

`remove-receipt` performs the same reconstruction and recomputation, then uses
the exact tree, file hash, link/type, and current-Linux mount preflight below.
It preserves the external receipt and source and removes only the authenticated
dedicated sparse tree. The receipt is an operational authority under this
exact-source model, not a signature, provenance proof, recovery of original
manifest text/composed inputs, or universal reorder detector. Post-preflight
I/O remains non-transactional. M4.30 changes only the parent-component
acquisition boundary above and does not claim post-preflight concurrency.

Use the same manifest and exact source tree that produced an ordinary sparse
overlay:

```bash
./scripts/ablpc-mod remove \
  mods/chars-flick-all-from-chars3-flickd-all.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --overlay-root work/mod-builds/chars-flick-all-overlay
```

`remove` recomputes all outputs and the unchanged ordinary receipt from that
manifest/source pair. Before deleting anything it requires:

- `.ablpc/receipt.json` to be strict JSON and byte-identical to the ordinary
  receipt encoding recomputed by the current tool;
- every recorded output and the receipt to be single-link regular files below
  non-symlink directory ancestors;
- every output SHA-256 to match the recomputed result; and
- the complete overlay tree to contain exactly the recorded outputs, receipt,
  and their necessary directories; and
- on Linux, readable trustworthy `/proc/self/mountinfo` showing that the
  overlay root, every necessary directory, every recorded output, and the
  receipt are not mountpoints, and that no proper overlay-root ancestor is a
  newer visible alias of a filesystem root already visible at an older path;
  lower same-path records covered through the mount parent stack are ignored.

On success it prints the authenticated receipt, deletes only the recorded
sparse output files and receipt, prunes their empty directories, and removes
the empty overlay root. It never deletes or restores a source-tree path.
Changed/missing files, source drift, malformed or mismatched receipts, symlinks,
FIFOs, hard links, extra content, protected roots, and a staged full tree fail
before deletion. This manifest-driven command remains available and unchanged;
M4.28 adds the separate strict `remove-receipt` path above without weakening
it or changing receipt bytes.

M4.11 reads Linux mountinfo before traversing or deleting overlay content and
fails closed if the table is missing, malformed, empty, or names any exact
deletion-plan path as a mountpoint. Private namespace tests cover bind-mounted
overlay root, intermediate directory, output, and receipt with complete
snapshots unchanged. Independent M4.12 preserves that exact-path behavior but
rejects the complete claim: the check does not include a mount alias at a
proper parent traversed to reach the overlay root. M4.13 now implements that
exact correction: the reproduced alias refuses with all snapshots unchanged,
while ordinary root, `/home`, `/tmp`, and same-path filesystem ancestry remains
usable in the retained cases. Independent M4.14 nevertheless rejects the
complete classification claim: if a lower alias at that parent pathname is
covered by a distinct ordinary top filesystem, the hidden lower record still
causes false refusal of the visible ordinary overlay. Exact M4.15 is limited to
excluding that covered lower record while retaining the uncovered alias and
every exact-path refusal. It now filters a lower record only when another
retained mountinfo entry names it as `parent_id` at the same mountpoint; both
candidate and source alias comparison use only the resulting visible records.
The exact lower-bind/upper-`tmpfs` overlay removes completely with its source
and hidden target unchanged, while all five prior mount cases still refuse.
Independent M4.16 preserves those results but falsifies the complete alias
claim: after a disposable lower-ID mount is released, a newer bind alias can
reuse that lower ID while its source stays mounted at a higher ID. The current
numeric mount-ID comparison omits that uncovered alias, so authenticated
removal can succeed through it and change the independent mounted target.
Exact M4.17 is limited to correcting that classifier defect. Removal remains
intentionally Linux-specific. It now enumerates unique mount IDs in explicit
later-first order with `listmount(2)`, maps them to mountinfo old ID, parent,
and device through `statmount(2)`, and fails closed if either view is malformed,
incomplete, inconsistent, or changes during preflight. The reused-lower-ID
alias refuses unchanged while covered ordinary-top removal still succeeds.
Independent M4.18 accepts this exact current-x86_64-Linux boundary after all
seven namespace cases, fail-closed sequence/mapping/table attacks, retained
ordinary/M4/M1/local gates, and complete no-follow snapshot checks pass. A
broader platform compatibility claim remains unsupported; M4.19 may publish
only a versioned statement of the exact supported hashes and tested scope.

This is not a staged-tree remover, backup/trash/package manager, source
restoration mechanism, or general rollback transaction. As with the accepted
M4.3 boundary, unexpected permission, storage, I/O, or concurrent-race changes
after deterministic preflight can still fail after an earlier filesystem
operation. Use it only on dedicated ordinary overlays created by this tool.

The example changes only the first candidate-center components at offsets
`0x0E60`, `0x0E74`, and `0x0E88` in the known Training DAT. A controlled Wine
A/B confirms that the three-record edit removes the central foreground flower
cluster. A single-record follow-up shows that records 124, 125, and 126 control
three distinct visible plant elements in the matched starting camera; later
static and runtime evidence establishes upstream visibility selection rather
than render translation. See `EXP-20260812-008` and `EXP-20260812-011`.

The two payload-target example manifests stage reciprocal pointer-only edits for
training primary records 124 and 125. The manifest path is intentionally limited
to the statically verified PC `0x49` dispatch and to positive-count target blocks.
Both candidates pass the matched Direct3D runtime experiment and substitute
placement-local visible content; see `EXP-20260812-010`.

The `set-scene-record-field-0c` operation remains offset-named and requires an
expected signed value. `EXP-20260812-012` demonstrates its positive visibility-
bound behavior for one Training record; negative-value semantics remain
unknown and must not be generalized.

## M1 support boundary

The tool intentionally exposes only three operations:

| Operation | Required guard | Scope |
|---|---|---|
| `set-scene-record-position` | exact file SHA, section/index | three signed candidate-center dwords; the historical name does not mean confirmed render position |
| `set-scene-record-field-0c` | exact file SHA plus expected signed value | the selected signed word; only positive visibility-bound behavior is evidenced |
| `set-scene-record-payload-target-offset` | exact file SHA, masked dispatch `0x49`, expected old target, valid positive old/new blocks | one payload target dword |

`inspect --payload-targets` reports only records in the supported PC class
`(flags & 0xBFEF) == 0x49`. Other dispatches and the negative-count target
layout are deliberately outside this command. The manifest loader rejects
unknown root/operation fields and duplicate file paths as well as unsafe paths,
wrong hashes, unsupported formats, and out-of-range values. The durable audit
matrix is `Vault/40-Implementation/M1 Tool Support Matrix.md`.

## Author and verify a no-game-bytes recipe

Start with a derived work copy owned by the researcher; never point the tool at
`originals/` or `media/`. Inspect the exact file and supported target class:

```bash
sha256sum work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT
./scripts/ablpc-mod inspect \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT \
  --records primary --payload-targets primary --json
```

Copy an existing manifest under `mods/` and change only evidence-backed fields.
The manifest's source hash and expected old value/target are part of the safety
contract. Build a sparse overlay first:

```bash
./scripts/ablpc-mod apply mods/level01-primary-record-261-target-3459c.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --output-root work/mod-builds/level01-record-261-overlay
jq . work/mod-builds/level01-record-261-overlay/.ablpc/receipt.json
```

For an original-executable test, build a complete ignored tree at a new path:

```bash
./scripts/ablpc-mod stage mods/level01-primary-record-261-target-3459c.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --game-root work/mod-builds/level01-record-261/PC/BUGS
```

Map the parent as a temporary Wine drive and launch from its `PC/BUGS`
directory. At the initial selector, press Down once and confirm hardware
acceleration. Accept runtime evidence only when `bugs.log` contains both
`Native software render mode is FALSE`, `RenderMode set to Direct3d render
mode`, `Screen mode 640x480x16 selected`, and `Starting Direct3D renderer`,
and does not contain `INITSOFTRENDER`.

Distribute the manifest, the independently authored tool, and (optionally) the
small receipt. Do not distribute the overlay or staged tree: both contain game
bytes. The Level 01 example is an acceptance/locality recipe whose edit is not
visible at the tested starting camera (`EXP-20260812-013`); the reciprocal
Training rebinds are the demonstrated visible substitutions
(`EXP-20260812-010`).

## Exact user-owned whole-file replacement

`mods/chars-flick-all-from-chars3-flickd-all.json` encodes only the exact
replacement demonstrated in `EXP-20260812-033`:

- destination `CD/CHARS/FLICK.ALL`, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- replacement source `CD/CHARS3/FLICKD.ALL`, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

Both files must already exist in a derived work copy owned by the user. Build
and inspect a sparse overlay without modifying that work copy:

```bash
./scripts/ablpc-mod apply \
  mods/chars-flick-all-from-chars3-flickd-all.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --output-root work/mod-builds/chars-flick-all-overlay
jq . work/mod-builds/chars-flick-all-overlay/.ablpc/receipt.json
```

Or create a complete new staged tree:

```bash
./scripts/ablpc-mod stage \
  mods/chars-flick-all-from-chars3-flickd-all.json \
  --source-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --game-root work/mod-builds/chars-flick-all/PC/BUGS
```

This is an exact-pair recipe, not a general `.ALL` compatibility claim or
editor. Do not distribute either output: the overlay and staged tree contain
user-owned game bytes. Distribute only the manifest, tool, documentation, and
optionally the receipt.

## Exact Level03 type-1 row discriminator

`scripts/make-level03-type1-row6-x-plus-128` applies one reversible,
hash-locked experiment recipe to the retail `CD/LEVEL03/LEVEL.DAT` under
`work/`:

```bash
./scripts/make-level03-type1-row6-x-plus-128 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL03/LEVEL.DAT \
  work/mod-builds/m3-level03-type1-row6-x-plus-128/LEVEL.DAT
```

The source must be SHA-256
`bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.
The recipe changes row 6 X from `15678` to `15806` at file offset
`0x4A4`, changes no other physical byte, preserves file size, reparses, and
proves an exact inverse. The expected output SHA-256 is
`4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12`.

This is a PC runtime discriminator for the candidate selector at
`0x00432930`, not a general type-1 editor and not evidence that the table is
a set of in-world checkpoint objects. Game-bearing output remains under
`work/` and must not be distributed.
