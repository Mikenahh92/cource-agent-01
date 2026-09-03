import { test } from "node:test";
import assert from "node:assert/strict";
import { parse, dedupe, sortByTime, filterErrors, aggregate, render } from "./analyzer";

test("parse parses a valid line", () => {
  const e = parse(["1700000000 INFO /health 200 5ms"])[0];
  assert.deepEqual(e, { ts: 1700000000, level: "INFO", endpoint: "/health", status: 200, ms: 5, raw: "1700000000 INFO /health 200 5ms" });
});

test("parse skips bad lines", () => {
  assert.deepEqual(parse(["garbage line", ""]), []);
});

test("dedupe keeps first occurrence", () => {
  const a = { ts: 1, level: "INFO", endpoint: "/a", status: 200, ms: 1, raw: "x" };
  const b = { ts: 2, level: "INFO", endpoint: "/a", status: 200, ms: 1, raw: "y" };
  assert.deepEqual(dedupe([a, a, b, a]), [a, b]);
});

test("sortByTime sorts and does not mutate", () => {
  const xs = [{ ts: 3 }, { ts: 1 }, { ts: 2 }] as any[];
  assert.deepEqual(sortByTime(xs).map(e => e.ts), [1, 2, 3]);
  assert.deepEqual(xs.map(e => e.ts), [3, 1, 2]);
});

test("filterErrors", () => {
  const es = [{ level: "ERROR" }, { level: "INFO" }, { level: "ERROR" }] as any[];
  assert.equal(filterErrors(es).length, 2);
});

test("aggregate counts and sums", () => {
  const es: any[] = [
    { endpoint: "/a", ms: 10 }, { endpoint: "/a", ms: 5 }, { endpoint: "/b", ms: 1 }];
  const r = aggregate(es);
  assert.equal(r.total, 3);
  assert.deepEqual(r.endpoints["/a"], { count: 2, total_ms: 15 });
});

test("render format", () => {
  const out = render({ total: 1, endpoints: { "/a": { count: 1, total_ms: 2 } } });
  assert.equal(out, "total_requests: 1\n/a: 1 requests, 2ms total\n");
});
