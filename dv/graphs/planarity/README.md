# Planarity

Euler's formula gives a necessary condition. With v ≥ 3 vertices a planar
graph has at most 3v − 6 edges, because every face is bounded by at least
three edges and every edge borders two faces. K5 has 10 edges against a bound
of 9 and is therefore not planar, decided by counting alone.

K3,3 has 9 edges against a bound of 12 and passes the count, yet is not
planar. The bound is necessary, not sufficient, and this is the graph that
shows it.

## Kuratowski

A graph is planar exactly when it contains no subdivision of K5 or K3,3. The
module searches for such a subdivision: it picks candidate branch vertices
and looks for vertex-disjoint paths between the required pairs. The search is
exhaustive and only usable on small graphs, which is what it is for.

The decision agrees with `networkx.check_planarity` on 40 random graphs and
on the deliberate cases: K5, K4, K3,3, a path, a triangle, and a K5 with one
edge subdivided by an extra vertex.

The exercise's digraph, read as undirected, is not planar: 22 edges against a
bound of 39, so counting decides nothing, and the Kuratowski search finds the
obstruction.
