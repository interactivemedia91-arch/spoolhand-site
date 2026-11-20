"""Every page's content. Numbers come from the build data (tools/examples.mjs), never typed in here."""

import math

from .calculator import calculator
from .layout import DISCLAIMER, EMAIL, PRICE, SITE, STORE_NAME, esc, source_list, store_button

PUBLISHER = {"@type": "Organization", "name": "Interactive Media"}


def web_app(name: str, path: str, description: str) -> dict:
    return {
        "@context": "https://schema.org", "@type": "WebApplication", "name": name, "url": SITE + path,
        "description": description, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
        "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": PUBLISHER,
    }


def steps_list(example: dict) -> str:
    items = "".join(
        f'<li>{esc(s["text"])}' + (f'<span class="source">{esc(s["source"])}</span>' if s.get("source") else "") + "</li>"
        for s in example["steps"]
    )
    return f'<ol class="worked-steps">{items}</ol>'


def marks_line(example: dict) -> str:
    if not example["marks"]:
        return ""
    parts = ", ".join(f'{m["label"].lower()} {esc(m["value"])}' for m in example["marks"])
    return f"<p>Before cutting each 90 to the angle, mark it along the {parts}.</p>"


def app_block(page: str, line: str) -> str:
    return f"""<section class="app-block" aria-labelledby="app-{page}">
  <div class="app-block-text">
    <h2 id="app-{page}">Keep it in your pocket</h2>
    <p>{line}</p>
    {store_button(page)}
    <p><a href="/">What's in the app</a></p>
  </div>
  <img class="app-shot" src="/static/img/app-offset.webp" width="360" height="622" loading="lazy"
    alt="Spoolhand on iPhone: a simple offset of 24 inches at 45 degrees on 6-inch long-radius 45s, cut length 26-3/16 inches.">
</section>"""


def multiplier_table() -> str:
    rows = []
    for label, degrees in [("5-5/8°", 5.625), ("11-1/4°", 11.25), ("22-1/2°", 22.5), ("30°", 30), ("45°", 45), ("60°", 60)]:
        theta = math.radians(degrees)
        rows.append(f"<tr><th scope=\"row\">{label}</th><td>{1 / math.sin(theta):.4f}</td>"
                    f"<td>{1 / math.tan(theta):.4f}</td><td>{math.tan(theta / 2):.4f}</td></tr>")
    return f"""<div class="table-wrap"><table class="data multipliers">
  <caption>Multipliers for common fitting angles</caption>
  <thead><tr><th scope="col">Angle</th><th scope="col">Travel = offset ×</th><th scope="col">Run = offset ×</th><th scope="col">Takeout of a 90 cut to it = A ×</th></tr></thead>
  <tbody>{"".join(rows)}</tbody>
</table></div>"""


def elbow_source_ids(data: dict) -> list:
    ids = []
    for size in data["sizes"]:
        for column in ("lr90", "lr45", "sr90"):
            for source_id in (size[column] or {}).get("sources", []):
                if source_id not in ids:
                    ids.append(source_id)
    return sorted(ids)


def pipe_source_ids(reference: dict) -> list:
    pipe = next(t for t in reference["tables"] if t["id"] == "pipe")
    return sorted({s for row in pipe["rows"] for s in row["cells"]["od"]["sources"]})


# ---------------------------------------------------------------- calculators

def offset_page(data: dict, reference: dict) -> dict:
    published, metric = data["offset"]["examples"]
    description = ("Free pipe offset calculator: enter the offset and the angle or run, pick the pipe size, and get "
                   "travel, run and cut length to 1/16\" with the elbow takeouts and every step shown.")
    main = f"""<div class="wrap page-head">
  <h1>Pipe offset calculator</h1>
  <p class="lede">Two elbows move the line over by the offset. Enter the offset and the angle or the run; the cut length takes off both elbows and a weld gap at each end.</p>
</div>
<div class="wrap">{calculator("offset", data["offset"]["default"], data["sizes"], data["calculatorSizes"])}</div>
<div class="wrap prose">
  <section aria-labelledby="worked">
    <h2 id="worked">A worked example</h2>
    <p>A 10" offset with a 12" run, on 6" pipe with long-radius 90s cut to the angle, and no gap. This one is from the worked examples in a handheld pipe calculator's published guide; the calculator here gives the same answers.</p>
    {steps_list(published)}
    {marks_line(published)}
    <p>Cut the pipe to <strong class="num">{esc(published["cut"])}</strong>.</p>
    <h3>The same idea in millimeters</h3>
    <p>A 600 mm offset at 45°, DN 150 long-radius 45s, a 3 mm gap:</p>
    {steps_list(metric)}
  </section>
  <section aria-labelledby="formulas">
    <h2 id="formulas">The formulas</h2>
    <ul class="formulas">
      <li><span class="formula">Travel = offset ÷ sin θ</span> and <span class="formula">run = offset ÷ tan θ</span>, θ being the fitting angle.</li>
      <li>With the run known instead: <span class="formula">travel = √(offset² + run²)</span> and <span class="formula">θ = atan(offset ÷ run)</span>.</li>
      <li><span class="formula">Cut = travel − 2 × takeout − 2 × gap</span> for butt welds: one takeout and one root gap at each end.</li>
      <li>A 90 cut to θ: <span class="formula">takeout = A × tan(θ/2)</span>, where A is the 90's center to end.</li>
    </ul>
    {multiplier_table()}
  </section>
  <section aria-labelledby="questions">
    <h2 id="questions">Questions</h2>
    <h3>Travel or cut length?</h3>
    <p>Travel is center to center between the two elbows. The cut length is the pipe you cut: the travel less both takeouts and a gap at each weld.</p>
    <h3>Which takeout does it use?</h3>
    <p>For long-radius elbows at 45°, the stock 45 from the <a href="/elbow-takeout-chart/">elbow takeout chart</a>. At any other angle, a 90 cut to the angle: A × tan(θ/2). Short-radius elbows don't come as stock 45s in the chart, so they're cut from a 90 too. For socket-weld, threaded, or a fitting you measured, open the pipe bar and choose My takeout.</p>
    <h3>Why two gaps?</h3>
    <p>The pipe has a weld at each end, and each weld has its own root gap. Set the gap to 0 for a fitting with no gap.</p>
    <h3>It says there's no pipe left to cut</h3>
    <p>The two elbows and gaps take up more than the travel. A bigger offset or a smaller angle gives a longer travel; a shorter fitting gives more pipe.</p>
    <h3>Can I work in metric?</h3>
    <p>Switch to mm. What you've typed converts, so 1/8" becomes 3.2 mm instead of resetting.</p>
  </section>
  <section aria-labelledby="sources">
    <h2 id="sources">Where the takeouts come from</h2>
    <p>Elbow center-to-end values are ASME B16.9 dimensions that agree in at least two of these catalogs:</p>
    {source_list(reference["sources"], elbow_source_ids(data))}
    <p>Pipe outside diameters, used for the cut marks:</p>
    {source_list(reference["sources"], pipe_source_ids(reference))}
    <p class="disclaimer">{DISCLAIMER}</p>
  </section>
  <p class="related">Also free: the <a href="/rolling-offset-calculator/">rolling offset calculator</a> and the <a href="/elbow-takeout-chart/">elbow takeout chart</a>.</p>
</div>
<div class="wrap">{app_block("offset", f"The app does this offline, saves it to a job and prints a cut sheet, and adds rolling offsets, laterals, miters, saddles and the fitting tables. {PRICE} once, no subscription.")}</div>"""
    return {
        "path": "/pipe-offset-calculator/",
        "title": "Pipe offset calculator: travel, run and cut length | Spoolhand",
        "description": description, "main": main,
        "jsonld": [web_app("Pipe offset calculator", "/pipe-offset-calculator/", description)],
        "scripts": ("/static/js/page.js",),
    }


def rolling_page(data: dict, reference: dict) -> dict:
    published, metric = data["rolling"]["examples"]
    description = ("Free rolling offset calculator: enter the set and roll plus the angle, run or travel, pick the pipe "
                   "size, and get true offset, travel and cut length to 1/16\" with every step shown.")
    main = f"""<div class="wrap page-head">
  <h1>Rolling offset calculator</h1>
  <p class="lede">The set and the roll move the line up and over at once. Enter both, plus the angle, the run or the travel.</p>
</div>
<div class="wrap">{calculator("rolling", data["rolling"]["default"], data["sizes"], data["calculatorSizes"])}</div>
<div class="wrap prose">
  <section aria-labelledby="worked">
    <h2 id="worked">A worked example</h2>
    <p>A 24" set and a 13" roll with a 32" run, on 6" pipe with long-radius 90s cut to the angle and a 3/32" gap. This one is from a handheld pipe calculator's published guide; the calculator here gives the same answers.</p>
    {steps_list(published)}
    {marks_line(published)}
    <p>Cut the pipe to <strong class="num">{esc(published["cut"])}</strong>.</p>
    <h3>The same idea in millimeters</h3>
    <p>A 600 mm set and a 300 mm roll at 45°, DN 150 long-radius 45s, a 3 mm gap:</p>
    {steps_list(metric)}
  </section>
  <section aria-labelledby="formulas">
    <h2 id="formulas">The formulas</h2>
    <ul class="formulas">
      <li><span class="formula">True offset = √(set² + roll²)</span>: the diagonal of the set and the roll.</li>
      <li>With the angle: <span class="formula">travel = true offset ÷ sin θ</span>, <span class="formula">run = true offset ÷ tan θ</span>.</li>
      <li>With the run: <span class="formula">travel = √(true offset² + run²)</span>, <span class="formula">θ = atan(true offset ÷ run)</span>.</li>
      <li>With the travel: <span class="formula">run = √(travel² − true offset²)</span>.</li>
      <li><span class="formula">Cut = travel − 2 × takeout − 2 × gap</span> for butt welds.</li>
    </ul>
    {multiplier_table()}
  </section>
  <section aria-labelledby="questions">
    <h2 id="questions">Questions</h2>
    <h3>Set or roll?</h3>
    <p>They're the two sides of the move, measured center to center: the set is usually the vertical one and the roll the horizontal one. Swapping them gives the same true offset, travel and cut.</p>
    <h3>What's the true offset?</h3>
    <p>The straight-line distance the pipe really moves, square to the run. Once you have it, a rolling offset works like a simple offset.</p>
    <h3>Which takeout does it use?</h3>
    <p>For long-radius elbows at 45°, the stock 45 from the <a href="/elbow-takeout-chart/">elbow takeout chart</a>; at any other angle, a 90 cut to the angle: A × tan(θ/2). For socket-weld, threaded, or a fitting you measured, choose My takeout.</p>
    <h3>The travel is too short</h3>
    <p>When you give the travel, it has to be longer than the true offset; otherwise there's no run that fits.</p>
  </section>
  <section aria-labelledby="sources">
    <h2 id="sources">Where the takeouts come from</h2>
    <p>Elbow center-to-end values are ASME B16.9 dimensions that agree in at least two of these catalogs:</p>
    {source_list(reference["sources"], elbow_source_ids(data))}
    <p>Pipe outside diameters, used for the cut marks:</p>
    {source_list(reference["sources"], pipe_source_ids(reference))}
    <p class="disclaimer">{DISCLAIMER}</p>
  </section>
  <p class="related">Also free: the <a href="/pipe-offset-calculator/">pipe offset calculator</a> and the <a href="/elbow-takeout-chart/">elbow takeout chart</a>.</p>
</div>
<div class="wrap">{app_block("rolling", f"The app does this offline, saves it to a job and prints a cut sheet, and adds parallel offsets, laterals, miters, saddles and the fitting tables. {PRICE} once, no subscription.")}</div>"""
    return {
        "path": "/rolling-offset-calculator/",
        "title": "Rolling offset calculator: true offset, travel and cut | Spoolhand",
        "description": description, "main": main,
        "jsonld": [web_app("Rolling offset calculator", "/rolling-offset-calculator/", description)],
        "scripts": ("/static/js/page.js",),
    }


# ---------------------------------------------------------------- chart

ELBOW_FIGURE = """<svg viewBox="0 -16 500 246" role="img" aria-label="A is the center to end of a 90° elbow; B is the center to end of a 45° elbow: from the end face to where the two centerlines cross.">
  <g transform="translate(10 0)">
    <path class="wall" d="M80 40 A120 120 0 0 1 200 160 L150 160 A70 70 0 0 0 80 90 Z"/>
    <path class="centerline" d="M80 65 A95 95 0 0 1 175 160"/>
    <path class="axis" d="M80 65 H175 V160"/>
    <path class="dimline" d="M80 34 V14 M175 58 V14 M80 22 H175 M182 65 H228 M182 160 H228 M216 65 V160"/>
    <text class="dim" x="127" y="16" text-anchor="middle">A</text>
    <text class="dim" x="224" y="118" text-anchor="start">A</text>
    <text class="label" x="130" y="212" text-anchor="middle">90° elbow</text>
  </g>
  <g transform="translate(290 0)">
    <path class="wall" d="M40 40 A120 120 0 0 1 124.85 75.15 L89.5 110.5 A70 70 0 0 0 40 90 Z"/>
    <path class="centerline" d="M40 65 A95 95 0 0 1 107.18 92.82"/>
    <path class="axis" d="M40 65 H79.36 L107.18 92.82"/>
    <path class="dimline" d="M40 34 V14 M79.36 58 V14 M40 22 H79.36"/>
    <text class="dim" x="60" y="16" text-anchor="middle">B</text>
    <text class="label" x="80" y="212" text-anchor="middle">45° elbow</text>
  </g>
</svg>"""


def chart_page(data: dict, reference: dict, chart_text: dict) -> dict:
    rows = []
    calc_sizes = set(data["calculatorSizes"])
    row_notes = next(t for t in reference["tables"] if t["id"] == "bw-elbows").get("rowNotes", {})
    for size in data["sizes"]:
        nps = size["nps"]
        slug = nps.replace("/", "-")
        cells = []
        for column in ("lr90", "lr45", "sr90"):
            cell = size[column]
            if not cell:
                cells.append('<td class="none"><span class="none-mark" role="img" aria-label="not in the catalogs"></span></td>')
                continue
            inches, millimeters = chart_text[nps][column]
            note = "derived" if cell["source"].startswith("Derived") else f'{len(cell["sources"])} catalogs'
            # The size's own note (some makers build the 3/4" LR elbow shorter) applies to long-radius values.
            ref = (f' · <a class="note-ref" href="#note-{esc(slug)}">see note</a>'
                   if nps in row_notes and column != "sr90" else "")
            cells.append(f'<td><span class="in">{esc(inches)}</span><span class="mm">{esc(millimeters)}</span>'
                         f'<span class="prov">{esc(note)}{ref}</span></td>')
        use = (f'<a href="/pipe-offset-calculator/?nps={esc(nps)}">Offset</a>'
               f'<a href="/rolling-offset-calculator/?nps={esc(nps)}">Rolling</a>') if nps in calc_sizes else ""
        inline = f'<span class="use-inline">{use}</span>' if use else ""
        rows.append(f'<tr id="nps-{esc(nps)}"><th scope="row"><span class="nps">{esc(nps)}"</span>'
                    f'<span class="dn">DN {size["dn"]}</span>{inline}</th>{"".join(cells)}<td class="use">{use}</td></tr>')
    description = ("Butt-weld elbow takeout chart: center to end of ASME B16.9 long-radius 90° and 45° and short-radius "
                   "90° elbows, 1/2\" to 48\", in inches and millimeters, each value from at least two catalogs.")
    six = next(s for s in data["sizes"] if s["nps"] == "6")
    thirty = six["lr90"]["value"] * math.tan(math.radians(15))
    main = f"""<div class="wrap page-head">
  <h1>Butt-weld elbow takeout chart</h1>
  <p class="lede">Center to end, the takeout, of ASME B16.9 butt-weld elbows from 1/2" to 48", in inches and millimeters. Each value agrees in at least two catalogs, and the line under it says how many.</p>
</div>
<div class="wrap chart-layout">
  <figure class="elbow-figure">{ELBOW_FIGURE}
    <figcaption>Center to end: from the weld face of one end to where the two centerlines cross. A for a 90°, B for a 45°.</figcaption>
  </figure>
  <div class="table-wrap chart-wrap" tabindex="0" role="region" aria-label="Elbow takeouts by pipe size">
  <table class="data chart">
    <caption>Center to end, inches (millimeters below)</caption>
    <thead><tr><th scope="col">Size</th><th scope="col">90° long radius <abbr title="center to end of a 90">A</abbr></th>
      <th scope="col">45° long radius <abbr title="center to end of a 45">B</abbr></th>
      <th scope="col">90° short radius <abbr title="center to end of a 90">A</abbr></th><th scope="col"><span class="visually-hidden">Calculators</span></th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
  </div>
</div>
<div class="wrap prose">
  <section aria-labelledby="odd">
    <h2 id="odd">Takeout of a 90 cut to another angle</h2>
    <p>Multiply the 90's center to end (A) by tan(θ/2). A 6" long-radius 90 cut to 30°: {six["lr90"]["value"]:g} × 0.2679 = {thirty:.3f}". A stock long-radius 45 is in the chart as B, so it isn't cut from a 90.</p>
    {multiplier_table()}
  </section>
  <section aria-labelledby="notes">
    <h2 id="notes">Notes</h2>
    <ul>
      <li>Long-radius 90s from 22" up without a catalog value are derived from the radius: A = 1.5 × NPS. They're marked derived.</li>
      <li>Short-radius 90s have A equal to the nominal size; there's no short-radius 45 in the catalogs.</li>
      <li>A short line means the catalogs don't list that size.</li>
      {"".join(f'<li id="note-{esc(nps.replace("/", "-"))}">{esc(text)}</li>' for nps, texts in row_notes.items() for text in texts)}
    </ul>
  </section>
  <section aria-labelledby="sources">
    <h2 id="sources">Sources</h2>
    {source_list(reference["sources"], elbow_source_ids(data))}
    <p class="disclaimer">{DISCLAIMER}</p>
  </section>
  <p class="related">Use these takeouts in the <a href="/pipe-offset-calculator/">pipe offset calculator</a> or the <a href="/rolling-offset-calculator/">rolling offset calculator</a>.</p>
</div>
<div class="wrap">{app_block("chart", f"The app carries this chart and eleven more (pipe, tees, reducers, caps, stub ends, socket-weld and threaded fittings, NPT, flanges with bolting), every value with its catalogs, offline. {PRICE} once, no subscription.")}</div>"""
    return {
        "path": "/elbow-takeout-chart/",
        "title": "Butt-weld elbow takeout chart, 1/2\" to 48\" | Spoolhand",
        "description": description, "main": main, "jsonld": [], "scripts": (),
    }


# ---------------------------------------------------------------- home

LAYOUT_TOOLS = ["Simple offset", "Fixed-dimension offset", "Rolling offset", "Parallel offsets", "Odd angle from a 90",
                "Back-to-back fittings", "Tee branch offset", "Miter elbow", "Fishmouth & saddle", "Lateral",
                "Dummy leg", "Flange 2-holing"]

MINI = {
    "offset": '<svg viewBox="0 0 120 64" aria-hidden="true"><path class="pipe" d="M6 52 H38 L82 12 H114"/><circle class="joint" cx="38" cy="52" r="4"/><circle class="joint" cx="82" cy="12" r="4"/></svg>',
    "rolling": '<svg viewBox="0 0 120 64" aria-hidden="true"><path class="dash" d="M30 54 H78 V24 L100 10"/><path class="pipe" d="M6 54 H30 L100 10 H114"/><circle class="joint" cx="30" cy="54" r="4"/><circle class="joint" cx="100" cy="10" r="4"/></svg>',
    "chart": '<svg viewBox="0 0 120 64" aria-hidden="true"><path class="pipe" d="M10 14 H40 A36 36 0 0 1 76 50 V60"/><path class="dash" d="M40 14 V50 H76"/></svg>',
}


def home_page(data: dict, reference: dict) -> dict:
    publishers = []
    for s in reference["sources"]:
        if s["publisher"] not in publishers:
            publishers.append(s["publisher"])
    tools = "".join(f"<li>{esc(t)}</li>" for t in LAYOUT_TOOLS)
    tool_rows = [
        ("offset", "/pipe-offset-calculator/", "Pipe offset calculator",
         "Travel, run and cut length for a simple or 45° offset, with the takeout from the elbow chart."),
        ("rolling", "/rolling-offset-calculator/", "Rolling offset calculator",
         "Set and roll plus an angle, run or travel: true offset, travel and cut."),
        ("chart", "/elbow-takeout-chart/", "Elbow takeout chart",
         "Center to end of long- and short-radius butt-weld elbows, 1/2\" to 48\", with their catalogs."),
    ]
    rows = "".join(
        f'<li><a class="tool-row" href="{href}">{MINI[key]}<span class="tool-text"><span class="tool-name">{esc(name)}</span>'
        f'<span class="tool-line">{esc(line)}</span></span><svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M7 4l6 6-6 6"/></svg></a></li>'
        for key, href, name, line in tool_rows
    )
    description = (f"Spoolhand is a pipefitter's calculator for iPhone and iPad: offsets, rolling offsets, takeouts, "
                   f"flange bolting and fitting tables, every reference dimension traced to its catalogs. Works offline. {PRICE} once.")
    main = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <h1>The pipefitter's calculator. <span class="nowrap">Pay once.</span></h1>
      <p class="lede">Cut lengths for offsets and rolling offsets, takeouts, flange bolting and fittings, on iPhone and iPad. Every reference dimension shows the catalogs it came from, and it all works with no signal.</p>
      {store_button("home", "store-large")}
      <p class="hero-try"><a href="/pipe-offset-calculator/">Try the offset calculator free</a></p>
    </div>
    <figure class="hero-shot">
      <img src="/static/img/app-offset.webp" width="360" height="622" fetchpriority="high"
        alt="Spoolhand on iPhone: a simple offset of 24 inches at 45 degrees on 6-inch long-radius 45s. The cut length, 26-3/16 inches, is in the yellow box; the takeout says ASME B16.9, 3 catalogs.">
    </figure>
  </div>
</section>
<section class="wrap band" aria-labelledby="free">
  <h2 id="free">Free on this site</h2>
  <p class="band-lede">The same math as the app, checked against the same test cases.</p>
  <ul class="tool-rows">{rows}</ul>
</section>
<section class="wrap band" aria-labelledby="inside">
  <h2 id="inside">In the app</h2>
  <div class="feature">
    <div class="feature-text">
      <h3>Jobs and cut sheets</h3>
      <p>Save calculations to a job, reopen and change them later, and share a PDF cut sheet with the drawing and every step, letter or A4.</p>
    </div>
    <img class="feature-shot" src="/static/img/cut-sheet.webp" width="1000" height="936" loading="lazy"
      alt="A Spoolhand cut sheet: a job with three calculations, the first drawn with its offset, angle and run, the cut length in yellow and the steps.">
  </div>
  <div class="feature feature-flip">
    <div class="feature-text">
      <h3>Reference tables, with their sources</h3>
      <p>Pipe dimensions and weights; butt-weld elbows, tees, reducing tees, reducers, caps and stub ends; forged socket-weld and threaded fittings; malleable-iron fittings; NPT threads; and flanges with their bolting and tightening order. Fractions or decimals, inches or millimeters.</p>
    </div>
    <img class="feature-shot phone" src="/static/img/app-flange.webp" width="360" height="463" loading="lazy"
      alt="Spoolhand's flange table: a 2-inch Class 300 weld neck flange with its dimensions and bolting, each group marked ASME B16.5 and its number of catalogs.">
  </div>
  <div class="feature-plain">
    <div>
      <h3>Layout tools</h3>
      <p>Each one starts from your pipe: size, schedule, fitting and gap. Every answer shows its steps and where its takeouts came from.</p>
      <ul class="tool-list">{tools}</ul>
    </div>
    <div>
      <h3>A trade calculator</h3>
      <p>Feet, inches and sixteenths with a paper tape, and any result from a layout tool sent straight to it.</p>
      <h3>Made for the job site</h3>
      <p>Keys at least 56 points for gloves, high contrast in the sun, light and dark, and nothing that needs a signal.</p>
    </div>
  </div>
</section>
<section class="wrap band" aria-labelledby="numbers">
  <h2 id="numbers">Where the numbers come from</h2>
  <div class="numbers">
    <p>Every reference dimension in the app agrees in at least two published manufacturer or distributor catalogs, and the app shows which ones. A value worked out from a formula says so and shows the formula.</p>
    <p>The math is checked against 2,051 cases worked out independently, and against the worked examples in a handheld pipe calculator's published guide. The calculators on this site run the same offset math and pass the 415 of those cases that cover them.</p>
    <p class="publishers"><span>Catalogs from</span> {esc(", ".join(publishers))}.</p>
    <p class="disclaimer">{DISCLAIMER}</p>
  </div>
</section>
<section class="wrap close" id="app" aria-labelledby="price">
  <h2 id="price">{PRICE}, once.</h2>
  <p>No subscription, no account, no ads. Buy it once and it's yours on your iPhone and iPad.</p>
  {store_button("home-close", "store-large")}
</section>"""
    app_ld = {
        "@context": "https://schema.org", "@type": "SoftwareApplication", "name": STORE_NAME, "url": SITE + "/",
        "description": description, "applicationCategory": "UtilitiesApplication", "operatingSystem": "iOS 18 or later",
        "image": SITE + "/static/img/icon-512.png", "publisher": PUBLISHER,
        "offers": {"@type": "Offer", "price": PRICE.lstrip("$"), "priceCurrency": "USD"},
    }
    return {
        "path": "/", "title": "Spoolhand: pipefitter's calculator for iPhone and iPad", "description": description,
        "main": main, "jsonld": [app_ld, {"@context": "https://schema.org", "@type": "WebSite", "name": "Spoolhand", "url": SITE + "/"}],
        "scripts": (),
    }


# ---------------------------------------------------------------- privacy, support, 404

def privacy_page() -> dict:
    main = f"""<div class="wrap prose page-head">
  <h1>Privacy</h1>
  <p class="lede">Spoolhand collects nothing about you. This page covers the app and this website. Updated 19 November 2026.</p>
  <h2>The app</h2>
  <p>No account, no analytics, no ads, no tracking. Your jobs and settings stay on your device and in your own device backups. A cut sheet or a report leaves the device only when you send it, through the share sheet or Mail, to whoever you choose.</p>
  <h2>Buying it</h2>
  <p>Apple handles the purchase. We don't receive your payment details.</p>
  <h2>Email</h2>
  <p>If you write to <a href="mailto:{EMAIL}">{EMAIL}</a>, we use your message and address only to answer you, and keep them in our mailbox while we help you. We don't add you to any list or share them.</p>
  <h2>This website</h2>
  <p>No cookies, no analytics, and no scripts or fonts from other sites. It's hosted on GitHub Pages; GitHub may log visitors' IP addresses for security, as its <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">privacy statement</a> explains.</p>
  <h2>Children</h2>
  <p>The app is rated 4+ and collects nothing from anyone.</p>
  <h2>Changes and contact</h2>
  <p>Changes go on this page with a new date. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>. Spoolhand is made by Interactive Media.</p>
</div>"""
    return {"path": "/privacy/", "title": "Privacy | Spoolhand",
            "description": "Spoolhand's privacy policy: the app collects no data, has no account, analytics or ads; this website sets no cookies.",
            "main": main, "jsonld": [], "scripts": ()}


def support_page() -> dict:
    main = f"""<div class="wrap prose page-head">
  <h1>Support</h1>
  <p class="lede">Write to <a href="mailto:{EMAIL}">{EMAIL}</a>. A person reads every message.</p>
  <h2>A number looks wrong</h2>
  <p>Use Report a wrong number in the app: it's in Settings, in a calculation's menu and on every table row, and it fills in the values and the data edition for you. Or email us the size, the value and the source you checked. We check it against the catalogs and fix confirmed errors in an update.</p>
  <h2>On another iPhone or iPad</h2>
  <p>Spoolhand is a one-time purchase. On another device signed in with the same Apple Account, find it in the App Store under your purchases and download it again at no charge.</p>
  <h2>Requirements</h2>
  <p>iPhone or iPad with iOS 18 or later. Everything works offline: the tables and the math are on the device.</p>
  <h2>Your jobs</h2>
  <p>Jobs are stored on the device and included in your device backups. To keep a copy elsewhere, share a job's cut sheet as a PDF.</p>
  <p class="disclaimer">{DISCLAIMER}</p>
</div>"""
    return {"path": "/support/", "title": "Support | Spoolhand",
            "description": f"Help with Spoolhand: report a wrong number, reinstall on another device, requirements. Email {EMAIL}.",
            "main": main, "jsonld": [], "scripts": ()}


def not_found_page() -> dict:
    main = """<div class="wrap prose page-head">
  <h1>That page isn't here</h1>
  <p class="lede">Try the <a href="/pipe-offset-calculator/">pipe offset calculator</a>, the <a href="/rolling-offset-calculator/">rolling offset calculator</a>, the <a href="/elbow-takeout-chart/">elbow takeout chart</a>, or <a href="/">the app</a>.</p>
</div>"""
    return {"path": "/404.html", "title": "Page not found | Spoolhand",
            "description": "This page doesn't exist on spoolhand.app. The pipe offset and rolling offset calculators and the elbow takeout chart are linked here.", "main": main, "jsonld": [], "scripts": ()}
