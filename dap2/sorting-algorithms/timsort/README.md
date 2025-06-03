# Timsort

Find the stretches that are already sorted, then merge them under a balance rule.

| | |
|---|---|
| Best | O(n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(n) |
| Stable | yes |
| Family | hybrid |

## The idea

Tim Peters's sort, built on Peter McIlroy's observation that real data is not
random. It arrives in stretches that are already ascending or descending: sorted
chunks concatenated, a file with a few new records appended, a list sorted by
another field.

Timsort finds those runs, reverses the descending ones, extends short runs to a
minimum length with binary insertion sort, and then merges them. The merges follow
a stack invariant that keeps run lengths in balance, so no merge ever faces one
enormous run against a tiny one.

Sorted input costs a single pass. That is why it is the default in Python, Java 7
and later, Android and Swift.

## How it runs

1. Compute minrun, around 32 to 64, chosen so the number of runs is near a power of
   two and the merge tree stays balanced.
2. Scan for the next run; reverse it if it descends; extend it to minrun with binary
   insertion sort if it is short.
3. Push it on a stack of pending runs and merge while the invariants are violated.
4. Merge whatever remains on the stack.

## When it is the right choice

The general-purpose sort for anything with real-world structure, which is nearly everything. If stability is needed too, there is no better default.
