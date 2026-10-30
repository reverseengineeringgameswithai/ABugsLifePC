#!/usr/bin/env python3
"""Deliver menu/chooser key presses to the owned game window.

Encodes, in code, the three input findings that this project learned at the
cost of wrong-level runs and a wasted experiment arm
(``Vault/10-Environment/PC autonomous game control.md``):

* The chooser and menus read input with ``GetAsyncKeyState`` (chooser at
  ``0x004A7600``), which under Wine reflects real keyboard state.  Synthetic
  ``XSendEvent`` input -- ``xdotool key --window <id>`` -- is ignored.  This
  tool only ever sends XTEST input to the focused window.
* A bare ``xdotool key`` press lasts about 12 ms and falls between polls, so
  presses are silently dropped.  EXP-20260816-156 lost two of three carousel
  presses that way and selected the wrong level.  Every press here is held,
  by default for 180 ms.
* Focus lapses drop presses and stall the game's logic loop, so focus is
  re-established and verified before every press.

Delivery is not acceptance.  ``--verify-level`` re-reads the internal level
global ``0x00861C84`` afterwards, because carousel position is not the
internal level number and a screenshot is not proof.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402


TOOL = "send-keys"
TOOL_VERSION = "1.0.0"
RECEIPT_SCHEMA_VERSION = 1


class UsageError(ValueError):
    """Raised for a malformed command line."""


def _fail(reason: str, detail: str = "") -> int:
    print(json.dumps(sl.refusal(TOOL, reason, detail)))
    return ev.EXIT_REFUSAL


def parse_keys(args: argparse.Namespace) -> list[str]:
    keys: list[str] = []
    for entry in args.key or []:
        keys.append(entry)
    for entry in args.keys or []:
        keys.extend(part.strip() for part in entry.split(",") if part.strip())
    if not keys:
        raise UsageError("at least one --key or --keys value is required")
    keys = keys * max(1, args.repeat)
    if len(keys) > sl.MAX_KEY_PRESSES:
        raise UsageError(
            f"{len(keys)} presses exceeds the {sl.MAX_KEY_PRESSES}-press cap"
        )
    for key in keys:
        if not sl.KEYSYM_RE.fullmatch(key):
            raise UsageError(f"not an X keysym name: {key!r}")
    return keys


def resolve_window(args: argparse.Namespace) -> tuple[str, int, int | None, str | None]:
    """Return ``(display, window_id, game_pid, session_id)``."""

    if args.session:
        manifest = sl.resolve_session(args.session)
        if not manifest.display or manifest.window_id is None:
            raise sl.SessionError(
                "session_incomplete",
                f"{manifest.session_id} has no recorded display/window",
            )
        return manifest.display, manifest.window_id, manifest.game_pid, manifest.session_id
    if not args.display or args.window_id is None:
        raise UsageError("either --session or both --display and --window-id are required")
    return args.display, args.window_id, args.pid, None


def cmd_send(args: argparse.Namespace) -> int:
    display, window_id, game_pid, session_id = resolve_window(args)
    keys = parse_keys(args)
    xdo = sl.XDo(display, executable=args.xdotool)

    # Confirm the window still is the exact game surface before typing into it.
    window_class = xdo.window_class(window_id)
    if window_class.lower() != sl.GAME_WINDOW_CLASS and not args.any_window:
        raise sl.SessionError(
            "window_class_mismatch",
            f"window {window_id} class is {window_class!r}, expected "
            f"{sl.GAME_WINDOW_CLASS!r} (pass --any-window to override)",
        )
    geometry = xdo.geometry(window_id)
    if geometry != sl.GAME_WINDOW_SIZE and not args.any_window:
        raise sl.SessionError(
            "window_size_mismatch",
            f"window {window_id} is {geometry[0]}x{geometry[1]}, expected "
            f"{sl.GAME_WINDOW_SIZE[0]}x{sl.GAME_WINDOW_SIZE[1]}",
        )

    presses = []
    started = time.monotonic_ns()
    for index, key in enumerate(keys):
        if index:
            time.sleep(args.gap_ms / 1000.0)
        receipt = xdo.send_key(
            window_id, key, hold_ms=args.hold_ms, verify_focus=not args.no_verify_focus
        )
        receipt["index"] = index
        presses.append(receipt)
    finished = time.monotonic_ns()

    result = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "session_id": session_id,
        "display": display,
        "window_id": window_id,
        "window_class": window_class,
        "geometry": list(geometry),
        "method": "xtest",
        "synthetic_xsendevent_used": False,
        "hold_ms": args.hold_ms,
        "gap_ms": args.gap_ms,
        "presses": presses,
        "press_count": len(presses),
        "elapsed_ms": round((finished - started) / 1e6, 3),
        "delivery_is_not_acceptance": True,
    }

    if args.verify_level is not None:
        if game_pid is None:
            raise UsageError("--verify-level requires --session or --pid")
        memory = sl.ProcessMemory(game_pid)
        observed = sl.read_internal_level(memory)
        expected_internal, label = _expected_level(args.verify_level)
        result["level_verification"] = {
            "requested": args.verify_level,
            "level_name": label,
            "expected_internal_index": expected_internal,
            "observed_internal_index": observed,
            "address": f"0x{sl.LEVEL_ADDRESS:08X}",
            "matched": observed == expected_internal,
        }
        print(json.dumps(result, indent=2))
        return ev.EXIT_OK if observed == expected_internal else ev.EXIT_TOOL_NEGATIVE

    print(json.dumps(result, indent=2))
    return ev.EXIT_OK


def _expected_level(requested: str) -> tuple[int, str | None]:
    text = requested.strip()
    if text.lstrip("-").isdigit():
        return int(text, 10), None
    _, label, internal = sl.level_by_name(text)
    return internal, label


def cmd_levels(args: argparse.Namespace) -> int:
    """Print the carousel-position/internal-index roster."""

    print(json.dumps({
        "tool": TOOL,
        "source": "Vault/20-Research/PC level roster and numbering.md",
        "internal_level_address": f"0x{sl.LEVEL_ADDRESS:08X}",
        "levels": [
            {"carousel_position": position, "name": name, "internal_index": internal}
            for position, name, internal in sl.LEVEL_TABLE
        ],
        "caution": (
            "carousel position is not the internal level number; confirm a "
            "loaded level by reading the internal level global"
        ),
    }, indent=2))
    return ev.EXIT_OK


def capabilities() -> dict:
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "session_lib_version": sl.SESSION_LIB_VERSION,
        "verbs": ["send", "levels"],
        "delivery": {
            "method": "xtest",
            "refuses_synthetic_xsendevent": True,
            "focus_before_every_press": True,
            "default_hold_ms": sl.DEFAULT_KEY_HOLD_MS,
            "default_gap_ms": sl.DEFAULT_KEY_GAP_MS,
            "max_presses": sl.MAX_KEY_PRESSES,
            "max_hold_ms": sl.MAX_KEY_HOLD_MS,
        },
        "claims_not_made": [
            "engine-frame synchronization",
            "that dispatched input was accepted by the game",
            "carousel position equals the internal level index",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="send-keys.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")

    send = sub.add_parser("send", help="hold and release keys on the game window")
    send.add_argument("--session", default=None, help="session id, or 'current'")
    send.add_argument("--display", default=None, help=":N nested display")
    send.add_argument("--window-id", type=int, default=None)
    send.add_argument("--pid", type=int, default=None,
                      help="game PID (only needed for --verify-level without --session)")
    send.add_argument("--key", action="append", default=None)
    send.add_argument("--keys", action="append", default=None,
                      help="comma-separated keysym list")
    send.add_argument("--repeat", type=int, default=1)
    send.add_argument("--hold-ms", type=int, default=sl.DEFAULT_KEY_HOLD_MS)
    send.add_argument("--gap-ms", type=int, default=sl.DEFAULT_KEY_GAP_MS)
    send.add_argument("--no-verify-focus", action="store_true")
    send.add_argument("--any-window", action="store_true",
                      help="skip the exact game window class/size check")
    send.add_argument("--verify-level", default=None,
                      help="level name or internal index to confirm afterwards")
    send.add_argument("--xdotool", default="xdotool")
    send.set_defaults(func=cmd_send)

    levels = sub.add_parser("levels", help="print the level roster")
    levels.set_defaults(func=cmd_levels)
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
