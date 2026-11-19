// Butt-weld elbows from the app's reference data, and the fitting an offset uses at its angle,
// the way the app's FitData picks it: a long-radius 45 from the table at 45°, otherwise a 90 cut
// to the angle (takeout = R × tan(θ/2)). A value the tables don't have is never made up.

/** Metric size (DN) for each nominal pipe size. */
export const DN = {
  '1/2': 15, '3/4': 20, '1': 25, '1-1/4': 32, '1-1/2': 40, '2': 50, '2-1/2': 65, '3': 80, '3-1/2': 90,
  '4': 100, '5': 125, '6': 150, '8': 200, '10': 250, '12': 300, '14': 350, '16': 400, '18': 450, '20': 500,
  '22': 550, '24': 600, '26': 650, '28': 700, '30': 750, '32': 800, '34': 850, '36': 900, '38': 950,
  '40': 1000, '42': 1050, '44': 1100, '46': 1150, '48': 1200,
};

/** "ASME B16.9 · 3 catalogs", or "Derived · A = 1.5 × NPS", as the app labels a value. */
function provenance(cell, standard) {
  if (cell.formula) return `Derived · ${cell.formula}`;
  const count = cell.sources.length;
  return `${standard} · ${count} ${count === 1 ? 'catalog' : 'catalogs'}`;
}

/** One entry per elbow size: center-to-end values with their provenance, and the pipe's OD when known. */
export function elbowSizes(reference) {
  const table = (id) => reference.tables.find((t) => t.id === id);
  const elbows = table('bw-elbows');
  const od = new Map();
  for (const row of table('pipe').rows) {
    if (!od.has(row.key.nps) && row.cells.od) od.set(row.key.nps, row.cells.od.number);
  }
  return elbows.rows.map((row) => {
    const value = (id) => {
      const cell = row.cells[id];
      return cell ? { value: cell.number, source: provenance(cell, elbows.standard), sources: cell.sources } : null;
    };
    const nps = row.key.nps;
    return { nps, dn: DN[nps], od: od.get(nps) ?? null, lr90: value('lr90'), lr45: value('lr45'), sr90: value('sr90') };
  });
}

/** The sizes a calculator offers: those with a pipe OD, like the app's spec bar. */
export function calculatorSizes(sizes) {
  return sizes.filter((size) => size.od !== null && size.lr90);
}

const ANGLE_TOLERANCE = 1e-6;

/**
 * The elbow at `angle` for `size` and `elbow` ("lr" or "sr"):
 * `{ takeout, source }` for a stock 45, `{ radius, od, source }` for a 90 cut to the angle,
 * or `{ missing }` with what to do when the tables don't have it.
 */
export function elbowAt(size, elbow, angle) {
  const name = `${size.nps}"`;
  if (elbow === 'lr' && Math.abs(angle - 45) < ANGLE_TOLERANCE) {
    if (!size.lr45) return { missing: `No 45° long-radius elbow for ${name} in the tables. Enter the measured takeout.` };
    return { takeout: size.lr45.value, source: size.lr45.source };
  }
  const ninety = elbow === 'sr' ? size.sr90 : size.lr90;
  if (!ninety) {
    const kind = elbow === 'sr' ? 'short' : 'long';
    return { missing: `No 90° ${kind}-radius elbow for ${name} in the tables. Enter the measured takeout.` };
  }
  return { radius: ninety.value, od: size.od, source: ninety.source };
}
