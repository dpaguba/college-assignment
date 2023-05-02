# Topological sort

An order where every edge points forwards.

| | |
|---|---|
| Time | O(V + E) |
| Memory | O(V) |
| Needs | a directed acyclic graph |
| Answers | a linear order respecting all dependencies |

## The idea

Two methods, both linear, and they detect the same impossibility differently.

**Kahn.** Count edges into each vertex. Anything at zero has no unmet prerequisite
and can go next; removing it lowers its neighbours' counts, which may free them in
turn. If the queue empties before every vertex is output, the remainder all have
incoming edges, which in a finite graph means they point at each other in a loop.
The cycle test is free.

**Depth-first.** A vertex finishes only after everything reachable from it has
finished, so the reverse of the finishing order is a topological order. That is the
whole proof, and it is why DFS finishing times keep turning up: they encode the
dependency structure without anyone counting anything. A grey vertex during the
search is the cycle.

## How it works

Kahn keeps a queue of ready vertices and in-degree counts. The DFS version collects finishing order and reverses it. Both raise rather than return a partial order when a cycle exists, because a partial order would look like an answer.

## Where it is used

Build systems (`make`, `cargo`, `npm`), package managers, spreadsheet recalculation, task schedulers, and the instruction scheduling inside a compiler. Every 'circular dependency detected' message is this check.
