"""Vereinfachung von Polygonzügen: Douglas-Peucker und das Optimum."""

import math


def perpendicular_distance(point, start, end):
    """Abstand eines Punktes zur Geraden durch zwei andere Punkte.

    Fallen Start und Ende zusammen, wird der Abstand zum Punkt selbst
    genommen.
    """
    (x, y), (x0, y0), (x1, y1) = point, start, end
    length = math.hypot(x1 - x0, y1 - y0)
    if length == 0:
        return math.hypot(x - x0, y - y0)
    return abs((y1 - y0) * x - (x1 - x0) * y + x1 * y0 - y1 * x0) / length


def douglas_peucker(points, tolerance):
    """Vereinfacht einen Polygonzug rekursiv.

    Der am weitesten von der Verbindungsstrecke entfernte Punkt wird
    behalten, wenn sein Abstand die Toleranz überschreitet, und die beiden
    Hälften werden getrennt weiterbehandelt.

    Args:
        points: die Punkte des Zuges.
        tolerance: erlaubter Höchstabstand.

    Returns:
        Die behaltenen Punkte, Anfang und Ende immer eingeschlossen.

    Raises:
        ValueError: bei negativer Toleranz oder weniger als zwei Punkten.
    """
    if tolerance < 0:
        raise ValueError("Toleranz ist negativ")
    if len(points) < 2:
        raise ValueError("mindestens zwei Punkte noetig")
    if len(points) == 2:
        return list(points)
    worst = 0.0
    index = 0
    for position in range(1, len(points) - 1):
        distance = perpendicular_distance(points[position], points[0],
                                          points[-1])
        if distance > worst:
            worst = distance
            index = position
    if worst <= tolerance:
        return [points[0], points[-1]]
    left = douglas_peucker(points[:index + 1], tolerance)
    right = douglas_peucker(points[index:], tolerance)
    return left[:-1] + right


def error(points, kept):
    """Grösster Abstand eines Originalpunktes zum vereinfachten Zug."""
    positions = [points.index(point) for point in kept]
    worst = 0.0
    for start, end in zip(positions, positions[1:]):
        for middle in range(start + 1, end):
            worst = max(worst, perpendicular_distance(points[middle],
                                                      points[start],
                                                      points[end]))
    return worst


def min_count(points, tolerance):
    """Bestimmt die kleinste Zahl von Punkten innerhalb der Toleranz.

    Das ist die min-#-Version nach Imai und Iri: über den erlaubten
    Abkürzungen wird der kürzeste Weg von Anfang zu Ende gesucht.

    Returns:
        Die Zahl der Punkte des kürzesten zulässigen Zuges.
    """
    count = len(points)
    allowed = [[False] * count for _ in range(count)]
    for start in range(count):
        for end in range(start + 1, count):
            if all(perpendicular_distance(points[middle], points[start],
                                          points[end]) <= tolerance
                   for middle in range(start + 1, end)):
                allowed[start][end] = True
    best = [None] * count
    best[0] = 1
    for end in range(1, count):
        for start in range(end):
            if allowed[start][end] and best[start] is not None:
                candidate = best[start] + 1
                if best[end] is None or candidate < best[end]:
                    best[end] = candidate
    if best[-1] is None:
        raise ValueError("keine zulaessige Vereinfachung")
    return best[-1]


def min_path(points, tolerance):
    """Gibt den kürzesten zulässigen Zug selbst zurück."""
    count = len(points)
    best = [None] * count
    previous = [None] * count
    best[0] = 1
    for end in range(1, count):
        for start in range(end):
            if best[start] is None:
                continue
            if all(perpendicular_distance(points[middle], points[start],
                                          points[end]) <= tolerance
                   for middle in range(start + 1, end)):
                candidate = best[start] + 1
                if best[end] is None or candidate < best[end]:
                    best[end] = candidate
                    previous[end] = start
    if best[-1] is None:
        raise ValueError("keine zulaessige Vereinfachung")
    path = [count - 1]
    while previous[path[-1]] is not None:
        path.append(previous[path[-1]])
    return [points[index] for index in reversed(path)]


def greedy_is_not_optimal():
    """Sucht einen Zug, auf dem das rekursive Verfahren zu viel behält.

    Douglas-Peucker teilt am weitesten entfernten Punkt und trifft damit
    eine Entscheidung, die es später nicht zurücknimmt; die
    Wegesuche über alle erlaubten Abkürzungen findet das Minimum.

    Returns:
        Abbildung mit beiden Punktzahlen und dem verwendeten Zug.
    """
    points = [(0, 0), (1, 0.1), (2, -0.1), (3, 5), (4, 6), (5, 7),
              (6, 8.1), (7, 9), (8, 9), (9, 9)]
    tolerance = 1.0
    return {"douglas peucker": len(douglas_peucker(points, tolerance)),
            "optimum": min_count(points, tolerance),
            "points": points}


def error_measures():
    """Nennt die Fehlermasse, die die Vorlesung unterscheidet."""
    return {"parallel strip": "distance to the segment line",
            "infinite beam": "distance to the infinite line",
            "hausdorff": "largest distance between the two curves"}
