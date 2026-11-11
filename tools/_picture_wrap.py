"""
Wrap each <img src="...site/images/X.jpg"> in a <picture> with a WebP source.

Ported from the same pass on dcbconstructionllc, which has been running this
pattern in production. Keeping the <img> as the fallback means nothing breaks
for a client on an old browser, and og:image meta tags are untouched because
this only rewrites <img> elements.

Idempotent: <img> tags already inside a <picture> are left alone, and tags
whose .webp sibling does not exist are skipped.

Usage:
    python tools/_picture_wrap.py --dry-run
    python tools/_picture_wrap.py
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMAGES = REPO / "site" / "images"

# Relative path (under site/images) of every available webp, e.g.
# "gallery/color-ash-blonde" -> True
WEBP = {
    p.relative_to(IMAGES).with_suffix("").as_posix()
    for p in IMAGES.rglob("*.webp")
}

IMG_RE = re.compile(
    r'<img\b(?P<before>[^>]*?)\bsrc="(?P<prefix>(?:\.\./)*)site/images/'
    r'(?P<stem>[^"]+)\.(?P<ext>jpe?g)"(?P<after>[^>]*)>',
    re.IGNORECASE,
)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


def process(path: Path, dry: bool) -> int:
    text = read(path)

    ranges = [(m.start(), m.end()) for m in
              re.finditer(r"<picture\b[^>]*>.*?</picture>", text,
                          re.DOTALL | re.IGNORECASE)]

    def inside(pos: int) -> bool:
        return any(a <= pos < b for a, b in ranges)

    wrapped = [0]

    def repl(m):
        if inside(m.start()):
            return m.group(0)
        stem = m.group("stem")
        if stem not in WEBP:
            return m.group(0)
        wrapped[0] += 1
        prefix = m.group("prefix")
        return (f'<picture><source srcset="{prefix}site/images/{stem}.webp" '
                f'type="image/webp">{m.group(0)}</picture>')

    new = IMG_RE.sub(repl, text)
    if wrapped[0] and not dry:
        path.write_text(new, encoding="utf-8")
    return wrapped[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    for html in sorted(REPO.rglob("*.html")):
        if "node_modules" in html.parts:
            continue
        n = process(html, args.dry_run)
        if n:
            total += n
            print(f"  {str(html.relative_to(REPO)):52s} -> {n} <img> wrapped")

    print(f"\n  {'would wrap' if args.dry_run else 'wrapped'} {total} tag(s)")
    print(f"  WebP siblings available: {len(WEBP)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
