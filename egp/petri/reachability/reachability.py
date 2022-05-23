"""Erreichbarkeit in Stellen-Transitions-Netzen: Übungsblatt 12."""


def enabled(net, marking):
    """Nennt die Transitionen, die schalten können.

    Eine Transition schaltet, wenn jede Stelle ihres Vorbereichs
    mindestens so viele Marken trägt, wie das Kantengewicht verlangt.
    Anders als im B/E-Netz gibt es keine obere Schranke; eine Stelle
    kann beliebig viele Marken tragen, und deshalb kann der
    Erreichbarkeitsgraph unendlich sein.

    Args:
        net: Abbildung je Transition auf ``pre`` und ``post``, jeweils
            von der Stelle auf das Gewicht.
        marking: Abbildung von der Stelle auf die Zahl der Marken.

    Returns:
        Die schaltbaren Transitionen, alphabetisch.
    """
    found = []
    for name in sorted(net):
        needed = net[name]["pre"]
        if all(marking.get(place, 0) >= count
               for place, count in needed.items()):
            found.append(name)
    return found


def fire(net, marking, transition):
    """Schaltet eine Transition.

    Raises:
        ValueError: bei einer unbekannten oder nicht schaltbaren
            Transition.
    """
    if transition not in net:
        raise ValueError("unbekannte Transition")
    if transition not in enabled(net, marking):
        raise ValueError("die Transition ist nicht schaltbar")
    changed = dict(marking)
    for place, count in net[transition]["pre"].items():
        changed[place] = changed.get(place, 0) - count
    for place, count in net[transition]["post"].items():
        changed[place] = changed.get(place, 0) + count
    return {place: count for place, count in changed.items() if count}


def _key(marking, places):
    """Bringt eine Markierung in eine vergleichbare Form."""
    return tuple(marking.get(place, 0) for place in places)


def table(net, marking, places=None, limit=500):
    """Baut die Erreichbarkeitstabelle.

    Jede Zeile ist eine erreichbare Markierung, jede Spalte eine
    Transition, und der Eintrag die Markierung nach dem Schalten. Aus
    der Tabelle folgt der Graph unmittelbar.

    Args:
        net: das Netz.
        marking: die Anfangsmarkierung.
        places: die Reihenfolge der Stellen; ohne Angabe alphabetisch.
        limit: obere Schranke der Markierungen.

    Returns:
        Abbildung mit den Markierungen, der Tabelle und den Kanten.

    Raises:
        ValueError: wenn die Schranke erreicht wird; das Netz ist dann
            vermutlich unbeschränkt.
    """
    if places is None:
        places = sorted({place for name in net
                         for side in ("pre", "post")
                         for place in net[name][side]}
                        | set(marking))
    start = _key(marking, places)
    known = {start: dict(marking)}
    order = [start]
    rows = {}
    edges = []
    stack = [start]
    while stack:
        current = stack.pop(0)
        rows[current] = {}
        for name in enabled(net, known[current]):
            following = fire(net, known[current], name)
            key = _key(following, places)
            rows[current][name] = key
            edges.append((current, name, key))
            if key not in known:
                if len(known) >= limit:
                    raise ValueError("die Menge erreicht die Schranke; "
                                     "das Netz ist vermutlich unbeschränkt")
                known[key] = following
                order.append(key)
                stack.append(key)
    return {"places": places, "markings": order, "table": rows,
            "edges": edges, "count": len(order)}


def example():
    """Ein kleines Netz mit einer Auswahl.

    Returns:
        Paar aus Netz und Anfangsmarkierung.
    """
    net = {
        "T1": {"pre": {"P1": 1}, "post": {"P2": 1, "P3": 1}},
        "T2": {"pre": {"P2": 1}, "post": {"P4": 1}},
        "T3": {"pre": {"P3": 1}, "post": {"P5": 1}},
        "T4": {"pre": {"P4": 1, "P5": 1}, "post": {"P1": 1}},
    }
    return net, {"P1": 1}


def unbounded_example():
    """Ein Netz, dessen Erreichbarkeitsmenge unendlich ist.

    Eine Transition, die eine Marke verbraucht und zwei zurücklegt,
    lässt die Zahl der Marken ohne Grenze wachsen. Der
    Erreichbarkeitsgraph hat dann unendlich viele Knoten, und die
    Tabelle lässt sich nicht aufstellen; die Funktion meldet das,
    statt zu laufen.

    Returns:
        Abbildung mit dem Netz und der Meldung.
    """
    net = {"T1": {"pre": {"P1": 1}, "post": {"P1": 2}}}
    try:
        table(net, {"P1": 1}, limit=50)
        message = None
    except ValueError as problem:
        message = str(problem)
    return {"net": net, "reported": message, "bounded": message is None,
            "why": "jede Schaltung erhöht die Zahl der Marken um eins"}


def is_live(net, marking, limit=500):
    """Prüft, ob von jeder erreichbaren Markierung aus jede Transition
    wieder schalten kann.

    Lebendigkeit in diesem Sinn ist die Eigenschaft, die ein Prozess
    braucht, der nie steckenbleiben soll: keine Transition wird je
    endgültig unmöglich.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    report = table(net, marking, limit=limit)
    reachable = {key: set() for key in report["markings"]}
    forward = {key: [] for key in report["markings"]}
    for source, name, target in report["edges"]:
        forward[source].append((name, target))
    for key in report["markings"]:
        seen = {key}
        stack = [key]
        while stack:
            current = stack.pop()
            for name, target in forward[current]:
                reachable[key].add(name)
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
    dead = sorted(name for name in net
                  if any(name not in reachable[key]
                         for key in report["markings"]))
    return {"live": not dead, "not always reachable": dead,
            "markings": report["count"]}
