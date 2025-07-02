"""Splines: natürliche kubische Interpolation, Bézier und B-Splines."""

import math


def natural_cubic(nodes):
    """Bestimmt den natürlichen kubischen Spline durch die Stützpunkte.

    Auf jedem Teilintervall steht ein Polynom dritten Grades; an den
    inneren Stellen stimmen Wert, Steigung und Krümmung überein, an den
    Rändern verschwindet die zweite Ableitung.

    Args:
        nodes: aufsteigend sortierte Paare (x, y).

    Returns:
        Abbildung mit ``xs`` und den Koeffizienten ``a``, ``b``, ``c``,
        ``d`` je Teilintervall.

    Raises:
        ValueError: bei weniger als drei Punkten oder nicht aufsteigenden
            Stützstellen.
    """
    if len(nodes) < 3:
        raise ValueError("mindestens drei Punkte noetig")
    xs = [x for x, _ in nodes]
    ys = [y for _, y in nodes]
    if any(later <= earlier for earlier, later in zip(xs, xs[1:])):
        raise ValueError("Stuetzstellen muessen aufsteigen")
    count = len(nodes) - 1
    widths = [xs[index + 1] - xs[index] for index in range(count)]
    matrix = [[0.0] * (count + 1) for _ in range(count + 1)]
    right = [0.0] * (count + 1)
    matrix[0][0] = 1.0
    matrix[count][count] = 1.0
    for index in range(1, count):
        matrix[index][index - 1] = widths[index - 1]
        matrix[index][index] = 2 * (widths[index - 1] + widths[index])
        matrix[index][index + 1] = widths[index]
        right[index] = 3 * ((ys[index + 1] - ys[index]) / widths[index]
                            - (ys[index] - ys[index - 1]) / widths[index - 1])
    curvature = _solve(matrix, right)
    a, b, c, d = [], [], [], []
    for index in range(count):
        a.append(ys[index])
        b.append((ys[index + 1] - ys[index]) / widths[index]
                 - widths[index] * (2 * curvature[index]
                                    + curvature[index + 1]) / 3)
        c.append(curvature[index])
        d.append((curvature[index + 1] - curvature[index])
                 / (3 * widths[index]))
    return {"xs": xs, "a": a, "b": b, "c": c, "d": d}


def _solve(matrix, right):
    """Löst ein lineares Gleichungssystem mit Gauss-Elimination."""
    size = len(matrix)
    rows = [list(matrix[index]) + [right[index]] for index in range(size)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(rows[row][column]))
        if abs(rows[pivot][column]) < 1e-12:
            raise ValueError("System ist singulaer")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column] / rows[column][column]
            for position in range(column, size + 1):
                rows[row][position] -= factor * rows[column][position]
    return [rows[index][size] / rows[index][index] for index in range(size)]


def _segment(spline, position):
    """Sucht das Teilintervall, in dem eine Stelle liegt."""
    xs = spline["xs"]
    if position < xs[0] - 1e-12 or position > xs[-1] + 1e-12:
        raise ValueError("Stelle liegt ausserhalb des Splines")
    for index in range(len(xs) - 1):
        if position <= xs[index + 1] + 1e-12:
            return index
    return len(xs) - 2


def evaluate(spline, position):
    """Wertet den Spline an einer Stelle aus."""
    index = _segment(spline, position)
    offset = position - spline["xs"][index]
    return (spline["a"][index] + spline["b"][index] * offset
            + spline["c"][index] * offset ** 2
            + spline["d"][index] * offset ** 3)


def derivative(spline, position):
    """Erste Ableitung des Splines."""
    index = _segment(spline, position)
    offset = position - spline["xs"][index]
    return (spline["b"][index] + 2 * spline["c"][index] * offset
            + 3 * spline["d"][index] * offset ** 2)


def second_derivative(spline, position):
    """Zweite Ableitung des Splines."""
    index = _segment(spline, position)
    offset = position - spline["xs"][index]
    return 2 * spline["c"][index] + 6 * spline["d"][index] * offset


def is_twice_differentiable(spline, tolerance=1e-9):
    """Prüft an den inneren Stützstellen, ob die Stücke glatt anschliessen."""
    xs = spline["xs"]
    for index in range(1, len(xs) - 1):
        position = xs[index]
        step = 1e-6
        for function in (evaluate, derivative, second_derivative):
            left = function(spline, position - step)
            right = function(spline, position + step)
            if abs(left - right) > 1e-4:
                return False
    return True


def de_casteljau(control, position):
    """Wertet eine Bézier-Kurve durch wiederholtes Halbieren aus.

    Raises:
        ValueError: bei einem Parameter ausserhalb von [0, 1] oder ohne
            Kontrollpunkte.
    """
    if not control:
        raise ValueError("keine Kontrollpunkte")
    if not 0.0 <= position <= 1.0:
        raise ValueError("Parameter liegt ausserhalb von [0, 1]")
    points = [tuple(float(value) for value in point) for point in control]
    while len(points) > 1:
        points = [tuple(a + (b - a) * position for a, b in zip(first, second))
                  for first, second in zip(points, points[1:])]
    return points[0]


def bernstein(control, position):
    """Wertet dieselbe Kurve über die Bernstein-Polynome aus."""
    degree = len(control) - 1
    result = [0.0] * len(control[0])
    for index, point in enumerate(control):
        weight = (math.comb(degree, index) * position ** index
                  * (1 - position) ** (degree - index))
        for axis in range(len(result)):
            result[axis] += weight * point[axis]
    return tuple(result)


def b_spline_basis(index, degree, knots, position):
    """Berechnet eine B-Spline-Basisfunktion nach Cox und de Boor."""
    if degree == 0:
        inside = knots[index] <= position < knots[index + 1]
        last = (position == knots[-1] and knots[index + 1] == knots[-1]
                and knots[index] < knots[index + 1])
        return 1.0 if inside or last else 0.0
    left = 0.0
    span = knots[index + degree] - knots[index]
    if span > 0:
        left = ((position - knots[index]) / span
                * b_spline_basis(index, degree - 1, knots, position))
    right = 0.0
    span = knots[index + degree + 1] - knots[index + 1]
    if span > 0:
        right = ((knots[index + degree + 1] - position) / span
                 * b_spline_basis(index + 1, degree - 1, knots, position))
    return left + right


def b_spline(control, degree, knots, position):
    """Wertet eine B-Spline-Kurve aus."""
    result = [0.0] * len(control[0])
    for index, point in enumerate(control):
        weight = b_spline_basis(index, degree, knots, position)
        for axis in range(len(result)):
            result[axis] += weight * point[axis]
    return tuple(result)


def locality():
    """Misst, wie weit sich das Verschieben eines Kontrollpunkts auswirkt.

    Bei einer Bézier-Kurve zieht jeder Punkt die ganze Kurve mit; bei
    einem B-Spline reicht der Einfluss nur über wenige Segmente.

    Returns:
        Abbildung mit der Änderung nahe am verschobenen Punkt und weit
        davon entfernt.
    """
    control = [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0), (4.0, 0.0),
               (5.0, 1.0)]
    degree = 3
    knots = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
    moved = list(control)
    moved[4] = (4.0, 5.0)
    near = abs(b_spline(control, degree, knots, 2.5)[1]
               - b_spline(moved, degree, knots, 2.5)[1])
    far = abs(b_spline(control, degree, knots, 0.2)[1]
              - b_spline(moved, degree, knots, 0.2)[1])
    return {"changed nearby": near, "changed far away": far}


def properties():
    """Nennt die Eigenschaften, die eine Bézier-Kurve immer hat."""
    return ["passes through the first and last control point",
            "lies inside the convex hull of the control points",
            "is affine invariant", "is symmetric in the control points"]
