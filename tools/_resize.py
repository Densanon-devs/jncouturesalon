"""
Cap salon photos at the size the site actually paints them.

Rather than a flat pixel cap, the budget is derived from the CSS. Each photo
sits in a fixed-aspect box with `object-fit: cover`, so the browser scales it
by `max(cellW/w, cellH/h)` and crops the overflow. A portrait photo in a
landscape box is therefore sized by its WIDTH, and a flat long-edge cap
starves it - that mistake makes the site upscale, which looks worse than
doing nothing.

The binding case is a PHONE, not the desktop grid. At <=480px the gallery
and team grids both collapse to `1fr`, so a cell is the full container:
480 - 48px of padding = 432 css px, and at 3x DPR that is 1296 device px --
wider than any desktop cell. Sizing for the desktop grid would ship soft
photos to the device clients actually browse a salon on.

  gallery   <=480px: 1fr, aspect-ratio 4/3 -> 432x324 css -> 1296x972
            (desktop is only 389x292 css -> 778x584, so mobile wins)
  interior  <=768px: full width, aspect-ratio 4/3 -> 1296x972
  team      <=480px: 1fr, aspect-ratio 3/4 -> 1296x1728

A photo is only resized when it is comfortably above what its cell needs
(MARGIN), and never below it. Anything already at or under budget is left
completely alone - re-encoding a small JPEG just adds generation loss for
no saving.

Note: several team and gallery photos are ALREADY SMALLER than their cell
needs, so the live site is upscaling them today. This script reports those
but does not touch them; they want re-shooting or re-exporting, not
compression.

Originals are recoverable from git history.

Usage:
    python tools/_resize.py --dry-run
    python tools/_resize.py
"""
import argparse
import io
import sys
from pathlib import Path

from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parent.parent
SRC_DIR = REPO / "site" / "images"

# folder -> (cell width, cell height) in device pixels, mobile 3x worst case
CELLS = {
    "gallery": (1296, 972),
    "interior": (1296, 972),
    "team": (1296, 1728),
}

# Only bother resizing when the photo is at least this much bigger than its
# cell needs; below that the saving is not worth a fresh JPEG generation.
MARGIN = 1.25
JPEG_QUALITY = 90


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not SRC_DIR.exists():
        print(f"Source dir not found: {SRC_DIR}")
        return 1

    before = after = 0
    changed = 0
    undersized = []

    for f in sorted(SRC_DIR.rglob("*")):
        if f.suffix.lower() not in (".jpg", ".jpeg") or not f.is_file():
            continue
        folder = f.parent.name
        cell = CELLS.get(folder)
        size_before = f.stat().st_size
        before += size_before
        label = f"{folder}/{f.name}"

        if cell is None:
            after += size_before
            continue

        with Image.open(f) as raw:
            im = ImageOps.exif_transpose(raw)
            w, h = im.size
            cw, ch = cell
            cover = max(cw / w, ch / h)   # what the browser will scale by

            if cover > 1.0:
                undersized.append((label, (w, h), (round(w * cover), round(h * cover))))
                after += size_before
                continue

            if cover > 1.0 / MARGIN:
                after += size_before
                print(f"  {label:44s} {w}x{h} close to budget, skipped")
                continue

            # Smallest source that still fills the cell without upscaling.
            nw, nh = max(1, round(w * cover)), max(1, round(h * cover))
            out = im.convert("RGB").resize((nw, nh), Image.LANCZOS)

            if args.dry_run:
                buf = io.BytesIO()
                out.save(buf, "JPEG", quality=JPEG_QUALITY,
                         optimize=True, progressive=True)
                size_after = len(buf.getvalue())
            else:
                out.save(f, "JPEG", quality=JPEG_QUALITY,
                         optimize=True, progressive=True)
                size_after = f.stat().st_size

        after += size_after
        changed += 1
        pct = 100 - (size_after * 100 // size_before)
        print(f"  {label:44s} {w}x{h} -> {nw}x{nh}  "
              f"{size_before // 1024:>4d} KB -> {size_after // 1024:>4d} KB  (-{pct}%)")

    if undersized:
        print("\n  Already SMALLER than their slot - the site upscales these "
              "today. Not touched:")
        for label, have, need in undersized:
            print(f"    {label:42s} has {have[0]}x{have[1]}, slot wants "
                  f"{need[0]}x{need[1]}")

    verb = "would shrink" if args.dry_run else "shrank"
    total_pct = 100 - (after * 100 // before) if before else 0
    print(f"\n  {verb} {changed} file(s): {before // 1024} KB -> "
          f"{after // 1024} KB  (-{total_pct}%)")
    if args.dry_run:
        print("  (dry run - nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
