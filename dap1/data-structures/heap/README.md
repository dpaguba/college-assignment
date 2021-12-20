# Heap and priority queue

Chapter nineteen. A complete binary tree stored in an array, where the
children of position i are at 2i+1 and 2i+2, so there is no node object and no
link anywhere.

The heap condition is local: a parent is at most its children. That locality
is what makes both operations logarithmic, because an insertion can only break
it along one path to the root and an extraction only along one path to a leaf.

## Building beats inserting

Exchanges needed to heapify 63 values in descending order:

| | exchanges |
|---|---:|
| sifting down from the last inner node | 57 |
| inserting one at a time | 258 |

Four and a half times fewer, and the gap grows with the size. The reason is
where the work sits: sifting down starts at the bottom, where almost all the
nodes are and where the paths are shortest, while inserting starts at the top,
where every value has to climb the full height. Half the nodes are leaves and
cost nothing at all in the first version.

That is the standard example of a bound that is easy to get wrong: n calls to
a log n operation looks like n log n, and building a heap is linear.

## Draining it sorts

Extracting until the queue is empty yields the values in order, which is
heapsort, verified on 100 random arrays against `Arrays.sort`. The heap
condition itself is checked directly after every build, since an algorithm
that produces sorted output from a broken heap is possible and the property
worth asserting is the invariant rather than the outcome.
