"""SIFT-Deskriptoren aus Zellen mit Teilhistogrammen."""

import numpy as np

SOBEL_H = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)

SOBEL_V = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)


def _correlate(field, mask):
    """Kreuzkorrelation mit fortgesetztem Rand."""
    high = mask.shape[0] // 2
    wide = mask.shape[1] // 2
    padded = np.pad(field, ((high, high), (wide, wide)), mode="edge")
    result = np.zeros_like(field)
    for row in range(mask.shape[0]):
        for column in range(mask.shape[1]):
            result += mask[row][column] * padded[
                row:row + field.shape[0], column:column + field.shape[1]]
    return result


def orientations(patch):
    """Rechnet Magnituden und Richtungen über den ganzen Kreis aus.

    Anders als die Folie, die den Arkustangens des Verhältnisses nennt,
    wird hier über beide Vorzeichen gerechnet. Der halbe Kreis kann eine
    steigende nicht von einer fallenden Kante unterscheiden, und genau
    dieser Unterschied trägt bei Schrift viel: der linke und der rechte
    Rand eines Strichs bekämen sonst denselben Eintrag.

    Returns:
        Ein Paar aus Magnituden und Richtungen im Bogenmass von null bis
        zwei Pi.
    """
    field = np.asarray(patch, dtype=float)
    horizontal = _correlate(field, SOBEL_V)
    vertical = _correlate(field, SOBEL_H)
    magnitude = np.sqrt(horizontal ** 2 + vertical ** 2)
    angle = np.arctan2(vertical, horizontal) % (2.0 * np.pi)
    return magnitude, angle


def describe(patch, cells=4, bins=8, threshold=0.2, report=False):
    """Bildet einen Ausschnitt auf einen Deskriptor ab.

    Der Ausschnitt wird in Zellen zerlegt, in jeder Zelle werden die
    Richtungen zu einem mit der Magnitude gewichteten Histogramm
    gezählt, und die Histogramme werden aneinandergehängt. Danach wird
    auf die Länge eins normiert, bei einem Schwellwert gekappt und noch
    einmal normiert.

    Das Normieren macht den Deskriptor unabhängig von der
    Beleuchtungsstärke, das Kappen begrenzt den Einfluss einzelner sehr
    starker Kanten. Ein Ausschnitt ohne Gradienten hat keine Richtung
    und bekommt den Nullvektor.

    Args:
        patch: der Ausschnitt.
        cells: die Zellen je Kante.
        bins: die Richtungsklassen je Zelle.
        threshold: der Schwellwert für das Kappen.
        report: ob die Zwischenergebnisse mitgegeben werden.

    Returns:
        Der Deskriptor, oder eine Abbildung mit Zwischenergebnissen.

    Raises:
        ValueError: bei einem zu kleinen Ausschnitt oder unzulässigen
            Zahlen.
    """
    field = np.asarray(patch, dtype=float)
    if cells <= 0 or bins <= 0:
        raise ValueError("Zellen und Klassen müssen positiv sein")
    if field.ndim != 2 or min(field.shape) < cells:
        raise ValueError("der Ausschnitt ist kleiner als das Zellgitter")
    magnitude, angle = orientations(field)
    rows = np.array_split(np.arange(field.shape[0]), cells)
    columns = np.array_split(np.arange(field.shape[1]), cells)
    parts = []
    for row_block in rows:
        for column_block in columns:
            piece = np.ix_(row_block, column_block)
            counted, _ = np.histogram(angle[piece], bins=bins,
                                      range=(0.0, 2.0 * np.pi),
                                      weights=magnitude[piece])
            parts.append(counted)
    descriptor = np.concatenate(parts)
    length = np.linalg.norm(descriptor)
    flat = length < 1e-9
    clipped = 0
    before = 0.0
    if not flat:
        descriptor = descriptor / length
        clipped = int(np.sum(descriptor > threshold))
        descriptor = np.minimum(descriptor, threshold)
        before = float(descriptor.max())
        descriptor = descriptor / np.linalg.norm(descriptor)
    if not report:
        return descriptor
    return {"descriptor": descriptor, "flat": flat, "clipped": clipped,
            "threshold": threshold, "cells": cells, "bins": bins,
            "largest before renormalising": before,
            "largest after renormalising": float(descriptor.max())
            if not flat else 0.0}


def turning_the_patch(size=16, seed=15):
    """Zeigt, dass der Deskriptor die Drehung sieht.

    Derselbe Ausschnitt, um einen Viertelkreis gedreht, ergibt einen
    deutlich anderen Deskriptor. Das ist gewollt: die Form soll erkannt
    werden, und eine gedrehte Form ist eine andere Form. Wer
    Drehinvarianz braucht, richtet den Ausschnitt vorher an seiner
    stärksten Richtung aus; für Schrift auf einer Seite ist das nicht
    nötig, weil die Zeilen ohnehin waagerecht laufen.

    Returns:
        Abbildung mit dem Abstand zwischen beiden Deskriptoren.
    """
    rng = np.random.default_rng(seed)
    field = np.zeros((size, size))
    field[:, size // 2:] = 200.0
    field = field + rng.normal(size=(size, size)) * 2.0
    one = describe(field)
    two = describe(np.rot90(field))
    return {"distance after turning": float(np.linalg.norm(one - two)),
            "largest possible": 2.0,
            "why it is wanted": "eine gedrehte Form ist eine andere Form",
            "when it is not": "wer Drehinvarianz braucht, richtet den "
                              "Ausschnitt vorher aus"}


def what_the_normalisation_buys():
    """Nennt, wogegen die beiden Schritte schützen.

    Das Normieren auf die Länge eins nimmt jeden gleichmässigen
    Helligkeits- und Kontrastunterschied heraus, denn beide skalieren
    alle Gradienten mit demselben Faktor. Das Kappen bei zwei Zehnteln
    begrenzt den Einfluss einzelner sehr starker Kanten, die von einem
    Fleck oder einem Riss stammen können und sonst das ganze Histogramm
    beherrschen würden.

    Der Schwellwert gilt dabei nur bis zur zweiten Normierung. Wird
    gekappt, so schrumpft die Länge des Vektors, und das Teilen durch die
    neue Länge hebt die grössten Einträge wieder über den Schwellwert.
    Der Schritt begrenzt also das Verhältnis zwischen den Einträgen und
    nicht ihren Betrag; wer den Betrag begrenzen will, muss abwechselnd
    kappen und normieren, bis sich nichts mehr ändert.
    """
    report = describe(_example_patch(), report=True)
    return {"unit length": "gegen Helligkeit und Kontrast",
            "clipping": "gegen einzelne sehr starke Kanten",
            "what it cannot fix": "eine Änderung der Form selbst",
            "order": "normieren, kappen, wieder normieren",
            "largest before renormalising":
                report["largest before renormalising"],
            "largest after renormalising":
                report["largest after renormalising"],
            "the threshold holds only until the second normalisation":
                report["largest after renormalising"] > report["threshold"]}


def _example_patch(size=16, seed=15):
    """Ein Ausschnitt mit einer senkrechten Kante und etwas Rauschen."""
    rng = np.random.default_rng(seed)
    field = np.zeros((size, size))
    field[:, size // 2:] = 200.0
    return field + rng.normal(size=(size, size)) * 2.0
