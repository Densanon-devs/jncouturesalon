"""
Write a WebP sibling next to every JPG under site/images/.

The photos are already correctly sized for the layout (see _resize.py, which
finds nothing to shrink), so format is the only remaining lever here. WebP at
q82 measured -50% across this site's 20 photos at identical pixel dimensions.

The JPG stays in place as the <picture> fallback and as the target of the
og:image tags, which social scrapers want as JPEG.

Skips files whose .webp sibling is already newer than the .jpg, so re-running
is cheap. Drops the WebP if it comes out larger than the JPG, which happens
on small already-optimised images.

Usage:
    python tools/_webp_convert.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parent.parent
SRC_DIR = REPO / "site" / "images"

QUALITY = 82


def main():
    if not SRC_DIR.exists():
        print(f"Source dir not found: {SRC_DIR}")
        return 1

    jpgs = sorted(p for p in SRC_DIR.rglob("*")
                  if p.suffix.lower() in (".jpg", ".jpeg") and p.is_file())
    if not jpgs:
        print("No JPGs found.")
        return 1

    total_jpg = total_out = 0
    for jpg in jpgs:
        webp = jpg.with_suffix(".webp")
        jpg_size = jpg.stat().st_size
        total_jpg += jpg_size
        label = f"{jpg.parent.name}/{jpg.name}"

        if webp.exists() and webp.stat().st_mtime >= jpg.stat().st_mtime:
            total_out += webp.stat().st_size
            print(f"  {label:44s} {jpg_size // 1024:>4d} KB -> cached "
                  f"{webp.stat().st_size // 1024:>4d} KB")
            continue

        with Image.open(jpg) as raw:
            im = ImageOps.exif_transpose(raw).convert("RGB")
            im.save(webp, "WEBP", quality=QUALITY, method=6)

        webp_size = webp.stat().st_size
        if webp_size >= jpg_size:
            webp.unlink()
            total_out += jpg_size
            print(f"  {label:44s} {jpg_size // 1024:>4d} KB -> webp larger, skipped")
            continue

        total_out += webp_size
        pct = 100 - (webp_size * 100 // jpg_size)
        print(f"  {label:44s} {jpg_size // 1024:>4d} KB -> "
              f"{webp_size // 1024:>4d} KB  (-{pct}%)")

    pct = 100 - (total_out * 100 // total_jpg) if total_jpg else 0
    print(f"\n  TOTAL: {total_jpg // 1024} KB JPG -> {total_out // 1024} KB "
          f"served  (-{pct}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
