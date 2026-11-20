"""Prepare Rikke's images for the site (Story 1.4b, UX-DR4, NFR-7).

Reads the approved sources in `.docs/planning-artifacts/` and writes every image
the guest pages use to `static/img/`. Nothing is drawn here: the seal, the
gypsophila, the lily garlands, the lace frame and the programme icons are
Rikke's cutouts from the UX work (DESIGN.md > Shapes), and the illustration and
photos are her own files and the venue's photos (permission: EXPERIENCE.md >
Inspiration & Anti-patterns).

It also writes the link-preview image `forhandsvisning.jpg` (Story 1.4c, FR-4,
AD-15): a centre crop of the same watercolour at 1000 x 525 (1.91:1, at least
600 x 315 so Messenger shows the large card). Every guest link shows this one
image, so it names nobody and carries no seal, initials, date or place. No page
loads it; only apps that build a link preview fetch it.

Rules (spec 1.4b, NFR-7: front page usable in under 3 seconds on 4G):
- every file is at most twice its largest display width, and never upscaled;
- photos and the illustration become progressive, optimised JPEG without
  metadata; cutouts and icons become palette PNG (256 colours, alpha kept);
- no WebP or AVIF, so old iPads show every image.

Run from the repository root; the output is the same every time, so a second
run leaves `git status` clean:

    uvx --with pillow==13.0.0 python -I tools/prepare_images.py

Pillow is only needed for this script, never by the app, so it is not a
project dependency. `static/img/README.md` lists each file with its source.
"""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PLANNING = ROOT / ".docs" / "planning-artifacts"
MOCKUPS = PLANNING / "ux-designs" / "ux-aill-handle-it-2026-11-10" / "mockups"
OWN_IMAGES = PLANNING / "ux" / "egne-bilder"
VENUE = PLANNING / "ux" / "stedet"
OUT = ROOT / "static" / "img"

PAGE_GREEN = (0x5A, 0x6C, 0x48)  # DESIGN.md colors.page-green, behind the apple-touch icon
JPEG_QUALITY = 76
FAVICON_SIZE = 32
TOUCH_ICON_SIZE = 180
TOUCH_ICON_SEAL = 148  # the seal's box inside the touch icon, so iOS's rounded corners miss it

# (target, source, file width): file width is twice the display width (DESIGN.md
# components), or the source width when the source is smaller.
CUTOUTS = [
    ("segl.png", MOCKUPS / "segl.png", 148),  # wax seal, 74px
    ("brudeslor.png", MOCKUPS / "brudeslor.png", 448),  # gypsophila, 224px in the hero
    ("lilje-topp.png", MOCKUPS / "lilje-topp.png", 592),  # lily garland, 296px
    ("lilje-bunn.png", MOCKUPS / "lilje-bunn.png", 592),
    ("blonde.png", MOCKUPS / "blonde.png", 320),  # lace frame, 136px / 220px; source is 320
]
ICON_NAMES = [
    "fjelltur",
    "hytte",
    "rebus",
    "middag",
    "stamp",
    "frokost",
    "yoga",
    "bil",
    "ringer",
    "lunsj",
    "fest",
    "avreise",
]
ICON_WIDTH = 112  # programme icons, 56px
PHOTOS = [
    ("illustrasjon.jpg", OWN_IMAGES / "04-Illustration.jpg", 524),  # hero illustration, 262px
    ("oss-strand.jpg", MOCKUPS / "us1-utsnitt.jpg", 400),  # the couple, front-page topic row
    ("oss-utsikt.jpg", OWN_IMAGES / "13-Us2.jpg", 440),  # the couple, Vår historie, 220px
    ("sted-middag.jpg", VENUE / "01-Venue.jpg", 440),  # Programmet topic row and sheet
    ("sted-tunet.jpg", VENUE / "03-Venue.jpg", 440),  # Praktisk topic row, Hardingasete sheet
    ("sted-kirka.jpg", VENUE / "18-Kirka.jpg", 440),  # Vielsen sheet
    ("sted-omradet.jpg", VENUE / "12-Area.jpg", 440),  # Området rundt sheet
]
# Link preview (og:image, Story 1.4c, FR-4): the hero watercolour, centre-cropped.
PREVIEW = ("forhandsvisning.jpg", OWN_IMAGES / "04-Illustration.jpg", (1000, 525))


def scaled(image: Image.Image, width: int) -> Image.Image:
    """`image` at `width` pixels wide (LANCZOS), never wider than the source.

    Transparent images are scaled with premultiplied alpha, so the colour of
    fully transparent pixels never bleeds into the edges.
    """
    width = min(width, image.width)
    if width == image.width:
        return image
    height = round(image.height * width / image.width)
    if image.mode == "RGBA":
        premultiplied = image.convert("RGBa").resize((width, height), Image.Resampling.LANCZOS)
        return premultiplied.convert("RGBA")
    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_png(image: Image.Image, name: str) -> None:
    """A 256-colour palette PNG that keeps the alpha channel."""
    palette = image.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
    palette.save(OUT / name, optimize=True)


def save_jpeg(image: Image.Image, name: str) -> None:
    """A progressive, optimised JPEG with no EXIF or other metadata."""
    image.save(OUT / name, quality=JPEG_QUALITY, optimize=True, progressive=True)


def open_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def fit_square(image: Image.Image, size: int) -> Image.Image:
    """`image` scaled to fit inside a `size` x `size` square, keeping its shape,
    so a replacement seal of any shape can never overflow the icon."""
    premultiplied = ImageOps.contain(image.convert("RGBa"), (size, size), Image.Resampling.LANCZOS)
    return premultiplied.convert("RGBA")


def centred(image: Image.Image, size: int, background: tuple[int, ...]) -> Image.Image:
    """`image` centred on a square canvas of `size` pixels."""
    canvas = Image.new("RGBA", (size, size), background)
    canvas.alpha_composite(image, ((size - image.width) // 2, (size - image.height) // 2))
    return canvas


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ikoner").mkdir(exist_ok=True)

    for name, source, width in CUTOUTS:
        save_png(scaled(open_rgba(source), width), name)

    for number, icon in enumerate(ICON_NAMES, start=1):
        name = f"ikon-{number:02d}-{icon}.png"
        save_png(scaled(open_rgba(MOCKUPS / "ikoner" / name), ICON_WIDTH), f"ikoner/{name}")

    # Favicon from the seal (DESIGN.md > Wax seal): transparent at 32px; the
    # apple-touch icon on page-green, since iOS paints transparency black.
    seal = open_rgba(MOCKUPS / "segl.png")
    favicon = centred(fit_square(seal, FAVICON_SIZE), FAVICON_SIZE, (0, 0, 0, 0))
    save_png(favicon, "favicon-32.png")
    touch = centred(fit_square(seal, TOUCH_ICON_SEAL), TOUCH_ICON_SIZE, (*PAGE_GREEN, 255))
    save_png(touch.convert("RGB"), "apple-touch-icon.png")  # opaque: no alpha in the palette

    for name, source, width in PHOTOS:
        photo = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
        save_jpeg(scaled(photo, width), name)

    name, source, size = PREVIEW
    illustration = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    if illustration.width < size[0] or illustration.height < size[1]:
        # ImageOps.fit would quietly upscale a smaller replacement (never upscale).
        raise SystemExit(f"{source.name} is {illustration.size}; the preview needs {size}")
    save_jpeg(ImageOps.fit(illustration, size, Image.Resampling.LANCZOS), name)


if __name__ == "__main__":
    main()
