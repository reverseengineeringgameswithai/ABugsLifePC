#!/usr/bin/env python3
"""Offline preview of an ALL model exported by original_levels.creature_model.

Usage: python3 render-model.py MODEL.json OUT.png [--pages DIR] [--views yaw:pitch,...]

System python3 with numpy and Pillow (the project venv lacks them, as for
research/starry-night/moon-preview.py). Positions are stored-pose (no
animation). PC Y grows downward, so it is flipped for display. With --pages,
each face samples page (tag >> 8) & 31 at u = word & 255, v = word >> 8,
modulated by vertex colour / 128; colour-keyed texels are skipped. Without it,
faces use vertex colour with simple Lambert shading. Output is a preview for
looking at shapes and textures, not a faithful reproduction of the renderer.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

SIZE = 420


def rotation(yaw, pitch):
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    return rx @ ry


def triangles(model):
    for face in model['faces']:
        idx, uv = face['indices'], face['uv']
        corners = list(zip(idx, uv))
        # creature_model stores quads in drawing order 0,1,3,2: fan them.
        for a, b, c in ((0, 1, 2), (0, 2, 3)) if len(corners) == 4 else ((0, 1, 2),):
            yield (corners[a], corners[b], corners[c]), face['tag']


def render(model, pages, yaw, pitch):
    pos = np.array([v['position'] for v in model['vertices']], float)
    pos[:, 1] *= -1  # PC Y is down
    col = np.array([v['rgb'] for v in model['vertices']], float)
    cam = pos @ rotation(math.radians(yaw), math.radians(pitch)).T
    lo, hi = cam[:, :2].min(0), cam[:, :2].max(0)
    scale = (SIZE - 20) / max(hi - lo)
    screen = (cam[:, :2] - lo) * scale + 10
    screen[:, 1] = SIZE - screen[:, 1]
    depth = np.full((SIZE, SIZE), np.inf)
    image = np.zeros((SIZE, SIZE, 3)) + (38, 38, 46)
    light = np.array([0.4, 0.7, -0.6]); light /= np.linalg.norm(light)
    for (p0, p1, p2), tag in triangles(model):
        ids = [p0[0], p1[0], p2[0]]
        s = screen[ids]
        x0, y0 = np.floor(s.min(0)).astype(int); x1, y1 = np.ceil(s.max(0)).astype(int)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, SIZE - 1), min(y1, SIZE - 1)
        if x1 < x0 or y1 < y0:
            continue
        area = (s[1, 0] - s[0, 0]) * (s[2, 1] - s[0, 1]) - (s[2, 0] - s[0, 0]) * (s[1, 1] - s[0, 1])
        if abs(area) < 1e-9:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        w1 = ((xs - s[0, 0]) * (s[2, 1] - s[0, 1]) - (s[2, 0] - s[0, 0]) * (ys - s[0, 1])) / area
        w2 = ((s[1, 0] - s[0, 0]) * (ys - s[0, 1]) - (xs - s[0, 0]) * (s[1, 1] - s[0, 1])) / area
        w0 = 1 - w1 - w2
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not inside.any():
            continue
        z = w0 * cam[ids[0], 2] + w1 * cam[ids[1], 2] + w2 * cam[ids[2], 2]
        rows, cols = np.nonzero(inside)
        py, px = rows + y0, cols + x0
        zz = z[rows, cols]
        nearer = zz < depth[py, px]
        if not nearer.any():
            continue
        py, px, zz = py[nearer], px[nearer], zz[nearer]
        b = np.stack([w0[rows, cols][nearer], w1[rows, cols][nearer], w2[rows, cols][nearer]], 1)
        shade = col[ids].T @ b.T  # 3 x n vertex colour
        page = pages.get((tag >> 8) & 31) if pages else None
        if page is not None:
            u = np.array([p0[1] & 255, p1[1] & 255, p2[1] & 255], float)
            v = np.array([p0[1] >> 8, p1[1] >> 8, p2[1] >> 8], float)
            tu = np.clip((b @ u).astype(int), 0, page.shape[1] - 1)
            tv = np.clip((b @ v).astype(int), 0, page.shape[0] - 1)
            texel = page[tv, tu]
            keep = texel[:, 3] > 0
            rgb = texel[:, :3] * np.clip(shade.T / 128, 0, 2)
            py, px, zz, rgb = py[keep], px[keep], zz[keep], rgb[keep]
        else:
            n = np.cross(pos[ids[1]] - pos[ids[0]], pos[ids[2]] - pos[ids[0]])
            norm = np.linalg.norm(n)
            lam = .45 + .55 * abs(n @ light) / norm if norm else .7
            rgb = shade.T * lam
        depth[py, px] = zz
        image[py, px] = np.clip(rgb, 0, 255)
    return Image.fromarray(image.astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('model', type=Path)
    ap.add_argument('out', type=Path)
    ap.add_argument('--pages', type=Path)
    ap.add_argument('--views', default='0:0,90:0,35:20,0:89')
    ap.add_argument('--title', default='')
    a = ap.parse_args()
    model = json.loads(a.model.read_text())
    pages = {}
    if a.pages:
        for f in a.pages.glob('page-*.png'):
            pages[int(f.stem.split('-')[1])] = np.array(Image.open(f).convert('RGBA'))
    views = [tuple(float(x) for x in v.split(':')) for v in a.views.split(',')]
    sheet = Image.new('RGB', (SIZE * len(views), SIZE + 24), (24, 24, 30))
    draw = ImageDraw.Draw(sheet)
    draw.text((6, 5), a.title, fill='white')
    for i, (yaw, pitch) in enumerate(views):
        sheet.paste(render(model, pages, yaw, pitch), (i * SIZE, 24))
        draw.text((i * SIZE + 6, SIZE + 8), f'yaw {yaw:g} pitch {pitch:g}', fill=(170, 170, 180))
    sheet.save(a.out)


if __name__ == '__main__':
    main()
