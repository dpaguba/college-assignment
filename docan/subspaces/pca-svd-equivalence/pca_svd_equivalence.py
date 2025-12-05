"""Der Zusammenhang zwischen Singulärwertzerlegung und PCA."""

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


def scatter(data):
    """Rechnet die Streumatrix als Summe der äusseren Produkte aus.

    Das ist die Matrix von der Folie: die Summe über f_i f_i^T, ohne
    Abzug eines Mittelwerts und ohne Teilen durch N.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = _matrix(data)
    return field.T @ field


def compare(data):
    """Zeigt, dass die Zerlegung und der Eigenwertansatz dasselbe geben.

    Die Singulärwerte der Matrix im Quadrat sind die Eigenwerte der
    Streumatrix, und die rechten Singulärvektoren sind deren
    Eigenvektoren. Der Beweis steht in der Rechnung selbst: aus
    F = U S V^T folgt F^T F = V S^2 V^T, und das ist eine
    Eigenwertzerlegung.

    Returns:
        Abbildung mit beiden Wegen.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = _matrix(data)
    _, values, right = np.linalg.svd(field, full_matrices=False)
    matrix = scatter(field)
    eigen, vectors = np.linalg.eigh(matrix)
    order = np.argsort(eigen)[::-1]
    return {"squared singular values": values ** 2,
            "eigenvalues of the scatter": eigen[order],
            "from svd": right, "from eigen": vectors[:, order].T,
            "scatter": matrix,
            "identity": "aus F = U S V^T folgt F^T F = V S^2 V^T"}


def _first_axis_from_svd(data):
    """Nennt die stärkste Richtung nach der Zerlegung."""
    _, _, right = np.linalg.svd(_matrix(data), full_matrices=False)
    return right[0]


def _first_axis_from_pca(data):
    """Nennt die stärkste Richtung der Kovarianzmatrix."""
    field = _matrix(data)
    centred = field - field.mean(axis=0)
    matrix = (centred.T @ centred) / field.shape[0]
    values, vectors = np.linalg.eigh(matrix)
    return vectors[:, np.argmax(values)]


def _angle(first, second):
    """Misst den Winkel zwischen zwei Richtungen in Grad.

    Raises:
        ValueError: wenn eine der Richtungen die Länge null hat.
    """
    one = np.asarray(first, dtype=float)
    two = np.asarray(second, dtype=float)
    lengths = np.linalg.norm(one) * np.linalg.norm(two)
    if lengths == 0.0:
        raise ValueError("eine Richtung hat die Länge null")
    cosine = abs(float(np.dot(one, two)) / lengths)
    return float(np.degrees(np.arccos(min(1.0, cosine))))


def centring_is_the_difference(data, tolerance=1e-8):
    """Nennt die Stelle, an der die Folie eine Bedingung verschweigt.

    Die Folie stellt die Summe der f_i f_i^T neben die Kovarianzmatrix,
    ohne zu sagen, dass die beiden nur bei mittelwertfreien Daten
    dieselben Achsen liefern. Termvektoren sind niemals mittelwertfrei:
    alle Einträge sind Häufigkeiten und damit nicht negativ. Die stärkste
    Richtung der unzentrierten Streumatrix zeigt deshalb ungefähr auf den
    Mittelwert und trägt kaum Information über die Unterschiede zwischen
    den Dokumenten.

    Returns:
        Abbildung mit beiden Achsen, den Winkeln zum Mittelwert und dem
        Urteil.

    Raises:
        ValueError: bei einer leeren Matrix.
    """
    field = _matrix(data)
    centre = field.mean(axis=0)
    raw = _first_axis_from_svd(field)
    pca = _first_axis_from_pca(field)
    centred = field - centre
    after = _first_axis_from_svd(centred)
    direction = centre if np.linalg.norm(centre) > 0 else np.ones(
        field.shape[1])
    return {"agree without centring": bool(np.allclose(np.abs(raw),
                                                       np.abs(pca),
                                                       atol=tolerance)),
            "agree after centring": bool(np.allclose(np.abs(after),
                                                     np.abs(pca),
                                                     atol=tolerance)),
            "angle to the mean without centring": _angle(raw, direction),
            "angle to the mean after centring": _angle(after, direction),
            "why it matters": "Termvektoren sind nie mittelwertfrei, "
                              "denn Häufigkeiten sind nicht negativ"}


def what_the_slide_says_and_what_it_needs():
    """Trennt die Aussage der Folie von ihrer Voraussetzung.

    Richtig ist: die Zerlegung der Term-Dokument-Matrix entspricht der
    Eigenwertanalyse der Summe der f_i f_i^T. Das gilt immer. Der
    Vergleich mit der Kovarianzmatrix daneben gilt nur nach Abzug des
    Mittelwerts, und dieser Schritt steht auf der Folie nicht.
    """
    return {"always true": "F^T F = V S^2 V^T, also Zerlegung gleich "
                           "Eigenwertanalyse der Streumatrix",
            "only after centring": "die Streumatrix gleich der "
                                   "Kovarianzmatrix",
            "what the slide leaves out": "den Abzug des Mittelwerts",
            "practical effect": "die erste Achse zeigt sonst auf den "
                                "Mittelwert"}
