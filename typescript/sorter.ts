/**
 * Sorting module.
 *
 * Uses the built-in Array.prototype.sort with a numeric comparator.
 * V8 implements this as TimSort — stable, O(n log n) — which replaces the
 * previous hand-rolled bubble sort (O(n^2)).
 */
export function sort(data: number[]): number[] {
  // Array.prototype.sort mutates in place, so copy first to keep the
  // non-mutating contract. The comparator is required: the default sort
  // compares elements as strings (lexicographic), not as numbers.
  return [...data].sort((a, b) => a - b);
}
