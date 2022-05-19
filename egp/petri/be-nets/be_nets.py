"""Bedingungs-Ereignis-Netze: Übungsblatt 11."""


def enabled(net, marking):
    """Nennt die Ereignisse, die eintreten können.

    In einem B/E-Netz trägt jede Stelle höchstens eine Marke. Ein
    Ereignis kann eintreten, wenn alle Stellen seines Vorbereichs
    markiert sind und keine Stelle seines Nachbereichs es ist; die
    zweite Bedingung ist der Unterschied zum Stellen-Transitions-Netz
    und sorgt dafür, dass keine Stelle zwei Marken bekommt.

    Args:
        net: Abbildung mit ``pre`` und ``post`` je Ereignis.
        marking: die Menge der markierten Stellen.

    Returns:
        Die möglichen Ereignisse, alphabetisch.
    """
    found = []
    for event in sorted(net):
        before = set(net[event]["pre"])
        after = set(net[event]["post"])
        if before <= set(marking) and not (after - before) & set(marking):
            found.append(event)
    return found


def fire(net, marking, event):
    """Lässt ein Ereignis eintreten.

    Raises:
        ValueError: bei einem unbekannten oder nicht eintrittsbereiten
            Ereignis.
    """
    if event not in net:
        raise ValueError("unbekanntes Ereignis")
    if event not in enabled(net, marking):
        raise ValueError("das Ereignis ist nicht eintrittsbereit")
    changed = set(marking) - set(net[event]["pre"])
    return frozenset(changed | set(net[event]["post"]))


def server_example():
    """Das Netz aus der Aufgabe: zwei Clients an einem Server.

    Zwei Clients greifen parallel zu, der Server kann zwei Anfragen
    zugleich annehmen. Die Kapazität steht als zwei Stellen ``frei1``
    und ``frei2`` im Netz; ein B/E-Netz kann nicht zählen, deshalb wird
    aus einer Kapazität von zwei eine Stelle je Platz.

    Returns:
        Paar aus Netz und Anfangsmarkierung.
    """
    net = {
        "anfrage1": {"pre": ["ruhe1", "frei1"], "post": ["wartet1"]},
        "antwort1": {"pre": ["wartet1"], "post": ["ruhe1", "frei1"]},
        "anfrage2": {"pre": ["ruhe2", "frei2"], "post": ["wartet2"]},
        "antwort2": {"pre": ["wartet2"], "post": ["ruhe2", "frei2"]},
    }
    marking = frozenset({"ruhe1", "ruhe2", "frei1", "frei2"})
    return net, marking


def states(net, marking, limit=200):
    """Sammelt die erreichbaren Markierungen.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    start = frozenset(marking)
    seen = {start}
    stack = [start]
    edges = []
    while stack:
        current = stack.pop()
        for event in enabled(net, current):
            following = fire(net, current, event)
            edges.append((current, event, following))
            if following not in seen:
                if len(seen) >= limit:
                    raise ValueError("die Suche erreicht die Schranke")
                seen.add(following)
                stack.append(following)
    return {"states": sorted(sorted(state) for state in seen),
            "edges": len(edges), "count": len(seen)}


def both_clients_can_wait():
    """Prüft, dass beide Clients gleichzeitig warten können.

    Das ist die Anforderung der Aufgabe: der Server nimmt zwei Anfragen
    zugleich entgegen. Im Netz heisst das, dass eine Markierung
    erreichbar ist, in der ``wartet1`` und ``wartet2`` zugleich gesetzt
    sind.

    Returns:
        Abbildung mit dem Befund und der Zahl der Markierungen.
    """
    net, marking = server_example()
    report = states(net, marking)
    both = any({"wartet1", "wartet2"} <= set(state)
               for state in report["states"])
    return {"both waiting reachable": both, "states": report["count"],
            "why two places": "ein B/E-Netz kann nicht zählen, also wird "
                              "aus der Kapazität zwei je eine Stelle"}


def why_no_two_tokens():
    """Erklärt die zweite Eintrittsbedingung.

    Ohne sie könnte ein Ereignis eine Stelle markieren, die schon
    markiert ist, und die Stelle trüge zwei Marken. Damit wäre es kein
    B/E-Netz mehr, denn dort ist eine Stelle eine Bedingung, und eine
    Bedingung gilt oder gilt nicht; zweimal gelten kann sie nicht.
    """
    return {"condition": "keine Stelle des Nachbereichs ist markiert",
            "without it": "eine Stelle könnte zwei Marken tragen",
            "why that is wrong": "eine Bedingung gilt oder gilt nicht",
            "in an S/T net": "dort ist es erlaubt und heisst Kapazität"}
