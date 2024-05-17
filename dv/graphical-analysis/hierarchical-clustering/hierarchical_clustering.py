"""Agglomeratives hierarchisches Clustering mit drei Verkettungsmassen."""

import math

METHODS = ("single", "complete", "average")


def _distance(first, second):
    """Euklidischer Abstand zweier Punkte."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def _between(first, second, points, method):
    """Abstand zweier Gruppen nach dem gewählten Verkettungsmass."""
    values = [_distance(points[a], points[b]) for a in first for b in second]
    if method == "single":
        return min(values)
    if method == "complete":
        return max(values)
    return sum(values) / len(values)


def linkage(points, method="single"):
    """Baut die Verschmelzungsfolge von unten nach oben auf.

    Args:
        points: die zu gruppierenden Punkte.
        method: ``single``, ``complete`` oder ``average``.

    Returns:
        Liste der Verschmelzungen, jede als Abbildung mit ``left``,
        ``right``, ``distance`` und ``members``.

    Raises:
        ValueError: bei einem unbekannten Verkettungsmass.
    """
    if method not in METHODS:
        raise ValueError("unbekanntes Verkettungsmass")
    groups = {index: [index] for index in range(len(points))}
    merges = []
    next_name = len(points)
    while len(groups) > 1:
        best = None
        for left in groups:
            for right in groups:
                if left >= right:
                    continue
                value = _between(groups[left], groups[right], points, method)
                if best is None or value < best[0]:
                    best = (value, left, right)
        value, left, right = best
        members = groups.pop(left) + groups.pop(right)
        groups[next_name] = members
        merges.append({"left": left, "right": right, "distance": value,
                       "members": sorted(members), "name": next_name})
        next_name += 1
    return merges


def cut(merges, count, k):
    """Schneidet den Baum so, dass k Gruppen bleiben.

    Args:
        merges: Ergebnis von :func:`linkage`.
        count: Anzahl der ursprünglichen Punkte.
        k: gewünschte Gruppenzahl.

    Returns:
        Liste der Gruppennummern je Punkt.

    Raises:
        ValueError: wenn k nicht zwischen eins und der Punktzahl liegt.
    """
    if not 1 <= k <= count:
        raise ValueError("k passt nicht zur Punktzahl")
    groups = {index: [index] for index in range(count)}
    for merge in merges[:count - k]:
        members = groups.pop(merge["left"]) + groups.pop(merge["right"])
        groups[merge["name"]] = members
    labels = [0] * count
    for number, members in enumerate(groups.values()):
        for index in members:
            labels[index] = number
    return labels


def agrees_with_spanning_tree(points):
    """Vergleicht die Einfachverkettung mit dem minimalen Spannbaum.

    Die Verschmelzungsabstände der Einfachverkettung sind genau die
    Kantenlängen des minimalen Spannbaums in aufsteigender Reihenfolge.
    Der Spannbaum wird hier unabhängig nach Prim gebaut.

    Returns:
        Wahr, wenn beide Folgen übereinstimmen.
    """
    merges = [merge["distance"] for merge in linkage(points, "single")]
    inside = {0}
    edges = []
    while len(inside) < len(points):
        best = None
        for a in inside:
            for b in range(len(points)):
                if b in inside:
                    continue
                value = _distance(points[a], points[b])
                if best is None or value < best[0]:
                    best = (value, b)
        edges.append(best[0])
        inside.add(best[1])
    return all(abs(a - b) < 1e-9 for a, b in zip(merges, sorted(edges)))


def shape_versus_compactness():
    """Stellt beide Verkettungsmasse an zwei langgestreckten Gruppen gegenüber.

    Die Punkte liegen auf zwei waagerechten Linien im Abstand 1.5, die
    Nachbarn innerhalb einer Linie im Abstand 1. Die Einfachverkettung
    folgt der Form und trennt die Linien; die Vollverkettung achtet auf
    Kompaktheit und schneidet quer, weil ihr die Enden einer Linie zu weit
    auseinanderliegen.

    Returns:
        Abbildung mit beiden Einteilungen bei zwei Gruppen und der Angabe,
        ob die Einfachverkettung die Linien getroffen hat.
    """
    points = [(0, 0), (1, 0), (2, 0), (3, 0),
              (0, 1.5), (1, 1.5), (2, 1.5), (3, 1.5)]
    single = cut(linkage(points, "single"), len(points), 2)
    complete = cut(linkage(points, "complete"), len(points), 2)
    rows = single[:4] == [single[0]] * 4 and single[4:] == [single[4]] * 4
    return {"single": single, "complete": complete,
            "single follows the rows": rows and single[0] != single[4],
            "complete cuts across": complete[0] == complete[4]}


def dendrogram_heights(merges):
    """Gibt die Höhen der Verschmelzungen in ihrer Reihenfolge zurück."""
    return [merge["distance"] for merge in merges]
