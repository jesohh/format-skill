from safe_output import new_output
#!/usr/bin/env python3
"""Layered PSD writer / editor (psd-tools).

Create from a job JSON:
  {"width":1200,"height":1600,"mode":"RGB"|"CMYK","dpi":300,
   "layers":[{"name":"背景","image":"bg.png","left":0,"top":0,"opacity":255},
             {"name":"主体","image":"fg.png","left":100,"top":200}],
   "out":"poster.psd"}
  Layer order in JSON = bottom -> top. Images are placed at left/top;
  layer bbox = the image's own size (crop/pad images beforehand).

Edit an existing PSD:
  --edit in.psd --replace "图层名=新图.png" --rename "旧名=新名"
  --hide 图层名 --out out.psd
  Replace requires the new image to have the SAME pixel size as the
  layer it replaces (resize it first); position is preserved.

IRON RULE (fire-poster lesson, 2026-10-21): always write a REAL merged
composite into the file header. A blank/absent composite makes some
Photoshop builds and viewers refuse or misrender the file.
"""
import sys, os, json, zlib, argparse
from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer
from psd_tools.constants import Compression


def pil_composite(size, mode, layers):
    """layers: list of (PIL image, left, top) bottom->top. Returns merged PIL."""
    base_mode = 'RGBA' if mode == 'RGB' else 'CMYK'
    canvas = Image.new('RGBA', size, (0, 0, 0, 0))
    for img, left, top in layers:
        canvas.alpha_composite(img.convert('RGBA'), (left, top))
    if base_mode == 'CMYK':
        bg = Image.new('CMYK', size, (0, 0, 0, 0))
        rgb = canvas.convert('RGB')
        return Image.merge('CMYK', rgb.convert('CMYK').split())
    return canvas.convert('RGB')


def write_composite(psd, comp_pil):
    rec = psd._record
    rec.image_data.compression = Compression.ZIP
    data = b''.join(ch.tobytes() for ch in comp_pil.split())
    rec.image_data.data = zlib.compress(data, 6)
    psd._updated = False


def add_resolution(psd, dpi):
    """ResolutionInfo block (16 bytes): fixed-point dpi + unit codes (1=ppi/inch)."""
    try:
        import struct
        from psd_tools.psd.image_resources import ImageResource
        from psd_tools.constants import Resource
        d = int(dpi) << 16
        data = struct.pack('>IHHIHH', d, 1, 1, d, 1, 1)
        psd._record.image_resources[Resource.RESOLUTION_INFO] = ImageResource(
            key=Resource.RESOLUTION_INFO, data=data)
    except Exception as e:
        print(f'warn: dpi resource skipped ({e})', file=sys.stderr)


def create(job):
    job['out'] = new_output(job['out'])
    W, H, mode = job['width'], job['height'], job.get('mode', 'RGB')
    psd = PSDImage.new(mode, (W, H))
    placed = []
    for spec in job['layers']:
        img = Image.open(spec['image'])
        if mode == 'CMYK':
            img = img.convert('CMYK')
        elif mode == 'RGB':
            img = img.convert('RGB')
        layer = PixelLayer.frompil(img, psd)
        layer.name = spec['name']   # setter routes non-macroman names to luni block
        layer.left, layer.top = spec.get('left', 0), spec.get('top', 0)
        layer.opacity = spec.get('opacity', 255)
        psd.append(layer)
        placed.append((Image.open(spec['image']), layer.left, layer.top))
    comp = pil_composite((W, H), mode, placed)
    if job.get('dpi'):
        add_resolution(psd, job['dpi'])
    psd.save(job['out'])           # first save so record exists fully
    psd2 = PSDImage.open(job['out'])
    write_composite(psd2, comp)
    psd2.save(job['out'])
    return job['out']


def edit(args):
    args.out = new_output(args.out, args.edit)
    psd = PSDImage.open(args.edit)
    by_name = {l.name: l for l in psd.descendants()}
    if args.replace:
        name, path = args.replace.split('=', 1)
        old = by_name[name]
        img = Image.open(path)
        if img.size != (old.width, old.height):
            raise SystemExit(f'replace size mismatch: layer {old.width}x{old.height} vs image {img.size}')
        img = img.convert({1: 'RGB', 4: 'CMYK'}.get(psd.color_mode, 'RGB'))
        chans = img.split()
        ids = [ci.id for ci in old._record.channel_info]
        for cd, cid in zip(old._channels, ids):
            if cid < 0 or cid >= len(chans):
                continue  # alpha/extra channels left untouched
            cd.compression = Compression.ZIP
            cd.set_data(chans[cid].tobytes(), old.width, old.height, 8, 1)
    if args.rename:
        old_name, new_name = args.rename.split('=', 1)
        by_name[old_name].name = new_name
    if args.hide:
        by_name[args.hide].visible = False
    out = args.out
    psd.save(out)
    # refresh composite after edit
    comp = psd.composite()
    if comp is not None:
        psd2 = PSDImage.open(out)
        write_composite(psd2, comp.convert({1: 'RGB', 4: 'CMYK'}.get(psd.color_mode, 'RGB')))
        psd2.save(out)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('job', nargs='?', help='job JSON for create mode')
    ap.add_argument('--edit')
    ap.add_argument('--replace')
    ap.add_argument('--rename')
    ap.add_argument('--hide')
    ap.add_argument('--out')
    a = ap.parse_args()
    if a.edit:
        print('edited ->', edit(a))
    else:
        job = json.load(open(a.job))
        print('created ->', create(job), os.path.getsize(job['out']), 'bytes')
