"""Bridges and articulation points: the single edges and vertices holding a graph together."""

from __future__ import annotations

def _low_link(graph):
    """Entry times and low-link values from one depth-first pass.

    The low-link of a vertex is the earliest entry time reachable from its
    subtree, using tree edges downwards and at most one back edge. Both answers
    below are read straight off these two numbers.
    """
    entry: dict = {}
    low: dict = {}
    parent: dict = {}
    order: list = []
    clock = 0

    for root in graph.vertices:
        if root in entry:
            continue
        parent[root] = None
        entry[root] = low[root] = clock
        clock += 1
        order.append(root)
        stack = [(root, iter(graph.neighbours(root)))]

        while stack:
            vertex, neighbours = stack[-1]
            advanced = False
            for neighbour in neighbours:
                if neighbour not in entry:
                    parent[neighbour] = vertex
                    entry[neighbour] = low[neighbour] = clock
                    clock += 1
                    order.append(neighbour)
                    stack.append((neighbour, iter(graph.neighbours(neighbour))))
                    advanced = True
                    break
                if neighbour != parent[vertex]:
                    low[vertex] = min(low[vertex], entry[neighbour])
            if not advanced:
                stack.pop()
                if stack:
                    low[stack[-1][0]] = min(low[stack[-1][0]], low[vertex])

    return entry, low, parent, order

def bridges(graph):
    """Edges whose removal splits the graph into more components.

    An edge from parent to child is a bridge exactly when nothing in the
    child's subtree can reach the parent or higher by any other route. In
    low-link terms: `low[child] > entry[parent]`. If the child could escape
    upwards, that escape route would keep the graph connected without this
    edge.

    Real use: a bridge in a network is a single point of failure, and finding
    them is how redundancy is audited. In a road network they are the crossings
    with no detour."""
    entry, low, parent, _ = _low_link(graph)
    return [
        (parent[vertex], vertex)
        for vertex in low
        if parent.get(vertex) is not None and low[vertex] > entry[parent[vertex]]
    ]

def articulation_points(graph):
    """Vertices whose removal splits the graph into more components.

    Two rules, and the root needs its own. A non-root vertex is an articulation
    point when some child's subtree cannot escape above it,
    `low[child] >= entry[vertex]`. The root is one when it has more than one
    child in the search tree, because those subtrees only meet through it.

    The difference from bridges is the comparison: `>=` rather than `>`. A
    child that can reach exactly this vertex, but no higher, still leaves the
    graph connected if the edge is removed, and disconnects it if the vertex is.
    """
    entry, low, parent, order = _low_link(graph)
    children: dict = {}
    for vertex, its_parent in parent.items():
        if its_parent is not None:
            children.setdefault(its_parent, []).append(vertex)

    found = set()
    for vertex in order:
        if parent[vertex] is None:
            if len(children.get(vertex, [])) > 1:
                found.add(vertex)
            continue
        for child in children.get(vertex, []):
            if low[child] >= entry[vertex]:
                found.add(vertex)
                break

    return [vertex for vertex in order if vertex in found]
