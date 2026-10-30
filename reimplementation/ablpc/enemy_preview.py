"""Editor-only placement silhouettes; native animated models remain in-game.

These meshes are deliberately independent of the game's model/texture format.
They are never compiled into game geometry or used as collision surfaces.
"""
import math

# Native creature donor (level, type) pairs (EXP-20260908-020).
DONORS = {'spider': (9, 0), 'mosquito': (10, 4), 'pill-bug': (39, 2),
          'caterpillar': (40, 13), 'bee': (13, 3)}


def preview(kind):
    if kind not in DONORS: raise ValueError('Unknown enemy preview')
    vertices = []; faces = []

    def ellipsoid(center, radii, rgb):
        base = len(vertices)
        points = [(0, -1, 0)]
        for latitude in (-math.pi/4, 0, math.pi/4):
            points.extend((math.cos(latitude)*math.cos(j*math.tau/8),
                           math.sin(latitude), math.cos(latitude)*math.sin(j*math.tau/8))
                          for j in range(8))
        points.append((0, 1, 0))
        vertices.extend(dict(position=[round(center[k]+radii[k]*p[k]) for k in range(3)],
                             rgb=rgb, opaque=[0, 0, 0]) for p in points)
        triangles = []
        for j in range(8):
            n = (j+1)%8
            triangles.extend(((0, 1+n, 1+j), (25, 17+j, 17+n)))
            for ring in range(2):
                a, b = 1+8*ring+j, 1+8*ring+n
                triangles.extend(((a, b, b+8), (a, b+8, a+8)))
        faces.extend(dict(tag=0x61, indices=[base+i for i in tri], uv=[0, 0, 0])
                     for tri in triangles)

    colors = {'spider': [128, 54, 115], 'mosquito': [75, 140, 130],
              'pill-bug': [130, 83, 45], 'caterpillar': [92, 166, 57], 'bee': [222, 165, 35]}
    color = colors[kind]
    if kind == 'caterpillar':
        for z in (-210, -70, 70, 210): ellipsoid((0, -130, z), (130, 130, 120), color)
    else:
        ellipsoid((0, -180, 0), (180, 170, 250), color)
        ellipsoid((0, -160, -260), (100, 100, 110), color)
    if kind == 'spider':
        for side in (-1, 1):
            for z in (-180, -60, 60, 180):
                ellipsoid((side*250, -55, z), (200, 35, 30), color)
    elif kind in ('mosquito', 'bee'):
        for side in (-1, 1): ellipsoid((side*250, -280, 50), (280, 15, 120), [190, 210, 215])
        if kind == 'mosquito': ellipsoid((0, -140, -420), (20, 20, 140), color)
    elif kind == 'pill-bug':
        for z in (-150, -50, 50, 150): ellipsoid((0, -220, z), (190, 100, 35), [95, 60, 36])
    return dict(id='enemy.'+kind, kind='decoration', vertices=vertices, faces=faces)
