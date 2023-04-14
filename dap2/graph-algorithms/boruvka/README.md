# Borůvka's algorithm

Every component picks its cheapest edge, all at the same time.

| | |
|---|---|
| Time | O(E log V) |
| Memory | O(V) |
| Needs | undirected weighted graph, distinct tie-breaking |
| Answers | minimum spanning tree |

## The idea

The oldest of the three, from 1926, written to plan an electrical network in
Moravia, and the one that fits modern hardware best.

Kruskal and Prim each make one decision at a time. Borůvka has every component
choose its own cheapest outgoing edge simultaneously, then merges all of them at
once.

Because every component merges with at least one other, their number at least
halves each round, so O(log V) rounds suffice. The test checks that: 64 vertices
finish in no more than 7 rounds.

The rounds are what make it interesting today. Choices within a round are
independent, so it parallelises where the other two do not, and modern parallel and
GPU spanning tree algorithms are Borůvka.

## How it works

Repeat until one component remains: scan the edges, record each component's
cheapest outgoing edge, then merge them all.

**One detail is load bearing.** Ties must be broken consistently, or two components
can each pick a different edge of equal weight between them and the result contains
a cycle. Comparing on (weight, source, target) settles it.

## Where it is used

Parallel and distributed spanning tree computation, and as a component of the fastest known sequential MST algorithms, which interleave Borůvka rounds with other techniques.
