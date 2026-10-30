---
type: experiment
id: EXP-20260814-110
date: 2026-08-14
question: Does the second M6 correction satisfy every retained release, smoke, installed lifecycle, and repository exit gate at its declared local-state-trust boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact clean tracked audit; ignored asset-free build, install, smoke, and consistency roots
environment_version: kernel 7.0.11-200.fc44.x86_64; x86_64; Python 3.14.6; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact clean audited HEAD 64d8ac1678eb34a72ea1b91833a3118ee963a40b; implementation commits 46fa294 and 7d8594e; tracked files read-only; no game execution
artifacts:
  - work/releases/james-m6-final-qa.CglA1B/build-a/ablpc-toolkit-v1.0.0.tar
  - work/releases/james-m6-final-qa.CglA1B/build-b/ablpc-toolkit-v1.0.0.tar
  - work/releases/james-m6-final-qa.CglA1B/install
  - work/releases/james-m6-final-qa.CglA1B/smoke-report.json
addresses: []
file_offsets: []
result: accept-m6-at-declared-boundary
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/release
  - milestone/m6
  - audit/hard-truth
---

# EXP-20260814-110 - Independent M6 state-locked lifecycle acceptance audit

## Verdict

**ACCEPT.** James independently accepts exact clean audited HEAD `64d8ac1`.
All four M6 exit gates are supported at the declared asset-free Fedora/Wine
launcher-readiness and unsigned local-state-trust boundary. M6 is Complete.

## Release identity

Two independent builds are byte-identical:

| Property | Result |
|---|---|
| archive size | 399,360 bytes |
| archive SHA-256 | `68d3d31a84b01bafe6ca3711991aad7e058f95c5e72e7cc3b28799d533cb060b` |
| source-tree SHA-256 | `2644263f44558a0874d74d65f82b6f7001270d5d19b16a41b55f9a3b6b69bef9` |
| inventory | 37 unique sorted regular members |
| modes | 32 mode-0644 and 5 mode-0755 |
| strict verification | pass |

All 13 retained noncanonical or inconsistent archive variants reject.

## Installed lifecycle and inventory

- All 55 required lifecycle cases reject with 55/55 complete pre/post
  snapshots unchanged.
- All 10 installed inventory, manifest, topology, and mode cases reject with
  10/10 complete snapshots unchanged.
- Every installed version, including inactive retained versions, remains bound
  to canonical schema-2 state archive/manifest/tree locks.
- All four installed entry points exit 0 with cache variables unset and with
  `PYTHONDONTWRITEBYTECODE=0` plus `PYTHONPYCACHEPREFIX` inside the selected
  release. Every snapshot matches and zero cache or `.pyc` entry appears.

Canonical `state.json` remains the declared local unsigned trust root.
Coordinated rewriting of that trust root and installed content, concurrent
replacement after inspection, and unlisted filesystems are not claimed.

## Exact smoke and repository gates

The exact Fedora smoke run passes all 21 `LEVEL*.DAT` files, all three schema
1/1/2 workflows, and all 747 source/stage entries with exact restoration. The
4,277-byte report is SHA-256
`c1fb69037def8c4093c8ede266b5ba858799705a7bd7eeb2807fa27a11b498dc`.

| Gate | Result |
|---|---|
| canonical tests | 509/509 pass |
| M4 compatibility | five anchors valid |
| Vault | 312 notes, 0 errors, 0 warnings |
| tracked protected-content audit | 0 violations |
| diff / staged diff / tracked tree | clean |

Tracked files remained read-only throughout the audit. Generated evidence is
ignored under `work/releases/james-m6-final-qa.CglA1B/`.

## Result

`ACCEPT`: close M6 without widening any explicit unsupported boundary.
