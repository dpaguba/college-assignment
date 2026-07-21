"""Merkmale durch Mischen bewerten."""

import numpy as np


def _fit(points, values):
    """Passt eine Gerade nach kleinsten Quadraten an."""
    design = np.hstack([np.ones((len(points), 1)), points])
    coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
    return coefficients


def _predict(coefficients, points):
    """Wertet das Modell aus."""
    design = np.hstack([np.ones((len(points), 1)), points])
    return design @ coefficients


def _error(coefficients, points, values):
    """Der mittlere quadratische Fehler."""
    return float(np.mean((_predict(coefficients, points) - values) ** 2))


def measure(coefficients, points, values, feature, repeats=10, seed=0):
    """Misst, wie viel schlechter das Modell ohne ein Merkmal wird.

    Die Spalte wird gemischt, sodass ihr Zusammenhang mit der
    Zielgrösse zerstört wird, während ihre Verteilung erhalten bleibt.
    Der Anstieg des Fehlers ist das Mass.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Wiederholungen.
    """
    if repeats <= 0:
        raise ValueError("es braucht mindestens eine Wiederholung")
    rng = np.random.default_rng(seed)
    base = _error(coefficients, points, values)
    total = 0.0
    for _ in range(repeats):
        shuffled = points.copy()
        rng.shuffle(shuffled[:, feature])
        total += _error(coefficients, shuffled, values) - base
    return total / repeats


def importance(size=2000, repeats=10, seed=0):
    """Bewertet ein nützliches und ein nutzloses Merkmal.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Wiederholungen.
    """
    if repeats <= 0:
        raise ValueError("es braucht mindestens eine Wiederholung")
    rng = np.random.default_rng(seed)
    points = rng.normal(size=(size, 2))
    values = points[:, 0] + rng.normal(scale=0.5, size=size)
    model = _fit(points, values)
    return {"signal": measure(model, points, values, 0, repeats, seed),
            "noise": measure(model, points, values, 1, repeats, seed),
            "base error": _error(model, points, values)}


def the_copy_hides_them_both(size=2000, repeats=10, seed=0):
    """Zeigt, was zwei gleiche Merkmale anrichten.

    Ein Merkmal steht zweimal in den Daten. Das Modell verteilt sein
    Gewicht auf beide, und beim Mischen der einen Spalte gleicht die
    andere den Verlust fast aus. Beide sehen deshalb unwichtig aus,
    obwohl das Merkmal alles erklärt.

    Das ist kein Randfall: bei stark zusammenhängenden Merkmalen tritt
    derselbe Effekt abgeschwächt immer auf, und die Rangliste der
    Wichtigkeiten sagt dann mehr über die Zusammenhänge zwischen den
    Merkmalen als über ihre Bedeutung.

    Returns:
        Abbildung mit den Wichtigkeiten in beiden Aufstellungen.
    """
    rng = np.random.default_rng(seed)
    single = rng.normal(size=(size, 1))
    values = single[:, 0] * 2.0 + rng.normal(scale=0.5, size=size)
    alone = _fit(single, values)
    doubled = np.hstack([single, single])
    both = _fit(doubled, values)
    dropped = _fit(single, values)
    return {"importance when alone": measure(alone, single, values, 0,
                                             repeats, seed),
            "importance of each copy": measure(both, doubled, values, 0,
                                               repeats, seed),
            "error with both": _error(both, doubled, values),
            "error with one copy dropped": _error(dropped, single,
                                                  values),
            "why": "die zweite Spalte gleicht das Mischen der ersten aus"}


def it_measures_the_model_not_the_data(size=2000, repeats=10, seed=0):
    """Zeigt, dass die Wichtigkeit am Modell hängt und nicht am Merkmal.

    Dasselbe Merkmal, zwei Modelle: eines benutzt es, das andere nicht.
    Im ersten ist es wichtig, im zweiten wertlos. Die Zahl beantwortet
    also die Frage, worauf dieses Modell sich stützt, und nicht die
    Frage, was in den Daten steckt.

    Wer sie als Aussage über die Welt liest, verwechselt zwei
    verschiedene Fragen, und bei einem schlechten Modell führt das
    zuverlässig in die Irre.

    Returns:
        Abbildung mit beiden Wichtigkeiten.
    """
    rng = np.random.default_rng(seed)
    points = rng.normal(size=(size, 2))
    values = points[:, 0] + points[:, 1] + rng.normal(scale=0.3,
                                                      size=size)
    using = _fit(points, values)
    ignoring = np.array([float(np.mean(values)), 0.0, 1.0])
    return {"importance in the model that uses it":
            measure(using, points, values, 0, repeats, seed),
            "importance in the model that ignores it":
                measure(ignoring, points, values, 0, repeats, seed),
            "what the number answers": "worauf dieses Modell sich stützt",
            "what it does not answer": "was in den Daten steckt"}


def what_to_do_instead():
    """Nennt, was die bekannten Schwächen abfängt.

    Gegen den Effekt gleicher Merkmale hilft, Gruppen zusammen zu
    mischen statt einzeln. Gegen die Verwechslung von Modell und Daten
    hilft nur, die Frage vorher zu stellen: geht es um dieses Modell
    oder um die Welt. Und gegen beides hilft, die Wichtigkeiten auf
    zurückgehaltenen Daten zu messen, denn auf den Trainingsdaten misst
    man mit, was das Modell auswendig gelernt hat.
    """
    return {"against duplicates": "Gruppen zusammen mischen",
            "against the confusion": "vorher fragen, worum es geht",
            "against both": "auf zurückgehaltenen Daten messen",
            "why held out": "sonst misst man das Auswendiggelernte mit"}
