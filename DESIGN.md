---
name: Spoolhand
description: The pipefitter's pocket handbook on the web. Warm paper, ink, and one safety-yellow answer.
colors:
  paper: "#F4F1E8"
  surface: "#FFFFFF"
  sunken: "#EAE5D7"
  ink: "#16181B"
  ink-2: "#5F5E57"
  border: "#CFC8B6"
  accent: "#F2C230"
  on-accent: "#16181B"
  source: "#6B580F"
  error: "#B3261E"
  segment-on: "#FFFFFF"
  paper-dark: "#1C1D1F"
  surface-dark: "#26282B"
  sunken-dark: "#2F3135"
  ink-dark: "#F1EEE6"
  ink-2-dark: "#A3A097"
  border-dark: "#3A3C40"
  source-dark: "#D4B44A"
  error-dark: "#FF6B5E"
  segment-on-dark: "#3A3C40"
typography:
  display:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "clamp(2.75rem, 5.2vw + 1rem, 5rem)"
    fontWeight: 700
    lineHeight: 0.96
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.01em"
  title:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 650
    lineHeight: 1.3
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 600
    lineHeight: 1.25
  numeral-result:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "3.5rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontFeature: "tnum"
  numeral-field:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 700
    lineHeight: 1.1
    fontFeature: "tnum"
  numeral-row:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.15
    fontFeature: "tnum"
rounded:
  focus: "4px"
  inner: "10px"
  card: "12px"
  segment-track: "14px"
  block: "16px"
  phone-shot: "26px"
spacing:
  gutter: "20px"
  stack: "10px"
  group: "16px"
  column-gap: "32px"
  band: "80px"
  container: "1160px"
components:
  spec-bar:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.numeral-row}"
    rounded: "{rounded.card}"
    padding: "0 16px"
    height: "56px"
  result:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.numeral-result}"
    rounded: "{rounded.card}"
    padding: "14px 18px 18px"
  result-refused:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
  field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.numeral-field}"
    rounded: "{rounded.card}"
    padding: "4px 8px 4px 16px"
    height: "64px"
  chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    height: "56px"
  chip-selected:
    backgroundColor: "{colors.sunken}"
    textColor: "{colors.ink}"
  segmented-track:
    backgroundColor: "{colors.sunken}"
    rounded: "{rounded.segment-track}"
    padding: "4px"
  segment-selected:
    backgroundColor: "{colors.segment-on}"
    textColor: "{colors.ink}"
    rounded: "{rounded.inner}"
    height: "48px"
  store-button:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.card}"
    padding: "10px 20px"
    height: "56px"
  store-soon:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "10px 20px"
    height: "56px"
  rows:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "0 16px"
  steps-panel:
    backgroundColor: "{colors.sunken}"
    rounded: "{rounded.card}"
    padding: "4px 16px 6px"
  tool-row:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    padding: "14px 18px"
    height: "92px"
  tool-row-hover:
    backgroundColor: "{colors.sunken}"
---

# Design System: Spoolhand

## Overview

**Creative North Star: "The Pocket Handbook"**

Every page is a page of the app's pocket handbook, not a software landing page. The system is the app's Blue Book world carried onto the web: warm paper ground, ink text, white cards with a tan outline, a sunken tan panel for worked steps, olive provenance lines under every reference value, and ink line diagrams with dashed dimension lines. On calculator pages the answer is the loudest thing on screen, and it is the only other place the safety yellow appears besides the pipe-spec bar.

Density is set by gloved thumbs on a phone outdoors: targets are 56px where they are tapped mid-task, 44px minimum everywhere else, numerals are big, condensed and tabular so fractions to 1/16" line up. The home page persuades (Persuade mode); calculator pages operate (Operate mode). Both share one token set; neither borrows the hero-with-phone-mockup-and-three-feature-cards template.

**Key Characteristics:**
- Warm paper, ink, and one safety yellow reserved for the spec bar and the result.
- Condensed tabular numerals for every number; system-ui for prose.
- 12px corners on every card-like container; tan hairlines instead of shadows.
- Provenance is visual: olive source lines sit under the values they justify.
- Ink line diagrams that relabel live as inputs change.
- Light, dark, and high-contrast are first-class, driven by the same custom properties.

## Colors

A warm, paper-and-ink neutral system with exactly one saturated accent.

### Primary
- **Safety Yellow** (accent): the pipe-spec bar and the result box, nothing else. Text on it is always ink (on-accent). It does not change in dark mode; yellow on charcoal still reads as the answer.

### Neutral
- **Handbook Paper** (paper): page ground; also the text color on the ink App Store button.
- **Card White** (surface): fields, chips, result rows, diagrams, tables, the tool list, the app block.
- **Sunken Tan** (sunken): worked-steps panel, spec panel, segmented-control track, selected chip fill, hover fill for nav and tool rows, targeted chart row.
- **Ink** (ink): body text, line work in diagrams, focus rings, the live App Store button, selected-chip outline.
- **Pencil Grey** (ink-2): field labels, secondary lines, captions, table headers, dashed dimension lines.
- **Tan Hairline** (border): card outlines, row dividers, link underlines at rest, the "Coming soon" outline.
- **Olive Provenance** (source): source lines ("ASME B16.9 · 3 catalogs") under reference values and chart cells.
- **Signal Red** (error): invalid field outline and its note. Never decorative.
- **Selected Segment** (segment-on): the raised segment in a segmented control (white in light, border-grey in dark), lifted with the lift shadow.

Dark mode swaps the neutrals to the `-dark` tokens (charcoal paper, graphite surface); accent and on-accent are unchanged. High contrast (`prefers-contrast: more`) collapses ink-2, source and border to ink in each scheme.

### Named Rules
**The Two Yellows Rule.** Safety yellow appears in exactly two places per calculator page: the pipe-spec bar and the result. Selection highlight (::selection) is the only other use. A third yellow surface means the answer is no longer the loudest thing.

**The Provenance Color Rule.** Olive is reserved for where a value came from. It never colors a heading, a link, or a decoration.

## Typography

**Display / Numeral Font:** Barlow Semi Condensed 500/600/700, self-hosted woff2 under OFL (with system-ui fallback)
**Body Font:** system-ui stack (-apple-system, Segoe UI, Roboto, Helvetica Neue)

**Character:** A condensed, workmanlike numeral face for headings and every number, beside the reader's own system face for prose. Barlow stands in for the app's SF Pro condensed numerals, which cannot be self-hosted.

### Hierarchy
- **Display** (700, clamp 2.75rem to 5rem, 0.96): home hero H1 only, max 12ch.
- **Headline** (700, 2.25rem mobile / 2.875rem at 900px+, 1.05): page H1; H2 at 1.875rem / 2.125rem. Closing H2 on home scales to 4rem.
- **Title** (650, 1.1875rem, 1.3): H3, steps summary, result label (1.125rem).
- **Body** (400, 1.0625rem, 1.55): prose, max 62ch for ledes, 760px prose column.
- **Label** (600, 0.9375rem): table headers, captions, disclaimers, source lines (400).
- **Numerals**: result value 3.5rem / 4.25rem at 900px+; field values 1.875rem; spec bar 1.375rem; result rows 1.5rem; chips 1.375rem; table cells 1.125rem. All tabular.

### Named Rules
**The Every-Number-Is-Barlow Rule.** Any measurement, fraction, size or angle is set in the numeral face with tabular figures, including inline numbers in prose (`.num`, `.formula`). Prose words stay in system-ui.

**The Stacked Fraction Rule.** Angle chips set fractions as superscript/subscript glyph pairs at 0.62em, never as slashed text that wraps.

## Layout

A single 1160px container with 20px gutters (respecting safe-area insets). Vertical stacking uses a 10px gap inside calculator columns, 16px between calculator groups, and 64–88px between page bands.

Calculator pages: one column on phones in the fixed order H1, one sentence, spec bar, mode switch, fields, chips, result, rows, diagram, steps, disclaimer. At 900px+ the calculator splits 5fr inputs / 6fr output with a 32px gap, and the output column is sticky (top 20px) with the diagram moved above the result.

Takeout chart: single column; at 1000px+ a 320px sticky elbow figure beside the table. At ≤600px the chart drops its min-width, tightens cell padding to 9px 7px, shrinks the type ramp (headers 0.8125rem, inch values 1.1875rem, provenance 0.75rem), hides the "Use" column and shows one 44px inline link per size instead.

Home: hero is a 1.2fr / 0.8fr grid at 880px+ (copy left, real app screen right); tool links as one divided list (max 820px); feature rows alternate as two-column grids at 880px+; app block goes two-column at 760px+.

Header nav scrolls horizontally on ≤640px rather than wrapping or collapsing into a menu.

## Elevation & Depth

Flat and tonal. Depth comes from paper / white / sunken layering and tan hairlines. Shadows exist in exactly three roles.

### Shadow Vocabulary
- **Lift** (`0 1px 2px rgb(22 24 27 / 0.10), 0 2px 8px -2px rgb(22 24 27 / 0.10)`): the selected segment in a segmented control, only.
- **Device shot** (`0 28px 56px -28px rgb(22 24 27 / 0.45)`): real app screenshots and the cut-sheet image.
- **Focus / outline rings** (inset or spread, 1–2px ink, tan or error): field focus, invalid state, "Coming soon" outline, selected elbow segment, store hover ring.

### Named Rules
**The Paper-Not-Plastic Rule.** Cards sit flat on paper. A drop shadow on a card, chip or result is wrong; use a hairline or a tonal step instead.

## Shapes

One corner radius carries the system: 12px on every card-like container (fields, chips, spec bar, result, rows, diagrams, steps, tables, App Store button, tool list). Inner controls step down to 10px (segments, fraction picker, nav pills), the segmented track steps up to 14px, the app block to 16px, phone screenshots to 26–34px. Focus rings round to 4px. Line work is round-capped and round-joined at 4px stroke for pipe, 1.25–1.5px for dimension and center lines with dashes.

## Components

### Spec Bar (signature)
Safety-yellow 56px bar (12px corners) reading the pipe spec as a sentence ("6" · BW LR · gap 1/8"") in 1.375rem numerals with a chevron; opens a sunken panel of selects. The chevron rotates 180° in 200ms.

### Result (signature)
Safety-yellow box: label at 1.125rem 650, value at 3.5rem (4.25rem desktop) tabular. On every new answer the value plays the one authored motion, **settle**: from translateY(5px) and 0.35 opacity to rest in 220ms, `cubic-bezier(0.16, 1, 0.3, 1)`, removed entirely under reduced motion. When the inputs cannot produce a cut, the box turns refused: white with a tan inset hairline, value in pencil grey, with a message (max 44ch).

### Fields
White, 64px tall, 12px corners, tan hairline. Label left in pencil grey at 1.125rem; value right-aligned in 1.875rem numerals with its unit. Focus: border and 1px ring in ink. Invalid: red border and ring, note in red beneath. Fraction picker is a 44px paper-ground select with 10px corners.

### Chips
Six-across grid of 56px white chips (12px corners) for common angles. Pressed: sunken fill with a 2px ink border. Active press scales to 0.96 in 120ms.

### Segmented Controls
Sunken track (14px corners, 4px padding), 48px segments. Selected segment uses segment-on with the lift shadow (160ms ease-out). Elbow-type variant sits on paper with a tan inset outline; its selected segment is white with a 1.5px ink inset instead of a lift.

### Result Rows and Steps
Rows: a white list with 1px tan dividers, term left in pencil grey, value right in 1.5rem numerals, olive source line spanning beneath. Steps: a sunken disclosure (52px summary, CSS chevron) holding a tabular numbered list.

### App Store Button
Live: an ink button (paper text, 56px, 12px corners), "Get it on the App Store" in Barlow 1.25rem with a price sub-line; hover adds a paper-then-ink double ring. Not yet live: **Coming soon** is an outlined label (`<p>`, transparent, 1.5px tan inset), not a link and not a disabled-looking button. Large variant is 64px.

### Tool List
The home page's tools are one white list (12px corners, overflow clipped) divided by tan hairlines: 92px rows with an ink mini-diagram, tool name in 1.5rem Barlow, one pencil-grey line, and an arrow. Hover fills sunken.

### Navigation
Wordmark (icon + Barlow 1.5rem) left; text links as 44px pills (10px corners) that fill sunken on hover; current page is a 2px ink underline, not a fill.

### Data Tables
White, tabular, 1px tan row rules, right-aligned numerals in Barlow 1.125rem, first column sticky on the chart with a hairline edge; targeted row fills sunken.

## Do's and Don'ts

### Do:
- **Do** keep yellow to the spec bar and the result; everything else is paper, white, sunken and ink.
- **Do** set every number in Barlow Semi Condensed with tabular figures.
- **Do** put an olive source line under any reference value that came from a catalog.
- **Do** keep tap targets at 56px for in-task controls (spec bar, chips, store button) and never below 44px.
- **Do** present tool links as one divided white list.
- **Do** show "Coming soon" as an outlined label and the live App Store link as an ink button.
- **Do** disable the result settle and all transitions under `prefers-reduced-motion`.

### Don't:
- **Don't** use the hero-with-phone-mockup-and-three-feature-cards arrangement, or split tool links into three cards.
- **Don't** add a third yellow surface, a yellow button, or yellow on links.
- **Don't** put drop shadows on cards, chips, fields or the result; the lift shadow belongs to the selected segment only.
- **Don't** introduce another corner radius for containers; cards are 12px.
- **Don't** set fractions as slashed text in chips, or numbers in system-ui.
- **Don't** add authored motion beyond the result settle and the 120–220ms state transitions.
