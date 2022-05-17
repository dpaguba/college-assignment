"""Die klassischen Probleme der Nebenläufigkeit."""

PROBLEMS = {
    "mutual exclusion": "höchstens einer im kritischen Abschnitt",
    "producer consumer": "einer füllt, einer leert, der Puffer ist "
                         "beschränkt",
    "readers writers": "viele dürfen lesen, nur einer schreiben",
    "dining philosophers": "fünf teilen sich fünf Gabeln",
}


def problems():
    """Nennt die vier Probleme mit ihrer Anforderung."""
    return dict(PROBLEMS)


def philosophers_deadlock(count=5, order="left first"):
    """Prüft, ob die Philosophen sich verklemmen können.

    Nimmt jeder zuerst die linke Gabel, so kann es dazu kommen, dass
    alle gleichzeitig ihre linke halten und keiner die rechte bekommt:
    ein Zyklus des Wartens, aus dem niemand herauskommt. Nimmt einer von
    ihnen die Gabeln in umgekehrter Reihenfolge, so ist der Zyklus
    unterbrochen und die Verklemmung unmöglich.

    Gerechnet wird über den Zustand «wer hält welche Gabel», und die
    Verklemmung ist eine erreichbare Belegung, in der jeder genau eine
    Gabel hält und keiner weiterkommt.

    Args:
        count: die Zahl der Philosophen.
        order: ``left first`` oder ``one turned``.

    Returns:
        Abbildung mit dem Befund.

    Raises:
        ValueError: bei weniger als zwei Philosophen oder einer
            unbekannten Reihenfolge.
    """
    if count < 2:
        raise ValueError("mindestens zwei Philosophen")
    if order not in ("left first", "one turned"):
        raise ValueError("unbekannte Reihenfolge")
    firsts = []
    for index in range(count):
        left = index
        right = (index + 1) % count
        if order == "one turned" and index == count - 1:
            firsts.append((right, left))
        else:
            firsts.append((left, right))
    holders = {}
    for index, (first, _) in enumerate(firsts):
        if first in holders:
            return {"deadlock possible": False,
                    "why": "zwei greifen zuerst nach derselben Gabel, der "
                           "Zyklus schliesst sich nicht",
                    "order": order}
        holders[first] = index
    stuck = all(second in holders for _, second in firsts)
    return {"deadlock possible": stuck,
            "everyone holds one": len(holders) == count,
            "why": "jeder hält seine erste Gabel und wartet auf die "
                   "zweite" if stuck else "der Wartezyklus ist "
                                          "unterbrochen",
            "order": order}


def four_conditions():
    """Nennt die vier Bedingungen, unter denen eine Verklemmung entsteht.

    Sie müssen alle vier gelten, und deshalb genügt es, eine davon zu
    brechen. Die Philosophen brechen die vierte, indem einer die Gabeln
    in umgekehrter Reihenfolge nimmt.
    """
    return {"mutual exclusion": "eine Ressource hat höchstens einen "
                                "Halter",
            "hold and wait": "wer eine hält, wartet auf die nächste",
            "no preemption": "niemand nimmt einem anderen etwas weg",
            "circular wait": "die Wartebeziehungen bilden einen Kreis",
            "to prevent": "eine der vier brechen genügt",
            "the philosophers break": "circular wait"}


def bounded_buffer(capacity, produced, consumed):
    """Prüft eine Folge von Ereignissen am beschränkten Puffer.

    Args:
        capacity: die Kapazität.
        produced: die Zahl der Ablagen.
        consumed: die Zahl der Entnahmen.

    Returns:
        Abbildung mit dem Bestand und den verletzten Bedingungen.

    Raises:
        ValueError: bei einer nicht positiven Kapazität oder negativen
            Zahlen.
    """
    if capacity < 1:
        raise ValueError("die Kapazität muss positiv sein")
    if produced < 0 or consumed < 0:
        raise ValueError("negative Zahl")
    level = produced - consumed
    return {"level": level, "overflow": level > capacity,
            "underflow": level < 0,
            "correct": 0 <= level <= capacity,
            "the two conditions": ["nie entnehmen, wenn leer",
                                   "nie ablegen, wenn voll"]}


def readers_writers(readers, writers):
    """Beurteilt eine Belegung beim Leser-Schreiber-Problem.

    Erlaubt ist entweder beliebig viele Leser oder genau ein Schreiber.
    Die Regel ist einfach; schwierig ist die Fairness, denn ein steter
    Strom von Lesern kann einen Schreiber beliebig lange warten lassen.

    Raises:
        ValueError: bei einer negativen Zahl.
    """
    if readers < 0 or writers < 0:
        raise ValueError("negative Zahl")
    return {"allowed": (writers == 0) or (writers == 1 and readers == 0),
            "readers": readers, "writers": writers,
            "starvation risk": "ein steter Strom von Lesern lässt den "
                               "Schreiber warten",
            "remedy": "ankommende Leser hinter einem wartenden Schreiber "
                      "anstellen"}


def why_these_four():
    """Sagt, warum gerade diese vier Probleme immer wieder auftauchen.

    Sie sind keine Aufgaben, sondern Muster. Jedes nebenläufige System
    enthält mindestens eines davon, meist mehrere, und die Lösungen
    unterscheiden sich nur in der Verpackung. Wer sie erkennt, muss die
    Lösung nicht neu erfinden, und wer sie nicht erkennt, erfindet eine
    falsche.
    """
    return {"mutual exclusion": "überall, wo geteilter Zustand geändert "
                                "wird",
            "producer consumer": "jede Warteschlange, jeder Kanal",
            "readers writers": "jeder Zwischenspeicher, der gelesen und "
                               "aktualisiert wird",
            "dining philosophers": "jede Situation mit mehreren "
                                   "Ressourcen je Vorgang",
            "point": "die Lösungen sind bekannt, das Erkennen ist die "
                     "Arbeit"}
