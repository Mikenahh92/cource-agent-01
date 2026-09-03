"""Sorter module. See ISSUE.md — this is embarrassingly slow."""


def sort(data):
    """Sort a list of integers and return a new sorted list.

    Uses a hand-rolled bubble sort because "it was easy to write".
    """
    items = list(data)
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items
