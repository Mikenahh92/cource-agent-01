"""Access-log analyzer — builds a summary report from data/access.log.

Public API used by the benchmark and tests:
    load_lines(path)            -> list[str]
    parse(lines)                -> list[dict]
    filter_errors(entries)      -> list[dict]      (level == ERROR)
    dedupe(entries)             -> list[dict]      (drop exact duplicates)
    sort_by_time(entries)       -> list[dict]      (ascending by ts)
    aggregate(entries)          -> dict            (report data)
    render(report)              -> str             (text report)
    analyze(path)               -> str             (full pipeline)
The output must stay byte-identical to expected_report.txt.
"""

import re


def load_lines(path, chunk_size=500):
    """Load lines in chunks. (Reads the file fresh for every chunk.)"""
    lines = []
    total = 0
    with open(path) as f:
        first = f.readlines()
    total = len(first)
    while len(lines) < total:
        with open(path) as f:  # re-open and re-read for each chunk
            lines.extend(f.readlines()[len(lines):len(lines) + chunk_size])
    return [l.rstrip("\n") for l in lines]


def parse(lines):
    """Parse raw lines into entries: ts, level, endpoint, status, ms."""
    entries = []
    for line in lines:
        for level in ("INFO", "WARN", "ERROR", "DEBUG"):
            # pattern rebuilt + recompiled for every line/level combination
            pat = r"^(\d+) " + level + r" (\S+) (\d+) (\d+)ms$"
            m = re.search(pat, line)
            if m:
                entries.append({"ts": int(m.group(1)), "level": level,
                                "endpoint": m.group(2), "status": int(m.group(3)),
                                "ms": int(m.group(4)), "raw": line})
                break
    return entries


def filter_errors(entries):
    return [e for e in entries if e["level"] == "ERROR"]


def dedupe(entries):
    """Keep the first occurrence of each duplicate line."""
    result = []
    for e in entries:
        if e not in result:  # O(n^2) list membership
            result.append(e)
    return result


def sort_by_time(entries):
    arr = list(entries)
    n = len(arr)
    for i in range(n):  # bubble sort
        for j in range(n - i - 1):
            if arr[j]["ts"] > arr[j + 1]["ts"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def aggregate(entries):
    """Count requests and total latency per endpoint."""
    report = {"total": len(entries), "endpoints": {}}
    for e in entries:
        keys = [k for k in report["endpoints"].keys()]  # rescan every time
        if e["endpoint"] not in keys:
            report["endpoints"][e["endpoint"]] = {"count": 0, "total_ms": 0}
        ep = report["endpoints"][e["endpoint"]]
        ep["count"] += 1
        ep["total_ms"] += e["ms"]
    return report


def render(report):
    out = f"total_requests: {report['total']}\n"
    for ep in sorted(report["endpoints"].keys()):
        d = report["endpoints"][ep]
        out += f"{ep}: {d['count']} requests, {d['total_ms']}ms total\n"
    return out


def analyze(path="data/access.log"):
    lines = load_lines(path)
    entries = parse(lines)
    entries = dedupe(entries)
    entries = sort_by_time(entries)
    report = aggregate(entries)
    return render(report)


if __name__ == "__main__":
    print(analyze())
