"""Der Satz vom fehlenden Mittagessen, vollständig nachgerechnet."""

from itertools import product


def learners():
    """Nennt die Lernverfahren, die verglichen werden.

    Jedes bekommt die Beschriftungen der gesehenen Punkte und muss die
    ungesehenen beschriften. Die Verfahren sind absichtlich verschieden:
    eines rät die Mehrheit, eines das Gegenteil, eines immer null, eines
    den nächsten gesehenen Nachbarn.

    Returns:
        Abbildung vom Namen auf die Funktion.
    """
    return {"majority": _majority, "against the majority": _contrarian,
            "always zero": _zero, "always one": _one,
            "nearest seen point": _nearest,
            "alternating": _alternating}


def _majority(seen, point):
    """Sagt die häufigste gesehene Beschriftung."""
    values = list(seen.values())
    return 1 if sum(values) * 2 > len(values) else 0


def _contrarian(seen, point):
    """Sagt das Gegenteil der Mehrheit."""
    return 1 - _majority(seen, point)


def _zero(seen, point):
    """Sagt immer null."""
    return 0


def _one(seen, point):
    """Sagt immer eins."""
    return 1


def _nearest(seen, point):
    """Sagt die Beschriftung des nächsten gesehenen Punktes."""
    closest = min(seen, key=lambda other: (abs(other - point), other))
    return seen[closest]


def _alternating(seen, point):
    """Sagt abwechselnd, je nach Lage des Punktes."""
    return point % 2


def average_over_all_targets(points=5, seen=3):
    """Mittelt den Fehler jedes Verfahrens über alle Zielfunktionen.

    Der Bereich hat wenige Punkte, also lassen sich alle Zielfunktionen
    aufzählen: bei fünf Punkten sind es zweiunddreissig. Für jede wird
    das Verfahren auf den gesehenen Punkten beschriftet und auf den
    ungesehenen geprüft.

    Heraus kommt für jedes Verfahren genau ein halber Fehler. Das ist
    der Satz, und der Grund ist einfach: zu jeder Zielfunktion gibt es
    eine zweite, die auf den gesehenen Punkten gleich ist und auf allen
    ungesehenen entgegengesetzt. Was ein Verfahren bei der einen
    gewinnt, verliert es bei der anderen, gleich wie es aufgebaut ist.

    Args:
        points: die Grösse des Bereichs.
        seen: die Anzahl der gesehenen Punkte.

    Returns:
        Abbildung mit dem mittleren Fehler je Verfahren.

    Raises:
        ValueError: wenn nichts ungesehen bleibt oder der Bereich zu
            klein ist.
    """
    if points < 2:
        raise ValueError("der Bereich braucht mindestens zwei Punkte")
    if not 0 < seen < points:
        raise ValueError("es muss gesehene und ungesehene Punkte geben")
    training = list(range(seen))
    rest = list(range(seen, points))
    found = {name: 0.0 for name in learners()}
    targets = 0
    for values in product((0, 1), repeat=points):
        targets += 1
        labels = {index: values[index] for index in training}
        for name, learner in learners().items():
            wrong = sum(1 for point in rest
                        if learner(labels, point) != values[point])
            found[name] += wrong / len(rest)
    return {"errors": {name: value / targets
                       for name, value in found.items()},
            "targets": targets, "points": points, "seen": seen,
            "unseen": len(rest),
            "why": "zu jeder Zielfunktion gibt es ihr Spiegelbild auf "
                   "den ungesehenen Punkten"}


def on_a_single_target(points=6, seen=3):
    """Zeigt, dass der Satz über einzelne Aufgaben nichts sagt.

    Auf einer bestimmten Zielfunktion sind die Verfahren sehr wohl
    verschieden gut. Der Satz mittelt über alle, und diese Mittelung
    ist die Stelle, an der er seinen Biss verliert: die Aufgaben, die
    tatsächlich vorkommen, sind keine gleichverteilte Auswahl aus allen
    denkbaren.

    Returns:
        Abbildung mit dem besten und dem schlechtesten Verfahren auf
        einer glatten Zielfunktion.

    Raises:
        ValueError: wie bei ``average_over_all_targets``.
    """
    if not 0 < seen < points:
        raise ValueError("es muss gesehene und ungesehene Punkte geben")
    values = tuple(0 if index < points // 2 else 1
                   for index in range(points))
    labels = {index: values[index] for index in range(seen)}
    rest = list(range(seen, points))
    found = {}
    for name, learner in learners().items():
        wrong = sum(1 for point in rest
                    if learner(labels, point) != values[point])
        found[name] = wrong / len(rest)
    return {"errors": found, "best": min(found.values()),
            "worst": max(found.values()),
            "target": values,
            "what it shows": "auf einer einzelnen Aufgabe sind die "
                             "Verfahren verschieden gut"}


def what_the_theorem_assumes():
    """Nennt die Annahme, ohne die der Satz nicht gilt.

    Er mittelt über alle Zielfunktionen mit gleichem Gewicht. Die
    Aufgaben der Welt sind aber nicht gleichverteilt: sie sind glatt,
    strukturiert und wiederholen sich. Deshalb ist der Satz kein Grund,
    Verfahren für gleichwertig zu halten, sondern eine Aufforderung, die
    Annahme zu benennen, unter der ein Verfahren gut ist.

    Für ein Brettspiel heisst das: eine KI ist für Catan gebaut und
    nicht für Spiele im Allgemeinen. Was sie an Catan gut macht, sind
    genau die Annahmen über Catan, die in ihr stecken.
    """
    return {"the assumption": "alle Zielfunktionen sind gleich "
                              "wahrscheinlich",
            "why it is false in practice": "wirkliche Aufgaben sind "
                                           "glatt und strukturiert",
            "what the theorem is good for": "es zwingt dazu, die "
                                            "eigenen Annahmen zu nennen",
            "for a board game": "eine KI ist für dieses Spiel gebaut, "
                                "nicht für Spiele überhaupt"}
