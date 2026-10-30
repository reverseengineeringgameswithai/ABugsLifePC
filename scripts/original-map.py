#!/usr/bin/env python3
"""Locate Blender and open an original-level reference map with its sidebar.

`edit <folder>` opens <folder>/level.blend with tools/blender/original_map.py
registered (N -> ABLPC Map). `blender_command()` is shared with
scripts/map-original-levels.py and scripts/populate-original-map.py.
"""
import argparse
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def blender_command():
    if os.environ.get('ABLPC_BLENDER'):
        return [os.environ['ABLPC_BLENDER']]
    if shutil.which('blender'): return [shutil.which('blender')]
    if shutil.which('flatpak'):
        result = subprocess.run(['flatpak','info','org.blender.Blender'],capture_output=True)
        if result.returncode == 0: return ['flatpak','run','--talk-name=org.freedesktop.Flatpak','org.blender.Blender']
    raise RuntimeError('Blender is unavailable; install it or set ABLPC_BLENDER to its executable')


def main():
    p = argparse.ArgumentParser(description='Open an original-level reference map in Blender.')
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('edit', help='Open the map with the ABLPC Map sidebar'); a.add_argument('project', type=Path)
    a = p.parse_args()
    project = a.project.resolve()
    if not (project/'original-map.json').is_file():
        raise SystemExit(f'{project} is not an original map (no original-map.json)')
    if not project.is_relative_to((ROOT/'work').resolve()):
        raise SystemExit('Original mapping project must be below work/')
    subprocess.Popen(blender_command()+['--disable-autoexec',str(project/'level.blend'),
        '--python',str(ROOT/'tools/blender/original_map.py'),'--','register'],start_new_session=True)
    print(f'Opened original map {project / "level.blend"}')


if __name__ == '__main__':
    main()
