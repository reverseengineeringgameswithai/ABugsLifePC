"""New barrier grammar tests; existing terrain directory tests stay authoritative."""
from pathlib import Path
import struct

import pytest

from reimplementation.ablpc.terrain_all import TerrainAll, TerrainFormatError
from reimplementation.ablpc.terrain_barriers import BarrierPayload, MAGIC, SENTINEL


def fixture(count=17):
    points = [[i,1000+i,-i] for i in range(count+1)]
    for first in range(0,count,16):
        if count-first < 16:
            points[first][1] = SENTINEL
        else:
            for j,v in enumerate((first,16,-first-16,16)):
                points[first+j][1] = v
    return struct.pack("<IHH",MAGIC,count,0xA5C3)+b"".join(struct.pack("<3i",*v) for v in points)


@pytest.mark.parametrize("count", (0,1,4,15,16,17,31,32,33))
def test_count_is_segments_and_blocks_share_endpoint(count):
    raw = fixture(count)
    strip = BarrierPayload.parse(raw,offset=200)
    assert strip.segment_count == count
    assert len(strip.points) == count+1
    assert [b.first_segment for b in strip.blocks] == list(range(0,count,16))
    assert sum(b.segment_count for b in strip.blocks) == count
    assert sum(b.bounds is not None for b in strip.blocks) == count//16
    assert sum(b.bounds is None for b in strip.blocks) == bool(count%16)
    assert all(strip.bounds_cover_points(b) for b in strip.blocks)
    assert strip.points[-1].offset == 208+count*12
    assert b"".join(point.raw for point in strip.points) == raw[8:]


def test_unknown_header_middle_and_suffix_are_retained_immutably():
    raw = bytearray(fixture(4)+b"unknown trailing bytes")
    strip = BarrierPayload.parse(raw)
    original = bytes(raw)
    raw[:] = b"x"*len(raw)
    assert strip.raw == original
    assert strip.unknown_06 == 0xA5C3
    assert strip.points[1].middle_dword == 1001
    assert strip.trailer == b"unknown trailing bytes"


@pytest.mark.parametrize("length", (0,1,4,7,8,19,20,67,68,211))
def test_truncation_rejected(length):
    with pytest.raises(TerrainFormatError,match="truncated|overruns"):
        BarrierPayload.parse(fixture(17)[:length])


@pytest.mark.parametrize("offset", (-1,True,1.0))
def test_invalid_offset_rejected(offset):
    with pytest.raises(TerrainFormatError,match="offset"):
        BarrierPayload.parse(fixture(),offset=offset)


@pytest.mark.parametrize("position,fmt,value,message", (
    (0,"I",0,"magic"), (4,"H",65535,"overruns"),
    (12,"i",SENTINEL,"sentinel in full"),
    (24,"i",-1,"negative"), (48,"i",-1,"negative"),
    (8+16*12+4,"i",0,"short final"),
))
def test_unsafe_or_noncanonical_layouts_rejected(position,fmt,value,message):
    raw = bytearray(fixture(17))
    struct.pack_into("<"+fmt,raw,position,value)
    with pytest.raises(TerrainFormatError,match=message):
        BarrierPayload.parse(raw)


def test_loose_bounds_are_preserved_and_inadequate_bounds_are_reported():
    raw = bytearray(fixture(16))
    struct.pack_into("<i",raw,24,100)
    strip = BarrierPayload.parse(raw)
    assert strip.bounds_cover_points(strip.blocks[0])
    assert strip.blocks[0].bounds[1] == 100
    struct.pack_into("<i",raw,24,1)
    strip = BarrierPayload.parse(raw)
    assert not strip.bounds_cover_points(strip.blocks[0])


def test_only_kind_0x101_uses_this_reader():
    payload=fixture(4)
    record=bytearray(76)
    struct.pack_into("<I",record,0,len(payload)//2)
    raw=struct.pack("<I",(4+len(payload))//2)+payload+struct.pack("<I",1)+record
    terrain=TerrainAll.parse(raw)
    with pytest.raises(TerrainFormatError,match="kind 0x101"):
        BarrierPayload.from_terrain(terrain,0)
    with pytest.raises(TerrainFormatError,match="index"):
        BarrierPayload.from_terrain(terrain,True)


def test_all_available_retail_barriers_follow_the_layout():
    root=Path(__file__).resolve().parents[1]/"work/copies/BUGS_PC-full-disc/PC/BUGS/CD"
    paths=sorted(path for path in root.glob("LEVEL*/*.ALL") if path.name in ("TERRAIN.ALL","TERR1.ALL"))
    if len(paths)!=18:
        pytest.skip("complete 18-file retail terrain corpus unavailable")
    strips=[]
    for path in paths:
        terrain=TerrainAll.from_path(path)
        for record in terrain.records:
            if record.field_10!=0x101:continue
            strip=BarrierPayload.from_terrain(terrain,record.index)
            assert strip.unknown_06==0 and strip.trailer==b""
            assert all(strip.bounds_cover_points(b) for b in strip.blocks)
            assert len(strip.raw)==8+12*(strip.segment_count+1)
            strips.append(strip)
    assert len(strips)==65
    assert sum(s.segment_count for s in strips)==6722
    assert sum(b.bounds is not None for s in strips for b in s.blocks)==396
    assert sum(b.bounds is None for s in strips for b in s.blocks)==62
