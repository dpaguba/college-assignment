"""Reduktion auf die Achsen mit der grössten Varianz."""

import numpy as np


def _points(data):
    """Prüft eine Punktmenge.

    Raises:
        ValueError: bei einer leeren oder zu kleinen Menge.
    """
    field = np.asarray(data, dtype=float)
    if field.ndim != 2 or field.shape[0] < 2:
        raise ValueError("mindestens zwei Punkte in einer Matrix")
    return field


def principal_axes(data):
    """Bestimmt Achsen und Eigenwerte der Beispieldaten.

    Raises:
        ValueError: bei einer zu kleinen Menge.
    """
    field = _points(data)
    centre = field.mean(axis=0)
    centred = field - centre
    matrix = (centred.T @ centred) / field.shape[0]
    values, vectors = np.linalg.eigh(matrix)
    order = np.argsort(values)[::-1]
    return {"axes": vectors[:, order].T, "eigenvalues": values[order],
            "mean": centre}


def reduce(data, k):
    """Projiziert auf die k stärksten Achsen und misst den Verlust.

    Der mittlere quadratische Rekonstruktionsfehler ist genau die Summe
    der weggelassenen Eigenwerte. Damit ist der Preis der Reduktion
    keine Schätzung, sondern ablesbar, bevor man sie durchführt.

    Args:
        data: die Punktmenge.
        k: die Anzahl der behaltenen Achsen.

    Returns:
        Abbildung mit den reduzierten Daten, der Rückrechnung und dem
        Fehler.

    Raises:
        ValueError: bei einem k ausserhalb von eins bis zur Dimension.
    """
    field = _points(data)
    if not 1 <= k <= field.shape[1]:
        raise ValueError("k liegt zwischen eins und der Dimension")
    report = principal_axes(field)
    axes = report["axes"][:k]
    centred = field - report["mean"]
    reduced = centred @ axes.T
    rebuilt = reduced @ axes + report["mean"]
    error = float(np.mean(np.sum((field - rebuilt) ** 2, axis=1)))
    return {"reduced": reduced, "reconstructed": rebuilt,
            "reconstruction error": error,
            "discarded eigenvalues": report["eigenvalues"][k:],
            "k": k}


def variance_kept(data, k):
    """Nennt den Anteil der Varianz, den k Achsen behalten.

    Raises:
        ValueError: bei einem unzulässigen k.
    """
    field = _points(data)
    if not 1 <= k <= field.shape[1]:
        raise ValueError("k liegt zwischen eins und der Dimension")
    values = principal_axes(field)["eigenvalues"]
    total = values.sum()
    if total <= 0.0:
        raise ValueError("die Daten streuen nicht")
    return float(values[:k].sum() / total)


def how_to_choose_k(data):
    """Stellt zusammen, woran k üblicherweise festgemacht wird.

    Die Folie sagt, k werde häufig empirisch bestimmt, und lässt offen,
    woran. In der Praxis sind es drei Dinge: ein Knick im Verlauf der
    Eigenwerte, ein Anteil der behaltenen Varianz, oder die Fehlerrate
    der nachfolgenden Aufgabe. Nur das dritte misst, worauf es ankommt,
    und nur das dritte braucht die Aufgabe selbst.

    Returns:
        Abbildung mit dem Verlauf und den drei Regeln.

    Raises:
        ValueError: bei einer zu kleinen Menge.
    """
    field = _points(data)
    values = principal_axes(field)["eigenvalues"]
    total = values.sum()
    running = np.cumsum(values) / total if total > 0 else values
    return {"scree": [float(value) for value in values],
            "cumulative share": [float(value) for value in running],
            "rules": ["ein Knick im Verlauf der Eigenwerte",
                      "ein fester Anteil der behaltenen Varianz",
                      "die Fehlerrate der eigentlichen Aufgabe"],
            "which one measures the point": "nur die dritte"}


def why_variance_is_not_information():
    """Warnt vor der stillen Gleichsetzung auf der Folie.

    Die Reduktion behält die Richtungen mit der grössten Varianz. Das ist
    nur dann die relevante Information, wenn die Aufgabe an der Streuung
    hängt. Trennt ein Merkmal zwei Klassen sauber, streut aber wenig, so
    fliegt es zuerst heraus. Die Hauptkomponentenanalyse kennt die
    Kategorien nicht und kann darauf keine Rücksicht nehmen.
    """
    return {"what it keeps": "die Richtungen mit der grössten Varianz",
            "what that assumes": "dass die Aufgabe an der Streuung hängt",
            "the counterexample": "ein Merkmal, das zwei Klassen trennt "
                                  "und wenig streut, fliegt zuerst heraus",
            "why": "das Verfahren kennt die Kategorien nicht"}
