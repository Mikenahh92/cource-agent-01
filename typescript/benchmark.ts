import { sort } from "./sorter";

const N = 60000;
const LIMIT_MS = 50;

function makeData(n: number): number[] {
  // deterministic pseudo-random data
  let seed = 42;
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    out.push(seed % 1000000);
  }
  return out;
}

const data = makeData(N);
const t0 = performance.now();
const result = sort(data);
const ms = performance.now() - t0;

// correctness check
const expected = [...data].sort((a, b) => a - b);
const correct = result.length === expected.length && result.every((v, i) => v === expected[i]);

console.log(`Sorted ${N} ints in ${ms.toFixed(1)} ms (limit: ${LIMIT_MS} ms)`);
if (!correct) { console.error("FAIL — not sorted correctly"); process.exit(1); }
if (ms >= LIMIT_MS) { console.error("FAIL — too slow"); process.exit(1); }
console.log("PASS");
