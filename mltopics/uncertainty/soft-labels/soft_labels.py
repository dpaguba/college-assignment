"""Was die Mehrheitsmarke wegwirft."""

import math

EXAMPLE = {"clear": {"deer": 48, "dog": 1, "horse": 1},
           "contested": {"deer": 33, "dog": 13, "horse": 4}}


def soft_label(votes):
    """Wandelt die Stimmen in eine Verteilung um.

    Raises:
        ValueError: bei einer leeren Abstimmung oder negativen Stimmen.
    """
    total = sum(votes.values())
    if total <= 0 or any(count < 0 for count in votes.values()):
        raise ValueError("leere oder unzulässige Abstimmung")
    return {name: count / total for name, count in votes.items()}


def hard_label(votes):
    """Nennt die Klasse mit den meisten Stimmen.

    Raises:
        ValueError: bei einer leeren Abstimmung.
    """
    if not votes:
        raise ValueError("leere Abstimmung")
    return max(votes, key=lambda name: (votes[name], name))


def entropy(distribution):
    """Die Entropie einer Verteilung, in Bit."""
    total = 0.0
    for value in distribution.values():
        if value > 0.0:
            total -= value * math.log2(value)
    return total


def cross_entropy(prediction, target):
    """Der Verlust zwischen einer Vorhersage und einem Ziel.

    Raises:
        ValueError: bei verschiedenen Klassen.
    """
    if set(prediction) != set(target):
        raise ValueError("die Klassen stimmen nicht überein")
    total = 0.0
    for name, weight in target.items():
        if weight > 0.0:
            total -= weight * math.log(max(prediction[name], 1e-12))
    return total


def what_aggregation_loses():
    """Zeigt zwei Fälle, die dieselbe Marke und nichts sonst teilen.

    Beide Bilder werden mehrheitlich als Hirsch benannt, und nach der
    Aggregation sind sie ununterscheidbar. In den Stimmen steht ein
    grosser Unterschied: das eine ist eindeutig, das andere hat ein
    Drittel Widerspruch. Diese Information ist erhoben worden und wird
    beim Zusammenfassen weggeworfen.

    Returns:
        Abbildung mit beiden Fällen.
    """
    clear = soft_label(EXAMPLE["clear"])
    contested = soft_label(EXAMPLE["contested"])
    return {"hard label of the clear one": hard_label(EXAMPLE["clear"]),
            "hard label of the contested one":
                hard_label(EXAMPLE["contested"]),
            "same hard label": hard_label(EXAMPLE["clear"])
            == hard_label(EXAMPLE["contested"]),
            "entropy of the clear one": entropy(clear),
            "entropy of the contested one": entropy(contested),
            "soft label of the contested one": contested,
            "what is lost": "der erhobene Widerspruch"}


def soft_loss_follows_the_crowd():
    """Misst den Verlust eines gut geeichten Modells auf beiden Fällen.

    Ein Modell, das die Verteilung der Stimmen trifft, hat auf dem
    umstrittenen Fall einen höheren Verlust als auf dem klaren, und das
    ist richtig so: der umstrittene Fall ist wirklich unsicherer. Der
    Verlust gegen die harte Marke würde das Gegenteil nahelegen.

    Returns:
        Abbildung mit beiden Verlusten.
    """
    found = {}
    for name in ("clear", "contested"):
        target = soft_label(EXAMPLE[name])
        found[name] = cross_entropy(target, target)
    return {"loss on the clear case": found["clear"],
            "loss on the contested one": found["contested"],
            "why": "der umstrittene Fall ist wirklich unsicherer",
            "the floor": "der Verlust kann die Entropie der Stimmen "
                         "nicht unterschreiten"}


def confidence_costs_on_contested_cases():
    """Vergleicht ein sicheres und ein zurückhaltendes Modell.

    Auf einem umstrittenen Fall sagt das eine Modell mit fast voller
    Sicherheit die Mehrheitsklasse, das andere gibt die Verteilung der
    Stimmen wieder. Gegen die weichen Marken gemessen ist das
    zurückhaltende Modell besser, gegen die harte Marke das sichere.

    Damit hängt die Rangfolge der beiden Modelle allein daran, welche
    Marke zum Messen genommen wird, und diese Wahl wird selten als
    Entscheidung behandelt.

    Returns:
        Abbildung mit beiden Verlusten für beide Modelle.
    """
    votes = EXAMPLE["contested"]
    target = soft_label(votes)
    winner = hard_label(votes)
    hard = {name: (1.0 if name == winner else 0.0) for name in votes}
    confident = {name: (0.97 if name == winner else 0.015)
                 for name in votes}
    hedging = dict(target)
    return {"loss of the confident model": cross_entropy(confident,
                                                         target),
            "loss of the hedging model": cross_entropy(hedging, target),
            "hard loss of the confident model": cross_entropy(confident,
                                                              hard),
            "hard loss of the hedging model": cross_entropy(hedging,
                                                            hard),
            "which model wins": "je nach Marke ein anderes",
            "why": "die Wahl der Marke entscheidet die Rangfolge"}


def why_this_matters_for_uncertainty():
    """Verbindet die weichen Marken mit der Messung von Unsicherheit.

    Wer eine Unsicherheitsschätzung prüfen will, braucht etwas, wogegen
    er sie hält. Bei aggregierten Marken gibt es das nicht: jeder Fall
    ist entweder richtig oder falsch, und die Schätzung lässt sich nur
    über ihre Wirkung prüfen. Mit den Stimmen liegt eine gemessene
    Unsicherheit vor, und sie lässt sich direkt vergleichen.

    Das ist der Grund, warum Datensätze mit erhaltenen Einzelstimmen für
    diese Frage so viel wertvoller sind als ihre Grösse vermuten lässt.
    """
    return {"the problem": "gegen aggregierte Marken lässt sich eine "
                           "Unsicherheit nur mittelbar prüfen",
            "what the votes give": "eine gemessene Unsicherheit je Fall",
            "why the datasets are valuable": "nicht wegen ihrer Grösse",
            "the risk": "die Stimmen messen die Uneinigkeit von "
                        "Menschen, nicht die der Aufgabe"}
