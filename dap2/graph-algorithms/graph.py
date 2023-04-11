"""The graph every algorithm in this folder takes.

One small adjacency structure, shared, so the algorithms differ in what they
do rather than in what they accept.
"""

from __future__ import annotations


class Graph:
    """An adjacency list with optional weights and direction.

    Adjacency list rather than matrix: a matrix costs V² memory and answers
    "is there an edge" in O(1), a list costs V + E and answers "what are the
    neighbours" in O(degree). Almost every algorithm here asks the second
    question, and almost every real graph is sparse, so the list wins twice.
    """

    def __init__(self, directed=False):
        """An empty graph, directed or not."""
        self.directed = directed
        self._adjacency: dict = {}

    def add_vertex(self, vertex):
        """Add a vertex with no edges.

        Adding one that already exists changes nothing.
        """
        self._adjacency.setdefault(vertex, {})
        return self

    def add_edge(self, source, target, weight=1):
        """Add an edge, and its mirror image when the graph is undirected.

        Missing endpoints are created.
        """
        self.add_vertex(source).add_vertex(target)
        self._adjacency[source][target] = weight
        if not self.directed:
            self._adjacency[target][source] = weight
        return self

    def neighbours(self, vertex):
        """Neighbours in insertion order, so traversals are reproducible."""
        return list(self._adjacency.get(vertex, {}))

    def weight(self, source, target):
        """Weight of the edge between two vertices."""
        return self._adjacency[source][target]

    def edges(self):
        """Every edge as a source, target, weight triple, each undirected edge once..
        """
        seen = set()
        for source, targets in self._adjacency.items():
            for target, weight in targets.items():
                if not self.directed:
                    pair = frozenset((source, target))
                    if pair in seen:
                        continue
                    seen.add(pair)
                yield source, target, weight

    def reversed(self):
        """The same graph with every edge turned around."""
        flipped = Graph(directed=self.directed)
        for vertex in self._adjacency:
            flipped.add_vertex(vertex)
        for source, target, weight in self.edges():
            flipped.add_edge(target, source, weight)
        return flipped

    @property
    def vertices(self):
        """Every vertex, in insertion order."""
        return list(self._adjacency)

    def __contains__(self, vertex):
        """Whether the key is stored."""
        return vertex in self._adjacency

    def __len__(self):
        """How many entries the structure holds."""
        return len(self._adjacency)
