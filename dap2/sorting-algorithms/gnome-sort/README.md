# Gnome sort

Step forward when the pair is ordered, step back and swap when it is not.

| | |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |
| Memory | O(1) |
| Stable | yes |
| Family | insertion |

## The idea

Named for a garden gnome sorting flower pots: he looks at the pot beside him, and
if the two are in the wrong order he swaps them and steps back, otherwise he steps
forward.

It performs exactly the work insertion sort performs, with one index and no inner
loop. The value is pedagogical: it shows that the nested loop in insertion sort is
bookkeeping, not substance.

## How it runs

1. If at the start, or the pair is in order, step forward.
2. Otherwise swap and step back.
3. Stop at the end.

## When it is the right choice

Nowhere in particular. It is the shortest correct sort that is not a joke.
