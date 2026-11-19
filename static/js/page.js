// The calculator pages: reads the fields as they're typed, solves with the app's math, and redraws
// the result, the drawing and the steps. The markup and the default result come from the build.
import { parseLength, parseAngle } from './parse.js';
import { solve, showLength } from './solve.js';
import { formatInches } from './fit.js';
import { drawing } from './diagram.js';

const LENGTHS = ['offset', 'set', 'roll', 'run', 'travel', 'takeout', 'gap'];

for (const root of document.querySelectorAll('[data-calc]')) setUp(root);

function setUp(root) {
  const kind = root.dataset.calc;
  const sizes = JSON.parse(root.querySelector('[data-sizes]').textContent);
  const form = root.querySelector('form');
  const el = (selector) => root.querySelector(selector);
  const fieldOf = (name) => form.querySelector(`[data-field="${name}"]`);
  let units = 'in';
  let lastCut = el('[data-cut]').textContent;

  const wanted = new URLSearchParams(location.search).get('nps');
  if (wanted && sizes.some((s) => s.nps === wanted)) form.elements.nps.value = wanted;

  /** A field's value in inches (or degrees), undefined when blank, NaN when it isn't a number. */
  function read(name) {
    const input = form.elements[name];
    if (name === 'angle') return parseAngle(input.value);
    const typed = parseLength(input.value, units);
    const frac = form.elements[`${name}-frac`];
    const typedFraction = /['/]/.test(input.value);   // a fraction or feet typed in the field wins over the menu
    const sixteenths = frac && !typedFraction && units === 'in' ? Number(frac.value) : 0;
    if (!sixteenths) return typed;
    return (typed ?? 0) + sixteenths / 16;
  }

  /** The note under a field: what a fraction or feet entry reads as, or what's wrong with it. */
  function annotate(name, value) {
    const field = fieldOf(name)?.matches('.field') ? fieldOf(name) : fieldOf(name)?.querySelector('.field');
    if (!field) return;
    const input = form.elements[name];
    const frac = form.elements[`${name}-frac`];
    const typedFraction = /['/]/.test(input.value);
    if (frac) frac.disabled = typedFraction || units === 'mm';
    const note = field.querySelector('[data-note]');
    const invalid = Number.isNaN(value);
    field.classList.toggle('invalid', invalid);
    input.setAttribute('aria-invalid', String(invalid));
    if (invalid) {
      note.textContent = name === 'angle' ? 'Type an angle like 45 or 22-1/2.'
        : units === 'mm' ? 'Type millimeters, like 609.6.' : 'Type a length like 24-3/8 or 2\' 3-3/8.';
    } else if (name !== 'angle' && units === 'in' && typedFraction && value !== undefined
      && formatInches(value).replace(/"$/, '') !== input.value.trim().replace(/"$/, '')) {
      note.textContent = `Reads ${formatInches(value)}`;   // only when it differs from what's typed
    } else {
      note.textContent = '';
    }
  }

  function mode() {
    return form.elements.mode.value;
  }

  function showFields() {
    for (const known of ['angle', 'run', 'travel']) {
      const field = fieldOf(known);
      if (field) field.hidden = known !== mode();
    }
    fieldOf('takeout').hidden = form.elements.elbow.value !== 'custom';
  }

  function specLabel(spec) {
    const gap = spec.gap === undefined || Number.isNaN(spec.gap) ? '—' : showLength(spec.gap, units);
    if (spec.elbow === 'custom') {
      const takeout = spec.takeout === undefined || Number.isNaN(spec.takeout) ? '—' : showLength(spec.takeout, units);
      return `Takeout ${takeout} · gap ${gap}`;
    }
    const size = units === 'mm' ? `DN ${spec.size.dn}` : `${spec.size.nps}"`;
    return `${size} · BW ${spec.elbow === 'sr' ? 'SR' : 'LR'} · gap ${gap}`;
  }

  function update() {
    showFields();
    const names = kind === 'rolling' ? ['set', 'roll', mode()] : ['offset', mode()];
    const fields = { mode: mode() };
    for (const name of names) {
      fields[name] = read(name);
      annotate(name, fields[name]);
    }
    const spec = {
      size: sizes.find((s) => s.nps === form.elements.nps.value),
      elbow: form.elements.elbow.value,
      gap: read('gap'),
      takeout: form.elements.elbow.value === 'custom' ? read('takeout') : undefined,
    };
    annotate('gap', spec.gap);
    if (spec.elbow === 'custom') annotate('takeout', spec.takeout);
    el('[data-spec-label]').textContent = specLabel(spec);
    for (const chip of root.querySelectorAll('.chip')) {
      chip.setAttribute('aria-pressed', String(Number(chip.dataset.angle) === fields.angle));
    }

    const invalidField = names.some((name) => Number.isNaN(fields[name])) || Number.isNaN(spec.gap) || Number.isNaN(spec.takeout);
    const solved = invalidField
      ? { refused: 'invalid', message: 'Fix the field marked in red.' }
      : solve(kind, fields, { ...spec, gap: spec.gap }, units);
    render(solved);
  }

  function render(solved) {
    const result = el('[data-result]');
    const cut = el('[data-cut]');
    const message = el('[data-message]');
    result.classList.toggle('refused', Boolean(solved.refused));
    message.hidden = !solved.refused;
    message.textContent = solved.refused ? solved.message : '';
    const text = solved.refused ? '—' : solved.cut;
    if (text !== lastCut) {
      cut.textContent = text;
      cut.classList.remove('settle');
      void cut.offsetWidth;   // restart the settle animation on every new answer
      cut.classList.add('settle');
      lastCut = text;
    }
    el('[data-diagram]').innerHTML = drawing(kind, solved.refused ? null : solved.values, units, showLength);
    const rows = el('[data-rows]');
    rows.hidden = Boolean(solved.refused);
    rows.replaceChildren(...(solved.rows ?? []).map(row));
    el('[data-marks]').hidden = !solved.marks?.length;
    el('[data-mark-rows]').replaceChildren(...(solved.marks ?? []).map(row));
    el('[data-steps]').closest('details').hidden = Boolean(solved.refused);
    el('[data-steps]').replaceChildren(...(solved.steps ?? []).map((step) => {
      const item = document.createElement('li');
      item.textContent = step.text;
      if (step.source) item.append(span('source', step.source));
      return item;
    }));
  }

  /** Switching units converts what's typed: 1/8" becomes 3.2 mm, it never resets. */
  function switchUnits(next) {
    const values = Object.fromEntries(LENGTHS.filter((name) => form.elements[name]).map((name) => [name, read(name)]));
    units = next;
    for (const [name, value] of Object.entries(values)) {
      const input = form.elements[name];
      const frac = form.elements[`${name}-frac`];
      if (frac) frac.value = '0';
      if (value === undefined || Number.isNaN(value)) continue;
      input.value = units === 'mm'
        ? (value * 25.4).toFixed(1).replace(/\.0$/, '')
        : formatInches(value).replace(/"$/, '');
    }
    for (const unit of root.querySelectorAll('[data-unit]')) {
      unit.textContent = units === 'mm' ? 'mm' : '"';
      unit.classList.toggle('mm', units === 'mm');
    }
    for (const frac of root.querySelectorAll('.frac')) frac.hidden = units === 'mm';
    update();
  }

  form.addEventListener('input', (event) => {
    if (event.target.name === 'units') return;
    update();
  });
  form.addEventListener('change', (event) => {
    if (event.target.name === 'units') switchUnits(event.target.value);
    else update();
  });
  form.addEventListener('submit', (event) => event.preventDefault());
  root.querySelector('.chips')?.addEventListener('click', (event) => {
    const chip = event.target.closest('.chip');
    if (!chip) return;
    form.elements.angle.value = chip.dataset.text;
    update();
  });
  update();
}

function row(item) {
  const wrapper = document.createElement('div');
  wrapper.className = 'row';
  const term = document.createElement('dt');
  term.textContent = item.label;
  const value = document.createElement('dd');
  value.textContent = item.value;
  wrapper.append(term, value);
  if (item.source) wrapper.append(span('source', item.source, 'dd'));
  return wrapper;
}

function span(className, text, tag = 'span') {
  const node = document.createElement(tag);
  node.className = className;
  node.textContent = text;
  return node;
}
