// One calculator run as the page shows it: the cut length, the result rows, the elbow marks and the
// steps, in inches or millimeters. Shared by the page script and the build (which prints the worked
// examples and the no-JavaScript result with it), so both show the same numbers.
import { simpleOffset, rollingOffset, formatInches, formatMillimeters, formatAngle } from './fit.js';
import { elbowAt } from './fitting.js';

const toRadians = (degrees) => (degrees * Math.PI) / 180;

/** A length as the result shows it. */
export function showLength(inches, units) {
  return units === 'mm' ? formatMillimeters(inches) : formatInches(inches);
}

/** A length inside a step: decimal inches to 3 places, or millimeters to 1, trailing zeros trimmed. */
function stepNumber(inches, units) {
  const value = units === 'mm' ? inches * 25.4 : inches;
  const text = value.toFixed(units === 'mm' ? 1 : 3).replace(/\.?0+$/, '');
  return text === '-0' ? '0' : text;
}

function stepLength(inches, units) {
  return units === 'mm' ? `${stepNumber(inches, units)} mm` : `${stepNumber(inches, units)}"`;
}

const factor = (value) => value.toFixed(4);

const MESSAGES = {
  offset: {
    missing: (mode) => `Enter the offset and the ${mode}.`,
    invalid: () => 'Check the numbers: lengths above zero, and an angle between 0° and 90°.',
  },
  rolling: {
    missing: (mode) => `Enter the set, the roll and the ${mode}.`,
    invalid: (mode) => mode === 'travel'
      ? 'Check the numbers: the travel has to be longer than the true offset.'
      : 'Check the numbers: lengths above zero, and an angle between 0° and 90°.',
  },
  tooShort: 'No pipe left to cut: the two elbows and gaps take up the whole travel.',
};

/**
 * Solves a simple (`kind` "offset") or rolling ("rolling") offset.
 * `fields`: inches and degrees, `mode` "angle" | "run" | "travel" (the third known).
 * `spec`: `{ size, elbow: "lr" | "sr" | "custom", takeout?, gap }`, lengths in inches.
 * Returns `{ refused, message }` or `{ cut, rows, marks, steps }`, every string ready to show.
 */
export function solve(kind, fields, spec, units = 'in') {
  const solver = kind === 'rolling' ? rollingOffset : simpleOffset;
  const known = kind === 'rolling'
    ? { set: fields.set, roll: fields.roll, [fields.mode]: fields[fields.mode] }
    : { offset: fields.offset, [fields.mode]: fields[fields.mode] };
  const messages = MESSAGES[kind];
  if (Object.values(known).some((value) => value === undefined)) {
    return { refused: 'missing', message: messages.missing(fields.mode) };
  }

  const shape = solver({ ...known, takeout: 0 });
  if (shape.refused) {
    return { refused: shape.refused, message: messages[shape.refused === 'missing' ? 'missing' : 'invalid'](fields.mode) };
  }

  let elbow;
  if (spec.elbow === 'custom') {
    if (spec.takeout === undefined) return { refused: 'missing', message: 'Enter the takeout of one elbow.' };
    if (!(spec.takeout >= 0)) return { refused: 'invalid', message: 'The takeout has to be a length, zero or more.' };
    elbow = { takeout: spec.takeout, source: 'Measured' };
  } else {
    elbow = elbowAt(spec.size, spec.elbow, shape.angle);
    if (elbow.missing) return { refused: 'needsMeasured', message: elbow.missing };
  }
  if (spec.gap === undefined || !(spec.gap >= 0)) {
    return { refused: 'invalid', message: 'The gap has to be a length, zero or more.' };
  }

  const fitting = elbow.radius === undefined ? { takeout: elbow.takeout } : { radius: elbow.radius, od: elbow.od };
  const result = solver({ ...known, ...fitting, gap: spec.gap });
  if (result.refused) {
    return { refused: result.refused, message: result.refused === 'tooShort' ? MESSAGES.tooShort : messages.invalid(fields.mode) };
  }

  const L = (inches) => stepLength(inches, units);
  const N = (inches) => stepNumber(inches, units);
  const theta = toRadians(result.angle);
  const steps = [];
  const offset = kind === 'rolling' ? result.trueOffset : result.travel * Math.sin(theta);
  if (kind === 'rolling') {
    steps.push({ text: `True offset = √(${N(result.set)}² + ${N(result.roll)}²) = ${L(result.trueOffset)}` });
  }
  const name = kind === 'rolling' ? 'true offset' : 'offset';
  if (fields.mode === 'angle') {
    steps.push({ text: `Travel = ${N(offset)} × ${factor(1 / Math.sin(theta))} = ${L(result.travel)}` });
    steps.push({ text: `Run = ${N(offset)} × ${factor(1 / Math.tan(theta))} = ${L(result.run)}` });
  } else if (fields.mode === 'run') {
    steps.push({ text: `Travel = √(${N(offset)}² + ${N(result.run)}²) = ${L(result.travel)}` });
    steps.push({ text: `Angle = atan(${name} ÷ run) = atan(${N(offset)} ÷ ${N(result.run)}) = ${formatAngle(result.angle)}` });
  } else {
    steps.push({ text: `Run = √(${N(result.travel)}² − ${N(offset)}²) = ${L(result.run)}` });
    steps.push({ text: `Angle = atan(${name} ÷ run) = atan(${N(offset)} ÷ ${N(result.run)}) = ${formatAngle(result.angle)}` });
  }
  if (elbow.radius === undefined) {
    steps.push({ text: `Takeout = ${L(result.takeout)} each`, source: elbow.source });
  } else {
    steps.push({
      text: `Takeout = R × tan(θ/2) = ${N(elbow.radius)} × ${factor(Math.tan(theta / 2))} = ${L(result.takeout)} each`,
      source: `R: ${elbow.source}`,
    });
  }
  const gapTerm = spec.gap > 0 ? ` − 2 × ${N(spec.gap)}` : '';
  const rounded = units === 'mm' ? '' : ` → ${showLength(result.cut, units)}`;   // millimeters are already rounded
  steps.push({ text: `Cut = ${N(result.travel)} − 2 × ${N(result.takeout)}${gapTerm} = ${L(result.cut)}${rounded}` });

  const rows = [];
  if (kind === 'rolling') rows.push({ label: 'True offset', value: showLength(result.trueOffset, units) });
  rows.push({ label: 'Travel', value: showLength(result.travel, units) });
  rows.push({ label: 'Run', value: showLength(result.run, units) });
  rows.push({ label: 'Angle', value: formatAngle(result.angle) });
  rows.push({
    label: elbow.radius === undefined ? 'Takeout, each' : 'Takeout, each (90 cut to angle)',
    value: showLength(result.takeout, units),
    source: elbow.radius === undefined ? elbow.source : `R × tan(θ/2) · R: ${elbow.source}`,
  });

  const marks = result.inner === undefined ? [] : [
    { label: 'Inside', value: showLength(result.inner, units) },
    { label: 'Centerline', value: showLength(result.center, units) },
    { label: 'Outside', value: showLength(result.outer, units) },
  ];

  return { cut: showLength(result.cut, units), rows, marks, steps, angle: result.angle, values: result };
}
