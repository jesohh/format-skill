#!/usr/bin/env python3
"""Export self-contained local SVG as PDF-compatible AI; never overwrite."""
import re
import sys
from pathlib import Path
from safe_output import new_output

def main(src, out):
    import cairosvg
    from defusedxml import ElementTree as ET
    out = new_output(out, src)
    data = Path(src).read_bytes()
    root = ET.fromstring(data)
    for element in root.iter():
        if element.tag.rsplit('}', 1)[-1] in ('style', 'script', 'foreignObject'):
            raise ValueError('Embedded styles, scripts and foreign objects are disabled')
        for key, value in element.attrib.items():
            if key.rsplit('}', 1)[-1] in ('href', 'src') and not value.startswith('#'):
                raise ValueError('External references are disabled')
            if 'url' in value.lower() or '@import' in value.lower():
                raise ValueError('CSS resource references are disabled')
    def deny_fetch(*args, **kwargs):
        raise ValueError('Resource loading is disabled')
    pdf = cairosvg.surface.PDFSurface.convert(bytestring=data, url_fetcher=deny_fetch)
    if not pdf.startswith(b'%PDF'):
        raise ValueError('Invalid PDF output')
    with open(out, 'xb') as stream:
        stream.write(pdf)
    print(f'AI-compatible PDF -> {out}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
