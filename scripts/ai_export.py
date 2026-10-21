#!/usr/bin/env python3
"""SVG -> .ai exporter.

Modern .ai files are PDF-based: Illustrator opens a conforming PDF
payload with an .ai extension natively, paths stay editable.
Route: SVG -(cairosvg)-> PDF payload -> write as .ai.
The SVG remains the editable master source; edit it and re-export.

Usage: ai_export.py in.svg out.ai
"""
import sys

def main(src, out):
    import cairosvg
    pdf = cairosvg.svg2pdf(url=src)
    with open(out, 'wb') as f:
        f.write(pdf)
    head = pdf[:8]
    assert head.startswith(b'%PDF'), f'bad payload: {head}'
    print(f'{out} written, {len(pdf)} bytes, header {head.decode()}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
