# Reachability

The reachability graph contains everything a bounded net can do, so questions
that sound temporal become questions about a finite object.

The net from the exercise sheet, one token in P1:

| Markings | Edges | Deadlocks |
|---|---|---|
| 4 | 4 | 1, namely `{P4: 1}` |

The four markings are `{P1:1}`, `{P2:1}`, `{P3:1}`, `{P4:1}`, and `{P2:1,
P3:1}` is absent: the token goes one way or the other, never both. That
absence is the answer the sheet is asking for, and it is visible in the graph
without any argument about interleaving.

## Firing sequences

Asking how a marking is reached is a shortest-path question on the same graph.
`{P4: 1}` is reached by `T1 T2` or by `T3 T4`, both of length two, and
`{P1: 2}` has no sequence at all, since nothing in this net creates tokens.

## The cost

A producer-consumer net with capacity three has four markings. Raise the
capacity and the count rises with it; put k independent components together
and the counts multiply. The graph is exact and it grows fast, which is the
motivation for the invariants in [properties](../properties/): they answer
some of the same questions from the incidence matrix alone.
