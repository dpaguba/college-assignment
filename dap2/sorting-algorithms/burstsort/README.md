# Burstsort

A trie whose leaves are flat buckets that burst into nodes when they fill.

| | |
|---|---|
| Best | O(n·k/d) |
| Average | O(n·k/d) |
| Worst | O(n·k/d) |
| Memory | O(n·k/d) |
| Stable | no |
| Family | non-comparison, strings |

## The idea

The n log n lower bound is a statement about comparison sorts: any algorithm that
learns about the data only by asking "is a < b" needs at least log₂(n!) questions.
Every sort in this family sidesteps the bound by looking at the key itself instead
of comparing keys, so the proof simply does not apply to them.

Sinha and Zobel's string sort, and one of the clearest cases of an algorithm
designed for the memory hierarchy rather than for the operation count.

MSD radix sort on strings creates a trie node per distinct prefix, and walking those
nodes misses the cache almost every step. Burstsort keeps strings in flat buckets and
only converts a bucket into a trie node when it grows past a threshold. The tree
stays shallow, strings sharing a prefix stay adjacent in memory, and the comparison
count barely changes while the cache misses collapse.

## How it runs

1. Insert each string by following the trie one character at a time.
2. When a bucket exceeds the threshold, burst it: make it a node and redistribute
   its strings one level deeper.
3. Traverse in order, sorting each small bucket by comparison as you reach it.

## When it is the right choice

Sorting large collections of strings in memory: dictionaries, log lines, identifiers.
