# Radix sort, most significant digit first

Split by the leading digit, then sort each bucket independently.

| | |
|---|---|
| Best | O(n) |
| Average | O(n·k/d) |
| Worst | O(n·k/d) |
| Memory | O(n + 2^d) |
| Stable | yes |
| Family | non-comparison |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Where LSD makes a fixed number of passes over everything, MSD splits by the leading
digit and recurses into each bucket. Once a bucket holds one element, the work
stops: the remaining digits are never examined.

That early exit is why MSD is the string sort. Comparing dictionary words rarely
needs more than the first few letters, and MSD stops exactly there. The cost is
recursion and many small buckets, where LSD is a flat loop.

## How it runs

1. Bucket the elements by their most significant digit.
2. Recurse into each bucket with the next digit down.
3. Stop when a bucket holds one element or the digits run out.
4. Concatenate in bucket order.

## When it is the right choice

Strings and variable-length keys. Burstsort in this folder is MSD radix with the cache behaviour fixed.
