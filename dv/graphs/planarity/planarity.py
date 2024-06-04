"""Planarität: die Schranke aus der Eulerschen Formel und die Sperrgraphen."""

import itertools


def edge_bound(vertices):
    """Obere Schranke der Kantenzahl eines planaren Graphen.

    Aus der Eulerschen Formel v − e + f = 2 und der Tatsache, dass jede
    Fläche von mindestens drei Kanten berandet wird, folgt e ≤ 3v − 6 für
    v ≥ 3; für kleinere Graphen ist die vollständige Kantenzahl die
    Schranke.

    Raises:
        ValueError: bei einer negativen Knotenzahl.
    """
    if vertices < 0:
        raise ValueError("Knotenzahl ist negativ")
    if vertices < 3:
        return vertices * (vertices - 1) // 2
    return 3 * vertices - 6


def _undirected_edges(graph):
    """Sammelt die Kanten als ungeordnete Paare ohne Wiederholung."""
    edges = set()
    for node, targets in graph.items():
        for target in targets:
            if node != target:
                edges.add(tuple(sorted((node, target), key=repr)))
    return edges


def satisfies_edge_bound(graph):
    """Prüft die notwendige Bedingung aus der Eulerschen Formel.

    Ein Graph, der sie verletzt, ist sicher nicht planar. Ein Graph, der
    sie erfüllt, kann trotzdem nicht planar sein.
    """
    return len(_undirected_edges(graph)) <= edge_bound(len(graph))


def contains_subdivision(graph, pattern_degrees):
    """Sucht eine Unterteilung eines der beiden Sperrgraphen.

    Gesucht werden Verzweigungsknoten mit den geforderten Graden, die
    paarweise durch knotendisjunkte Wege verbunden sind. Die Suche ist
    erschöpfend und nur für kleine Graphen gedacht.

    Args:
        graph: Abbildung von Knoten auf Nachbarn.
        pattern_degrees: ``5`` für K5, ``33`` für K3,3.

    Returns:
        Wahr, wenn eine Unterteilung gefunden wurde.

    Raises:
        ValueError: bei einem unbekannten Muster.
    """
    if pattern_degrees not in (5, 33):
        raise ValueError("unbekanntes Muster")
    nodes = sorted(graph, key=repr)
    if pattern_degrees == 5:
        needed = 5
        pairs = lambda chosen: list(itertools.combinations(chosen, 2))
    else:
        needed = 6
        pairs = None
    for chosen in itertools.combinations(nodes, needed):
        if pattern_degrees == 5:
            wanted = pairs(chosen)
            if _paths_exist(graph, chosen, wanted):
                return True
        else:
            for left in itertools.combinations(chosen, 3):
                right = [node for node in chosen if node not in left]
                wanted = [(a, b) for a in left for b in right]
                if _paths_exist(graph, chosen, wanted):
                    return True
    return False


def _paths_exist(graph, branch_nodes, wanted):
    """Prüft, ob alle geforderten Paare knotendisjunkt verbunden sind.

    Die Wege dürfen sich ausser in den Verzweigungsknoten nicht treffen;
    die Suche geht die Paare der Reihe nach durch und belegt die benutzten
    Zwischenknoten.
    """
    used = set()

    def search(index):
        """Sucht einen Weg für das Paar an der Stelle ``index``."""
        if index == len(wanted):
            return True
        start, end = wanted[index]
        for path in _simple_paths(graph, start, end, branch_nodes, used):
            inner = set(path[1:-1])
            used.update(inner)
            if search(index + 1):
                return True
            used.difference_update(inner)
        return False

    return search(0)


def _simple_paths(graph, start, end, branch_nodes, blocked, limit=6):
    """Zählt einfache Wege auf, deren innere Knoten frei sind."""
    stack = [(start, [start])]
    while stack:
        node, path = stack.pop()
        if node == end and len(path) > 1:
            yield path
            continue
        if len(path) > limit:
            continue
        for neighbour in sorted(graph.get(node, []), key=repr):
            if neighbour in path:
                continue
            if neighbour != end and neighbour in branch_nodes:
                continue
            if neighbour in blocked:
                continue
            stack.append((neighbour, path + [neighbour]))


def is_planar(graph):
    """Entscheidet die Planarität kleiner Graphen.

    Zuerst wird die Schranke geprüft; danach wird nach einer Unterteilung
    von K5 oder K3,3 gesucht. Nach dem Satz von Kuratowski ist ein Graph
    genau dann planar, wenn er keine solche Unterteilung enthält.
    """
    if not satisfies_edge_bound(graph):
        return False
    if contains_subdivision(graph, 5):
        return False
    if contains_subdivision(graph, 33):
        return False
    return True


def _to_undirected(graph):
    """Vergisst die Richtungen eines Digraphen."""
    result = {node: set() for node in graph}
    for node, targets in graph.items():
        for target in targets:
            result[node].add(target)
            result.setdefault(target, set()).add(node)
    return {node: sorted(targets, key=repr)
            for node, targets in result.items()}


def exercise_report():
    """Beantwortet die Planaritätsfrage für den Graphen der Aufgabe 2.2.

    Returns:
        Abbildung mit der eigenen Antwort, der von networkx, der
        Kantenzahl und der Schranke.
    """
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "graph-basics"))
    import graph_basics
    import networkx

    undirected = _to_undirected(graph_basics.exercise_digraph())
    other = networkx.Graph(graph_basics.EXERCISE_EDGES)
    return {"planar": is_planar(undirected),
            "networkx": networkx.check_planarity(other)[0],
            "edges": len(_undirected_edges(undirected)),
            "bound": edge_bound(len(undirected))}


def agrees_with_networkx():
    """Vergleicht die Entscheidung auf einer Reihe kleiner Graphen."""
    import networkx

    graphs = []
    graphs.append({node: [other for other in range(5) if other != node]
                   for node in range(5)})
    graphs.append({node: [other for other in range(4) if other != node]
                   for node in range(4)})
    k33 = {node: [other + 3 for other in range(3)] for node in range(3)}
    for node in range(3, 6):
        k33[node] = list(range(3))
    graphs.append(k33)
    graphs.append({0: [1], 1: [0, 2], 2: [1]})
    graphs.append({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    subdivided = {node: [other for other in range(5) if other != node]
                  for node in range(5)}
    subdivided[0].remove(1)
    subdivided[1].remove(0)
    subdivided[0].append(9)
    subdivided[1].append(9)
    subdivided[9] = [0, 1]
    graphs.append(subdivided)
    for graph in graphs:
        edges = [(node, target) for node, targets in graph.items()
                 for target in targets if node < target]
        other = networkx.Graph()
        other.add_nodes_from(graph)
        other.add_edges_from(edges)
        if is_planar(graph) != networkx.check_planarity(other)[0]:
            return False
    return True
