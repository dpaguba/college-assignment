"""Auffälligkeit über den Rekonstruktionsfehler."""

import numpy as np


def fit(data, components=2):
    """Lernt einen Unterraum aus den normalen Daten.

    Der Engpass ist das ganze Verfahren: das Modell darf die Daten nicht
    einfach durchreichen, sondern muss sie durch wenige Zahlen
    hindurchzwingen. Was danach noch fehlt, ist der Fehler, und der ist
    die Bewertung.

    Raises:
        ValueError: bei einer unzulässigen Zahl von Komponenten.
    """
    field = np.asarray(data, dtype=float)
    if field.ndim != 2 or field.shape[0] < 2:
        raise ValueError("mindestens zwei Punkte in einer Matrix")
    if not 1 <= components <= field.shape[1]:
        raise ValueError("die Zahl der Komponenten liegt zwischen eins "
                         "und der Dimension")
    centre = field.mean(axis=0)
    centred = field - centre
    matrix = (centred.T @ centred) / len(field)
    values, vectors = np.linalg.eigh(matrix)
    order = np.argsort(values)[::-1][:components]
    return {"mean": centre, "axes": vectors[:, order].T,
            "eigenvalues": values[order], "components": components}


def reconstruct(model, data):
    """Projiziert Punkte in den Unterraum und zurück."""
    field = np.asarray(data, dtype=float)
    centred = field - model["mean"]
    return (centred @ model["axes"].T) @ model["axes"] + model["mean"]


def error(model, data):
    """Misst den quadratischen Rekonstruktionsfehler je Punkt."""
    field = np.asarray(data, dtype=float)
    return np.sum((field - reconstruct(model, field)) ** 2, axis=1)


def example(seed=0):
    """Ein Unterraum, ein Punkt darin und einer daneben.

    Returns:
        Abbildung mit beiden Fehlern.
    """
    rng = np.random.default_rng(seed)
    basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    data = rng.normal(size=(300, 2)) @ basis
    model = fit(data, components=2)
    on_plane = np.array([[1.5, -2.0, 0.0]])
    off_plane = np.array([[1.5, -2.0, 4.0]])
    return {"error on the plane": float(error(model, on_plane)[0]),
            "error off the plane": float(error(model, off_plane)[0]),
            "components": 2}


def over_components(seed=1):
    """Misst den mittleren Fehler über die Zahl der Komponenten.

    Returns:
        Liste mit einer Zeile je Zahl.
    """
    rng = np.random.default_rng(seed)
    data = rng.normal(size=(300, 3)) @ rng.normal(size=(3, 6))
    data = data + rng.normal(size=(300, 6)) * 0.1
    found = []
    for components in range(1, 7):
        model = fit(data, components)
        found.append({"components": components,
                      "mean error": float(error(model, data).mean())})
    return found


def the_bottleneck_is_the_detector(seed=2):
    """Zeigt, dass ohne Engpass nichts erkannt wird.

    Mit so vielen Komponenten wie Merkmalen ist die Rekonstruktion
    exakt, und zwar für jeden Punkt, auch für den auffälligen. Der
    Fehler ist dann überall null und trennt nichts. Erst der Engpass
    macht aus dem Modell einen Detektor, und das ist der Grund, warum
    ein Autoencoder ohne Verengung nutzlos ist, egal wie gut er
    rekonstruiert.

    Returns:
        Abbildung mit der Trennschärfe in beiden Fällen.
    """
    rng = np.random.default_rng(seed)
    normal = rng.normal(size=(400, 2)) @ rng.normal(size=(2, 6))
    strange = rng.normal(size=(20, 6)) * 3.0
    found = {}
    for name, components in (("the bottleneck", 2), ("full rank", 6)):
        model = fit(normal, components)
        inside = error(model, normal)
        outside = error(model, strange)
        spread = float(inside.std() + outside.std()) + 1e-12
        found[name] = abs(float(outside.mean() - inside.mean())) / spread
    return {"separation at the bottleneck": found["the bottleneck"],
            "separation at full rank": found["full rank"],
            "why": "ohne Engpass ist die Rekonstruktion für jeden Punkt "
                   "exakt"}


def the_blind_spot(seed=3):
    """Zeigt, was das Verfahren grundsätzlich nicht sieht.

    Ein auffälliger Punkt, der zufällig im gelernten Unterraum liegt,
    wird fehlerfrei rekonstruiert und bekommt die Bewertung null. Er
    kann noch so weit von allen normalen Daten entfernt sein.

    Das Verfahren misst den Abstand zum Unterraum und nicht den Abstand
    zu den Daten, und diese beiden Dinge werden regelmässig verwechselt.
    Wer es einsetzt, nimmt an, dass Auffälligkeit aus dem Unterraum
    herausführt.

    Returns:
        Abbildung mit beiden Bewertungen.
    """
    rng = np.random.default_rng(seed)
    normal = np.zeros((400, 3))
    normal[:, :2] = rng.normal(size=(400, 2))
    model = fit(normal, components=2)
    inside = np.array([[40.0, 40.0, 0.0]])
    outside = np.array([[0.2, 0.2, 12.0]])
    return {"score of the inside anomaly": float(error(model, inside)[0]),
            "score of the outside anomaly":
                float(error(model, outside)[0]),
            "distance from the data, inside anomaly":
                float(np.linalg.norm(inside)),
            "distance from the data, outside anomaly":
                float(np.linalg.norm(outside)),
            "what it measures": "den Abstand zum Unterraum, nicht den zu "
                                "den Daten"}


def what_the_slide_calls_a_heuristic():
    """Nennt die Annahme, die das Verfahren trägt.

    Die Themenbeschreibung sagt es offen: das Modell versagt bei einer
    Auffälligkeit, weil es nicht darauf trainiert wurde. Das ist eine
    Heuristik und kein Argument, denn ein Modell mit genügend Kapazität
    lernt auch das Ungesehene zu rekonstruieren, und ein Modell mit zu
    wenig Kapazität versagt auch bei normalen Daten.

    Dazwischen liegt der brauchbare Bereich, und wo er liegt, lässt sich
    nur messen.
    """
    return {"the heuristic": "das Modell versagt bei Auffälligem, weil "
                             "es nicht darauf trainiert wurde",
            "too much capacity": "es rekonstruiert auch das Ungesehene",
            "too little": "es versagt auch bei normalen Daten",
            "in between": "lässt sich nur messen"}
