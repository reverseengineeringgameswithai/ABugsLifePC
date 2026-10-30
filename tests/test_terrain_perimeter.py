import struct

import pytest

from ablpc.terrain_all import TerrainFormatError
from ablpc.terrain_barriers import BarrierPayload, MAGIC, SENTINEL
from ablpc.terrain_perimeter import closed_outline, install_perimeter, reshape_short_loop, reshape_loop


LOOP = ((10, 10), (90, 10), (90, 90), (10, 90), (10, 10))


def donor():
    points = [[i % 2, 0x123400 + i, i % 3] for i in range(17)]
    for i, value in enumerate((0, 100, 0, 100)):
        points[i][1] = value
    return struct.pack("<IHH", MAGIC, 16, 0xBEEF) + b"".join(struct.pack("<3i", *p) for p in points) + b"opaque-tail!"


@pytest.mark.parametrize("reverse", [False, True])
def test_loop_preserves_all_unestablished_bytes(reverse):
    raw = donor()
    loop = tuple(reversed(LOOP)) if reverse else LOOP
    result = reshape_short_loop(raw, loop)
    strip = BarrierPayload.parse(result)
    assert [(p.x, p.z) for p in strip.points] == list(loop)
    assert strip.segment_count == 4 and strip.unknown_06 == 0xBEEF
    assert strip.points[0].middle_dword == SENTINEL
    allowed = set(range(4, 6)) | set(range(12, 16))
    for i in range(len(loop)):
        allowed.update(range(8 + 12 * i, 12 + 12 * i))
        allowed.update(range(16 + 12 * i, 20 + 12 * i))
    assert len(result) == len(raw)
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(raw, result)))


@pytest.mark.parametrize("points", [
    LOOP[:-1], ((0, 0), (1, 1), (2, 0), (0, 0)),
    ((0, 0), (1, 0), (0, 0), (0, 1), (0, 0)),
    ((0, 0), (0, 0), (1, 1), (0, 0)),
    ((True, 0), (10, 0), (10, 10), (True, 10), (True, 0)),
    ((0, 0), (67108864, 0), (67108864, 10), (0, 10), (0, 0)),
    ((0, 0), (10, 0), (10, 10), (5, 10), (5, -5), (0, -5), (0, 0)),
])
def test_reject_bad_outline(points):
    with pytest.raises(TerrainFormatError):
        closed_outline(points)


@pytest.mark.parametrize("cut", [0, 7, 20, 100, 210])
def test_bounds_checked_donor(cut):
    with pytest.raises(TerrainFormatError):
        reshape_short_loop(donor()[:cut], LOOP)


def test_exact_unlinked_terrain_control():
    raw = donor()
    record = bytearray(76)
    struct.pack_into("<I", record, 0, len(raw) // 2)
    struct.pack_into("<I", record, 16, 0x101)
    record[24:28] = b"KEEP"
    directory = len(raw) + 4
    data = struct.pack("<I", directory // 2) + b"\0" * 4 + raw[4:] + struct.pack("<I", 1) + bytes(record) + b"tail"
    result = install_perimeter(data, raw, 0, LOOP)
    assert result[:4] == data[:4] and result[directory:] == data[directory:]
    assert result[4:directory] == reshape_short_loop(raw, LOOP)
    with pytest.raises(TerrainFormatError):
        install_perimeter(result, raw, 0, LOOP)
    for index in (-1, 1, True):
        with pytest.raises(TerrainFormatError):
            install_perimeter(data, raw, index, LOOP)


def outline(count):
    corners=((0,0),(9000,0),(9000,9000),(0,9000),(0,0));points=[]
    for i,(a,b) in enumerate(zip(corners,corners[1:])):
        n=count//4+(i<count%4)
        points.extend(tuple(round(a[k]+(b[k]-a[k])*j/n) for k in range(2)) for j in range(n))
    return (*points,points[0])


def full_donor():
    points=[[x,0x123400+i,z] for i,(x,z) in enumerate(outline(36))]
    for first in (0,16):
        xs,_,zs=zip(*points[first:first+17])
        for j,value in enumerate((min(xs),max(xs)-min(xs),min(zs),max(zs)-min(zs))):points[first+j][1]=value
    points[32][1]=SENTINEL
    return struct.pack('<IHH',MAGIC,36,0xBEEF)+b''.join(struct.pack('<3i',*p) for p in points)+b'opaque-tail!'


@pytest.mark.parametrize('count',[15,16,17,31,32,33,36])
def test_full_and_short_block_metadata_preserve_unused_fields(count):
    original=full_donor();short=reshape_short_loop(original,LOOP)
    result=reshape_loop(short,outline(count),allocation_template=original)
    strip=BarrierPayload.parse(result)
    assert strip.segment_count==count and [(p.x,p.z) for p in strip.points]==list(outline(count))
    assert all(strip.bounds_cover_points(b) for b in strip.blocks)
    assert sum(b.bounds is not None for b in strip.blocks)==count//16
    assert len(result)==len(original) and strip.unknown_06==0xBEEF
    changed=set(range(4,6))
    for i in range(count+1):changed.update(range(8+12*i,12+12*i));changed.update(range(16+12*i,20+12*i))
    for first in range(0,count,16):
        for j in range(4 if count-first>=16 else 1):changed.update(range(12+12*(first+j),16+12*(first+j)))
    assert all(a==b or i in changed for i,(a,b) in enumerate(zip(short,result)))


def test_cannot_reinterpret_unknown_trailer_or_changed_unused_point_bytes():
    original=full_donor();short=reshape_short_loop(original,LOOP)
    with pytest.raises(TerrainFormatError,match='allocation'):reshape_loop(short,outline(16))
    corrupt=bytearray(short);corrupt[100]^=1
    with pytest.raises(TerrainFormatError,match='exact original suffix'):
        reshape_loop(bytes(corrupt),outline(16),allocation_template=original)
    with pytest.raises(TerrainFormatError,match='15 segments'):reshape_short_loop(original,outline(16))
