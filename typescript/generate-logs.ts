/** Generate a deterministic access log for the analyzer (fixed seed). */
import * as fs from "fs";

const LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"];
const ENDPOINTS = ["/api/users", "/api/orders", "/api/items", "/health", "/metrics", "/login"];
const STATUS = [200, 201, 204, 400, 401, 404, 500];

// deterministic LCG so both generators produce comparable data
function makeRng(seed: number) {
  let s = seed;
  return () => (s = (s * 1103515245 + 12345) % 2147483648) / 2147483648;
}

export function generate(n = 25000, path = "data/access.log"): void {
  const rnd = makeRng(42);
  const pick = <T>(arr: T[]): T => arr[Math.floor(rnd() * arr.length)];
  const lines: string[] = [];
  let t = 1_700_000_000;
  for (let i = 0; i < n; i++) {
    t += Math.floor(rnd() * 30) + 1;
    lines.push(`${t} ${pick(LEVELS)} ${pick(ENDPOINTS)} ${pick(STATUS)} ${Math.floor(rnd() * 500) + 1}ms`);
  }
  // ~10% exact duplicates — the analyzer is supposed to dedupe these
  const dupes: string[] = [];
  for (let i = 0; i < Math.floor(n / 10); i++) dupes.push(lines[Math.floor(rnd() * n)]);
  lines.push(...dupes);
  // shuffle deterministically
  for (let i = lines.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [lines[i], lines[j]] = [lines[j], lines[i]];
  }
  fs.mkdirSync("data", { recursive: true });
  fs.writeFileSync(path, lines.join("\n") + "\n");
  console.log(`wrote ${lines.length} lines to ${path}`);
}

if (process.argv[1] && process.argv[1].endsWith("generate-logs.ts")) {
  generate(process.argv[2] ? parseInt(process.argv[2]) : 25000);
}
