"""Vektorquantisierung: Median-Schnitt und Hyper-Octree."""

import math


def _distance(first, second):
    """Euklidischer Abstand zweier Farbvektoren."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def _average(colours):
    """Mittelt eine nichtleere Menge von Farbvektoren komponentenweise."""
    dimension = len(colours[0])
    return tuple(sum(colour[axis] for colour in colours) / len(colours)
                 for axis in range(dimension))


def median_cut(colours, size):
    """Bestimmt eine Palette nach dem Median-Schnitt-Verfahren.

    Die Farbmenge wird wiederholt entlang der Achse mit der grössten
    Ausdehnung am Median geteilt, bis die gewünschte Zahl von Zellen
    erreicht ist; jede Zelle liefert ihren Mittelwert.

    Args:
        colours: die vorkommenden Farben.
        size: gewünschte Palettengrösse.

    Returns:
        Liste der Palettenfarben.

    Raises:
        ValueError: wenn die Grösse nicht zwischen eins und der Zahl der
            Farben liegt.
    """
    if not 1 <= size <= len(colours):
        raise ValueError("Palettengroesse passt nicht zu den Daten")
    boxes = [list(colours)]
    while len(boxes) < size:
        widest = max(boxes, key=_spread)
        if _spread(widest) == 0:
            break
        axis = _widest_axis(widest)
        widest.sort(key=lambda colour: colour[axis])
        middle = len(widest) // 2
        boxes.remove(widest)
        boxes.append(widest[:middle])
        boxes.append(widest[middle:])
    return [_average(box) for box in boxes if box]


def _spread(box):
    """Grösste Ausdehnung einer Zelle über alle Achsen."""
    if not box:
        return 0
    return max(max(colour[axis] for colour in box)
               - min(colour[axis] for colour in box)
               for axis in range(len(box[0])))


def _widest_axis(box):
    """Achse, entlang der eine Zelle am weitesten ausgedehnt ist."""
    return max(range(len(box[0])),
               key=lambda axis: max(colour[axis] for colour in box)
               - min(colour[axis] for colour in box))


def octree_buckets(colours, depth):
    """Teilt den Farbwürfel nach den führenden Bits der Kanäle auf.

    Args:
        colours: Farben mit Kanälen von 0 bis 255.
        depth: Zahl der betrachteten führenden Bits.

    Returns:
        Abbildung vom Zellschlüssel auf die Farben darin.

    Raises:
        ValueError: bei einer Tiefe ausserhalb von 1 bis 8.
    """
    if not 1 <= depth <= 8:
        raise ValueError("Tiefe liegt ausserhalb von 1 bis 8")
    buckets = {}
    for colour in colours:
        key = tuple(channel >> (8 - depth) for channel in colour)
        buckets.setdefault(key, []).append(colour)
    return buckets


def quantise(colours, palette):
    """Ersetzt jede Farbe durch die nächstgelegene Palettenfarbe."""
    return [min(palette, key=lambda entry: _distance(colour, entry))
            for colour in colours]


def error(colours, palette):
    """Mittlerer quadrierter Abstand zur zugeordneten Palettenfarbe."""
    if not colours:
        raise ValueError("keine Farben")
    return sum(_distance(colour, entry) ** 2
               for colour, entry in zip(colours, quantise(colours, palette))
               ) / len(colours)


def compare_with_uniform():
    """Vergleicht den Median-Schnitt mit einem gleichmässigen Gitter.

    Die Farben häufen sich in einer Ecke des Würfels; das gleichmässige
    Gitter verteilt seine Palettenpunkte trotzdem über den ganzen Raum.

    Returns:
        Abbildung mit dem mittleren quadrierten Fehler beider Paletten.
    """
    colours = [(index, index, index) for index in range(0, 40, 4)]
    colours += [(240 + index, 10, 10) for index in range(0, 15, 3)]
    adaptive = median_cut(colours, 4)
    uniform = [(step, step, step) for step in (32, 96, 160, 224)]
    return {"median cut": error(colours, adaptive),
            "uniform": error(colours, uniform)}
