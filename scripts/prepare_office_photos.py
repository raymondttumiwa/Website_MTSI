"""Create polished website photographs from the original Green Lake office photos.

Requires Pillow and NumPy. Originals remain untouched. Edits are limited to
framing, colour balance, tonal adjustments, and light sharpening.
"""

from pathlib import Path
import json

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "GreenLake Company Pictures"
OUTPUT = ROOT / "figs" / "office"

# Crops remove excess ceiling/floor while retaining the photographed premises.
PHOTOS = [
    dict(name="entrance", source="WhatsApp Image 2026-10-10 at 01.19.16 (1).jpeg",
         crop=(.025, .025, .975, .985), gamma=.94, balance=(1.0, 1.0, 1.0), focus=(.5, .35)),
    dict(name="reception", source="WhatsApp Image 2026-10-10 at 01.19.16 (2).jpeg",
         crop=(0, .22, 1, .985), gamma=.91, balance=(.99, 1.0, 1.02), focus=(.5, .78)),
    dict(name="meeting-room", source="WhatsApp Image 2026-10-10 at 01.19.13 (1).jpeg",
         crop=(0, .19, 1, .97), gamma=.91, balance=(1.0, 1.01, 1.025), focus=(.5, .48)),
    dict(name="visitor-lounge", source="WhatsApp Image 2026-10-10 at 01.19.12.jpeg",
         crop=(0, .29, 1, .96), gamma=.87, balance=(.99, 1.0, 1.025), focus=(.5, .64)),
    dict(name="workspace", source="WhatsApp Image 2026-10-10 at 01.19.18.jpeg",
         crop=(.015, .025, .985, .97), gamma=.93, balance=(.995, 1.0, 1.02), focus=(.5, .6)),
]


def prepare_photo(photo):
    original = ImageOps.exif_transpose(Image.open(SOURCE / photo["source"])).convert("RGB")
    box = tuple(round(value * (original.width if i % 2 == 0 else original.height))
                for i, value in enumerate(photo["crop"]))
    image = original.crop(box)
    image = ImageOps.autocontrast(image, cutoff=.3, preserve_tone=True)
    values = np.asarray(image, dtype=np.float32) / 255
    values = np.clip(values * np.array(photo["balance"], dtype=np.float32), 0, 1)
    values = np.power(values, photo["gamma"])
    image = Image.fromarray(np.uint8(np.clip(values * 255 + .5, 0, 255)))
    image = ImageEnhance.Color(image).enhance(.97)
    image = ImageEnhance.Contrast(image).enhance(1.025)
    image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=3))

    # Re-encoding removes camera metadata from public derivatives.
    large = OUTPUT / f"{photo['name']}-large.jpg"
    image.save(large, quality=89, optimize=True, progressive=True)
    ratio = (16, 9) if photo["name"] == "entrance" else (4, 3)
    widths = [720, 1440] if photo["name"] == "entrance" else [480, 960]
    derivatives = []
    for width in widths:
        size = (width, round(width * ratio[1] / ratio[0]))
        preview = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS,
                               centering=photo["focus"])
        path = OUTPUT / f"{photo['name']}-{width}.webp"
        preview.save(path, quality=84, method=6)
        derivatives.append(dict(file=str(path.relative_to(ROOT)), width=width,
                                height=size[1], bytes=path.stat().st_size))
    return dict(name=photo["name"], source=photo["source"],
                edit="Crop, gentle colour balance and shadow lift, light sharpening; no scene changes.",
                crop=photo["crop"], gamma=photo["gamma"],
                large=str(large.relative_to(ROOT)), derivatives=derivatives)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = [prepare_photo(photo) for photo in PHOTOS]
    (OUTPUT / "photo-edits.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for photo in manifest:
        total = sum(item["bytes"] for item in photo["derivatives"])
        print(f"{photo['name']}: website derivatives {total / 1024:.0f} KB")


if __name__ == "__main__":
    main()
