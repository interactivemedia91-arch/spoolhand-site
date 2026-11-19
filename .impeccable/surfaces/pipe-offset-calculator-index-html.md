---
version: 1
slug: "pipe-offset-calculator-index-html"
primary_target: "pipe-offset-calculator/index.html"
related_targets: ["index.html","rolling-offset-calculator/index.html","elbow-takeout-chart/index.html"]
---

# Spoolhand site: calculators, chart and home

Scope: the whole static site. Calculator pages (`/pipe-offset-calculator/`, `/rolling-offset-calculator/`) and the chart (`/elbow-takeout-chart/`) are Operate; the home page is Persuade; privacy and support are Read.

Audience and job: a fitter on a phone, often gloved, finds a calculator through search, types an offset and pipe size, reads the cut length, checks the steps and the sources, and learns the app does this offline with saved jobs and PDF cut sheets for $19.99 once.

Constraints: no analytics, cookies or third-party hosts; fonts served from the site; the explanation readable without JavaScript; the result visible without scrolling on a 390 × 844 phone once inputs are in.

Memorable moment: the yellow cut-length box changing as you type, over an ink diagram that redraws with its dimensions.

Unresolved: the App Store URL (button reads "Coming soon" until release).

## Direction contract

THESIS: the site is a page of the app's pocket handbook, not a software landing page. The calculator is the first thing on its page and the answer is the loudest thing on screen; it refuses the hero-with-phone-mockup-and-three-feature-cards arrangement.

OWN-WORLD: Blue Book. Warm paper ground, ink text, white cards with 12 px corners and a tan outline, a sunken tan panel for steps, safety yellow only on the pipe-spec bar and the result, olive provenance lines ("ASME B16.9 · 3 catalogs"), condensed tabular numerals, ink line diagrams with dashed dimension lines.

STORY: the visitor gets a correct number, sees how it was worked and where the takeout came from, believes it, then sees what the app adds and the price.

FIRST VIEWPORT: calculator pages on a phone: a one-line H1, the yellow spec bar (size · elbow · gap), the angle/run switch, offset and angle fields with angle chips, then the yellow Cut length box with the default 24" offset at 45° on 6" LR already solved (26-3/16"). Desktop: inputs left, diagram and result right. Home: wordmark, an H1 that names the job and the price model, the App Store button, and the real app screen at work beside it.

FORM: seed: none (pinned): "the visual world is Blue Book, carried over from `design/design-system.md`"; "the home page is Persuade mode; the calculator pages are Operate mode"; page order fixed in plan Task 3 Step 5 (H1, one sentence, calculator and result, diagram, worked example, formulas, FAQ, sources, then the app). Signature interaction: live solve with the diagram relabeling.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
