"""The page shell shared by every page: head, header, footer, and small HTML helpers."""

import json
from html import escape

SITE = "https://spoolhand.app"
EMAIL = "hello@spoolhand.app"
STORE_NAME = "Spoolhand: Pipefitter Calc"
PRICE = "$19.99"
DISCLAIMER = "Verify critical dimensions against the current standard before fabrication."

# Set at release (plan Task 10): the App Store page and the provider token, so the button links
# with a campaign (`ct=site-<page>`) that App Store Connect counts without analytics on the site.
APP_STORE_URL = "https://apps.apple.com/app/apple-store/id6837216630"
PROVIDER_TOKEN = "129114170"


def esc(text) -> str:
    return escape(str(text), quote=True)


def store_button(page: str, extra_class: str = "") -> str:
    """The App Store button: "Coming soon" until the app is live, then a campaign link."""
    cls = f"store {extra_class}".strip()
    if APP_STORE_URL is None:
        return (f'<p class="{cls} store-soon"><span class="store-line">Coming soon to the App Store</span>'
                f'<span class="store-sub">{PRICE} once · iPhone and iPad</span></p>')
    query = f"?pt={PROVIDER_TOKEN}&ct=site-{page}&mt=8" if PROVIDER_TOKEN else ""
    return (f'<a class="{cls}" href="{esc(APP_STORE_URL + query)}"><span class="store-line">Get it on the App Store</span>'
            f'<span class="store-sub">{PRICE} once · iPhone and iPad</span></a>')


NAV = [
    ("/pipe-offset-calculator/", "Pipe offset"),
    ("/rolling-offset-calculator/", "Rolling offset"),
    ("/elbow-takeout-chart/", "Takeout chart"),
]


def header(path: str) -> str:
    current = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{href}"{current if href == path else ""}>{label}</a></li>' for href, label in NAV
    )
    return f"""<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="/"{current if path == "/" else ""}>
      <img src="/static/img/icon-128.png" width="36" height="36" alt="">
      <span>Spoolhand</span>
    </a>
    <nav aria-label="Free tools"><ul>{links}</ul></nav>
  </div>
</header>"""


def footer(edition: str) -> str:
    tools = "".join(f'<li><a href="{href}">{label} calculator</a></li>' if "chart" not in href
                    else f'<li><a href="{href}">Elbow takeout chart</a></li>' for href, label in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <h2>Free tools</h2>
      <ul>{tools}</ul>
    </div>
    <div>
      <h2>Spoolhand</h2>
      <ul>
        <li><a href="/">The app</a></li>
        <li><a href="/support/">Support</a></li>
        <li><a href="/privacy/">Privacy</a></li>
      </ul>
    </div>
    <div>
      <h2>Contact</h2>
      <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>{DISCLAIMER}</p>
    <p>© 2026 Interactive Media · Reference data edition {esc(edition)}</p>
  </div>
</footer>"""


def page(path: str, title: str, description: str, main: str, *, edition: str, version: str,
         jsonld: list | None = None, scripts: tuple = ()) -> str:
    canonical = SITE + path
    index = ('<meta name="robots" content="noindex">' if path == "/404.html"
             else f'<link rel="canonical" href="{canonical}">')
    ld = "".join(
        f'\n<script type="application/ld+json">{json.dumps(item, ensure_ascii=False)}</script>' for item in (jsonld or [])
    )
    js = "".join(f'\n<script type="module" src="{src}?v={version}"></script>' for src in scripts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{index}
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F4F1E8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1C1D1F" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spoolhand">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/static/img/icon-512.png">
<link rel="icon" href="/static/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/static/img/apple-touch-icon.png">
<link rel="preload" href="/static/fonts/barlow-semi-condensed-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/static/css/site.css?v={version}">{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(path)}
<main id="main">
{main}
</main>
{footer(edition)}{js}
</body>
</html>
"""


def source_list(sources: list, ids: list) -> str:
    """The catalogs behind a set of values, in the order given, as a list with links."""
    by_id = {s["id"]: s for s in sources}
    items = []
    for source_id in ids:
        s = by_id[source_id]
        items.append(
            f'<li><a href="{esc(s["url"])}" rel="nofollow">{esc(s["title"])}</a>'
            f'<span class="source-meta">{esc(s["publisher"])} · retrieved {esc(s["retrieved"])}</span></li>'
        )
    return f'<ul class="sources">{"".join(items)}</ul>'
