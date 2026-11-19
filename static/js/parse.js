// What a fitter types into a field, as a number: inches for lengths, degrees for angles.
// Blank is undefined (missing); anything that isn't a length or an angle is NaN (invalid).

const DECIMAL = /^(?:\d+(?:\.\d+)?|\.\d+)$/;
const FRACTION = /^(\d+)\/(\d+)$/;
const MIXED = /^(\d+)\s*(?:-\s*|\s)(\d+)\/(\d+)$/;

/** `24`, `24.5`, `3/8`, `24-3/8` or `24 3/8`, in the field's unit; NaN for anything else. */
function plainNumber(text) {
  if (DECIMAL.test(text)) return Number(text);
  let match = text.match(FRACTION);
  if (match) return Number(match[2]) === 0 ? Number.NaN : Number(match[1]) / Number(match[2]);
  match = text.match(MIXED);
  if (match) {
    const [whole, top, bottom] = match.slice(1).map(Number);
    return bottom > 0 && top < bottom ? whole + top / bottom : Number.NaN;
  }
  return Number.NaN;
}

function normalized(text) {
  return String(text ?? '').trim().replace(/[′’‘]/g, "'").replace(/[″”“]/g, '"');
}

/** A length in inches from `24-3/8`, `2' 3-3/8"` or, in millimeters, `609.6`. */
export function parseLength(text, units = 'in') {
  let value = normalized(text);
  if (value === '') return undefined;
  if (units === 'mm') {
    value = value.replace(/\s*mm$/i, '');
    return DECIMAL.test(value) ? Number(value) / 25.4 : Number.NaN;
  }
  let feet = 0;
  const footMark = value.indexOf("'");
  if (footMark !== -1) {
    const feetText = value.slice(0, footMark).trim();
    if (!DECIMAL.test(feetText)) return Number.NaN;
    feet = Number(feetText);
    value = value.slice(footMark + 1).trim().replace(/^-\s*/, '');
    if (value.includes("'")) return Number.NaN;
  }
  value = value.replace(/\s*"$/, '').trim();
  if (value === '') return footMark === -1 ? Number.NaN : feet * 12;
  return feet * 12 + plainNumber(value);
}

/** An angle in degrees from `45`, `22-1/2` or `11 1/4°`. */
export function parseAngle(text) {
  const value = normalized(text).replace(/\s*°$/, '');
  if (value === '') return undefined;
  return plainNumber(value);
}
