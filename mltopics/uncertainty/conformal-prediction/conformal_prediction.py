"""Vorhersagemengen mit einer Deckungsgarantie."""

import math

import numpy as np


def level(size, alpha=0.1):
    """Nennt das Quantil, das die endliche Garantie sichert.

    Genommen wird nicht das Quantil zu eins minus alpha, sondern das
    zur aufgerundeten Zahl (n + 1) mal (1 − alpha), geteilt durch n. Die
    Korrektur ist der ganze Unterschied zwischen einer Faustregel und
    einer Garantie: mit ihr gilt die Deckung für jede endliche
    Stichprobe, ohne sie nur ungefähr.

    Raises:
        ValueError: bei einem alpha ausserhalb von null bis eins oder
            einer Stichprobe, die für dieses alpha zu klein ist.
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha liegt zwischen null und eins")
    rank = math.ceil((size + 1) * (1.0 - alpha))
    if rank > size:
        raise ValueError("die Stichprobe ist für dieses alpha zu klein")
    return rank / size


def calibrate(residuals, alpha=0.1):
    """Bestimmt die halbe Breite aus den Fehlern der Eichmenge.

    Raises:
        ValueError: bei einer leeren Eichmenge oder unzulässigem alpha.
    """
    values = np.asarray(residuals, dtype=float)
    if values.size == 0:
        raise ValueError("leere Eichmenge")
    return float(np.quantile(values, level(len(values), alpha),
                             method="higher"))


def _split(size, seed, noise=1.0, slope=2.0):
    """Zieht Daten und teilt sie in drei Teile."""
    rng = np.random.default_rng(seed)
    points = rng.uniform(-3.0, 3.0, size=size)
    values = slope * points + rng.normal(scale=noise, size=size)
    cut = size // 3
    return ((points[:cut], values[:cut]),
            (points[cut:2 * cut], values[cut:2 * cut]),
            (points[2 * cut:], values[2 * cut:]))


def _fit(points, values):
    """Passt eine Gerade an."""
    design = np.vstack([np.ones_like(points), points]).T
    coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
    return coefficients


def _predict(coefficients, points):
    """Wertet die Gerade aus."""
    return coefficients[0] + coefficients[1] * np.asarray(points)


def coverage(runs=100, size=900, alpha=0.1, seed=0):
    """Misst, wie oft das Intervall den wahren Wert enthält.

    Die Garantie verspricht mindestens eins minus alpha, und zwar ohne
    eine Annahme über das Modell. Gemessen über viele Läufe liegt die
    Deckung leicht darüber, weil das aufgerundete Quantil ein wenig zu
    breit ist.

    Raises:
        ValueError: bei unzulässigen Angaben.
    """
    if runs <= 0 or size <= 0:
        raise ValueError("Läufe und Grösse müssen positiv sein")
    covered = 0
    total = 0
    widths = []
    for index in range(runs):
        train, hold, test = _split(size, seed + index)
        model = _fit(*train)
        residuals = np.abs(hold[1] - _predict(model, hold[0]))
        half = calibrate(residuals, alpha)
        inside = np.abs(test[1] - _predict(model, test[0])) <= half
        covered += int(inside.sum())
        total += len(inside)
        widths.append(2.0 * half)
    return {"measured coverage": covered / total,
            "promised": 1.0 - alpha, "mean width": float(np.mean(widths)),
            "runs": runs, "alpha": alpha}


def a_bad_model_still_covers(runs=60, size=900, alpha=0.1, seed=0):
    """Zeigt, dass die Garantie nicht am Modell hängt.

    Ein Modell, das die Steigung ignoriert und immer den Mittelwert
    sagt, bekommt dieselbe Deckung wie das richtige. Es zahlt dafür mit
    der Breite: das Intervall wird so weit, dass die Aussage kaum noch
    nützt.

    Die Güte des Modells zeigt sich also nicht in der Deckung, sondern
    in der Breite, und wer nur die Deckung berichtet, sagt nichts über
    das Modell.

    Returns:
        Abbildung mit Deckung und Breite für beide Modelle.
    """
    found = {}
    for name in ("good", "bad"):
        covered = 0
        total = 0
        widths = []
        for index in range(runs):
            train, hold, test = _split(size, seed + index)
            model = (_fit(*train) if name == "good"
                     else np.array([float(np.mean(train[1])), 0.0]))
            residuals = np.abs(hold[1] - _predict(model, hold[0]))
            half = calibrate(residuals, alpha)
            inside = np.abs(test[1] - _predict(model, test[0])) <= half
            covered += int(inside.sum())
            total += len(inside)
            widths.append(2.0 * half)
        found[name] = (covered / total, float(np.mean(widths)))
    return {"coverage of the good model": found["good"][0],
            "coverage of the bad model": found["bad"][0],
            "width of the good model": found["good"][1],
            "width of the bad model": found["bad"][1],
            "why": "die Garantie hängt am Verfahren, nicht am Modell"}


def exchangeability_is_the_condition(runs=60, size=900, alpha=0.1,
                                     seed=0, shift=4.0):
    """Zeigt die eine Annahme, die gebraucht wird.

    Verlangt wird, dass Eichmenge und Testmenge austauschbar sind, also
    aus derselben Quelle stammen. Verschiebt sich die Verteilung
    zwischen beiden, bricht die Garantie, und zwar ohne Warnung: die
    Intervalle sehen unverändert aus, nur der wahre Wert liegt öfter
    daneben.

    Verschoben wird hier die Zielgrösse und nicht die Eingabe. Eine
    Verschiebung entlang der gelernten Geraden würde nichts ändern,
    weil die Fehler dieselben blieben; es kommt auf die Verteilung der
    Fehler an und nicht auf die der Punkte.

    Returns:
        Abbildung mit der Deckung mit und ohne Verschiebung.
    """
    found = {}
    for name in ("plain", "shifted"):
        covered = 0
        total = 0
        for index in range(runs):
            train, hold, test = _split(size, seed + index)
            model = _fit(*train)
            residuals = np.abs(hold[1] - _predict(model, hold[0]))
            half = calibrate(residuals, alpha)
            values = test[1] + (shift if name == "shifted" else 0.0)
            inside = np.abs(values - _predict(model, test[0])) <= half
            covered += int(inside.sum())
            total += len(inside)
        found[name] = covered / total
    return {"coverage without a shift": found["plain"],
            "coverage after the shift": found["shifted"],
            "promised": 1.0 - alpha, "shift": shift,
            "why": "die Garantie verlangt austauschbare Daten"}


def what_it_does_not_promise():
    """Grenzt die Garantie ein.

    Sie gilt im Mittel über alle Fälle, nicht für jeden einzelnen. Ein
    Verfahren darf die schwierigen Fälle systematisch verfehlen und die
    leichten übererfüllen und hält die Zusage trotzdem. Wer Deckung für
    Teilgruppen braucht, muss sie eigens herstellen.
    """
    return {"promises": "Deckung im Mittel über alle Fälle",
            "does not promise": "Deckung für jeden einzelnen Fall",
            "the loophole": "die schweren Fälle verfehlen und die "
                            "leichten übererfüllen",
            "if you need more": "Deckung für Teilgruppen eigens "
                                "herstellen"}
