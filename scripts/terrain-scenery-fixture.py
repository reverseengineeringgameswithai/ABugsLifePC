#!/usr/bin/env python3
"""Build an unlaunched mushroom fixture in a fresh work/copies directory.

Placements JSON: [{"variant":"tall", "origin":[6000,-3200,17000]}, ...].
Origins are absolute stored units, not Flik world units. Retains each donor's
rotation/scale; original Level01 textures must remain installed. No live access.
For removal, rebuild from the mushroom-free base with omitted placements;
an empty list restores that base exactly. Never rebuild over a running stage.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'reimplementation'))
from ablpc.terrain_scenery import append_instances, digest, mushroom_template
from ablpc.terrain_scenery import scene_pointer_fields
from ablpc.terrain_all import TerrainAll

VARIANTS = {'tall': (344, 147), 'small-front': (342, 142),
            'small-back': (396, 146), 'small-far': (400, 148)}


def build(control, original, placements):
    if set(control) != {'LEVEL.DAT', 'TERRAIN.ALL', 'PLANTTER.ALL'}:
        raise ValueError('expected both level files and retained plant templates')
    if not isinstance(placements, list) or not 0 <= len(placements) <= 64:
        raise ValueError('expected zero to 64 placements')
    d, t = control['LEVEL.DAT'], control['TERRAIN.ALL']
    if not placements:
        # No allocator runs in the remove-all case; still reject invalid inputs.
        scene_pointer_fields(d)
        TerrainAll.parse(t)
        TerrainAll.parse(control['PLANTTER.ALL'])
    rows = []
    for placement in placements:
        if not isinstance(placement, dict) or set(placement) != {'variant', 'origin'}:
            raise ValueError('placement requires exactly variant and origin')
        if not isinstance(placement['variant'], str) or placement['variant'] not in VARIANTS:
            raise ValueError('unknown mapped mushroom variant')
        scene, source = VARIANTS[placement['variant']]
        template = mushroom_template(original['LEVEL.DAT'], original['TERRAIN.ALL'],
                                     scene_index=scene, source_index=source)
        d, t, row = append_instances(d, t, template, [placement['origin']])
        rows.append({'variant': placement['variant'], 'donor_scene': scene,
                     'donor_source': source, **row})
    result = {'LEVEL.DAT': d, 'TERRAIN.ALL': t, 'PLANTTER.ALL': control['PLANTTER.ALL']}
    return result, {'status': 'offline candidate; not installed or live-accepted',
                    'base_hashes': {n: digest(b) for n, b in control.items()},
                    'hashes': {n: digest(b) for n, b in result.items()},
                    'placements': placements, 'additions': rows,
                    'plant_templates_unchanged': True,
                    'scope': 'new scenery mushrooms, not seed-grown bouncing plants; Level01 atlas dependency retained'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True, help='flat fixture containing three input files')
    parser.add_argument('--original', type=Path, required=True, help='original copied LEVEL01 directory')
    parser.add_argument('--placements', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    destination, report = args.out.resolve(), args.report.resolve()
    if not destination.is_relative_to((ROOT/'work/copies').resolve()) or destination.exists():
        parser.error('output must be a fresh directory under work/copies')
    if not report.is_relative_to((ROOT/'work').resolve()) or report.exists():
        parser.error('report must be fresh under work')
    control = {n: (args.base/n).read_bytes() for n in ('LEVEL.DAT', 'TERRAIN.ALL', 'PLANTTER.ALL')}
    original = {n: (args.original/n).read_bytes() for n in ('LEVEL.DAT', 'TERRAIN.ALL')}
    placements = json.loads(args.placements.read_text())
    result, meta = build(control, original, placements)
    destination.mkdir(parents=True)
    for name, data in result.items():
        with (destination/name).open('xb') as stream:
            stream.write(data)
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open('x') as stream:
        json.dump(meta, stream, indent=2); stream.write('\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
