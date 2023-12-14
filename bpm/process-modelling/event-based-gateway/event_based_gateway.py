"""Das ereignisbasierte Gateway und das Rennen zwischen den Zweigen."""

DECIDED_BY = {
    "data based": "the value of a data object",
    "event based": "whichever event occurs first",
}

EVENT_KINDS = ("message", "timer", "signal", "condition")


def decided_by(kind):
    """Sagt, woran ein Gateway entscheidet.

    Das datenbasierte Gateway wertet eine Bedingung aus und wählt danach.
    Das ereignisbasierte wählt nicht selbst: es wartet, und der Zweig, auf
    dem zuerst etwas eintrifft, gewinnt.

    Raises:
        ValueError: bei einer unbekannten Art.
    """
    if kind not in DECIDED_BY:
        raise ValueError("unbekannte Gateway-Art")
    return DECIDED_BY[kind]


def check_branches(branches):
    """Prüft, dass jeder Zweig mit einem Ereignis beginnt.

    Hinter einem ereignisbasierten Gateway darf keine Aufgabe stehen: das
    Gateway entscheidet nicht, sondern wartet, und warten kann es nur auf
    ein Ereignis. Eine Aufgabe würde sofort beginnen und damit die
    Entscheidung vorwegnehmen.

    Args:
        branches: die Arten der ersten Knoten der Zweige.

    Returns:
        Die geprüfte Liste.

    Raises:
        ValueError: bei weniger als zwei Zweigen oder wenn ein Zweig nicht
            mit einem Ereignis beginnt.
    """
    if len(branches) < 2:
        raise ValueError("ein Gateway braucht mindestens zwei Zweige")
    for branch in branches:
        if branch not in EVENT_KINDS:
            raise ValueError("kein Ereignis am Zweiganfang: %s" % branch)
    return list(branches)


def race(message_after, timer_after):
    """Entscheidet das Rennen zwischen Nachricht und Zeitgeber.

    Das Beispiel der Vorlesung: entweder trifft die Nachricht ein und wird
    geprüft, oder nach zehn Minuten läuft der Zeitgeber ab und der Prozess
    geht ohne sie weiter. Genau ein Zweig gewinnt, der andere wird
    verworfen.

    Args:
        message_after: wann die Nachricht eintrifft.
        timer_after: wann der Zeitgeber abläuft.

    Returns:
        Abbildung mit dem Gewinner, dem Zeitpunkt und dem verworfenen
        Zweig.

    Raises:
        ValueError: bei einem negativen Zeitpunkt.
    """
    if message_after < 0 or timer_after < 0:
        raise ValueError("negativer Zeitpunkt")
    if message_after < timer_after:
        return {"winner": "message", "at": message_after,
                "discarded": "timer"}
    if timer_after < message_after:
        return {"winner": "timer", "at": timer_after,
                "discarded": "message"}
    return {"winner": "undecided", "at": timer_after,
            "discarded": None,
            "note": "the specification leaves a tie to the engine"}


def example():
    """Der Ablauf aus der Vorlesung als Beschreibung.

    Returns:
        Abbildung mit den beiden Zweigen und dem, was danach passiert.
    """
    return {"gateway": "event based",
            "branches": [{"event": "message", "then": "Nachricht validieren"},
                         {"event": "timer", "after": "10 Minuten",
                          "then": "weiter ohne Nachricht"}],
            "joined by": "xor"}


def difference():
    """Stellt die beiden Gateways gegenüber."""
    return {"data based": {"decides": "the process itself",
                           "needs": "a value it already has",
                           "branch labels": "conditions"},
            "event based": {"decides": "the environment",
                            "needs": "nothing, it waits",
                            "branch labels": "events"}}
