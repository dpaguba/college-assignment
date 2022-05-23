# Reachability

In a place/transition net a place holds any number of tokens, so a transition
fires when every place in its preset holds at least the required weight, and
there is no upper bound. `table` builds the reachability table of sheet 12,
one row per reachable marking and one column per transition, and the graph
follows from it.

The example has five reachable markings and is live: from every marking every
transition can fire again.

## Unbounded nets

A transition that consumes one token and produces two lets the token count
grow without limit. The reachability set is then infinite and the table
cannot be built. `unbounded_example` reports that rather than running,
because a function that quietly stops at an arbitrary limit would report a
finite state space for a net that has none.

That is the difference from the condition/event net, where a place holds at
most one token and the state space is bounded by construction.
