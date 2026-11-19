// The page's calculator runs: elbow choice, steps and messages (node --test tests/solve.test.mjs).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { elbowSizes, calculatorSizes, elbowAt } from '../static/js/fitting.js';
import { solve } from '../static/js/solve.js';

const reference = JSON.parse(fs.readFileSync(new URL('../data/reference-data.json', import.meta.url), 'utf8'));
const sizes = elbowSizes(reference);
const size = (nps) => sizes.find((s) => s.nps === nps);

test('elbow sizes carry the table values and the app\'s provenance labels', () => {
  assert.equal(sizes.length, 33);
  assert.deepEqual([size('6').lr90.value, size('6').lr45.value, size('6').sr90.value, size('6').od], [9, 3.75, 6, 6.625]);
  assert.equal(size('6').lr45.source, 'ASME B16.9 · 3 catalogs');
  assert.equal(size('22').lr90.source, 'Derived · A = 1.5 × NPS');
  assert.equal(size('6').dn, 150);
  assert.ok(calculatorSizes(sizes).every((s) => s.od !== null));
  assert.ok(!calculatorSizes(sizes).some((s) => s.nps === '22'));
});

test('a long-radius elbow at 45° is the stock 45; any other angle cuts a 90', () => {
  assert.deepEqual(elbowAt(size('6'), 'lr', 45), { takeout: 3.75, source: 'ASME B16.9 · 3 catalogs' });
  assert.deepEqual(elbowAt(size('6'), 'lr', 30), { radius: 9, od: 6.625, source: 'ASME B16.9 · 3 catalogs' });
  assert.equal(elbowAt(size('6'), 'sr', 45).radius, 6);            // no stock short-radius 45
  assert.match(elbowAt(size('1/2'), 'sr', 30).missing, /No 90° short-radius elbow for 1\/2"/);
});

const spec6 = { size: size('6'), elbow: 'lr', gap: 0.125 };

test('the default offset: 24" at 45° on 6" LR 45s with a 1/8" gap', () => {
  const run = solve('offset', { offset: 24, angle: 45, mode: 'angle' }, spec6);
  assert.equal(run.cut, '26-3/16"');
  assert.deepEqual(run.rows.map((r) => r.value), ['33-15/16"', '24"', '45.00°', '3-3/4"']);
  assert.deepEqual(run.steps.map((s) => s.text), [
    'Travel = 24 × 1.4142 = 33.941"',
    'Run = 24 × 1.0000 = 24"',
    'Takeout = 3.75" each',
    'Cut = 33.941 − 2 × 3.75 − 2 × 0.125 = 26.191" → 26-3/16"',
  ]);
  assert.deepEqual(run.marks, []);
});

test('a published example: 10" offset, 12" run, 6" LR cut from 90s, no gap', () => {
  const run = solve('offset', { offset: 10, run: 12, mode: 'run' }, { ...spec6, gap: 0 });
  assert.equal(run.cut, '9-1/8"');
  assert.deepEqual(run.marks.map((m) => m.value), ['3-15/16"', '6-1/4"', '8-9/16"']);
  assert.equal(run.rows.find((r) => r.label.startsWith('Takeout')).value, '3-1/4"');
  assert.equal(run.rows.find((r) => r.label === 'Angle').value, '39.81°');
});

test('a published rolling example: set 24, roll 13, run 32, 6" LR cut from 90s, 3/32" gap', () => {
  const run = solve('rolling', { set: 24, roll: 13, run: 32, mode: 'run' }, { ...spec6, gap: 0.09375 });
  assert.equal(run.cut, '35-1/4"');
  assert.equal(run.rows.find((r) => r.label === 'Travel').value, '42-1/16"');
  assert.equal(run.rows.find((r) => r.label === 'Angle').value, '40.46°');
});

test('metric shows millimeters in the result and the steps', () => {
  const run = solve('offset', { offset: 24, angle: 45, mode: 'angle' }, spec6, 'mm');
  assert.equal(run.cut, '665.3 mm');
  assert.equal(run.steps[0].text, 'Travel = 609.6 × 1.4142 = 862.1 mm');
});

test('refusals say what to fix', () => {
  assert.equal(solve('offset', { mode: 'angle', angle: 45 }, spec6).message, 'Enter the offset and the angle.');
  assert.equal(solve('offset', { mode: 'run', offset: 24 }, spec6).message, 'Enter the offset and the run.');
  assert.equal(solve('rolling', { mode: 'travel', set: 24, roll: 13 }, spec6).message, 'Enter the set, the roll and the travel.');
  assert.equal(solve('offset', { offset: 24, angle: 95, mode: 'angle' }, spec6).refused, 'invalid');
  assert.equal(solve('offset', { offset: 2, angle: 45, mode: 'angle' }, spec6).refused, 'tooShort');
  assert.equal(solve('rolling', { set: 24, roll: 13, travel: 20, mode: 'travel' }, spec6).message,
    'Check the numbers: the travel has to be longer than the true offset.');
  assert.match(solve('offset', { offset: 24, angle: 30, mode: 'angle' }, { ...spec6, size: size('1/2'), elbow: 'sr' }).message,
    /Enter the measured takeout/);
  assert.equal(solve('offset', { offset: 24, angle: 45, mode: 'angle' }, { ...spec6, elbow: 'custom' }).message,
    'Enter the takeout of one elbow.');
  assert.equal(solve('offset', { offset: 24, angle: 45, mode: 'angle' }, { ...spec6, gap: undefined }).refused, 'invalid');
});
