"""Guard the exact visual companion, using the previously tested mesh writer."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("floor_visual", ROOT / "scripts/terrain-floor-visual-fixture.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def test_unpinned_bytes_rejected():
    with pytest.raises(probe.DatFormatError, match="pinned"):
        probe.fixture(b"wrong source")


def test_output_must_stay_under_work_copies(tmp_path):
    with pytest.raises(probe.DatFormatError, match="work/copies"):
        probe.write_fixture(tmp_path / "LEVEL.DAT", b"")


def test_exact_visual_fixture_preserves_every_other_field():
    if not probe.SOURCE.exists():
        pytest.skip("retail work copy unavailable")
    raw = probe.SOURCE.read_bytes()
    changed, edits = probe.fixture(raw)
    assert len(edits) == 17
    assert len(raw) == len(changed)
    allowed = {e["field_offset"] + d for e in edits for d in (0, 1)}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(raw, changed, strict=True)))
    restored = changed
    for e in edits:
        restored = probe.LevelDat.parse(restored).set_static_mesh_vertex_component(
            e["section"], e["record"], e["vertex"], 2, e["new"], e["old"])
    assert restored == raw
    with pytest.raises(probe.DatFormatError, match="pinned"):
        probe.fixture(changed)
