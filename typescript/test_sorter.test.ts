import { test } from "node:test";
import assert from "node:assert/strict";
import { sort } from "./sorter";

test("sorts random ints", () => {
  const data = [5, 3, 9, 1, 7];
  assert.deepEqual(sort(data), [1, 3, 5, 7, 9]);
});

test("handles empty and single element", () => {
  assert.deepEqual(sort([]), []);
  assert.deepEqual(sort([42]), [42]);
});

test("handles duplicates and negatives", () => {
  assert.deepEqual(sort([3, -1, 3, 0, -1]), [-1, -1, 0, 3, 3]);
});

test("does not mutate input", () => {
  const data = [2, 1];
  sort(data);
  assert.deepEqual(data, [2, 1]);
});
