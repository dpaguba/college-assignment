# CCS

Milner's calculus of communicating systems, as lectures 5 to 8 present it.

| Module | Topic |
|---|---|
| [ccs-syntax](ccs-syntax/) | the six operators and the structural laws |
| [ccs-semantics](ccs-semantics/) | the transition rules and the τ-chains of sheet 4 |
| [transition-graph](transition-graph/) | reachable states and the language |
| [bisimulation](bisimulation/) | when two processes are the same process |
| [buffer-and-stack](buffer-and-stack/) | sheet 5, and why states have to carry the data |

The engine is written once and repeated in the four modules that need it, so
each folder runs on its own. It is about forty lines: the transition rules
are short, and everything else in this block is a walk over the graph they
generate.
