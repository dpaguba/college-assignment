"""Nacharbeit: was eine Schleife die Durchlaufzeit kostet."""

import random


def repetitions(repeat, at_least_once=True):
    """Die mittlere Zahl der Durchläufe eines Schleifenrumpfes.

    Läuft der Rumpf mindestens einmal und danach mit Wahrscheinlichkeit r
    erneut, so ist die Zahl der Durchläufe geometrisch verteilt und ihr
    Mittelwert 1/(1 − r). Wird der Rumpf nur bei Bedarf betreten, fällt
    der erste Durchlauf weg und es bleibt r/(1 − r).

    Args:
        repeat: die Wahrscheinlichkeit einer Wiederholung.
        at_least_once: ob der Rumpf in jedem Fall einmal läuft.

    Raises:
        ValueError: bei einer Wahrscheinlichkeit ausserhalb von null bis
            unter eins.
    """
    if not 0.0 <= repeat < 1.0:
        raise ValueError("die Wiederholung liegt ausserhalb von 0 bis unter 1")
    full = 1.0 / (1.0 - repeat)
    return full if at_least_once else full - 1.0


def cycle_time(body, repeat, at_least_once=True):
    """Die Durchlaufzeit einer Schleife.

    Raises:
        ValueError: bei einer negativen Rumpfzeit oder einer unzulässigen
            Wahrscheinlichkeit.
    """
    if body < 0:
        raise ValueError("negative Zeit")
    return body * repetitions(repeat, at_least_once)


def simulate(repeat, runs=100000, seed=0):
    """Misst die Zahl der Durchläufe durch Nachspielen.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Durchläufen.
    """
    if runs < 1:
        raise ValueError("mindestens ein Durchlauf")
    generator = random.Random(seed)
    total = 0
    for _ in range(runs):
        total += 1
        while generator.random() < repeat:
            total += 1
    return total / runs


def table(rates=(0.0, 0.1, 0.2, 0.5, 0.9)):
    """Zeigt, wie die Kosten der Nacharbeit wachsen.

    Der Zusammenhang ist nicht linear: von zehn auf zwanzig Prozent kostet
    wenig, von fünfzig auf neunzig Prozent verfünffacht sich der Rumpf.

    Returns:
        Abbildung von der Rate auf die Zahl der Durchläufe.
    """
    return {rate: repetitions(rate) for rate in rates}


def where_it_comes_from():
    """Nennt, woher Nacharbeit im Verwaltungsprozess stammt."""
    return {"incomplete input": "ein Formular ohne Pflichtangaben",
            "failed check": "eine Prüfung, die nicht besteht",
            "rejected approval": "eine Freigabe, die zurückgeht",
            "cheapest fix": "die Eingabe prüfen, bevor der Fall beginnt"}
