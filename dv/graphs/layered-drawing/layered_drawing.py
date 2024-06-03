"""Schichtenweises Zeichnen gerichteter Graphen nach Sugiyama."""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "graph-basics"))

import graph_basics


def remove_cycles(graph):
    """Dreht so lange Kanten um, bis der Graph kreisfrei ist.

    Der erste Schritt des Verfahrens von Sugiyama; im Ergebnis zeigt jede
    Kante in dieselbe Richtung, was die Schichtzuordnung erst möglich
    macht.

    Returns:
        Ein kreisfreier Graph mit denselben Knoten.
    """
    working = {node: list(targets) for node, targets in graph.items()}
    while True:
        cycle = graph_basics.find_cycle(working)
        if not cycle:
            return working
        source, target = cycle[-1], cycle[0]
        working[source].remove(target)
        if source not in working[target]:
            working[target].append(source)
        if graph_basics.find_cycle(working):
            working[target].remove(source)


def assign_layers(graph):
    """Ordnet jedem Knoten die Länge des längsten Weges von einer Quelle zu.

    Damit liegt jede Kante zwischen benachbarten oder weiter entfernten
    Schichten, aber niemals innerhalb einer Schicht.

    Raises:
        ValueError: wenn der Graph einen Kreis enthält.
    """
    order = graph_basics.topological_order(graph)
    layers = {node: 0 for node in graph}
    for node in order:
        for target in graph[node]:
            layers[target] = max(layers[target], layers[node] + 1)
    return layers


def insert_dummies(graph, layers):
    """Ersetzt Kanten über mehrere Schichten durch Ketten von Hilfsknoten.

    Returns:
        Abbildung mit dem erweiterten Graphen, den Schichten und der Zahl
        der eingefügten Hilfsknoten.
    """
    extended = {node: list(targets) for node, targets in graph.items()}
    positions = dict(layers)
    added = 0
    for node in list(graph):
        for target in list(graph[node]):
            span = positions[target] - positions[node]
            if span <= 1:
                continue
            extended[node].remove(target)
            previous = node
            for step in range(1, span):
                name = ("dummy", node, target, step)
                extended[name] = []
                positions[name] = positions[node] + step
                extended[previous].append(name)
                previous = name
                added += 1
            extended[previous].append(target)
    return {"graph": extended, "layers": positions, "dummies": added}


def count_crossings(upper, lower, edges):
    """Zählt die Kreuzungen zwischen zwei Schichten.

    Zwei Kanten kreuzen sich, wenn ihre Endpunkte in beiden Schichten in
    entgegengesetzter Reihenfolge stehen.

    Args:
        upper: Reihenfolge der oberen Schicht.
        lower: Reihenfolge der unteren Schicht.
        edges: Paare (oberer Knoten, unterer Knoten).

    Returns:
        Zahl der sich kreuzenden Kantenpaare.
    """
    top = {node: index for index, node in enumerate(upper)}
    bottom = {node: index for index, node in enumerate(lower)}
    total = 0
    for first, second in itertools.combinations(edges, 2):
        if ((top[first[0]] - top[second[0]])
                * (bottom[first[1]] - bottom[second[1]])) < 0:
            total += 1
    return total


def barycentre_order(upper, lower, edges):
    """Ordnet die untere Schicht nach dem Mittelwert der Nachbarpositionen.

    Knoten ohne Nachbarn oben behalten ihre Position, damit die Ordnung
    stabil bleibt.
    """
    top = {node: index for index, node in enumerate(upper)}
    keys = {}
    for index, node in enumerate(lower):
        partners = [top[first] for first, second in edges if second == node]
        keys[node] = sum(partners) / len(partners) if partners else index
    return sorted(lower, key=lambda node: (keys[node], lower.index(node)))


def minimum_crossings(upper, lower, edges):
    """Bestimmt die kleinstmögliche Kreuzungszahl durch Aufzählung.

    Raises:
        ValueError: bei mehr als acht Knoten in der unteren Schicht.
    """
    if len(lower) > 8:
        raise ValueError("zu viele Knoten fuer die Aufzaehlung")
    return min(count_crossings(upper, list(order), edges)
               for order in itertools.permutations(lower))


def crossing_example():
    """Misst die Kreuzungszahl vor und nach dem Baryzentrum-Schritt.

    Returns:
        Abbildung mit beiden Zahlen und der erreichten Reihenfolge.
    """
    upper = ["a", "b", "c"]
    lower = ["x", "y", "z"]
    edges = [("a", "z"), ("b", "y"), ("c", "x")]
    before = count_crossings(upper, lower, edges)
    ordered = barycentre_order(upper, lower, edges)
    return {"before": before,
            "after": count_crossings(upper, ordered, edges),
            "order": ordered}


def compared_with_the_optimum():
    """Vergleicht das Baryzentrum mit der besten Reihenfolge.

    Returns:
        Abbildung mit der Kreuzungszahl des Verfahrens und dem Optimum.
    """
    upper = ["a", "b", "c", "d"]
    lower = ["w", "x", "y", "z"]
    edges = [("a", "x"), ("a", "z"), ("b", "w"), ("b", "y"),
             ("c", "x"), ("c", "w"), ("d", "z"), ("d", "y")]
    ordered = barycentre_order(upper, lower, edges)
    return {"barycentre": count_crossings(upper, ordered, edges),
            "optimum": minimum_crossings(upper, lower, edges)}


def counting_agrees():
    """Prüft die Kreuzungszählung gegen eine geometrische Rechnung.

    Für zufällige Reihenfolgen werden die Kanten als Strecken zwischen
    zwei waagerechten Linien gelegt und die Schnittpunkte bestimmt; das
    Ergebnis muss mit der kombinatorischen Zählung übereinstimmen.
    """
    import random

    generator = random.Random(7)
    for _ in range(30):
        upper = list("abcd")
        lower = list("wxyz")
        edges = [(generator.choice(upper), generator.choice(lower))
                 for _ in range(5)]
        edges = list(dict.fromkeys(edges))
        generator.shuffle(upper)
        generator.shuffle(lower)
        top = {node: index for index, node in enumerate(upper)}
        bottom = {node: index for index, node in enumerate(lower)}
        geometric = 0
        for first, second in itertools.combinations(edges, 2):
            x1, x2 = top[first[0]], bottom[first[1]]
            x3, x4 = top[second[0]], bottom[second[1]]
            if (x1 - x3) * (x2 - x4) < 0:
                geometric += 1
        if geometric != count_crossings(upper, lower, edges):
            return False
    return True


def steps():
    """Nennt die vier Schritte des Verfahrens."""
    return ["remove cycles", "assign layers", "reduce crossings",
            "assign horizontal coordinates"]
