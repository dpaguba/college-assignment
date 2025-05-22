# Radix sort, least significant digit first

One stable counting sort per digit, from the last digit to the first.

| | |
|---|---|
| Best | O(n·k/d) |
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

Sort by the last digit, then by the second to last, and so on. The reason this works
is subtle and worth stating: each pass must be stable, so the order established by
the previous, less significant digit survives inside every group. After the final
pass the numbers are fully ordered.

Negative keys have no digits, so they are sorted by absolute value and reversed in
front.

## How it runs

1. For digit position 1, 10, 100 and so on up to the largest key:
2. Run a stable counting sort on that digit alone.

## When it is the right choice

Fixed-width keys in bulk: integers, dates, IP addresses, fixed-length strings. It is the fastest way to sort a few million integers when memory allows.
