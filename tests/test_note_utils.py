from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from note_utils import next_dated_id, slug, write_new


def test_slug_is_stable_and_safe():
    assert slug("Reads level records?") == "reads-level-records"


def test_write_new_never_overwrites(tmp_path):
    target = tmp_path / "note.md"
    write_new(target, "first")
    with pytest.raises(SystemExit):
        write_new(target, "second")
    assert target.read_text() == "first\n"


def test_next_id_advances_existing_ids(tmp_path):
    note = tmp_path / "one.md"
    from note_utils import now
    day = now().strftime("%Y%m%d")
    note.write_text(f"---\nid: EXP-{day}-007\n---\n")
    assert next_dated_id("EXP", tmp_path) == f"EXP-{day}-008"
