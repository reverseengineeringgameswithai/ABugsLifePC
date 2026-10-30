"""Original PC instructions, synthetic floor/player/visibility; no live RAM access."""
import hashlib
from pathlib import Path
import runpy
import struct
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'reimplementation'))
from ablpc.level_seeds import actor_packet
from ablpc.level_dat import LevelDat
Native=runpy.run_path(str(ROOT/'scripts/probe-soil-audio.py'))['Native']
STOP=0x3200000


class Dot(Native):
    def __init__(self,exe,dat,raw,base=0x400000):
        assert hashlib.sha256(exe).hexdigest()=='97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878'
        super().__init__(exe,base)
        self.actor=self.va(0x59c30c)
        self.visible=True;self.sounds=[]
        records=[r for r in LevelDat.parse(dat).top_records if r.type_id==1]
        assert len(records)==1
        r=records[0];self.path=0x3001000
        self.u.mem_write(self.path,dat[r.offset:r.offset+r.size])
        self.put(self.va(0x5c5864),self.path)
        parts,_,i=actor_packet(raw)
        row=parts[i][2][4+25*28:4+26*28]
        self.u.mem_write(self.va(0x599eb0+25*28),row)
        self.put(self.actor+128,self.va(0x599eb0+25*28))
        self.hook(self.va(0x4abe00),lambda:self.ret(value=0))
        for addr in (0x415320,0x42aa50):self.hook(self.va(addr),self.ret)
        self.hook(self.va(0x414f80),lambda:(self.sounds.append(self.arg(0)),self.ret()))
        self.hook(self.va(0x459620),lambda:self.ret(value=int(self.visible)))
        assert self.call(0x41bd10,self.actor)==STOP
        self.u.mem_write(self.actor+0x5c,struct.pack('<H',0x4081))
        self.position_player(self.xyz())

    def xyz(self):return struct.unpack('<3i',self.u.mem_read(self.actor+4,12))
    def position_player(self,xyz):self.u.mem_write(self.va(0x59d910),struct.pack('<3i',*xyz))
    def cursor(self):return struct.unpack('<h',self.u.mem_read(self.actor+0x5e,2))[0]
    def tick(self):
        self.put(self.va(0x599c60),self.va(0x4c2100))
        assert self.call(0x4317d0)==STOP
        assert self.call(0x41dc60,self.actor)==STOP
        return dict(cursor=self.cursor(),xyz=self.xyz(),animation=self.get(self.actor+0x40),
                    flags=self.get(self.actor+0x5c)&65535,script=self.get(self.actor+0x70)-self.delta)
