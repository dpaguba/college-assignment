# Introsort

Quicksort that switches to heapsort before its worst case can land.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(log n) |
| Stable | no |
| Family | hybrid |

## The idea

David Musser's answer to the one real objection to quicksort: the n² worst case,
which an adversary or an unlucky input can trigger.

Introsort counts recursion depth. Past 2·log₂(n) it stops trusting quicksort and
finishes that range with heapsort, which is n log n whatever happens. Short ranges
are left alone and swept up by a single insertion sort pass at the end.

Average case: quicksort's. Worst case: heapsort's. Small inputs: insertion sort's.
This is what `std::sort` does in C++.

## How it runs

1. Quicksort with a median-of-three pivot, recursing into the smaller side.
2. Stop recursing on ranges of 16 or fewer.
3. If the depth limit is reached, heapsort that range instead.
4. One insertion sort pass over the whole array at the end.

## When it is the right choice

The default unstable sort in systems code. It is the answer to 'quicksort is fast but I cannot accept its worst case'.
