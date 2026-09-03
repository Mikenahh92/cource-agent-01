import analyzer


def test_parse():
    e = analyzer.parse(["1700000000 INFO /health 200 5ms"])[0]
    assert e == {"ts": 1700000000, "level": "INFO", "endpoint": "/health",
                 "status": 200, "ms": 5, "raw": "1700000000 INFO /health 200 5ms"}


def test_parse_skips_bad_lines():
    assert analyzer.parse(["garbage line", ""]) == []


def test_dedupe():
    a = {"raw": "x"}; b = {"raw": "y"}
    assert analyzer.dedupe([a, a, b, a]) == [a, b]


def test_sort():
    import itertools
    xs = [{"ts": 3}, {"ts": 1}, {"ts": 2}]
    assert [e["ts"] for e in analyzer.sort_by_time(xs)] == [1, 2, 3]
    assert xs == [{"ts": 3}, {"ts": 1}, {"ts": 2}]  # no mutation


def test_filter_errors():
    es = [{"level": "ERROR"}, {"level": "INFO"}, {"level": "ERROR"}]
    assert analyzer.filter_errors(es) == [{"level": "ERROR"}, {"level": "ERROR"}]


def test_aggregate():
    es = [{"endpoint": "/a", "ms": 10}, {"endpoint": "/a", "ms": 5}, {"endpoint": "/b", "ms": 1}]
    r = analyzer.aggregate(es)
    assert r["total"] == 3
    assert r["endpoints"]["/a"] == {"count": 2, "total_ms": 15}
    assert r["endpoints"]["/b"] == {"count": 1, "total_ms": 1}


def test_render():
    out = analyzer.render({"total": 1, "endpoints": {"/a": {"count": 1, "total_ms": 2}}})
    assert out == "total_requests: 1\n/a: 1 requests, 2ms total\n"
