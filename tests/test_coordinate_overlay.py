from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import struct
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "coordinate-overlay.py"
PYTHON = ROOT / ".venv" / "bin" / "python"


def _load_module():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("ablpc_coordinate_overlay", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


overlay = _load_module()


class FakeMemory:
    def __init__(self, *, collision_index: int = 571) -> None:
        self.collision_index = collision_index
        self.calls: list[tuple[tuple[int, int], ...]] = []

    def read_many(self, requests):
        plan = tuple(requests)
        self.calls.append(plan)
        if len(self.calls) == 1:
            assert plan == (
                (overlay.XYZ_ADDRESS, 12),
                (overlay.FLAGS_ADDRESS, 2),
                (overlay.NEXT_LIFE_ADDRESS, 2),
                (overlay.STATE_COUNTER_ADDRESS, 2),
                (overlay.LEVEL_ADDRESS, 4),
                (overlay.COLLISION_INDEX_ADDRESS, 4),
            )
            return (
                struct.pack("<iii", 471712, -1234, 537728),
                struct.pack("<H", 0x18),
                struct.pack("<H", 2),
                struct.pack("<h", -3),
                struct.pack("<i", 3),
                struct.pack("<i", self.collision_index),
            )
        expected = (
            overlay.COLLISION_TABLE_ADDRESS
            + self.collision_index * overlay.COLLISION_STRIDE
            + overlay.COLLISION_MATERIAL_OFFSET
        )
        assert plan == ((expected, 2),)
        return (struct.pack("<h", 1),)


def test_coordinate_sample_decodes_signed_pc_fields_and_collision_value() -> None:
    assert overlay.XYZ_ADDRESS == 0x0059D910
    memory = FakeMemory()
    sample = overlay.read_coordinate_sample(memory, monotonic_ns=lambda: 123456)
    assert sample == overlay.CoordinateSample(
        x=471712,
        y=-1234,
        z=537728,
        level=3,
        flags=0x18,
        next_life=2,
        state_counter=-3,
        collision_index=571,
        collision_material=1,
        sampled_ns=123456,
    )
    assert sample.coordinate_text() == "X    471712\nY     -1234\nZ    537728"
    assert "FLAGS 0x0018" in sample.detail_text()
    assert "COLLISION  571   VALUE 1" in sample.detail_text()


def test_coordinate_sample_rejects_impossible_collision_index_without_second_read() -> None:
    memory = FakeMemory(collision_index=5000)
    sample = overlay.read_coordinate_sample(memory, monotonic_ns=lambda: 1)
    assert sample.collision_index == 5000
    assert sample.collision_material is None
    assert len(memory.calls) == 1


def test_proc_stat_identity_handles_spaces_parentheses_and_required_fields() -> None:
    tail = ["S", "1", "456"] + ["0"] * 16 + ["987654"]
    raw = "123 (odd name) here) " + " ".join(tail)
    assert overlay._proc_stat_identity(raw) == (456, 987654)
    with pytest.raises(overlay.OverlayError, match="malformed"):
        overlay._proc_stat_identity("123 malformed")


def test_overlay_argument_bounds_fail_closed() -> None:
    assert overlay._opacity("0.78") == 0.78
    assert overlay._interval("100") == 100
    with pytest.raises(Exception):
        overlay._opacity("0.1")
    with pytest.raises(Exception):
        overlay._interval("5")


def test_overlay_capabilities_declare_read_only_scope() -> None:
    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), "--capabilities"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["read_backend"] == "process_vm_readv"
    assert payload["writes_target_memory"] is False
    assert payload["attaches_debugger"] is False
    assert payload["pauses_target"] is False
    assert payload["sets_breakpoints"] is False
    assert payload["modes"] == ["overlay", "window"]
    assert payload["coordinate_address"] == "0x0059D910"
    assert payload["coordinate_evidence"] == "EXP-20260815-128"
    assert payload["default_readout"] == ["actor_x", "actor_y", "actor_z"]
    assert payload["overlay"]["target_display_aware"] is True
    assert payload["overlay"]["gamescope_external_overlay_atom"] is True
    assert payload["overlay"]["click_through"] is False


def test_gamescope_property_targets_tk_child_and_mapped_top_level(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeRoot:
        @staticmethod
        def winfo_id() -> int:
            return 101

    window = object.__new__(overlay.CoordinateWindow)
    window.root = FakeRoot()
    calls: list[list[str]] = []

    def fake_run(command, **_kwargs):
        calls.append(command)
        if command[0] == "/tools/xdotool":
            return subprocess.CompletedProcess(command, 0, "202\n", "")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setenv("DISPLAY", ":2")
    monkeypatch.setattr(overlay.shutil, "which", lambda name: f"/tools/{name}")
    monkeypatch.setattr(overlay.subprocess, "run", fake_run)

    window.set_x11_cardinal("GAMESCOPE_EXTERNAL_OVERLAY", 1)

    assert calls[0][0] == "/tools/xdotool"
    assert [call[call.index("-id") + 1] for call in calls[1:]] == ["101", "202"]


# --- EXP-20260815-139 nearest grain-gate readout ---------------------------

TUNNELS_RETAIL_ROWS = (
    # (type, unknown, requirement, x, z) — EXP-20260815-136 resident table.
    (0x10C7, 26, 20, 193754, 131692),
    (0x10C7, 23, 10, 505642, -451306),
    (0x10C7, 24, 10, 832302, 291075),
    (0x10C7, 22, 10, 509676, 510143),
    (0x10C7, 25, 20, 833246, 612273),
    (0x10C7, 21, 20, 1142934, 1308289),
    (0x10C7, 28, 30, 1471643, 1410369),
    (0x10C7, 20, 10, 1202034, 1986285),
    (0x10C7, 27, 30, 1634925, 2534812),
)


def _coordinate_sample(x: int, z: int, level: int) -> "overlay.CoordinateSample":
    return overlay.CoordinateSample(
        x=x,
        y=0,
        z=z,
        level=level,
        flags=0,
        next_life=0,
        state_counter=0,
        collision_index=5000,
        collision_material=None,
        sampled_ns=0,
    )


class FakeGateMemory:
    def __init__(self, payloads: dict[tuple[int, int], bytes]) -> None:
        self.payloads = payloads
        self.calls: list[tuple[tuple[int, int], ...]] = []

    def read_many(self, requests):
        plan = tuple(requests)
        self.calls.append(plan)
        return tuple(self.payloads[request] for request in plan)


def test_gate_geometry_constants_pin_exp_139_static_extraction() -> None:
    assert overlay.TUNNELS_GATE_TABLE_ADDRESS == 0x004DA9C8
    assert overlay.TUNNELS_OPEN_DISTANCE_SQ == 0x2710
    assert overlay.TUNNELS_MESSAGE_DISTANCE_SQ == 0x640
    assert overlay.CITY_GATE_STATE_ADDRESS == 0x0059F020
    assert overlay.CITY_REQUIREMENT_TABLE_ADDRESS == 0x004338B0
    assert overlay.CITY_GATES == (
        (-71129, -184314, 80),
        (354031, 35256, 90),
        (582271, 310212, 100),
    )
    assert overlay.CITY_RETAIL_REQUIREMENTS == (10, 20, 30)


def test_engine_distance_reproduces_accepted_exp_137_boundary_points() -> None:
    # Tunnels row 3 from the EXP-130/137 known walkable point.
    row3 = overlay.engine_gate_distance_sq(501696, 494016, 509676, 510143)
    assert row3 == (-32) ** 2 + (-63) ** 2 == 4993
    assert row3 < overlay.TUNNELS_OPEN_DISTANCE_SQ
    assert row3 >= overlay.TUNNELS_MESSAGE_DISTANCE_SQ
    # City gate 0: accepted trigger point is inside r=80, the saved
    # ordinarily-reached approach point is outside — matching EXP-137.
    trigger = overlay.engine_gate_distance_sq(-87622, -182181, -71129, -184314)
    approach = overlay.engine_gate_distance_sq(-92603, -181281, -71129, -184314)
    assert trigger == (-65) ** 2 + 8**2 == 4289
    assert approach == (-84) ** 2 + 11**2 == 7177
    assert trigger < 80 * 80 <= approach


def test_nearest_tunnels_row_uses_one_table_read_and_live_values() -> None:
    table = b"".join(struct.pack("<5i", *row) for row in TUNNELS_RETAIL_ROWS)
    memory = FakeGateMemory({(overlay.TUNNELS_GATE_TABLE_ADDRESS, 180): table})
    sample = _coordinate_sample(501696, 494016, overlay.TUNNELS_INTERNAL_LEVEL)
    gate = overlay.read_nearest_gate(memory, sample, (None, None, None))
    assert memory.calls == [((overlay.TUNNELS_GATE_TABLE_ADDRESS, 180),)]
    assert gate is not None
    assert (gate.kind, gate.index, gate.requirement) == ("T", 3, 10)
    assert gate.status == 0x10C7
    assert gate.distance_sq == 4993 and gate.threshold_sq == 0x2710
    assert gate.inside is True
    assert gate.world_radius == 25600
    assert gate.world_distance == math.isqrt(7980**2 + 16127**2)
    assert "GATE T3   REQ 10   TYPE 0x10C7" in gate.gate_text()
    assert "IN" in gate.gate_text()


def test_nearest_city_gate_reads_state_and_flags_trigger_boundary() -> None:
    states = struct.pack("<iii", -1, -1, -1)
    memory = FakeGateMemory({(overlay.CITY_GATE_STATE_ADDRESS, 12): states})
    inside = overlay.read_nearest_gate(
        memory,
        _coordinate_sample(-87622, -182181, overlay.CITY_INTERNAL_LEVEL),
        overlay.CITY_RETAIL_REQUIREMENTS,
    )
    assert memory.calls == [((overlay.CITY_GATE_STATE_ADDRESS, 12),)]
    assert inside is not None
    assert (inside.kind, inside.index, inside.requirement) == ("C", 0, 10)
    assert inside.status == -1
    assert inside.distance_sq == 4289 and inside.threshold_sq == 6400
    assert inside.inside is True and inside.world_radius == 20480
    outside = overlay.read_nearest_gate(
        memory,
        _coordinate_sample(-92603, -181281, overlay.CITY_INTERNAL_LEVEL),
        overlay.CITY_RETAIL_REQUIREMENTS,
    )
    assert outside is not None and outside.index == 0
    assert outside.inside is False
    assert "STATE -1" in outside.gate_text() and "out" in outside.gate_text()


def test_gate_readout_reads_nothing_outside_levels_three_and_four() -> None:
    memory = FakeGateMemory({})
    sample = _coordinate_sample(0, 0, 0)
    assert overlay.read_nearest_gate(memory, sample, (None, None, None)) is None
    assert memory.calls == []


def test_city_requirements_come_from_formula_or_profile_lookup_only() -> None:
    memory = FakeGateMemory(
        {(overlay.CITY_REQUIREMENT_TABLE_ADDRESS, 12): struct.pack("<iii", 1, 2, 3)}
    )
    assert overlay.resolve_city_requirements(
        memory, overlay.KNOWN_RETAIL_SHA256.upper()
    ) == (10, 20, 30)
    assert memory.calls == []
    assert overlay.resolve_city_requirements(
        memory, overlay.KNOWN_GRAIN_GATES_PROFILE_SHA256
    ) == (1, 2, 3)
    assert memory.calls == [((overlay.CITY_REQUIREMENT_TABLE_ADDRESS, 12),)]
    assert overlay.resolve_city_requirements(memory, "ab" * 32) == (None, None, None)
    assert len(memory.calls) == 1


def test_identity_boundary_is_exactly_retail_plus_accepted_profile() -> None:
    assert overlay.ALLOWED_EXECUTABLE_SHA256S == frozenset(
        {
            "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
            "69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b",
        }
    )


def test_capabilities_declare_gate_readout_and_two_hash_boundary() -> None:
    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), "--capabilities"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["tool_version"] == "1.3.0"
    assert payload["writes_target_memory"] is False
    assert payload["nearest_gate_readout_opt_in"] is True
    assert payload["gate_geometry_evidence"] == "EXP-20260815-139"
    assert sorted(payload["allowed_executable_sha256s"]) == sorted(
        overlay.ALLOWED_EXECUTABLE_SHA256S
    )
    assert "nearest_grain_gate" in payload["fields"]
