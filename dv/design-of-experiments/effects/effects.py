"""Haupt- und Wechselwirkungseffekte aus einer Zweifaktortafel."""


def _values(table):
    """Ordnet die vier Zellen der Tafel den Vorzeichenpaaren zu.

    Raises:
        ValueError: wenn eine der vier Kombinationen fehlt.
    """
    wanted = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    if any(key not in table for key in wanted):
        raise ValueError("die Tafel ist nicht vollstaendig")
    return {key: float(table[key]) for key in wanted}


def main_effect(table, factor):
    """Berechnet den Haupteffekt eines der beiden Faktoren.

    Der Effekt ist die mittlere Änderung des Ertrags, wenn der Faktor von
    der unteren auf die obere Stufe wechselt, gemittelt über die Stufen
    des anderen Faktors.

    Raises:
        ValueError: bei einer unvollständigen Tafel oder falschem Index.
    """
    if factor not in (0, 1):
        raise ValueError("es gibt nur zwei Faktoren")
    cells = _values(table)
    high = [value for key, value in cells.items() if key[factor] > 0]
    low = [value for key, value in cells.items() if key[factor] < 0]
    return sum(high) / len(high) - sum(low) / len(low)


def interaction(table):
    """Berechnet den Wechselwirkungseffekt.

    Der Effekt ist die Differenz der beiden Differenzen: wie stark der
    Einfluss des ersten Faktors davon abhängt, auf welcher Stufe der
    zweite steht.
    """
    cells = _values(table)
    upper = cells[(1, 1)] - cells[(-1, 1)]
    lower = cells[(1, -1)] - cells[(-1, -1)]
    return (upper - lower) / 2


def average(table):
    """Mittlerer Ertrag über alle vier Zellen."""
    cells = _values(table)
    return sum(cells.values()) / 4


def model(table):
    """Stellt das lineare Modell mit Wechselwirkung auf.

    Returns:
        Abbildung mit dem Mittelwert und den drei halben Effekten, wie sie
        als Koeffizienten in die Vorhersage eingehen.
    """
    return {"mean": average(table),
            "a": main_effect(table, 0) / 2,
            "b": main_effect(table, 1) / 2,
            "ab": interaction(table) / 2}


def predict(parameters, first, second):
    """Sagt den Ertrag für eine Stufenkombination voraus."""
    return (parameters["mean"] + parameters["a"] * first
            + parameters["b"] * second
            + parameters["ab"] * first * second)


def model_reproduces(table):
    """Prüft, ob das volle Modell die Tafel genau wiedergibt.

    Vier Zellen und vier Parameter: das Modell mit Wechselwirkung trifft
    jede Zelle ohne Rest.
    """
    parameters = model(table)
    for (first, second), value in _values(table).items():
        if abs(predict(parameters, first, second) - value) > 1e-9:
            return False
    return True


def ignoring_the_interaction(table):
    """Misst, was ein Modell ohne Wechselwirkung danebenliegt.

    Returns:
        Abbildung mit dem grössten Fehler und der Zelle, in der er auftritt.
    """
    parameters = dict(model(table))
    parameters["ab"] = 0.0
    worst = 0.0
    where = None
    for (first, second), value in _values(table).items():
        error = abs(predict(parameters, first, second) - value)
        if error > worst:
            worst = error
            where = (first, second)
    return {"largest error": worst, "cell": where}


def reading():
    """Beschreibt, woran eine Wechselwirkung im Bild zu erkennen ist."""
    return {"no interaction": "the two lines are parallel",
            "interaction": "the lines have different slopes or cross"}
