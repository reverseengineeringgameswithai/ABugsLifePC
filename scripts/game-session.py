#!/usr/bin/env python3
"""Launch, address, and close one owned PC game session.

Implements as a command the recipe that previously existed only as prose in
``Vault/10-Environment/PC autonomous game control.md``: detached launch,
owned-display and owned-window discovery, the fail-closed six-marker renderer
gate, carousel navigation confirmed from memory rather than a screenshot, and
closure that signals only the identities recorded at launch.

Every session writes ``dynamic/wine/RUN-SESSION-<stamp>/session.json``: the
ownership ledger the Agent Operating Manual requires but nothing previously
produced.  It records the process group, the game PID with its start ticks,
the display and window, the private audio sink, and the inventory of runtime
processes that already existed before the launch -- so a later audit can tell
this session's residue from someone else's.

Acceptance rules preserved from the Vault:

* Renderer acceptance comes from the log's six positive markers with no
  software marker.  A screenshot, a key receipt, or an early selection summary
  is not proof, and a failed gate rejects the arm.
* Carousel position is not the internal level number; a navigation is
  confirmed by reading the internal level global.
* Cleanup may target only recorded identities, and start ticks are compared so
  a recycled PID is never signalled.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Any, Callable

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402


TOOL = "game-session"
TOOL_VERSION = "1.0.0"

DEFAULT_LAUNCHER = "scripts/play-pristine.sh"
DEFAULT_GAME_DIR = "work/copies/BUGS_PC-full-disc/PC/BUGS"
DEFAULT_PREFIX = "work/wine/baseline"

# The chooser times out to the software default after 60000 ms
# (cmp dword [0x7f1170], 0xea60), so the whole boot-to-confirm sequence has a
# hard real-time deadline.
CHOOSER_TIMEOUT_MS = 60_000
CHOOSER_SAFETY_MARGIN_MS = 10_000


class UsageError(ValueError):
    """Raised for a malformed command line."""


def _fail(reason: str, detail: str = "") -> int:
    print(json.dumps(sl.refusal(TOOL, reason, detail)))
    return ev.EXIT_REFUSAL


def _emit(payload: dict, ok: bool = True) -> int:
    print(json.dumps(payload, indent=2))
    return ev.EXIT_OK if ok else ev.EXIT_TOOL_NEGATIVE


def _root(args: argparse.Namespace) -> Path:
    return ev.repo_root()


# --------------------------------------------------------------------------
# Audit and preflight
# --------------------------------------------------------------------------


def _audit_names(args: argparse.Namespace) -> tuple[str, ...]:
    override = getattr(args, "audit_name", None)
    return tuple(override) if override else sl.RUNTIME_PROCESS_NAMES


def _open_session_groups(root: Path | None = None) -> set[int]:
    groups: set[int] = set()
    for manifest in sl.iter_sessions(root=root):
        if manifest.state == "open" and manifest.process_group is not None:
            groups.add(manifest.process_group)
    return groups


def cmd_audit(args: argparse.Namespace) -> int:
    records = sl.process_records()
    owned = _open_session_groups()
    audit = sl.audit_runtime(records, owned_groups=owned, names=_audit_names(args))
    sinks = sl.list_null_sinks(pactl=args.pactl)
    recorded_sinks = {
        entry.get("sink_name")
        for manifest in sl.iter_sessions()
        if manifest.state == "open"
        for entry in manifest.owned_sinks
    }
    payload = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "audit",
        "processes": audit,
        "null_sinks": [
            {**sink, "owned": sink.get("sink_name") in recorded_sinks} for sink in sinks
        ],
        "open_sessions": sorted(
            manifest.session_id
            for manifest in sl.iter_sessions()
            if manifest.state == "open"
        ),
        "clean": audit["unattributed_count"] == 0,
    }
    return _emit(payload, ok=payload["clean"])


def cmd_preflight(args: argparse.Namespace) -> int:
    records = sl.process_records()
    owned = _open_session_groups()
    audit = sl.audit_runtime(records, owned_groups=owned, names=_audit_names(args))
    payload = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "preflight",
        "audit_names": list(_audit_names(args)),
        "processes": audit,
        "clean": audit["unattributed_count"] == 0,
        "policy": "Vault/00-System/Agent Operating Manual.md#Runtime instance lifecycle",
    }
    return _emit(payload, ok=payload["clean"])


def cmd_list(args: argparse.Namespace) -> int:
    rows = []
    for manifest in sl.iter_sessions():
        rows.append({
            "session_id": manifest.session_id,
            "state": manifest.state,
            "created_at": manifest.created_at,
            "process_group": manifest.process_group,
            "game_pid": manifest.game_pid,
            "display": manifest.display,
            "live": sl.session_is_live(manifest),
            "renderer_accepted": (manifest.renderer_gate or {}).get("accepted"),
            "level": manifest.level,
        })
    return _emit({
        "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "list",
        "sessions": rows, "count": len(rows),
    })


# --------------------------------------------------------------------------
# Launch
# --------------------------------------------------------------------------


def _launcher_argv(args: argparse.Namespace, root: Path) -> list[str]:
    launcher = Path(args.launcher)
    if not launcher.is_absolute():
        launcher = root / launcher
    argv = [str(launcher)]
    if args.research:
        argv.append("--research")
    if args.windowed:
        argv.append("--windowed")
    if args.mute:
        argv.append("--mute")
    if args.auto_hardware:
        argv.append("--auto-hardware")
    if args.game_dir:
        argv.extend(["--game-dir", str(args.game_dir)])
    if args.prefix:
        argv.extend(["--prefix", str(args.prefix)])
    if args.output:
        argv.extend(["--output", args.output])
    argv.extend(args.launcher_arg or [])
    return argv


def cmd_launch(args: argparse.Namespace) -> int:
    root = _root(args)
    game_dir = Path(args.game_dir) if args.game_dir else root / DEFAULT_GAME_DIR
    game_dir = game_dir if game_dir.is_absolute() else root / game_dir
    argv = _launcher_argv(args, root)
    log_path = game_dir / sl.GAME_LOG_BASENAME

    if args.dry_run:
        return _emit({
            "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "launch",
            "dry_run": True, "launcher_command": argv,
            "game_dir": str(game_dir), "log_path": str(log_path),
            "auto_hardware": bool(args.auto_hardware),
            "renderer_plan": (
                "auto-hardware build boots to Direct3D with no chooser input"
                if args.auto_hardware else
                "send Down then Return with held presses, then require the six "
                "positive log markers"
            ),
        })

    # Preflight: refuse to add a session on top of unattributed runtime
    # processes unless the caller explicitly records them.
    records = sl.process_records()
    owned_groups = _open_session_groups()
    pre_audit = sl.audit_runtime(records, owned_groups=owned_groups,
                                 names=_audit_names(args))
    pre_audit["audit_names"] = list(_audit_names(args))
    if pre_audit["unattributed_count"] and not args.allow_existing:
        return _fail(
            "unattributed_runtime_processes",
            f"{pre_audit['unattributed_count']} runtime processes are not owned by "
            "an open session; close them, or pass --allow-existing to record them "
            "as pre-existing in this session's ledger",
        )
    sinks_before = sl.list_null_sinks(pactl=args.pactl)

    session_id = sl.new_session_id()
    run_dir = sl.session_dir(session_id)
    run_dir.mkdir(parents=True, exist_ok=False)
    stdout_path = run_dir / "launcher-stdout.txt"
    stderr_path = run_dir / "launcher-stderr.txt"

    manifest = sl.SessionManifest(
        session_id=session_id,
        created_at=ev.now().isoformat(),
        launcher_command=argv,
        game_dir=str(game_dir),
        prefix=str(args.prefix or (root / DEFAULT_PREFIX)),
        log_path=str(log_path),
        auto_hardware=bool(args.auto_hardware),
        owned_processes=[],
        notes=[],
    )
    manifest.notes.append(
        f"pre-existing runtime processes at launch: {pre_audit['unattributed_count']}"
    )
    (run_dir / "preflight.json").write_text(
        json.dumps(pre_audit, indent=2) + "\n", encoding="utf-8"
    )

    started = time.monotonic()
    with open(stdout_path, "wb") as out, open(stderr_path, "wb") as err:
        process = subprocess.Popen(
            argv, cwd=str(root), stdout=out, stderr=err,
            stdin=subprocess.DEVNULL, start_new_session=True,
        )
    manifest.launcher_pid = process.pid
    try:
        manifest.process_group = os.getpgid(process.pid)
    except OSError:
        manifest.process_group = process.pid
    manifest.save()

    # Wait for the owned game window.
    target = _await_window(manifest, game_dir, args)
    if target is None:
        manifest.notes.append("game window never appeared")
        manifest.save()
        closure = _close_manifest(manifest, args, reason="window_timeout")
        return _emit({
            "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "launch",
            "session_id": session_id, "accepted": False,
            "reason": "window_timeout",
            "launcher_stderr_tail": _tail(stderr_path),
            "closure": closure,
        }, ok=False)

    manifest.display = target.display
    manifest.window_id = target.window_id
    manifest.game_pid = target.pid
    manifest.game_start_ticks = target.start_ticks
    manifest.exe_sha256 = target.exe_sha256
    manifest.save()

    # Renderer selection and the fail-closed log gate.
    gate, gate_detail = _select_renderer(manifest, args, started)
    manifest.renderer_gate = gate.to_dict() | gate_detail
    manifest.save()

    # Record ownership: current members of the owned group, and any null sink
    # that appeared during this launch.
    _record_ownership(manifest, sinks_before, args)
    manifest.save()

    accepted = gate.accepted
    result: dict[str, Any] = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "launch",
        "session_id": session_id,
        "accepted": accepted,
        "session": manifest.to_dict(),
        "elapsed_s": round(time.monotonic() - started, 3),
    }

    if not accepted:
        result["reason"] = "renderer_gate_failed"
        if not args.keep_on_reject:
            result["closure"] = _close_manifest(manifest, args, reason="renderer_gate_failed")
        else:
            result["note"] = "session kept open for inspection (--keep-on-reject)"
        return _emit(result, ok=False)

    if args.level:
        navigation = _navigate_level(manifest, args)
        manifest.level = navigation
        manifest.save()
        result["session"] = manifest.to_dict()
        result["level"] = navigation
        if not navigation.get("matched"):
            result["reason"] = "level_navigation_failed"
            return _emit(result, ok=False)

    return _emit(result, ok=True)


def _tail(path: Path, limit: int = 4000) -> str:
    try:
        raw = path.read_bytes()
    except OSError:
        return ""
    return raw[-limit:].decode("utf-8", "replace")


def _await_window(
    manifest: sl.SessionManifest, game_dir: Path, args: argparse.Namespace
) -> sl.GameTarget | None:
    deadline = time.monotonic() + args.window_timeout
    while time.monotonic() < deadline:
        try:
            target = sl.discover_game_target(
                manifest.process_group,
                game_dir,
                accepted_sha256=(
                    args.accept_sha or sl.ACCEPTED_EXECUTABLE_SHA256S
                ),
                loader_re=args.loader_re,
                xdo_factory=lambda display: sl.XDo(display, executable=args.xdotool),
            )
        except sl.SessionError:
            target = None
        if target is not None:
            return target
        time.sleep(args.poll_ms / 1000.0)
    return None


def _select_renderer(
    manifest: sl.SessionManifest, args: argparse.Namespace, started: float
) -> tuple[sl.RendererGate, dict]:
    """Drive renderer selection when needed, then apply the log gate.

    The gate is authoritative either way: the auto-hardware build is expected
    to reach Direct3D with no input, but it is still required to prove all six
    markers rather than being trusted because of its hash.
    """

    log_path = Path(manifest.log_path)
    detail: dict[str, Any] = {"auto_hardware": manifest.auto_hardware, "presses": []}

    if not manifest.auto_hardware:
        time.sleep(args.chooser_delay_ms / 1000.0)
        xdo = sl.XDo(manifest.display, executable=args.xdotool)
        for keysym in ("Down", "Return"):
            elapsed_ms = (time.monotonic() - started) * 1000.0
            if elapsed_ms > CHOOSER_TIMEOUT_MS - CHOOSER_SAFETY_MARGIN_MS:
                detail["chooser_deadline_risk"] = {
                    "elapsed_ms": round(elapsed_ms, 1),
                    "chooser_timeout_ms": CHOOSER_TIMEOUT_MS,
                    "note": "chooser times out to the software default",
                }
            try:
                receipt = xdo.send_key(
                    manifest.window_id, keysym, hold_ms=args.hold_ms
                )
            except sl.SessionError as exc:
                detail["press_error"] = {"reason": exc.reason, "detail": exc.detail}
                break
            detail["presses"].append(receipt)
            time.sleep(args.gap_ms / 1000.0)

    deadline = time.monotonic() + args.gate_timeout
    gate = sl.evaluate_renderer_log("")
    while time.monotonic() < deadline:
        if log_path.exists():
            text, _ = sl.read_log_text(log_path)
            gate = sl.evaluate_renderer_log(text)
            if gate.accepted or gate.rejects_found:
                break
        time.sleep(args.poll_ms / 1000.0)
    detail["log_path"] = str(log_path)
    detail["gate_elapsed_s"] = round(time.monotonic() - started, 3)
    return gate, detail


def _record_ownership(
    manifest: sl.SessionManifest, sinks_before, args: argparse.Namespace
) -> None:
    records = sl.process_records()
    members = sl.group_members(records, manifest.process_group)
    manifest.owned_processes = [record.to_dict() for record in members]
    before = {(sink["module_id"], sink["sink_name"]) for sink in sinks_before}
    after = sl.list_null_sinks(pactl=args.pactl)
    manifest.owned_sinks = [
        sink for sink in after if (sink["module_id"], sink["sink_name"]) not in before
    ]


# --------------------------------------------------------------------------
# Level navigation
# --------------------------------------------------------------------------


def _navigate_level(manifest: sl.SessionManifest, args: argparse.Namespace) -> dict:
    """Walk the carousel to a named level and confirm the load from memory.

    Each Right press is confirmed against the carousel position counter, so a
    press dropped between ``GetAsyncKeyState`` polls is retried immediately
    instead of silently selecting the wrong level (the EXP-20260816-156
    failure).  The final confirmation still comes from the internal level
    global after the level loads.
    """

    position, label, internal = sl.level_by_name(args.level)
    xdo = sl.XDo(manifest.display, executable=args.xdotool)
    memory = sl.ProcessMemory(manifest.game_pid)
    carousel_address = int(args.carousel_address, 16)
    level_address = int(args.level_address, 16)

    steps: list[dict] = []
    observed_start = sl.read_carousel_position(memory, carousel_address)
    current = observed_start
    for index in range(position):
        attempts = 0
        while True:
            attempts += 1
            xdo.send_key(manifest.window_id, "Right", hold_ms=args.hold_ms)
            time.sleep(args.gap_ms / 1000.0)
            updated = sl.read_carousel_position(memory, carousel_address)
            advanced = updated != current
            steps.append({
                "press": index,
                "attempt": attempts,
                "carousel_before": current,
                "carousel_after": updated,
                "advanced": advanced,
            })
            if advanced:
                current = updated
                break
            if attempts >= args.max_press_retries:
                return {
                    "requested": args.level,
                    "level_name": label,
                    "carousel_target": position,
                    "carousel_observed": current,
                    "internal_expected": internal,
                    "matched": False,
                    "reason": "carousel_press_not_registered",
                    "steps": steps,
                    "carousel_address": f"0x{carousel_address:08X}",
                }

    xdo.send_key(manifest.window_id, "Return", hold_ms=args.hold_ms)

    deadline = time.monotonic() + args.level_timeout
    observed_level = None
    while time.monotonic() < deadline:
        try:
            xdo.focus(manifest.window_id)
        except sl.SessionError:
            pass
        observed_level = int.from_bytes(
            memory.read(level_address, 4), "little", signed=True
        )
        if observed_level == internal:
            break
        time.sleep(args.poll_ms / 1000.0)

    return {
        "requested": args.level,
        "level_name": label,
        "carousel_target": position,
        "carousel_observed": current,
        "carousel_start": observed_start,
        "internal_expected": internal,
        "internal_observed": observed_level,
        "internal_level_address": f"0x{level_address:08X}",
        "carousel_address": f"0x{carousel_address:08X}",
        "matched": observed_level == internal,
        "steps": steps,
    }


def cmd_level(args: argparse.Namespace) -> int:
    manifest = sl.resolve_session(args.session)
    if manifest.display is None or manifest.window_id is None or manifest.game_pid is None:
        raise sl.SessionError("session_incomplete", f"{manifest.session_id} is not addressable")
    navigation = _navigate_level(manifest, args)
    manifest.level = navigation
    manifest.save()
    return _emit({
        "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "level",
        "session_id": manifest.session_id, "level": navigation,
    }, ok=bool(navigation.get("matched")))


# --------------------------------------------------------------------------
# Status and closure
# --------------------------------------------------------------------------


def cmd_status(args: argparse.Namespace) -> int:
    manifest = sl.resolve_session(args.session) if args.session else sl.resolve_session(None)
    live = sl.session_is_live(manifest)
    detail: dict[str, Any] = {
        "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "status",
        "session_id": manifest.session_id, "state": manifest.state, "live": live,
        "session": manifest.to_dict(),
    }
    if live and manifest.game_pid is not None:
        try:
            proof = ev.ownership_proof(manifest.game_pid)
            detail["ownership"] = proof.to_dict()
        except ev.OwnershipError as exc:
            detail["ownership_error"] = {"reason": exc.reason, "detail": exc.detail}
        try:
            memory = sl.ProcessMemory(manifest.game_pid)
            detail["internal_level"] = sl.read_internal_level(memory)
        except sl.SessionError as exc:
            detail["memory_error"] = {"reason": exc.reason, "detail": exc.detail}
    records = sl.process_records()
    detail["group_members"] = [
        record.to_dict() for record in sl.group_members(records, manifest.process_group or -1)
    ]
    return _emit(detail, ok=live)


def _close_manifest(
    manifest: sl.SessionManifest, args: argparse.Namespace, *, reason: str = "requested"
) -> dict:
    """Terminate only recorded identities, then re-audit.

    Signals are issued per PID after re-checking start ticks, so a PID that has
    been recycled since launch is recorded and skipped rather than killed.
    """

    recorded = {
        entry["pid"]: entry.get("start_ticks")
        for entry in manifest.owned_processes
        if isinstance(entry, dict) and "pid" in entry
    }
    records = sl.process_records()
    group = manifest.process_group
    for record in sl.group_members(records, group or -1):
        recorded.setdefault(record.pid, record.start_ticks)

    actions: list[dict] = []
    for pid, ticks in sorted(recorded.items()):
        if pid == os.getpid():
            continue
        try:
            live_group, live_ticks = sl.pid_identity(pid)
        except sl.SessionError:
            actions.append({"pid": pid, "action": "already_gone"})
            continue
        if ticks is not None and live_ticks != ticks:
            actions.append({
                "pid": pid, "action": "skipped_recycled",
                "recorded_start_ticks": ticks, "observed_start_ticks": live_ticks,
            })
            continue
        if group is not None and live_group != group:
            actions.append({
                "pid": pid, "action": "skipped_foreign_group",
                "recorded_group": group, "observed_group": live_group,
            })
            continue
        try:
            os.kill(pid, signal.SIGTERM)
            actions.append({"pid": pid, "action": "sigterm"})
        except OSError as exc:
            actions.append({"pid": pid, "action": "sigterm_failed", "detail": str(exc)})

    deadline = time.monotonic() + args.grace_s
    while time.monotonic() < deadline:
        alive = [
            pid for pid, ticks in recorded.items()
            if ticks is not None and sl.pid_matches_identity(pid, ticks)
        ]
        if not alive:
            break
        time.sleep(0.1)

    for pid, ticks in sorted(recorded.items()):
        if ticks is None or not sl.pid_matches_identity(pid, ticks):
            continue
        try:
            os.kill(pid, signal.SIGKILL)
            actions.append({"pid": pid, "action": "sigkill"})
        except OSError as exc:
            actions.append({"pid": pid, "action": "sigkill_failed", "detail": str(exc)})

    sink_actions: list[dict] = []
    live_sinks = {sink["module_id"]: sink for sink in sl.list_null_sinks(pactl=args.pactl)}
    for sink in manifest.owned_sinks:
        module_id = sink.get("module_id")
        present = live_sinks.get(module_id)
        if present is None:
            sink_actions.append({"module_id": module_id, "action": "already_unloaded"})
            continue
        if present.get("sink_name") != sink.get("sink_name"):
            sink_actions.append({
                "module_id": module_id, "action": "skipped_name_mismatch",
                "recorded": sink.get("sink_name"), "observed": present.get("sink_name"),
            })
            continue
        result = subprocess.run(
            [args.pactl, "unload-module", str(module_id)],
            capture_output=True, text=True, check=False,
        )
        sink_actions.append({
            "module_id": module_id, "action": "unloaded",
            "returncode": result.returncode,
        })

    survivors = [
        {"pid": pid, "start_ticks": ticks}
        for pid, ticks in sorted(recorded.items())
        if ticks is not None and sl.pid_matches_identity(pid, ticks)
    ]
    post_records = sl.process_records()
    post_audit = sl.audit_runtime(
        post_records,
        owned_groups=_open_session_groups() - {group} if group else set(),
        names=_audit_names(args),
    )
    closure = {
        "reason": reason,
        "closed_at": ev.now().isoformat(),
        "process_actions": actions,
        "sink_actions": sink_actions,
        "survivors": survivors,
        "post_audit": post_audit,
        "clean": not survivors,
    }
    manifest.state = "closed"
    manifest.closed_at = closure["closed_at"]
    manifest.closure = closure
    manifest.save()
    return closure


def cmd_close(args: argparse.Namespace) -> int:
    manifest = sl.resolve_session(args.session) if args.session else sl.resolve_session(None)
    closure = _close_manifest(manifest, args, reason=args.reason)
    return _emit({
        "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "close",
        "session_id": manifest.session_id, "closure": closure,
    }, ok=closure["clean"])


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def capabilities() -> dict:
    return {
        "schema_version": sl.SESSION_SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "session_lib_version": sl.SESSION_LIB_VERSION,
        "verbs": ["preflight", "launch", "status", "level", "close", "audit", "list"],
        "renderer_gate": {
            "required_markers": list(sl.HARDWARE_MARKERS),
            "reject_markers": list(sl.SOFTWARE_REJECT_MARKERS),
            "reject_patterns": [p.pattern for p in sl.SOFTWARE_REJECT_PATTERNS],
            "authority": "game log only; screenshots and key receipts are not proof",
        },
        "ownership": {
            "manifest": "dynamic/wine/RUN-SESSION-<stamp>/session.json",
            "identity": "pid + process group + PID start ticks",
            "cleanup": "recorded identities only; recycled PIDs are skipped",
        },
        "level_navigation": {
            "carousel_address": f"0x{sl.CAROUSEL_POSITION_ADDRESS:08X}",
            "internal_level_address": f"0x{sl.LEVEL_ADDRESS:08X}",
            "confirmation": "internal level global, never carousel position or a screenshot",
        },
        "claims_not_made": [
            "engine-frame synchronization",
            "that a launched session is deterministic",
            "that closure can reclaim processes it did not record",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="game-session.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--pactl", default="pactl")
        p.add_argument("--xdotool", default="xdotool")
        p.add_argument("--poll-ms", type=int, default=200)
        p.add_argument("--audit-name", action="append", default=None,
                       help="restrict the runtime-process audit to these "
                            "process names; the set used is recorded in the "
                            "preflight receipt")

    launch = sub.add_parser("launch", help="launch and gate one session")
    add_common(launch)
    launch.add_argument("--launcher", default=DEFAULT_LAUNCHER)
    launch.add_argument("--launcher-arg", action="append", default=None)
    launch.add_argument("--game-dir", default=None)
    launch.add_argument("--prefix", default=None)
    launch.add_argument("--output", default=None)
    launch.add_argument("--auto-hardware", action="store_true")
    launch.add_argument("--research", action="store_true", default=True)
    launch.add_argument("--no-research", dest="research", action="store_false")
    launch.add_argument("--windowed", action="store_true", default=True)
    launch.add_argument("--fullscreen", dest="windowed", action="store_false")
    launch.add_argument("--mute", action="store_true", default=True)
    launch.add_argument("--no-mute", dest="mute", action="store_false")
    launch.add_argument("--level", default=None, help="navigate to this level after the gate")
    launch.add_argument("--window-timeout", type=float, default=60.0)
    launch.add_argument("--gate-timeout", type=float, default=90.0)
    launch.add_argument("--level-timeout", type=float, default=60.0)
    launch.add_argument("--chooser-delay-ms", type=int, default=4000)
    launch.add_argument("--hold-ms", type=int, default=sl.DEFAULT_KEY_HOLD_MS)
    launch.add_argument("--gap-ms", type=int, default=sl.DEFAULT_KEY_GAP_MS)
    launch.add_argument("--max-press-retries", type=int, default=3)
    launch.add_argument("--grace-s", type=float, default=5.0)
    launch.add_argument("--allow-existing", action="store_true")
    launch.add_argument("--keep-on-reject", action="store_true")
    launch.add_argument("--dry-run", action="store_true")
    launch.add_argument("--carousel-address",
                        default=f"0x{sl.CAROUSEL_POSITION_ADDRESS:08X}",
                        help="override for fixture validation only")
    launch.add_argument("--level-address", default=f"0x{sl.LEVEL_ADDRESS:08X}",
                        help="override for fixture validation only")
    launch.add_argument("--accept-sha", action="append", default=None,
                        help="widen the accepted executable hash set; "
                             "fixture validation and disclosed builds only")
    launch.add_argument("--loader-re", default=ev.DEFAULT_LOADER_RE,
                        help="override for fixture validation only")
    launch.set_defaults(func=cmd_launch)

    level = sub.add_parser("level", help="navigate to a level in an open session")
    add_common(level)
    level.add_argument("--session", default=None)
    level.add_argument("--level", required=True)
    level.add_argument("--hold-ms", type=int, default=sl.DEFAULT_KEY_HOLD_MS)
    level.add_argument("--gap-ms", type=int, default=sl.DEFAULT_KEY_GAP_MS)
    level.add_argument("--max-press-retries", type=int, default=3)
    level.add_argument("--level-timeout", type=float, default=60.0)
    level.add_argument("--carousel-address",
                       default=f"0x{sl.CAROUSEL_POSITION_ADDRESS:08X}")
    level.add_argument("--level-address", default=f"0x{sl.LEVEL_ADDRESS:08X}")
    level.set_defaults(func=cmd_level)

    status = sub.add_parser("status", help="re-verify one session")
    add_common(status)
    status.add_argument("--session", default=None)
    status.set_defaults(func=cmd_status)

    close = sub.add_parser("close", help="close a session by its recorded identities")
    add_common(close)
    close.add_argument("--session", default=None)
    close.add_argument("--grace-s", type=float, default=5.0)
    close.add_argument("--reason", default="requested")
    close.set_defaults(func=cmd_close)

    preflight = sub.add_parser("preflight", help="audit for pre-existing runtime processes")
    add_common(preflight)
    preflight.set_defaults(func=cmd_preflight)

    audit = sub.add_parser("audit", help="classify runtime processes and sinks by owner")
    add_common(audit)
    audit.set_defaults(func=cmd_audit)

    listing = sub.add_parser("list", help="list recorded sessions")
    add_common(listing)
    listing.set_defaults(func=cmd_list)
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
    except UsageError as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return ev.EXIT_USAGE
    except sl.SessionError as exc:
        return _fail(exc.reason, exc.detail)
    except ev.OwnershipError as exc:
        return _fail(exc.reason, exc.detail)


if __name__ == "__main__":
    sys.exit(main())
