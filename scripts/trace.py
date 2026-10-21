#!/usr/bin/env python3
"""Raster -> traced vector SVG via vtracer (image-to-.ai route).

Presets:
  logo  : few colors, hard edges  (logos, icons, flat illustration)
  poster: more colors, smoother   (poster artwork, photos - expect碎路径)
Usage: trace.py in.png out.svg [logo|poster]
Then feed out.svg to ai_export.py for a .ai deliverable.
"""
import subprocess, sys, os

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin', 'vtracer')
VTRACER = BIN if os.path.exists(BIN) else 'vtracer'

PRESETS = {
    'logo':   ['--color-precision', '6', '--filter-speckle', '8',
               '--path-precision', '2', '--mode', 'spline'],
    'poster': ['--preset', 'poster', '--color-precision', '7',
               '--filter-speckle', '4', '--path-precision', '1',
               '--mode', 'spline', '--hierarchical', 'stacked'],
}

def main(src, out, preset='logo'):
    cmd = [VTRACER, '--input', src, '--output', out] + PRESETS[preset]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f'vtracer failed: {r.stderr}')
    print(f'traced -> {out} (preset {preset})')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'logo')
