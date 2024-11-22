"""Training gegen Test."""

import numpy as np


def truth(x):
    """Die Funktion hinter den Daten."""
    return np.sin(1.5 * x) + 0.3 * x


def _data(points, noise, rng):
    """Zieht eine Stichprobe."""
    x = rng.uniform(-3.0, 3.0, size=points)
    return x, truth(x) + rng.normal(scale=noise, size=points)


def fit_degree(degree, points=20, noise=0.4, seed=0, test_points=400):
    """Passt ein Polynom an und misst beide Fehler.

    Raises:
        ValueError: bei einem Grad, für den die Daten nicht reichen.
    """
    if degree < 0:
        raise ValueError("der Grad darf nicht negativ sein")
    if degree + 1 > points:
        raise ValueError("mehr Freiheitsgrade als Punkte")
    rng = np.random.default_rng(seed)
    x, y = _data(points, noise, rng)
    design = np.vander(x, degree + 1, increasing=True)
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ coefficients
    grid = np.linspace(-3.0, 3.0, test_points)
    test = np.vander(grid, degree + 1, increasing=True) @ coefficients
    return {"degree": degree,
            "training error": float(np.mean((fitted - y) ** 2)),
            "test error": float(np.mean((test - truth(grid)) ** 2)),
            "points": points}


def curve(degrees=range(0, 15), points=20, noise=0.4, seed=0):
    """Misst beide Fehler über die Modellkomplexität.

    Der Trainingsfehler fällt mit jedem Grad, und zwar mit Sicherheit:
    ein Polynom vom Grad d ist auch eines vom Grad d plus eins mit
    Koeffizient null, also kann die beste Anpassung nicht schlechter
    werden. Der Testfehler hat kein solches Argument und dreht um.

    Returns:
        Liste mit einer Zeile je Grad.
    """
    return [fit_degree(degree, points, noise, seed)
            for degree in degrees]


def exact_fit(points=8, noise=0.4, seed=1):
    """Legt ein Polynom durch jeden einzelnen Punkt.

    Mit so vielen Freiheitsgraden wie Punkten wird der Trainingsfehler
    null, und das sagt genau nichts: das Modell hat die Daten
    auswendig gelernt, das Rauschen eingeschlossen.

    Raises:
        ValueError: bei zu wenigen Punkten.
    """
    if points < 2:
        raise ValueError("es braucht mindestens zwei Punkte")
    return fit_degree(points - 1, points, noise, seed)


def more_data_helps(points=20, more=200):
    """Zeigt, dass mehr Daten den Umkehrpunkt verschiebt.

    Returns:
        Abbildung mit beiden besten Graden.
    """
    small = curve(range(0, 15), points=points)
    large = curve(range(0, 15), points=more)
    best = min(small, key=lambda row: row["test error"])["degree"]
    later = min(large, key=lambda row: row["test error"])["degree"]
    return {"best degree": best, "best degree with more data": later,
            "points": points, "more points": more,
            "why": "mit mehr Punkten kostet ein zusätzlicher "
                   "Freiheitsgrad weniger Streuung"}


def when_to_stop():
    """Sagt, woran das Ende des Experimentierens hängt.

    Die Folie nennt es beiläufig: man hört auf, wenn das gewünschte
    Ergebnis da ist. Das ist die ehrlichste Beschreibung der Praxis und
    zugleich die gefährlichste Regel, denn wer lange genug Modelle
    vergleicht, findet auf jedem Testdatensatz eines, das gut aussieht.
    Der Testfehler wird dann selbst zum Trainingsfehler einer zweiten,
    unsichtbaren Anpassung.
    """
    return {"the rule on the slide": "wir hören auf, wenn das Ergebnis "
                                     "stimmt",
            "what people actually do": "Modelle vergleichen, bis eines "
                                       "auf den Testdaten gut aussieht",
            "the cost": "der Testfehler wird zum Trainingsfehler einer "
                        "zweiten Anpassung",
            "the fix": "ein dritter Datensatz, der einmal benutzt wird"}
