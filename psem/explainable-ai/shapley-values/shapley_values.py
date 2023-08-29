"""Shapley-Werte: die exakte Aufteilung eines Ergebnisses auf Beteiligte."""

import itertools
import math


def shapley(players, value):
    """Rechnet die Shapley-Werte einer Koalitionsfunktion aus.

    Der Wert eines Spielers ist sein mittlerer Beitrag über alle
    Reihenfolgen, in denen die Spieler eintreten können. Gerechnet wird
    als gewichtete Summe über alle Teilmengen ohne ihn; das Gewicht ist
    der Anteil der Reihenfolgen, in denen genau diese Teilmenge vor ihm
    da ist.

    Args:
        players: die Beteiligten.
        value: eine Funktion von einer Teilmenge auf ihren Wert.

    Returns:
        Abbildung vom Spieler auf seinen Wert.

    Raises:
        ValueError: ohne Beteiligte.
    """
    names = list(players)
    if not names:
        raise ValueError("keine Beteiligten")
    count = len(names)
    result = {}
    for name in names:
        others = [other for other in names if other != name]
        total = 0.0
        for size in range(len(others) + 1):
            weight = (math.factorial(size)
                      * math.factorial(count - size - 1)
                      / math.factorial(count))
            for group in itertools.combinations(others, size):
                with_him = value(frozenset(group) | {name})
                without = value(frozenset(group))
                total += weight * (with_him - without)
        result[name] = total
    return result


def efficiency(players, value):
    """Prüft, dass die Werte das Ganze aufteilen.

    Die Summe der Shapley-Werte ist der Wert der vollen Koalition minus
    dem der leeren. Nichts geht verloren und nichts kommt hinzu; das ist
    die Eigenschaft, die eine Erklärung überhaupt zu einer Aufteilung
    macht.

    Raises:
        ValueError: ohne Beteiligte.
    """
    values = shapley(players, value)
    whole = value(frozenset(players)) - value(frozenset())
    return {"sum": sum(values.values()), "whole": whole,
            "holds": abs(sum(values.values()) - whole) < 1e-9}


def symmetry(players, value, first, second):
    """Prüft, dass zwei austauschbare Spieler denselben Wert bekommen.

    Austauschbar heisst: zu jeder Koalition ohne die beiden trägt der
    eine genauso viel bei wie der andere.

    Raises:
        ValueError: bei einem unbekannten Spieler.
    """
    names = list(players)
    for name in (first, second):
        if name not in names:
            raise ValueError("unbekannter Spieler: %s" % name)
    others = [name for name in names if name not in (first, second)]
    same = True
    for size in range(len(others) + 1):
        for group in itertools.combinations(others, size):
            base = frozenset(group)
            if abs(value(base | {first}) - value(base | {second})) > 1e-9:
                same = False
    values = shapley(players, value)
    return {"interchangeable": same,
            "equal values": abs(values[first] - values[second]) < 1e-9,
            "values": {first: values[first], second: values[second]}}


def dummy(players, value, name):
    """Prüft, dass ein Spieler ohne Beitrag den Wert null bekommt.

    Raises:
        ValueError: bei einem unbekannten Spieler.
    """
    names = list(players)
    if name not in names:
        raise ValueError("unbekannter Spieler")
    others = [other for other in names if other != name]
    contributes = False
    for size in range(len(others) + 1):
        for group in itertools.combinations(others, size):
            base = frozenset(group)
            if abs(value(base | {name}) - value(base)) > 1e-9:
                contributes = True
    return {"contributes nothing": not contributes,
            "value": shapley(players, value)[name]}


def additivity(players, first, second):
    """Prüft, dass sich die Werte zweier Spiele addieren.

    Wer zwei Spiele nebeneinander spielt, bekommt in der Summe so viel
    wie in beiden einzeln. Daran hängt in der Praxis, dass sich die
    Erklärung eines zusammengesetzten Modells aus den Erklärungen seiner
    Teile ergibt.

    Raises:
        ValueError: ohne Beteiligte.
    """
    left = shapley(players, first)
    right = shapley(players, second)
    both = shapley(players, lambda group: first(group) + second(group))
    return {"holds": all(abs(both[name] - left[name] - right[name]) < 1e-9
                         for name in left),
            "separate": {name: left[name] + right[name] for name in left},
            "together": both}


def glove_game():
    """Ein Spiel, in dem der Wert nicht am Beitrag der Einzelnen hängt.

    Zwei Spieler haben einen linken Handschuh, einer einen rechten. Ein
    Paar ist einen Euro wert, einzelne Handschuhe nichts. Der Besitzer
    des rechten Handschuhs bekommt zwei Drittel, die beiden anderen je
    ein Sechstel: die knappe Seite ist mehr wert, obwohl alle drei
    dieselbe Menge beitragen.

    Returns:
        Abbildung mit den Werten.
    """
    def value(group):
        """Ein Paar ist einen Euro wert."""
        left = len({"L1", "L2"} & set(group))
        right = len({"R"} & set(group))
        return float(min(left, right))

    return shapley(["L1", "L2", "R"], value)


def why_this_and_not_something_else():
    """Nennt, was die Shapley-Werte auszeichnet.

    Sie sind die einzige Aufteilung, die alle vier Eigenschaften zugleich
    erfüllt: Effizienz, Symmetrie, den Nullbeitrag und die Additivität.
    Jede andere Aufteilung verletzt mindestens eine, und deshalb ist die
    Wahl keine Geschmacksfrage.

    Der Preis steht daneben: die Rechnung geht über alle Teilmengen, also
    über zwei hoch n. Bei zwanzig Merkmalen ist das eine Million
    Auswertungen des Modells je erklärter Vorhersage.
    """
    return {"unique under": ["Effizienz", "Symmetrie", "Nullbeitrag",
                             "Additivität"],
            "cost": "2 hoch n Auswertungen",
            "at 20 features": 2 ** 20,
            "consequence": "in der Praxis wird genähert, und die Näherung "
                           "erbt die Eigenschaften nur ungefähr"}
