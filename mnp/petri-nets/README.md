# Petri nets

| Topic | |
|---|---|
| [net-structure](net-structure/) | places, transitions, firing, conflict, concurrency |
| [reachability](reachability/) | the graph of everything the net can do |
| [properties](properties/) | liveness, boundedness, invariants |
| [workflow-nets](workflow-nets/) | soundness, and the fragments behind BPMN |

Petri nets make concurrency structural. Two transitions with no shared input
place are independent because of how they are connected, so a net says what
can happen at the same time without anyone writing that down separately.

The block's two answers about the dining philosophers show what that buys.
Three philosophers modelled as a net give 14 reachable markings with exactly
one deadlock, and the deadlock is named: every philosopher holding a left
fork. The interleaving search in
[concurrency-problems](../concurrency-problems/) reports that a deadlock
exists. The net reports which state it is.

The other lesson is that the graph is not always needed. A place invariant is
one linear equation that holds in every reachable marking, computed from the
incidence matrix without enumerating anything, and for the sheet net it proves
safety in a line.
