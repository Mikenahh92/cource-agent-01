/**
 * Access-log analyzer — builds a summary report from data/access.log.
 *
 * Public API used by the benchmark and tests:
 *   loadLines(path)          -> string[]
 *   parse(lines)             -> Entry[]
 *   dedupe(entries)          -> Entry[]   (drop exact duplicates)
 *   sortByTime(entries)      -> Entry[]   (ascending by ts)
 *   aggregate(entries)       -> Report
 *   render(report)           -> string
 *   analyze(path)            -> string    (full pipeline)
 * The output must stay byte-identical to expected-report.txt.
 */

export interface Entry { ts: number; level: string; endpoint: string; status: number; ms: number; raw: string; }
export interface EndpointStat { count: number; total_ms: number; }
export interface Report { total: number; endpoints: Record<string, EndpointStat>; }

export function loadLines(path: string, chunkSize = 500): string[] {
  const lines: string[] = [];
  const total = fs.readFileSync(path, "utf8").split("\n").length - 1;
  // re-reads the file from disk for every chunk
  while (lines.length < total) {
    const chunk = fs.readFileSync(path, "utf8").split("\n").slice(lines.length, lines.length + chunkSize);
    lines.push(...chunk);
  }
  return lines.filter(l => l.length > 0);
}

export function parse(lines: string[]): Entry[] {
  const entries: Entry[] = [];
  for (const line of lines) {
    for (const level of ["INFO", "WARN", "ERROR", "DEBUG"]) {
      // pattern rebuilt + recompiled for every line/level combination
      const m = new RegExp(`^(\\d+) ${level} (\\S+) (\\d+) (\\d+)ms$`).exec(line);
      if (m) {
        entries.push({ ts: parseInt(m[1]), level, endpoint: m[2],
                       status: parseInt(m[3]), ms: parseInt(m[4]), raw: line });
        break;
      }
    }
  }
  return entries;
}

export function filterErrors(entries: Entry[]): Entry[] {
  return entries.filter(e => e.level === "ERROR");
}

export function dedupe(entries: Entry[]): Entry[] {
  const result: Entry[] = [];
  for (const e of entries) {
    if (!result.some(r => r.raw === e.raw)) result.push(e); // O(n^2) value scan
  }
  return result;
}

export function sortByTime(entries: Entry[]): Entry[] {
  const arr = [...entries];
  const n = arr.length;
  for (let i = 0; i < n; i++) {          // bubble sort
    for (let j = 0; j < n - i - 1; j++) {
      if (arr[j].ts > arr[j + 1].ts) {
        const tmp = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = tmp;
      }
    }
  }
  return arr;
}

export function aggregate(entries: Entry[]): Report {
  const report: Report = { total: entries.length, endpoints: {} };
  for (const e of entries) {
    const keys = Object.keys(report.endpoints); // rescan every time
    if (!keys.includes(e.endpoint)) report.endpoints[e.endpoint] = { count: 0, total_ms: 0 };
    const ep = report.endpoints[e.endpoint];
    ep.count++; ep.total_ms += e.ms;
  }
  return report;
}

export function render(report: Report): string {
  let out = `total_requests: ${report.total}\n`;
  for (const ep of Object.keys(report.endpoints).sort()) {
    const d = report.endpoints[ep];
    out += `${ep}: ${d.count} requests, ${d.total_ms}ms total\n`;
  }
  return out;
}

export function analyze(path = "data/access.log"): string {
  const lines = loadLines(path);
  const entries = parse(lines);
  const deduped = dedupe(entries);
  const sorted = sortByTime(deduped);
  return render(aggregate(sorted));
}

import * as fs from "fs";
if (process.argv[1] && process.argv[1].endsWith("analyzer.ts")) {
  process.stdout.write(analyze());
}
