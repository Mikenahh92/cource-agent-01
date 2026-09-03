/** Per-stage benchmark. Exit 0 only if total < LIMIT_MS and output matches golden. */
import * as fs from "fs";
import * as path from "path";
import { loadLines, parse, dedupe, sortByTime, aggregate, render, analyze } from "./analyzer";
import { generate } from "./generate-logs";

const LIMIT_MS = 200;

function timeIt<T>(fn: () => T): [T, number] {
  const t0 = performance.now();
  const out = fn();
  return [out, performance.now() - t0];
}

function main() {
  if (!fs.existsSync("data/access.log")) {
    console.log("data/access.log missing — generating (deterministic)...");
    generate();
  }
  const t: Record<string, number> = {};
  let lines: string[]; let entries; let report: ReturnType<typeof aggregate>; let output: string;
  [lines, t.load] = timeIt(() => loadLines("data/access.log"));
  [entries, t.parse] = timeIt(() => parse(lines));
  let deduped; [deduped, t.dedupe] = timeIt(() => dedupe(entries));
  let sorted; [sorted, t.sort] = timeIt(() => sortByTime(deduped));
  [report, t.aggregate] = timeIt(() => aggregate(sorted));
  [output, t.render] = timeIt(() => render(report));

  const totalMs = Object.values(t).reduce((a, b) => a + b, 0);
  for (const [k, v] of Object.entries(t)) console.log(`  ${k.padEnd(10)} ${v.toFixed(1).padStart(9)} ms`);
  console.log(`  ${"TOTAL".padEnd(10)} ${totalMs.toFixed(1).padStart(9)} ms  (limit: ${LIMIT_MS} ms)`);

  const expected = fs.readFileSync("expected-report.txt", "utf8");
  if (output !== expected) { console.error("FAIL — output differs from expected-report.txt"); process.exit(1); }
  if (totalMs >= LIMIT_MS) { console.error("FAIL — too slow"); process.exit(1); }
  console.log("PASS");
}
main();
