"""Cut Rikke's lilies (21-FlowersTop/Bottom) and lace frame (23-Frame) out of their black backgrounds.

Transparency comes from brightness: the brightest channel from 14 to 70 ramps from clear to solid, and the
dark edge is un-mixed (colour divided by alpha), so no black fringe remains. Isolated JPEG specks are dropped.
With a colour argument (hex, no '#') the image is recoloured to that colour and its alpha is taken from
brightness 20 to 200, which suits the one-colour lace frame.

Usage (from this folder):
  python cutout-liljer-blonde.py ../../../ux/inspirasjon/21-FlowersTop.jpg    ../mockups/lilje-topp-21.png 760
  python cutout-liljer-blonde.py ../../../ux/inspirasjon/21-FlowersBottom.jpg ../mockups/lilje-bunn-21.png 760
  python cutout-liljer-blonde.py ../../../ux/inspirasjon/23-Frame.jpg         ../mockups/blonde-23.png 320 EBE4D5
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd


def main(src, out, width, recolor=''):
    a = np.asarray(Image.open(src).convert('RGB')).astype(float)
    mx = a.max(2)
    core = mx > 40
    lab, n = nd.label(core)
    sizes = nd.sum(core, lab, range(1, n + 1))
    big = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 25])
    near = nd.binary_dilation(big, iterations=4)
    if recolor:
        c = tuple(int(recolor[i:i + 2], 16) for i in (0, 2, 4))
        rgb = np.empty_like(a)
        rgb[...] = c
        alpha = np.clip((mx - 20) / (200 - 20), 0, 1) * near
    else:
        alpha = np.clip((mx - 14) / (70 - 14), 0, 1) * near
        rgb = np.where(alpha[..., None] > 0, np.clip(a / np.maximum(alpha, 1e-3)[..., None], 0, 255), 0)
    im = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA')
    im = im.crop(im.getbbox())
    im = im.resize((width, round(width * im.height / im.width)), Image.LANCZOS)
    im.save(out, optimize=True)
    print(out, im.size)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else '')
