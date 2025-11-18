"""Bag-of-Features und die räumliche Pyramide."""

import numpy as np


def quantise(descriptors, centroids):
    """Ordnet jedem Deskriptor das nächste Wort des Vokabulars zu.

    Raises:
        ValueError: bei einem leeren Vokabular oder Deskriptoren der
            falschen Länge.
    """
    field = np.asarray(descriptors, dtype=float)
    centres = np.asarray(centroids, dtype=float)
    if centres.size == 0 or centres.ndim != 2:
        raise ValueError("leeres Vokabular")
    if field.ndim != 2 or field.shape[1] != centres.shape[1]:
        raise ValueError("Deskriptoren und Vokabular passen nicht "
                         "zusammen")
    measured = ((field[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(measured, axis=1)


def histogram(descriptors, centroids):
    """Zählt, wie oft jedes visuelle Wort vorkommt.

    Das ist die ganze Darstellung: aus einem Bild wird ein Histogramm
    über ein Vokabular, genau wie aus einem Text ein Histogramm über
    Terme wird. Verloren geht dabei dasselbe, nämlich wo im Bild das
    Wort stand.

    Raises:
        ValueError: wie bei ``quantise``.
    """
    centres = np.asarray(centroids, dtype=float)
    counted = np.zeros(len(centres))
    for index in quantise(descriptors, centres):
        counted[index] += 1.0
    return counted


def _cell_of(position, shape, parts):
    """Nennt die Zelle eines Punktes im Gitter.

    Raises:
        ValueError: bei einem Punkt ausserhalb des Bildes.
    """
    row, column = position
    high, wide = shape
    if not (0 <= row < high and 0 <= column < wide):
        raise ValueError("der Punkt liegt ausserhalb des Bildes")
    return (min(parts - 1, int(row * parts / high)),
            min(parts - 1, int(column * parts / wide)))


def spatial_pyramid(descriptors, positions, centroids, shape, levels=2):
    """Baut die Darstellung über mehrere Auflösungen.

    Die unterste Stufe ist das gewöhnliche Histogramm über das ganze
    Bild. Jede weitere teilt das Bild feiner auf und hängt die
    Histogramme der Zellen an. Damit kommt ein Teil der Ortsinformation
    zurück, die das reine Histogramm wegwirft, ohne dass eine
    Segmentierung nötig wäre.

    Args:
        descriptors: die Deskriptoren.
        positions: ihre Mittelpunkte im Bild.
        centroids: das visuelle Vokabular.
        shape: die Grösse des Bildes.
        levels: die Anzahl der Stufen.

    Returns:
        Der aneinandergehängte Vektor.

    Raises:
        ValueError: bei weniger als einer Stufe, unpassend vielen
            Positionen oder einem Punkt ausserhalb des Bildes.
    """
    if levels < 1:
        raise ValueError("mindestens eine Stufe")
    field = np.asarray(descriptors, dtype=float)
    if len(positions) != len(field):
        raise ValueError("zu jedem Deskriptor gehört eine Position")
    centres = np.asarray(centroids, dtype=float)
    words = quantise(field, centres)
    built = []
    for level in range(levels):
        parts = 2 ** level
        cells = np.zeros((parts, parts, len(centres)))
        for word, position in zip(words, positions):
            row, column = _cell_of(position, shape, parts)
            cells[row][column][word] += 1.0
        built.append(cells.reshape(-1))
    return np.concatenate(built)


def layout_matters():
    """Zeigt, was die Pyramide sieht und das Histogramm nicht.

    Zwei Bilder mit denselben Deskriptoren an vertauschten Stellen haben
    dasselbe Histogramm. Auf der zweiten Stufe der Pyramide fallen sie
    auseinander. Für Wortabbilder ist das der Unterschied zwischen zwei
    Wörtern aus denselben Buchstaben in anderer Reihenfolge.

    Returns:
        Abbildung mit beiden Darstellungen.
    """
    centroids = np.array([[0.0, 0.0], [10.0, 0.0]])
    descriptors = np.array([[0.0, 0.0], [10.0, 0.0]])
    shape = (40, 40)
    first = [(10, 10), (30, 30)]
    second = [(30, 30), (10, 10)]
    return {"histogram one": histogram(descriptors, centroids),
            "histogram two": histogram(descriptors, centroids),
            "pyramid one": spatial_pyramid(descriptors, first, centroids,
                                           shape, levels=2),
            "pyramid two": spatial_pyramid(descriptors, second, centroids,
                                           shape, levels=2),
            "what it means": "zwei Wörter aus denselben Buchstaben in "
                             "anderer Reihenfolge"}


def what_the_pyramid_costs():
    """Nennt den Preis der zusätzlichen Stufen.

    Die Länge des Vektors wächst mit der Summe der Zellen, also bei drei
    Stufen auf das Einundzwanzigfache der Vokabulargrösse. Zugleich wird
    jede Zelle dünner besetzt, denn dieselben Deskriptoren verteilen sich
    auf mehr Fächer. Und die Darstellung wird empfindlich gegen
    Verschiebungen: ein Wort, das einen halben Zellenrand weiter steht,
    füllt andere Fächer.
    """
    return {"length": "die Summe der Zellen, bei drei Stufen "
                      "einundzwanzig Histogramme",
            "sparsity": "dieselben Deskriptoren auf mehr Fächer",
            "shift": "eine Verschiebung um einen halben Zellenrand "
                     "ändert die Darstellung",
            "trade": "Ortsinformation gegen Robustheit"}
