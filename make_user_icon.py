"""Convert assets/icon-source.png to multi-size ICO for exe embedding."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SRC = ASSETS / "icon-source.png"
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]


def main():
    if not SRC.exists():
        raise FileNotFoundError(f"Missing {SRC}")

    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    img = img.crop((0, 0, w, int(h * 0.92)))

    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    master = img.resize((256, 256), Image.Resampling.LANCZOS)
    master.save(ASSETS / "icon-preview.png", "PNG")

    ico_path = ASSETS / "user-dual.ico"
    master.save(ico_path, format="ICO", sizes=[(s, s) for s in ICO_SIZES])
    print(f"ICO: {ico_path}")


if __name__ == "__main__":
    main()
