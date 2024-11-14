"""Die Zerlegung des erwarteten Fehlers."""

import numpy as np


def truth(x):
    """Die Funktion, die gelernt werden soll."""
    return np.sin(1.5 * x) + 0.3 * x


SPAN = 3.0


def _design(points, degree, basis="legendre"):
    """Baut die Entwurfsmatrix in der gewählten Basis.

    Die Legendre-Basis ist auf dem Intervall orthogonal und deshalb gut
    konditioniert. Die Monombasis spannt denselben Raum auf, ihre
    Spalten sind aber fast parallel, und ab etwa Grad zehn bricht die
    Anpassung numerisch zusammen.

    Raises:
        ValueError: bei einer unbekannten Basis.
    """
    scaled = np.asarray(points, dtype=float) / SPAN
    if basis == "legendre":
        return np.polynomial.legendre.legvander(scaled, degree)
    if basis == "monomial":
        return np.vander(scaled, degree + 1, increasing=True)
    raise ValueError("unbekannte Basis: %s" % basis)


def _fit(points, values, degree, basis="legendre"):
    """Passt ein Polynom nach der Methode der kleinsten Quadrate an."""
    design = _design(points, degree, basis)
    coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
    return coefficients


def _apply(coefficients, points, basis="legendre"):
    """Wertet ein Polynom aus."""
    return _design(points, len(coefficients) - 1, basis) @ coefficients


def decompose(degree=3, samples=400, size=25, noise=0.5, seed=0,
              grid=41, basis="legendre"):
    """Zerlegt den erwarteten Fehler in Verzerrung, Streuung und Rauschen.

    Gezogen werden viele Stichproben aus derselben Quelle, auf jeder wird
    ein Polynom angepasst, und an jeder Teststelle werden drei Grössen
    gemessen: wie weit der mittlere Vorhersagewert von der Wahrheit
    abweicht, wie stark die Vorhersagen um ihren eigenen Mittelwert
    streuen, und wie stark die Beobachtungen selbst rauschen.

    Die drei müssen sich zum erwarteten quadratischen Fehler addieren.
    Das ist keine Näherung, sondern eine Identität, und sie ist die
    Probe für die ganze Rechnung.

    Args:
        degree: der Grad des Polynoms.
        samples: die Anzahl der Stichproben.
        size: die Grösse einer Stichprobe.
        noise: die Streuung des Rauschens.
        seed: der Startwert.
        grid: die Anzahl der Teststellen.

    Returns:
        Abbildung mit den drei Teilen und ihrer Summe.

    Raises:
        ValueError: bei einem negativen Grad oder zu wenigen Punkten.
    """
    if degree < 0:
        raise ValueError("der Grad darf nicht negativ sein")
    if size <= degree + 1:
        raise ValueError("zu wenige Punkte für diesen Grad")
    rng = np.random.default_rng(seed)
    test = np.linspace(-3.0, 3.0, grid)
    wanted = truth(test)
    predictions = np.zeros((samples, grid))
    for index in range(samples):
        points = rng.uniform(-3.0, 3.0, size=size)
        values = truth(points) + rng.normal(scale=noise, size=size)
        predictions[index] = _apply(_fit(points, values, degree, basis),
                                    test, basis)
    mean = predictions.mean(axis=0)
    bias = float(np.mean((mean - wanted) ** 2))
    variance = float(np.mean(predictions.var(axis=0)))
    error = float(np.mean((predictions - wanted) ** 2)) + noise ** 2
    return {"degree": degree, "bias squared": bias, "variance": variance,
            "noise": noise ** 2, "expected error": error,
            "samples": samples, "size": size}


def over_degrees(degrees=(0, 1, 2, 3, 4, 5), **rest):
    """Misst die Zerlegung über mehrere Modellkomplexitäten.

    Der Bereich endet bei fünf, denn darüber trägt eine Stichprobe von
    fünfundzwanzig Punkten die Anpassung nicht mehr, und dann steigen
    beide Teile zugleich. Was das bedeutet, steht in
    ``the_textbook_curve_breaks_down``.

    Returns:
        Liste mit einer Zeile je Grad.
    """
    return [decompose(degree=degree, **rest) for degree in degrees]


def the_sweet_spot(degrees=(0, 1, 2, 3, 4, 5, 6, 8, 10, 12)):
    """Sucht den Grad mit dem kleinsten erwarteten Fehler.

    Die Verzerrung fällt mit der Komplexität, die Streuung steigt, und
    die Summe hat dazwischen ein Minimum. Das ist die ganze Aussage der
    Folie, und sie lässt sich messen statt zeichnen.

    Returns:
        Abbildung mit dem besten Grad und dem Verlauf.
    """
    rows = [decompose(degree=degree, samples=300, size=25)
            for degree in degrees]
    best = min(rows, key=lambda row: row["expected error"])
    return {"best degree": best["degree"],
            "highest degree": max(degrees),
            "error there": best["expected error"],
            "curve": [(row["degree"], round(row["expected error"], 4))
                      for row in rows],
            "bias falls": rows[0]["bias squared"]
            > rows[-1]["bias squared"],
            "variance rises": rows[0]["variance"] < rows[-1]["variance"]}


def the_textbook_curve_breaks_down(degrees=(3, 5, 8, 11, 14)):
    """Zeigt, wo das übliche Bild von der Folie aufhört zu gelten.

    Gezeichnet wird die Verzerrung als fallend und die Streuung als
    steigend, und dazwischen liegt der gesuchte Punkt. Das gilt, solange
    die Stichprobe die Anpassung noch trägt. Bei fünfundzwanzig Punkten
    und Grad elf ist das nicht mehr der Fall: die einzelnen Anpassungen
    schlagen an den Rändern so weit aus, dass sogar ihr Mittelwert weit
    neben der Wahrheit liegt.

    Dann steigt die gemessene Verzerrung mit dem Grad, statt zu fallen,
    und zwar um Grössenordnungen. Das ist kein Rechenfehler und auch
    keine Frage der Basis; mit der Zerlegung über eine orthogonale
    Basis kommt dasselbe heraus. Es ist die Grenze der Aussage: unter
    ihr beschreibt sie das Verhalten, über ihr nicht mehr.

    Returns:
        Abbildung mit beiden Teilen über die Grade.
    """
    rows = [decompose(degree=degree, samples=200, size=25)
            for degree in degrees]
    bias = [row["bias squared"] for row in rows]
    variance = [row["variance"] for row in rows]
    return {"degrees": list(degrees),
            "bias squared": [round(value, 4) for value in bias],
            "variance": [round(value, 4) for value in variance],
            "bias falls throughout": bias[0] > bias[-1],
            "both rise at the end": bias[-1] > bias[-2]
            and variance[-1] > variance[-2],
            "points in the sample": 25,
            "why": "die Anpassungen schlagen an den Rändern aus, und "
                   "auch ihr Mittelwert liegt dann daneben"}


def what_the_decomposition_does_not_give():
    """Nennt, was die Zerlegung im Ernstfall unmöglich macht.

    Sie braucht die wahre Funktion und viele Stichproben aus derselben
    Quelle. Beides hat man beim Lernen nicht: es gibt eine Stichprobe,
    und die Wahrheit ist gesucht. Die Zerlegung erklärt also, warum ein
    mittlerer Grad gewinnt, sagt aber nicht, welcher es ist. Dafür
    bleibt nur die Messung auf zurückgehaltenen Daten.
    """
    return {"needs": ["die wahre Funktion", "viele Stichproben"],
            "has": "eine Stichprobe",
            "what it explains": "warum ein mittlerer Grad gewinnt",
            "what it does not say": "welcher es ist",
            "what is left": "messen auf zurückgehaltenen Daten"}
