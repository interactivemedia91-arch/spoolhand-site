// Spoolhand's simple offset and rolling offset, for the website's free calculators.
//
// The same math as the app (SpoolCore's SimpleOffset and RollingOffset), checked against the app's golden
// vectors in tests/fit.test.mjs. Lengths are inches and angles degrees, center to center; a fitting is
// either a takeout, or a bend radius and the pipe's OD (takeout = R × tan(θ/2), the elbow cut from a 90).
// A result that can't be had comes back as { refused: "missing" | "invalid" | "tooShort" }; a blank field is
// missing, and a result that isn't finite is refused. A value that isn't a length formats as "—", never as 0".

const refuse = (kind) => ({ refused: kind });
const toRadians = (degrees) => (degrees * Math.PI) / 180;
const toDegrees = (radians) => (radians * 180) / Math.PI;

/** A finite number, or undefined when the field is absent or blank; NaN means "invalid". */
function read(inputs, name) {
  const raw = typeof inputs[name] === 'string' ? inputs[name].trim() : inputs[name];
  if (raw === undefined || raw === null || raw === '') return undefined;
  const value = Number(raw);
  return Number.isFinite(value) ? value : Number.NaN;
}

/** The other leg of a right triangle, factored so large lengths aren't squared. */
function otherLeg(hypotenuse, leg) {
  if (hypotenuse <= leg) return Number.NaN;
  return hypotenuse * Math.sqrt(((hypotenuse - leg) / hypotenuse) * (1 + leg / hypotenuse));
}

/** The fitting's allowance at `angle`, from a takeout or from a bend radius; NaN when it can't be had. */
function fitting(inputs, angle) {
  const takeout = read(inputs, 'takeout');
  const radius = read(inputs, 'radius');
  const od = read(inputs, 'od');
  if (takeout !== undefined) return radius === undefined && od === undefined && takeout >= 0 ? { takeout } : null;
  if (radius === undefined || od === undefined) return undefined;
  if (!(radius >= 0) || !(od >= 0)) return null;
  return { takeout: radius * Math.tan(toRadians(angle) / 2), radius, od };
}

/** The arcs along the inside, the centerline and the outside of an elbow trimmed to `angle`. */
function arcs(bend, angle) {
  if (!bend.radius || bend.radius <= bend.od / 2) return {};
  const theta = toRadians(angle);
  return { inner: (bend.radius - bend.od / 2) * theta, center: bend.radius * theta, outer: (bend.radius + bend.od / 2) * theta };
}

/** Travel less both fittings' allowances, one gap per weld, plus thread engagement at each end. */
function cutLength(travel, takeout, inputs) {
  const gap = read(inputs, 'gap') ?? 0;
  const engagement = read(inputs, 'engagement') ?? 0;
  if (!(gap >= 0) || !(engagement >= 0)) return Number.NaN;
  return travel - 2 * takeout - 2 * gap + 2 * engagement;
}

/** Two equal fittings move the line sideways by `offset`: from the fitting angle, or from the run. */
export function simpleOffset(inputs) {
  const offset = read(inputs, 'offset');
  const givenAngle = read(inputs, 'angle');
  const givenRun = read(inputs, 'run');
  if ((givenAngle === undefined) === (givenRun === undefined)) return refuse('invalid');
  if (offset === undefined) return refuse('missing');
  if (!(offset > 0)) return refuse('invalid');

  let angle, travel, run;
  if (givenAngle !== undefined) {
    if (!(givenAngle > 0 && givenAngle < 90)) return refuse('invalid');
    angle = givenAngle;
    travel = offset / Math.sin(toRadians(angle));
    run = offset / Math.tan(toRadians(angle));
  } else {
    if (!(givenRun > 0)) return refuse('invalid');
    run = givenRun;
    travel = Math.hypot(offset, run);
    angle = toDegrees(Math.atan2(offset, run));
  }

  const bend = fitting(inputs, angle);
  if (bend === undefined) return refuse('missing');
  if (bend === null) return refuse('invalid');
  const cut = cutLength(travel, bend.takeout, inputs);
  if (Number.isNaN(cut)) return refuse('invalid');
  if (cut <= 0) return refuse('tooShort');
  const result = { travel, run, angle, takeout: bend.takeout, cut, ...arcs(bend, angle) };
  return Object.values(result).every(Number.isFinite) ? result : refuse('invalid');
}

/**
 * A rolling offset from any three consistent values of set, roll, true offset, run, travel and angle.
 * Set and roll are the offset's two sides; the true offset is their diagonal, the travel the hypotenuse
 * of true offset and run.
 */
export function rollingOffset(inputs) {
  const names = ['set', 'roll', 'trueOffset', 'run', 'travel'];
  const given = {};
  for (const name of names) {
    const value = read(inputs, name);
    if (value === undefined) continue;
    if (!(value > 0)) return refuse('invalid');
    given[name] = value;
  }
  const givenAngle = read(inputs, 'angle');
  if (givenAngle !== undefined && !(givenAngle > 0 && givenAngle < 90)) return refuse('invalid');
  if (givenAngle !== undefined) given.angle = givenAngle;
  const keys = Object.keys(given);
  const count = (list) => list.filter((name) => name in given).length;
  if (keys.length > 3 || count(['set', 'roll', 'trueOffset']) > 2 || count(['trueOffset', 'run', 'travel', 'angle']) > 2) {
    return refuse('invalid');
  }

  let { set, roll, trueOffset: offset, run, travel, angle } = given;
  if (offset !== undefined) {
    if ((set !== undefined && offset <= set) || (roll !== undefined && offset <= roll)) return refuse('invalid');
  } else if (set !== undefined && roll !== undefined) {
    offset = Math.hypot(set, roll);
  }
  if (travel !== undefined && ((run !== undefined && travel <= run) || (offset !== undefined && travel <= offset))) {
    return refuse('invalid');
  }

  if (angle !== undefined) {
    const theta = toRadians(angle);
    if (offset !== undefined) { travel = offset / Math.sin(theta); run = offset / Math.tan(theta); }
    else if (run !== undefined) { offset = run * Math.tan(theta); travel = run / Math.cos(theta); }
    else if (travel !== undefined) { offset = travel * Math.sin(theta); run = travel * Math.cos(theta); }
    else return refuse('missing');
  } else if (offset !== undefined && run !== undefined) {
    travel = Math.hypot(offset, run);
    angle = toDegrees(Math.atan2(offset, run));
  } else if (offset !== undefined && travel !== undefined) {
    run = otherLeg(travel, offset);
    angle = toDegrees(Math.atan2(offset, run));
  } else if (run !== undefined && travel !== undefined) {
    offset = otherLeg(travel, run);
    angle = toDegrees(Math.atan2(offset, run));
  } else {
    return refuse('missing');
  }
  if (![offset, run, travel].every((value) => Number.isFinite(value) && value > 0) || !(angle > 0 && angle < 90)) {
    return refuse('invalid');
  }
  if (set !== undefined && roll === undefined) roll = otherLeg(offset, set);
  else if (roll !== undefined && set === undefined) set = otherLeg(offset, roll);

  const bend = fitting(inputs, angle);
  if (bend === undefined) return refuse('missing');
  if (bend === null || !Number.isFinite(bend.takeout)) return refuse('invalid');
  const cut = cutLength(travel, bend.takeout, inputs);
  if (Number.isNaN(cut)) return refuse('invalid');
  if (cut <= 0) return refuse('tooShort');

  const result = { trueOffset: offset, run, travel, angle, takeout: bend.takeout, cut, ...arcs(bend, angle) };
  if (set !== undefined && roll !== undefined) {
    Object.assign(result, { set, roll, rollAngle: toDegrees(Math.atan2(roll, set)) });
  }
  return Object.values(result).every(Number.isFinite) ? result : refuse('invalid');
}

/** `26-3/16"`: the nearest 1/16 (or 1/32), ties away from zero, like a tape measure and the app. */
export function formatInches(inches, denominator = 16) {
  if (!Number.isFinite(inches)) return '—';
  const exact = Math.abs(inches) * denominator;
  const rounded = Math.floor(exact + 0.5);   // magnitude rounded half up = ties away from zero
  const whole = Math.floor(rounded / denominator);
  let numerator = rounded % denominator;
  let bottom = denominator;
  if (numerator !== 0) {
    const divisor = gcd(numerator, denominator);
    numerator /= divisor;
    bottom /= divisor;
  }
  const sign = inches < 0 && rounded !== 0 ? '-' : '';
  const body = numerator === 0 ? `${whole}` : whole === 0 ? `${numerator}/${bottom}` : `${whole}-${numerator}/${bottom}`;
  return `${sign}${body}"`;
}

const millimeterFormat = new Intl.NumberFormat('en-US', { maximumFractionDigits: 1, useGrouping: false, roundingMode: 'halfEven' });
const angleFormat = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: false, roundingMode: 'halfEven' });

/** `665.6 mm`. */
export function formatMillimeters(inches) {
  if (!Number.isFinite(inches)) return '—';
  const text = millimeterFormat.format(inches * 25.4);
  return `${text === '-0' ? '0' : text} mm`;
}

/** `30.65°`. */
export function formatAngle(degrees) {
  return `${angleFormat.format(degrees)}°`;
}

function gcd(a, b) {
  return b === 0 ? a : gcd(b, a % b);
}
