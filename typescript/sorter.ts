/**
 * Sorting module — O(n log n) implementation.
 *
 * Uses the engine's built-in Array.prototype.sort (TimSort in V8), which is
 * far faster than the previous hand-rolled bubble sort (O(n^2)).
 *
 * Notes:
 * - The default comparator sorts lexicographically, so we must pass an
 *   explicit numeric one.
 * - We use a comparison form rather than `(a, b) => a - b` to avoid the
 *   overflow edge case with values near Number.MAX_SAFE_INTEGER.
 */
export function sort(data: number[]): number[] {
  const arr = [...data]; // do not mutate the input
  arr.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
  return arr;
}
