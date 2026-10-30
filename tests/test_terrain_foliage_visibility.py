"""EXP-011 regression: mesh growth must use the PC side-plane bound."""
import hashlib
import struct
from pathlib import Path

import pytest

from ablpc.level_dat import LevelDat
from ablpc.terrain_foliage import append_scene_mesh, encode_mesh, mesh_bytes
from ablpc.terrain_visibility import patch_scene_visibility, scene_visibility_radius
from test_terrain_additive import dat


def triangle(points):
    return encode_mesh(tuple(struct.pack('<3h', *p)+bytes.fromhex('112233445566') for p in points),
                       ((0x61, (((0, 1, 2), (0xc000, 0xc03f, 0xff00)),)),))


def fixture(point, previous=0, center=(0, 0, 0), origin=(0, 0, 0)):
    mesh = triangle((point, (0, 0, 0), (0, 1, 0)))
    raw = bytearray(dat(mesh))
    struct.pack_into('<3ih', raw, 8, *center, previous)
    struct.pack_into('<3i', raw, 72, *origin)
    return bytes(raw), mesh


@pytest.mark.parametrize('point,geometric', [((100, 0, 0), 100), ((1, 1, 0), 2),
                                           ((10023, 0, 0), 10023), ((3, 4, 0), 5)])
def test_growth_uses_shared_conservative_bound_and_preserves_bytes(point, geometric):
    raw, mesh = fixture(point)
    out, report = append_scene_mesh(raw, 0, mesh)
    ref = LevelDat.parse(out).static_mesh_reference('primary', 0)
    assert report['radius'] == scene_visibility_radius(geometric)
    assert struct.unpack_from('<h', out, 20)[0] == report['radius']
    assert mesh_bytes(out, 0)[0] == mesh
    allowed = {20, 21, 92, 93, 94, 95}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(raw[:-4], out)))
    assert out[ref.geometry_offset:ref.geometry_offset+len(mesh)] == mesh
    assert len(out)-struct.unpack_from('<i', out, len(out)-4)[0] == len(raw)-324


def test_scene_center_and_object_origin_are_used():
    raw, mesh = fixture((100, 0, 0), center=(10, -10, 20), origin=(20, -10, 20))
    _, report = append_scene_mesh(raw, 0, mesh)
    assert report['radius'] == scene_visibility_radius(110)


def test_unused_vertices_are_conservatively_enclosed():
    raw, _ = fixture((1, 0, 0))
    mesh = triangle(((1, 0, 0), (0, 0, 0), (0, 1, 0), (10023, 0, 0)))
    _, report = append_scene_mesh(raw, 0, mesh)
    assert report['radius'] == 14183


def test_larger_existing_bound_does_not_shrink():
    raw, mesh = fixture((10023, 0, 0), previous=20000)
    out, report = append_scene_mesh(raw, 0, mesh)
    assert report['radius'] == 20000
    assert out[20:22] == raw[20:22]


@pytest.mark.parametrize('point,previous', [((24000, 0, 0), 0), ((1, 0, 0), -1)])
def test_overflow_and_negative_prior_bound_fail_closed(point, previous):
    raw, mesh = fixture(point, previous)
    with pytest.raises(ValueError):
        append_scene_mesh(raw, 0, mesh)


@pytest.mark.parametrize('offset,value', [(84, 1), (86, 1), (88, 1), (91, 0xc1)])
def test_unestablished_transforms_rejected(offset, value):
    raw, mesh = fixture((100, 0, 0))
    raw = raw[:offset]+bytes([value])+raw[offset+1:]
    with pytest.raises(ValueError, match='unrotated, unscaled'):
        append_scene_mesh(raw, 0, mesh)


def test_empty_draw_stream_rejected():
    raw, _ = fixture((1, 0, 0))
    mesh = encode_mesh((bytes(12),), ((0x61, ()),))
    with pytest.raises(ValueError, match='at least one face'):
        append_scene_mesh(raw, 0, mesh)


def test_private_expanded_growth_agrees_with_radius_only_repair():
    path = Path('work/copies/EXP-20260906-010/expanded-fixture-02/LEVEL.DAT')
    if not path.exists():
        pytest.skip('private expanded control unavailable')
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == 'a60b8d902a68b6b4f7b1a7cd1c3cb533d9be9083afd2b2de1305e053c345232f'
    mesh, ref = mesh_bytes(raw, 160)
    grown, growth = append_scene_mesh(raw, 160, mesh)
    patched, patch = patch_scene_visibility(raw, expected_bound=10087)
    assert growth['radius'] == patch['bound_after'] == 14183
    assert grown[ref.record_offset:ref.record_offset+16] == patched[ref.record_offset:ref.record_offset+16]
    assert mesh_bytes(grown, 160)[0] == mesh_bytes(patched, 160)[0] == mesh
    assert patched[:8592] == raw[:8592] and patched[8594:] == raw[8594:]


@pytest.mark.parametrize('matrix,camera,old_accepts', [
    ((1267, 0, -3895, 0, 4096, 0, 3895, 0, 1267), (223118, -115207, 710692), True),
    ((873, 0, -4002, 0, 4096, 0, 4002, 0, 873), (303451, -115207, 734176), False),
    ((288, 0, -4085, 0, 4096, 0, 4085, 0, 288), (212134, -115207, 723713), True),
])
def test_original_pc_gate_at_captured_corner_cameras(matrix, camera, old_accepts):
    # Camera metadata from EXP-011; original instructions are a private input,
    # never distributed. This is offline execution, not a live branch trace.
    import pefile
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_ESI, UC_X86_REG_EBP

    path = Path('work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe')
    if not path.exists():
        pytest.skip('private original PC executable unavailable')
    binary = path.read_bytes()
    assert hashlib.sha256(binary).hexdigest() == '97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878'
    pe = pefile.PE(data=binary)
    image = pe.get_memory_mapped_image()
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(0x400000, (max(len(image), 0x500000)+4095) & ~4095)
    cpu.mem_write(0x400000, image)
    cpu.mem_map(0x3000000, 0x20000)
    for address, value in ((0x861c60, 640), (0x861dac, 480), (0x511508, 320)):
        cpu.mem_write(address, struct.pack('<i', value))
    cpu.mem_write(0x63e888, bytes(60))
    for row in range(3):
        cpu.mem_write(0x63e888+row*16, struct.pack('<3i', *matrix[row*3:row*3+3]))
    stored = [(abs(v)//32)*(-1 if v < 0 else 1) for v in camera]
    cpu.mem_write(0x5bdb9c, struct.pack('<3i', *stored))
    center = (4243, -570, 16018)
    raw, mesh = fixture((10023, 0, 0), previous=10087, center=center, origin=center)
    grown, report = append_scene_mesh(raw, 0, mesh)
    assert report['radius'] == 14183
    scene = grown[8:28]
    for radius, expected in ((10087, old_accepts), (report['radius'], True)):
        cpu.mem_write(0x3010200, scene[:12]+struct.pack('<h', radius)+scene[14:])
        cpu.reg_write(UC_X86_REG_ESP, 0x300f000)
        cpu.reg_write(UC_X86_REG_ESI, 0x3010200)
        cpu.reg_write(UC_X86_REG_EBP, 520**2)
        trace = []

        def hook(machine, address, size, user):
            trace.append(address)
            if address in (0x44d6a7, 0x44d728):
                machine.emu_stop()

        handle = cpu.hook_add(UC_HOOK_CODE, hook)
        try:
            cpu.emu_start(0x44d59f, 0x44d729, count=2000)
        finally:
            cpu.hook_del(handle)
        assert trace[-1] == (0x44d6a7 if expected else 0x44d728)
        if not expected:
            assert trace[-2] == 0x44d677
