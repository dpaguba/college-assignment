"""Konvexe Hülle einer ebenen Punktmenge."""

import itertools


def cross(origin, first, second):
    """Kreuzprodukt der Vektoren vom Ursprungspunkt zu den beiden anderen.

    Das Vorzeichen sagt, ob der Weg nach links oder nach rechts abbiegt.
    """
    return ((first[0] - origin[0]) * (second[1] - origin[1])
            - (first[1] - origin[1]) * (second[0] - origin[0]))


def hull(points):
    """Berechnet die konvexe Hülle nach Andrew.

    Die Punkte werden sortiert und in zwei Durchläufen zur unteren und
    zur oberen Kette zusammengesetzt; ein Punkt, der keine Linkskurve
    erzeugt, fällt wieder heraus.

    Args:
        points: die Punkte der Menge.

    Returns:
        Die Eckpunkte der Hülle gegen den Uhrzeigersinn, beginnend beim
        kleinsten Punkt; Punkte auf einer Kante fallen weg.

    Raises:
        ValueError: bei weniger als drei verschiedenen Punkten.
    """
    unique = sorted(set(tuple(point) for point in points))
    if len(unique) < 3:
        raise ValueError("mindestens drei verschiedene Punkte noetig")

    def half(sequence):
        """Baut eine Kette der Hülle auf."""
        chain = []
        for point in sequence:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], point) <= 0:
                chain.pop()
            chain.append(point)
        return chain

    lower = half(unique)
    upper = half(unique[::-1])
    return lower[:-1] + upper[:-1]


def contains(polygon, point):
    """Prüft, ob ein Punkt in einem konvexen Polygon liegt, Rand eingeschlossen."""
    if len(polygon) < 3:
        return False
    signs = []
    for index in range(len(polygon)):
        first = polygon[index]
        second = polygon[(index + 1) % len(polygon)]
        signs.append(cross(first, second, point))
    return all(value >= -1e-12 for value in signs) or \
        all(value <= 1e-12 for value in signs)


def agrees_with_supporting_lines(points, directions=3600):
    """Vergleicht die Hülle mit der Definition über Stützgeraden.

    Ein Punkt ist genau dann Ecke der Hülle, wenn es eine Richtung gibt, in
    der er allein am weitesten aussen liegt. Diese Prüfung tastet die
    Richtungen ab und benutzt weder Sortierung noch Kreuzprodukt, ist also
    vom Verfahren nach Andrew unabhängig.

    Returns:
        Wahr, wenn beide Wege dieselben Ecken liefern.
    """
    import math

    unique = sorted(set(tuple(point) for point in points))
    corners = set()
    for step in range(directions):
        angle = 2 * math.pi * step / directions
        direction = (math.cos(angle), math.sin(angle))
        best = None
        for point in unique:
            value = direction[0] * point[0] + direction[1] * point[1]
            if best is None or value > best[0] + 1e-9:
                best = (value, [point])
            elif abs(value - best[0]) <= 1e-9:
                best[1].append(point)
        if len(best[1]) == 1:
            corners.add(best[1][0])
    return corners == set(hull(points))


def area(polygon):
    """Fläche eines Polygons nach der Trapezformel."""
    total = 0.0
    for index in range(len(polygon)):
        first = polygon[index]
        second = polygon[(index + 1) % len(polygon)]
        total += first[0] * second[1] - second[0] * first[1]
    return abs(total) / 2.0
