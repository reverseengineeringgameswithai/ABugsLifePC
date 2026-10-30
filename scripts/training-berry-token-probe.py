#!/usr/bin/env python3
"""Original-PC Training pickup/lesson proof; offline Unicorn, no live process."""
import json
from pathlib import Path
import runpy
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reimplementation'))
from ablpc.original_level import NativeMatrices, TRAINING, digest
from ablpc.level_dat import LevelDat
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EAX


def proof(project):
    inputs={k:(project/'inputs'/Path(v[0]).name).read_bytes() for k,v in TRAINING.items()}
    assert all(digest(inputs[k])==v[1] for k,v in TRAINING.items())
    exe=project/'inputs/bugs.exe'
    initializer=runpy.run_path(str(ROOT/'scripts/populate-original-map.py'))['native_pickups']
    _,_,top,initialized,init=initializer(inputs['dat'],inputs['terrain'],exe)
    cpu=NativeMatrices(exe.read_bytes()).cpu
    base=0x10004000
    def put(a,fmt,*values):cpu.mem_write(a,struct.pack('<'+fmt,*values))
    def get(a,fmt):return struct.unpack('<'+fmt,cpu.mem_read(a,struct.calcsize('<'+fmt)))
    def coords(i):return list(get(base+4+i*16,'3i'))
    put(0x5c595c,'I',base);cpu.mem_write(base,initialized)
    put(0x599c60,'I',0x1000a000);cpu.mem_write(0x1000a000,bytes([1])*4096)
    put(0x599dde,'H',1)  # Exclude unrelated HUD cadence/random refresh.
    stubs={0x414ba0,0x49d320,0x42c0d0,0x42c110,0x428590,0x4148a0,
           0x41a550,0x403a10,0x4039d0,0x414cc0,0x4595e0,0x42aa50,0x41a2b0}
    callbacks=[];visited=[]
    def hook(uc,pc,size,_):
        if not 0x401000<=pc<0x4c1000:raise ValueError(f'Execution escaped PC text: {pc:x}')
        visited.append(pc)
        if pc in stubs:
            sp=uc.reg_read(UC_X86_REG_ESP)
            callbacks.append(dict(pc=hex(pc),args=list(get(sp+4,'2I'))))
            uc.reg_write(UC_X86_REG_ESP,sp+4);uc.reg_write(UC_X86_REG_EAX,0)
            uc.reg_write(UC_X86_REG_EIP,get(sp,'I')[0])
    cpu.hook_add(UC_HOOK_CODE,hook)
    def call(entry):
        callbacks.clear();visited.clear();put(0x1000f000,'I',0x1000fff0);cpu.reg_write(UC_X86_REG_ESP,0x1000f000)
        cpu.emu_start(entry,0x1000fff0,count=200000)
        assert cpu.reg_read(UC_X86_REG_EIP)==0x1000fff0
        return dict(entry=hex(entry),instructions=len(visited),callbacks=list(callbacks),
                    ordered_pc_sha256=digest(b''.join(struct.pack('<I',p) for p in visited)))
    berries=[i for i in range(top.count) if initialized[4+i*16+12]==0x23]
    tokens=[i for i in range(top.count) if initialized[4+i*16+12]==0x2c]
    assert berries==[54,55] and tokens==[58,59,60,61]
    before={str(i):coords(i) for i in berries+tokens}
    setup=call(0x43c040)
    assert all(coords(i)[1]==before[str(i)][1]+8000 for i in tokens)
    hidden={str(i):coords(i) for i in tokens}
    put(0x59f6b8,'I',12);put(0x59d9a7,'B',0)
    negative=call(0x43c340);assert get(0x59f6b8,'I')==(12,)
    def collect(i):
        # Native proximity/consume/counter branches; synthetic placement of Flik.
        x,y,z=coords(i);put(base+4+i*16+13,'B',1)
        put(0x59d910,'3i',x*32,(y+230)*32,z*32)
        result=call(0x417720)
        assert coords(i)[1]==-0x80000000
        return result
    pickup=collect(54);assert get(0x59d9a7,'B')==(1,)
    advance=call(0x43c340);assert get(0x59f6b8,'I')==(13,) and get(0x59f690,'I')==(30,)
    delay=[call(0x43c340) for _ in range(30)]
    assert {str(i):coords(i) for i in tokens}==hidden
    reveal=call(0x43c340)
    assert all(coords(i)==before[str(i)] for i in tokens)
    rows=[];put(0x59d9ab,'B',0)
    for n,i in enumerate(tokens,1):
        result=collect(i);assert get(0x59d9ab,'B')==(17*n,)
        assert any(c['pc']=='0x4595e0' and c['args']==[24,n-1] for c in result['callbacks'])
        rows.append(dict(row=i,seed_byte=17*n,execution=result))
    return dict(experiment='EXP-20260910-001',scope='Offline original x86; feedback/audio/HUD/plant-refresh callbacks stubbed, synthetic Flik proximity',
                stub_addresses=list(map(hex,sorted(stubs))),initialized_positions=before,hidden_positions=hidden,
                blueberry_rows=berries,berry_seed_token_rows=tokens,
                native=dict(initializer=init,setup=setup,no_berry_control=negative,blueberry_pickup=pickup,
                            stage12_to13=advance,delay_calls=len(delay),stage13_reveal=reveal,token_progression=rows),
                confirmed='Four pre-existing type2C tokens are hidden by +8000 Y, then restored on entering lesson13 after a nonzero berry weapon completes lesson12; no new token allocation.')


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if not a.out.resolve().is_relative_to(ROOT/'work') or a.out.exists():raise ValueError('Evidence output must be fresh under work/')
    result=proof(a.project);a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='native'},indent=2))
