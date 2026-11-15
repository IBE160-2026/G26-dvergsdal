"""Cut Rikke's twelve programme icons (egne-bilder/14-Icons.jpg: 4 x 3 grid of light lines on black) into one PNG each.

The sheet is split into 4 equal columns; rows are found from the empty horizontal bands between them. Each icon is
cropped to its lines, centred on a square canvas so all icons share one size, and recoloured to the ink colour
(#3B372F) with alpha taken from brightness 20 to 140 (a little heavier than the lace frame, so the thin lines survive scaling down). Isolated JPEG specks are dropped.

Usage (from this folder):
  python cutout-ikoner.py ../../../ux/egne-bilder/14-Icons.jpg ../mockups/ikoner 128
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

NAMES = ['fjelltur', 'hytte', 'rebus', 'middag',
         'stamp', 'frokost', 'yoga', 'bil',
         'ringer', 'lunsj', 'fest', 'avreise']
INK = (0x3B, 0x37, 0x2F)


def bands(profile, want):
    """Return `want` (start, end) runs where the profile has content, merging small gaps."""
    on = profile > 0
    runs, start = [], None
    for i, v in enumerate(on):
        if v and start is None:
            start = i
        if not v and start is not None:
            runs.append([start, i]); start = None
    if start is not None:
        runs.append([start, len(on)])
    while len(runs) > want:  # merge the pair with the smallest gap (e.g. steam above a cup)
        gaps = [runs[i + 1][0] - runs[i][1] for i in range(len(runs) - 1)]
        i = int(np.argmin(gaps))
        runs[i][1] = runs[i + 1][1]; del runs[i + 1]
    assert len(runs) == want, runs
    return runs


def main(src, outdir, size):
    a = np.asarray(Image.open(src).convert('RGB')).astype(float)
    mx = a.max(2)
    core = mx > 40
    lab, n = nd.label(core)
    sizes = nd.sum(core, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 25])
    alpha = np.clip((mx - 20) / (140 - 20), 0, 1) * nd.binary_dilation(keep, iterations=4)
    h, w = mx.shape
    rows = bands(keep.sum(1), 3)
    os.makedirs(outdir, exist_ok=True)
    crops = []
    for r0, r1 in rows:
        for c in range(4):
            c0, c1 = c * w // 4, (c + 1) * w // 4
            cell = alpha[r0:r1, c0:c1]
            ys, xs = np.nonzero(cell > 0.02)
            crops.append(cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    # One canvas size for all icons, so every line has the same weight and the icons keep their drawn sizes.
    side = int(max(max(c.shape) for c in crops) * 1.06)
    for k, crop in enumerate(crops):
        sq = np.zeros((side, side))
        oy, ox = (side - crop.shape[0]) // 2, (side - crop.shape[1]) // 2
        sq[oy:oy + crop.shape[0], ox:ox + crop.shape[1]] = crop
        rgba = np.zeros((side, side, 4), np.uint8)
        rgba[..., :3] = INK
        rgba[..., 3] = (sq * 255).astype(np.uint8)
        im = Image.fromarray(rgba, 'RGBA').resize((size, size), Image.LANCZOS)
        out = os.path.join(outdir, f'ikon-{k + 1:02d}-{NAMES[k]}.png')
        im.save(out, optimize=True)
        print(out, im.size)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
