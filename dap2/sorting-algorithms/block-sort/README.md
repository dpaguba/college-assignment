# Block sort

A stable merge sort that borrows its own array as scratch space.

| | |
|---|---|
| Best | O(n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(1) in the full algorithm |
| Stable | yes |
| Family | hybrid |

## The idea

Also called WikiSort. Merge sort is stable and n log n but wants n spare slots. The
in-place merges that avoid that are usually unstable or add a log factor. Block sort
gets all three properties at once by taking a section of the array itself as an
internal buffer, merging fixed-size blocks by rotation, and restoring the buffer at
the end.

**What this implementation does and does not do.** It keeps the shape: insertion
sort on short runs, bottom-up merging, and merges performed by rotation rather than
by copying. It leaves out the buffer extraction, so the memory here is the recursion
stack rather than a true O(1), and the merge costs a log factor. The O(1) claim is
the entire point of the real algorithm, so it is named rather than quietly
inherited.

## How it runs

1. Insertion sort every block of 16.
2. Merge blocks pairwise, doubling the width each round.
3. Merge by splitting the longer run at its median, binary searching for that value
   in the other run, and rotating the middle blocks past each other.

## When it is the right choice

Where stability and bounded memory are both required. In practice most standard libraries choose timsort and accept the n extra slots.
