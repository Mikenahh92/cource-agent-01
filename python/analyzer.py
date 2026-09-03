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
from operator import itemgetter

# Compiled once at import time; one alternation covers all levels.
_ENTRY_RE = re.compile(r"^(\d+) (INFO|WARN|ERROR|DEBUG) (\S+) (\d+) (\d+)ms$")


def load_lines(path, chunk_size=500):
    """Load lines, stripping trailing newlines. chunk_size kept for API compat."""
    with open(path) as f:
        return [l.rstrip("\n") for l in f]


def parse(lines):
    """Parse raw lines into entries: ts, level, endpoint, status, ms."""
    entries = []
    for line in lines:
        m = _ENTRY_RE.match(line)
        if m:
            entries.append({"ts": int(m.group(1)), "level": m.group(2),
                            "endpoint": m.group(3), "status": int(m.group(4)),
                            "ms": int(m.group(5)), "raw": line})
    return entries


def filter_errors(entries):
    return [e for e in entries if e["level"] == "ERROR"]


def dedupe(entries):
    """Keep the first occurrence of each duplicate line."""
    result = []
    seen = set()
    for e in entries:
        key = frozenset(e.items())  # hashable, order-independent dict identity
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


def sort_by_time(entries):
    # sorted() is stable and does not mutate the input (like the old bubble sort)
    return sorted(entries, key=itemgetter("ts"))


def aggregate(entries):
    """Count requests and total latency per endpoint."""
    report = {"total": len(entries), "endpoints": {}}
    endpoints = report["endpoints"]
    for e in entries:
        ep = endpoints.get(e["endpoint"])
        if ep is None:
            ep = endpoints[e["endpoint"]] = {"count": 0, "total_ms": 0}
        ep["count"] += 1
        ep["total_ms"] += e["ms"]
    return report


def render(report):
    lines = [f"total_requests: {report['total']}"]
    for ep in sorted(report["endpoints"].keys()):
        d = report["endpoints"][ep]
        lines.append(f"{ep}: {d['count']} requests, {d['total_ms']}ms total")
    return "\n".join(lines) + "\n"


def analyze(path="data/access.log"):
    lines = load_lines(path)
    entries = parse(lines)
    entries = dedupe(entries)
    entries = sort_by_time(entries)
    report = aggregate(entries)
    return render(report)


if __name__ == "__main__":
    print(analyze())
