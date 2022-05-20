# A net as a triple

Places, transitions, and a flow relation that may only run from a place to a
transition or back. An edge between two places or two transitions does not
exist, which is what makes the graph bipartite; `net` refuses one.

## What the triple leaves out

The structure and nothing else. It says nothing about the marking, about edge
weights or about place capacities. Two nets with the same triple and
different initial markings behave completely differently, which is why the
triple is where sheet 10 starts and not where it ends.
