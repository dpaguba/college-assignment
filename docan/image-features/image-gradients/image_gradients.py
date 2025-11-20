"""Bildgradienten mit dem Sobel-Operator."""

import numpy as np

SOBEL_H = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)

SOBEL_V = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)


def cross_correlate(image, kernel):
    """Führt die Kreuzkorrelation von der Folie aus.

    Gerechnet wird die Summe über K(s,t) mal I(x+s, y+t), also ohne das
    Spiegeln des Kerns, das die Faltung vornimmt. Bei den
    antisymmetrischen Sobelmasken ist das kein Detail: die Faltung
    liefert dasselbe mit umgekehrtem Vorzeichen, und damit zeigt der
    Gradient in die Gegenrichtung.

    Am Rand wird der Randwert fortgesetzt, damit das Ergebnis dieselbe
    Grösse behält wie das Bild.

    Args:
        image: das Bild als zweidimensionales Feld.
        kernel: der Kern mit ungerader Kantenlänge.

    Returns:
        Das Ergebnis in der Grösse des Bildes.

    Raises:
        ValueError: bei einem Kern mit gerader Kantenlänge oder einem
            Kern, der grösser ist als das Bild.
    """
    field = np.asarray(image, dtype=float)
    mask = np.asarray(kernel, dtype=float)
    if field.ndim != 2 or mask.ndim != 2:
        raise ValueError("Bild und Kern sind zweidimensional")
    if mask.shape[0] % 2 == 0 or mask.shape[1] % 2 == 0:
        raise ValueError("der Kern braucht eine ungerade Kantenlänge")
    if mask.shape[0] > field.shape[0] or mask.shape[1] > field.shape[1]:
        raise ValueError("der Kern ist grösser als das Bild")
    high = mask.shape[0] // 2
    wide = mask.shape[1] // 2
    padded = np.pad(field, ((high, high), (wide, wide)), mode="edge")
    result = np.zeros_like(field)
    for row in range(mask.shape[0]):
        for column in range(mask.shape[1]):
            weight = mask[row][column]
            if weight != 0.0:
                result += weight * padded[row:row + field.shape[0],
                                          column:column + field.shape[1]]
    return result


def gradients(image):
    """Rechnet Gradienten, Magnituden und Orientierungen aus.

    Gx entsteht aus der senkrechten Maske und antwortet auf senkrechte
    Kanten, Gy aus der waagerechten. Die Orientierung ist der Arkustangens
    des Verhältnisses und liegt damit in einem halben Kreis: der
    Gradient einer hellen Kante auf dunklem Grund und einer dunklen auf
    hellem Grund bekommt denselben Winkel.

    Returns:
        Abbildung mit ``x``, ``y``, ``magnitude`` und ``direction``.

    Raises:
        ValueError: bei einem zu kleinen Bild.
    """
    field = np.asarray(image, dtype=float)
    horizontal = cross_correlate(field, SOBEL_V)
    vertical = cross_correlate(field, SOBEL_H)
    magnitude = np.sqrt(horizontal ** 2 + vertical ** 2)
    direction = np.degrees(np.arctan2(vertical, horizontal))
    direction = np.where(direction > 90.0, direction - 180.0, direction)
    direction = np.where(direction <= -90.0, direction + 180.0, direction)
    return {"x": horizontal, "y": vertical, "magnitude": magnitude,
            "direction": direction}


def correlation_is_not_convolution():
    """Misst den Unterschied zwischen beiden Rechenarten.

    Auf einer steigenden Rampe liefert die Kreuzkorrelation mit der
    senkrechten Sobelmaske das Achtfache der Steigung, die Faltung
    dasselbe mit umgekehrtem Vorzeichen. Wer die beiden verwechselt,
    bekommt eine Kantenrichtung, die um einen halben Kreis verdreht ist,
    und merkt es nicht, solange nur die Magnitude betrachtet wird.

    Returns:
        Abbildung mit beiden Werten.
    """
    ramp = np.tile(np.arange(9, dtype=float), (9, 1))
    correlated = cross_correlate(ramp, SOBEL_V)[4][4]
    convolved = cross_correlate(ramp, SOBEL_V[::-1, ::-1])[4][4]
    return {"cross correlation": float(correlated),
            "convolution": float(convolved),
            "angle between them": 180.0,
            "why it hides": "in der Magnitude ist der Unterschied nicht "
                            "zu sehen"}


def what_the_gradient_shows_on_a_document():
    """Sagt, warum Gradienten auf Dokumentenbildern arbeiten.

    Ein Dokumentenbild besteht fast nur aus Kanten: Schriftzüge sind
    dunkle Striche auf hellem Grund, und deren Richtung und Stärke
    tragen die Form des Buchstabens. Der Grauwert selbst trägt wenig,
    weil er von Beleuchtung, Papier und Alter abhängt und von Seite zu
    Seite schwankt.
    """
    return {"what carries the shape": "Richtung und Stärke der Kanten",
            "what does not": "der Grauwert, der von Papier und "
                             "Beleuchtung abhängt",
            "consequence": "Verfahren auf Gradienten überstehen einen "
                           "Wechsel der Vorlage besser"}
