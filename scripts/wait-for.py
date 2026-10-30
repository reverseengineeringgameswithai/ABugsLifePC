#!/usr/bin/env python3
"""Wait for a runtime condition and report how it resolved.

One implementation of the waits that were previously written three separate
times (``input-movie.py`` ``LogMilestone``, the ``gdb-harness.py`` monitor
thread, and the ``frozen-capture.sh`` poll loop) plus the waits that had no
implementation at all: a memory value, a loaded level, and a file that an
asynchronous producer is still writing.

Subcommands:

``log``     a marker appearing in game-log bytes appended after the wait
            starts (the game recreates ``bugs.log`` on each ``log``-argument
            launch, so truncation restarts the scan rather than silently
            skipping content).
``memory``  a value at an address becoming equal to, differing from, or
            changing away from a reference.
``level``   the internal level global reaching a named level's index.
``file``    a path existing and its size holding steady, for the asynchronous
            ``gamescopectl screenshot`` backend.
``window``  the owned 640x480 game window becoming discoverable.

``--hold-focus`` re-activates the game window between polls.  On this
Gamescope/Wine setup the game advances its logic loop only while its window
holds input focus (EXP-20260816-148), so a wait for a logic-dependent result
must hold focus across the wait or it will time out for the wrong reason.

Exit codes: 0 satisfied, 1 timed out, 2 usage, 3 refusal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import sys
import time
from typing import Any, Callable

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402


TOOL = "wait-for"
TOOL_VERSION = "1.0.0"
RESULT_SCHEMA_VERSION = 1

MAX_TIMEOUT_S = 3600.0
MIN_POLL_MS = 1
_WIDTHS = {"u8": "<B", "i8": "<b", "u16": "<H", "i16": "<h",
           "u32": "<I", "i32": "<i", "u64": "<Q", "i64": "<q"}


class UsageError(ValueError):
    """Raised for a malformed command line."""


def _fail(reason: str, detail: str = "") -> int:
    print(json.dumps(sl.refusal(TOOL, reason, detail)))
    return ev.EXIT_REFUSAL


def _result(condition: str, satisfied: bool, started: float, **extra: Any) -> dict:
    payload = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": RESULT_SCHEMA_VERSION,
        "condition": condition,
        "satisfied": satisfied,
        "elapsed_s": round(time.monotonic() - started, 6),
    }
    payload.update(extra)
    return payload


def _emit(payload: dict) -> int:
    print(json.dumps(payload, indent=2))
    return ev.EXIT_OK if payload["satisfied"] else ev.EXIT_TOOL_NEGATIVE


def _validate_timing(args: argparse.Namespace) -> None:
    if args.timeout <= 0 or args.timeout > MAX_TIMEOUT_S:
        raise UsageError(f"--timeout must be 0 < t <= {MAX_TIMEOUT_S}")
    if args.poll_ms < MIN_POLL_MS:
        raise UsageError(f"--poll-ms must be >= {MIN_POLL_MS}")


def _focus_holder(args: argparse.Namespace) -> Callable[[], None]:
    """Return a callable that re-establishes game-window focus, or a no-op."""

    if not getattr(args, "hold_focus", False):
        return lambda: None
    manifest = sl.resolve_session(getattr(args, "session", None))
    if not manifest.display or manifest.window_id is None:
        raise sl.SessionError(
            "session_incomplete", f"{manifest.session_id} has no display/window"
        )
    xdo = sl.XDo(manifest.display, executable=getattr(args, "xdotool", "xdotool"))
    window_id = manifest.window_id

    def hold() -> None:
        try:
            xdo.focus(window_id)
        except sl.SessionError:
            # A transient focus failure must not abort the wait; the caller
            # sees the outcome in the final satisfied/timed-out verdict.
            pass

    return hold


# --------------------------------------------------------------------------
# Conditions
# --------------------------------------------------------------------------


def cmd_log(args: argparse.Namespace) -> int:
    _validate_timing(args)
    path = Path(args.path)
    started = time.monotonic()
    deadline = started + args.timeout
    hold = _focus_holder(args)

    if args.from_offset is not None:
        offset = args.from_offset
    elif args.from_start:
        offset = 0
    else:
        try:
            offset = path.stat().st_size
        except OSError:
            offset = 0
    initial_offset = offset
    polls = 0
    while True:
        polls += 1
        hold()
        if path.exists():
            text, offset = sl.read_log_text(path, from_offset=offset)
            for number, line in enumerate(text.splitlines(), start=1):
                if args.marker in line:
                    return _emit(_result(
                        "log", True, started,
                        path=str(path), marker=args.marker,
                        initial_offset=initial_offset, end_offset=offset,
                        matched_line=line.strip(), relative_line=number, polls=polls,
                    ))
        if time.monotonic() >= deadline:
            return _emit(_result(
                "log", False, started, path=str(path), marker=args.marker,
                initial_offset=initial_offset, end_offset=offset, polls=polls,
                reason="timeout",
            ))
        time.sleep(args.poll_ms / 1000.0)


def _resolve_pid(args: argparse.Namespace) -> tuple[int, str | None]:
    if getattr(args, "session", None):
        manifest = sl.resolve_session(args.session)
        if manifest.game_pid is None:
            raise sl.SessionError(
                "session_incomplete", f"{manifest.session_id} has no game PID"
            )
        if manifest.game_start_ticks is not None and not sl.pid_matches_identity(
            manifest.game_pid, manifest.game_start_ticks
        ):
            raise sl.SessionError(
                "pid_recycled",
                f"pid {manifest.game_pid} no longer matches the recorded identity",
            )
        return manifest.game_pid, manifest.session_id
    if args.pid is None:
        raise UsageError("one of --pid or --session is required")
    return args.pid, None


def _decode_scalar(payload: bytes, fmt: str) -> int:
    return struct.unpack(_WIDTHS[fmt], payload)[0]


def cmd_memory(args: argparse.Namespace) -> int:
    _validate_timing(args)
    pid, session_id = _resolve_pid(args)
    address = int(args.addr, 16)
    fmt = args.format
    size = struct.calcsize(_WIDTHS[fmt])
    modes = [m for m in (args.equals, args.not_equals) if m is not None]
    if len(modes) + int(args.changed) != 1:
        raise UsageError("exactly one of --equals, --not-equals, or --changed is required")

    memory = sl.ProcessMemory(pid)
    started = time.monotonic()
    deadline = started + args.timeout
    hold = _focus_holder(args)
    baseline: int | None = None
    polls = 0
    observed: int | None = None
    while True:
        polls += 1
        hold()
        observed = _decode_scalar(memory.read(address, size), fmt)
        if baseline is None:
            baseline = observed
        satisfied = (
            (args.equals is not None and observed == int(args.equals, 0))
            or (args.not_equals is not None and observed != int(args.not_equals, 0))
            or (args.changed and observed != baseline)
        )
        if satisfied:
            return _emit(_result(
                "memory", True, started, session_id=session_id, pid=pid,
                address=f"0x{address:08X}", format=fmt, observed=observed,
                baseline=baseline, polls=polls,
            ))
        if time.monotonic() >= deadline:
            return _emit(_result(
                "memory", False, started, session_id=session_id, pid=pid,
                address=f"0x{address:08X}", format=fmt, observed=observed,
                baseline=baseline, polls=polls, reason="timeout",
            ))
        time.sleep(args.poll_ms / 1000.0)


def cmd_level(args: argparse.Namespace) -> int:
    _validate_timing(args)
    pid, session_id = _resolve_pid(args)
    if args.name:
        position, label, internal = sl.level_by_name(args.name)
    elif args.index is not None:
        position, label, internal = None, None, args.index
    else:
        raise UsageError("one of --name or --index is required")

    memory = sl.ProcessMemory(pid)
    started = time.monotonic()
    deadline = started + args.timeout
    hold = _focus_holder(args)
    polls = 0
    while True:
        polls += 1
        hold()
        observed = sl.read_internal_level(memory)
        if observed == internal:
            return _emit(_result(
                "level", True, started, session_id=session_id, pid=pid,
                level_name=label, carousel_position=position,
                expected_internal_index=internal, observed_internal_index=observed,
                address=f"0x{sl.LEVEL_ADDRESS:08X}", polls=polls,
            ))
        if time.monotonic() >= deadline:
            return _emit(_result(
                "level", False, started, session_id=session_id, pid=pid,
                level_name=label, carousel_position=position,
                expected_internal_index=internal, observed_internal_index=observed,
                address=f"0x{sl.LEVEL_ADDRESS:08X}", polls=polls, reason="timeout",
            ))
        time.sleep(args.poll_ms / 1000.0)


def cmd_file(args: argparse.Namespace) -> int:
    """Wait for a file to exist and stop growing.

    ``gamescopectl screenshot`` returns before the file lands, so a capture
    consumed immediately can be truncated or absent.
    """

    _validate_timing(args)
    path = Path(args.path)
    started = time.monotonic()
    deadline = started + args.timeout
    stable_needed = args.stable_ms / 1000.0
    last_size: int | None = None
    stable_since: float | None = None
    polls = 0
    while True:
        polls += 1
        try:
            size = path.stat().st_size
        except OSError:
            size = None
        now = time.monotonic()
        if size is not None and size > 0:
            if size == last_size:
                if stable_since is None:
                    stable_since = now
                elif now - stable_since >= stable_needed:
                    return _emit(_result(
                        "file", True, started, path=str(path), size=size,
                        stable_ms=args.stable_ms, polls=polls,
                    ))
            else:
                stable_since = None
            last_size = size
        if now >= deadline:
            return _emit(_result(
                "file", False, started, path=str(path), size=size,
                stable_ms=args.stable_ms, polls=polls, reason="timeout",
            ))
        time.sleep(args.poll_ms / 1000.0)


def cmd_window(args: argparse.Namespace) -> int:
    _validate_timing(args)
    if args.session:
        manifest = sl.resolve_session(args.session)
        process_group = manifest.process_group
        game_dir = Path(manifest.game_dir)
    else:
        if args.process_group is None or not args.game_dir:
            raise UsageError(
                "either --session or both --process-group and --game-dir are required"
            )
        process_group = args.process_group
        game_dir = Path(args.game_dir)
    if process_group is None:
        raise sl.SessionError("session_incomplete", "no recorded process group")

    started = time.monotonic()
    deadline = started + args.timeout
    polls = 0
    last_error: str | None = None
    while True:
        polls += 1
        try:
            target = sl.discover_game_target(process_group, game_dir)
        except sl.SessionError as exc:
            target, last_error = None, f"{exc.reason}: {exc.detail}"
        if target is not None:
            return _emit(_result(
                "window", True, started, polls=polls, target=target.to_dict(),
            ))
        if time.monotonic() >= deadline:
            return _emit(_result(
                "window", False, started, polls=polls, reason="timeout",
                last_error=last_error, process_group=process_group,
                game_dir=str(game_dir),
            ))
        time.sleep(args.poll_ms / 1000.0)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def capabilities() -> dict:
    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "session_lib_version": sl.SESSION_LIB_VERSION,
        "conditions": ["log", "memory", "level", "file", "window"],
        "limits": {"max_timeout_s": MAX_TIMEOUT_S, "min_poll_ms": MIN_POLL_MS},
        "hold_focus": (
            "re-activates the owned game window between polls; required when "
            "waiting on a logic-dependent result because the game advances its "
            "logic loop only while focused (EXP-20260816-148)"
        ),
        "exit_codes": {"0": "satisfied", "1": "timed out", "2": "usage", "3": "refusal"},
    }


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--poll-ms", type=int, default=100)


def _add_focus(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--session", default=None, help="session id, or 'current'")
    parser.add_argument("--hold-focus", action="store_true")
    parser.add_argument("--xdotool", default="xdotool")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wait-for.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")

    log = sub.add_parser("log", help="wait for a marker in newly appended log bytes")
    _add_common(log)
    _add_focus(log)
    log.add_argument("--path", required=True)
    log.add_argument("--marker", required=True)
    log.add_argument("--from-offset", type=int, default=None)
    log.add_argument("--from-start", action="store_true",
                     help="scan the whole existing file, not only new bytes")
    log.set_defaults(func=cmd_log)

    memory = sub.add_parser("memory", help="wait for a memory value")
    _add_common(memory)
    _add_focus(memory)
    memory.add_argument("--pid", type=int, default=None)
    memory.add_argument("--addr", required=True)
    memory.add_argument("--format", choices=sorted(_WIDTHS), default="i32")
    memory.add_argument("--equals", default=None)
    memory.add_argument("--not-equals", default=None)
    memory.add_argument("--changed", action="store_true")
    memory.set_defaults(func=cmd_memory)

    level = sub.add_parser("level", help="wait for the internal level index")
    _add_common(level)
    _add_focus(level)
    level.add_argument("--pid", type=int, default=None)
    level.add_argument("--name", default=None)
    level.add_argument("--index", type=int, default=None)
    level.set_defaults(func=cmd_level)

    file_parser = sub.add_parser("file", help="wait for a file to exist and settle")
    _add_common(file_parser)
    file_parser.add_argument("--path", required=True)
    file_parser.add_argument("--stable-ms", type=int, default=200)
    file_parser.set_defaults(func=cmd_file)

    window = sub.add_parser("window", help="wait for the owned game window")
    _add_common(window)
    window.add_argument("--session", default=None)
    window.add_argument("--process-group", type=int, default=None)
    window.add_argument("--game-dir", default=None)
    window.set_defaults(func=cmd_window)
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
    except ValueError as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return ev.EXIT_USAGE
    except sl.SessionError as exc:
        return _fail(exc.reason, exc.detail)
    except ev.OwnershipError as exc:
        return _fail(exc.reason, exc.detail)


if __name__ == "__main__":
    sys.exit(main())
