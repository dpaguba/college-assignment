# Floyd-Warshall

Every shortest path, from three nested loops.

| | |
|---|---|
| Time | O(V³) |
| Memory | O(V²) |
| Needs | no negative cycles |
| Answers | cheapest path between every pair |

## The idea

Running Dijkstra from every vertex costs V·(E + V log V). This costs V³ and is
usually faster on a dense graph, because there is nothing in it but array access:
no heap, no queue, no allocation.

The induction is beautifully small. Let D(k) hold the cheapest costs using only the
first k vertices as intermediates. Then D(k) is D(k-1) with one question asked per
pair: is it cheaper to go through vertex k? The answer needs only D(k-1), so the
whole thing is one array updated in place.

**The loop order is the algorithm.** The allowed intermediate must be the outer
loop. Putting it innermost gives a program that runs, produces plausible numbers,
and is wrong. It is the most common way to get this wrong.

## How it works

Initialise the table from the edges, then three loops with the intermediate
outermost. A negative value on the diagonal afterwards means a vertex reaches
itself at negative cost, which is a negative cycle.

Replacing addition with "and" and minimum with "or" turns the same loops into
reachability. That is Warshall's original 1962 algorithm, and the same shape as
matrix multiplication over a different semiring, which is why these three loops
keep reappearing in unrelated places.

## Where it is used

Dense graphs, all-pairs queries, transitive closure, and finding the diameter or centre of a network.
