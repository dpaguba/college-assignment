"""Gewichtung von Bag-of-Words Matrizen."""

import numpy as np


def _as_matrix(matrix):
    """Prüft eine Matrix und gibt sie als Fliesskommafeld zurück.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = np.asarray(matrix, dtype=float)
    if field.size == 0 or field.ndim != 2:
        raise ValueError("leere oder falsch geformte Matrix")
    return field


def absolute(matrix):
    """Behält die gezählten Häufigkeiten.

    Sie sind der Ausgangspunkt jeder anderen Gewichtung und für sich
    genommen von der Länge des Dokuments abhängig: ein doppelt so langer
    Text über dasselbe Thema hat doppelt so hohe Werte.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    return _as_matrix(matrix).copy()


def relative(matrix):
    """Normiert jede Zeile auf die Summe eins.

    Damit fällt die Länge des Dokuments heraus, und zwei Texte über
    dasselbe Thema werden vergleichbar, auch wenn einer zehnmal so lang
    ist.

    Raises:
        ValueError: bei einer leeren Matrix oder einem Dokument ohne
            Terme.
    """
    field = _as_matrix(matrix)
    sums = field.sum(axis=1)
    if np.any(sums <= 0):
        raise ValueError("ein Dokument enthält keinen Term des Vokabulars")
    return field / sums[:, None]


def document_frequency(matrix):
    """Zählt, in wie vielen Dokumenten jeder Term vorkommt.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = _as_matrix(matrix)
    return (field > 0).sum(axis=0).astype(float)


def inverse_document_frequency(matrix, smoothed=False):
    """Gewichtet Terme nach ihrer Diskriminativität.

    Ein Term, der in jedem Dokument steht, trennt nichts und bekommt das
    Gewicht null. Ein seltener Term bekommt ein hohes Gewicht. Das ist
    dieselbe Überlegung wie bei den Stopwords, nur aus den Daten
    geschätzt statt aus einer Liste genommen.

    Args:
        matrix: die Term-Dokument-Matrix.
        smoothed: ob die geglättete Form log(1 + N/df) verwendet wird.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = _as_matrix(matrix)
    frequency = document_frequency(field)
    count = float(field.shape[0])
    safe = np.where(frequency > 0, frequency, 1.0)
    if smoothed:
        return np.log(1.0 + count / safe)
    return np.log(count / safe)


def tf_idf(matrix, smoothed=False):
    """Verbindet die relative Häufigkeit mit der Diskriminativität.

    Raises:
        ValueError: bei einer leeren Matrix oder einem leeren Dokument.
    """
    return relative(matrix) * inverse_document_frequency(matrix, smoothed)


def why_the_variant_matters():
    """Zeigt, was die Wahl der idf-Form entscheidet.

    In der schlichten Form log(N/df) bekommt ein Term, der in jedem
    Dokument steht, das Gewicht null und verschwindet vollständig. In der
    geglätteten Form log(1 + N/df) behält er ein kleines Gewicht. Die
    Entscheidung ist nicht kosmetisch: im ersten Fall kann ein Dokument,
    das nur aus solchen Termen besteht, den Nullvektor bekommen, und der
    hat zu jedem anderen Vektor denselben Kosinusabstand.

    Returns:
        Abbildung mit beiden Formen und ihren Folgen.
    """
    matrix = [[1.0, 1.0], [1.0, 3.0]]
    plain = tf_idf(matrix)
    smooth = tf_idf(matrix, smoothed=True)
    return {"plain": {"formula": "log(N/df)",
                      "weight of a term in every document": 0.0,
                      "first row": [round(value, 6) for value
                                    in plain[0]]},
            "smoothed": {"formula": "log(1 + N/df)",
                         "first row": [round(value, 6) for value
                                       in smooth[0]]},
            "consequence": "in der schlichten Form kann ein Dokument zum "
                           "Nullvektor werden",
            "why that hurts": "der Kosinusabstand ist für den "
                              "Nullvektor nicht definiert"}
