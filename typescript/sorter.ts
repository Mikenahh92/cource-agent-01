/**
 * Sorting module — deliberately slow implementation (bubble sort).
 * Target for the optimization assignment: see the issue tracker.
 */
export function sort(data: number[]): number[] {
  const arr = [...data];
  const n = arr.length;
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        const tmp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = tmp;
      }
    }
  }
  return arr;
}
