"""Fixture tests for scripts/ablrec-analyze.py (flight-recorder Phase 2)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "ablrec_analyze",
    Path(__file__).resolve().parents[1] / "scripts" / "ablrec-analyze.py",
)
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
sys.modules["ablrec_analyze"] = _MOD  # needed so @dataclass can resolve annotations
_SPEC.loader.exec_module(_MOD)

GAME = _MOD.GAME_CR3

# 6 valid records (one cr3=0 boot write) + 1 garbage line; header says 9 total
# occurred but only 6 retained -> truncated.
DUMP = """\
# ABLREC total=9 shown=6 nranges=2 dump_eip=00460000 dump_cr3=00454000
# range 0 [00001000,00001010)
# range 1 [00002000,00002008)
300 cr3=00454000 pc=00401001 oldpc=00401000 addr=00001000 val=0000000a w=4
100 cr3=00454000 pc=00401001 oldpc=00401000 addr=00001000 val=00000005 w=4
200 cr3=00454000 pc=00402001 oldpc=00402000 addr=00001002 val=000000ff w=1
150 cr3=00000000 pc=00003001 oldpc=00003000 addr=00001000 val=00000000 w=4
400 cr3=00454000 pc=00403001 oldpc=00403000 addr=00002000 val=00000011 w=4
this line is not a record and must be skipped
500 cr3=00454000 pc=00401001 oldpc=00401000 addr=00001000 val=00000007 w=4
"""

PHASE0_DUMP = """\
# ABLREC total=3 shown=3 range=[0059d900,0059d930)
50 cr3=00454000 pc=004ab88b oldpc=004ab889 addr=0059d910 val=ffffaa20 w=4
60 cr3=00454000 pc=004ab88b oldpc=004ab889 addr=0059d910 val=ffffa9e4 w=4
70 cr3=00454000 pc=004ab891 oldpc=004ab88f addr=0059d914 val=00002468 w=4
"""


def test_parse_header_and_records():
    d = _MOD.parse_dump(DUMP)
    assert d.total == 9 and d.shown == 6
    assert d.truncated is True
    assert d.dump_eip == 0x00460000 and d.dump_cr3 == 0x00454000
    assert d.ranges == [(0x1000, 0x1010), (0x2000, 0x2008)]
    assert len(d.records) == 6
    assert d.skipped == 1
    r = d.records[0]
    assert (r.tsc, r.cr3, r.pc, r.oldpc, r.addr, r.val, r.width) == (
        300, 0x454000, 0x401001, 0x401000, 0x1000, 0x0A, 4)


def test_parse_phase0_inline_range():
    d = _MOD.parse_dump(PHASE0_DUMP)
    assert d.total == 3 and d.shown == 3 and d.truncated is False
    assert d.ranges == [(0x0059D900, 0x0059D930)]
    assert len(d.records) == 3
    assert d.dump_cr3 is None  # phase-0 header has no dump_cr3


def test_cr3_split():
    d = _MOD.parse_dump(DUMP)
    assert _MOD.cr3_split(d) == {0x454000: 5, 0x0: 1}


def test_who_wrote_overlap_and_cr3_filter():
    d = _MOD.parse_dump(DUMP)
    # query the single byte 0x1000: the 3 dword writes at 0x1000 (game) cover it;
    # the byte write at 0x1002 does NOT; the cr3=0 write is filtered out.
    g = _MOD.who_wrote(d, 0x1000, qwidth=1, cr3=GAME)
    assert set(g) == {0x401000}
    assert len(g[0x401000]) == 3
    # query byte 0x1002: dword@0x1000 (covers 0x1000-0x1003) AND byte@0x1002 match.
    g2 = _MOD.who_wrote(d, 0x1002, qwidth=1, cr3=GAME)
    assert set(g2) == {0x401000, 0x402000}
    # cr3=all now includes the boot write at 0x1000.
    g3 = _MOD.who_wrote(d, 0x1000, qwidth=1, cr3=None)
    assert set(g3) == {0x401000, 0x003000}


def test_who_wrote_query_width():
    d = _MOD.parse_dump(DUMP)
    # a 4-byte query at 0x1000 covers 0x1000-0x1003, so the byte write at 0x1002 matches.
    g = _MOD.who_wrote(d, 0x1000, qwidth=4, cr3=GAME)
    assert set(g) == {0x401000, 0x402000}


def test_timeline_orders_by_tsc_and_derives_old():
    d = _MOD.parse_dump(DUMP)
    tl = _MOD.timeline(d, 0x1000, cr3=GAME)
    # exact addr 0x1000, game cr3 -> tsc 100,300,500 with vals 5,0xa,7
    assert [(r.tsc, r.val, old) for r, old in tl] == [
        (100, 0x5, None),   # first old is unknown (ring window)
        (300, 0xA, 0x5),
        (500, 0x7, 0xA),
    ]


def test_writers_census():
    d = _MOD.parse_dump(DUMP)
    cen = _MOD.writers(d, cr3=GAME)
    assert set(cen) == {0x401000, 0x402000, 0x403000}
    assert cen[0x401000]["count"] == 3
    assert cen[0x401000]["addrs"] == {0x1000}
    assert cen[0x401000]["widths"] == {4}
    assert cen[0x402000]["widths"] == {1}


def test_containing_function_nearest_preceding_entry():
    funcs = [(0x401000, "A"), (0x402000, "B"), (0x403000, "C")]
    assert _MOD.containing_function(funcs, 0x401500) == (0x401000, "A")
    assert _MOD.containing_function(funcs, 0x403000) == (0x403000, "C")
    assert _MOD.containing_function(funcs, 0x403abc) == (0x403000, "C")
    assert _MOD.containing_function(funcs, 0x400fff) is None  # below first entry


def test_extract_disasm():
    objdump = (
        "bugs.exe:     file format pei-i386\n\n"
        "Disassembly of section .text:\n\n"
        "004ab889 <.text>:\n"
        "  4ab889:\t89 02                \tmov    DWORD PTR [edx],eax\n"
        "  4ab88b:\t8b 44 24 44          \tmov    eax,DWORD PTR [esp+0x44]\n"
    )
    assert _MOD.extract_disasm(objdump, 0x4AB889) == "mov    DWORD PTR [edx],eax"
    assert _MOD.extract_disasm(objdump, 0x4AB88B) == "mov    eax,DWORD PTR [esp+0x44]"
    assert _MOD.extract_disasm(objdump, 0x4AB999) is None
