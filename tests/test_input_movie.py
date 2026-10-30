from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import time

import pytest


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "input-movie.py"
PYTHON = ROOT / ".venv" / "bin" / "python"
WINDOW_ID = 99


def _sandbox(tmp_path: Path) -> tuple[Path, Path, str]:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("/work/\n", encoding="utf-8")
    game_dir = tmp_path / "work" / "copies" / "run" / "PC" / "BUGS"
    game_dir.mkdir(parents=True)
    exe = game_dir / "bugs.exe"
    exe.write_bytes(b"MZ-input-movie-fixture")
    digest = hashlib.sha256(exe.read_bytes()).hexdigest()
    return tmp_path, game_dir, digest


def _spawn_game(game_dir: Path) -> subprocess.Popen:
    return subprocess.Popen(
        ["bugs.exe", "-c", "import time; time.sleep(30)"],
        executable=sys.executable,
        cwd=game_dir,
    )


def _xdotool_stub(tmp_path: Path, game_pid: int, log: Path, *, focus: int = WINDOW_ID) -> Path:
    stub = tmp_path / f"xdotool-{game_pid}.py"
    stub.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"log={str(log)!r}\n"
        "args=sys.argv[1:]\n"
        "cmd=args[0] if args else ''\n"
        f"pid={game_pid}\n"
        f"focus={focus}\n"
        "if cmd == 'getwindowpid': print(pid)\n"
        "elif cmd == 'getwindowname': print('ABLPC fixture')\n"
        "elif cmd == 'getwindowclassname': print('gamescope-fixture')\n"
        "elif cmd == 'getwindowgeometry':\n"
        " print('WINDOW=99\\nX=10\\nY=20\\nWIDTH=1280\\nHEIGHT=960\\nSCREEN=0')\n"
        "elif cmd == 'getwindowfocus': print(focus)\n"
        "elif cmd in {'keydown','keyup'}:\n"
        " with open(log,'a',encoding='utf-8') as h: h.write(' '.join(args)+'\\n')\n"
        "else:\n"
        " print('unsupported '+repr(args), file=sys.stderr); raise SystemExit(2)\n",
        encoding="utf-8",
    )
    stub.chmod(0o755)
    return stub


def _event_stream(path: Path, *items: dict) -> Path:
    path.write_text(
        "".join(json.dumps(item, sort_keys=True) + "\n" for item in items),
        encoding="utf-8",
    )
    return path


def _target_args(
    root: Path,
    game_dir: Path,
    digest: str,
    child: subprocess.Popen,
    xdotool: Path,
) -> list[str]:
    return [
        "--pid", str(child.pid),
        "--window-id", str(WINDOW_ID),
        "--expected-sha", digest,
        "--loader-re", ".*python.*",
        "--cwd-prefix", str(game_dir) + os.sep,
        "--window-owner-re", ".*python.*",
        "--window-name-re", "^ABLPC fixture$",
        "--window-class-re", "^gamescope-fixture$",
        "--display", ":test",
        "--xdotool", str(xdotool),
        "--anchor-timeout", "2",
    ]


def _run(
    root: Path,
    argv: list[str],
    *,
    event_stream: Path | None = None,
    replay_echo_stream: Path | None = None,
    status_path: Path | None = None,
    timeout: float = 20,
) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    if event_stream is not None:
        env["ABLPC_INPUT_EVENT_STREAM"] = str(event_stream)
    else:
        env.pop("ABLPC_INPUT_EVENT_STREAM", None)
    if replay_echo_stream is not None:
        env["ABLPC_INPUT_REPLAY_ECHO_STREAM"] = str(replay_echo_stream)
    else:
        env.pop("ABLPC_INPUT_REPLAY_ECHO_STREAM", None)
    command = [str(PYTHON), str(TOOL), *argv]
    if status_path is None:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
        )
    with status_path.open("wb") as status_handle:
        return subprocess.run(
            [*command, "--status-fd", str(status_handle.fileno())],
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
            pass_fds=(status_handle.fileno(),),
        )


class _StatusChannel:
    """Inherited `--status-fd` pipe, read to order test actions after the
    tool's own readiness transitions instead of after a fixed sleep.

    `scripts/input-movie.py` snapshots the anchor log's baseline size in
    `LogMilestone.__init__` and only then emits its `armed` transition (record:
    `_anchor_for_record`; replay: `_anchor_for_replay`).  Waiting for `armed`
    therefore guarantees an anchor line appended afterwards falls inside the
    new-bytes window the tool polls, and the tool re-reads everything from that
    baseline on every poll, so no marker can be missed once `armed` is seen.

    A fixed sleep left those two events unordered and was the cause of KU-065:
    when the freshly spawned recorder had not yet reached its baseline
    snapshot, the appended marker became part of the "old bytes" the tool must
    ignore, and the anchor timed out.  Measured on this host, the recorder
    reaches `armed` at a median of 104 ms idle and 120-164 ms under CPU load,
    against the former 120 ms sleep.
    """

    def __init__(self) -> None:
        self.read_fd, self.write_fd = os.pipe()
        self._pending = b""
        self._records: list[dict] = []
        self._read_open = True
        self._write_open = True

    def release_write_end(self) -> None:
        """Drop the parent's write end so the reader observes EOF at exit."""
        if self._write_open:
            os.close(self.write_fd)
            self._write_open = False

    def _next_record(self) -> dict | None:
        index = self._pending.find(b"\n")
        if index < 0:
            return None
        line, self._pending = self._pending[:index], self._pending[index + 1:]
        record = json.loads(line.decode("utf-8"))
        self._records.append(record)
        return record

    def wait_for(self, event: str, timeout: float = 10.0) -> dict:
        deadline = time.monotonic() + timeout
        while True:
            record = self._next_record()
            if record is not None:
                if record["event"] == event:
                    return record
                continue
            remaining = deadline - time.monotonic()
            assert remaining > 0, f"no {event!r} status: {self._records}"
            if not select.select([self.read_fd], [], [], remaining)[0]:
                continue
            chunk = os.read(self.read_fd, 4096)
            assert chunk, f"status channel closed before {event!r}: {self._records}"
            self._pending += chunk

    def records(self) -> list[dict]:
        """Every status record in order.  Call once the tool has exited."""
        while True:
            chunk = os.read(self.read_fd, 4096)
            if not chunk:
                break
            self._pending += chunk
        while self._next_record() is not None:
            pass
        return list(self._records)

    def close(self) -> None:
        self.release_write_end()
        if self._read_open:
            os.close(self.read_fd)
            self._read_open = False


def _record_fixture(
    tmp_path: Path,
    *,
    stream_items: tuple[dict, ...] | None = None,
) -> tuple[Path, Path, Path, subprocess.Popen, str, Path]:
    root, game_dir, digest = _sandbox(tmp_path)
    child = _spawn_game(game_dir)
    dispatch_log = tmp_path / "dispatch.log"
    xdotool = _xdotool_stub(tmp_path, child.pid, dispatch_log)
    stream = _event_stream(
        tmp_path / "events.jsonl",
        *(stream_items or (
            {"delay_ms": 1, "kind": "down", "keysym": "Up", "keycode": 111},
            {"delay_ms": 2, "kind": "up", "keysym": "Up", "keycode": 111},
            {"delay_ms": 1, "kind": "down", "keysym": "F12", "keycode": 96},
        )),
    )
    movie = tmp_path / "work" / "input-movies" / "route.json"
    movie.parent.mkdir(parents=True)
    result = _run(
        root,
        ["record", *_target_args(root, game_dir, digest, child, xdotool),
         "--movie", str(movie), "--start-now", "--arm-delay", "0",
         "--max-duration", "2"],
        event_stream=stream,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return root, game_dir, movie, child, digest, xdotool


def test_capabilities_are_window_scoped_and_not_host_wide() -> None:
    result = subprocess.run(
        [str(PYTHON), str(TOOL), "--capabilities"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == 2
    assert payload["supported_schema_versions"] == [1, 2]
    assert payload["input_scope"] == "one-explicit-X11-window-keyboard-events"
    assert payload["display_wide_capture"] is False
    assert payload["host_input_device_capture"] is False
    assert payload["internal_game_frame_synchronization"] is False
    assert payload["target_echo_required"] is True
    assert payload["replay_backend"] == (
        "persistent X11/XTEST with exact-window echo"
    )
    assert payload["log_anchored_runtime_checkpoint"] == (
        "bounded post-anchor log segment and ROUTINE trace"
    )
    assert payload["supervisor_status_events"] == [
        "armed",
        "recording-started",
        "replay-started",
    ]


def test_record_writes_strict_hash_gated_movie_and_receipt(tmp_path: Path) -> None:
    root, _game_dir, movie, child, digest, _xdotool = _record_fixture(tmp_path)
    try:
        data = json.loads(movie.read_text(encoding="utf-8"))
        assert data["schema_version"] == 2
        assert data["runtime_log_checkpoint"] is None
        assert data["recording_backend"] == "synthetic-jsonl-v1"
        assert data["target"]["executable_sha256"] == digest
        assert [(item["action"], item["keysym"]) for item in data["events"]] == [
            ("down", "Up"), ("up", "Up")
        ]
        assert data["termination"] == "stop-keysym"
        assert data["complete"] is True

        run = next((root / "dynamic" / "wine").glob("RUN-INP-REC-*"))
        receipt = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
        assert receipt["status"] == "complete"
        assert receipt["accepted"] is False  # fixture backend cannot be live evidence
        assert receipt["movie_sha256"] == hashlib.sha256(movie.read_bytes()).hexdigest()
        assert receipt["window_before"]["same_process_group"] is True
        assert receipt["all_keys_released"] is True
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_record_normalizes_preparatory_unmatched_release(tmp_path: Path) -> None:
    root, _game_dir, movie, child, _digest, _xdotool = _record_fixture(
        tmp_path,
        stream_items=(
            {"delay_ms": 1, "kind": "up", "keysym": "Down", "keycode": 116},
            {"delay_ms": 1, "kind": "down", "keysym": "Down", "keycode": 116},
            {"delay_ms": 1, "kind": "up", "keysym": "Down", "keycode": 116},
            {"delay_ms": 1, "kind": "down", "keysym": "F12", "keycode": 96},
        ),
    )
    try:
        data = json.loads(movie.read_text(encoding="utf-8"))
        assert [(item["action"], item["keysym"]) for item in data["events"]] == [
            ("down", "Down"), ("up", "Down")
        ]
        run = next((root / "dynamic" / "wine").glob("RUN-INP-REC-*"))
        receipt = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
        assert receipt["ignored_unmatched_release_count"] == 1
        assert receipt["ignored_unmatched_releases"][0]["keysym"] == "Down"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_validate_accepts_exact_movie_and_rejects_unpaired_release(tmp_path: Path) -> None:
    root, _game_dir, movie, child, _digest, _xdotool = _record_fixture(tmp_path)
    try:
        valid = _run(root, ["validate", "--movie", str(movie)])
        assert valid.returncode == 0, valid.stdout + valid.stderr
        assert json.loads(valid.stdout)["event_count"] == 2

        legacy = json.loads(movie.read_text(encoding="utf-8"))
        legacy["schema_version"] = 1
        legacy.pop("runtime_log_checkpoint")
        legacy_path = movie.with_name("legacy-v1.json")
        legacy_path.write_text(json.dumps(legacy), encoding="utf-8")
        legacy_result = _run(root, ["validate", "--movie", str(legacy_path)])
        assert legacy_result.returncode == 0, legacy_result.stdout + legacy_result.stderr

        malformed = json.loads(movie.read_text(encoding="utf-8"))
        malformed["events"] = [malformed["events"][1]]
        malformed["events"][0]["sequence"] = 0
        malformed["schedule_sha256"] = "0" * 64
        bad = movie.with_name("bad.json")
        bad.write_text(json.dumps(malformed), encoding="utf-8")
        rejected = _run(root, ["validate", "--movie", str(bad)])
        assert rejected.returncode == 3
        assert json.loads(rejected.stdout)["reason"] == "movie_invalid"

        empty = json.loads(movie.read_text(encoding="utf-8"))
        empty["events"] = []
        empty["schedule_sha256"] = hashlib.sha256(b"[]").hexdigest()
        empty_path = movie.with_name("empty.json")
        empty_path.write_text(json.dumps(empty), encoding="utf-8")
        empty_result = _run(root, ["validate", "--movie", str(empty_path)])
        assert empty_result.returncode == 3
        assert json.loads(empty_result.stdout)["reason"] == "movie_invalid"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_replay_refuses_synthetic_by_default_then_dispatches_when_test_enabled(
    tmp_path: Path,
) -> None:
    root, game_dir, movie, child, digest, xdotool = _record_fixture(tmp_path)
    try:
        refused = _run(
            root,
            ["replay", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--arm-delay", "0"],
        )
        assert refused.returncode == 3
        assert json.loads(refused.stdout)["reason"] == "synthetic_movie_refused"

        status_path = tmp_path / "replay-status.jsonl"
        accepted = _run(
            root,
            ["replay", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--arm-delay", "0",
             "--max-drift-ms", "1000", "--max-delivery-drift-ms", "1000",
             "--allow-synthetic"],
            status_path=status_path,
        )
        assert accepted.returncode == 0, accepted.stdout + accepted.stderr
        summary = json.loads(accepted.stdout)
        assert summary["accepted"] is True
        receipt_path = next(
            (root / "dynamic" / "wine").glob("RUN-INP-REP-*/metadata.json")
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["events_dispatched"] == receipt["event_count"] == 2
        assert receipt["events_delivered"] == receipt["event_count"] == 2
        assert receipt["target_echo_verified"] is True
        assert receipt["replay_backend"]["backend"] == (
            "synthetic-persistent-replay-v1"
        )
        assert receipt["all_keys_released"] is True
        assert [item["keysym"] for item in receipt["dispatches"]] == ["Up", "Up"]
        statuses = [
            json.loads(line)
            for line in status_path.read_text(encoding="utf-8").splitlines()
        ]
        assert [(item["event"], item["mode"]) for item in statuses] == [
            ("armed", "replay"),
            ("replay-started", "replay"),
        ]
        assert statuses[0]["anchor_type"] == "manual-delay"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_replay_refuses_mismatched_target_echo(tmp_path: Path) -> None:
    root, game_dir, movie, child, digest, xdotool = _record_fixture(tmp_path)
    echo = _event_stream(
        tmp_path / "mismatch-echo.jsonl",
        {"kind": "down", "keysym": "Right", "keycode": 114},
    )
    try:
        result = _run(
            root,
            [
                "replay", *_target_args(root, game_dir, digest, child, xdotool),
                "--movie", str(movie), "--arm-delay", "0",
                "--max-drift-ms", "1000", "--max-delivery-drift-ms", "1000",
                "--allow-synthetic",
            ],
            replay_echo_stream=echo,
        )
        assert result.returncode == 1, result.stdout + result.stderr
        summary = json.loads(result.stdout)
        assert summary["accepted"] is False
        assert summary["target_echo_verified"] is False
        assert summary["failure"]["reason"] == "target_echo_mismatch"
        receipt_path = next(
            (root / "dynamic" / "wine").glob("RUN-INP-REP-*/metadata.json")
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["events_dispatched"] == 1
        assert receipt["events_delivered"] == 0
        assert receipt["target_echo_verified"] is False
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_replay_refuses_unexpected_extra_target_event(tmp_path: Path) -> None:
    root, game_dir, movie, child, digest, xdotool = _record_fixture(tmp_path)
    echo = _event_stream(
        tmp_path / "extra-echo.jsonl",
        {"kind": "down", "keysym": "Up", "keycode": 111},
        {"kind": "down", "keysym": "Right", "keycode": 114},
    )
    try:
        result = _run(
            root,
            [
                "replay", *_target_args(root, game_dir, digest, child, xdotool),
                "--movie", str(movie), "--arm-delay", "0",
                "--max-drift-ms", "1000", "--max-delivery-drift-ms", "1000",
                "--allow-synthetic",
            ],
            replay_echo_stream=echo,
        )
        assert result.returncode == 1, result.stdout + result.stderr
        assert json.loads(result.stdout)["failure"]["reason"] == (
            "unexpected_target_event"
        )
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_replay_echo_normalizes_preparatory_release(tmp_path: Path) -> None:
    root, game_dir, movie, child, digest, xdotool = _record_fixture(tmp_path)
    echo = _event_stream(
        tmp_path / "preparatory-release-echo.jsonl",
        {"kind": "up", "keysym": "Up", "keycode": 111},
        {"kind": "down", "keysym": "Up", "keycode": 111},
        {"delay_ms": 1, "kind": "up", "keysym": "Up", "keycode": 111},
    )
    try:
        result = _run(
            root,
            [
                "replay", *_target_args(root, game_dir, digest, child, xdotool),
                "--movie", str(movie), "--arm-delay", "0",
                "--max-drift-ms", "1000", "--max-delivery-drift-ms", "1000",
                "--allow-synthetic",
            ],
            replay_echo_stream=echo,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        receipt_path = next(
            (root / "dynamic" / "wine").glob("RUN-INP-REP-*/metadata.json")
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert receipt["target_echo_verified"] is True
        assert receipt["ignored_unmatched_release_count"] == 1
        assert receipt["ignored_unmatched_releases"][0]["keysym"] == "Up"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_replay_refuses_late_or_missing_target_echo(tmp_path: Path) -> None:
    root, game_dir, movie, child, digest, xdotool = _record_fixture(tmp_path)
    late_echo = _event_stream(
        tmp_path / "late-echo.jsonl",
        {"delay_ms": 25, "kind": "down", "keysym": "Up", "keycode": 111},
    )
    missing_echo = _event_stream(tmp_path / "missing-echo.jsonl")
    try:
        late = _run(
            root,
            [
                "replay", *_target_args(root, game_dir, digest, child, xdotool),
                "--movie", str(movie), "--arm-delay", "0",
                "--max-drift-ms", "1000", "--max-delivery-drift-ms", "5",
                "--echo-timeout-ms", "100", "--allow-synthetic",
            ],
            replay_echo_stream=late_echo,
        )
        assert late.returncode == 1, late.stdout + late.stderr
        assert json.loads(late.stdout)["failure"]["reason"] == (
            "target_delivery_timing_drift"
        )
        for run in (root / "dynamic" / "wine").glob("RUN-INP-REP-*"):
            run.rename(run.with_name(run.name + "-late"))

        missing = _run(
            root,
            [
                "replay", *_target_args(root, game_dir, digest, child, xdotool),
                "--movie", str(movie), "--arm-delay", "0",
                "--max-drift-ms", "1000", "--max-delivery-drift-ms", "1000",
                "--echo-timeout-ms", "10", "--allow-synthetic",
            ],
            replay_echo_stream=missing_echo,
        )
        assert missing.returncode == 1, missing.stdout + missing.stderr
        assert json.loads(missing.stdout)["failure"]["reason"] == (
            "target_echo_timeout"
        )
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_focus_loss_fails_and_releases_held_key(tmp_path: Path) -> None:
    root, game_dir, digest = _sandbox(tmp_path)
    child = _spawn_game(game_dir)
    dispatch_log = tmp_path / "dispatch.log"
    xdotool = _xdotool_stub(tmp_path, child.pid, dispatch_log)
    stream = _event_stream(
        tmp_path / "events.jsonl",
        {"delay_ms": 1, "kind": "down", "keysym": "Right", "keycode": 114},
        {"delay_ms": 1, "kind": "focus-out"},
    )
    movie = tmp_path / "work" / "input-movies" / "failed.json"
    movie.parent.mkdir(parents=True)
    try:
        result = _run(
            root,
            ["record", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--start-now", "--arm-delay", "0",
             "--max-duration", "2"],
            event_stream=stream,
        )
        assert result.returncode == 3
        assert json.loads(result.stdout)["reason"] == "focus_lost_during_recording"
        assert not movie.exists()
        assert "keyup --window 99 Right" in dispatch_log.read_text(encoding="utf-8")
        run = next((root / "dynamic" / "wine").glob("RUN-INP-REC-*"))
        receipt = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
        assert receipt["status"] == "recording-failed"
        assert receipt["all_keys_released"] is True
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_empty_recording_refuses_without_writing_movie(tmp_path: Path) -> None:
    root, game_dir, digest = _sandbox(tmp_path)
    child = _spawn_game(game_dir)
    dispatch_log = tmp_path / "dispatch.log"
    xdotool = _xdotool_stub(tmp_path, child.pid, dispatch_log)
    stream = _event_stream(
        tmp_path / "events.jsonl",
        {"delay_ms": 1000, "kind": "down", "keysym": "F12", "keycode": 96},
    )
    movie = tmp_path / "work" / "input-movies" / "empty.json"
    movie.parent.mkdir(parents=True)
    try:
        result = _run(
            root,
            ["record", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--start-now", "--arm-delay", "0",
             "--max-duration", "0.1"],
            event_stream=stream,
        )
        assert result.returncode == 3
        assert json.loads(result.stdout)["reason"] == "recorded_movie_invalid"
        assert not movie.exists()
        run = next((root / "dynamic" / "wine").glob("RUN-INP-REC-*"))
        receipt = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
        assert receipt["status"] == "recording-failed"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_log_anchor_uses_only_new_log_bytes(tmp_path: Path) -> None:
    root, game_dir, digest = _sandbox(tmp_path)
    child = _spawn_game(game_dir)
    dispatch_log = tmp_path / "dispatch.log"
    xdotool = _xdotool_stub(tmp_path, child.pid, dispatch_log)
    log = game_dir / "bugs.log"
    log.write_text("ROUTINE : NextLife. old\n", encoding="utf-8")
    stream = _event_stream(
        tmp_path / "events.jsonl",
        {"delay_ms": 300, "kind": "down", "keysym": "Left", "keycode": 113},
        {"delay_ms": 2, "kind": "up", "keysym": "Left", "keycode": 113},
        {"delay_ms": 1, "kind": "down", "keysym": "F12", "keycode": 96},
    )
    movie = tmp_path / "work" / "input-movies" / "anchored.json"
    movie.parent.mkdir(parents=True)
    env = dict(os.environ)
    env.update({"ABLPC_ROOT": str(root), "ABLPC_INPUT_EVENT_STREAM": str(stream)})
    # One status pipe per tool invocation.  `pass_fds` keeps each child from
    # inheriting the others' descriptors.
    status = _StatusChannel()
    replay_status = _StatusChannel()
    mismatch_status = _StatusChannel()
    proc = subprocess.Popen(
        [str(PYTHON), str(TOOL), "record",
         *_target_args(root, game_dir, digest, child, xdotool),
         "--movie", str(movie), "--start-milestone", "NextLife.", "--log", str(log),
         "--max-duration", "2", "--status-fd", str(status.write_fd)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        pass_fds=(status.write_fd,),
    )
    status.release_write_end()
    try:
        # The recorder has taken its log baseline once `armed` arrives; only
        # then is appending the anchor line guaranteed to be new bytes.
        status.wait_for("armed")
        with log.open("a", encoding="utf-8") as handle:
            handle.write("ROUTINE : NextLife.\n")
            handle.flush()
        stdout, stderr = proc.communicate(timeout=10)
        assert proc.returncode == 0, stdout + stderr
        data = json.loads(movie.read_text(encoding="utf-8"))
        assert data["anchor"]["type"] == "log-milestone"
        assert data["anchor"]["start_offset"] == len("ROUTINE : NextLife. old\n")
        assert data["anchor"]["matched_offset"] >= data["anchor"]["start_offset"]
        assert data["anchor"]["neutral_wait_ns"] >= 0
        statuses = status.records()
        assert [(item["event"], item["mode"]) for item in statuses] == [
            ("armed", "record"),
            ("recording-started", "record"),
        ]
        assert statuses[0]["anchor_type"] == "log-milestone"
        assert statuses[0]["marker"] == "NextLife."
        assert data["runtime_log_checkpoint"]["segment_sha256"] == hashlib.sha256(
            b"NextLife.\n"
        ).hexdigest()

        replay = subprocess.Popen(
            [str(PYTHON), str(TOOL), "replay",
             *_target_args(root, game_dir, digest, child, xdotool),
                 "--movie", str(movie), "--log", str(log), "--allow-synthetic",
                 "--max-drift-ms", "1000", "--max-delivery-drift-ms", "1000",
                 "--status-fd",
             str(replay_status.write_fd)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "ABLPC_ROOT": str(root)},
            pass_fds=(replay_status.write_fd,),
        )
        replay_status.release_write_end()
        replay_status.wait_for("armed")
        with log.open("a", encoding="utf-8") as handle:
            handle.write("ROUTINE : NextLife.\n")
            handle.flush()
        replay_stdout, replay_stderr = replay.communicate(timeout=10)
        assert replay.returncode == 0, replay_stdout + replay_stderr
        replay_summary = json.loads(replay_stdout)
        assert replay_summary["accepted"] is True
        replay_receipts = sorted(
            (root / "dynamic" / "wine").glob("RUN-INP-REP-*/metadata.json")
        )
        replay_receipt = json.loads(
            replay_receipts[-1].read_text(encoding="utf-8")
        )
        assert replay_receipt["replay_anchor"]["neutral_wait_ns"] == data["anchor"][
            "neutral_wait_ns"
        ]
        checkpoint = replay_receipt["runtime_log_checkpoint"]
        assert checkpoint["log_basename"] == "bugs.log"
        assert checkpoint["size"] > 0
        assert checkpoint["segment_sha256"] == hashlib.sha256(
            (replay_receipts[-1].parent / "runtime-log-segment.bin").read_bytes()
        ).hexdigest()
        replay_statuses = replay_status.records()
        assert [item["event"] for item in replay_statuses] == [
            "armed",
            "replay-started",
        ]
        for run in (root / "dynamic" / "wine").glob("RUN-INP-REP-*"):
            run.rename(run.with_name(run.name + "-accepted"))

        mismatched_data = json.loads(movie.read_text(encoding="utf-8"))
        mismatched_data["runtime_log_checkpoint"]["segment_sha256"] = "0" * 64
        mismatched_movie = movie.with_name("mismatched-checkpoint.json")
        mismatched_movie.write_text(json.dumps(mismatched_data), encoding="utf-8")
        mismatched_replay = subprocess.Popen(
            [str(PYTHON), str(TOOL), "replay",
             *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(mismatched_movie), "--log", str(log),
             "--allow-synthetic", "--max-drift-ms", "1000",
             "--max-delivery-drift-ms", "1000",
             "--status-fd", str(mismatch_status.write_fd)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "ABLPC_ROOT": str(root)},
            pass_fds=(mismatch_status.write_fd,),
        )
        mismatch_status.release_write_end()
        mismatch_status.wait_for("armed")
        with log.open("a", encoding="utf-8") as handle:
            handle.write("ROUTINE : NextLife.\n")
            handle.flush()
        mismatch_stdout, mismatch_stderr = mismatched_replay.communicate(timeout=10)
        assert mismatched_replay.returncode == 1, mismatch_stdout + mismatch_stderr
        assert json.loads(mismatch_stdout)["failure"]["reason"] == (
            "runtime_log_checkpoint_mismatch"
        )
    finally:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
        for channel in (status, replay_status, mismatch_status):
            channel.close()
        child.terminate()
        child.wait(timeout=5)


def test_window_owner_must_share_game_process_group(tmp_path: Path) -> None:
    root, game_dir, digest = _sandbox(tmp_path)
    child = _spawn_game(game_dir)
    unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"], start_new_session=True)
    dispatch_log = tmp_path / "dispatch.log"
    xdotool = _xdotool_stub(tmp_path, unrelated.pid, dispatch_log)
    stream = _event_stream(
        tmp_path / "events.jsonl",
        {"kind": "down", "keysym": "F12", "keycode": 96},
    )
    movie = tmp_path / "work" / "input-movies" / "bad-owner.json"
    movie.parent.mkdir(parents=True)
    try:
        result = _run(
            root,
            ["record", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--start-now", "--arm-delay", "0"],
            event_stream=stream,
        )
        assert result.returncode == 3
        assert json.loads(result.stdout)["reason"] == "window_process_group_mismatch"
        assert not list((root / "dynamic" / "wine").glob("RUN-INP-*"))
    finally:
        unrelated.terminate()
        unrelated.wait(timeout=5)
        child.terminate()
        child.wait(timeout=5)


def test_frame_hash_is_required_to_match_on_replay(tmp_path: Path) -> None:
    root, game_dir, digest = _sandbox(tmp_path)
    child = _spawn_game(game_dir)
    dispatch_log = tmp_path / "dispatch.log"
    xdotool = _xdotool_stub(tmp_path, child.pid, dispatch_log)
    frame = tmp_path / "work" / "frame.png"
    frame.parent.mkdir(parents=True, exist_ok=True)
    frame.write_bytes(b"frame-a")
    stream = _event_stream(
        tmp_path / "events.jsonl",
        {"delay_ms": 1, "kind": "down", "keysym": "Up", "keycode": 111},
        {"delay_ms": 1, "kind": "up", "keysym": "Up", "keycode": 111},
        {"delay_ms": 1, "kind": "down", "keysym": "F12", "keycode": 96},
    )
    movie = tmp_path / "work" / "input-movies" / "frame-anchored.json"
    movie.parent.mkdir(parents=True)
    try:
        recorded = _run(
            root,
            ["record", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--start-now", "--arm-delay", "0",
             "--anchor-frame", str(frame)],
            event_stream=stream,
        )
        assert recorded.returncode == 0, recorded.stdout + recorded.stderr
        frame.write_bytes(b"frame-b")
        replayed = _run(
            root,
            ["replay", *_target_args(root, game_dir, digest, child, xdotool),
             "--movie", str(movie), "--arm-delay", "0",
             "--anchor-frame", str(frame), "--allow-synthetic"],
        )
        assert replayed.returncode == 3
        assert json.loads(replayed.stdout)["reason"] == "anchor_frame_mismatch"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_compare_requires_accepted_complete_matching_replays(tmp_path: Path) -> None:
    receipt_a = tmp_path / "a.json"
    receipt_b = tmp_path / "b.json"
    base = {
        "tool": "input-movie",
        "mode": "replay",
        "accepted": True,
        "tool_version": "1.3.0",
        "implementation_sha256": "0" * 64,
        "movie_sha256": "a" * 64,
        "schedule_sha256": "b" * 64,
        "max_request_drift_ns": 50_000_000,
        "max_delivery_drift_ns": 5_000_000,
        "echo_timeout_ns": 100_000_000,
        "event_count": 2,
        "events_dispatched": 2,
        "events_delivered": 2,
        "target_echo_verified": True,
        "all_keys_released": True,
        "window_before": {"signature": {"name": "fixture"}},
        "replay_anchor": {"type": "log-milestone", "marker": "NextLife"},
        "runtime_log_checkpoint": {
            "segment_sha256": "c" * 64,
            "routine_trace_sha256": "d" * 64,
        },
    }
    receipt_a.write_text(json.dumps(base), encoding="utf-8")
    receipt_b.write_text(json.dumps(base), encoding="utf-8")
    result = subprocess.run(
        [str(PYTHON), str(TOOL), "compare", str(receipt_a), str(receipt_b)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["agreement"] is True

    changed = dict(base)
    changed["events_dispatched"] = 1
    receipt_b.write_text(json.dumps(changed), encoding="utf-8")
    mismatch = subprocess.run(
        [str(PYTHON), str(TOOL), "compare", str(receipt_a), str(receipt_b)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert mismatch.returncode == 1
    assert json.loads(mismatch.stdout)["agreement"] is False

    changed_state = dict(base)
    changed_state["runtime_log_checkpoint"] = {
        "segment_sha256": "e" * 64,
        "routine_trace_sha256": "f" * 64,
    }
    receipt_b.write_text(json.dumps(changed_state), encoding="utf-8")
    state_mismatch = subprocess.run(
        [str(PYTHON), str(TOOL), "compare", str(receipt_a), str(receipt_b)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert state_mismatch.returncode == 1
    assert "runtime log segment differs" in state_mismatch.stdout

    missing_state_digest = dict(base)
    missing_state_digest["runtime_log_checkpoint"] = {}
    receipt_b.write_text(json.dumps(missing_state_digest), encoding="utf-8")
    invalid_state = subprocess.run(
        [str(PYTHON), str(TOOL), "compare", str(receipt_a), str(receipt_b)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert invalid_state.returncode == 1
    assert "invalid runtime log segment digest" in invalid_state.stdout

    legacy = dict(base)
    legacy.pop("events_delivered")
    legacy.pop("target_echo_verified")
    receipt_b.write_text(json.dumps(legacy), encoding="utf-8")
    unverified = subprocess.run(
        [str(PYTHON), str(TOOL), "compare", str(receipt_a), str(receipt_b)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert unverified.returncode == 1
    assert "no accepted target echo" in json.loads(unverified.stdout)["reasons"][1]

    one = subprocess.run(
        [str(PYTHON), str(TOOL), "compare", str(receipt_a)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert one.returncode == 3
    assert json.loads(one.stdout)["reason"] == "receipt_count"
