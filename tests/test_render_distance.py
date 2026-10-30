"""Distance guards and original-PC initializer bounds; no embedded game bytes."""
import hashlib
from pathlib import Path
import struct

import pytest

from ablpc import render_distance as rd
from ablpc.terrain_isolated import pe_file_offset

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def retail():
    path = ROOT/'work/copies/BUGS_PC-disc/bugs.exe'
    if not path.exists():pytest.skip('private PC executable unavailable')
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878'
    return raw


@pytest.mark.parametrize('settings', [None, {}, {'near': 1728}, {'near': 1728, 'far': 2496, 'typo': 1},
    {'near': True, 'far': 2496}, {'near': 1728.0, 'far': 2496}, {'near': 1728, 'far': '2496'},
    {'near': 0, 'far': 2496}, {'near': 2305, 'far': 3328}, {'near': 1728, 'far': 3329},
    {'near': 1728, 'far': 1663}, {'near': 1728, 'far': 1728}])
def test_invalid_configuration(settings):
    with pytest.raises(ValueError):rd.validate_settings(settings)


@pytest.mark.parametrize('settings', [rd.ORIGINAL, rd.DEFAULT, {'near': 2304, 'far': 3328}])
def test_exact_initializer_edits_and_inverse(retail, settings):
    output, receipt = rd.patch_executable(retail, settings)
    allowed = {i for site in receipt['sites'] for i in range(site['file_offset'], site['file_offset']+4)}
    assert len(output) == len(retail)
    assert {i for i, (a,b) in enumerate(zip(retail,output)) if a != b} <= allowed
    inverse = bytearray(output)
    for site in receipt['sites']:struct.pack_into('<i', inverse, site['file_offset'], site['before'])
    assert bytes(inverse) == retail
    if settings != rd.ORIGINAL:
        with pytest.raises(ValueError, match='initializer'):rd.patch_executable(output, settings)


def test_guard_refuses_changed_surrounding_code_and_truncation(retail):
    changed = bytearray(retail);at = pe_file_offset(retail, rd.INITIALIZER_VA, rd.INITIALIZER_SIZE)
    changed[at+100] ^= 1
    with pytest.raises(ValueError, match='initializer'):rd.patch_executable(bytes(changed), rd.DEFAULT)
    with pytest.raises(ValueError):rd.patch_executable(retail[:at+90], rd.DEFAULT)


@pytest.mark.parametrize('settings', [rd.ORIGINAL, rd.DEFAULT, {'near': 2304, 'far': 3328}])
@pytest.mark.parametrize('renderer', [1,2])
def test_original_initializer_matches_all_table_words_and_stays_in_bounds(retail, settings, renderer):
    import pefile
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_MEM_WRITE
    from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EIP
    image,_ = rd.patch_executable(retail, settings)
    pe = pefile.PE(data=image);mapped = pe.get_memory_mapped_image()
    cpu = Uc(UC_ARCH_X86,UC_MODE_32);cpu.mem_map(0x400000,(len(mapped)+4095)&~4095)
    cpu.mem_write(0x400000,mapped);cpu.mem_map(0x3000000,0x20000)
    cpu.reg_write(UC_X86_REG_ESP,0x3010000)
    cpu.mem_write(0x59f7f0,struct.pack('<h',renderer))
    cpu.mem_write(0x861c60,struct.pack('<i',640));cpu.mem_write(0x861dac,struct.pack('<i',480))
    cpu.mem_write(rd.TABLE_START-16,b'\xa5'*16);cpu.mem_write(rd.TABLE_END,b'\x5a'*16)
    globals_ = {0x5bf824,0x5bf828,0x5bfa3c,0x5bfa40,0x5b56d0,0x5c02fc,0x5ba80c,0x5b1ec8}
    writes = []
    def write_guard(cpu, access, address, size, value, user):
        assert (0x3000000 <= address and address+size <= 0x3020000 or
                rd.TABLE_START <= address and address+size <= rd.TABLE_END or
                address in globals_ and size == 4), hex(address)
        writes.append((address,size))
    cpu.hook_add(UC_HOOK_MEM_WRITE,write_guard)
    cpu.emu_start(rd.INITIALIZER_VA,0x44bc61,count=50000)
    assert cpu.reg_read(UC_X86_REG_EIP) == 0x44bc61
    near,far = rd.validate_settings(settings);band=(far-near)//3
    expected = [0]*near + [0x600]*band + [0x400]*band + [0x200]*(4095-near-2*band)
    assert list(struct.unpack('<4095H',cpu.mem_read(rd.TABLE_START,8190))) == expected
    assert cpu.mem_read(rd.TABLE_START-16,16) == b'\xa5'*16 and cpu.mem_read(rd.TABLE_END,16) == b'\x5a'*16
    assert struct.unpack('<i',cpu.mem_read(0x5c02fc,4))[0] == near
    assert struct.unpack('<i',cpu.mem_read(0x5ba80c,4))[0] == far
    assert writes
