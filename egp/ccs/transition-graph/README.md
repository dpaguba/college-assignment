# Transition graph and language

The nodes are the reachable processes, the edges the transitions. Simplifying
after each step matters more than it looks: without `P | 0 ≡ P` the same
state appears under several spellings and the graph never closes.

The two processes of exercise 6a: the finite one has six states, the
recursive one `P = a.b.P + c.(d.P + e.P)` has three, because the recursion
returns to the same term rather than growing it.

## The language is coarser than the graph

The language is the set of action sequences a process can perform. Two
processes with the same language can behave differently, and that gap is the
entire reason bisimulation exists. The module computes the language up to a
depth so the two can be compared side by side.

## An infinite graph

Exercise 6c asks for a process whose graph has infinitely many nodes.
`P = a.(P | b.0)` puts another `b.0` beside itself at every step, so the term
grows without bound and no two states coincide. The module enumerates it up
to a limit and reports the growth rather than pretending to finish.
