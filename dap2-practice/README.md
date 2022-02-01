# DAP2 practicals

Every programming task from the DAP2 practical, in Java, solved and verified.
One folder per task, each holding the source, the sample input where the task
uses one, and a README with the idea, the cost, and how the result was checked.

Java only, no build file and no dependencies. Compile a folder with `javac
*.java` and run it in place; assertions are part of several tasks, so run with
`java -ea`. Four tasks build on an earlier one and need a source path, which
their README spells out.

## The tasks

| Sheet | Task | Folder | Run it |
|---|---|---|---|
| 1.1 | command line parameters | [euclid](euclid/) | `java Euclid 264 846` |
| 1.2 | arrays | [sieve-of-eratosthenes](sieve-of-eratosthenes/) | `java Eratosthenes 100 -o` |
| 2.1 | random numbers, insertion sort | [insertion-sort](insertion-sort/) | `java InsertionSort 10 ab` |
| 2.2 | divide and conquer, merge sort | [merge-sort](merge-sort/) | `java Sortierung 6 merge ab` |
| 2.3 | running time measurement | [merge-sort](merge-sort/) | `java Laufzeitmessung` |
| 3.1 | quicksort | [quicksort](quicksort/) | `java QuickSort 5 3 9 1` |
| 3.2 | exponential and ternary search | [exponential-and-ternary-search](exponential-and-ternary-search/) | `java Search 1337` |
| 4.1 | points and lines | [points-and-lines](points-and-lines/) | `java Application 5 678` |
| 4.2 | convex hull | [convex-hull](convex-hull/) | `java SimpleConvexHull 5 678` |
| 5.1 | coin change | [coin-change](coin-change/) | `java CoinChange Mira 432` |
| 5.2 | shortest common superstring | [shortest-common-superstring](shortest-common-superstring/) | `java ShortestCommonSuperstring AEIOU AAE IIAU UUAI` |
| 6.1 | interval scheduling | [interval-scheduling](interval-scheduling/) | `java IntervalSchedulingDemo` |
| 6.2 | maximum subproduct | [maximum-subproduct](maximum-subproduct/) | `java MaxProdDemo` |
| 7.1 | longest common subsequence | [longest-common-subsequence](longest-common-subsequence/) | `java LongestCommonSubsequence ABACABC BACCABBC` |
| 7.2 | time measurement | [longest-common-subsequence](longest-common-subsequence/) | `java Zeitmessung` |
| 8.1 | traversing binary trees | [binary-tree-traversal](binary-tree-traversal/) | `java SearchTreeApplication < sample1.csv` |
| 8.2 | AVL trees | [avl-tree](avl-tree/) | `java AVLTreeApplication < sample2.csv` |
| 9.1 | bit vector structures | [bit-vector](bit-vector/) | `java Example` |
| 10.1 | own graph class | [graph-class](graph-class/) | `java GraphDemo` |
| 10.2 | Dijkstra | [dijkstra](dijkstra/) | `java DijkstraApplication < BspGraphKlein0-4.graph` |
| 11.1 | union-find, Kruskal, Prim | [prim-and-kruskal](prim-and-kruskal/) | `java Prim < BspGraphKlein.graph` |
| 12.1 | Bellman-Ford | [bellman-ford](bellman-ford/) | `java ShortestPaths bf < positiv.graph` |
| 12.2 | Floyd-Warshall | [floyd-warshall](floyd-warshall/) | `java ShortestPaths fw < positiv.graph` |

Two more folders are not from these sheets:
[binary-calculator](binary-calculator/) and [binary-tree](binary-tree/), which
were written outside the practical and are kept because they were worth
finishing.

## How the answers were checked

The sheets are unusually good test oracles: most of them print the exact output
they expect, down to the seed of the random generator. Wherever they do, the
programs here reproduce it character for character. That includes the ones that
are easy to get subtly wrong:

- quicksort's partition counts of 8, 12 and 668, which only come out if the
  generator is seeded once with 1337 and the left half is recursed into first
- the whole four-line ternary search trace for x = 1337
- the generated points for seed 678, and the order in which the convex hull
  discovers its edges
- the reconstructed subsequences `BACABC` and `EoCAXY`, not only their length
- the full AVL trace, every rotation named and every subtree height
- all 45 lines of the bit vector example
- Prim's spanning tree of weight 17, printed edge for edge

Where a sheet gives no expected output, the answer was checked against an
independent one: interval scheduling against brute force over all subsets, the
maximum subproduct against every range, Dijkstra against Floyd-Warshall on 500
random graphs, Prim and Kruskal against a brute force over all spanning trees
on 400 graphs, Bellman-Ford against Floyd-Warshall on 800 graphs with negative
weights.

Two results differ from the sheet on purpose, and both are documented where
they occur: the [superstring](shortest-common-superstring/) for eleven random
strings has the same length as the sheet's but a different letter order,
because the sheet fixes no tie-breaking rule; and the tree
[height](binary-tree-traversal/) counts nodes rather than edges, because the
sheet's own expected outputs are one larger than its hint says.

## What was missing from the archive

The course template archives (`VorlagenBlatt08.zip`, `VorlagenBlatt10.zip`,
`VorgabenBlatt11.zip`, `ShortestPaths.java`) were not in the material that
survived. The classes they contained are reimplemented from the interfaces the
sheets describe, and the sample input files were reconstructed from the
expected outputs: the CSV files by rebuilding each tree from two of its
traversals, the graph files by building a graph whose shortest path or spanning
tree is the one printed on the sheet. Every reconstruction reproduces the
sheet's output, which is what says it was right.

## Where the theory lives

These are the applied versions of topics covered on their own in
[dap2](../dap2/): the [sorting](../dap2/sorting-algorithms/) and
[searching](../dap2/searching-algorithms/) libraries, the
[data structures](../dap2/data-structures/),
[graph algorithms](../dap2/graph-algorithms/),
[dynamic programming](../dap2/dynamic-programming/),
[divide and conquer](../dap2/divide-and-conquer/) and
[greedy algorithms](../dap2/greedy-algorithms/) folders.
