"""Depth-first search: follow one branch to its end before trying the next."""

from __future__ import annotations

WHITE, GREY, BLACK = 0, 1, 2

def depth_first_search(graph, start):
    """Return the reachable vertices in the order DFS enters them.

    BFS and DFS differ by one data structure: a queue against a stack. That is
    the whole difference, and everything else follows from it. BFS spreads
    evenly and measures distance; DFS plunges and measures structure.

    What DFS gives that BFS cannot is the entry and exit times below. Those two
    numbers per vertex are the foundation of topological order, strongly
    connected components, bridges, articulation points and cycle detection, all
    of which read the shape of the search rather than its result.

    Written with an explicit stack. The recursive form is shorter and dies on a
    graph twenty thousand vertices deep, which is a chain, not an exotic case.

    Neighbours are pushed in reverse, so the first neighbour is the first one
    explored once they come back off the stack. That keeps the iterative walk
    in the same order as the recursive one.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    seen = set()
    order = []
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        order.append(vertex)
        for neighbour in reversed(graph.neighbours(vertex)):
            if neighbour not in seen:
                stack.append(neighbour)

    return order

def times(graph, start):
    """Entry and exit time per vertex, the numbers everything else is built on.

    A vertex is entered when the search first reaches it and left when every
    descendant is finished. The intervals nest: one vertex is an ancestor of
    another exactly when its interval contains the other's, which turns
    questions about tree shape into questions about numbers.
    """
    entered: dict = {}
    left: dict = {}
    clock = 0
    stack = [(start, iter(graph.neighbours(start)))]
    entered[start] = clock
    clock += 1

    while stack:
        vertex, neighbours = stack[-1]
        advanced = False
        for neighbour in neighbours:
            if neighbour not in entered:
                entered[neighbour] = clock
                clock += 1
                stack.append((neighbour, iter(graph.neighbours(neighbour))))
                advanced = True
                break
        if not advanced:
            left[vertex] = clock
            clock += 1
            stack.pop()

    return entered, left

def has_cycle(graph):
    """True when the graph contains a cycle.

    The three colours are the standard argument. White is unvisited, grey is on
    the current path, black is finished. Reaching a grey vertex means the path
    has looped back on itself, which is a cycle; reaching a black one only
    means the vertex was seen through some other branch.

    In an undirected graph the same walk would call every edge a cycle, since
    the way back to the parent is grey, so the parent is skipped explicitly.
    """
    colour = {vertex: WHITE for vertex in graph.vertices}

    for root in graph.vertices:
        if colour[root] != WHITE:
            continue
        stack = [(root, None, iter(graph.neighbours(root)))]
        colour[root] = GREY

        while stack:
            vertex, parent, neighbours = stack[-1]
            advanced = False
            for neighbour in neighbours:
                if not graph.directed and neighbour == parent:
                    continue
                if colour[neighbour] == GREY:
                    return True
                if colour[neighbour] == WHITE:
                    colour[neighbour] = GREY
                    stack.append((neighbour, vertex, iter(graph.neighbours(neighbour))))
                    advanced = True
                    break
            if not advanced:
                colour[vertex] = BLACK
                stack.pop()

    return False
