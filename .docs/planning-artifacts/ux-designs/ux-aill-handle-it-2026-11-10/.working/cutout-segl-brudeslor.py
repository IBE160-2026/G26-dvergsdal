"""Cut the couple's seal (19) and gypsophila divider (20) out of their cream backgrounds.

Usage: python -I cutout.py <inspirasjon-dir> <out-dir>
Seal: solid body (everything not connected to the black background), feathered edge.
Flowers: 'colour to alpha' against the flat background, so white petals stay white on any panel.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src, out = Path(sys.argv[1]), Path(sys.argv[2])

def save_scaled(rgba, width, path):
    im = Image.fromarray(rgba.astype(np.uint8), "RGBA").convert("RGBa")
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS).convert("RGBA")
    im.save(path, optimize=True)
    print(path.name, im.size, path.stat().st_size, "bytes")

# ---- Seal ----
# Version 2 of 19-Stamp.jpg has a black background (no paper, no shadow). The body is everything
# not connected to the corner; the edge is feathered by one pixel. The page adds its own drop shadow.
a = np.asarray(Image.open(src / "19-Stamp.jpg").convert("RGB")).astype(float)
d = a.max(-1)
body = Image.fromarray(((d > 28) * 255).astype(np.uint8)).copy()  # copy: floodfill needs a writable image
ImageDraw.floodfill(body, (0, 0), 128)
m = np.asarray(body) != 128
m_img = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.3))
alpha = np.asarray(m_img) / 255.0
ys, xs = np.where(alpha > 0.02)
pad = 4
y0, y1, x0, x1 = max(0, ys.min() - pad), ys.max() + pad, max(0, xs.min() - pad), xs.max() + pad
rgba = np.dstack([a, alpha * 255])[y0:y1, x0:x1]
save_scaled(rgba, 200, out / "segl-19.png")

# ---- Gypsophila ----
a = np.asarray(Image.open(src / "20-Flowers.jpg").convert("RGB")).astype(float)
border = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
bg = np.median(border, axis=0)  # the flat background colour, measured from the image edges
print("flower background", bg)
diff = a - bg
up = np.where(diff > 0, diff / (255 - bg), 0)
down = np.where(diff < 0, -diff / bg, 0)
al = np.maximum(up, down).max(-1)
al = np.clip((al - 0.06) / 0.94, 0, 1)
al[np.abs(diff).max(-1) <= 5] = 0
safe = np.maximum(al, 1e-3)[..., None]
rgb = np.clip(bg + diff / safe, 0, 255)
ys, xs = np.where(al > 0.03)
pad = 8
y0, y1, x0, x1 = max(0, ys.min() - pad), ys.max() + pad, max(0, xs.min() - pad), xs.max() + pad
rgba = np.dstack([rgb, al * 255])[y0:y1, x0:x1]
save_scaled(rgba, 640, out / "brudeslor-20.png")
