# Spreadsort

Radix or comparison sorting, chosen per piece by measuring the key range.

| | |
|---|---|
| Best | O(n) |
| Average | O(n·k/d) |
| Worst | O(n·(k/s + d)) |
| Memory | O(k/d · 2^d) |
| Stable | no |
| Family | non-comparison |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Steven Ross's hybrid, the default integer sort in Boost. Pure radix pays for every
digit even when the data barely needs sorting; pure comparison sorting pays log n
per element regardless of key width. Spreadsort measures the range at each step and
picks: wide range and enough elements means split by the top bits, otherwise hand
the piece to a comparison sort.

The result behaves like radix where radix wins and like introsort where it does
not.

## How it runs

1. If the piece is small, sort it by comparison and stop.
2. Measure the key range; if it is too narrow for a split to pay off, sort by
   comparison.
3. Otherwise bucket by the leading bits and recurse into each bucket.

## When it is the right choice

Large integer and float arrays of unknown distribution, where you want radix speed without radix's bad cases.
