"""Schleifen und die Stellen, an denen sie sich unterscheiden."""


def for_next(first, last, step=1):
    """Bildet ``For i = first To last Step step`` nach.

    Die Schleife prüft vor jedem Durchlauf; bei einem Schritt in die
    falsche Richtung läuft sie deshalb kein einziges Mal, statt endlos zu
    laufen.

    Returns:
        Die Werte, die die Laufvariable annimmt.

    Raises:
        ValueError: bei einer Schrittweite von null.
    """
    if step == 0:
        raise ValueError("die Schrittweite darf nicht null sein")
    values = []
    current = first
    while (current <= last) if step > 0 else (current >= last):
        values.append(current)
        current += step
    return values


def value_after_the_loop(first, last, step=1):
    """Nennt den Wert der Laufvariablen nach dem Ende.

    In VBA lebt sie weiter und steht auf dem ersten Wert, der die
    Bedingung verletzt: nach ``For i = 1 To 10`` ist i gleich elf, nicht
    zehn. Wer danach mit i weiterrechnet, rechnet mit einem Wert, den die
    Schleife nie bearbeitet hat.

    Raises:
        ValueError: bei einer Schrittweite von null.
    """
    values = for_next(first, last, step)
    return values[-1] + step if values else first


def do_while(condition, body, state, limit=1000):
    """Bildet ``Do While ... Loop`` nach: die Prüfung steht vorn.

    Args:
        condition: prüft den Zustand.
        body: liefert den nächsten Zustand.
        state: der Anfangszustand.
        limit: obere Schranke gegen eine endlose Schleife.

    Returns:
        Abbildung mit dem Endzustand und der Zahl der Durchläufe.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    passes = 0
    while condition(state):
        state = body(state)
        passes += 1
        if passes >= limit:
            raise ValueError("die Schleife erreicht die Schranke")
    return {"state": state, "passes": passes}


def do_loop_while(condition, body, state, limit=1000):
    """Bildet ``Do ... Loop While`` nach: die Prüfung steht hinten.

    Der Unterschied zur vorderen Prüfung zeigt sich nur in einem Fall,
    und in dem immer: ist die Bedingung von Anfang an falsch, läuft die
    vordere Form null mal und die hintere einmal.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    passes = 0
    while True:
        state = body(state)
        passes += 1
        if passes >= limit:
            raise ValueError("die Schleife erreicht die Schranke")
        if not condition(state):
            break
    return {"state": state, "passes": passes}


def until_against_while(start):
    """Zeigt, dass Until die verneinte Bedingung von While ist.

    ``Do Until x > 5`` läuft genauso lange wie ``Do While x <= 5``. Die
    beiden Formen sind gleichwertig, und die Wahl ist eine Frage der
    Lesbarkeit: man schreibt die, deren Bedingung ohne Verneinung
    auskommt.

    Returns:
        Abbildung mit beiden Durchlaufzahlen.
    """
    def step(value):
        """Erhöht den Wert um eins."""
        return value + 1

    while_form = do_while(lambda value: value <= 5, step, start)
    until_form = do_while(lambda value: not value > 5, step, start)
    return {"while": while_form["passes"], "until": until_form["passes"],
            "equal": while_form["passes"] == until_form["passes"]}


def the_empty_range():
    """Zeigt, was bei einer leeren Schleife herauskommt.

    ``For i = 5 To 1`` läuft nicht, weil die Bedingung schon beim ersten
    Durchgang verletzt ist. Erst mit ``Step -1`` läuft sie rückwärts. Wer
    die Schrittweite vergisst, bekommt keine Fehlermeldung, sondern eine
    Schleife, die nichts tut, und das ist schwer zu sehen.

    Returns:
        Abbildung mit beiden Fällen.
    """
    return {"without step": for_next(5, 1),
            "with step minus one": for_next(5, 1, -1),
            "silent": "die leere Schleife meldet nichts"}
