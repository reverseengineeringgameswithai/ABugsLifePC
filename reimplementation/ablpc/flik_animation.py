"""Flik's animation catalogue: ANM slots joined to the native action states.

Reads two inputs and never edits either:

* ``CHARS/FLICK.ANM`` through :mod:`.anm` (records as read by 0x00445FF0);
* the retail ``bugs.exe`` action-state table that 0x00402DC0 indexes with
  Flik's state word 0x0059D998: 35 rows of 20 bytes at 0x004C1CE8, each
  ``{frame-script pointer, ANM slot A, ANM slot B, speed, idle-family flag}``,
  followed by a 0xFFFFFFFF word and three 8-entry idle-fidget tables.

Authored meanings live in ``config/animation/pc-flik-animations.json``; every
label there carries its own status and evidence. This module validates that
file against the binary rather than trusting it.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import struct

import pefile

from .anm import AnmFile, AnmRecord


RETAIL_SHA256 = '97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878'
FLICK_ANM_SHA256 = '1743b26a13770b6453dfcf900d9f02a515e52a1b04e5679149c06ec77e5e8ab1'
IMAGE_BASE = 0x400000
STATE_TABLE_VA = 0x004C1CE8
STATE_STRIDE = 20
STATE_COUNT = 35
STATE_TABLE_END_VA = STATE_TABLE_VA + STATE_COUNT * STATE_STRIDE  # holds 0xFFFFFFFF
IDLE_TABLES = {  # VA -> 0x00861C84 values that select it in 0x00402DC0
    0x004C1FA8: 'default',
    0x004C1FB8: (6, 10, 11, 15),
    0x004C1FC8: (4, 5),
}
IDLE_STATE = 0x16
IDLE_PICK_FRAME = 11  # 0x00402DC0 rolls a fidget when state 0x16 is at 0xB0000
THROW_OVERLAY = {'layered': 2, 'idle': 11, 'slot16': 23}
THROW_FRAMES = 0x12
AIM_SLOT = 32  # header +0x88, sampled while 0x0059D99C is nonzero
SCRIPT_LIMIT = 256
LEFT_STEP_EVENTS = (0x82, 0x83, 0x85)  # dust beside heading-0x400, sound 0
RIGHT_STEP_EVENTS = (0x87, 0x8A, 0x91)  # dust beside heading+0x400, sound 1
LOOP, END = 0xFF, 0xFE
LABELS_PATH = Path(__file__).resolve().parents[2]/'config/animation/pc-flik-animations.json'
LABEL_SCHEMA = 'ablpc.flik-animations.v1'
STATUSES = ('confirmed', 'inferred', 'unknown')


class FlikAnimationError(ValueError):
    """Raised when an input does not match the evidenced retail layout."""


@dataclass(frozen=True)
class Script:
    va: int
    raw: bytes
    frames: tuple[int, ...]  # ANM frame per step (low seven bits)
    events: tuple[tuple[int, str], ...]  # (step, 'left_step' | 'right_step')
    end: str  # 'loop' or 'end'
    loop_to: int | None  # step that 0xFF NN returns to

    @property
    def loop_steps(self) -> int:
        return len(self.frames) - (self.loop_to or 0) if self.end == 'loop' else 0


@dataclass(frozen=True)
class ActionState:
    index: int
    script: Script
    slot_a: int
    slot_b: int
    speed: int  # 16.16 per update; negative scales with ground speed 0x0059D948
    idle_family: bool


def decode_script(read, va: int) -> Script:
    """Decode a frame script with the 0x00402DC0 rules, bounded to 256 bytes."""
    raw = bytearray()
    while len(raw) < SCRIPT_LIMIT:
        byte = read(va+len(raw), 1)[0]
        raw.append(byte)
        if byte == END:
            frames = tuple(b & 0x7F for b in raw[:-1])
            return Script(va, bytes(raw), frames, _events(raw[:-1]), 'end', None)
        if byte == LOOP:
            back = read(va+len(raw), 1)[0]
            raw.append(back)
            steps = len(raw)-2
            if not 0 < back <= steps:
                raise FlikAnimationError(f'Script {va:#x} loops {back} back from step {steps}')
            if raw[steps-back] in (LOOP, END):
                raise FlikAnimationError(f'Script {va:#x} loops onto a control byte')
            frames = tuple(b & 0x7F for b in raw[:-2])
            return Script(va, bytes(raw), frames, _events(raw[:-2]), 'loop', steps-back)
    raise FlikAnimationError(f'Script {va:#x} has no terminator within {SCRIPT_LIMIT} bytes')


def _events(steps: bytes) -> tuple[tuple[int, str], ...]:
    return tuple((i, 'left_step' if b in LEFT_STEP_EVENTS else 'right_step')
                 for i, b in enumerate(steps) if b in LEFT_STEP_EVENTS+RIGHT_STEP_EVENTS)


def read_executable(data: bytes):
    """Return a bounds-checked ``read(va, size)`` over the retail executable."""
    if hashlib.sha256(data).hexdigest() != RETAIL_SHA256:
        raise FlikAnimationError('The state table is only evidenced for the retail executable')
    pe = pefile.PE(data=data, fast_load=True)
    if pe.OPTIONAL_HEADER.ImageBase != IMAGE_BASE:
        raise FlikAnimationError('Unexpected image base')

    def read(va, size):
        section = pe.get_section_by_rva(va-IMAGE_BASE)
        if section is None or va-IMAGE_BASE+size > section.VirtualAddress+section.SizeOfRawData:
            raise FlikAnimationError(f'{va:#x}+{size} is outside initialised section data')
        return pe.get_data(va-IMAGE_BASE, size)
    return read


def state_table(read) -> tuple[ActionState, ...]:
    states = []
    for index in range(STATE_COUNT):
        script_va, slot_a, slot_b, speed, flag = struct.unpack(
            '<IiiiI', read(STATE_TABLE_VA+index*STATE_STRIDE, STATE_STRIDE))
        if flag not in (0, 1):
            raise FlikAnimationError(f'State {index:#x} idle flag {flag}')
        states.append(ActionState(index, decode_script(read, script_va), slot_a, slot_b,
                                  speed, bool(flag)))
    if read(STATE_TABLE_END_VA, 4) != b'\xff'*4:
        raise FlikAnimationError('State table is not followed by its 0xFFFFFFFF word')
    return tuple(states)


def idle_tables(read) -> dict[int, tuple[int, ...]]:
    tables = {va: struct.unpack('<8H', read(va, 16)) for va in IDLE_TABLES}
    if any(not 0 <= s < STATE_COUNT for t in tables.values() for s in t):
        raise FlikAnimationError('Idle table names a state outside the table')
    return tables


def check_slots(states, records: tuple[AnmRecord | None, ...]) -> list[str]:
    """Return script/slot mismatches; raise on anything the sampler would misread."""
    notes = []
    for state in states:
        for slot in {state.slot_a, state.slot_b}:
            if not 0 <= slot < len(records):
                raise FlikAnimationError(f'State {state.index:#x} names slot {slot}')
            if records[slot] is None:
                notes.append(f'state {state.index:#x} names absent slot {slot}')
                continue
            if max(state.script.frames) >= records[slot].frame_count:
                raise FlikAnimationError(
                    f'State {state.index:#x} frame {max(state.script.frames)} exceeds slot '
                    f'{slot} ({records[slot].frame_count} frames)')
    return notes


MODEL_PATHS = {  # 0x00445020 resource-ID-0 arms, selected by 0x00861C84
    'CHARS/FLICK.ANM': 'default',
    'CHARS3/FLICKD.ANM': (2, 3),
    'CHARS4/FLICKP.ANM': (4, 5),
    'CHARS3/FLICKP.ANM': (6, 10, 11, 14),
}


def variants(cd_root: Path) -> list[dict]:
    """Compare every player-model ANM with FLICK.ANM slot for slot."""
    base = AnmFile.from_path(cd_root/'CHARS/FLICK.ANM').records()
    rows = []
    for rel, levels in MODEL_PATHS.items():
        anm = AnmFile.from_path(cd_root/rel)
        records = anm.records()
        if len(records) != len(base):
            raise FlikAnimationError(f'{rel} has {len(records)} slots, FLICK has {len(base)}')
        mismatched = [i for i, (r, b) in enumerate(zip(records, base))
                      if r and b and r.frame_count != b.frame_count]
        present = [r for r in records if r]
        rows.append({
            'path': rel, 'sha256': anm.sha256, 'selected_by_0x00861C84': levels,
            'absent_slots': [i for i, r in enumerate(records) if r is None],
            'part_counts': sorted({r.part_count for r in present}),
            'words_per_frame': sorted({r.words_per_frame for r in present}),
            'frame_count_mismatches': mismatched,
        })
    return rows


OTHER_MODELS = {  # non-player Flik models, sampled per entity by 0x00448569
    'CHARS3/FLIKHARV.ANM': 0x23,
    'CHARS2/ATTAFLIK.ANM': 0x15,
}


def other_models(cd_root: Path, label_data: dict | None = None) -> list[dict]:
    """List the entity-driven Flik models' slots with their authored labels."""
    label_data = labels() if label_data is None else label_data
    authored = {row['path']: row for row in label_data.get('other_models', [])}
    rows = []
    for rel, entity_type in OTHER_MODELS.items():
        anm = AnmFile.from_path(cd_root/rel)
        label = authored.get(rel, {})
        slot_labels = {row['slot']: row for row in label.get('slots', [])}
        records = anm.records()
        if any(not 0 <= s < len(records) or records[s] is None for s in slot_labels):
            raise FlikAnimationError(f'{rel} labels a slot the file does not have')
        slots = []
        for slot, record in enumerate(records):
            row = {'slot': slot, 'present': record is not None}
            if record is not None:
                row.update(frames=record.frame_count, part_count=record.part_count,
                           seconds_at_30=round(record.frame_count/30, 3))
            row.update({k: v for k, v in slot_labels.get(slot, {}).items() if k != 'slot'})
            slots.append(row)
        rows.append({'path': rel, 'sha256': anm.sha256, 'entity_type': entity_type,
                     **{k: v for k, v in label.items() if k not in ('path', 'slots')},
                     'slots': slots})
    return rows


def labels(path: Path = LABELS_PATH) -> dict:
    data = json.loads(path.read_text())
    if data.get('schema') != LABEL_SCHEMA:
        raise FlikAnimationError('Unsupported Flik animation label file')
    seen = set()
    for row in data['states']:
        if row['state'] in seen or not 0 <= row['state'] < STATE_COUNT:
            raise FlikAnimationError(f'Duplicate or unknown state label {row["state"]}')
        if row['status'] not in STATUSES or not row.get('evidence'):
            raise FlikAnimationError(f'State {row["state"]} label lacks status or evidence')
        seen.add(row['state'])
    if seen != set(range(STATE_COUNT)):
        raise FlikAnimationError('Every state needs a label row, even an unknown one')
    slots = [row['slot'] for row in data.get('slots', [])]
    if len(slots) != len(set(slots)):
        raise FlikAnimationError('Duplicate slot label')
    for row in data.get('slots', []):
        if row['status'] not in STATUSES or not row.get('evidence') or not row.get('name'):
            raise FlikAnimationError(f'Slot {row["slot"]} label lacks name, status or evidence')
    for model in data.get('other_models', []):
        if model['path'] not in OTHER_MODELS:
            raise FlikAnimationError(f'Unknown non-player model {model["path"]}')
        for row in model.get('slots', []):
            if row['status'] not in STATUSES or not row.get('evidence') or not row.get('name'):
                raise FlikAnimationError(f'{model["path"]} slot {row["slot"]} label is incomplete')
    return data


def catalog(exe: bytes, anm: bytes, label_data: dict | None = None,
            variant_rows: list[dict] | None = None,
            other_rows: list[dict] | None = None) -> dict:
    """Join the ANM slots, the state table and the authored labels."""
    if hashlib.sha256(anm).hexdigest() != FLICK_ANM_SHA256:
        raise FlikAnimationError('Labels are evidenced for the retail FLICK.ANM only')
    read = read_executable(exe)
    records = AnmFile.parse(anm).records()
    states = state_table(read)
    idles = idle_tables(read)
    notes = check_slots(states, records)
    label_data = labels() if label_data is None else label_data
    state_labels = {row['state']: row for row in label_data['states']}
    slot_labels = {row['slot']: row for row in label_data.get('slots', [])}

    users = {slot: [] for slot in range(len(records))}
    for state in states:
        for layer, slot in (('A', state.slot_a), ('B', state.slot_b)):
            if layer == 'B' and state.slot_b == state.slot_a:
                continue
            users[slot].append(f'state {state.index:#04x} layer {layer}')
    for use, slot in THROW_OVERLAY.items():
        users[slot].append(f'throw overlay ({use})')
    users[AIM_SLOT].append('0x0059D99C mode (header +0x88)')

    slot_rows = []
    for slot, record in enumerate(records):
        row = {'slot': slot, 'present': record is not None, 'used_by': users[slot]}
        if record is not None:
            row.update(
                offset=record.offset, frames=record.frame_count,
                words_per_frame=record.words_per_frame, part_count=record.part_count,
                driven_parts=list(record.driven_parts),
                inherited_parts=list(record.inherited_parts),
                skipped_parts=list(record.skipped_parts),
                extra_channel_parts=[p for p in record.driven_parts if record.part_has_extra(p)],
                layer=('full' if not record.inherited_parts else
                       'upper' if record.inherited_parts[0] == 0 else 'lower'),
                seconds_at_30=round(record.frame_count/30, 3))
        label = slot_labels.get(slot, {})
        if label.get('name') == 'unreferenced' and users[slot]:
            raise FlikAnimationError(f'Slot {slot} is labelled unreferenced but has users')
        if (label.get('name') == 'absent') == (record is not None) and label:
            raise FlikAnimationError(f'Slot {slot} absent label disagrees with the file')
        row.update({k: v for k, v in label.items() if k != 'slot'})
        slot_rows.append(row)

    state_rows = []
    for state in states:
        script = state.script
        row = {
            'state': state.index, 'hex': f'{state.index:#04x}',
            'slot_a': state.slot_a, 'slot_b': state.slot_b,
            'speed_16_16': state.speed,
            'speed': ('ground-speed x %d/65536' % -state.speed if state.speed < 0
                      else round(state.speed/65536, 4)),
            'idle_family': state.idle_family,
            'script_va': f'{script.va:#010x}', 'script_hex': script.raw.hex(' '),
            'steps': len(script.frames), 'frames': list(script.frames),
            'end': script.end, 'loop_to': script.loop_to,
            'footstep_events': [{'step': s, 'side': e} for s, e in script.events],
            'idle_fidget_in': [f'{va:#010x}' for va, t in idles.items() if state.index in t],
        }
        row.update({k: v for k, v in state_labels[state.index].items() if k != 'state'})
        state_rows.append(row)

    return {
        'schema': 'ablpc.flik-animation-catalog.v1',
        'inputs': {'executable_sha256': RETAIL_SHA256, 'flick_anm_sha256': FLICK_ANM_SHA256},
        'state_table_va': f'{STATE_TABLE_VA:#010x}',
        'idle_tables': {f'{va:#010x}': {'selected_by_0x00861C84': IDLE_TABLES[va],
                                        'states': list(t)} for va, t in idles.items()},
        'slot_count': len(records),
        'model_variants': variant_rows or [],
        'other_flik_models': other_rows or [],
        'slots': slot_rows,
        'states': state_rows,
        'notes': notes + label_data.get('notes', []),
    }
