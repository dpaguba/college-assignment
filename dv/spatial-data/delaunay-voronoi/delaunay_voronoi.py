"""Delaunay-Triangulierung und ihr duales Voronoi-Diagramm."""

import itertools
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "polygon-triangulation"))

import polygon_triangulation


def triangulate(points):
    """Bestimmt die Delaunay-Triangulierung über die Umkreisbedingung.

    Geprüft wird jedes Tripel: es gehört zur Triangulierung, wenn seine
    Umkreisscheibe leer ist. Das Verfahren ist in der Punktzahl vierter
    Ordnung und dient hier der Anschauung, nicht der Geschwindigkeit.

    Returns:
        Liste der Dreiecke als Punktetripel.

    Raises:
        ValueError: bei weniger als drei Punkten.
    """
    unique = [tuple(point) for point in dict.fromkeys(points)]
    if len(unique) < 3:
        raise ValueError("mindestens drei Punkte noetig")
    triangles = []
    for triple in itertools.combinations(unique, 3):
        try:
            centre, radius = polygon_triangulation.circumcircle(triple)
        except ValueError:
            continue
        if all(math.dist(centre, point) >= radius - 1e-9
               for point in unique if point not in triple):
            triangles.append(triple)
    return triangles


def circumcircles_are_empty(triangles, points):
    """Prüft die Umkreisbedingung für alle Dreiecke."""
    return polygon_triangulation.is_delaunay(triangles, points)


def smallest_angle(triangles):
    """Kleinster Innenwinkel aller Dreiecke im Bogenmass."""
    smallest = math.pi
    for triangle in triangles:
        for index in range(3):
            a = triangle[index]
            b = triangle[(index + 1) % 3]
            c = triangle[(index + 2) % 3]
            first = (b[0] - a[0], b[1] - a[1])
            second = (c[0] - a[0], c[1] - a[1])
            dot = first[0] * second[0] + first[1] * second[1]
            lengths = math.hypot(*first) * math.hypot(*second)
            if lengths == 0:
                continue
            smallest = min(smallest,
                           math.acos(max(-1.0, min(1.0, dot / lengths))))
    return smallest


def angle_comparison():
    """Vergleicht den kleinsten Winkel mit der anderen Zerlegung eines Vierecks.

    Ein Viereck lässt sich auf zwei Arten in Dreiecke teilen. Die
    Delaunay-Wahl ist die, deren kleinster Winkel grösser ist.

    Returns:
        Abbildung mit beiden kleinsten Winkeln im Gradmass.
    """
    square = [(0.0, 0.0), (4.0, 0.0), (5.0, 3.0), (1.0, 1.0)]
    first = [(square[0], square[1], square[2]),
             (square[0], square[2], square[3])]
    second = [(square[0], square[1], square[3]),
              (square[1], square[2], square[3])]
    delaunay = first if circumcircles_are_empty(first, square) else second
    other = second if delaunay is first else first
    return {"delaunay": math.degrees(smallest_angle(delaunay)),
            "alternative": math.degrees(smallest_angle(other))}


def voronoi_cell(points, index, box, resolution=60):
    """Nähert eine Voronoi-Zelle durch Abtasten eines Rechtecks an.

    Args:
        points: die Zentren.
        index: welches Zentrum gemeint ist.
        box: (xmin, ymin, xmax, ymax).
        resolution: Zahl der Abtastschritte je Achse.

    Returns:
        Liste der abgetasteten Punkte, die diesem Zentrum am nächsten sind.
    """
    xmin, ymin, xmax, ymax = box
    found = []
    for row in range(resolution + 1):
        for column in range(resolution + 1):
            x = xmin + (xmax - xmin) * column / resolution
            y = ymin + (ymax - ymin) * row / resolution
            nearest = min(range(len(points)),
                          key=lambda other: math.dist(points[other], (x, y)))
            if nearest == index:
                found.append((x, y))
    return found


def cells_agree_with_sampling(points):
    """Prüft die Definition der Zelle an einer Abtastung.

    Jeder abgetastete Punkt einer Zelle muss zu ihrem Zentrum näher liegen
    als zu jedem anderen; das ist die Definition selbst, hier über ein
    Gitter nachgerechnet.
    """
    box = (-0.5, -0.5, 1.5, 1.5)
    for index in range(len(points)):
        for sample in voronoi_cell(points, index, box, resolution=20):
            own = math.dist(points[index], sample)
            for other in range(len(points)):
                if other == index:
                    continue
                if math.dist(points[other], sample) < own - 1e-9:
                    return False
    return True


def duality_holds(points):
    """Prüft, dass Delaunay-Kanten benachbarten Voronoi-Zellen entsprechen.

    Zwei Punkte sind genau dann durch eine Delaunay-Kante verbunden, wenn
    ihre Voronoi-Zellen eine gemeinsame Grenze haben. Die Nachbarschaft
    wird hier über die Abtastung bestimmt.
    """
    box = (-1.0, -1.0, 2.0, 2.0)
    resolution = 80
    xmin, ymin, xmax, ymax = box
    owner = {}
    for row in range(resolution + 1):
        for column in range(resolution + 1):
            x = xmin + (xmax - xmin) * column / resolution
            y = ymin + (ymax - ymin) * row / resolution
            owner[(row, column)] = min(
                range(len(points)),
                key=lambda index: math.dist(points[index], (x, y)))
    adjacent = set()
    for (row, column), index in owner.items():
        for step in ((0, 1), (1, 0)):
            neighbour = owner.get((row + step[0], column + step[1]))
            if neighbour is not None and neighbour != index:
                adjacent.add(tuple(sorted((index, neighbour))))
    edges = set()
    for triangle in triangulate(points):
        for first, second in itertools.combinations(triangle, 2):
            edges.add(tuple(sorted((points.index(first),
                                    points.index(second)))))
    return edges <= adjacent


def cocircular_case():
    """Zeigt, dass vier Punkte auf einem Kreis keine eindeutige Wahl lassen.

    Returns:
        Abbildung mit der Zahl der leeren Dreiecke und der Feststellung,
        dass mehr als drei davon existieren.
    """
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = triangulate(points)
    return {"triangles": len(triangles), "ambiguous": len(triangles) > 2,
            "reason": "all four points lie on one circle"}


def voronoi_vertices(points):
    """Die Umkreismittelpunkte der Delaunay-Dreiecke sind die Voronoi-Ecken."""
    vertices = []
    for triangle in triangulate(points):
        centre, _ = polygon_triangulation.circumcircle(triangle)
        vertices.append(centre)
    return vertices
