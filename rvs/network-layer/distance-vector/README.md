# The distance vector algorithm

Each router knows its neighbours and what they claim, and computes

    D(x, y) = min over neighbours v of ( c(x,v) + D(v, y) )

which is Bellman's equation solved by gossip. It converges to the shortest
paths, verified here against Dijkstra on the exercise's own five-node network:
every entry of every router's table agrees.

The final table reproduces the published one, including `D(A,E) = 10` via B and
`D(B,E) = 6` via C.

## Count to infinity

When a link gets worse, a router can hear its own stale distance back from a
neighbour and believe it, so the reported distance creeps up in small steps.
The exercise's tables show exactly that after the D-B link changes: the
distances rise by two per round over several rounds instead of jumping.

The problem is not slow convergence, it is **wrong** intermediate answers: a
router believes a route that does not exist, and forwards packets into a loop
while it does.

## The partial fixes

**Split horizon** does not advertise a route back to the neighbour it was
learned from, which removes the two-router loop. **Poisoned reverse**
advertises infinity instead of staying silent, so the neighbour acts at once
rather than waiting for a timeout.

Neither fixes a loop of three or more routers. That is why RIP caps the metric
at 16 and calls it infinity, bounding the damage rather than preventing it, and
why link state protocols exist.
