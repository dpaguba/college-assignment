# Pattern-defeating quicksort

Quicksort that notices the shape of its input and stops doing unnecessary work.

| | |
|---|---|
| Best | O(n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(log n) |
| Stable | no |
| Family | hybrid |

## The idea

Orson Peters's sort, behind Rust's `sort_unstable`. Introsort fixes the worst case
but still does full work on inputs that need almost none. pdqsort reads what the
partition tells it:

- a partition that moved nothing means the range may already be sorted, so it
  checks, and returns early if it is;
- a badly unbalanced partition means the pivot choice is being defeated, so it
  shuffles a few elements to break whatever pattern is doing it;
- too many bad partitions and it falls back, like introsort.

Sorted, reverse sorted, all-equal and organ-pipe inputs become linear or near
linear, while random input costs what quicksort costs.

## How it runs

1. Choose a pivot: median of three, or the ninther on large ranges.
2. Partition, and note whether anything moved and how balanced the split was.
3. React: check for sortedness, or break the pattern, or fall back.
4. Insertion sort the short ranges.

## When it is the right choice

A modern replacement for introsort wherever stability is not required.
