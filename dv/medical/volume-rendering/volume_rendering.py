"""Direkte Volumenvisualisierung durch Strahlverfolgung."""

import math


def example_volume(size=4):
    """Baut einen kleinen Datensatz mit einer Kugel aus dichtem Material.

    Returns:
        Verschachtelte Liste mit den Dichten, indiziert als
        ``volume[depth][row][column]``.
    """
    centre = (size - 1) / 2.0
    volume = []
    for depth in range(size):
        plane = []
        for row in range(size):
            line = []
            for column in range(size):
                distance = math.sqrt((depth - centre) ** 2
                                     + (row - centre) ** 2
                                     + (column - centre) ** 2)
                line.append(max(0.0, 1.0 - distance / (size / 2.0)))
            plane.append(line)
        volume.append(plane)
    return volume


def default_transfer(density):
    """Bildet eine Dichte auf Farbe und Deckkraft ab.

    Returns:
        Tupel (rot, grün, blau, Deckkraft).
    """
    opacity = min(1.0, max(0.0, density))
    return (opacity, opacity * 0.8, opacity * 0.6, opacity * 0.5)


def cast_ray(volume, pixel, transfer=None, threshold=None):
    """Verfolgt einen Strahl von vorn nach hinten durch das Volumen.

    Jede Probe trägt mit ihrer Deckkraft bei, gewichtet mit dem, was der
    Strahl noch durchlässt. Sobald nichts mehr durchkommt, ist der Rest
    ohne Wirkung.

    Args:
        volume: die Dichten.
        pixel: Paar (Zeile, Spalte).
        transfer: Abbildung von Dichte auf Farbe und Deckkraft.
        threshold: Deckkraft, ab der abgebrochen wird.

    Returns:
        Abbildung mit ``colour``, ``opacity`` und ``samples``.

    Raises:
        IndexError: wenn das Bildelement ausserhalb liegt.
    """
    if transfer is None:
        transfer = default_transfer
    row, column = pixel
    colour = [0.0, 0.0, 0.0]
    opacity = 0.0
    used = 0
    for plane in volume:
        red, green, blue, alpha = transfer(plane[row][column])
        remaining = 1.0 - opacity
        colour[0] += remaining * alpha * red
        colour[1] += remaining * alpha * green
        colour[2] += remaining * alpha * blue
        opacity += remaining * alpha
        used += 1
        if threshold is not None and opacity >= threshold:
            break
    return {"colour": tuple(colour), "opacity": opacity, "samples": used}


def cast_ray_back_to_front(volume, pixel, transfer=None):
    """Verfolgt denselben Strahl von hinten nach vorn.

    Die hintere Reihenfolge braucht keinen Rest mitzuführen: jede Probe
    überdeckt, was bisher zusammengesetzt wurde.
    """
    if transfer is None:
        transfer = default_transfer
    row, column = pixel
    colour = [0.0, 0.0, 0.0]
    opacity = 0.0
    for plane in reversed(volume):
        red, green, blue, alpha = transfer(plane[row][column])
        for axis, value in enumerate((red, green, blue)):
            colour[axis] = alpha * value + (1 - alpha) * colour[axis]
        opacity = alpha + (1 - alpha) * opacity
    return {"colour": tuple(colour), "opacity": opacity}


def matches_absorption(alpha=0.2, count=8):
    """Prüft die Zusammensetzung an der geschlossenen Formel.

    Bei gleicher Deckkraft je Probe muss die aufgesammelte Deckkraft nach
    n Proben 1 − (1 − α)ⁿ betragen; das ist das Absorptionsgesetz in
    diskreter Form.
    """
    volume = [[[1.0]] for _ in range(count)]
    result = cast_ray(volume, (0, 0),
                      transfer=lambda density: (1.0, 1.0, 1.0, alpha))
    expected = 1.0 - (1.0 - alpha) ** count
    return abs(result["opacity"] - expected) < 1e-12


def orders_agree():
    """Prüft, dass beide Durchlaufrichtungen dasselbe Bild ergeben."""
    volume = example_volume()
    for row in range(len(volume[0])):
        for column in range(len(volume[0][0])):
            front = cast_ray(volume, (row, column))
            back = cast_ray_back_to_front(volume, (row, column))
            for a, b in zip(front["colour"], back["colour"]):
                if abs(a - b) > 1e-9:
                    return False
            if abs(front["opacity"] - back["opacity"]) > 1e-9:
                return False
    return True


def transfer_function_matters():
    """Zeigt, dass die Transferfunktion entscheidet, was sichtbar wird.

    Eine Funktion hebt die dichten Bereiche hervor, die andere die
    schwachen; dasselbe Volumen ergibt zwei verschiedene Bilder.

    Returns:
        Abbildung mit der Deckkraft beider Einstellungen.
    """
    volume = example_volume()

    def bone(density):
        """Zeigt nur, was dichter als die halbe Skala ist."""
        return (1.0, 1.0, 1.0, 0.9 if density > 0.5 else 0.0)

    def tissue(density):
        """Zeigt das schwache Gewebe und blendet das dichte aus."""
        return (0.8, 0.5, 0.5, 0.3 if 0.0 < density <= 0.5 else 0.0)

    return {"bone": cast_ray(volume, (1, 1), transfer=bone)["opacity"],
            "tissue": cast_ray(volume, (1, 1), transfer=tissue)["opacity"]}


def maximum_intensity(volume, pixel, reverse=False):
    """Gibt den grössten Dichtewert entlang eines Strahls zurück.

    Das Verfahren setzt nichts zusammen, sondern wählt aus; deshalb ist es
    von der Reihenfolge unabhängig, verliert aber jede Tiefeninformation.
    """
    row, column = pixel
    planes = list(reversed(volume)) if reverse else volume
    return max(plane[row][column] for plane in planes)


def early_termination_is_safe(threshold=0.99):
    """Prüft, wie stark der Abbruch das Bild verändert.

    Returns:
        Wahr, wenn die Farbe um weniger als ein Prozent abweicht.
    """
    volume = example_volume(8)
    for row in range(len(volume[0])):
        for column in range(len(volume[0][0])):
            full = cast_ray(volume, (row, column))
            cut = cast_ray(volume, (row, column), threshold=threshold)
            for a, b in zip(full["colour"], cut["colour"]):
                if abs(a - b) > 0.01:
                    return False
    return True


def acceleration():
    """Nennt die Beschleunigungstechniken der Vorlesung."""
    return ["early ray termination", "empty space skipping",
            "adaptive sampling", "precomputed gradients"]
