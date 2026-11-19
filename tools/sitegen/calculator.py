"""The calculator block of the offset pages, rendered with its default already solved.

The page script (static/js/page.js) takes over the same markup; without JavaScript the default
result, its drawing and its steps still read as a worked example.
"""

import json

from .layout import DISCLAIMER, esc

SIXTEENTHS = ["+ 16ths", "1/16", "1/8", "3/16", "1/4", "5/16", "3/8", "7/16",
              "1/2", "9/16", "5/8", "11/16", "3/4", "13/16", "7/8", "15/16"]

# Angle chips, as in the app: label parts (whole, numerator, denominator) and the value.
CHIPS = [(5, 5, 8, 5.625), (11, 1, 4, 11.25), (22, 1, 2, 22.5), (30, 0, 0, 30), (45, 0, 0, 45), (60, 0, 0, 60)]

MODES = {
    "offset": [("angle", "Angle"), ("run", "Run")],
    "rolling": [("angle", "Angle"), ("run", "Run"), ("travel", "Travel")],
}
FIELDS = {
    "offset": [("offset", "Offset")],
    "rolling": [("set", "Set"), ("roll", "Roll")],
}
KNOWN = {"angle": "Angle", "run": "Run", "travel": "Travel"}


def number_text(value: float) -> str:
    """A default value as typed: 24, 13, 45."""
    return f"{value:g}"


def length_field(kind: str, name: str, label: str, value: str = "", hidden: bool = False) -> str:
    field_id = f"{kind}-{name}"
    options = "".join(f'<option value="{i}">{esc(text)}</option>' for i, text in enumerate(SIXTEENTHS))
    return f"""<div class="field" data-field="{name}"{" hidden" if hidden else ""}>
  <label for="{field_id}">{esc(label)}</label>
  <span class="field-entry">
    <input id="{field_id}" name="{name}" type="text" inputmode="decimal" autocomplete="off" autocorrect="off"
      spellcheck="false" enterkeyhint="done" value="{esc(value)}" aria-describedby="{field_id}-note">
    <span class="unit" data-unit aria-hidden="true">"</span>
  </span>
  <select class="frac" name="{name}-frac" aria-label="{esc(label)}: add sixteenths">{options}</select>
  <p class="field-note" id="{field_id}-note" data-note></p>
</div>"""


def angle_field(kind: str, value: str, hidden: bool) -> str:
    field_id = f"{kind}-angle"
    chips = []
    for whole, top, bottom, degrees in CHIPS:
        label = f"{whole}<span class=\"frac-glyph\"><sup>{top}</sup>⁄<sub>{bottom}</sub></span>°" if top else f"{whole}°"
        pressed = "true" if f"{degrees:g}" == value else "false"
        spoken = f"{whole} and {top}/{bottom} degrees" if top else f"{whole} degrees"
        typed = f"{whole}-{top}/{bottom}" if top else f"{whole}"
        chips.append(f'<button type="button" class="chip" data-angle="{degrees:g}" data-text="{typed}" aria-pressed="{pressed}" '
                     f'aria-label="{spoken}">{label}</button>')
    return f"""<div class="field-group" data-field="angle"{" hidden" if hidden else ""}>
  <div class="field">
    <label for="{field_id}">Angle</label>
    <span class="field-entry">
      <input id="{field_id}" name="angle" type="text" inputmode="decimal" autocomplete="off" autocorrect="off"
        spellcheck="false" enterkeyhint="done" value="{esc(value)}" aria-describedby="{field_id}-note">
      <span class="unit" aria-hidden="true">°</span>
    </span>
    <p class="field-note" id="{field_id}-note" data-note></p>
  </div>
  <div class="chips" role="group" aria-label="Common fitting angles">{"".join(chips)}</div>
</div>"""


def segmented(name: str, options: list, checked: str, label: str, cls: str = "") -> str:
    items = "".join(
        f'<label><input type="radio" name="{name}" value="{value}"{" checked" if value == checked else ""}>'
        f'<span>{esc(text)}</span></label>'
        for value, text in options
    )
    return f'<fieldset class="segmented {cls}"><legend class="visually-hidden">{esc(label)}</legend>{items}</fieldset>'


def result_block(solved: dict) -> str:
    rows = "".join(
        f'<div class="row"><dt>{esc(r["label"])}</dt><dd>{esc(r["value"])}</dd>'
        + (f'<dd class="source">{esc(r["source"])}</dd>' if r.get("source") else "")
        + "</div>"
        for r in solved["rows"]
    )
    marks = "".join(f'<div class="row"><dt>{esc(m["label"])}</dt><dd>{esc(m["value"])}</dd></div>' for m in solved["marks"])
    steps = "".join(
        f'<li>{esc(s["text"])}' + (f'<span class="source">{esc(s["source"])}</span>' if s.get("source") else "") + "</li>"
        for s in solved["steps"]
    )
    return f"""<div class="result" data-result>
  <span class="result-label">Cut length</span>
  <output class="result-value" data-cut aria-live="polite">{esc(solved["cut"])}</output>
  <p class="result-message" data-message hidden></p>
</div>
<dl class="rows" data-rows>{rows}</dl>
<div class="marks" data-marks{"" if solved["marks"] else " hidden"}>
  <p class="marks-title">Mark the 90 before cutting it to the angle</p>
  <dl class="rows" data-mark-rows>{marks}</dl>
</div>
<details class="steps" open>
  <summary>Steps</summary>
  <ol data-steps>{steps}</ol>
</details>"""


def calculator(kind: str, default: dict, sizes: list, calculator_sizes: list) -> str:
    fields, spec = default["fields"], default["spec"]
    mode = fields["mode"]
    size_options = "".join(
        f'<option value="{esc(s["nps"])}"{" selected" if s["nps"] == spec["nps"] else ""}>'
        f'{esc(s["nps"])}" · DN {s["dn"]}</option>'
        for s in sizes if s["nps"] in calculator_sizes
    )
    inputs = "".join(length_field(kind, name, label, number_text(fields[name])) for name, label in FIELDS[kind])
    for known, label in KNOWN.items():
        if known not in dict(MODES[kind]):
            continue
        value = number_text(fields[known]) if known in fields else ""
        if known == "angle":
            inputs += angle_field(kind, value, hidden=mode != "angle")
        else:
            inputs += length_field(kind, known, label, value, hidden=mode != known)
    elbow_sizes = json.dumps([s for s in sizes if s["nps"] in calculator_sizes], separators=(",", ":"))
    return f"""<section class="calc" data-calc="{kind}" aria-label="Calculator">
<script type="application/json" data-sizes>{elbow_sizes}</script>
<form class="calc-form" novalidate autocomplete="off">
  <div class="calc-top">
    {segmented("mode", MODES[kind], mode, "What you know besides the " + ("offset" if kind == "offset" else "set and roll"), "modes")}
    {segmented("units", [("in", "in"), ("mm", "mm")], "in", "Units", "units")}
  </div>
  <details class="spec">
    <summary class="spec-bar"><span data-spec-label>{esc(spec["nps"])}" · BW LR · gap 1/8"</span>
      <svg class="chevron" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8l5 5 5-5"/></svg></summary>
    <div class="spec-panel">
      <div class="field">
        <label for="{kind}-nps">Pipe size</label>
        <select id="{kind}-nps" name="nps" class="field-select">{size_options}</select>
        <svg class="chevron" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8l5 5 5-5"/></svg>
      </div>
      {segmented("elbow", [("lr", "Long radius"), ("sr", "Short radius"), ("custom", "My takeout")], spec["elbow"], "Elbows", "elbows")}
      {length_field(kind, "takeout", "Takeout, each", "", hidden=True)}
      {length_field(kind, "gap", "Weld gap", "1/8")}
      <p class="spec-note">Butt-weld elbows from the chart: a long-radius 45 at 45°, otherwise a 90 cut to the angle. For socket-weld, threaded or a fitting you measured, choose My takeout.</p>
    </div>
  </details>
  {inputs}
</form>
<div class="calc-out">
  <figure class="diagram" data-diagram>{default["drawing"]}</figure>
  {result_block(default)}
  <noscript><p class="noscript">This calculator needs JavaScript. The numbers above are a worked example with the defaults.</p></noscript>
  <p class="disclaimer">{DISCLAIMER}</p>
</div>
</section>"""
