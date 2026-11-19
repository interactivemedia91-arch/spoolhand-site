"""Build spoolhand.app into _site/.

Usage: python3 -I tools/build.py [--out _site]

The numbers on the pages (defaults, worked examples, chart fractions) come from the calculators'
own JavaScript through `node tools/examples.mjs`, so the site can't print a different number than
its calculators. A failed build leaves the previous _site alone.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

# -I leaves the script's own directory off sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitegen import pages  # noqa: E402
from sitegen.layout import SITE, page  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def build_data(reference_path: Path) -> dict:
    output = subprocess.run(["node", str(ROOT / "tools" / "examples.mjs"), str(reference_path)],
                            check=True, capture_output=True, text=True).stdout
    return json.loads(output)


def asset_version() -> str:
    digest = hashlib.sha256()
    for path in sorted((ROOT / "static").rglob("*")):
        if path.is_file() and path.suffix in {".css", ".js"}:
            digest.update(path.read_bytes())
    return digest.hexdigest()[:10]


def build(out: Path) -> list:
    reference_path = ROOT / "data" / "reference-data.json"
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    data = build_data(reference_path)
    version = asset_version()
    built = [
        pages.home_page(data, reference),
        pages.offset_page(data, reference),
        pages.rolling_page(data, reference),
        pages.chart_page(data, reference, data["chart"]),
        pages.privacy_page(),
        pages.support_page(),
        pages.not_found_page(),
    ]
    for item in built:
        html = page(item["path"], item["title"], item["description"], item["main"], edition=reference["edition"],
                    version=version, jsonld=item["jsonld"], scripts=item["scripts"])
        target = out / (item["path"].lstrip("/") or "index.html")
        if item["path"].endswith("/"):
            target = out / item["path"].lstrip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    shutil.copytree(ROOT / "static", out / "static")
    listed = [item["path"] for item in built if item["path"].endswith("/")]
    urls = "".join(f"<url><loc>{SITE}{path}</loc></url>" for path in listed)
    (out / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (out / "CNAME").write_text("spoolhand.app\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    return listed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(ROOT / "_site"))
    args = parser.parse_args()
    out = Path(args.out)
    tmp = out.with_name(out.name + ".building")
    if tmp.exists():
        shutil.rmtree(tmp)
    try:
        listed = build(tmp)
    except (subprocess.CalledProcessError, KeyError, ValueError, OSError) as error:
        shutil.rmtree(tmp, ignore_errors=True)
        detail = getattr(error, "stderr", "") or ""
        print(f"Build stopped: {error!r}\n{detail}", file=sys.stderr)
        return 1
    if out.exists():
        shutil.rmtree(out)
    tmp.rename(out)
    print(f"Built {len(listed)} pages into {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
