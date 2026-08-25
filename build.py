#!/usr/bin/env python3
"""Build self-contained copies of the homepage from index.html.

index.html is the source of truth; it links Profile.JPG and CV.pdf as
sibling files. This inlines those assets so a single .html file stands alone.

  ./build.py                  -> dist/younghun-kim.html  (portrait + CV embedded)
  ./build.py --artifact PATH  -> same, but CV swapped for a mailto and the
                                 document skeleton stripped, for hosts that
                                 supply their own <head>/<body> and block
                                 page-initiated downloads.
"""
import argparse
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SITE = ROOT  # site files live at the repo root, where Pages serves them


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", metavar="PATH", help="write the artifact variant here")
    args = ap.parse_args()

    src = (SITE / "index.html").read_text(encoding="utf-8")
    if 'src="Profile.JPG"' not in src:
        sys.exit("index.html no longer references Profile.JPG - update build.py")

    out = src.replace('src="Profile.JPG"', f'src="{data_uri(SITE / "Profile.JPG", "image/jpeg")}"')

    if args.artifact:
        out = out.replace(
            '<a class="cv" href="CV.pdf">Curriculum Vitae (PDF)</a>',
            '<a class="cv" href="mailto:andy1220@kaist.ac.kr?subject=CV%20request">Request CV</a>',
        )
        parts = re.search(r"<head>\n(.*?)</head>\n<body>\n(.*)</body>", out, re.S)
        if not parts:
            sys.exit("could not locate head/body in index.html")
        head = re.sub(r'^<meta charset.*?<link rel="icon".*?>\n', "", parts.group(1), flags=re.S)
        dest = pathlib.Path(args.artifact)
        dest.write_text(head.rstrip() + "\n\n" + parts.group(2).rstrip() + "\n", encoding="utf-8")
    else:
        # keep the CV a real download, just carried inside the file
        out = out.replace(
            '<a class="cv" href="CV.pdf">',
            f'<a class="cv" download="Younghun-Kim-CV.pdf" '
            f'href="{data_uri(SITE / "CV.pdf", "application/pdf")}">',
        )
        dest = ROOT / "dist" / "younghun-kim.html"
        dest.parent.mkdir(exist_ok=True)
        dest.write_text(out, encoding="utf-8")

    print(f"{dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest}  ({dest.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
