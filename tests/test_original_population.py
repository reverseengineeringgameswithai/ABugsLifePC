from pathlib import Path
import struct

import pytest

from ablpc.original_population import actors, stored_model, letter_pixels
from ablpc.level_raw import packets
from ablpc.original_population import initialized_placements, TOKEN_KINDS

ROOT=Path(__file__).resolve().parents[1]
CD=ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD'


def pickup_fixture():
    raw=struct.pack('<3iBBh',100,-50,300,0x2b,0x77,123)
    initialized=struct.pack('<hh',1,0x3f)+struct.pack('<3iBBh',100,-900,300,0x2b,0x77,-100)
    rows=[dict(id='type3f.000',offset=8,selector=0x2b,position=[100,-50,300],raw_hex=raw.hex(),label='Unknown')]
    return rows,initialized


def test_seed_tokens_are_selected_as_pickups_not_seed_actors():
    rows,data=pickup_fixture();result=initialized_placements(rows,4,data)
    assert result[0]['label']=='Green seed token' and result[0]['preview_kind']=='token-green'
    assert result[0]['position']==[100,-900,300] and result[0]['stored_position']==[100,-50,300]
    assert result[0]['raw_hex']==rows[0]['raw_hex'] and bytes.fromhex(result[0]['initialized_hex'])==data[4:]
    assert initialized_placements(rows,4,data,TOKEN_KINDS)==result
    assert initialized_placements(rows,4,data,{0x14})==[]


@pytest.mark.parametrize('case',['short','wrong-type','wrong-count','unaligned','duplicate','selector','xz','short-source'])
def test_initialized_pickup_join_rejects_invalid_references(case):
    rows,data=pickup_fixture()
    if case=='short':data=data[:-1]
    elif case=='wrong-type':data=data[:2]+b'\x2c\0'+data[4:]
    elif case=='wrong-count':data=b'\xff\x7f'+data[2:]
    elif case=='unaligned':rows[0]['offset']=9
    elif case=='duplicate':rows*=2
    elif case=='selector':data=data[:16]+b'\x2a'+data[17:]
    elif case=='xz':data=data[:4]+struct.pack('<i',101)+data[8:]
    elif case=='short-source':rows[0]['raw_hex']='00'
    with pytest.raises(ValueError):initialized_placements(rows,4,data)


def test_training_native_seed_token_census_and_positions():
    import runpy
    project=ROOT/'work/level-projects/original-training-populated'
    if not (project/'inputs/bugs.exe').exists():pytest.skip('Private Training fixture absent')
    import json
    cli=runpy.run_path(str(ROOT/'scripts/populate-original-map.py'))
    _,_,top,data,_=cli['native_pickups']((project/'inputs/LEVEL1.DAT').read_bytes(),
                                       (project/'inputs/TERR1.ALL').read_bytes(),project/'inputs/bugs.exe')
    rows=initialized_placements(json.loads((project/'original-map.json').read_text())['placements'],top.offset,data)
    tokens=[r for r in rows if r['selector'] in TOKEN_KINDS]
    assert len(rows)==62 and len(tokens)==2
    assert [r['offset'] for r in tokens]==[0x388,0x398]
    assert [r['position'] for r in tokens]==[[-1197,-328,148],[-3786,-539,1300]]


@pytest.mark.parametrize('selector,kind',[(0x29,'token-yellow'),(0x2a,'token-blue'),(0x2b,'token-green')])
def test_all_confirmed_seed_token_selectors_are_included(selector,kind):
    rows,data=pickup_fixture();rows[0]['selector']=selector
    raw=bytearray.fromhex(rows[0]['raw_hex']);raw[12]=selector;rows[0]['raw_hex']=raw.hex()
    data=data[:16]+bytes([selector])+data[17:]
    assert initialized_placements(rows,4,data)[0]['preview_kind']==kind


def test_unidentified_selector_is_not_promoted_to_seed_token():
    rows,data=pickup_fixture();rows[0]['selector']=0x2e
    assert initialized_placements(rows,4,data)==[]


def test_native_blueberry_lesson_reveals_four_preexisting_berry_seed_tokens():
    import runpy
    project=ROOT/'work/level-projects/original-training-populated'
    if not (project/'inputs/bugs.exe').exists():pytest.skip('Private Training fixture absent')
    result=runpy.run_path(str(ROOT/'scripts/training-berry-token-probe.py'))['proof'](project)
    assert result['blueberry_rows']==[54,55]
    assert result['berry_seed_token_rows']==[58,59,60,61]
    assert result['native']['delay_calls']==30
    assert [r['seed_byte'] for r in result['native']['token_progression']]==[17,34,51,68]


def actor_packet():
    p=bytearray(struct.pack('<I',35)+bytes(64*28))
    for slot,kind in ((0,38),(7,9),(63,11)):
        off=4+slot*28;struct.pack_into('<3i',p,off,-1,200,-300);p[off+12]=kind;p[off+13]=7;p[off+27]=0xa5
    return bytes(p)


def test_actors_full_capacity_and_opaque_fields():
    data=actor_packet();rows=actors(data)
    assert [r['slot'] for r in rows]==[0,7,63]
    assert rows[0]['position']==[-1,200,-300] and rows[0]['script']==7
    assert all(bytes.fromhex(r['raw_hex'])==data[r['offset']:r['offset']+28] for r in rows)


@pytest.mark.parametrize('mutation',[lambda d:d[:-1],lambda d:d+b'\0',lambda d:b'\x22'+d[1:],
                                    lambda d:d[:16]+b'\xff'+d[17:]])
def test_actor_packet_refuses_unsupported_or_truncated(mutation):
    with pytest.raises(ValueError):actors(mutation(actor_packet()))


def synthetic_all(count=4):
    size=48 if count==4 else 36;p=bytearray(size)
    p[:4]=bytes((1,2,3,0x3c if count==4 else 0x34))
    for i in range(count):struct.pack_into('<3hH',p,4+8*i,-i,i*2,i*3,0x1234+i)
    for i in range(count-1):p[4+count*8+i*4:7+count*8+i*4]=bytes((20+i,30+i,40+i))
    struct.pack_into('<H',p,size-2,0x1388)
    p+=bytes(4);descriptor=bytearray(76);struct.pack_into('<I4i',descriptor,0,len(p)//2,100,-200,300,1)
    return struct.pack('<I',(len(p)+4)//2)+p+struct.pack('<I',1)+descriptor


@pytest.mark.parametrize('count',[3,4])
def test_all_subset_signed_coordinates_translation_uvs_and_opaque(count):
    raw=synthetic_all(count);m=stored_model(raw);f=m['faces'][0]
    assert m['vertices'][1]['position']==[99,-198,303]
    assert m['vertices'][0]['rgb']==[1,2,3]
    assert m['vertices'][1]['rgb']==[20,30,40]
    assert f['indices']==([0,1,3,2] if count==4 else [0,1,2])
    assert f['uv']==([0x1234,0x1235,0x1237,0x1236] if count==4 else [0x1234,0x1235,0x1236])
    assert f['tag']==0x1388 and bytes.fromhex(f['raw_hex'])==raw[4:52 if count==4 else 40]
    assert len(bytes.fromhex(m['sources'][0]['raw_hex']))==76


@pytest.mark.parametrize('offset,value',[(7,0x20),(55,0x3c),(0,255),(4,0)])
def test_all_invalid_layouts_reject(offset,value):
    raw=bytearray(synthetic_all());raw[offset]=value
    # offset4 is an ordinary colour, deliberately valid rather than an assumed tag.
    if offset==4:assert stored_model(bytes(raw))['vertices'][0]['rgb'][0]==0
    else:
        with pytest.raises(ValueError):stored_model(bytes(raw))


def test_letter_strip_native_nibble_and_palette():
    palette=bytes(v for i in range(256) for v in (i,255-i,i))
    p=struct.pack('<IIHH',34,16,24,24)+b'\x21'+bytes(4607)
    assert letter_pixels(p,palette)==[dict(x=0,y=0,rgb=[113,142,113]),dict(x=1,y=0,rgb=[114,141,114])]
    for bad,pal in ((p[:-1],palette),(p,bytes(767)),(p[:4]+struct.pack('<I',20)+p[8:],palette)):
        with pytest.raises(ValueError):letter_pixels(bad,pal)


@pytest.mark.parametrize('name,faces',[('CHARS3/SOIL.ALL',207),('CHARS/BADBUG.ALL',76)])
def test_real_all_subset_corpus(name,faces):
    p=CD/name
    if not p.exists():pytest.skip('Private PC fixture absent')
    assert len(stored_model(p.read_bytes())['faces'])==faces


def test_training_and_anthill_actor_packets():
    for name in ('LEVEL07/LEVEL1.RAW','LEVEL01/LEVEL.RAW'):
        path=CD/name
        if not path.exists():pytest.skip('Private PC fixture absent')
        rows,_=packets(path.read_bytes());p=next(d for _,_,d in rows if d[:4]==struct.pack('<I',35))
        if name.startswith('LEVEL07'):
            result=actors(p);assert len(result)==9
            assert [r['type'] for r in result]==[38,11,11,11,11,9,9,9,9]
        else:
            with pytest.raises(ValueError,match='Unsupported Training'):actors(p)


def test_native_result_three_selects_training_completion():
    from ablpc.original_level import NativeMatrices
    from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ESP, UC_X86_REG_EIP
    path=ROOT/'work/copies/BUGS_PC-disc/bugs.exe'
    if not path.exists():pytest.skip('Private PC fixture absent')
    cpu=NativeMatrices(path.read_bytes()).cpu
    assert struct.unpack('<I',cpu.mem_read(0x440af0,4))==(0x440920,)
    cpu.reg_write(UC_X86_REG_ESP,0x1000f000);cpu.reg_write(UC_X86_REG_EAX,3)
    cpu.mem_write(0x59a5b0,bytes(2));cpu.mem_write(0x59d9b8,bytes(2))
    # Exact original dispatch through the state writes, stopping before audio.
    cpu.emu_start(0x4408ce,0x440934,count=100)
    assert cpu.reg_read(UC_X86_REG_EIP)==0x440934
    assert struct.unpack('<H',cpu.mem_read(0x59a5b0,2))==(1,)
    assert struct.unpack('<H',cpu.mem_read(0x59d9b8,2))==(23,)
