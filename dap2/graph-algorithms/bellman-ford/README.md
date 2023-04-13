# Bellman-Ford

Relax every edge, V-1 times, and the answers settle.

| | |
|---|---|
| Time | O(V·E) |
| Memory | O(V) |
| Needs | nothing, and it detects negative cycles |
| Answers | cheapest path from one source |

## The idea

Dijkstra commits to a vertex as soon as it comes off the queue, which is only sound
when edges cannot lower a cost later. Bellman-Ford commits to nothing: it relaxes
every edge, over and over, until nothing improves.

The bound is V-1 rounds, and the reason is simple. A shortest path without negative
cycles visits at most V vertices, so it uses at most V-1 edges, and each round
extends every known path by one more edge.

That gives the negative cycle test for free. If a V-th round still improves
something, some path uses more than V-1 edges, which can only pay off by going
round a loop that reduces cost, and then no shortest path exists at all.

## How it works

V-1 sweeps over the edge list, then one more sweep as the check. The
implementation stops early when a sweep changes nothing, which on most graphs is
long before V-1.

The negative cycle check is raised as an exception rather than returned as a flag:
the distances are meaningless when one exists, so handing them back would invite
their use.

## Where it is used

Distance-vector routing (RIP), and currency arbitrage detection, where the negative cycle is not an error condition but the thing being looked for.
