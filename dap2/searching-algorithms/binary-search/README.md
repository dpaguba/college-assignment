# Binary search

Halve the range until the target is cornered.

| | |
|---|---|
| Average | O(log n) |
| Worst | O(log n) |
| Memory | O(1) |
| Needs | a sorted array |
| Answers | where is this value |

## The idea

Compare with the middle element: either it is the answer, or half the array can be
discarded. A million elements are exhausted in twenty comparisons, a billion in
thirty.

Two classic bugs are worth naming. The loop condition: `low <= high` with
`high = middle - 1` terminates correctly, while `low < high` with `high = middle`
needs a different check after the loop, and mixing the two silently loses the last
element. And `(low + high) / 2` overflows for large arrays in C and Java, a bug that
sat in the JDK for nine years; Python's unbounded integers make it a non-issue here.

The precondition is absolute. On unsorted input it returns a wrong answer rather
than failing, which is worse than being slow.

## How it runs

1. Look at the middle of the current range.
2. Equal: done. Smaller: keep the right half. Larger: keep the left half.
3. Repeat until the range is empty.

## When it is the right choice

The default for repeated lookups in sorted data. It is also the shape of every 'find the boundary' problem: the answer to `bisect` questions, binary search on the answer, and parametric search.
