# Layered drawing

Sugiyama's algorithm in four steps: remove the cycles, assign the layers,
reduce the crossings, place the horizontal coordinates.

Step one turns edges around until nothing points backwards. Step two gives
each vertex the length of the longest path from a source, so every edge goes
strictly downwards. On 40 random digraphs the result is acyclic and no edge
points upwards after layering.

An edge that spans several layers is split by dummy vertices, one per layer
crossed, so the crossing count only ever has to look at neighbouring layers.

## Crossings

Two edges between the same pair of layers cross exactly when their endpoints
appear in opposite order. The counting is checked against a geometric
computation, drawing the edges as segments between two horizontal lines and
intersecting them, on 30 random configurations.

The barycentre heuristic sorts the lower layer by the mean position of each
vertex's neighbours above. It reduces the crossings, and it is not optimal:
on the four-by-four case in `compared_with_the_optimum` it is compared with
the true minimum found by trying all orderings.
