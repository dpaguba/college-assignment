"""Kovarianzmatrix und Hauptkomponentenanalyse."""

import numpy as np


def _points(data):
    """Prüft eine Punktmenge und gibt sie als Feld zurück.

    Raises:
        ValueError: bei einer leeren oder falsch geformten Menge.
    """
    field = np.asarray(data, dtype=float)
    if field.size == 0 or field.ndim != 2:
        raise ValueError("leere oder falsch geformte Punktmenge")
    return field


def mean(data):
    """Schätzt den Mittelwert der Beispieldaten.

    Er ist der Ursprung des neuen Koordinatensystems.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    return _points(data).mean(axis=0)


def covariance(data):
    """Schätzt die Kovarianzmatrix.

    Auf der Hauptdiagonale stehen die Varianzen, daneben die
    Kovarianzen; die Matrix ist symmetrisch, weil cov(x,y) gleich
    cov(y,x) ist. Geteilt wird durch N und nicht durch N-1, weil die
    Eigenwerte dann genau die Varianzen entlang der neuen Achsen sind.

    Raises:
        ValueError: bei weniger als zwei Punkten.
    """
    field = _points(data)
    if field.shape[0] < 2:
        raise ValueError("mindestens zwei Punkte")
    centred = field - field.mean(axis=0)
    return (centred.T @ centred) / field.shape[0]


def principal_axes(data):
    """Bestimmt das neue Koordinatensystem aus den Beispieldaten.

    Die Achsen sind die Eigenvektoren der Kovarianzmatrix, die Eigenwerte
    sind die Varianzen entlang dieser Achsen. Weil die Matrix symmetrisch
    ist, sind die Eigenwerte reell und die Eigenvektoren orthogonal; das
    ist der Grund, warum sich überhaupt ein Koordinatensystem daraus
    bauen lässt.

    Returns:
        Abbildung mit ``axes``, ``eigenvalues`` und ``mean``.

    Raises:
        ValueError: bei weniger als zwei Punkten.
    """
    matrix = covariance(data)
    values, vectors = np.linalg.eigh(matrix)
    order = np.argsort(values)[::-1]
    return {"axes": vectors[:, order].T, "eigenvalues": values[order],
            "mean": mean(data), "rank": int(np.sum(values[order] > 1e-12))}


def transform(data, report=None):
    """Rechnet die Punkte in das neue Koordinatensystem um.

    Erst wird der Mittelwert abgezogen, dann auf die Achsen projiziert.
    Danach sind die Koordinaten unkorreliert, denn die Kovarianzmatrix
    der gedrehten Daten ist die Diagonalmatrix der Eigenwerte.

    Raises:
        ValueError: bei weniger als zwei Punkten.
    """
    field = _points(data)
    report = principal_axes(field) if report is None else report
    return (field - report["mean"]) @ report["axes"].T


def inverse(turned, report):
    """Rechnet Punkte aus dem neuen System zurück.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    field = _points(turned)
    return field @ report["axes"] + report["mean"]


def what_the_rotation_does_not_change():
    """Nennt, was die Drehung erhält.

    Die Summe der Varianzen über alle Achsen, also die Spur der
    Kovarianzmatrix, und die Abstände zwischen den Punkten. Die Drehung
    verteilt die Streuung nur anders auf die Achsen; sie erzeugt und
    vernichtet nichts. Erst das Weglassen von Achsen kostet etwas.
    """
    return {"kept": ["die Summe der Varianzen", "die Abstände zwischen "
                     "den Punkten"],
            "changed": "die Verteilung der Streuung auf die Achsen",
            "what costs": "erst das Weglassen von Achsen"}
