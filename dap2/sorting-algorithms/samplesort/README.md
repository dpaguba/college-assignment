# Samplesort

Quicksort with many pivots at once, so every bucket can go to a different machine.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n²) |
| Memory | O(n) |
| Stable | no |
| Family | parallel |

## The idea

Quicksort splits into two parts, which is exactly wrong when sixteen processors are
waiting. Samplesort takes a random sample, sorts it, picks k-1 pivots out of it, and
splits the input into k buckets at once.

The buckets are independent and already in relative order, so each machine sorts one
and the results are concatenated with no merge step at all. That is why it is the
standard sort for clusters, MPI and GPUs.

Everything rests on the sample. Oversampling, taking several candidates per pivot
and picking the median of each group, is what keeps the buckets roughly equal; with
a bad sample one bucket swallows the input and the parallelism evaporates.

## How it runs

1. Sample about 3k elements at random and sort the sample.
2. Take k-1 evenly spaced values from it as pivots.
3. Bucket every element by binary search over the pivots.
4. Sort the buckets independently and concatenate.

## When it is the right choice

Distributed and parallel sorting. It is also the shape of the shuffle step in MapReduce.
