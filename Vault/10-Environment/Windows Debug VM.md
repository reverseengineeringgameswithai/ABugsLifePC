---
type: environment
id: ENV-WINVM-DEBUG
status: blocked
updated: 2026-08-11
tags:
  - environment/windows-vm
---

# Windows Debug VM

## Intent

A modern Windows KVM/libvirt guest may be used for x32dbg/x64dbg, Process Monitor, Process Explorer, ProcDump, a hex editor, and a hash utility.

## Host readiness

KVM acceleration, `virtqemud.socket`, `qemu:///system`, and the libvirt default NAT network were observed working. `virt-manager` and `virt-install` require the documented sudo-authorized Fedora transaction.

## Planned controls

- Start from a clean snapshot.
- Prefer networking disabled; use host-only networking when file transfer or a local debugger link is required.
- Never expose debugger or agent-control services externally.
- Use controlled file transfer and hash transferred artifacts.
- Record guest Windows build, tool versions, snapshot identity, and relevant configuration per run.

## Blocked dependencies

User-authorized Windows installation media and a valid license are absent. Windows debugging utilities are intentionally not downloaded yet.
