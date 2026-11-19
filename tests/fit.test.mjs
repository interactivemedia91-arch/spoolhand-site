// The site's calculators against the app's golden vectors (node --test tests/fit.test.mjs).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { simpleOffset, rollingOffset, formatInches, formatMillimeters, formatAngle } from '../static/js/fit.js';

const load = (name) => JSON.parse(fs.readFileSync(new URL(`../data/golden/${name}`, import.meta.url), 'utf8'));

for (const [file, solve] of [['offset.json', simpleOffset], ['rolling-offset.json', rollingOffset]]) {
  test(`${file}: every differential case, within the file's tolerance`, () => {
    const { cases, tolerance } = load(file);
    assert.ok(cases.length > 200);
    for (const c of cases) {
      const result = solve(c.inputs);
      const where = JSON.stringify(c.inputs);
      if (c.refused) {
        assert.equal(result.refused, c.refused, where);
        continue;
      }
      assert.equal(result.refused, undefined, `${where} refused ${result.refused}`);
      for (const [key, expected] of Object.entries(c.outputs)) {
        const limit = key.toLowerCase().endsWith('angle') ? tolerance.angle : tolerance.length;
        assert.ok(Math.abs(result[key] - expected) <= limit, `${where} ${key}: ${result[key]} vs ${expected}`);
      }
    }
  });
}

test('published worked examples print the same strings', () => {
  const solvers = { offset: simpleOffset, 'rolling-offset': rollingOffset };
  const examples = load('fit.json').filter((example) => example.calculator in solvers);
  assert.equal(examples.length, 10);
  for (const example of examples) {
    const result = solvers[example.calculator](example.inputs);
    for (const [key, expected] of Object.entries(example.expected)) {
      const printed = key === 'angle' ? formatAngle(result[key]) : formatInches(result[key], example.resolution ?? 16);
      assert.equal(printed, expected, `${example.name}: ${key}`);
    }
  }
});

test('fractions round like the app: nearest 1/16, ties away from zero', () => {
  assert.equal(formatInches(26.1912), '26-3/16"');
  assert.equal(formatInches(0.03), '0"');
  assert.equal(formatInches(-0.125), '-1/8"');
  assert.equal(formatInches(0.0625), '1/16"');
  assert.equal(formatInches(24), '24"');
  assert.equal(formatInches(1.03125), '1-1/16"');            // a tie at 1/16 goes away from zero
  assert.equal(formatInches(-1.03125), '-1-1/16"');          // and so does a negative one
  assert.equal(formatInches(4.015625, 32), '4-1/32"');        // a tie at 1/32
  assert.equal(formatInches(0.96875), '1"');                  // 15.5/16 carries into the inch
  assert.equal(formatInches(-0.03), '0"');                    // no negative zero
});

test('a value that is not a length never prints as one', () => {
  assert.equal(formatInches(Number.NaN), '—');
  assert.equal(formatInches(Number.POSITIVE_INFINITY), '—');
  assert.equal(formatMillimeters(Number.NaN), '—');
});

test('millimeters and angles', () => {
  assert.equal(formatMillimeters(26.2052), '665.6 mm');
  assert.equal(formatMillimeters(1000 / 25.4), '1000 mm');
  assert.equal(formatAngle(30.6526), '30.65°');
  assert.equal(formatAngle(45), '45.00°');
});

test('refusals name what to fix', () => {
  assert.equal(simpleOffset({ offset: 24, takeout: 3.75 }).refused, 'invalid');           // neither angle nor run
  assert.equal(simpleOffset({ offset: 1, angle: 45, takeout: 3.75, gap: 0.125 }).refused, 'tooShort');
  assert.equal(rollingOffset({ set: 24, takeout: 1 }).refused, 'missing');
});

test('a blank field is missing, not zero', () => {
  assert.equal(simpleOffset({ offset: 24, angle: 45, takeout: ' ' }).refused, 'missing');
  assert.equal(simpleOffset({ offset: '  ', angle: 45, takeout: 3.75 }).refused, 'missing');
  assert.equal(rollingOffset({ set: 24, roll: 10, angle: 45, takeout: '\t' }).refused, 'missing');
  assert.equal(simpleOffset({ offset: ' 24 ', angle: 45, takeout: 3.75 }).refused, undefined);
});

test('results that are not finite are refused', () => {
  assert.equal(simpleOffset({ offset: 1e308, angle: 1, takeout: 0 }).refused, 'invalid');
  assert.equal(simpleOffset({ offset: 24, angle: 45, takeout: 0, engagement: 1e308 }).refused, 'invalid');
});
