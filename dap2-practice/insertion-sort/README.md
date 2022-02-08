# Insertion sort

Insertion sort with a comparison counter. Practical sheet 2, task 2.1.

```
java InsertionSort 10 ab
10 9 8 7 6 5 4 3 2 1
1 2 3 4 5 6 7 8 9 10
Feld ist sortiert!
Das Sortieren des Arrays hat 45 Vergleiche benoetigt.
```

## The algorithm

Keep a sorted prefix and insert the next element into it by shifting everything
larger one place right. The loop invariant is that before iteration i the range
`array[0..i-1]` holds the first i input elements in order.

Θ(n²) comparisons on a descending input, Θ(n) on an ascending one, because the
inner loop then fails its first test every time. That gap is the whole reason
insertion sort survives: it is the fastest thing there is on nearly sorted data
and on very short arrays, which is why real sort implementations fall back to
it below a threshold of a few dozen elements.

## What counts as a comparison

Only the element-to-element test. Reaching the left end of the array is a
bounds check and is not counted, which is exactly what makes ten descending
elements cost 45 = 9 + 8 + … + 1 comparisons, the number the sheet prescribes.

## Verification

The sample call, matching 45 comparisons, and all three error cases. The
assertion on `isSorted` runs with `java -ea`.

The one thing the sheet leaves open is the range of the random values, so
`rng.nextInt(1000)` with the prescribed seed 951 is a choice, not a
requirement.
