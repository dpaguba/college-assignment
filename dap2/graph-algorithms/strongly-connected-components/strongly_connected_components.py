"""Strongly connected components: the groups where everyone can reach everyone."""

from __future__ import annotations


def tarjan(graph):
    """Find the components in a single depth-first pass.

    A strongly connected component is a set of vertices where every one can
    reach every other. Contract each component to a point and the graph becomes
    acyclic, which is why this is the first step in almost any analysis of a
    directed graph.

    Tarjan's insight is the low-link number: for each vertex, the smallest entry
    time reachable from its subtree using at most one edge that goes backwards.
    When a vertex's low-link equals its own entry time, nothing under it escapes
    to an earlier vertex, so it is the root of a component, and everything above
    it on the stack belongs to that component.

    One pass, linear time, and the components come out in reverse topological
    order of the contracted graph, which callers often want anyway.

    Written iteratively: the recursive form is shorter and dies on any graph
    deeper than the interpreter's stack.
    """
    index_of: dict = {}
    low: dict = {}
    on_stack: dict = {}
    stack: list = []
    components: list = []
    counter = 0

    for root in graph.vertices:
        if root in index_of:
            continue

        work = [(root, iter(graph.neighbours(root)))]
        index_of[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack[root] = True

        while work:
            vertex, neighbours = work[-1]
            advanced = False
            for neighbour in neighbours:
                if neighbour not in index_of:
                    index_of[neighbour] = low[neighbour] = counter
                    counter += 1
                    stack.append(neighbour)
                    on_stack[neighbour] = True
                    work.append((neighbour, iter(graph.neighbours(neighbour))))
                    advanced = True
                    break
                if on_stack.get(neighbour):
                    low[vertex] = min(low[vertex], index_of[neighbour])
            if advanced:
                continue

            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[vertex])

            if low[vertex] == index_of[vertex]:
                component = []
                while True:
                    member = stack.pop()
                    on_stack[member] = False
                    component.append(member)
                    if member == vertex:
                        break
                components.append(component)

    return components


def kosaraju(graph):
    """Find the same components in two passes, with an argument you can hold.

    Run a depth-first search and record the finishing order. Reverse every edge.
    Run depth-first search again, taking roots in decreasing finishing time:
    each search now reaches exactly one component.

    Why it works: reversing the edges leaves the components unchanged, because
    mutual reachability is symmetric, but it cuts every route between them. The
    finishing order guarantees the second pass starts in a component that
    nothing else can reach in the reversed graph, so it cannot spill over.

    Twice the work of Tarjan and a fraction of the explanation, which is why
    this is the one that gets taught and Tarjan's is the one that gets used.
    """
    visited = set()
    finished = []

    for root in graph.vertices:
        if root in visited:
            continue
        stack = [(root, iter(graph.neighbours(root)))]
        visited.add(root)
        while stack:
            vertex, neighbours = stack[-1]
            advanced = False
            for neighbour in neighbours:
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append((neighbour, iter(graph.neighbours(neighbour))))
                    advanced = True
                    break
            if not advanced:
                finished.append(vertex)
                stack.pop()

    reversed_graph = graph.reversed()
    assigned = set()
    components = []

    for root in reversed(finished):
        if root in assigned:
            continue
        component = []
        stack = [root]
        assigned.add(root)
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbour in reversed_graph.neighbours(vertex):
                if neighbour not in assigned:
                    assigned.add(neighbour)
                    stack.append(neighbour)
        components.append(component)

    return components
