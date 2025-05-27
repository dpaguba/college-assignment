# Selection sort

Find the smallest remaining element, swap it into place, repeat.

| | |
|---|---|
| Best | O(n²) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | no |
| Family | selection |

## The idea

The most direct reading of "sort": find the smallest, put it first, then do the
same with the rest.

It has no best case. The scan for the minimum looks at everything regardless, so
an already sorted list costs the same n(n-1)/2 comparisons as a reversed one. What
it does have is a minimum of writes: exactly n-1 swaps, whatever the input.

## How it runs

1. Scan positions i..n-1 for the smallest key.
2. Swap it with position i.
3. Move i forward.

## When it is the right choice

When writing is expensive and reading is not: EEPROM, flash, anything with limited
write cycles. Cycle sort takes that idea further and writes each element at most
once.
