from __future__ import annotations

from pathlib import Path
import struct

import pytest

from reimplementation.ablpc import flik_animation as fa
from reimplementation.ablpc.anm import AnmFile


ROOT = Path(__file__).resolve().parents[1]
CD = ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD'
EXE = ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe'


def memory(blobs: dict[int, bytes]):
    """A bounds-checked read(va, size) over synthetic blobs."""
    def read(va, size):
        for base, blob in blobs.items():
            if base <= va and va+size <= base+len(blob):
                return blob[va-base:va-base+size]
        raise fa.FlikAnimationError(f'{va:#x} unmapped')
    return read


def test_script_end_keeps_frames_and_footstep_events() -> None:
    script = fa.decode_script(memory({0x1000: bytes([0, 0x82, 2, 0x91, 0xFE])}), 0x1000)
    assert script.frames == (0, 2, 2, 0x11)
    assert script.events == ((1, 'left_step'), (3, 'right_step'))
    assert (script.end, script.loop_to, script.loop_steps) == ('end', None, 0)


@pytest.mark.parametrize(('back', 'loop_to'), [(4, 0), (1, 3)])
def test_script_loop_returns_to_the_named_step(back: int, loop_to: int) -> None:
    script = fa.decode_script(memory({0x1000: bytes([0, 1, 2, 3, 0xFF, back])}), 0x1000)
    assert script.frames == (0, 1, 2, 3)
    assert (script.end, script.loop_to, script.loop_steps) == ('loop', loop_to, 4-loop_to)


@pytest.mark.parametrize('raw', [bytes([0, 1, 0xFF, 3]), bytes([0, 1, 0xFF, 0])])
def test_script_rejects_a_loop_outside_the_script(raw: bytes) -> None:
    with pytest.raises(fa.FlikAnimationError, match='loops'):
        fa.decode_script(memory({0x1000: raw}), 0x1000)


def test_script_rejects_a_missing_terminator() -> None:
    with pytest.raises(fa.FlikAnimationError, match='no terminator'):
        fa.decode_script(memory({0x1000: bytes(fa.SCRIPT_LIMIT)}), 0x1000)
    with pytest.raises(fa.FlikAnimationError, match='unmapped'):
        fa.decode_script(memory({0x1000: bytes(8)}), 0x1000)


def synthetic_table(rows, end=b'\xff'*4):
    table = b''.join(struct.pack('<IiiiI', *row) for row in rows)
    return memory({fa.STATE_TABLE_VA: table+end, 0x2000: bytes([0, 1, 2, 0xFF, 3])})


def test_state_table_reads_every_row_and_its_end_word() -> None:
    rows = [(0x2000, i % 3, (i+1) % 3, -0x30 if i == 0 else 0x10000, i % 2)
            for i in range(fa.STATE_COUNT)]
    states = fa.state_table(synthetic_table(rows))
    assert len(states) == fa.STATE_COUNT
    assert (states[0].slot_a, states[0].slot_b, states[0].speed) == (0, 1, -0x30)
    assert states[1].idle_family and not states[0].idle_family
    with pytest.raises(fa.FlikAnimationError, match='0xFFFFFFFF'):
        fa.state_table(synthetic_table(rows, end=b'\0'*4))
    rows[3] = (0x2000, 0, 0, 0, 2)
    with pytest.raises(fa.FlikAnimationError, match='idle flag'):
        fa.state_table(synthetic_table(rows))


def anm_with_frames(*frame_counts: int | None) -> AnmFile:
    blobs, offsets, cursor = b'', [], 8+4*len(frame_counts)
    for slot, frames in enumerate(frame_counts):
        if frames is None:
            offsets.append(0)
            continue
        record = struct.pack('<6H', slot, frames, 1, 6, 1, 2) + struct.pack('<h', 0) + bytes(2)
        record += bytes(frames*12)
        offsets.append(cursor)
        blobs += record
        cursor += len(record)
    head = struct.pack('<HhHH', 0, len(frame_counts), 0, 0)
    return AnmFile.parse(head+struct.pack(f'<{len(offsets)}I', *offsets)+blobs)


def test_check_slots_notes_absent_slots_and_rejects_overruns() -> None:
    script = fa.Script(0, b'', (0, 3), (), 'loop', 0)
    records = anm_with_frames(4, None, 3).records()
    fine = fa.ActionState(0, script, 0, 0, 0x10000, False)
    absent = fa.ActionState(1, script, 1, 1, 0x10000, False)
    assert fa.check_slots([fine, absent], records) == ['state 0x1 names absent slot 1']
    with pytest.raises(fa.FlikAnimationError, match='exceeds slot 2'):
        fa.check_slots([fa.ActionState(2, script, 0, 2, 0x10000, False)], records)
    with pytest.raises(fa.FlikAnimationError, match='names slot 9'):
        fa.check_slots([fa.ActionState(3, script, 9, 9, 0x10000, False)], records)


def test_labels_need_one_row_with_status_and_evidence_per_state(tmp_path: Path) -> None:
    rows = [{'state': i, 'status': 'unknown', 'evidence': ['x']} for i in range(fa.STATE_COUNT)]
    path = tmp_path/'labels.json'

    def check(data):
        path.write_text(__import__('json').dumps(data))
        return fa.labels(path)

    assert check({'schema': fa.LABEL_SCHEMA, 'states': rows})
    with pytest.raises(fa.FlikAnimationError, match='Unsupported'):
        check({'schema': 'other', 'states': rows})
    with pytest.raises(fa.FlikAnimationError, match='Every state'):
        check({'schema': fa.LABEL_SCHEMA, 'states': rows[:-1]})
    with pytest.raises(fa.FlikAnimationError, match='lacks status'):
        check({'schema': fa.LABEL_SCHEMA, 'states': rows[:-1]+[{'state': 34, 'status': 'maybe', 'evidence': ['x']}]})


def test_committed_labels_cover_every_state() -> None:
    data = fa.labels()
    assert {row['state'] for row in data['states']} == set(range(fa.STATE_COUNT))
    assert {row['slot'] for row in data['slots']} == set(range(40))


def test_retail_catalog_matches_the_evidenced_layout() -> None:
    if not (EXE.exists() and (CD/'CHARS/FLICK.ANM').exists()):
        pytest.skip('Private retail work copy absent')
    catalog = fa.catalog(EXE.read_bytes(), (CD/'CHARS/FLICK.ANM').read_bytes(),
                         variant_rows=fa.variants(CD))
    slots = {row['slot']: row for row in catalog['slots']}
    states = {row['state']: row for row in catalog['states']}
    assert not slots[26]['present'] and slots[26]['used_by'] == ['state 0x20 layer A']
    assert slots[7]['used_by'] == slots[12]['used_by'] == []
    assert (slots[0]['layer'], slots[1]['layer'], slots[2]['layer']) == ('upper', 'lower', 'upper')
    assert states[0x16]['idle_family'] and states[0x16]['slot_a'] == 4
    assert states[0]['footstep_events'] == [{'step': 2, 'side': 'left'+'_step'},
                                            {'step': 10, 'side': 'right_step'}]
    assert all(not row['frame_count_mismatches'] for row in catalog['model_variants'])
    assert catalog['model_variants'][2]['absent_slots'] == [26, 30, 31, 37]


def test_retail_non_player_models_are_fully_labelled() -> None:
    if not (CD/'CHARS3/FLIKHARV.ANM').exists():
        pytest.skip('Private retail work copy absent')
    models = {row['path']: row for row in fa.other_models(CD)}
    harvester, stand_in = models['CHARS3/FLIKHARV.ANM'], models['CHARS2/ATTAFLIK.ANM']
    assert (harvester['entity_type'], stand_in['entity_type']) == (0x23, 0x15)
    assert [s['frames'] for s in harvester['slots']] == [24, 12, 6]
    assert [s['frames'] for s in stand_in['slots']] == [12, 28, 18, 32]
    assert all(s.get('name') and s.get('status') for m in models.values() for s in m['slots'])


def test_non_player_labels_must_name_existing_slots(tmp_path: Path) -> None:
    if not (CD/'CHARS3/FLIKHARV.ANM').exists():
        pytest.skip('Private retail work copy absent')
    data = fa.labels()
    data['other_models'][0]['slots'].append(
        {'slot': 9, 'name': 'x', 'status': 'unknown', 'evidence': ['x']})
    with pytest.raises(fa.FlikAnimationError, match='does not have'):
        fa.other_models(CD, data)
