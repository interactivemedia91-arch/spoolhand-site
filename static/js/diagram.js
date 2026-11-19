// The calculators' line drawings, as SVG strings: ink pipe, dots at the fittings, dashed dimension
// lines with their values. Shared by the page script and the build (the no-JavaScript drawing).

const esc = (text) => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

function text(x, y, label, anchor = 'middle', cls = 'dim') {
  return `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" text-anchor="${anchor}" class="${cls}">${esc(label)}</text>`;
}

const line = (x1, y1, x2, y2, cls = 'pipe') =>
  `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" class="${cls}"/>`;
const dot = (x, y) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="5" class="joint"/>`;

/**
 * A simple offset drawn at its angle (kept between 20° and 70° so it stays legible).
 * `labels`: `{ travel, offset, run, angle }`, strings already formatted.
 */
export function offsetDiagram(angle, labels) {
  const theta = (Math.min(70, Math.max(20, Number.isFinite(angle) ? angle : 45)) * Math.PI) / 180;
  const height = 120;
  const run = Math.min(230, height / Math.tan(theta));
  const ax = (420 - run) / 2 - 10, ay = 176, bx = ax + run, by = ay - height;
  return `<svg viewBox="0 0 420 236" role="img" aria-label="Simple offset: travel ${esc(labels.travel)}, offset ${esc(labels.offset)}, run ${esc(labels.run)}, angle ${esc(labels.angle)}">
${line(24, ay, ax, ay)}${line(ax, ay, bx, by)}${line(bx, by, 396, by)}
${line(bx, by + 10, bx, ay, 'dash')}${line(ax, ay + 18, bx, ay + 18, 'dash')}
${dot(ax, ay)}${dot(bx, by)}
${text((ax + bx) / 2 - 14, (ay + by) / 2 - 8, labels.travel, 'end')}
${text(bx + 10, (ay + by) / 2 + 6, `Offset ${labels.offset}`, 'start')}
${text((ax + bx) / 2, ay + 40, `Run ${labels.run}`)}
${text(ax + 34, ay - 12, labels.angle, 'start')}
</svg>`;
}

/**
 * A rolling offset in isometric: the run along the line, the set up, the roll back, the travel
 * across the box, and the true offset as a faint diagonal. `labels`: `{ travel, set, roll, run }`.
 */
export function rollingDiagram(labels) {
  const sx = 70, sy = 186;                    // start of the travel
  const run = 170, set = 104, rollX = 74, rollY = 42;
  const r1x = sx + run, r1y = sy;               // end of the run
  const r2x = r1x, r2y = sy - set;              // up the set
  const ex = r2x + rollX, ey = r2y - rollY;     // back the roll: the end of the travel
  return `<svg viewBox="0 0 420 236" role="img" aria-label="Rolling offset: set ${esc(labels.set)}, roll ${esc(labels.roll)}, run ${esc(labels.run)}, travel ${esc(labels.travel)}">
${line(r1x, r1y, r2x, r2y, 'dash')}${line(r2x, r2y, ex, ey, 'dash')}${line(sx, sy, r1x, r1y, 'dash')}${line(r1x, r1y, ex, ey, 'dash faint')}
${line(16, sy, sx, sy)}${line(sx, sy, ex, ey)}${line(ex, ey, 404, ey)}
${dot(sx, sy)}${dot(ex, ey)}
${text((sx + ex) / 2 - 10, (sy + ey) / 2 - 10, labels.travel, 'end')}
${text((sx + r1x) / 2, sy + 26, `Run ${labels.run}`)}
${text(r1x - 8, (r1y + r2y) / 2 + 26, `Set ${labels.set}`, 'end')}
${text((r2x + ex) / 2 + 12, (r2y + ey) / 2 + 18, `Roll ${labels.roll}`, 'start')}
</svg>`;
}

/** The drawing for a solved run (`values` from `solve`), or a blank one when `values` is missing. */
export function drawing(kind, values, units, show) {
  const L = (inches) => (values ? show(inches, units) : '—');
  if (kind === 'rolling') {
    return rollingDiagram({
      travel: L(values?.travel), set: L(values?.set), roll: L(values?.roll), run: L(values?.run), trueOffset: L(values?.trueOffset),
    });
  }
  const angle = values?.angle ?? 45;
  return offsetDiagram(angle, {
    travel: L(values?.travel),
    offset: L(values ? values.travel * Math.sin((angle * Math.PI) / 180) : 0),
    run: L(values?.run),
    angle: values ? `${angle.toFixed(2)}°` : '—',
  });
}
