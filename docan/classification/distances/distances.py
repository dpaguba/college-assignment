"""Die drei Bewertungsmasse zwischen Termvektoren."""

import numpy as np

MEASURES = ("euclidean", "cityblock", "cosine")


def _pair(first, second):
    """Prüft zwei Vektoren und gibt sie als Felder zurück.

    Raises:
        ValueError: bei verschiedenen Längen oder leeren Vektoren.
    """
    one = np.asarray(first, dtype=float)
    two = np.asarray(second, dtype=float)
    if one.shape != two.shape or one.size == 0:
        raise ValueError("die Vektoren müssen gleich lang und nicht leer "
                         "sein")
    return one, two


def euclidean(first, second):
    """Der euklidische Abstand.

    Er misst die Strecke im Raum und wächst mit der Länge der Dokumente.
    Zwei Texte über dasselbe Thema, von denen einer zehnmal so lang ist,
    liegen weit auseinander, obwohl sie dasselbe sagen.

    Raises:
        ValueError: bei verschiedenen Längen.
    """
    one, two = _pair(first, second)
    return float(np.sqrt(np.sum((one - two) ** 2)))


def cityblock(first, second):
    """Der Cityblock-Abstand.

    Er summiert die Beträge der Unterschiede. Gegenüber dem euklidischen
    Abstand gewichtet er einen einzelnen grossen Unterschied schwächer,
    weil er ihn nicht quadriert.

    Raises:
        ValueError: bei verschiedenen Längen.
    """
    one, two = _pair(first, second)
    return float(np.sum(np.abs(one - two)))


def cosine(first, second):
    """Der Kosinusabstand.

    Er misst den Winkel und nicht die Länge, und genau deshalb wird er
    für Dokumente genommen: die Länge eines Textes soll das Ergebnis
    nicht bestimmen. Der Nullvektor hat keine Richtung, für ihn ist das
    Mass nicht erklärt.

    Raises:
        ValueError: bei verschiedenen Längen oder einem Nullvektor.
    """
    one, two = _pair(first, second)
    lengths = np.linalg.norm(one) * np.linalg.norm(two)
    if lengths == 0.0:
        raise ValueError("der Nullvektor hat keine Richtung")
    return float(1.0 - np.dot(one, two) / lengths)


def distance_matrix(rows, columns, measure="euclidean"):
    """Rechnet alle Abstände zwischen zwei Mengen von Punkten aus.

    Raises:
        ValueError: bei einem unbekannten Mass.
    """
    if measure not in MEASURES:
        raise ValueError("unbekanntes Mass: %s" % measure)
    chosen = {"euclidean": euclidean, "cityblock": cityblock,
              "cosine": cosine}[measure]
    return np.array([[chosen(row, column) for column in columns]
                     for row in rows])


def cosine_breaks_the_triangle():
    """Zeigt, dass der Kosinusabstand keine Metrik ist.

    Für die drei Punkte (1,0), (1,1) und (0,1) beträgt der Abstand über
    die Mitte zweimal 1 - 1/√2, zusammen etwa 0.586, der direkte Abstand
    aber 1. Der Umweg ist kürzer als der direkte Weg, und damit ist die
    Dreiecksungleichung verletzt.

    Das ist kein Grund, das Mass zu verwerfen; es heisst nur, dass
    Verfahren, die sich auf die Dreiecksungleichung verlassen, mit ihm
    nicht sicher arbeiten.

    Returns:
        Abbildung mit beiden Wegen.
    """
    first, middle, last = [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]
    over = cosine(first, middle) + cosine(middle, last)
    direct = cosine(first, last)
    return {"through the middle": over, "direct": direct,
            "is a metric": over >= direct,
            "what it costs": "Verfahren, die auf der "
                             "Dreiecksungleichung aufbauen, gelten nicht"}


def which_one_for_documents():
    """Sagt, warum für Dokumente der Kosinusabstand genommen wird.

    Ein Termvektor zählt Wörter, also wächst er mit der Länge des Textes.
    Der euklidische und der Cityblock-Abstand messen diese Länge mit; der
    Kosinusabstand nicht. Wer stattdessen relative Häufigkeiten verwendet,
    nimmt die Länge schon vorher heraus, und dann liegen die drei Masse
    wieder näher beieinander.
    """
    return {"the problem": "ein Termvektor wächst mit der Länge des "
                           "Textes",
            "cosine": "misst den Winkel und nicht die Länge",
            "the other way": "relative Häufigkeiten nehmen die Länge "
                             "vorher heraus",
            "then": "die drei Masse liegen näher beieinander"}
