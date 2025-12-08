"""Topic-Modell durch Singulärwertzerlegung."""

import numpy as np


def _matrix(data):
    """Prüft eine Matrix.

    Raises:
        ValueError: bei einer leeren oder falsch geformten Matrix.
    """
    field = np.asarray(data, dtype=float)
    if field.size == 0 or field.ndim != 2:
        raise ValueError("leere oder falsch geformte Matrix")
    return field


def decompose(data):
    """Zerlegt die Term-Dokument-Matrix in X, S und D.

    Die linken Singulärvektoren spannen den Unterraum auf, die
    Singulärwerte skalieren die Achsen, und die rechten Singulärvektoren
    sind die Koeffizienten der Dokumente in diesem Raum. Das ist
    dieselbe Struktur wie bei der Hauptkomponentenanalyse, nur ohne den
    Umweg über die Kovarianzmatrix.

    Returns:
        Abbildung mit ``left``, ``values`` und ``right``.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = _matrix(data)
    left, values, right = np.linalg.svd(field, full_matrices=False)
    return {"left": left, "values": values, "right": right,
            "rank": int(np.sum(values > 1e-10))}


def topics(data, k):
    """Bildet die Dokumente in den k-dimensionalen Topic-Raum ab.

    Raises:
        ValueError: bei einem k ausserhalb des Zulässigen.
    """
    field = _matrix(data)
    report = decompose(field)
    if not 1 <= k <= len(report["values"]):
        raise ValueError("k liegt zwischen eins und der Anzahl der "
                         "Singulärwerte")
    return report["left"][:, :k] * report["values"][:k]


def approximate(data, k):
    """Baut die beste Näherung vom Rang k und misst ihren Fehler.

    Nach dem Satz von Eckart und Young ist der Frobeniusfehler genau die
    Wurzel aus der Summe der weggelassenen quadrierten Singulärwerte, und
    keine andere Matrix von Rang k kommt näher.

    Raises:
        ValueError: bei einem unzulässigen k.
    """
    field = _matrix(data)
    report = decompose(field)
    if not 1 <= k <= len(report["values"]):
        raise ValueError("k liegt zwischen eins und der Anzahl der "
                         "Singulärwerte")
    rebuilt = ((report["left"][:, :k] * report["values"][:k])
               @ report["right"][:k])
    return {"approximation": rebuilt,
            "frobenius error": float(np.linalg.norm(field - rebuilt)),
            "discarded": report["values"][k:], "k": k}


def no_better_approximation(data, k, trials=400, seed=9):
    """Sucht vergeblich nach einer besseren Matrix vom Rang k.

    Geprüft wird nicht mit beliebigen Zufallsmatrizen, die ohnehin weit
    danebenlägen, sondern mit Störungen der optimalen Zerlegung selbst.
    Wenn schon kleine Auslenkungen den Fehler nur vergrössern, ist der
    Satz an dieser Matrix bestätigt.

    Returns:
        Abbildung mit dem besten Versuch und dem Urteil.

    Raises:
        ValueError: bei einem unzulässigen k.
    """
    field = _matrix(data)
    best = approximate(field, k)
    report = decompose(field)
    rng = np.random.default_rng(seed)
    left = report["left"][:, :k] * report["values"][:k]
    right = report["right"][:k]
    lowest = best["frobenius error"]
    for _ in range(trials):
        scale = rng.uniform(1e-4, 0.5)
        one = left + rng.normal(size=left.shape) * scale
        two = right + rng.normal(size=right.shape) * scale
        error = float(np.linalg.norm(field - one @ two))
        lowest = min(lowest, error)
    return {"optimal error": best["frobenius error"],
            "best found": lowest,
            "none was better": lowest >= best["frobenius error"] - 1e-9,
            "trials": trials}


def what_the_subspace_is_for():
    """Sagt, was der Topic-Raum leistet und was nicht.

    Er fasst Terme zusammen, die gemeinsam auftreten, und macht damit
    zwei Dokumente ähnlich, die dasselbe Thema mit verschiedenen Wörtern
    behandeln. Das ist genau die Lücke, die ein Vergleich über rohe
    Termvektoren offenlässt.

    Was er nicht leistet: die Achsen tragen keine Bedeutung. Sie sind
    nach Varianz sortiert, nicht nach Verständlichkeit, und eine Achse
    mischt regelmässig Wörter, die inhaltlich nichts verbindet.
    """
    return {"why": "zwei Texte zum selben Thema mit verschiedenen "
                   "Wörtern werden ähnlich",
            "what it does not give": "die Achsen sind nicht deutbar",
            "sorted by": "Varianz, nicht Verständlichkeit",
            "no ground truth needed": True}
