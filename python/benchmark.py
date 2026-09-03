"""Benchmark for the log analyzer.

Prints per-stage timings, then the total. Exit code 0 only if:
  - total < LIMIT_MS
  - output is byte-identical to expected_report.txt
Run:  python generate_logs.py && python benchmark.py
"""
import os
import sys
import time

import analyzer

LIMIT_MS = 200

STAGES = [
    ("load", lambda: analyzer.load_lines("data/access.log")),
    ("parse", None), ("dedupe", analyzer.dedupe),
    ("sort", analyzer.sort_by_time), ("aggregate", analyzer.aggregate),
    ("render", analyzer.render),
]


def main():
    if not os.path.exists("data/access.log"):
        print("data/access.log missing — generating (deterministic)...")
        import generate_logs
        generate_logs.main()

    t = {}
    t0 = time.perf_counter(); lines = analyzer.load_lines("data/access.log"); t["load"] = time.perf_counter() - t0
    t0 = time.perf_counter(); entries = analyzer.parse(lines); t["parse"] = time.perf_counter() - t0
    t0 = time.perf_counter(); entries = analyzer.dedupe(entries); t["dedupe"] = time.perf_counter() - t0
    t0 = time.perf_counter(); entries = analyzer.sort_by_time(entries); t["sort"] = time.perf_counter() - t0
    t0 = time.perf_counter(); report = analyzer.aggregate(entries); t["aggregate"] = time.perf_counter() - t0
    t0 = time.perf_counter(); output = analyzer.render(report); t["render"] = time.perf_counter() - t0

    total_ms = sum(t.values()) * 1000
    for k in t:
        print(f"  {k:<10} {t[k]*1000:9.1f} ms")
    print(f"  {'TOTAL':<10} {total_ms:9.1f} ms  (limit: {LIMIT_MS} ms)")

    with open("expected_report.txt") as f:
        expected = f.read()
    if output != expected:
        print("FAIL — output differs from expected_report.txt")
        sys.exit(1)
    if total_ms >= LIMIT_MS:
        print("FAIL — too slow")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
