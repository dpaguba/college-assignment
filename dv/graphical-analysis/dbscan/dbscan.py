"""Dichtebasiertes Clustering nach DBSCAN."""

import math

NOISE = -1


def _distance(first, second):
    """Euklidischer Abstand zweier Punkte."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def neighbours(points, index, eps):
    """Sammelt die Punkte in der Epsilon-Umgebung, den Punkt selbst inbegriffen."""
    return [other for other in range(len(points))
            if _distance(points[index], points[other]) <= eps]


def core_points(points, eps, min_points):
    """Bestimmt die Kernpunkte.

    Ein Punkt ist Kernpunkt, wenn seine Epsilon-Umgebung mindestens
    ``min_points`` Punkte enthält, ihn selbst mitgezählt.

    Raises:
        ValueError: bei einem nicht positiven Epsilon.
    """
    if eps <= 0:
        raise ValueError("eps muss positiv sein")
    return {index for index in range(len(points))
            if len(neighbours(points, index, eps)) >= min_points}


def cluster(points, eps, min_points):
    """Gruppiert die Punkte und markiert Rauschen mit −1.

    Von jedem noch unbesuchten Kernpunkt aus wächst eine Gruppe über die
    Dichteerreichbarkeit; Punkte in der Umgebung eines Kernpunkts, die
    selbst keine Kernpunkte sind, werden Randpunkte derselben Gruppe.

    Returns:
        Liste der Gruppennummern je Punkt, −1 für Rauschen.
    """
    cores = core_points(points, eps, min_points)
    labels = [None] * len(points)
    current = 0
    for index in range(len(points)):
        if index not in cores or labels[index] is not None:
            continue
        labels[index] = current
        queue = [index]
        while queue:
            node = queue.pop(0)
            for other in neighbours(points, node, eps):
                if labels[other] is None:
                    labels[other] = current
                    if other in cores:
                        queue.append(other)
        current += 1
    return [NOISE if label is None else label for label in labels]


def agrees_with_components(points, eps, min_points):
    """Vergleicht das Ergebnis mit den Komponenten des Kernpunktgraphen.

    Die Gruppen sind genau die Zusammenhangskomponenten der Kernpunkte,
    die sich innerhalb von Epsilon erreichen. Diese Komponenten werden
    hier unabhängig berechnet.

    Returns:
        Wahr, wenn beide Einteilungen der Kernpunkte übereinstimmen.
    """
    cores = sorted(core_points(points, eps, min_points))
    parent = {index: index for index in cores}

    def find(node):
        """Sucht den Vertreter einer Komponente."""
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first in cores:
        for second in cores:
            if _distance(points[first], points[second]) <= eps:
                parent[find(first)] = find(second)
    by_component = {}
    for index in cores:
        by_component.setdefault(find(index), []).append(index)
    labels = cluster(points, eps, min_points)
    by_label = {}
    for index in cores:
        by_label.setdefault(labels[index], []).append(index)
    return (sorted(sorted(group) for group in by_component.values())
            == sorted(sorted(group) for group in by_label.values()))


def border_example():
    """Zeigt einen Randpunkt: in einer Gruppe, aber kein Kernpunkt.

    Returns:
        Abbildung mit der Zahl der Randpunkte und der Gruppennummer des
        ersten davon.
    """
    points = [(0, 0), (0.5, 0), (1, 0), (1.9, 0)]
    eps, min_points = 1.0, 3
    labels = cluster(points, eps, min_points)
    cores = core_points(points, eps, min_points)
    borders = [index for index in range(len(points))
               if index not in cores and labels[index] != NOISE]
    return {"border points": len(borders),
            "label": labels[borders[0]] if borders else NOISE,
            "cores": sorted(cores)}


def finds_the_count_itself():
    """Prüft, dass die Gruppenzahl aus den Daten kommt, nicht als Parameter.

    Zwei Datensätze mit zwei und mit drei Gruppen werden mit denselben
    Parametern behandelt; die Zahl der gefundenen Gruppen unterscheidet
    sich.
    """
    two = [(0, 0), (0.4, 0), (0.8, 0), (10, 0), (10.4, 0), (10.8, 0)]
    three = two + [(20, 0), (20.4, 0), (20.8, 0)]
    first = len(set(cluster(two, 1.0, 3)) - {NOISE})
    second = len(set(cluster(three, 1.0, 3)) - {NOISE})
    return first == 2 and second == 3


def parameter_effect():
    """Beschreibt, was die beiden Parameter steuern."""
    return {"eps": "how close counts as neighbouring",
            "min_points": "how many neighbours make a point dense",
            "too small eps": "everything becomes noise",
            "too large eps": "everything becomes one cluster"}
