# Serialisability

Two operations conflict when they touch the same item, belong to different
transactions and at least one of them writes. The conflict graph has an edge
for every such pair in schedule order, and a schedule is conflict
serialisable exactly when that graph is acyclic.

The lost update is the standard example: both transactions read `a`, then
both write it. Each read precedes the other's write, so the graph has edges
in both directions and the schedule is rejected. Two reads never produce an
edge, and a schedule of reads alone has an empty graph.

`serial_order` returns the equivalent serial execution as a topological sort,
and raises when the graph has a cycle, since then no such execution exists.

## Conflict against view

Conflict serialisability is the stricter of the two conditions and can be
decided in polynomial time. View serialisability accepts more schedules and
deciding it is NP-complete, which is why systems check the first one.
