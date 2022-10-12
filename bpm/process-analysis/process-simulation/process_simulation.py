"""Prozesssimulation: Dauer, Kosten und Streuung aus vielen Fällen."""

import math
import random


def task(name, mean, deviation=0.0, resource=None):
    """Eine Aktivität mit normalverteilter Dauer.

    Args:
        name: der Name der Aktivität.
        mean: die mittlere Dauer.
        deviation: die Standardabweichung.
        resource: die Ressource, die sie ausführt.

    Raises:
        ValueError: bei einer negativen Dauer oder Abweichung.
    """
    if mean < 0 or deviation < 0:
        raise ValueError("negative Dauer")
    return {"type": "task", "name": name, "mean": mean,
            "deviation": deviation, "resource": resource}


def app_release(deviation=None):
    """Der App-Prozess aus Zettel 4 mit Zeiten, Kosten und Rollen.

    Die Planung schwankt um eine Stunde, die Veröffentlichung um eine
    halbe, die Fehlerbehebung um vier Stunden und die Entwicklung um einen
    Arbeitstag. Die Planung macht der Projektmanager für 55 Euro die
    Stunde, die Entwicklung die Entwickler für 50, die Veröffentlichung
    ein Werkstudent für 20.

    Args:
        deviation: setzt alle Abweichungen auf denselben Wert; ohne
            Angabe gelten die Zahlen des Blattes.

    Returns:
        Abbildung mit den Blöcken, den Fällen des inklusiven Gateways und
        den Stundensätzen.
    """
    def spread(value):
        """Nimmt die Abweichung des Blattes oder die vorgegebene."""
        return value if deviation is None else deviation

    return {
        "before": [task("Neue Version der App planen", 4, spread(1),
                        "Projektmanager")],
        "branches": [task("Bugs beheben", 6, spread(4), "Entwickler"),
                     task("Features entwickeln", 24, spread(8),
                          "Entwickler")],
        "cases": [(0.1, (1,)), (0.3, (0,)), (0.6, (0, 1))],
        "after": [task("Neue Version der App veröffentlichen", 2,
                       spread(0.5), "Werkstudent")],
        "rates": {"Projektmanager": 55.0, "Entwickler": 50.0,
                  "Werkstudent": 20.0},
    }


def _duration(activity, generator):
    """Zieht eine Dauer; negative Ziehungen werden auf null gesetzt."""
    if activity["deviation"] <= 0:
        return activity["mean"]
    return max(0.0, generator.gauss(activity["mean"],
                                    activity["deviation"]))


def _one_case(model, generator):
    """Spielt einen einzelnen Fall durch.

    Returns:
        Paar aus Dauer und Kosten.
    """
    duration = 0.0
    cost = 0.0
    for activity in model["before"]:
        drawn = _duration(activity, generator)
        duration += drawn
        cost += drawn * model["rates"][activity["resource"]]
    cut = generator.random()
    seen = 0.0
    chosen = model["cases"][-1][1]
    for probability, indices in model["cases"]:
        seen += probability
        if cut <= seen:
            chosen = indices
            break
    drawn = [_duration(model["branches"][index], generator)
             for index in chosen]
    duration += max(drawn)
    for index, value in zip(chosen, drawn):
        cost += value * model["rates"][model["branches"][index]["resource"]]
    for activity in model["after"]:
        drawn = _duration(activity, generator)
        duration += drawn
        cost += drawn * model["rates"][activity["resource"]]
    return duration, cost


def run(model, runs=1000, seed=0, buckets=10):
    """Simuliert viele Fälle und fasst sie zusammen.

    Die parallelen Zweige kosten beide, dauern aber nur so lange wie der
    längere. Deshalb steigen die Kosten mit jedem Zweig, die Dauer nicht;
    genau das trennt die Simulation von einer Rechnung mit Mittelwerten.

    Args:
        model: die Beschreibung aus ``app_release``.
        runs: die Zahl der Fälle.
        seed: der Startwert des Zufallsgenerators.
        buckets: die Zahl der Klassen des Histogramms.

    Returns:
        Abbildung mit Mittelwerten, Streuung, Spanne und Histogramm.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Fällen oder
            Klassen.
    """
    if runs < 1:
        raise ValueError("mindestens ein Fall")
    if buckets < 1:
        raise ValueError("mindestens eine Klasse")
    generator = random.Random(seed)
    durations = []
    costs = []
    for _ in range(runs):
        duration, cost = _one_case(model, generator)
        durations.append(duration)
        costs.append(cost)
    mean = sum(durations) / runs
    variance = sum((value - mean) ** 2 for value in durations) / runs
    low, high = min(durations), max(durations)
    width = (high - low) / buckets if high > low else 1.0
    histogram = {}
    for value in durations:
        index = min(buckets - 1, int((value - low) / width))
        key = round(low + index * width, 3)
        histogram[key] = histogram.get(key, 0) + 1
    return {"mean duration": mean, "deviation": math.sqrt(variance),
            "mean cost": sum(costs) / runs,
            "shortest": low, "longest": high,
            "histogram": histogram, "runs": runs}


def what_to_watch_out_for():
    """Nennt die Vorbehalte, die die Vorlesung der Simulation mitgibt.

    Die Ergebnisse ruhen auf einem Modell und auf vereinfachten Annahmen,
    sie hängen an der Genauigkeit der eingegebenen Zahlen, und Menschen
    sind keine Roboter. Deshalb: Sensitivitätsprüfungen rechnen und die
    Zahlen mit den Beteiligten gegenprüfen.
    """
    return {"rests on": "a model and simplified assumptions",
            "sensitive to": "the accuracy of the input numbers",
            "people": "are not machines and do not work at a constant rate",
            "remedy": ["run a sensitivity check",
                       "check the numbers with the people involved",
                       "repeat for alternative scenarios"]}


def tools():
    """Nennt die Werkzeuge aus der Vorlesung."""
    return ["BIMP", "Appian", "ARIS", "IBM BPM",
            "Oracle Geschäftsprozessanalyse", "Signavio Prozess-Manager"]
