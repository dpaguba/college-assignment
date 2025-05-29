# Smoothsort

Heapsort on Leonardo heaps, which costs almost nothing when the input is already sorted.

| | |
|---|---|
| Best | O(n) |
| Average | O(n log n) |
| Worst | O(n log n) |
| Memory | O(1) |
| Stable | no |
| Family | selection |

## The idea

Dijkstra's answer to heapsort's one weakness: it takes n log n even on input that
is already in order. Smoothsort keeps a forest of heaps whose sizes are Leonardo
numbers, L(k) = L(k-1) + L(k-2) + 1, and the shape of that forest follows the data.
On sorted input almost nothing ever sifts, and the run is linear.

It is the most fiddly algorithm in this folder by a wide margin, which is why it is
admired and almost never used. Timsort reaches the same goal, adaptivity to
existing order, with far simpler machinery.

## How it runs

1. Grow the forest one element at a time, merging two neighbouring heaps whenever
   their orders are consecutive.
2. After each insertion, trinkle: walk left across the roots and move the new
   element into the heap where it belongs.
3. To sort, dismantle the forest from the right, restoring the heap property as
   each root is exposed.

## When it is the right choice

Almost nowhere. Its value is as a proof that O(1) memory, guaranteed n log n and adaptivity to sorted input can coexist.
