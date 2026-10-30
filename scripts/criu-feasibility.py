#!/usr/bin/env python3
"""Report whether CRIU could checkpoint the Wine game process tree here.

The in-process checkpoint in ``game-memory.py snapshot``/``restore`` is a
same-process, memory-only state restore.  A checkpoint that survives a crash or
a deliberate close needs CRIU (or a full VM snapshot).  CRIU on a Wine +
Gamescope + GPU + ntsync process is exactly the class of environment that
already defeated ``rr`` (KU-028), so this tool does the read-only feasibility
survey and prints the blockers, rather than attempting a dump that needs root
and would likely fail mid-way.

It never dumps, freezes, or signals anything.  It inspects tool availability,
kernel configuration, this process's capabilities, and — if given a live game
PID — the open files and mappings that CRIU is known to struggle with (GPU DRM
fds, the ntsync device, X11/Wayland sockets, PulseAudio connections).

Actually dumping is a separate, authorized, root action and is out of scope
here (CAP-011).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402


TOOL = "criu-feasibility"
TOOL_VERSION = "1.0.0"

# Open-file targets CRIU is known to be unable to checkpoint transparently.
HARD_FD_MARKERS = {
    "/dev/dri/": "GPU DRM device (rendering state CRIU cannot capture)",
    "/dev/ntsync": "Wine ntsync device (the same driver that blocks rr, KU-028)",
    "anon_inode:[ntsync]": "Wine ntsync anonymous inode",
    "anon_inode:ntsync": "Wine ntsync anonymous inode",
    "socket:": "an open socket (X11/Wayland/PulseAudio connections need "
               "--tcp-established or external handling)",
    "/dev/snd/": "ALSA/sound device",
    "anon_inode:[io_uring]": "io_uring instance",
}


def _fail(reason: str, detail: str = "") -> int:
    print(json.dumps(sl.refusal(TOOL, reason, detail)))
    return ev.EXIT_REFUSAL


def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def check_tooling() -> dict:
    criu = shutil.which("criu")
    version = ""
    if criu:
        try:
            out = subprocess.run([criu, "--version"], capture_output=True,
                                 text=True, timeout=10)
            version = (out.stdout or out.stderr).strip().splitlines()[0] if (
                out.stdout or out.stderr) else ""
        except (OSError, subprocess.TimeoutExpired):
            version = "unknown"
    return {"criu_path": criu, "criu_version": version, "installed": bool(criu)}


def check_kernel() -> dict:
    config = _read(f"/boot/config-{os.uname().release}")
    flags = {}
    for name in ("CONFIG_CHECKPOINT_RESTORE", "CONFIG_MEM_SOFT_DIRTY",
                 "CONFIG_NAMESPACES", "CONFIG_PID_NS"):
        flags[name] = f"{name}=y" in config if config else None
    return {"config_readable": bool(config), "flags": flags}


def check_capabilities() -> dict:
    """CRIU dump of another user's-equivalent tree typically needs
    CAP_CHECKPOINT_RESTORE and CAP_SYS_ADMIN, or root."""

    status = _read("/proc/self/status")
    cap_eff = ""
    for line in status.splitlines():
        if line.startswith("CapEff:"):
            cap_eff = line.split()[1]
            break
    eff = int(cap_eff, 16) if cap_eff else 0
    CAP_SYS_ADMIN = 21
    CAP_CHECKPOINT_RESTORE = 40
    return {
        "euid": os.geteuid(),
        "is_root": os.geteuid() == 0,
        "cap_eff": cap_eff,
        "has_cap_sys_admin": bool(eff & (1 << CAP_SYS_ADMIN)),
        "has_cap_checkpoint_restore": bool(eff & (1 << CAP_CHECKPOINT_RESTORE)),
    }


def survey_process(pid: int) -> dict:
    """Enumerate the open files and mapping paths CRIU struggles with."""

    fd_dir = Path(f"/proc/{pid}/fd")
    hard: list[dict] = []
    fd_count = 0
    try:
        entries = list(fd_dir.iterdir())
    except OSError as exc:
        raise sl.SessionError("fd_unreadable", f"{fd_dir}: {exc}") from exc
    for entry in entries:
        fd_count += 1
        try:
            target = os.readlink(entry)
        except OSError:
            continue
        for marker, why in HARD_FD_MARKERS.items():
            if marker in target:
                hard.append({"fd": entry.name, "target": target, "issue": why})
                break

    mapped_paths: set[str] = set()
    for mapping in sl.read_maps(pid):
        if mapping.path.startswith("/dev/dri") or "ntsync" in mapping.path:
            mapped_paths.add(mapping.path)

    return {
        "pid": pid,
        "open_fd_count": fd_count,
        "hard_to_checkpoint_fds": hard,
        "hard_fd_count": len(hard),
        "device_mappings": sorted(mapped_paths),
    }


def cmd_check(args: argparse.Namespace) -> int:
    tooling = check_tooling()
    kernel = check_kernel()
    caps = check_capabilities()
    process: dict | None = None
    if args.pid is not None:
        # Prove identity read-only before inspecting the process.
        ev.ownership_proof(
            args.pid,
            expected_sha256=args.expected_sha,
            loader_re=args.loader_re,
            cwd_prefix=args.cwd_prefix,
        )
        process = survey_process(args.pid)

    blockers: list[str] = []
    if not tooling["installed"]:
        blockers.append("criu is not installed")
    if kernel["flags"].get("CONFIG_CHECKPOINT_RESTORE") is False:
        blockers.append("kernel lacks CONFIG_CHECKPOINT_RESTORE")
    if not (caps["is_root"] or caps["has_cap_checkpoint_restore"]):
        blockers.append(
            "no CAP_CHECKPOINT_RESTORE and not root: a dump needs authorized "
            "privilege"
        )
    if process:
        if process["hard_fd_count"]:
            issues = sorted({fd["issue"] for fd in process["hard_to_checkpoint_fds"]})
            blockers.extend(issues)
        if process["device_mappings"]:
            blockers.append(
                "GPU/ntsync device mappings present: CRIU cannot restore GPU "
                "state, and ntsync is the driver that already blocks rr"
            )

    verdict = "blocked" if blockers else (
        "prerequisites present; a live dump is still unproven and authorized"
        if process else
        "prerequisites present; supply --pid and run an authorized dump to know"
    )
    result = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "check",
        "note": (
            "This is a read-only feasibility survey. It does not dump, freeze, "
            "or signal. Actually running a CRIU dump/restore is a separate "
            "root-privileged, authorized action (CAP-011). The in-process "
            "same-session alternative is game-memory.py snapshot/restore."
        ),
        "tooling": tooling,
        "kernel": kernel,
        "capabilities": caps,
        "process": process,
        "blockers": blockers,
        "feasible_without_more_authority": not blockers,
        "verdict": verdict,
    }
    print(json.dumps(result, indent=2))
    return ev.EXIT_OK if not blockers else ev.EXIT_TOOL_NEGATIVE


def capabilities() -> dict:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verbs": ["check"],
        "actions": "read-only survey only; never dumps, freezes, or signals",
        "authority": "a real CRIU dump/restore needs root and explicit user "
                     "authorization; this tool does neither",
        "alternative": "game-memory.py snapshot/restore for same-session state",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="criu-feasibility.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check", help="survey CRIU checkpoint feasibility")
    check.add_argument("--pid", type=int, default=None,
                       help="optional live game PID to inspect for hard fds")
    check.add_argument("--expected-sha", default=None)
    check.add_argument("--loader-re", default=ev.DEFAULT_LOADER_RE)
    check.add_argument("--cwd-prefix", default=None)
    check.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2))
        return ev.EXIT_OK
    if not getattr(args, "command", None):
        parser.print_usage(sys.stderr)
        return ev.EXIT_USAGE
    try:
        return args.func(args)
    except ev.OwnershipError as exc:
        return _fail(exc.reason, exc.detail)
    except sl.SessionError as exc:
        return _fail(exc.reason, exc.detail)


if __name__ == "__main__":
    sys.exit(main())
