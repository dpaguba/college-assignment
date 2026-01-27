"""Fenster über einer Zeitreihe."""

import numpy as np


def windows(series, size=10, step=1):
    """Schneidet überlappende Fenster aus einer Reihe.

    Raises:
        ValueError: bei einem Fenster, das länger ist als die Reihe,
            oder einem nicht positiven Schritt.
    """
    values = np.asarray(series, dtype=float)
    if size <= 0 or step <= 0:
        raise ValueError("Fenster und Schritt müssen positiv sein")
    if size > len(values):
        raise ValueError("das Fenster ist länger als die Reihe")
    starts = range(0, len(values) - size + 1, step)
    return np.array([values[start:start + size] for start in starts])


def kinds():
    """Nennt die drei Arten von Auffälligkeit in einer Reihe.

    Sie werden regelmässig in einen Topf geworfen, obwohl sie
    verschiedene Verfahren verlangen. Ein Punktausreisser fällt in
    jedem Fenster auf; ein kontextueller Ausreisser ist für sich
    genommen ein normaler Wert an der falschen Stelle; ein kollektiver
    besteht aus lauter normalen Werten in einer ungewöhnlichen Folge.
    """
    return {"Punkt": "ein einzelner Wert, der in jedem Zusammenhang "
                     "auffällt",
            "kontextuell": "ein normaler Wert an der falschen Stelle",
            "kollektiv": "normale Werte in ungewöhnlicher Folge"}


def _score(series, size):
    """Bewertet jedes Fenster nach seinem Abstand zum Mittel aller."""
    cut = windows(series, size=size, step=1)
    centre = cut.mean(axis=0)
    return np.sqrt(((cut - centre) ** 2).sum(axis=1))


def point_anomaly(length=300, at=180, seed=0):
    """Setzt einen einzelnen Ausschlag und sucht ihn mit kurzem Fenster.

    Raises:
        ValueError: bei einer Stelle ausserhalb der Reihe.
    """
    if not 0 <= at < length:
        raise ValueError("die Stelle liegt ausserhalb der Reihe")
    rng = np.random.default_rng(seed)
    series = np.sin(np.arange(length) * 0.15) + rng.normal(scale=0.1,
                                                           size=length)
    series[at] += 6.0
    scores = _score(series, size=5)
    return {"planted at": at, "found at": int(np.argmax(scores)) + 2,
            "window": 5, "length": length}


def the_window_decides(length=400, seed=1):
    """Zeigt, dass die Fensterlänge bestimmt, was gefunden wird.

    Ein Niveausprung besteht aus lauter unauffälligen Werten. Ein kurzes
    Fenster sieht in jedem einzelnen nichts Besonderes und findet ihn
    nicht; ein Fenster, das über den Sprung reicht, sieht zwei Niveaus
    in einem Ausschnitt und findet ihn sofort.

    Die Fensterlänge ist damit keine technische Einstellung, sondern die
    Aussage darüber, wie lang eine Auffälligkeit sein darf.

    Returns:
        Abbildung mit dem Rang des Sprungs unter beiden Längen.
    """
    start = 250
    found = {"short": 0, "long": 0}
    runs = 40
    for index in range(runs):
        rng = np.random.default_rng(seed + index)
        series = rng.normal(scale=0.5, size=length)
        series[start:start + 40] += 0.5
        for name, size in (("short", 3), ("long", 60)):
            peak = int(np.argmax(_score(series, size)))
            if start - size <= peak <= start + 40:
                found[name] += 1
    return {"short window finds the shift": found["short"] / runs,
            "long window finds the shift": found["long"] / runs,
            "shift at": start, "windows": (3, 60), "runs": runs,
            "size of the shift": 0.5, "noise": 0.5,
            "why": "ein Sprung von der Grösse des Rauschens ist in "
                   "einem kurzen Fenster nicht zu sehen"}


def context_matters(length=480, seed=2):
    """Zeigt einen Wert, der nur ausserhalb seiner Jahreszeit auffällt.

    Die Reihe schwankt mit einer Periode. Der Wert drei kommt an jedem
    Maximum vor und ist damit für sich genommen gewöhnlich; im Tal, wo
    minus drei zu erwarten wäre, ist er es nicht. Ein Verfahren, das nur
    die Höhe misst, schlägt deshalb nicht an, und eines, das die Periode
    abzieht, schlägt sofort an.

    Returns:
        Abbildung mit beiden Urteilen.
    """
    rng = np.random.default_rng(seed)
    season = np.sin(np.arange(length) * 2.0 * np.pi / 24.0) * 3.0
    series = season + rng.normal(scale=0.3, size=length)
    trough = 24 * 8 + 18
    series[trough] = 3.0
    without = abs(series[trough] - series.mean()) / series.std()
    residual = series - season
    with_season = abs(residual[trough]
                      - residual.mean()) / residual.std()
    return {"value": float(series[trough]), "limit": 2.0,
            "flagged by the global detector": bool(without > 2.0),
            "flagged by the seasonal detector": bool(with_season > 2.0),
            "score without the season": float(without),
            "score with the season": float(with_season),
            "why": "der Wert ist gewöhnlich, seine Stelle ist es nicht"}


def why_the_series_is_not_a_bag_of_points():
    """Nennt, was beim Übergang zu Fenstern verloren geht und was nicht.

    Ein Fenster bringt die Reihenfolge innerhalb seiner Länge zurück,
    die ein einzelner Wert nicht hat. Was es nicht bringt, ist alles,
    was länger dauert als das Fenster: ein Trend über die ganze Reihe,
    eine Periode, die nicht hineinpasst, und jede Abhängigkeit über die
    Fenstergrenze hinweg.

    Deshalb steht vor jedem Fensterverfahren eine Entscheidung über die
    Zeitskala, und sie wird meistens nicht als solche behandelt.
    """
    return {"what a window restores": "die Reihenfolge innerhalb seiner "
                                      "Länge",
            "what it cannot see": ["einen Trend über die ganze Reihe",
                                   "eine längere Periode",
                                   "Abhängigkeiten über die Grenze"],
            "the decision": "die Zeitskala, meist unausgesprochen"}
