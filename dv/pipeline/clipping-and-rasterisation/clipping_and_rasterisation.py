"""Clipping nach Cohen-Sutherland und Rasterung nach Bresenham."""

LEFT, RIGHT, BOTTOM, TOP = 1, 2, 4, 8


def outcode(point, window):
    """Bestimmt den Bereichscode eines Punktes zum Fenster.

    Args:
        point: Punkt als Paar.
        window: Fenster als (xmin, ymin, xmax, ymax).

    Returns:
        Bitmuster aus LEFT, RIGHT, BOTTOM und TOP; null heisst innerhalb.
    """
    xmin, ymin, xmax, ymax = window
    x, y = point
    code = 0
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code


def cohen_sutherland(segment, window):
    """Schneidet eine Strecke am Fenster zu.

    Der Algorithmus nimmt eine Strecke sofort an, wenn beide Codes null
    sind, und verwirft sie sofort, wenn die Codes eine gemeinsame Seite
    nennen. Sonst wird der Punkt ausserhalb auf die verletzte Kante
    gezogen und die Prüfung wiederholt.

    Returns:
        Die zugeschnittene Strecke oder None, wenn nichts übrig bleibt.
    """
    xmin, ymin, xmax, ymax = window
    (x0, y0), (x1, y1) = segment
    code0 = outcode((x0, y0), window)
    code1 = outcode((x1, y1), window)
    while True:
        if not (code0 | code1):
            return (x0, y0), (x1, y1)
        if code0 & code1:
            return None
        outside = code0 if code0 else code1
        if outside & TOP:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif outside & BOTTOM:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif outside & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        else:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin
        if outside == code0:
            x0, y0 = x, y
            code0 = outcode((x0, y0), window)
        else:
            x1, y1 = x, y
            code1 = outcode((x1, y1), window)


def agrees_with_sampling(window, steps=200):
    """Vergleicht das Clipping mit einer Abtastung der Strecke.

    Für eine Reihe von Strecken wird geprüft, dass der zugeschnittene Teil
    genau die abgetasteten Punkte innerhalb des Fensters überdeckt.

    Returns:
        Wahr, wenn beide Wege für alle geprüften Strecken übereinstimmen.
    """
    xmin, ymin, xmax, ymax = window
    segments = [((-5, 5), (15, 5)), ((-5, -5), (15, 15)), ((1, 1), (9, 9)),
                ((-5, -5), (-1, -1)), ((5, -5), (5, 15)), ((-1, 11), (11, -1))]
    for segment in segments:
        clipped = cohen_sutherland(segment, window)
        (x0, y0), (x1, y1) = segment
        inside = []
        for step in range(steps + 1):
            position = step / steps
            x = x0 + (x1 - x0) * position
            y = y0 + (y1 - y0) * position
            if xmin <= x <= xmax and ymin <= y <= ymax:
                inside.append(position)
        if not inside:
            if clipped is not None:
                return False
            continue
        if clipped is None:
            return False
        length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        if length == 0:
            continue
        start = (((clipped[0][0] - x0) ** 2
                  + (clipped[0][1] - y0) ** 2) ** 0.5) / length
        end = (((clipped[1][0] - x0) ** 2
                + (clipped[1][1] - y0) ** 2) ** 0.5) / length
        tolerance = 1.5 / steps
        if abs(start - min(inside)) > tolerance:
            return False
        if abs(end - max(inside)) > tolerance:
            return False
    return True


def bresenham(start, end):
    """Rastert eine Strecke mit ganzzahliger Arithmetik.

    Der Algorithmus führt einen Fehlerterm mit und entscheidet je Schritt,
    ob die Nebenachse mitgezogen wird. Multiplikationen und Divisionen
    kommen nicht vor.

    Returns:
        Liste der Pixel von ``start`` bis ``end`` einschliesslich.
    """
    x0, y0 = int(start[0]), int(start[1])
    x1, y1 = int(end[0]), int(end[1])
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    error = dx + dy
    pixels = []
    while True:
        pixels.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pixels
        doubled = 2 * error
        if doubled >= dy:
            error += dy
            x0 += step_x
        if doubled <= dx:
            error += dx
            y0 += step_y


def largest_deviation(start, end):
    """Misst den grössten Abstand eines Pixels zur idealen Strecke.

    Returns:
        Der grösste senkrechte Abstand; er bleibt unter einem halben Pixel.
    """
    x0, y0 = start
    x1, y1 = end
    length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if length == 0:
        return 0.0
    worst = 0.0
    for x, y in bresenham(start, end):
        distance = abs((y1 - y0) * x - (x1 - x0) * y + x1 * y0 - y1 * x0)
        worst = max(worst, distance / length)
    return worst
