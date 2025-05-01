# Cycle sort

Write every element straight to its final position, once, and never again.

| | |
|---|---|
| Best | O(n²) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | no |
| Family | selection |

## The idea

Counting how many elements are smaller than x tells you exactly where x belongs. So
compute that position and write x there. Whatever was sitting in that slot now
needs a home, so repeat with it. The chain closes into a cycle, and then you start
the next one.

The result is the theoretical minimum number of writes: every element is written
at most once. Nothing else in this folder can say that.

## How it runs

1. Take the element at position i and count the smaller ones to its right.
2. That count is its destination. Skip past equal keys so it lands after them.
3. Swap it in, take the displaced value, and repeat until the cycle returns to i.

## When it is the right choice

Memory that wears out: flash and EEPROM, where a write costs orders of magnitude
more than a comparison. Paying n² comparisons to avoid a handful of writes is a
sensible trade there and absurd everywhere else.
