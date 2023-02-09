# Link state routing

Every router floods a description of its own links, so all of them build the
same map and run Dijkstra locally. The opposite trade from the distance vector
approach: more information per router and much faster convergence, because
nobody relies on anybody else's arithmetic.

There is no count to infinity, because no router believes a distance it did not
compute itself.

| | distance vector | link state |
|---|---|---|
| what is sent | distances, to neighbours | link states, to everyone |
| messages per change | `n(n-1)` | `2 * links` |
| convergence | can take many rounds | one flood plus a local computation |
| memory | one row | the whole topology |

## Forwarding tables store one hop

A router keeps the **next hop** towards each destination, not the path: the
next router repeats the decision. That is what makes forwarding a table lookup
per packet and routing a periodic computation, and it is why the two words are
not synonyms.

## Dijkstra needs non-negative costs

The greedy argument is that the nearest unvisited node cannot be reached more
cheaply through one that is further away, which fails if an edge can reduce the
distance. Routing metrics are always positive, so the question never arises in
practice, and it is the reason it never arises.
