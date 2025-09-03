"""Register allocation by graph colouring.

Two variables may share a register exactly when they are never live at the same
time. Build a graph with an edge for every pair that is, and a colouring with
`k` colours is an allocation to `k` registers.

Graph colouring is NP-complete, so the standard algorithm is a heuristic:
repeatedly remove a node with fewer than `k` neighbours, since it can always be
coloured once the rest are, and colour the nodes back in reverse order. When no
such node exists, one is chosen to spill to memory, and the search continues.
"""

from __future__ import annotations

SPILL = "spill"
"""The marker for a variable that did not get a register."""


def interference(live_sets):
    """The interference graph as adjacency lists, isolated nodes included.

    Two variables interfere when some program point has both of them live.
    Nothing else is needed: the graph does not care what the instructions do,
    only when values are needed, which is why liveness analysis and register
    allocation are always adjacent in a compiler.

    Variables that never interfere with anything still have to appear, or the
    allocator silently gives them nothing.
    """
    graph = {}
    for live in live_sets:
        names = sorted(live)
        for name in names:
            graph.setdefault(name, set())
        for index, first in enumerate(names):
            for second in names[index + 1:]:
                graph[first].add(second)
                graph[second].add(first)
    return graph


def edges(graph):
    """The interference graph as unordered pairs."""
    return {(first, second) for first, adjacent in graph.items()
            for second in adjacent if first < second}


def allocate(graph, registers):
    """Assign registers by simplify, optimistic spill, and colour in reverse.

    The simplify step removes any node of degree less than `k`, since such a
    node can always be coloured after its neighbours, whatever they get. When
    every remaining node has degree `k` or more, one is pushed anyway and only
    marked as a **potential** spill.

    That last word is Briggs' optimistic colouring, and it is not a detail. A
    four-cycle with two registers has no node of degree below two, so the
    pessimistic version spills immediately, while the graph is plainly
    two-colourable: opposite corners share a colour. Trying the colour first
    and spilling only when none is free gets it right.

    Which node to push when none is simple matters too. A real allocator
    chooses by a cost estimate weighted by loop depth, since spilling inside a
    loop is far more expensive than outside one.
    """
    working = {name: set(adjacent) for name, adjacent in graph.items()}
    stack = []

    while working:
        simple = [name for name, adjacent in working.items() if len(adjacent) < registers]

        if simple:
            name = min(simple)
        else:
            name = max(working, key=lambda candidate: (len(working[candidate]), candidate))

        stack.append(name)
        for other in working[name]:
            working[other].discard(name)
        del working[name]

    assignment = {}
    for name in reversed(stack):
        taken = {assignment.get(other) for other in graph[name]}
        for colour in range(registers):
            if colour not in taken:
                assignment[name] = colour
                break
        else:
            assignment[name] = SPILL

    return assignment


def chromatic_lower_bound(graph):
    """The size of the largest clique found greedily, a lower bound on colours.

    Useful as a sanity check on an allocation: a graph containing a clique of
    size `n` cannot be coloured with fewer than `n` registers, so a spill there
    is unavoidable rather than a weakness of the heuristic.
    """
    best = 0

    for start in sorted(graph):
        clique = {start}
        for candidate in sorted(graph[start]):
            if all(candidate in graph[member] for member in clique):
                clique.add(candidate)
        best = max(best, len(clique))

    return best


def is_valid(assignment, graph):
    """Whether no two interfering variables share a register."""
    for first, second in edges(graph):
        if assignment[first] == SPILL or assignment[second] == SPILL:
            continue
        if assignment[first] == assignment[second]:
            return False
    return True


def registers_needed(graph):
    """The smallest number of registers this heuristic manages without spilling."""
    for count in range(1, len(graph) + 1):
        if SPILL not in allocate(graph, count).values():
            return count
    return len(graph)
