"""Guarded PC distance-initializer edits, EXP-20260907-009/010.

This changes both scenery groups at level initialization, preserving object
depth adjustments, geometry, relocation entries and the initializer's table.
"""
from __future__ import annotations

import hashlib
import struct

from .terrain_isolated import checked, pe_file_offset, replace_spans

INITIALIZER_VA = 0x0044BB70
INITIALIZER_SIZE = 0xF1
INITIALIZER_SHA256 = 'ed89aa9da5df494194b9a3f3bbb28557600f6df8f847978117ba096417820fd2'
ORIGINAL = {'near': 1152, 'far': 1664}
DEFAULT = {'near': 1728, 'far': 2496}
TABLE_START, TABLE_END = 0x005C0410, 0x005C240E


def validate_settings(settings):
    if not isinstance(settings, dict) or set(settings) != {'near', 'far'}:
        raise ValueError('Render distance requires near and far integer settings')
    near, far = settings['near'], settings['far']
    if type(near) is not int or type(far) is not int:
        raise ValueError('Render distances must be integers')
    # Bounded to the investigated original through 2x profiles. This is not
    # a claim that every value within this envelope has live acceptance.
    if not ORIGINAL['near'] <= near <= 2304 or not ORIGINAL['far'] <= far <= 3328 or near >= far:
        raise ValueError('Render distance outside the investigated near/far envelope')
    band = (far-near)//3
    if near+2*band > (TABLE_END-TABLE_START)//2 or far*5 >= 32768:
        raise ValueError('Render distance exceeds lookup or signed-depth bounds')
    return near, far


def patch_executable(source: bytes, settings: dict) -> tuple[bytes, dict]:
    """Patch immutable derived bytes only after complete initializer identity.

    Rebuild from the project's clean input to change or restore settings; a
    second application to an already changed initializer is deliberately refused.
    """
    near, far = validate_settings(settings)
    offset = pe_file_offset(source, INITIALIZER_VA, INITIALIZER_SIZE)
    if hashlib.sha256(checked(source, offset, INITIALIZER_SIZE)).hexdigest() != INITIALIZER_SHA256:
        raise ValueError('Unsupported or already modified render-distance initializer')
    edits = []
    sites = []
    for address, original, replacement, purpose in (
        (0x0044BBA3, 1664, far, 'hardware distance'),
        (0x0044BBAF, 1664, far, 'software distance'),
        (0x0044BBC1, -512, near-far, 'near group derivation'),
    ):
        at = pe_file_offset(source, address, 4)
        before, after = struct.pack('<i', original), struct.pack('<i', replacement)
        edits.append((at, before, after))
        sites.append({'va': address, 'file_offset': at, 'before': original,
                      'after': replacement, 'purpose': purpose})
    output = replace_spans(source, edits)
    return output, {'settings': {'near': near, 'far': far}, 'original': ORIGINAL.copy(),
                    'source_sha256': hashlib.sha256(source).hexdigest(),
                    'output_sha256': hashlib.sha256(output).hexdigest(), 'sites': sites,
                    'table_words': (TABLE_END-TABLE_START)//2,
                    'table_transition_end_index': near+2*((far-near)//3),
                    'scope': 'General distance initializer; original geometry, object bias and render code retained'}
