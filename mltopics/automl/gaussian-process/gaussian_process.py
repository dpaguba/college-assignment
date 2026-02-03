"""Regression mit einem Gaussprozess."""

import numpy as np


def kernel(first, second, length=1.0, amplitude=1.0):
    """Die quadratisch exponentielle Kovarianzfunktion.

    Sie sagt, wie stark zwei Punkte einander binden: nahe Punkte fast
    vollständig, ferne gar nicht. Die Längenskala ist der Massstab
    dafür und damit die eigentliche Annahme über die gesuchte Funktion.

    Raises:
        ValueError: bei einer nicht positiven Längenskala oder Amplitude.
    """
    if length <= 0.0 or amplitude <= 0.0:
        raise ValueError("Längenskala und Amplitude müssen positiv sein")
    one = np.atleast_2d(np.asarray(first, dtype=float))
    two = np.atleast_2d(np.asarray(second, dtype=float))
    squared = ((one[:, None, :] - two[None, :, :]) ** 2).sum(axis=2)
    return amplitude ** 2 * np.exp(-0.5 * squared / length ** 2)


def posterior(points, values, grid, length=1.0, amplitude=1.0,
              noise=1e-6):
    """Rechnet Mittelwert und Streuung der Nachverteilung aus.

    Ohne Rauschen geht der Mittelwert exakt durch jede Beobachtung, und
    die Streuung ist dort null. Das ist die Probe: ein Verfahren, dessen
    Vorhersage an einer Beobachtung danebenliegt, hat einen Fehler in
    der Algebra.

    Args:
        points: die beobachteten Stellen.
        values: die beobachteten Werte.
        grid: die Stellen, an denen vorhergesagt wird.
        length: die Längenskala.
        amplitude: die Amplitude.
        noise: die angenommene Streuung der Beobachtungen.

    Returns:
        Abbildung mit ``mean`` und ``variance``.

    Raises:
        ValueError: bei unpassend vielen Werten oder einem negativen
            Rauschen.
    """
    train = np.atleast_2d(np.asarray(points, dtype=float))
    observed = np.asarray(values, dtype=float)
    if len(train) != len(observed):
        raise ValueError("zu jeder Stelle gehört genau ein Wert")
    if noise < 0.0:
        raise ValueError("das Rauschen darf nicht negativ sein")
    test = np.atleast_2d(np.asarray(grid, dtype=float))
    inside = kernel(train, train, length, amplitude)
    inside = inside + noise * np.eye(len(train))
    cross = kernel(test, train, length, amplitude)
    solved = np.linalg.solve(inside, observed)
    weights = np.linalg.solve(inside, cross.T)
    variance = (amplitude ** 2
                - np.sum(cross * weights.T, axis=1))
    return {"mean": cross @ solved,
            "variance": np.maximum(variance, 0.0),
            "deviation": np.sqrt(np.maximum(variance, 0.0))}


def information_never_hurts(seed=0, length=1.0):
    """Prüft, dass eine zusätzliche Beobachtung nirgends schadet.

    Die Streuung der Nachverteilung kann durch einen weiteren Punkt an
    keiner Stelle grösser werden. Das folgt aus der Algebra und ist eine
    scharfe Prüfung, weil ein Vorzeichenfehler in der Formel sie sofort
    verletzt.

    Returns:
        Abbildung mit dem Urteil und der grössten Zunahme.
    """
    rng = np.random.default_rng(seed)
    points = rng.uniform(-3.0, 3.0, size=(5, 1))
    values = np.sin(points).reshape(-1)
    grid = np.linspace(-4.0, 4.0, 300).reshape(-1, 1)
    before = posterior(points, values, grid, length)["variance"]
    extra = np.array([[0.7]])
    after = posterior(np.vstack([points, extra]),
                      np.concatenate([values, np.sin(extra).reshape(-1)]),
                      grid, length)["variance"]
    rise = float(np.max(after - before))
    return {"never higher": rise <= 1e-9, "largest rise": rise,
            "why": "eine Beobachtung kann die Streuung nirgends "
                   "vergrössern"}


def the_length_scale_decides(seed=0):
    """Zeigt, dass die Längenskala die Annahme über die Funktion ist.

    Eine kurze Skala lässt den Mittelwert zwischen den Beobachtungen
    wild schwingen und zur Nulllinie zurückfallen; eine lange glättet
    alles zu einer flachen Kurve. Beide passen genau durch dieselben
    Punkte. Was zwischen den Punkten steht, kommt nicht aus den Daten,
    sondern aus dieser Zahl.

    Returns:
        Abbildung mit einem Mass für die Welligkeit bei beiden Skalen.
    """
    rng = np.random.default_rng(seed)
    points = np.sort(rng.uniform(-3.0, 3.0, size=(7, 1)), axis=0)
    values = np.sin(points).reshape(-1)
    grid = np.linspace(-3.0, 3.0, 400).reshape(-1, 1)
    found = {}
    for name, length in (("short", 0.15), ("long", 3.0)):
        mean = posterior(points, values, grid, length)["mean"]
        found[name] = float(np.sum(np.abs(np.diff(mean))))
    return {"wiggles with a short scale": found["short"],
            "wiggles with a long scale": found["long"],
            "scales": (0.15, 3.0),
            "why": "was zwischen den Punkten steht, kommt aus der Skala"}


def what_it_costs():
    """Nennt, warum das Verfahren nicht überall eingesetzt wird.

    Das Lösen des Gleichungssystems wächst mit der dritten Potenz der
    Beobachtungen, also ist bei einigen tausend Punkten Schluss. Für die
    Hyperparametersuche ist das kein Hindernis, weil dort jede
    Beobachtung teuer ist und es deshalb nie viele gibt. Genau dieses
    Verhältnis macht den Gaussprozess dort zur naheliegenden Wahl.
    """
    return {"cost": "die dritte Potenz der Anzahl Beobachtungen",
            "limit": "einige tausend Punkte",
            "why it fits hyperparameter search": "dort ist jede "
                                                 "Beobachtung teuer und "
                                                 "es gibt nie viele",
            "what it gives in return": "eine Streuung zu jeder Vorhersage"}
