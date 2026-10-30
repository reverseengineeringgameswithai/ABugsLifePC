from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402

# Reuse the synthetic ELF core builder from the evidence_lib tests.
from test_evidence_lib import build_core  # noqa: E402


def _load_core_grep():
    spec = importlib.util.spec_from_file_location("core_grep", SCRIPTS / "core-grep.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core_grep = _load_core_grep()


def test_finds_dword_with_correct_vaddr() -> None:
    payload = b"\xaa\xbb\xcc\xdd" + b"\x11\x22\x33\x44" + b"\xee" * 8
    core = build_core(segments=((0x00400000, payload, 0x6),))
    result = core_grep.scan_core(core, (0x44332211).to_bytes(4, "little"))
    assert result["match_count"] == 1
    # The dword sits at offset 4 in the segment starting at 0x00400000.
    assert result["matches"][0]["vaddr"] == "0x400004"
    assert result["matches"][0]["p_flags"] == "rw-"


def test_two_segments_report_distinct_vaddrs() -> None:
    core = build_core(segments=(
        (0x00400000, b"\x99\x99\x99\x99AAAA", 0x5),
        (0x005AA000, b"BBBB\x99\x99\x99\x99", 0x6),
    ))
    result = core_grep.scan_core(core, b"\x99\x99\x99\x99")
    vaddrs = {m["vaddr"] for m in result["matches"]}
    assert vaddrs == {"0x400000", "0x5aa004"}


def test_match_spanning_chunk_boundary() -> None:
    # Pattern straddles a small chunk boundary; overlap handling must find it.
    payload = b"\x00" * 6 + b"\xde\xad\xbe\xef" + b"\x00" * 6
    core = build_core(segments=((0x00400000, payload, 0x6),))
    result = core_grep.scan_core(
        core, b"\xde\xad\xbe\xef", chunk_size=8
    )
    assert result["match_count"] == 1
    assert result["matches"][0]["vaddr"] == "0x400006"


def test_no_match_returns_empty() -> None:
    core = build_core(segments=((0x00400000, b"AAAABBBB", 0x6),))
    result = core_grep.scan_core(core, b"\xff\xff\xff\xff")
    assert result["match_count"] == 0


def test_truncated_segment_reported() -> None:
    core = build_core(segments=((0x00400000, b"ABCDEFGH", 0x6),), truncate=3)
    result = core_grep.scan_core(core, b"ABCD")
    assert result["truncated_segments"] == [0]
    assert result["match_count"] == 1


def test_max_matches_caps() -> None:
    payload = b"\x99\x99" * 100
    core = build_core(segments=((0x00400000, payload, 0x6),))
    result = core_grep.scan_core(core, b"\x99\x99", max_matches=5)
    assert result["match_count"] == 5
    assert result["capped"] is True


def test_rejects_non_core_via_cli(tmp_path: Path) -> None:
    bad = tmp_path / "not.core"
    bad.write_bytes(b"\x7fELF" + b"\x00" * 200)  # class byte 0 → unsupported
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "core-grep.py"), str(bad), "--dword", "0x1"],
        capture_output=True, text=True,
    )
    assert result.returncode == ev.EXIT_USAGE
    payload = json.loads(result.stdout)
    assert payload["error"] in ("elf", "usage")


def test_cli_exit_codes(tmp_path: Path) -> None:
    payload = b"\x11\x22\x33\x44" + b"\x00" * 8
    core = build_core(segments=((0x00400000, payload, 0x6),))
    core_path = tmp_path / "test.core"
    core_path.write_bytes(core)

    found = subprocess.run(
        [sys.executable, str(SCRIPTS / "core-grep.py"), str(core_path),
         "--dword", "0x44332211"],
        capture_output=True, text=True,
    )
    assert found.returncode == ev.EXIT_OK

    missing = subprocess.run(
        [sys.executable, str(SCRIPTS / "core-grep.py"), str(core_path),
         "--dword", "0xdeadbeef"],
        capture_output=True, text=True,
    )
    assert missing.returncode == ev.EXIT_TOOL_NEGATIVE


@pytest.mark.parametrize("bad", ["abc", "gg", "0x1"])
def test_rejects_bad_hex(bad: str, tmp_path: Path) -> None:
    core = build_core()
    core_path = tmp_path / "c.core"
    core_path.write_bytes(core)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "core-grep.py"), str(core_path), "--hex", bad],
        capture_output=True, text=True,
    )
    assert result.returncode == ev.EXIT_USAGE
