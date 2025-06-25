"""Polygontriangulierung durch Abschneiden von Ohren."""

import math


def area(polygon):
    """Fläche eines einfachen Polygons nach der Trapezformel."""
    return abs(signed_area(polygon))


def signed_area(polygon):
    """Vorzeichenbehaftete Fläche; positiv gegen den Uhrzeigersinn."""
    total = 0.0
    for index in range(len(polygon)):
        first = polygon[index]
        second = polygon[(index + 1) % len(polygon)]
        total += first[0] * second[1] - second[0] * first[1]
    return total / 2.0


def is_counterclockwise(polygon):
    """Sagt, ob die Punkte gegen den Uhrzeigersinn angegeben sind."""
    return signed_area(polygon) > 0


def triangle_area(triangle):
    """Fläche eines Dreiecks."""
    (x1, y1), (x2, y2), (x3, y3) = triangle
    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0


def _cross(origin, first, second):
    """Kreuzprodukt zur Bestimmung der Drehrichtung."""
    return ((first[0] - origin[0]) * (second[1] - origin[1])
            - (first[1] - origin[1]) * (second[0] - origin[0]))


def _inside(triangle, point):
    """Prüft, ob ein Punkt echt im Dreieck liegt."""
    a, b, c = triangle
    first = _cross(a, b, point)
    second = _cross(b, c, point)
    third = _cross(c, a, point)
    return ((first > 1e-12 and second > 1e-12 and third > 1e-12)
            or (first < -1e-12 and second < -1e-12 and third < -1e-12))


def is_ear(polygon, index):
    """Prüft, ob die Ecke an dieser Stelle ein Ohr ist.

    Ein Ohr ist eine konvexe Ecke, deren Dreieck keinen weiteren
    Polygonpunkt enthält.
    """
    count = len(polygon)
    previous = polygon[(index - 1) % count]
    current = polygon[index]
    following = polygon[(index + 1) % count]
    orientation = 1 if is_counterclockwise(polygon) else -1
    if _cross(previous, current, following) * orientation <= 0:
        return False
    triangle = (previous, current, following)
    for position, point in enumerate(polygon):
        if position in ((index - 1) % count, index, (index + 1) % count):
            continue
        if _inside(triangle, point):
            return False
    return True


def ear_clipping(polygon):
    """Zerlegt ein einfaches Polygon in Dreiecke.

    Es wird wiederholt ein Ohr abgeschnitten, bis nur noch ein Dreieck
    übrig ist. Ein einfaches Polygon mit n Ecken zerfällt dabei stets in
    n − 2 Dreiecke.

    Returns:
        Liste der Dreiecke als Punktetripel.

    Raises:
        ValueError: bei weniger als drei Ecken oder wenn kein Ohr gefunden
            wird, das Polygon also nicht einfach ist.
    """
    if len(polygon) < 3:
        raise ValueError("mindestens drei Ecken noetig")
    remaining = list(polygon)
    triangles = []
    while len(remaining) > 3:
        for index in range(len(remaining)):
            if is_ear(remaining, index):
                count = len(remaining)
                triangles.append((remaining[(index - 1) % count],
                                  remaining[index],
                                  remaining[(index + 1) % count]))
                remaining.pop(index)
                break
        else:
            raise ValueError("kein Ohr gefunden, Polygon nicht einfach")
    triangles.append(tuple(remaining))
    return triangles


def circumcircle(triangle):
    """Bestimmt Mittelpunkt und Radius des Umkreises.

    Raises:
        ValueError: wenn die drei Punkte auf einer Geraden liegen.
    """
    (ax, ay), (bx, by), (cx, cy) = triangle
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:
        raise ValueError("Punkte liegen auf einer Geraden")
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay)
          + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx)
          + (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy), math.dist((ux, uy), (ax, ay))


def is_delaunay(triangles, points):
    """Prüft, ob keine Umkreisscheibe einen weiteren Punkt enthält."""
    for triangle in triangles:
        try:
            centre, radius = circumcircle(triangle)
        except ValueError:
            return False
        for point in points:
            if point in triangle:
                continue
            if math.dist(centre, point) < radius - 1e-9:
                return False
    return True


def simplex_vertices(dimension):
    """Zahl der Ecken eines d-Simplex.

    Ein 0-Simplex ist ein Punkt, ein 1-Simplex eine Strecke, ein 2-Simplex
    ein Dreieck und ein 3-Simplex ein Tetraeder: der einfachste Körper der
    jeweiligen Dimension hat d + 1 Ecken.

    Raises:
        ValueError: bei negativer Dimension.
    """
    if dimension < 0:
        raise ValueError("Dimension ist negativ")
    return dimension + 1
