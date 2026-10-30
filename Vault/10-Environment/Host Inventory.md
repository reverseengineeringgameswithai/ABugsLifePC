---
type: environment
id: ENV-HOST-20260811
status: confirmed
created: 2026-08-11
updated: 2026-10-02
evidence:
  - direct command output captured during bootstrap
tags:
  - environment/host
---

# Host Inventory

Inventory collected read-only on 2026-08-11 in `America/Toronto` before project changes.

## Operating system and kernel

```text
Fedora Linux 44 (Workstation Edition)
VERSION_ID=44
Linux fedora 7.0.11-200.fc44.x86_64
Architecture: x86_64
```

## CPU and memory

```text
AMD Ryzen 7 9800X3D 8-Core Processor
8 cores / 16 threads
AMD-V (SVM): present on all 16 logical CPUs
RAM: 123 GiB total, 75 GiB available at inventory time
Swap: 8.0 GiB total, effectively full at inventory time
```

## Storage

```text
/home filesystem: 1.9 TiB total, 1.5 TiB used, 349 GiB available, 82% used
```

## Virtualization

```text
/dev/kvm: present and accessible
modules: kvm_amd, kvm
QEMU hardware virtualization: PASS
vhost-net: PASS
/dev/net/tun: PASS
IOMMU: PASS
cgroup devices controller: WARN
secure guest support (SEV/TDX): WARN / unavailable
virtqemud.socket: active and enabled
qemu:///system: reachable
libvirt default network: active, autostart, persistent
```

The warnings are not blockers for the planned local Windows debugging VM.

## Command inventory before changes

| Command | Initial state |
|---|---|
| `git` | `/usr/bin/git` |
| `python3`, `pip` | `/usr/bin/python3`, `/usr/bin/pip` |
| `java` | `/usr/bin/java` |
| `wine` | `/usr/bin/wine` |
| `virsh` | `/usr/bin/virsh` |
| `virt-manager`, `virt-install` | not found |
| `qemu-system-x86_64` | `/usr/bin/qemu-system-x86_64` |
| `ghidraRun` | not found |
| `radare2`, `rabin2` | installed |
| `gdb` | installed |
| `strace` | not found |
| `clang`, `gcc`, `cmake`, `ninja` | installed |
| `rg` | Codex-bundled executable only |
| `jq` | installed |
| `fzf` | not found |
| `7z` | installed |
| `cabextract` | not found |
| `flatpak` | installed |
| `obsidian` | not found |
| `codex`, `claude` | user-local installations |

## Observed versions before changes

```text
OpenJDK Runtime 25.0.3 (javac was absent)
wine-11.0 (Staging)
libvirt/virsh 12.0.0
QEMU 10.2.2
Git 2.54.0
Python 3.14.6
radare2 5.9.8
Codex CLI 0.147.0
Claude Code 2.1.228
```

## Fedora 44 repository resolution

Package names were queried against only the official `fedora` and `updates` repositories. Valid names include:

```text
virt-manager 5.1.0-4.fc44
virt-install 5.1.0-4.fc44
strace 7.1-1.fc44
mingw32-binutils 2.46.0-1.fc44
mingw64-binutils 2.46.0-1.fc44
ripgrep 15.2.0-1.fc44
fzf 0.74.2-1.fc44
cabextract 1.11-10.fc44
java-25-openjdk-devel 25.0.4.0.7-1.1.fc44
```

`java-21-openjdk-devel`, `ghidra`, `86box`, `pcem`, and `obsidian` had no Fedora 44 package match. The installed `wget2-wget` already supplies `wget`.

## Post-bootstrap additions

- Gamescope `3.16.25-1.fc44` was installed from the Fedora package repository on 2026-08-12 and tested in [[EXP-20260812-007 - Gamescope hardware presentation baseline]].
- Later additions are not itemized here. The `make doctor` block in
  [[Environment Status]] (2026-09-26) records them, among them rr 5.9.0,
  apitrace, Ghidra 12.1.2 with PyGhidra 3.1.0, project-local 86Box 6.0 and
  Obsidian 1.13.6. `rpm -q` on 2026-10-02 shows `rr` and `apitrace` as Fedora
  packages; `strace`, `virt-manager`, `fzf` and `cabextract` are still absent.

## Proposed sudo transaction

The Fedora-only transaction was previewed with `dnf --assumeno`: 17 installs, 2 MinGW filesystem upgrades, 15 MiB download, and 66 MiB added. Sudo required interactive authorization, so it was not performed. No third-party RPM repository was added.
