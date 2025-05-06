# Heapsort

Selection sort with a heap, so finding the maximum costs log n instead of n.

| | |
|---|---|
| Best | O(n log n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(1) |
| Stable | no |
| Family | selection |

## The idea

Selection sort spends a linear scan to find each next element. A binary max-heap
answers the same question in log n. That single substitution turns n² into n log n,
and it is the cleanest example of a data structure changing the complexity of an
algorithm without changing its shape.

The heap lives inside the same array: positions 0..k-1 are the heap, positions
k..n-1 are the sorted tail. Nothing is allocated, which is why heapsort is the
guaranteed-n-log-n sort that also uses O(1) memory.

## How it runs

1. Build a max-heap over the whole array, bottom up. This costs O(n), not
   O(n log n): most nodes are leaves and sift down no distance.
2. Swap the root, the largest element, with the last heap position.
3. Shrink the heap by one and sift the new root down.
4. Repeat until the heap holds one element.

## When it is the right choice

When the worst case must be bounded: real-time systems, and as the fallback inside
introsort. In ordinary use quicksort beats it, because heapsort jumps around the
array and misses the cache on nearly every sift.
