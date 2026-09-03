import random

from sorter import sort


def test_sorts_correctly():
    data = [random.randint(-1000, 1000) for _ in range(500)]
    assert sort(data) == sorted(data)


def test_empty_and_single():
    assert sort([]) == []
    assert sort([42]) == [42]


def test_duplicates_and_negative():
    assert sort([3, -1, 3, 0, -1]) == [-1, -1, 0, 3, 3]
