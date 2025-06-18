"""Alpha-Hülle und Alpha-Form nach Edelsbrunner."""

import itertools
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "convex-hull"))

import convex_hull


def radius_of(alpha):
    """Rechnet den Parameter in den Radius der Kreisscheibe um.

    Die Vorlesung benutzt negative Werte: ein α-Ball ist dann das
    Komplement einer offenen Kreisscheibe mit dem Radius 1/|α|. Je näher α
    an null liegt, desto grösser der Radius und desto ähnlicher wird die
    Form der konvexen Hülle.

    Raises:
        ValueError: bei einem nicht negativen α.
    """
    if alpha >= 0:
        raise ValueError("diese Umsetzung erwartet ein negatives alpha")
    return 1.0 / abs(alpha)


def _circle_centres(first, second, radius):
    """Bestimmt die Mittelpunkte der beiden Kreise durch zwei Punkte.

    Returns:
        Liste der Mittelpunkte; leer, wenn der Radius zu klein ist.
    """
    (x1, y1), (x2, y2) = first, second
    half = math.hypot(x2 - x1, y2 - y1) / 2.0
    if half > radius or half == 0:
        return []
    middle = ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
    height = math.sqrt(max(radius * radius - half * half, 0.0))
    direction = ((y2 - y1) / (2 * half), -(x2 - x1) / (2 * half))
    return [(middle[0] + direction[0] * height,
             middle[1] + direction[1] * height),
            (middle[0] - direction[0] * height,
             middle[1] - direction[1] * height)]


def shape_edges(points, alpha):
    """Bestimmt die Kanten der Alpha-Form.

    Zwei Punkte sind verbunden, wenn eine Kreisscheibe vom Radius 1/|α|
    durch beide gelegt werden kann, in deren Innerem kein weiterer Punkt
    liegt.

    Args:
        points: die Punktwolke.
        alpha: negativer Parameter.

    Returns:
        Menge der Kanten als sortierte Punktpaare.

    Raises:
        ValueError: bei einem nicht negativen α.
    """
    radius = radius_of(alpha)
    unique = sorted(set(tuple(point) for point in points))
    edges = set()
    for first, second in itertools.combinations(unique, 2):
        for centre in _circle_centres(first, second, radius):
            empty = True
            for other in unique:
                if other in (first, second):
                    continue
                if math.dist(centre, other) < radius - 1e-9:
                    empty = False
                    break
            if empty:
                edges.add(tuple(sorted((first, second))))
                break
    return edges


def boundary_points(points, alpha):
    """Nennt die Punkte, die auf dem Rand der Alpha-Form liegen."""
    found = set()
    for first, second in shape_edges(points, alpha):
        found.add(first)
        found.add(second)
    return sorted(found)


def hull_versus_shape():
    """Beschreibt den Unterschied zwischen Alpha-Hülle und Alpha-Form.

    Die Alpha-Hülle ist der Durchschnitt aller α-Bälle, die alle Punkte
    enthalten; ihr Rand besteht aus Kreisbögen. Die Alpha-Form entsteht
    daraus, indem jeder Bogen durch die Strecke zwischen seinen beiden
    Endpunkten ersetzt wird.
    """
    return {"hull": "curved boundary of the intersection",
            "shape": "straight edges between the points",
            "same vertices": True}


def as_alpha_grows(points):
    """Zeigt, wie die Form mit wachsendem Radius zur konvexen Hülle wird.

    Returns:
        Abbildung von α auf die Zahl der Kanten der Form.
    """
    return {alpha: len(shape_edges(points, alpha))
            for alpha in (-2.0, -1.0, -0.5, -0.25, -0.001)}


def is_closed_cycle(edges):
    """Prüft, ob die Kanten einen einzigen geschlossenen Rand bilden.

    Jeder beteiligte Punkt muss genau zwei Kanten tragen, und alle Kanten
    müssen zusammenhängen.
    """
    if not edges:
        return False
    degree = {}
    for first, second in edges:
        degree[first] = degree.get(first, 0) + 1
        degree[second] = degree.get(second, 0) + 1
    if any(value != 2 for value in degree.values()):
        return False
    start = next(iter(degree))
    seen = {start}
    queue = [start]
    while queue:
        node = queue.pop()
        for first, second in edges:
            for a, b in ((first, second), (second, first)):
                if a == node and b not in seen:
                    seen.add(b)
                    queue.append(b)
    return len(seen) == len(degree)


def exercise_report():
    """Beantwortet die Aufgabe 3.1 für die zehn vorgegebenen Punkte.

    Bei α = −0.5 gehört zu jedem Punktpaar des Randes eine leere Scheibe
    vom Radius 2, und keine Einbuchtung ist tief genug, als dass die
    Scheibe hineinreichen könnte: die Form fällt mit dem Rand der konvexen
    Hülle zusammen. Erst ein kleinerer Radius greift nach innen.

    Returns:
        Abbildung mit den Kanten bei α = −0.5, der Angabe, ob sie mit der
        konvexen Hülle übereinstimmen, und dem grössten α, bei dem sie es
        nicht mehr tun.
    """
    points = [(0, 0), (0, 1), (1, 1), (1, 2), (0, 3),
              (0, 4), (1, 4), (2, 2), (2, 1), (1, 0)]
    edges = shape_edges(points, -0.5)
    boundary = hull_boundary_edges(points)
    first_difference = None
    for alpha in (-0.5, -0.75, -1.0, -1.5, -2.0):
        if shape_edges(points, alpha) != boundary:
            first_difference = alpha
            break
    return {"edges": sorted(edges), "equals the hull": edges == boundary,
            "first alpha that differs": first_difference,
            "closed": is_closed_cycle(edges)}


def hull_boundary_edges(points):
    """Verbindet die Randpunkte der konvexen Hülle der Reihe nach.

    Punkte, die auf einer Kante der Hülle liegen, werden mitgenommen; der
    Rand besteht dann aus den Strecken zwischen aufeinanderfolgenden
    Randpunkten.
    """
    corners = convex_hull.hull(points)
    unique = [tuple(point) for point in dict.fromkeys(points)]
    edges = set()
    for index in range(len(corners)):
        first = corners[index]
        second = corners[(index + 1) % len(corners)]
        on_edge = [first, second]
        for point in unique:
            if point in (first, second):
                continue
            if abs(convex_hull.cross(first, second, point)) > 1e-12:
                continue
            if min(first[0], second[0]) - 1e-12 <= point[0] \
                    <= max(first[0], second[0]) + 1e-12 \
                    and min(first[1], second[1]) - 1e-12 <= point[1] \
                    <= max(first[1], second[1]) + 1e-12:
                on_edge.append(point)
        on_edge.sort(key=lambda point: (point[0] - first[0]) ** 2
                     + (point[1] - first[1]) ** 2)
        for a, b in zip(on_edge, on_edge[1:]):
            edges.add(tuple(sorted((a, b))))
    return edges


def falls_apart_below(points):
    """Sucht den Radius, unter dem keine Kante mehr übrig bleibt.

    Returns:
        Abbildung mit dem halben kleinsten Punktabstand und der Kantenzahl
        knapp darunter und knapp darüber.
    """
    smallest = min(math.dist(first, second)
                   for first, second in itertools.combinations(points, 2))
    half = smallest / 2.0
    return {"half the smallest distance": half,
            "below": len(shape_edges(points, -1.0 / (half * 0.9))),
            "above": len(shape_edges(points, -1.0 / (half * 1.1)))}


def matches_convex_hull(points, alpha=-0.001):
    """Prüft, ob die Form bei sehr grossem Radius die Hülle enthält."""
    hull = convex_hull.hull(points)
    expected = {tuple(sorted((hull[index], hull[(index + 1) % len(hull)])))
                for index in range(len(hull))}
    return expected <= shape_edges(points, alpha)
