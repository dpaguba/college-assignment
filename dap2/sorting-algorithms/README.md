# Sorting algorithms

Thirty-four sorting algorithms, one folder each, in plain Python with no
dependencies. Every folder holds the implementation and a README explaining
how that algorithm works, what it costs, and when it is the right choice.

The lecture stops at the lower bound proof for comparison sorting. Most of what
a working sort does today happens on the other side of it, which is why the
list runs well past the five that were taught.

## Comparison sorts

They learn about the data only by asking "is a smaller than b", which is what
puts them under the n log n lower bound.

### By exchange

| Algorithm | Average | Memory | Stable | |
|---|---|---|---|---|
| [bubble-sort](bubble-sort/) | O(n²) | O(1) | yes |  |
| [cocktail-shaker-sort](cocktail-shaker-sort/) | O(n²) | O(1) | yes | |
| [odd-even-sort](odd-even-sort/) | O(n²) | O(1) | yes | |
| [comb-sort](comb-sort/) | O(n²) | O(1) | no | |
| [quicksort](quicksort/) | O(n log n) | O(log n) | no |  |

### By selection

| Algorithm | Average | Memory | Stable | |
|---|---|---|---|---|
| [selection-sort](selection-sort/) | O(n²) | O(1) | no |  |
| [heapsort](heapsort/) | O(n log n) | O(1) | no |  |
| [cycle-sort](cycle-sort/) | O(n²) | O(1) | no | minimum writes |
| [tournament-sort](tournament-sort/) | O(n log n) | O(n) | yes | |
| [smoothsort](smoothsort/) | O(n log n) | O(1) | no | linear on sorted input |

### By insertion

| Algorithm | Average | Memory | Stable | |
|---|---|---|---|---|
| [insertion-sort](insertion-sort/) | O(n²) | O(1) | yes |  |
| [gnome-sort](gnome-sort/) | O(n²) | O(1) | yes | |
| [shellsort](shellsort/) | gap dependent | O(1) | no | |
| [tree-sort](tree-sort/) | O(n log n) | O(n) | yes | |
| [library-sort](library-sort/) | O(n log n) | O(n) | no | |
| [patience-sort](patience-sort/) | O(n log n) | O(n) | no | also computes the LIS |

### By merging

| Algorithm | Average | Memory | Stable | |
|---|---|---|---|---|
| [merge-sort](merge-sort/) | O(n log n) | O(n) | yes |  |
| [in-place-merge-sort](in-place-merge-sort/) | O(n log² n) | O(log n) | yes | |
| [strand-sort](strand-sort/) | O(n²) | O(n) | yes | |

## Non-comparison sorts

They read the key itself rather than comparing keys, so the n log n bound does
not apply to them at all.

| Algorithm | Average | Memory | Stable | |
|---|---|---|---|---|
| [counting-sort](counting-sort/) | O(n + r) | O(n + r) | yes | |
| [pigeonhole-sort](pigeonhole-sort/) | O(n + r) | O(r) | yes | |
| [bucket-sort](bucket-sort/) | O(n + k) | O(n + k) | yes | |
| [radix-sort-lsd](radix-sort-lsd/) | O(n·k/d) | O(n + 2^d) | yes | |
| [radix-sort-msd](radix-sort-msd/) | O(n·k/d) | O(n + 2^d) | yes | |
| [flashsort](flashsort/) | O(n + r) | O(m) | no | |
| [spreadsort](spreadsort/) | O(n·k/d) | O(k/d · 2^d) | no | radix or comparison, per piece |
| [burstsort](burstsort/) | O(n·k/d) | O(n·k/d) | no | strings |

## What real libraries ship

| Algorithm | Average | Memory | Stable | Used by |
|---|---|---|---|---|
| [timsort](timsort/) | O(n log n) | O(n) | yes | Python, Java, Android, Swift |
| [introsort](introsort/) | O(n log n) | O(log n) | no | C++ `std::sort` |
| [pattern-defeating-quicksort](pattern-defeating-quicksort/) | O(n log n) | O(log n) | no | Rust `sort_unstable` |
| [block-sort](block-sort/) | O(n log n) | O(1) in full form | yes | stable sorts under memory pressure |

## Parallel and sorting networks

The comparison schedule is fixed before the data is seen, which is what lets
hardware run a whole stage at once.

| Algorithm | Depth | Memory | Stable | |
|---|---|---|---|---|
| [bitonic-sort](bitonic-sort/) | O(log² n) | O(1) | no | the standard GPU sort |
| [odd-even-merge-sort](odd-even-merge-sort/) | O(log² n) | O(1) | no | fewer comparators |
| [samplesort](samplesort/) | O(n log n) | O(n) | no | clusters, MPI, MapReduce shuffles |

## Using them

Every algorithm exposes one function named after its folder, takes any
iterable, returns a new list and does not touch the input:

```python
from merge_sort import merge_sort

merge_sort([5, 2, 9, 1])                      # [1, 2, 5, 9]
merge_sort(people, key=lambda person: person.age)
```

The non-comparison sorts need integer keys, and `bucket-sort` and `flashsort`
need numeric ones. `burstsort` takes strings and has no `key` parameter.

## How this was built

Test first. Each algorithm got a test file before it had an implementation,
run to watch it fail for the right reason, then the code, then the run again.
A shared contract checked every algorithm against the same 37 inputs: empty,
single, all equal, already sorted, reversed, negatives, duplicates, and 25
random lists; stability was checked separately where it is claimed, and the
two sorting networks were verified exhaustively against every binary input of
width 4, 8 and 16, which by the zero-one principle proves they sort everything.

Three real defects surfaced that way: patience sort built its piles in the
wrong direction, block sort recursed forever when merging two single elements,
and sleep sort turned out to depend on a scheduler tick the machine does not
guarantee.

The tests were removed once all 103 of them passed, so what remains is the
library and the explanations.
