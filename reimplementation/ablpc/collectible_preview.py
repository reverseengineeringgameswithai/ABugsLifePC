"""Small labeled editor meshes; native pickup sprites remain in the game."""
import math
# Native pickup kind bytes (EXP-20260908-021, EXP-20260909-013).
KINDS = {'grain': 0x14, 'letter-f': 0x10, 'letter-l': 0x11,
         'letter-i': 0x12, 'letter-k': 0x13,
         'token-yellow': 0x29, 'token-blue': 0x2a, 'token-green': 0x2b,
         'berry-blue': 0x23, 'berry-green': 0x21,
         'berry-gold': 0x22, 'berry-purple': 0x24}


def preview(kind):
    if kind not in KINDS: raise ValueError('Unknown collectible preview')
    vertices = []; faces = []
    colors = {'yellow': [225, 180, 35], 'blue': [45, 120, 230],
              'green': [65, 190, 60], 'gold': [245, 190, 45], 'purple': [170, 65, 210],
              'white': [245, 245, 245], 'black': [26, 5, 43]}
    color = colors.get(kind.split('-')[-1], [240, 205, 80])
    def box(x,y,z,w,h,d):
        base = len(vertices)
        for a,b,c in ((0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)):
            vertices.append(dict(position=[x+a*w,y+b*h,z+c*d],rgb=color,opaque=[0,0,0]))
        for a,b,c,d in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)):
            for tri in ((a,b,c),(a,c,d)):
                faces.append(dict(tag=0x61,indices=[base+i for i in tri],uv=[0,0,0]))
    if kind.startswith(('letter-', 'iaabad-')):
        # Readable block-letter silhouettes in the PC X/Y plane.
        patterns = {'f': ['111','100','110','100','100'], 'l': ['100','100','100','100','111'],
                    'i': ['111','010','010','010','111'], 'k': ['101','110','100','110','101'],
                    'a': ['010','101','111','101','101'], 'b': ['110','101','110','101','110'],
                    'd': ['110','101','101','101','110']}
        for y,row in enumerate(patterns[kind[-1]]):
            for x,c in enumerate(row):
                if c=='1': box(x*80-120,y*80-200,-35,80,80,70)
    else:
        rx,ry,rz = (75,150,60) if kind=='grain' else (170,170,40) if kind.startswith('token') else (150,150,150)
        points = [(0,-1,0)]
        for lat in (-math.pi/4,0,math.pi/4):
            points.extend((math.cos(lat)*math.cos(j*math.tau/8), math.sin(lat),
                           math.cos(lat)*math.sin(j*math.tau/8)) for j in range(8))
        points.append((0,1,0))
        vertices.extend(dict(position=[round(x*rx),round(y*ry),round(z*rz)],rgb=color,opaque=[0,0,0]) for x,y,z in points)
        for j in range(8):
            n=(j+1)%8; triangles=[(0,1+n,1+j),(25,17+j,17+n)]
            for ring in range(2):
                a,b=1+8*ring+j,1+8*ring+n;triangles.extend(((a,b,b+8),(a,b+8,a+8)))
            faces.extend(dict(tag=0x61,indices=list(tri),uv=[0,0,0]) for tri in triangles)
    return dict(id='collectible.'+kind,kind='decoration',vertices=vertices,faces=faces)
