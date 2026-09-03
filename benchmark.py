"""Benchmark for sorter.sort().

Exit code 0 means the sort is fast enough (< 50 ms for 20k ints).
"""
import random
import sys
import time

from sorter import sort

LIMIT_MS = 50.0
SIZE = 10000


def main():
    data = [random.randint(0, 1_000_000) for _ in range(SIZE)]
    start = time.perf_counter()
    result = sort(data)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    assert result == sorted(data), "sort() returned wrong result!"
    print(f"Sorted {SIZE} ints in {elapsed_ms:.1f} ms (limit: {LIMIT_MS} ms)")
    if elapsed_ms < LIMIT_MS:
        print("PASS")
        return 0
    print("FAIL — too slow")
    return 1


if __name__ == "__main__":
    sys.exit(main())
