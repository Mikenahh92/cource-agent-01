"""Sorter module. See ISSUE.md — use the built-in Timsort (O(n log n))."""


def sort(data):
    """Sort a list of integers and return a new sorted list.

    Delegates to Python's built-in sorted(), which uses Timsort.
    Returns a new list; the input is not mutated.
    """
    return sorted(data)
