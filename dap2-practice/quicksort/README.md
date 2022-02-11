# Quicksort

Quicksort with a random pivot, sorting descending. Practical sheet 3, task 3.1.

```
java QuickSort 10 -5 1 0 3 -42 -19 2 -1 10 5 3
10, 10, 5, 3, 3, 2, 1, 0, -1, -5, -19, -42
8
```

The second line is the number of calls to `partition`.

## The algorithm

Partition puts the pivot where it belongs and guarantees everything to its left
is at least as large, so the two sides are sorted independently with no merge
step. The work is in the split, not in the combine, which is the mirror image
of merge sort.

Expected O(n log n) with a random pivot, Θ(n²) in the worst case. A fixed pivot
makes that worst case reachable by sorted input, which is common; a random one
makes it a matter of luck that no adversary controls.

## Reproducibility

Three things have to agree for the partition count to match: the seed 1337, one
single generator created once, and descending into the left half first. The
sheet pins all three down, and the counts it lists are 8, 12 and 668. All three
come out.

## One trap

The pseudocode's inner walk `while A[i] < pivot do i++` has no bounds test, and
adding one breaks it. It is safe as written because the pivot sits at position
r and stops the walk. Guarding it with `i < j` makes i stop early, and the array
comes out unsorted on the second example. That was a real bug here, caught by
the assertion.

## Verification

All three examples from the sheet, exactly, plus both error cases.
