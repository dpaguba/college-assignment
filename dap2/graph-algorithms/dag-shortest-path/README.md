# Shortest paths in a DAG

Relax the edges in topological order, once each.

| | |
|---|---|
| Time | O(V + E) |
| Memory | O(V) |
| Needs | no cycles, any weights |
| Answers | cheapest or most expensive path from one source |

## The idea

Dijkstra costs E + V log V and refuses negative edges. Bellman-Ford accepts them
and costs V·E. On a graph without cycles both are unnecessary.

Sort the vertices topologically and relax each vertex's outgoing edges once, in
that order. When a vertex is reached, every path into it has already been
considered, because every such path comes from earlier in the order. One pass,
linear time, and the sign of the weights never enters the argument.

Turning the comparison round gives the **longest** path, and that is worth pausing
on: longest path is NP-hard in general, because a cycle can be walked repeatedly.
Remove the cycles and it collapses to the same single pass.

## How it works

Topological sort first, which also detects the cycle that would make the whole thing meaningless, then one relaxation pass in that order.

## Where it is used

Critical path analysis in project scheduling, dependency resolution with costs, and dynamic programming over any acyclic state graph, which is most of it.
