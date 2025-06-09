# Datenstrukturen und Algorithmen 2

The largest subject in the collection: 100 modules in seven blocks, plain
Python, no dependencies. One folder per algorithm or structure, each with an
implementation and a README explaining the idea, what it costs, and when it is
the right choice.

| Block | Modules | What it holds |
|---|---:|---|
| [sorting-algorithms](sorting-algorithms/) | 34 | from bubble sort to timsort, introsort, spreadsort and pattern-defeating quicksort |
| [graph-algorithms](graph-algorithms/) | 14 | traversal, shortest paths, spanning trees, connectivity, union-find |
| [data-structures](data-structures/) | 13 | the arrangements: heaps, balanced trees, hash tables, tries, skip lists, van Emde Boas |
| [dynamic-programming](dynamic-programming/) | 13 | knapsack, edit distance, matrix chain, Held-Karp and the classics |
| [searching-algorithms](searching-algorithms/) | 10 | binary and its relatives, plus selection in linear time |
| [divide-and-conquer](divide-and-conquer/) | 9 | Karatsuba, Strassen, closest pair, convex hull, the master theorem |
| [greedy-algorithms](greedy-algorithms/) | 5 | scheduling, partitioning, Huffman, fractional knapsack |

## Why the list runs past the lecture

The course stops at the lower bound proof for comparison sorting. Almost
everything a working sort does today happens on the other side of that bound,
which is why the sorting block holds thirty-four algorithms and not the five
that were taught. The same reasoning applies to the structures: sorting and
searching are algorithms over data that somebody else arranged, and most of
the cost in the other blocks follows from which arrangement was chosen.

The graph algorithms all take the same small `Graph` from
[graph-algorithms/graph.py](graph-algorithms/graph.py), an adjacency list with
optional weights and direction, so they can be compared on the same input.

## What each module README carries

The idea in a sentence, the cost, the stability where it applies, and the
input on which the algorithm is the right choice. The last of those is what
the pages are written around: timsort's is about input that arrives in runs
already ordered, and Dijkstra's says plainly that on negative weights a wrong
answer is worse than a refusal, which is what Bellman-Ford is for.
