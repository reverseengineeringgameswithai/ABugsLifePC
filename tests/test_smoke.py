from __future__ import annotations

from pathlib import Path

import pytest

from reimplementation.ablpc.smoke import (
    SmokeError,
    _launcher_dry_run,
    _tree_inventory,
    _validated_game_root,
)


EXE_SHA256 = "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"


def test_tree_inventory_detects_exact_change_and_links(tmp_path: Path) -> None:
    root = tmp_path / "tree"
    (root / "CD").mkdir(parents=True)
    target = root / "CD" / "LEVEL.DAT"
    target.write_bytes(b"one")
    before = _tree_inventory(root)
    target.write_bytes(b"two")
    assert _tree_inventory(root) != before
    (root / "link").symlink_to(target)
    with pytest.raises(SmokeError, match="symbolic link"):
        _tree_inventory(root)


def test_validated_game_root_requires_work_copy_descendant(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    game = repo / "work" / "copies" / "game"
    game.mkdir(parents=True)
    assert _validated_game_root(repo, game) == game.resolve()
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(SmokeError, match="must be below"):
        _validated_game_root(repo, outside)


def test_launcher_dry_run_requires_all_contract_markers(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    launcher = scripts / "play-pristine.sh"
    launcher.write_text(
        "#!/bin/sh\n"
        f"echo 'Verified bugs.exe: {EXE_SHA256}'\n"
        "echo 'At the renderer selector, press Down once'\n"
        "echo 'gamescope -w 640 -h 480 -S fit -F nearest'\n"
        "echo 'PULSE_SINK=ablpc_mute_123 wine ./bugs.exe log cheat mpeg'\n",
        encoding="utf-8",
    )
    launcher.chmod(0o755)
    result = _launcher_dry_run(repo, tmp_path / "game", tmp_path / "prefix", EXE_SHA256)
    assert result["validated"] is True

    launcher.write_text("#!/bin/sh\necho incomplete\n", encoding="utf-8")
    with pytest.raises(SmokeError, match="lacks required markers"):
        _launcher_dry_run(repo, tmp_path / "game", tmp_path / "prefix", EXE_SHA256)
