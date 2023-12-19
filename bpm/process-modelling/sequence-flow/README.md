# Sequence flow

The control flow read as a graph, and the four things that can be checked
without any semantics at all:

- exactly one start event;
- at least one end event;
- every node reachable from the start;
- an end reachable from every node.

The last two are the weak precursors of soundness. They catch forgotten
edges and orphan nodes, which is most of what goes wrong in a hand-drawn
model, and they are cheap: two graph walks, one forward and one backward.

## What they do not catch

Reachability sees the graph, not the tokens. A model where a parallel split
meets an exclusive join passes every check in this module and still stops
dead when it runs. That needs the token game, which is the next module.

A flow to a node that does not exist raises rather than being reported: it
is not a modelling mistake but a broken file, and continuing with it would
produce nonsense downstream.
