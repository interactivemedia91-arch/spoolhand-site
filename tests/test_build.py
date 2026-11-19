"""The built site: page basics, sitemap, chart values, trademarks and outside hosts.

Run: python3 -I -m unittest discover -s tests -p 'test_*.py'
"""

import json
import re
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402

TRADEMARKS = ["Weldolet", "Sockolet", "Thredolet", "Victaulic", "Pipe Trades Pro", "Blue Book",
              "Calculated Industries", "PipeSnap", "FitterMaster", "PipeBase"]
PAGES = ["index.html", "pipe-offset-calculator/index.html", "rolling-offset-calculator/index.html",
         "elbow-takeout-chart/index.html", "privacy/index.html", "support/index.html", "404.html"]


def fraction_text(inches: float) -> str:
    """Nearest 1/16, ties away from zero, written like the app: 1-7/8\", 5/8\", 36\"."""
    sixteenths = int(Fraction(abs(inches)) * 16 + Fraction(1, 2))
    whole, part = divmod(sixteenths, 16)
    if part == 0:
        return f'{whole}"'
    frac = Fraction(part, 16)
    body = f"{frac.numerator}/{frac.denominator}"
    return f'{whole}-{body}"' if whole else f'{body}"'


class BuiltSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        cls.listed = build.build(cls.out)
        cls.html = {name: (cls.out / name).read_text(encoding="utf-8") for name in PAGES}
        cls.reference = json.loads((ROOT / "data" / "reference-data.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_page_has_title_description_canonical_and_one_h1(self):
        for name, html in self.html.items():
            with self.subTest(page=name):
                self.assertRegex(html, r"<title>[^<]{10,}</title>")
                self.assertRegex(html, r'<meta name="description" content="[^"]{50,}">')
                if name == "404.html":
                    self.assertIn('<meta name="robots" content="noindex">', html)
                else:
                    self.assertRegex(html, r'<link rel="canonical" href="https://spoolhand\.app/[^"]*">')
                self.assertEqual(len(re.findall(r"<h1[ >]", html)), 1)

    def test_sitemap_lists_every_page(self):
        sitemap = (self.out / "sitemap.xml").read_text(encoding="utf-8")
        for path in ["/", "/pipe-offset-calculator/", "/rolling-offset-calculator/", "/elbow-takeout-chart/",
                     "/privacy/", "/support/"]:
            self.assertIn(f"<loc>https://spoolhand.app{path}</loc>", sitemap)
        self.assertNotIn("404", sitemap)
        self.assertTrue((self.out / "robots.txt").is_file())
        self.assertEqual((self.out / "CNAME").read_text().strip(), "spoolhand.app")

    def test_chart_cells_are_the_reference_values_as_fractions(self):
        html = self.html["elbow-takeout-chart/index.html"]
        elbows = next(t for t in self.reference["tables"] if t["id"] == "bw-elbows")
        for row in elbows["rows"]:
            nps = row["key"]["nps"]
            match = re.search(rf'<tr id="nps-{re.escape(nps)}">(.*?)</tr>', html)
            self.assertIsNotNone(match, nps)
            shown = re.findall(r'<span class="in">([^<]+)</span>', match.group(1))
            expected = [fraction_text(row["cells"][c]["number"]).replace('"', "&quot;")
                        for c in ("lr90", "lr45", "sr90") if c in row["cells"]]
            self.assertEqual(shown, expected, nps)

    def test_calculators_open_solved(self):
        self.assertIn('data-cut aria-live="polite">26-3/16&quot;</output>', self.html["pipe-offset-calculator/index.html"])
        self.assertIn('data-cut aria-live="polite">30-7/8&quot;</output>', self.html["rolling-offset-calculator/index.html"])
        self.assertIn("9-1/8&quot;", self.html["pipe-offset-calculator/index.html"])      # the published example
        self.assertIn("35-1/4&quot;", self.html["rolling-offset-calculator/index.html"])

    def test_no_trademarks(self):
        for name, html in self.html.items():
            for mark in TRADEMARKS:
                with self.subTest(page=name, mark=mark):
                    self.assertNotIn(mark.lower(), html.lower())

    def test_nothing_loads_from_another_host(self):
        for name, html in self.html.items():
            for tag, attr in (("script", "src"), ("link", "href"), ("img", "src")):
                for value in re.findall(rf'<{tag}\b[^>]*\b{attr}="([^"]+)"', html):
                    with self.subTest(page=name, value=value):
                        if tag == "link" and "rel=\"canonical\"" in html and value.startswith("https://spoolhand.app"):
                            continue
                        self.assertTrue(value.startswith("/"), value)

    def test_json_ld_parses(self):
        for name, html in self.html.items():
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
                with self.subTest(page=name):
                    self.assertIn("@type", json.loads(block))

    def test_disclaimer_on_reference_pages(self):
        for name in PAGES[1:4]:
            self.assertIn("Verify critical dimensions against the current standard before fabrication.", self.html[name])


if __name__ == "__main__":
    unittest.main()
