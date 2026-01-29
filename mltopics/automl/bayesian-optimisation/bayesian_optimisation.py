"""Die Schleife der bayesschen Optimierung."""

import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _name in (("..", "gaussian-process"), ("..", "expected-improvement")):
    sys.path.insert(0, os.path.join(_HERE, *_name))

import expected_improvement as acquisition
import gaussian_process as gp

LOW = -2.0

HIGH = 10.0

OPTIMUM = 1.878166


def target(point):
    """Die Zielfunktion des Beispiels.

    Eine glatte Funktion mit mehreren örtlichen Gipfeln, damit eine
    Suche, die nur bergauf geht, hängen bleibt. Der höchste Punkt liegt
    bei etwa 1.878 und ist geschlossen nicht ablesbar, also wird er
    einmal über zwei Millionen Stellen bestimmt und danach als bekannt
    behandelt. Die Prüfung rechnet ihn nach.
    """
    values = np.asarray(point, dtype=float)
    return (np.sin(values) + np.sin(values * 0.6)
            - 0.02 * (values - 3.0) ** 2)


def best_on_a_fine_grid(steps=2000001):
    """Bestimmt den Gipfel durch feines Abtasten."""
    grid = np.linspace(LOW, HIGH, steps)
    return float(grid[int(np.argmax(target(grid)))])


def run(steps=25, start=4, seed=0, length=1.2, grid=400):
    """Führt die Schleife aus: schätzen, wählen, messen.

    Die ersten Punkte werden gewürfelt, weil ein Modell aus null
    Beobachtungen nichts sagt. Danach schlägt die Erwerbsfunktion die
    nächste Stelle vor, sie wird gemessen, das Modell wird neu
    angepasst, und das wiederholt sich.

    Args:
        steps: das Gesamtbudget an Messungen.
        start: wie viele davon zufällig gewählt werden.
        seed: der Startwert.
        length: die Längenskala des Modells.
        grid: die Feinheit, mit der die Erwerbsfunktion durchsucht wird.

    Returns:
        Abbildung mit dem besten gefundenen Punkt und dem Verlauf.

    Raises:
        ValueError: bei einem nicht positiven Budget oder einem Start,
            der grösser ist als das Budget.
    """
    if steps <= 0:
        raise ValueError("das Budget muss positiv sein")
    if start > steps or start < 1:
        raise ValueError("der zufällige Anfang passt nicht ins Budget")
    rng = np.random.default_rng(seed)
    points = list(rng.uniform(LOW, HIGH, size=start))
    values = list(target(np.array(points)))
    candidates = np.linspace(LOW, HIGH, grid).reshape(-1, 1)
    for _ in range(steps - start):
        report = gp.posterior(np.array(points).reshape(-1, 1),
                              np.array(values), candidates, length=length)
        best = max(values)
        scores = [acquisition.expected_improvement(float(mean),
                                                   float(deviation), best)
                  for mean, deviation in zip(report["mean"],
                                             report["deviation"])]
        chosen = float(candidates[int(np.argmax(scores))][0])
        points.append(chosen)
        values.append(float(target(chosen)))
    index = int(np.argmax(values))
    return {"best point": points[index], "best value": values[index],
            "steps": steps, "random start": start,
            "regret": float(target(OPTIMUM)) - values[index],
            "points": points}


def _random_search(steps, seed):
    """Misst an gewürfelten Stellen."""
    rng = np.random.default_rng(seed)
    points = rng.uniform(LOW, HIGH, size=steps)
    return float(np.max(target(points)))


def _grid_search(steps):
    """Misst auf einem gleichmässigen Gitter."""
    return float(np.max(target(np.linspace(LOW, HIGH, steps))))


def against_the_baselines(budget=25, runs=20):
    """Vergleicht die Schleife mit Würfeln und mit einem Gitter.

    Verglichen wird das Bedauern, also der Abstand zum wahren Gipfel,
    bei gleichem Budget. Das Gitter bekommt genauso viele Messungen und
    ist deterministisch; die anderen beiden werden über mehrere Läufe
    gemittelt.

    Returns:
        Abbildung mit dem mittleren Bedauern je Verfahren.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Läufen.
    """
    if runs <= 0:
        raise ValueError("die Zahl der Läufe muss positiv sein")
    peak = float(target(OPTIMUM))
    smart = float(np.mean([run(steps=budget, seed=index)["regret"]
                           for index in range(runs)]))
    random = float(np.mean([peak - _random_search(budget, index)
                            for index in range(runs)]))
    return {"bayesian": smart, "random": random,
            "grid": peak - _grid_search(budget),
            "budget": budget, "runs": runs, "peak": peak}


def the_advantage_is_early(small=15, large=120, runs=12):
    """Zeigt, wo der Vorsprung liegt und wo er verschwindet.

    Bei kleinem Budget ist der Unterschied gross, weil jede Messung
    zählt. Bei grossem Budget findet auch das Würfeln den Gipfel,
    und der Vorsprung schrumpft. Das ist keine Schwäche des Verfahrens,
    sondern die Aussage darüber, wofür es gebaut ist: teure Messungen
    und wenige davon.

    Returns:
        Abbildung mit dem Vorsprung bei beiden Budgets.
    """
    peak = float(target(OPTIMUM))
    found = {}
    for name, budget in (("small", small), ("large", large)):
        smart = float(np.mean([run(steps=budget, seed=index)["regret"]
                               for index in range(runs)]))
        random = float(np.mean([peak - _random_search(budget, index)
                                for index in range(runs)]))
        found[name] = random - smart
    return {"advantage at a small budget": found["small"],
            "advantage at a large budget": found["large"],
            "budgets": (small, large),
            "what it is built for": "teure Messungen und wenige davon"}


def what_the_model_assumes():
    """Nennt, was die Schleife über die Zielfunktion voraussetzt.

    Dass sie glatt ist im Sinne der gewählten Kovarianzfunktion, also
    dass nahe Stellen ähnliche Werte haben. Trifft das nicht zu, sagt
    das Modell nichts Brauchbares vorher, die Erwerbsfunktion sucht ins
    Leere, und das Verfahren ist schlechter als Würfeln, weil es sich in
    eine Gegend verrennt.

    Für Hyperparameter ist die Annahme meist vertretbar und für
    kategoriale Parameter nicht, und das ist der Grund, warum dort
    andere Modelle verwendet werden.
    """
    return {"the assumption": "nahe Einstellungen geben ähnliche "
                              "Ergebnisse",
            "when it fails": "das Verfahren ist schlechter als Würfeln",
            "why": "es verrennt sich in eine Gegend",
            "where it does not hold": "bei kategorialen Parametern"}
