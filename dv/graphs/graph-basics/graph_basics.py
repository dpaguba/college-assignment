"""Grundbegriffe der Graphentheorie an der Vorgabe der zweiten Übung."""

EXERCISE_EDGES = [(0, 1), (0, 4), (1, 2), (1, 3), (4, 6), (4, 11), (3, 11),
                  (4, 5), (5, 7), (2, 7), (8, 9), (7, 8), (3, 10), (6, 11),
                  (6, 13), (2, 11), (11, 14), (12, 14), (13, 14), (10, 12),
                  (13, 4), (9, 14)]


def exercise_digraph():
    """Liefert den Digraphen der Aufgabe 2.2 als Nachfolgerabbildung.

    Returns:
        Abbildung von 0 bis 14 auf die Liste der Nachfolger.
    """
    graph = {node: [] for node in range(15)}
    for source, target in EXERCISE_EDGES:
        graph[source].append(target)
    return graph


def order(graph):
    """Ordnung eines Graphen, die Zahl seiner Knoten."""
    return len(graph)


def size(graph):
    """Grösse eines Graphen, die Zahl seiner Kanten."""
    return sum(len(targets) for targets in graph.values())


def adjacency_matrix(graph):
    """Baut die Adjazenzmatrix in der Reihenfolge der sortierten Knoten."""
    nodes = sorted(graph)
    position = {node: index for index, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for node, targets in graph.items():
        for target in targets:
            matrix[position[node]][position[target]] = 1
    return matrix


def out_degree(graph, node):
    """Zahl der ausgehenden Kanten eines Knotens."""
    return len(graph[node])


def in_degree(graph, node):
    """Zahl der eingehenden Kanten eines Knotens."""
    return sum(1 for targets in graph.values() if node in targets)


def degree(graph, node):
    """Valenz eines Knotens in einem ungerichteten Graphen."""
    return len(graph[node])


def sources(graph):
    """Knoten ohne eingehende Kante."""
    return [node for node in sorted(graph) if in_degree(graph, node) == 0]


def sinks(graph):
    """Knoten ohne ausgehende Kante."""
    return [node for node in sorted(graph) if out_degree(graph, node) == 0]


def neighbours(graph, node):
    """Nachbarn eines Knotens, ein- und ausgehend zusammengefasst."""
    found = set(graph[node])
    for other, targets in graph.items():
        if node in targets:
            found.add(other)
    return sorted(found)


def find_cycle(graph):
    """Sucht einen gerichteten Kreis.

    Returns:
        Die Knoten des Kreises in Reihenfolge oder eine leere Liste.
    """
    path = []
    on_path = set()
    visited = set()

    def visit(node):
        """Verfolgt einen Pfad und meldet den Kreis, sobald er sich schliesst."""
        path.append(node)
        on_path.add(node)
        visited.add(node)
        for target in graph.get(node, []):
            if target in on_path:
                return path[path.index(target):]
            if target not in visited:
                found = visit(target)
                if found:
                    return found
        path.pop()
        on_path.discard(node)
        return []

    for node in sorted(graph):
        if node not in visited:
            found = visit(node)
            if found:
                return found
    return []


def is_acyclic(graph):
    """Sagt, ob ein gerichteter Graph kreisfrei ist."""
    return not find_cycle(graph)


def make_acyclic(graph=None):
    """Entfernt so lange eine Rückwärtskante, bis der Graph kreisfrei ist.

    Entfernt wird jeweils die letzte Kante des gefundenen Kreises, also
    die, die zum Ausgangspunkt zurückführt.

    Returns:
        Abbildung mit den entfernten Kanten, dem Ergebnis und der
        Bestätigung der Kreisfreiheit.
    """
    if graph is None:
        graph = exercise_digraph()
    working = {node: list(targets) for node, targets in graph.items()}
    removed = []
    while True:
        cycle = find_cycle(working)
        if not cycle:
            break
        source, target = cycle[-1], cycle[0]
        working[source].remove(target)
        removed.append((source, target))
    return {"removed": removed, "graph": working,
            "acyclic": is_acyclic(working)}


def topological_order(graph):
    """Ordnet die Knoten so, dass jede Kante nach vorn zeigt.

    Raises:
        ValueError: wenn der Graph einen Kreis enthält.
    """
    incoming = {node: in_degree(graph, node) for node in graph}
    ready = sorted(node for node in graph if incoming[node] == 0)
    order_of_nodes = []
    while ready:
        node = ready.pop(0)
        order_of_nodes.append(node)
        for target in graph[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
        ready.sort()
    if len(order_of_nodes) != len(graph):
        raise ValueError("Graph enthaelt einen Kreis")
    return order_of_nodes


def agrees_with_networkx():
    """Vergleicht Ordnung, Grösse, Quellen, Senken und Kreisfreiheit.

    Returns:
        Wahr, wenn networkx auf dem Übungsgraphen dasselbe sagt.
    """
    import networkx

    graph = exercise_digraph()
    other = networkx.DiGraph(EXERCISE_EDGES)
    if other.number_of_nodes() != order(graph):
        return False
    if other.number_of_edges() != size(graph):
        return False
    if sorted(node for node in other if other.in_degree(node) == 0) \
            != sources(graph):
        return False
    if sorted(node for node in other if other.out_degree(node) == 0) \
            != sinks(graph):
        return False
    return networkx.is_directed_acyclic_graph(other) == is_acyclic(graph)
