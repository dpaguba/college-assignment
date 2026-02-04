"""Budget statt Vollausbau."""

import math

import numpy as np


def rungs(configurations=27, factor=3, budget=1):
    """Rechnet die Stufen aus: wie viele bleiben, mit wie viel Budget.

    Auf jeder Stufe überlebt ein Bruchteil der Einstellungen, und die
    Überlebenden bekommen das Vielfache an Budget. Beide Zahlen ändern
    sich mit demselben Faktor, deshalb kostet jede Stufe ungefähr
    gleich viel, und das ist die ganze Idee: das Budget wird nicht
    gespart, sondern umverteilt.

    Args:
        configurations: die Zahl der Einstellungen am Anfang.
        factor: um welchen Faktor je Stufe ausgedünnt wird.
        budget: das Budget je Einstellung auf der ersten Stufe.

    Returns:
        Liste mit einer Zeile je Stufe.

    Raises:
        ValueError: bei einem Faktor unter zwei oder keiner Einstellung.
    """
    if factor < 2:
        raise ValueError("der Faktor ist mindestens zwei")
    if configurations < 1 or budget < 1:
        raise ValueError("Einstellungen und Budget müssen positiv sein")
    found = []
    left = configurations
    each = budget
    while left >= 1:
        found.append({"configurations": left, "budget each": each,
                      "total": left * each})
        if left == 1:
            break
        left = left // factor
        each = each * factor
    return found


def against_the_full_run(configurations=81, factor=3, budget=1):
    """Vergleicht die Ausgabe mit dem vollen Durchlauf aller Einstellungen.

    Der volle Durchlauf gibt jeder Einstellung das grösste Budget. Das
    Ausdünnen gibt es nur der letzten und spart damit fast alles, ohne
    die Zahl der geprüften Einstellungen zu senken.

    Returns:
        Abbildung mit beiden Summen.

    Raises:
        ValueError: wie bei ``rungs``.
    """
    stairs = rungs(configurations, factor, budget)
    largest = stairs[-1]["budget each"]
    return {"spent by halving": sum(row["total"] for row in stairs),
            "spent by the full run": configurations * largest,
            "rungs": len(stairs), "largest budget": largest,
            "saving": 1.0 - sum(row["total"] for row in stairs)
            / (configurations * largest)}


def the_late_bloomer(configurations=27, factor=3, seed=0):
    """Zeigt die Einstellung, die das Verfahren nicht finden kann.

    Eine Einstellung, die früh schlecht aussieht und spät die beste
    wäre, wird auf der ersten Stufe abgeschnitten und kommt nie wieder.
    Das Verfahren nimmt an, dass die Reihenfolge nach kurzem Budget
    etwas über die Reihenfolge nach langem sagt. Für viele
    Lernverfahren stimmt das ungefähr, und für solche mit einer langen
    Anlaufzeit stimmt es nicht.

    Returns:
        Abbildung mit dem Rang der Einstellung früh und spät.
    """
    rng = np.random.default_rng(seed)
    early = rng.uniform(size=configurations)
    late = early + rng.normal(scale=0.05, size=configurations)
    early[0] = 0.02
    late[0] = 1.5
    order = np.argsort(-early)
    survivors = order[:configurations // factor]
    return {"rank early": int(np.where(order == 0)[0][0]),
            "rank late": int(np.where(np.argsort(-late) == 0)[0][0]),
            "survives": bool(0 in survivors.tolist()),
            "configurations": configurations,
            "the assumption": "die Reihenfolge nach kurzem Budget sagt "
                              "etwas über die nach langem"}


def hyperband(budget=81, factor=3):
    """Verteilt das Budget auf mehrere Läufe mit verschiedenem Anfang.

    Ein einzelner Durchlauf muss sich entscheiden: viele Einstellungen
    mit wenig Budget, oder wenige mit viel. Beides ist manchmal richtig,
    und welches, weiss man vorher nicht. Hyperband führt deshalb mehrere
    Durchläufe mit verschiedenen Anfangszahlen aus und gibt jedem
    ungefähr dasselbe Gesamtbudget.

    Args:
        budget: das grösste Budget je Einstellung.
        factor: der Faktor des Ausdünnens.

    Returns:
        Abbildung mit den Durchläufen.

    Raises:
        ValueError: bei einem Faktor unter zwei oder einem zu kleinen
            Budget.
    """
    if factor < 2:
        raise ValueError("der Faktor ist mindestens zwei")
    if budget < factor:
        raise ValueError("das Budget ist kleiner als der Faktor")
    rounds = int(math.floor(math.log(budget, factor)))
    brackets = []
    for index in range(rounds, -1, -1):
        configurations = int(math.ceil((rounds + 1) / (index + 1)
                                       * factor ** index))
        start = budget / factor ** index
        brackets.append({"configurations": configurations,
                         "budget each": start,
                         "rungs": index + 1})
    return {"brackets": brackets, "rounds": rounds + 1,
            "why several": "ob viele mit wenig oder wenige mit viel "
                           "besser ist, weiss man vorher nicht"}


def what_it_assumes():
    """Nennt die Annahme und wo sie bricht.

    Dass die Reihenfolge der Einstellungen bei kleinem Budget ungefähr
    die bei grossem vorhersagt. Bricht sie, so schneidet das Verfahren
    genau die Einstellung ab, die es finden sollte, und merkt es nicht,
    weil es keine Möglichkeit hat, eine abgeschnittene Einstellung
    zurückzuholen.

    Prüfen lässt sich die Annahme nur, indem man ein paar abgeschnittene
    Einstellungen doch zu Ende rechnet, und dieser Aufwand wird selten
    getrieben.
    """
    return {"the assumption": "die Reihenfolge bei kleinem Budget sagt "
                              "die bei grossem vorher",
            "what happens when it breaks": "die gesuchte Einstellung "
                                           "wird früh abgeschnitten",
            "why it is not noticed": "eine abgeschnittene Einstellung "
                                     "kommt nie zurück",
            "how to check": "einige abgeschnittene doch zu Ende rechnen"}
