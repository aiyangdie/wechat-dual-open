"""Convert user-provided PNG to multi-size ICO for exe embedding."""
from pathlib import Path

from PIL import Image

SRC = Path(
    r"C:\Users\aike1\.cursor\projects\c-Users-aike1-Downloads\assets"
    r"\c__Users_aike1_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images"
    r"_________-332de7ad-1653-4e25-9dce-3fda0cf528bd.png"
)
OUT_DIR = Path(__file__).resolve().parent
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]


def main():
    img = Image.open(SRC).convert("RGBA")
    # Trim bottom-right watermark band (~8% height)
    w, h = img.size
    img = img.crop((0, 0, w, int(h * 0.92)))

    # Square center crop if needed
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    master = img.resize((256, 256), Image.Resampling.LANCZOS)
    master.save(OUT_DIR / "user-dual-preview.png", "PNG")

    ico_path = OUT_DIR / "user-dual.ico"
    master.save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in ICO_SIZES],
    )

    # verify
    check = Image.open(ico_path)
    sizes = []
    i = 0
    while True:
        try:
            check.seek(i)
            sizes.append(check.size)
            i += 1
        except EOFError:
            break
    print(f"ICO: {ico_path} frames={sizes}")


if __name__ == "__main__":
    main()
