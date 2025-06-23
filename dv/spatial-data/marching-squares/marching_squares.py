"""Marching Squares: Isolinien aus einer impliziten Funktion."""

import math


def circle_grid(size=7, extent=1.5):
    """Wertet x² + y² − 1 auf einem gleichmässigen Gitter aus.

    Args:
        size: Zahl der Gitterpunkte je Achse.
        extent: halbe Breite des abgedeckten Bereichs.

    Returns:
        Abbildung mit ``values``, ``xs`` und ``ys``.
    """
    xs = [-extent + 2 * extent * index / (size - 1) for index in range(size)]
    ys = list(xs)
    values = [[x * x + y * y - 1.0 for x in xs] for y in ys]
    return {"values": values, "xs": xs, "ys": ys}


def case(corners):
    """Bestimmt die Fallnummer einer Zelle aus den Vorzeichen ihrer Ecken.

    Die Ecken werden gegen den Uhrzeigersinn gezählt, beginnend links
    unten; ein positiver Wert setzt das entsprechende Bit.
    """
    number = 0
    for index, value in enumerate(corners):
        if value > 0:
            number |= 1 << index
    return number


def _interpolate(first, second, first_value, second_value, digits=None):
    """Bestimmt den Nulldurchgang auf einer Kante durch lineare Interpolation.

    Args:
        first, second: die Endpunkte der Kante.
        first_value, second_value: die Funktionswerte dort.
        digits: auf so viele Nachkommastellen wird das Teilungsverhältnis
            gerundet, wie es die Übung verlangt; None rechnet exakt.

    Returns:
        Der Punkt des Nulldurchgangs.
    """
    span = second_value - first_value
    ratio = 0.5 if span == 0 else -first_value / span
    if digits is not None:
        ratio = round(ratio, digits)
    return (first[0] + (second[0] - first[0]) * ratio,
            first[1] + (second[1] - first[1]) * ratio)


EDGES = {
    0: [], 15: [],
    1: [(3, 0)], 14: [(3, 0)],
    2: [(0, 1)], 13: [(0, 1)],
    3: [(3, 1)], 12: [(3, 1)],
    4: [(1, 2)], 11: [(1, 2)],
    6: [(0, 2)], 9: [(0, 2)],
    7: [(3, 2)], 8: [(3, 2)],
    5: [(3, 0), (1, 2)], 10: [(0, 1), (2, 3)],
}


def contour(grid, digits=None):
    """Legt einen Polygonzug durch die Nullstellen der Funktion.

    Für jede Zelle wird die Fallnummer bestimmt und für jede geschnittene
    Kante der Nulldurchgang interpoliert.

    Returns:
        Liste der Strecken als Punktpaare.
    """
    values = grid["values"]
    xs, ys = grid["xs"], grid["ys"]
    segments = []
    for row in range(len(ys) - 1):
        for column in range(len(xs) - 1):
            corners = [values[row][column], values[row][column + 1],
                       values[row + 1][column + 1], values[row + 1][column]]
            points = [(xs[column], ys[row]), (xs[column + 1], ys[row]),
                      (xs[column + 1], ys[row + 1]), (xs[column], ys[row + 1])]
            number = case(corners)
            for first_edge, second_edge in EDGES[number]:
                start = _edge_point(points, corners, first_edge, digits)
                end = _edge_point(points, corners, second_edge, digits)
                segments.append((start, end))
    return segments


def _edge_point(points, corners, edge, digits):
    """Nulldurchgang auf der Kante mit der genannten Nummer."""
    first = edge
    second = (edge + 1) % 4
    return _interpolate(points[first], points[second], corners[first],
                        corners[second], digits)


def largest_radius_error(grid=None, digits=None):
    """Misst, wie weit die Kontur vom Einheitskreis abweicht.

    Returns:
        Der grösste Betrag der Abweichung des Radius von eins.
    """
    if grid is None:
        grid = circle_grid()
    worst = 0.0
    for start, end in contour(grid, digits):
        for point in (start, end):
            worst = max(worst, abs(math.hypot(*point) - 1.0))
    return worst


def rounding_cost():
    """Vergleicht die exakte Interpolation mit der gerundeten der Übung.

    Das Runden des Teilungsverhältnisses auf eine Nachkommastelle
    verschiebt jeden Konturpunkt um bis zu einem Zwanzigstel der
    Zellenbreite. Auf einem groben Gitter fällt das nicht auf, auf einem
    feinen bleibt der Fehler dort stehen, wo die exakte Rechnung längst
    genauer ist.

    Returns:
        Abbildung mit beiden grössten Abweichungen je Gitterweite und der
        Zahl der Gitter, auf denen das Runden schadet.
    """
    rows = {}
    worse = 0
    for size in (5, 7, 9, 13, 21):
        grid = circle_grid(size)
        exact = largest_radius_error(grid, digits=None)
        rounded = largest_radius_error(grid, digits=1)
        rows[size] = {"exact": exact, "rounded": rounded}
        if rounded > exact:
            worse += 1
    return {"by size": rows, "rounding is worse on": worse,
            "grids": len(rows),
            "exact keeps improving": rows[21]["exact"] < rows[5]["exact"] / 10,
            "rounded stalls": rows[21]["rounded"] > rows[9]["rounded"] / 3}


def is_closed(segments, tolerance=1e-9):
    """Prüft, ob jeder Endpunkt der Kontur genau zweimal vorkommt."""
    counts = {}
    for start, end in segments:
        for point in (start, end):
            key = (round(point[0] / tolerance), round(point[1] / tolerance))
            counts[key] = counts.get(key, 0) + 1
    return all(value % 2 == 0 for value in counts.values())


def ambiguous_cases():
    """Nennt die Fälle, in denen die Zelle zwei Deutungen zulässt.

    Bei den Fällen 5 und 10 liegen die beiden positiven Ecken diagonal
    gegenüber; ob die Kontur die Ecken trennt oder verbindet, sagt das
    Vorzeichenmuster allein nicht.
    """
    return [5, 10]


def asymptotic_decider(corners):
    """Entscheidet einen Sattelfall über die bilineare Interpolation.

    Der Wert im Sattelpunkt der bilinearen Fläche gibt die Antwort: hat er
    dasselbe Vorzeichen wie die diagonal liegenden Ecken, sind sie
    verbunden, sonst getrennt.

    Args:
        corners: die vier Eckwerte gegen den Uhrzeigersinn.

    Returns:
        Abbildung mit dem Sattelwert und der Entscheidung.

    Raises:
        ValueError: wenn der Fall gar nicht mehrdeutig ist.
    """
    if case(corners) not in ambiguous_cases():
        raise ValueError("dieser Fall ist eindeutig")
    a, b, c, d = corners
    denominator = a - b + c - d
    if abs(denominator) < 1e-12:
        return {"saddle": 0.0, "connection": "separated"}
    saddle = (a * c - b * d) / denominator
    positive = a > 0
    connected = (saddle > 0) == positive
    return {"saddle": saddle,
            "connection": "joined" if connected else "separated"}


def marching_cubes_cases():
    """Zählt die Fälle des dreidimensionalen Verfahrens.

    Acht Ecken mit je zwei Vorzeichen ergeben 256 Muster; unter Drehung
    und Vorzeichentausch bleiben die 15 Grundfälle der Vorlesung übrig.
    """
    return {"patterns": 256, "elementary": 15,
            "problem": "ambiguous faces can leave holes in the surface"}
