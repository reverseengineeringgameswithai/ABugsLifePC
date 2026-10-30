#!/usr/bin/env python3
"""EXP-20260904-006 fixed flat deck and raised-block test fixture.

Reuses existing bounded readers, retail loader and original movement. This is
an isolated synthetic fixture, not a general mesh encoder or repair of EXP-005.
Default output is asset-free measurements. Optional assets stay in work/copies.
"""
from pathlib import Path
import sys,struct,hashlib,json,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'reimplementation'))
from ablpc.terrain_all import TerrainAll
from ablpc.level_dat import LevelDat
SOURCE=ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01'
# Stored coordinates: flat deck high above the original terrain, box forward-left.
DECK=(4000,8300,13000,18100,-3200)
BOX=(5100,5750,15550,16250,-3392)
def quad(x0,x1,z0,z1,y):return [(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)]
def normal(tri):
 a,b,c=tri;u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
 cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);length=math.sqrt(sum(x*x for x in cross));assert length
 return tuple(round(-v*16384/length) for v in cross)
def build():
 t=TerrainAll.from_path(SOURCE/'TERRAIN.ALL');d=LevelDat.from_path(SOURCE/'LEVEL.DAT')
 assert hashlib.sha256(t.data).hexdigest()=='62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868'
 assert d.sha256=='786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53'
 # Render quads use the existing ground's winding. Collision reverses it.
 deck=quad(*DECK);top=quad(*BOX);bottom=quad(*BOX[:4],DECK[4]);quads=[deck,top]+[[top[i],bottom[i],bottom[(i+1)%4],top[(i+1)%4]] for i in range(4)]
 r=t.records[99];assert (r.field_10,r.field_44,r.field_46)==(6,-1,0)
 colquads=[quad(*DECK[:4],DECK[4]-96),quad(*BOX[:4],BOX[4]-96)]
 ct=colquads[1];cb=quad(*BOX[:4],DECK[4]+96)
 colquads += [[ct[i],cb[i],cb[(i+1)%4],ct[(i+1)%4]] for i in range(4)]
 payload=bytearray();cells=[]
 for qi,q in enumerate(colquads):
  for ids in ((0,2,1),(0,3,2)):
   tri=[q[i] for i in ids];n=normal(tri);local=[tuple(p[i]-(r.component_x,r.component_y,r.component_z)[i] for i in range(3)) for p in tri]
   a,b,c=local;xmin=min(p[0] for p in local);xmax=max(p[0] for p in local);zmin=min(p[2] for p in local);zmax=max(p[2] for p in local);ymin=min(p[1] for p in local);ymax=max(p[1] for p in local)
   ybase=(ymin-a[1])//64;yspan=max(1,math.ceil((ymax-a[1]-64*ybase)/64))
   zbase=(zmin-a[2])//64;zspan=max(1,math.ceil((zmax-a[2]-64*zbase)/64))
   assert all(-128<=v<=127 for v in (ybase,yspan,zbase,zspan))
   words=(*n,*a,*(b[i]-a[i] for i in range(3)),*(c[i]-a[i] for i in range(3)),xmin,xmax-xmin)
   cell=struct.pack('<14h4b',*words,ybase,yspan,zbase,zspan)
   offset=r.payload_offset+len(payload)+12
   payload+=struct.pack('<6h',1,1,xmin,xmax-xmin,zmin,zmax-zmin)+cell
   cells.append({'file_offset':offset,'surface':qi,'normal':n,'vertices':tri})
 payload+=b'\xff\xff';assert len(payload)<r.payload_size
 terrain=bytearray(t.data);terrain[r.payload_offset:r.payload_offset+len(payload)]=payload
 ref=d.static_mesh_reference('primary',160);template=ref.payload.vertices[9].to_bytes();verts=[v for q in quads for v in q]
 origin=struct.unpack_from('<3i',d.data,ref.object_offset)
 mesh=bytearray(struct.pack('<i',len(verts)))
 for v in verts:mesh+=struct.pack('<3h',*(v[i]-origin[i] for i in range(3)))+template[6:]
 assert ref.payload.tag==0x60
 mesh+=struct.pack('<HH',ref.payload.tag,len(quads))
 for i in range(len(quads)):
  mesh+=struct.pack('<8H',*(12*(4*i+j) for j in range(4)),*ref.payload.faces[0].field_words)
 mesh+=b'\xff\xff';assert len(mesh)<=ref.payload.end_offset-ref.geometry_offset
 dat=bytearray(d.data);dat[ref.geometry_offset:ref.geometry_offset+len(mesh)]=mesh
 struct.pack_into('<3i',dat,ref.record_offset,6150,-3296,15550)
 # Original positive radius4442 is retained, greater than the new deck radius.
 reparsed=LevelDat.parse(bytes(dat)).static_mesh_reference('primary',160);assert len(reparsed.payload.vertices)==24 and len(reparsed.payload.faces)==6
 return bytes(terrain),bytes(dat),{'deck':DECK,'box':BOX,'source99_payload_offset':r.payload_offset,'source99_replaced_prefix_bytes':len(payload),'mesh160_geometry_offset':ref.geometry_offset,'mesh160_replaced_prefix_bytes':len(mesh),'scene_record_offset':ref.record_offset,'cells':cells}


def report():
 import importlib.util
 spec=importlib.util.spec_from_file_location('deck_reference',ROOT/'scripts/terrain-barrier-authoring-probe.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);b=a.b
 terrain,dat,meta=build();source=TerrainAll.parse(terrain);text=b.p.load_text(b.p.DEFAULT_BINARY)
 def run(start,legs,src=source):
  probe=a.reference(src,text);probe.reset();b.p.put(probe.cpu,b.retail.POSITION,'4i',*start,0);b.p.put(probe.cpu,b.retail.FLAGS,'I',0)
  landing=probe.step((0,2048,0));moves=[]
  for count,delta in legs:moves.extend(probe.step(delta) for _ in range(count))
  return {'start':start,'landing':landing,'steps':moves}
 decky=DECK[4]*32;topy=BOX[4]*32
 cases={
  'approach_reverse':run((197091,decky-1024,492897),[(32,(-900,512,700)),(32,(900,512,-700))]),
  'top_leave_return':run((5425*32,topy-1024,15900*32),[(25,(900,512,0)),(35,(-900,512,0))]),
  'deck_roundtrip':run((6500*32,decky-1024,14500*32),[(20,(0,512,900)),(20,(0,512,-900))]),
 }
 # Negative controls remove only the newly generated top or side groups,
 # leaving the broad deck as a catch floor.
 def without(surfaces):
  record=source.records[99];groups=source.collision_payload(99).groups
  prefix=b''.join(g.raw for i,g in enumerate(groups) if i//2 not in surfaces)+b'\xff\xff'
  raw=bytearray(source.data);raw[record.payload_offset:record.payload_offset+len(prefix)]=prefix
  return TerrainAll.parse(bytes(raw))
 cases['without_sides']=run((197091,decky-1024,492897),[(25,(-900,512,700))],without({2,3,4,5}))
 cases['without_top']=run((5425*32,topy-1024,15900*32),[(25,(0,512,0))],without({1}))
 return {'experiment':'EXP-20260904-006','scope':'fixed synthetic fixture; offline original instructions, not a live input replay','binary_sha256':b.p.BINARY_SHA256,'terrain_sha256':hashlib.sha256(terrain).hexdigest(),'level_dat_sha256':hashlib.sha256(dat).hexdigest(),'fixture':meta,'cases':cases,'provenance':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(a.__file__),Path(b.__file__),Path(b.retail.__file__))}}

def write_fixture(directory):
 target=Path(directory).resolve()
 if not target.is_relative_to((ROOT/'work/copies').resolve()):raise ValueError('fixture assets must stay under work/copies')
 if target.exists():raise FileExistsError('choose a new output directory')
 terrain,dat,_=build();target.mkdir()
 (target/'TERRAIN.ALL').write_bytes(terrain);(target/'LEVEL.DAT').write_bytes(dat)

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-fixture',type=Path);args=parser.parse_args()
 result=report()
 if args.write_fixture is not None:write_fixture(args.write_fixture)
 print(json.dumps(result,indent=2))
