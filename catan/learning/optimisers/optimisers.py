"""Die Verfahren des Abstiegs."""

import numpy as np

MATRIX = np.array([[3.0, 0.4], [0.4, 1.0]])

TARGET = np.array([2.0, -1.0])

START = np.array([-4.0, 5.0])

OPTIMUM = TARGET

METHODS = ("gradient descent", "momentum", "nesterov", "adagrad",
           "rmsprop", "adam")

RATES = {"gradient descent": 0.1, "momentum": 0.05, "nesterov": 0.05,
         "adagrad": 1.0, "rmsprop": 0.05, "adam": 0.1}


def value(point, matrix=None, target=None):
    """Der Wert der quadratischen Zielfunktion."""
    matrix = MATRIX if matrix is None else matrix
    target = TARGET if target is None else target
    offset = np.asarray(point, dtype=float) - target
    if not np.all(np.isfinite(offset)):
        return float("inf")
    with np.errstate(over="ignore", invalid="ignore"):
        return float(0.5 * offset @ matrix @ offset)


def gradient(point, matrix=None, target=None):
    """Der Gradient derselben Funktion."""
    matrix = MATRIX if matrix is None else matrix
    target = TARGET if target is None else target
    return matrix @ (np.asarray(point, dtype=float) - target)


def closed_form(matrix=None, target=None):
    """Löst das Minimum geschlossen.

    Für eine quadratische Form ist der Gradient null genau im
    Scheitelpunkt, und der lässt sich durch Lösen eines linearen
    Gleichungssystems bestimmen. Jedes Abstiegsverfahren muss dorthin
    kommen; das ist der Massstab.
    """
    matrix = MATRIX if matrix is None else matrix
    target = TARGET if target is None else target
    return np.linalg.solve(matrix, matrix @ target)


def run(method, steps=1000, rate=None, decay=0.9, second=0.999,
        epsilon=1e-8, start=None, matrix=None, target=None):
    """Läuft ein Verfahren und misst, wie weit es kommt.

    Args:
        method: der Name des Verfahrens.
        steps: die Anzahl der Schritte.
        rate: die Schrittweite, oder None für den Vorgabewert des
            Verfahrens. AdaGrad braucht die grösste, weil es seine
            eigene Schrittweite am schnellsten herunterregelt.
        decay: der Gewichtungsfaktor des ersten Moments.
        second: der Gewichtungsfaktor des zweiten Moments.
        epsilon: die Zahl gegen die Division durch null.

    Returns:
        Abbildung mit dem Endpunkt und dem Abstand zum Minimum.

    Raises:
        ValueError: bei einem unbekannten Verfahren oder einer nicht
            positiven Schrittzahl.
    """
    if method not in METHODS:
        raise ValueError("unbekanntes Verfahren: %s" % method)
    if steps <= 0:
        raise ValueError("die Schrittzahl muss positiv sein")
    rate = RATES[method] if rate is None else rate
    point = np.array(START if start is None else start, dtype=float)
    velocity = np.zeros_like(point)
    squares = np.zeros_like(point)
    path = [point.copy()]
    for step in range(1, steps + 1):
        if method == "nesterov":
            slope = gradient(point + decay * velocity, matrix, target)
        else:
            slope = gradient(point, matrix, target)
        if method == "gradient descent":
            point = point - rate * slope
        elif method in ("momentum", "nesterov"):
            velocity = decay * velocity - rate * slope
            point = point + velocity
        elif method == "adagrad":
            squares = squares + slope ** 2
            point = point - rate * slope / (np.sqrt(squares) + epsilon)
        elif method == "rmsprop":
            squares = decay * squares + (1.0 - decay) * slope ** 2
            point = point - rate * slope / (np.sqrt(squares) + epsilon)
        else:
            velocity = decay * velocity + (1.0 - decay) * slope
            squares = second * squares + (1.0 - second) * slope ** 2
            first = velocity / (1.0 - decay ** step)
            scaled = squares / (1.0 - second ** step)
            point = point - rate * first / (np.sqrt(scaled) + epsilon)
        if not np.all(np.isfinite(point)):
            break
        path.append(point.copy())
    optimum = closed_form(matrix, target)
    return {"method": method, "point": point,
            "distance to the optimum": float(np.linalg.norm(point
                                                            - optimum)),
            "value": value(point, matrix, target), "steps": len(path) - 1,
            "diverged": not np.all(np.isfinite(point))}


def step_size(rates=(0.01, 0.1, 0.3, 0.6, 0.8, 1.0)):
    """Zeigt, ab welcher Schrittweite das Verfahren auseinanderläuft.

    Für eine quadratische Form ist die Grenze bekannt: der einfache
    Abstieg konvergiert genau dann, wenn die Schrittweite kleiner ist
    als zwei geteilt durch den grössten Eigenwert. Hier sind das
    ungefähr zwei geteilt durch drei Komma eins.

    Returns:
        Abbildung mit den Ergebnissen und der Grenze.
    """
    limit = 2.0 / float(np.linalg.eigvalsh(MATRIX).max())
    found = []
    diverges = []
    for rate in rates:
        report = run("gradient descent", steps=500, rate=rate)
        broke = (report["diverged"]
                 or report["distance to the optimum"] > 1e3)
        found.append({"rate": rate,
                      "distance": report["distance to the optimum"],
                      "diverges": broke})
        diverges.append(broke)
    return {"rows": found, "diverges": diverges, "limit": limit,
            "largest eigenvalue": float(np.linalg.eigvalsh(MATRIX).max()),
            "rule": "der einfache Abstieg konvergiert unter zwei durch "
                    "den grössten Eigenwert"}


def the_narrow_valley(stretch=40.0, rate=0.02, wanted=1e-3):
    """Zählt die Schritte in einem lang gezogenen Tal.

    In einem Tal mit sehr verschiedenen Krümmungen springt der einfache
    Abstieg zwischen den steilen Wänden hin und her und kommt in
    Längsrichtung kaum voran. Der Impuls addiert die Schritte auf und
    hebt die Querbewegung teilweise auf, weil sie das Vorzeichen
    wechselt, während die Längsbewegung es behält.

    Returns:
        Abbildung mit der Zahl der Schritte für beide Verfahren.
    """
    matrix = np.array([[stretch, 0.0], [0.0, 1.0]])
    target = np.array([0.0, 0.0])
    start = np.array([1.0, 1.0])
    found = {}
    for method in ("gradient descent", "momentum"):
        point = np.array(start, dtype=float)
        velocity = np.zeros_like(point)
        steps = 0
        for steps in range(1, 20001):
            slope = matrix @ point
            if method == "gradient descent":
                point = point - rate * slope
            else:
                velocity = 0.9 * velocity - rate * slope
                point = point + velocity
            if np.linalg.norm(point - target) < wanted:
                break
        found[method] = steps
    return {"plain": found["gradient descent"],
            "with momentum": found["momentum"],
            "condition number": stretch,
            "why": "die Querbewegung wechselt das Vorzeichen, die "
                   "Längsbewegung nicht"}


def rules_match_their_definition():
    """Prüft jeden Schritt gegen seine veröffentlichte Formel.

    Ein Schritt jedes Verfahrens wird von Hand nachgerechnet, aus dem
    Startpunkt und mit denselben Zahlen. Weicht die Rechnung im Modul
    ab, so ist eine Formel falsch abgeschrieben, und das fällt bei einem
    Verfahren, das trotzdem irgendwohin läuft, sonst nicht auf.

    Returns:
        Abbildung vom Verfahren auf das Urteil.
    """
    rate = 0.1
    decay = 0.9
    second = 0.999
    epsilon = 1e-8
    start = np.array(START, dtype=float)
    slope = gradient(start)
    wanted = {
        "gradient descent": start - rate * slope,
        "momentum": start + (-rate * slope),
        "nesterov": start + (-rate * gradient(start + decay
                                              * np.zeros_like(start))),
        "adagrad": start - rate * slope / (np.sqrt(slope ** 2) + epsilon),
        "rmsprop": start - rate * slope / (np.sqrt((1.0 - decay)
                                                   * slope ** 2)
                                           + epsilon),
    }
    first = (1.0 - decay) * slope / (1.0 - decay)
    scaled = (1.0 - second) * slope ** 2 / (1.0 - second)
    wanted["adam"] = start - rate * first / (np.sqrt(scaled) + epsilon)
    found = {}
    for method in METHODS:
        report = run(method, steps=1, rate=rate, decay=decay,
                     second=second, epsilon=epsilon)
        found[method] = bool(np.allclose(report["point"], wanted[method],
                                         atol=1e-10))
    return found


def why_the_rate_decreases(steps=4000, noise=1.0, seed=0):
    """Zeigt, warum die Schrittweite bei verrauschten Daten fallen muss.

    Mit einer festen Schrittweite springt das Verfahren um das Minimum
    herum, und zwar dauerhaft: der Gradient ist auch im Minimum nicht
    null, sondern nur im Mittel null. Eine Schrittweite, die wie eins
    durch die Schrittzahl fällt, lässt die Sprünge kleiner werden und
    das Verfahren stehenbleiben.

    Gemittelt wird über zwanzig Läufe, denn ein einzelner Lauf endet an
    einer zufälligen Stelle des Kreisens und sagt für sich nichts.

    Returns:
        Abbildung mit beiden Abständen zum Minimum.

    Raises:
        ValueError: bei einer nicht positiven Schrittzahl.
    """
    if steps <= 0:
        raise ValueError("die Schrittzahl muss positiv sein")
    optimum = closed_form()
    found = {"fixed": [], "decreasing": []}
    for run_index in range(20):
        rng = np.random.default_rng(seed + run_index)
        for name in found:
            point = np.array(START, dtype=float)
            for step in range(1, steps + 1):
                slope = gradient(point) + rng.normal(scale=noise, size=2)
                rate = 0.05 if name == "fixed" else 2.0 / step
                point = point - rate * slope
            found[name].append(float(np.linalg.norm(point - optimum)))
    return {"with a fixed rate": float(np.mean(found["fixed"])),
            "with a decreasing rate": float(np.mean(found["decreasing"])),
            "runs": len(found["fixed"]), "noise": noise,
            "why": "im Minimum ist der verrauschte Gradient nur im "
                   "Mittel null"}
