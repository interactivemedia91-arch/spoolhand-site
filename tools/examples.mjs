// Prints, as JSON, what the build needs from the calculators: the elbow sizes, the calculators'
// defaults (shown before any JavaScript runs) and the worked examples, all solved by the same
// modules the page uses. Usage: node tools/examples.mjs data/reference-data.json
import fs from 'node:fs';
import { elbowSizes, calculatorSizes } from '../static/js/fitting.js';
import { solve, showLength } from '../static/js/solve.js';
import { drawing } from '../static/js/diagram.js';
import { formatInches, formatMillimeters } from '../static/js/fit.js';

const reference = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const sizes = elbowSizes(reference);
const size = (nps) => sizes.find((s) => s.nps === nps);
const mm = (value) => value / 25.4;

function run(kind, fields, spec, units = 'in') {
  const solved = solve(kind, fields, { ...spec, size: size(spec.nps) }, units);
  if (solved.refused) throw new Error(`${kind} example refused: ${solved.message}`);
  const { values, ...shown } = solved;
  return { fields, spec, units, ...shown, drawing: drawing(kind, values, units, showLength) };
}

const lr6 = { nps: '6', elbow: 'lr', gap: 0.125 };

console.log(JSON.stringify({
  sizes,
  calculatorSizes: calculatorSizes(sizes).map((s) => s.nps),
  chart: Object.fromEntries(sizes.map((s) => [s.nps, Object.fromEntries(['lr90', 'lr45', 'sr90']
    .filter((column) => s[column])
    .map((column) => [column, [formatInches(s[column].value), formatMillimeters(s[column].value)]]))])),
  offset: {
    default: run('offset', { mode: 'angle', offset: 24, angle: 45 }, lr6),
    examples: [
      run('offset', { mode: 'run', offset: 10, run: 12 }, { ...lr6, gap: 0 }),
      run('offset', { mode: 'angle', offset: mm(600), angle: 45 }, { ...lr6, gap: mm(3) }, 'mm'),
    ],
  },
  rolling: {
    default: run('rolling', { mode: 'angle', set: 24, roll: 13, angle: 45 }, lr6),
    examples: [
      run('rolling', { mode: 'run', set: 24, roll: 13, run: 32 }, { ...lr6, gap: 0.09375 }),
      run('rolling', { mode: 'angle', set: mm(600), roll: mm(300), angle: 45 }, { ...lr6, gap: mm(3) }, 'mm'),
    ],
  },
}));
