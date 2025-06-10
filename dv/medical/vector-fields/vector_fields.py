"""Visualisierung von Vektorfeldern: Stromlinien und kritische Punkte."""

import math


def rotation_field(point):
    """Ein Wirbelfeld: die Geschwindigkeit steht senkrecht auf dem Radius."""
    x, y = point
    return (-y, x)


def source_field(point):
    """Ein Quellenfeld: die Geschwindigkeit zeigt nach aussen."""
    x, y = point
    return (x, y)


def saddle_field(point):
    """Ein Sattelfeld: eine Richtung zieht an, die andere stösst ab."""
    x, y = point
    return (x, -y)


def _step_euler(field, point, size):
    """Ein Schritt des expliziten Euler-Verfahrens."""
    velocity = field(point)
    return (point[0] + size * velocity[0], point[1] + size * velocity[1])


def _step_runge_kutta(field, point, size):
    """Ein Schritt des klassischen Verfahrens vierter Ordnung."""
    first = field(point)
    second = field((point[0] + size / 2 * first[0],
                    point[1] + size / 2 * first[1]))
    third = field((point[0] + size / 2 * second[0],
                   point[1] + size / 2 * second[1]))
    fourth = field((point[0] + size * third[0], point[1] + size * third[1]))
    return (point[0] + size / 6 * (first[0] + 2 * second[0] + 2 * third[0]
                                   + fourth[0]),
            point[1] + size / 6 * (first[1] + 2 * second[1] + 2 * third[1]
                                   + fourth[1]))


def streamline(field, start, steps, size, method="runge kutta"):
    """Verfolgt eine Stromlinie durch das Feld.

    Args:
        field: Abbildung von Punkt auf Geschwindigkeit.
        start: Startpunkt.
        steps: Zahl der Schritte.
        size: Schrittweite.
        method: ``euler`` oder ``runge kutta``.

    Returns:
        Liste der Punkte einschliesslich des Startpunkts.

    Raises:
        ValueError: bei einem unbekannten Verfahren.
    """
    if method not in ("euler", "runge kutta"):
        raise ValueError("unbekanntes Verfahren")
    step = _step_euler if method == "euler" else _step_runge_kutta
    point = tuple(float(value) for value in start)
    line = [point]
    for _ in range(steps):
        point = step(field, point, size)
        line.append(point)
    return line


def circle_error(method, steps):
    """Misst den Fehler nach genau einem Umlauf im Wirbelfeld.

    Die Schrittweite wird als 2π geteilt durch die Schrittzahl gewählt,
    damit der letzte Schritt genau auf dem Startpunkt endet. Sonst
    überdeckt der Rest des Umlaufs den Verfahrensfehler.

    Args:
        method: ``euler`` oder ``runge kutta``.
        steps: Zahl der Schritte für den vollen Umlauf.

    Returns:
        Der Abstand des Endpunkts vom Startpunkt.
    """
    size = 2 * math.pi / steps
    line = streamline(rotation_field, (1.0, 0.0), steps, size, method)
    return math.dist(line[-1], (1.0, 0.0))


def integration_error(steps=628):
    """Vergleicht beide Verfahren bei gleicher Schrittzahl.

    Returns:
        Abbildung mit dem Fehler beider Verfahren nach einem Umlauf.
    """
    return {"euler": circle_error("euler", steps),
            "runge kutta": circle_error("runge kutta", steps)}


def error_orders():
    """Bestimmt die Fehlerordnung beider Verfahren empirisch.

    Halbiert man die Schrittweite, so fällt der Fehler des Euler-Verfahrens
    um den Faktor zwei und der des Verfahrens vierter Ordnung um sechzehn.
    Aus dem Verhältnis zweier Fehler wird hier der Exponent zurückgerechnet.

    Returns:
        Abbildung mit beiden gemessenen Ordnungen und den Fehlern.
    """
    def order(method, coarse, fine):
        """Rechnet aus zwei Fehlern die Ordnung zurück."""
        first = circle_error(method, coarse)
        second = circle_error(method, fine)
        return math.log(first / second) / math.log(fine / coarse)

    return {"euler order": order("euler", 200, 400),
            "runge kutta order": order("runge kutta", 20, 40),
            "euler errors": (circle_error("euler", 200),
                             circle_error("euler", 400)),
            "runge kutta errors": (circle_error("runge kutta", 20),
                                   circle_error("runge kutta", 40))}


def classify(jacobian):
    """Ordnet einen kritischen Punkt anhand der Jacobi-Matrix ein.

    Reelle Eigenwerte gleichen Vorzeichens ergeben Quelle oder Senke,
    verschiedene Vorzeichen einen Sattel; rein imaginäre Eigenwerte ein
    Zentrum, komplexe mit Realteil eine Spirale.

    Raises:
        ValueError: wenn die Matrix nicht zweireihig ist.
    """
    if len(jacobian) != 2 or len(jacobian[0]) != 2:
        raise ValueError("nur fuer zweireihige Matrizen")
    trace = jacobian[0][0] + jacobian[1][1]
    determinant = (jacobian[0][0] * jacobian[1][1]
                   - jacobian[0][1] * jacobian[1][0])
    discriminant = trace * trace - 4 * determinant
    if discriminant >= 0:
        if determinant < 0:
            return "saddle"
        if trace > 0:
            return "source"
        if trace < 0:
            return "sink"
        return "degenerate"
    if abs(trace) < 1e-12:
        return "centre"
    return "spiral source" if trace > 0 else "spiral sink"


def classification_agrees():
    """Vergleicht die Einordnung mit den Eigenwerten aus numpy."""
    import numpy

    matrices = [[[1.0, 0.0], [0.0, 1.0]], [[-1.0, 0.0], [0.0, -1.0]],
                [[1.0, 0.0], [0.0, -1.0]], [[0.0, -1.0], [1.0, 0.0]],
                [[0.5, -1.0], [1.0, 0.5]], [[-0.5, -1.0], [1.0, -0.5]]]
    for matrix in matrices:
        values = numpy.linalg.eigvals(numpy.array(matrix))
        real = [value.real for value in values]
        imaginary = [abs(value.imag) for value in values]
        if max(imaginary) < 1e-12:
            if real[0] * real[1] < 0:
                expected = "saddle"
            elif min(real) > 0:
                expected = "source"
            elif max(real) < 0:
                expected = "sink"
            else:
                expected = "degenerate"
        elif abs(sum(real)) < 1e-12:
            expected = "centre"
        else:
            expected = "spiral source" if sum(real) > 0 else "spiral sink"
        if classify(matrix) != expected:
            return False
    return True


def arrow_density(width=512, height=512, spacing=16):
    """Vergleicht, wie viele Werte ein Pfeilbild und eine Textur zeigen.

    Pfeile brauchen Platz, damit sie lesbar bleiben; eine texturbasierte
    Darstellung wie die Linienintegralfaltung setzt jedes Bildelement ein.

    Returns:
        Abbildung mit beiden Zahlen.
    """
    return {"arrows": (width // spacing) * (height // spacing),
            "texture": width * height}


def representations():
    """Nennt die Darstellungsarten für Vektorfelder aus der Vorlesung."""
    return {"direct": "arrows and colour coded magnitude",
            "texture": "line integral convolution",
            "geometric": "streamlines, ribbons and surfaces",
            "feature": "critical points and vortex cores"}
