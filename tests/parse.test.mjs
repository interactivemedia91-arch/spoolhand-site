// What a fitter types into a length or angle field (node --test tests/parse.test.mjs).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseLength, parseAngle } from '../static/js/parse.js';

test('inches: decimals, fractions and mixed numbers, as written on a tape', () => {
  assert.equal(parseLength('24'), 24);
  assert.equal(parseLength('24.5'), 24.5);
  assert.equal(parseLength('.5'), 0.5);
  assert.equal(parseLength('3/8'), 0.375);
  assert.equal(parseLength('24-3/8'), 24.375);
  assert.equal(parseLength('24 3/8'), 24.375);
  assert.equal(parseLength(' 24 - 3/8 " '), 24.375);
  assert.equal(parseLength('24"'), 24);
});

test("feet and inches: 2' 3-3/8\" and its spellings", () => {
  assert.equal(parseLength("2'"), 24);
  assert.equal(parseLength("2' 3"), 27);
  assert.equal(parseLength("2'3-3/8\""), 27.375);
  assert.equal(parseLength("2' 3 3/8"), 27.375);
  assert.equal(parseLength("2'-3 3/8"), 27.375);
  assert.equal(parseLength('2′ 3″'), 27);
});

test('millimeters: a number, with or without "mm"', () => {
  assert.ok(Math.abs(parseLength('609.6', 'mm') - 24) < 1e-12);
  assert.ok(Math.abs(parseLength('609.6 mm', 'mm') - 24) < 1e-12);
  assert.ok(Number.isNaN(parseLength('24-3/8', 'mm')));
});

test('blank is missing, nonsense is invalid', () => {
  assert.equal(parseLength(''), undefined);
  assert.equal(parseLength('   '), undefined);
  for (const text of ['abc', '3/0', '24-9/8', '1e3', '0x10', '24..5', "2' 3' 4", '-4', '24 3', '/8']) {
    assert.ok(Number.isNaN(parseLength(text)), text);
  }
});

test('angles: decimals, fractions and the degree sign', () => {
  assert.equal(parseAngle('45'), 45);
  assert.equal(parseAngle('22-1/2'), 22.5);
  assert.equal(parseAngle('11 1/4°'), 11.25);
  assert.equal(parseAngle('5-5/8'), 5.625);
  assert.equal(parseAngle('30.65°'), 30.65);
  assert.equal(parseAngle(''), undefined);
  assert.ok(Number.isNaN(parseAngle("2' 3")));
});
