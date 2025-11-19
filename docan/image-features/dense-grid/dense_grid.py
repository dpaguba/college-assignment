"""Das regelmässige Gitter von Ausschnitten."""

import numpy as np


def points(shape, step=8, size=16):
    """Nennt die Mittelpunkte der Ausschnitte.

    Das Gitter beginnt so weit innen, dass der erste Ausschnitt noch
    ganz im Bild liegt, und endet ebenso. Damit ist jeder Ausschnitt
    vollständig, und es muss nichts am Rand aufgefüllt werden.

    Args:
        shape: die Grösse des Bildes als Paar.
        step: der Abstand zwischen zwei Mittelpunkten.
        size: die Kantenlänge eines Ausschnitts.

    Returns:
        Liste der Mittelpunkte als Paare aus Zeile und Spalte.

    Raises:
        ValueError: bei einem nicht positiven Schritt, einer nicht
            positiven Grösse oder einem Ausschnitt, der nicht ins Bild
            passt.
    """
    if step <= 0 or size <= 0:
        raise ValueError("Schritt und Grösse müssen positiv sein")
    high, wide = shape
    half = size // 2
    if size > high or size > wide:
        raise ValueError("der Ausschnitt ist grösser als das Bild")
    return [(row, column)
            for row in range(half, high - half + 1, step)
            for column in range(half, wide - half + 1, step)]


def patches(image, step=8, size=16):
    """Schneidet die Ausschnitte aus dem Bild.

    Raises:
        ValueError: wie bei ``points``.
    """
    field = np.asarray(image, dtype=float)
    half = size // 2
    return [field[row - half:row - half + size,
                  column - half:column - half + size]
            for row, column in points(field.shape, step, size)]


def coverage(shape, step=8, size=16):
    """Misst, wie oft jeder Bildpunkt von einem Ausschnitt getroffen wird.

    Bei einem Schritt kleiner als die Kantenlänge überlappen sich die
    Ausschnitte, und jeder Bildpunkt geht mehrfach in die Darstellung
    ein. Das ist der übliche Fall und der Grund, warum ein feineres
    Gitter nicht nur mehr, sondern auch stabilere Deskriptoren liefert.

    Raises:
        ValueError: wie bei ``points``.
    """
    high, wide = shape
    counted = np.zeros((high, wide))
    half = size // 2
    for row, column in points(shape, step, size):
        counted[row - half:row - half + size,
                column - half:column - half + size] += 1.0
    return {"minimum": float(counted.min()), "maximum": float(counted.max()),
            "mean": float(counted.mean()),
            "overlapping": step < size,
            "points": len(points(shape, step, size))}


def why_dense_and_not_keypoints():
    """Sagt, warum auf Dokumentenbildern dicht abgetastet wird.

    Verfahren zur Auswahl markanter Punkte suchen Ecken und Blobs. Eine
    Handschrift besteht aus Strichen von ähnlicher Stärke und liefert
    davon wenige und unzuverlässige; zwei Abbilder desselben Worts
    ergäben verschiedene Punktmengen, und die Darstellungen wären nicht
    mehr vergleichbar.

    Ein festes Gitter liefert dagegen für jedes Bild gleich viele
    Deskriptoren an vergleichbaren Stellen. Der Preis ist, dass auch
    leere Stellen beschrieben werden, und die liefern den Nullvektor.
    """
    return {"why": "auf Schrift findet ein Punktdetektor wenige und "
                   "unzuverlässige Stellen",
            "what the grid gives": "gleich viele Deskriptoren an "
                                   "vergleichbaren Stellen",
            "the price": "auch leere Stellen werden beschrieben",
            "what they give": "den Nullvektor"}
