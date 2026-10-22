from safe_output import new_output
#!/usr/bin/env python3
"""CMYK print PDF from a job JSON.

  {"image":"art.png",            # artwork INCLUDING bleed area
   "trim_mm":[100,150],          # finished size
   "bleed_mm":3, "dpi":300,
   "crop_marks":true, "out":"print.pdf"}

The PDF page = trim + 2*bleed. Crop marks are drawn in the bleed margin
when crop_marks is on. Image is converted to CMYK and embedded as JPEG.
Verify afterwards with pypdf: mediabox mm must equal trim+2*bleed.
"""
import json, sys
from PIL import Image, ImageDraw

MM = 72 / 25.4

def main(job_path):
    job = json.load(open(job_path))
    job['out'] = new_output(job['out'])
    tw, th = job['trim_mm']
    bleed = job.get('bleed_mm', 3)
    dpi = job.get('dpi', 300)
    pw, ph = tw + 2 * bleed, th + 2 * bleed
    img = Image.open(job['image']).convert('CMYK')
    target = (round(pw / 25.4 * dpi), round(ph / 25.4 * dpi))
    if img.size != target:
        img = img.resize(target, Image.LANCZOS)
    if job.get('crop_marks', True):
        rgb = img.convert('RGB')
        d = ImageDraw.Draw(rgb)
        b = bleed / 25.4 * dpi          # bleed px
        L = 5 / 25.4 * dpi              # mark length
        off = 1.5 / 25.4 * dpi
        W, H = rgb.size
        c = (0, 0, 0)
        for x0 in (b, W - b):
            d.line([(x0, 0), (x0, b - off)], fill=c, width=2)
            d.line([(x0, H - b + off), (x0, H)], fill=c, width=2)
        for y0 in (b, H - b):
            d.line([(0, y0), (b - off, y0)], fill=c, width=2)
            d.line([(W - b + off, y0), (W, y0)], fill=c, width=2)
        img = rgb.convert('CMYK')
    img.save(job['out'], 'PDF', resolution=float(dpi))
    print(f"print pdf -> {job['out']} page {pw}x{ph}mm @{dpi}dpi CMYK")

if __name__ == '__main__':
    main(sys.argv[1])
