# ABLPC toolkit v1.0.0

This is an asset-free, Wine/Linux-scoped toolkit release. It contains Python
source, shell launchers, guarded JSON recipes, compatibility metadata, and
documentation. It contains no executable, game file, disc image, ROM, Windows
media, memory dump, or virtual disk.

The exact machine-readable release contract is
`reimplementation/release/m6-v1.0.0.json`. It supports only executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`,
manifest schemas 1 and 2, and the exact data hashes named there.

## Build and verify

The builder refuses untracked, staged, or dirty package sources. It writes a
deterministic uncompressed tar with fixed member order, epoch, owner, group,
mode, path, and canonical byte inventory.

```bash
./scripts/ablpc-release build --output-dir work/releases/a
./scripts/ablpc-release verify work/releases/a/ablpc-toolkit-v1.0.0.tar
```

Build twice from the same clean tracked tree and compare the reported archive
SHA-256 to establish byte reproducibility.

## Install, migrate, and roll back

Installation verifies every archive path, type, size, mode, SHA-256, release
identity, and exact allowlist before extracting. Each version is immutable
under `INSTALL_ROOT/releases/`; an atomic canonical `state.json` selects the
current version. Installing a newer version retains the prior selection in the
rollback history. Existing version directories are never overwritten. Every
packaged Python entry point suppresses bytecode generation, so ordinary tool
use preserves the complete installed inventory. Lifecycle operations inspect
`state.json`, `releases/`, and the selected version as lexical final entries;
links, dangling links, and incompatible entry types reject before selection
changes. State, manifests, and package files must be canonical single-link
regular files. Package directory topology and modes must be exact, every
installed version is revalidated even when inactive, and absent state is
accepted for installation only with an absent or empty release directory.
Canonical state schema 2 records the verified archive, release-manifest, and
source-tree SHA-256 values for every installed version. Verification
reconstructs the canonical archive from installed files and requires all three
locks, so editing content and recomputing its in-tree manifest does not create
a new accepted baseline. Earlier incomplete state schemas fail closed.

```bash
./scripts/ablpc-release install \
  work/releases/a/ablpc-toolkit-v1.0.0.tar \
  --install-root work/toolkit-install
./scripts/ablpc-release current --install-root work/toolkit-install
./scripts/ablpc-release rollback --install-root work/toolkit-install
```

Rollback verifies the complete prior installed inventory, then atomically
changes only `state.json`. It does not delete either toolkit version and never
reads or changes game files. Manifest schemas 1 and 2 need no content
migration; other schemas fail closed.

These checks establish the declared non-link final-entry boundary on the named
primary filesystem. They do not claim protection against concurrent
replacement after inspection or behavior on unlisted filesystems.

## Primary Linux smoke matrix

The full smoke command checks the active M4 v0.2 compatibility statement, the
known executable and selected data hashes, and all 21 PC `LEVEL*.DAT` files.
It then creates disposable complete staged copies for Training, Level 01, and
the schema-2 Training character recipe. Each copy passes the hash-checking
Wine/Gamescope launcher dry-run and is restored byte-for-byte through the
manifest/source-authenticated M4 path. The original work copy is re-inventoried
afterward and all disposable stage trees are removed.

```bash
./scripts/m6-smoke \
  --game-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --prefix work/wine/baseline \
  --report work/m6-smoke-report.json
```

This automated matrix establishes clean-copy preparation, launcher readiness,
and rollback. It does not execute or automate gameplay. Hardware acceleration
still requires Down then confirm at the selector. A live run is acceptable
only when its complete new log includes all four documented Direct3D markers
and contains no `INITSOFTRENDER`.

## Compatibility limits

The primary tested configuration is x86_64 Fedora Linux, Python 3.14.6, Wine
11.0 Staging, Gamescope 3.16.25, WineD3D's Direct3D path, a 640x480x16 game
surface, and `fit`/`nearest` presentation. The smoke command checks the exact
host package/version rows before running.

The release does not automate renderer, menu, level, or gameplay input. Its
audio arm validates construction of the private PipeWire/Pulse null-sink
launch command without playing or measuring audio. WineD3D/driver/filtering,
other displays, other input and audio stacks, other Wine/Gamescope/kernel/
filesystem versions, non-x86_64 hosts, Windows 98, and modern Windows remain
untested unless a separate controlled experiment says otherwise.
