import os
import io
from pathlib import Path

from PIL import Image
import cairosvg

ROOT = Path(r"c:\Users\infin\Documents\LMS.MARSANIX.COM\Python Full-Stack")

SVG_FILES = [
    ROOT / "Pertemuan_1" / "diagram_alur_crud.svg",
    ROOT / "Pertemuan_2" / "diagram_membangun_dari_nol.svg",
    ROOT / "Pertemuan_3" / "diagram_validasi_integrasi.svg",
    ROOT / "Pertemuan_4" / "diagram_proyek_mandiri.svg",
]


def svg_to_jpg(svg_path: Path, jpg_path: Path, scale: float = 1.0, bg=(255, 255, 255)):
    """Render SVG to PNG via CairoSVG, then convert to JPEG with white background.
    """
    # Render SVG to PNG bytes
    png_bytes = cairosvg.svg2png(url=str(svg_path), scale=scale)

    # Open PNG from bytes and convert to JPG
    with Image.open(io.BytesIO(png_bytes)) as im:
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            background = Image.new("RGB", im.size, bg)
            alpha = im.convert("RGBA").split()[-1]
            background.paste(im, mask=alpha)
            background.save(jpg_path, "JPEG", quality=95, optimize=True)
        else:
            im.convert("RGB").save(jpg_path, "JPEG", quality=95, optimize=True)


def main():
    created = []
    for svg in SVG_FILES:
        if not svg.exists():
            print(f"SKIP: {svg} not found")
            continue
        out = svg.with_name(svg.stem + "-rendered.jpg")
        try:
            svg_to_jpg(svg, out, scale=1.0)
            created.append(out)
            print(f"OK: {svg.name} -> {out.name}")
        except Exception as e:
            print(f"ERROR converting {svg}: {e}")

    if not created:
        raise SystemExit(1)


if __name__ == "__main__":
    main()