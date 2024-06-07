"""Transitives Hülle eines gerichteten Graphen."""


def reachable(graph):
    """Berechnet die Erreichbarkeit durch eine Suche von jedem Knoten aus.

    Args:
        graph: Abbildung von Knoten auf ihre Nachfolger.

    Returns:
        Abbildung von Knoten auf die sortierte Liste der von dort aus
        erreichbaren Knoten, den Startknoten selbst nur bei einem Kreis.
    """
    result = {}
    for start in graph:
        seen = set()
        queue = list(graph[start])
        while queue:
            node = queue.pop()
            if node in seen:
                continue
            seen.add(node)
            queue.extend(graph.get(node, []))
        result[start] = sorted(seen)
    return result


def warshall(matrix):
    """Berechnet die transitive Hülle einer Adjazenzmatrix nach Warshall.

    Der Algorithmus lässt jeden Knoten einmal als Zwischenstation zu und
    ist in der Knotenzahl kubisch.

    Raises:
        ValueError: wenn die Matrix nicht quadratisch ist.
    """
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("Matrix ist nicht quadratisch")
    closure = [list(row) for row in matrix]
    for middle in range(size):
        for start in range(size):
            if not closure[start][middle]:
                continue
            for end in range(size):
                if closure[middle][end]:
                    closure[start][end] = 1
    return closure


def methods_agree(graph):
    """Vergleicht die Suche mit dem Verfahren von Warshall.

    Returns:
        Wahr, wenn beide Wege dieselbe Hülle liefern.
    """
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "graph-basics"))
    import graph_basics

    nodes = sorted(graph)
    position = {node: index for index, node in enumerate(nodes)}
    closure = warshall(graph_basics.adjacency_matrix(graph))
    by_search = reachable(graph)
    for node in nodes:
        row = {nodes[index] for index in range(len(nodes))
               if closure[position[node]][index]}
        if row != set(by_search[node]):
            return False
    return True


def agrees_with_networkx():
    """Vergleicht die Hülle mit der von networkx auf dem Übungsgraphen."""
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "graph-basics"))
    import graph_basics
    import networkx

    graph = graph_basics.exercise_digraph()
    other = networkx.transitive_closure(
        networkx.DiGraph(graph_basics.EXERCISE_EDGES))
    mine = reachable(graph)
    for node in graph:
        if sorted(other.successors(node)) != mine[node]:
            return False
    return True


def is_transitive(graph):
    """Sagt, ob ein Graph bereits transitiv ist."""
    for node, targets in graph.items():
        for target in targets:
            for far in graph.get(target, []):
                if far not in targets and far != node:
                    return False
    return True


def transitive_reduction(graph):
    """Entfernt jede Kante, die schon über einen Umweg erreichbar ist.

    Raises:
        ValueError: wenn der Graph nicht kreisfrei ist, weil die Reduktion
            dann nicht eindeutig ist.
    """
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "graph-basics"))
    import graph_basics

    if not graph_basics.is_acyclic(graph):
        raise ValueError("Reduktion nur fuer kreisfreie Graphen")
    closure = reachable(graph)
    reduced = {node: [] for node in graph}
    for node, targets in graph.items():
        for target in targets:
            detour = any(target in closure[other]
                         for other in targets if other != target)
            if not detour:
                reduced[node].append(target)
    return reduced
