"""Der Kontrollfluss als Graph und die Prüfung auf Wohlgeformtheit."""


def example():
    """Ein kleines, wohlgeformtes Modell.

    Returns:
        Abbildung mit ``nodes`` und ``flows``.
    """
    return {
        "nodes": {"start": {"type": "start"},
                  "check": {"type": "task"},
                  "decide": {"type": "gateway", "gateway": "xor"},
                  "accept": {"type": "task"},
                  "reject": {"type": "task"},
                  "end": {"type": "end"}},
        "flows": [("start", "check"), ("check", "decide"),
                  ("decide", "accept"), ("decide", "reject"),
                  ("accept", "end"), ("reject", "end")],
    }


def _validate(model):
    """Prüft, dass jeder Fluss zwischen vorhandenen Knoten läuft.

    Raises:
        ValueError: bei einem Fluss auf einen unbekannten Knoten.
    """
    for source, target in model["flows"]:
        for name in (source, target):
            if name not in model["nodes"]:
                raise ValueError("unbekannter Knoten: %s" % name)


def successors(model, name):
    """Nennt die Nachfolger eines Knotens in der Reihenfolge der Flüsse.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    if name not in model["nodes"]:
        raise ValueError("unbekannter Knoten")
    return [target for source, target in model["flows"] if source == name]


def predecessors(model, name):
    """Nennt die Vorgänger eines Knotens.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    if name not in model["nodes"]:
        raise ValueError("unbekannter Knoten")
    return [source for source, target in model["flows"] if target == name]


def nodes_of_type(model, kind):
    """Nennt alle Knoten einer Art, alphabetisch."""
    return sorted(name for name, node in model["nodes"].items()
                  if node["type"] == kind)


def _reachable(model, starts, forward=True):
    """Sammelt die von einer Menge aus erreichbaren Knoten."""
    seen = set(starts)
    stack = list(starts)
    while stack:
        name = stack.pop()
        step = successors if forward else predecessors
        for other in step(model, name):
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return seen


def check(model):
    """Prüft ein Modell auf die Grundregeln des Kontrollflusses.

    Geprüft wird, dass es genau ein Startereignis und mindestens ein
    Endereignis gibt, dass jeder Knoten vom Start aus erreichbar ist und
    dass von jedem Knoten aus ein Ende erreichbar ist. Die letzten beiden
    Bedingungen sind die schwachen Vorstufen der Soundness: sie fangen
    vergessene Kanten ab, sagen aber noch nichts über die Semantik der
    Gateways.

    Returns:
        Abbildung mit ``problems`` und den beiden Ereignismengen.

    Raises:
        ValueError: bei einem Fluss auf einen unbekannten Knoten.
    """
    _validate(model)
    problems = []
    starts = nodes_of_type(model, "start")
    ends = nodes_of_type(model, "end")
    if len(starts) > 1:
        problems.append("more than one start event")
    if not starts:
        problems.append("no start event")
    if not ends:
        problems.append("no end event")
    if starts:
        forward = _reachable(model, starts)
        for name in sorted(model["nodes"]):
            if name not in forward:
                problems.append("unreachable: %s" % name)
    if ends:
        backward = _reachable(model, ends, forward=False)
        for name in sorted(model["nodes"]):
            if name not in backward:
                problems.append("cannot reach an end event: %s" % name)
    return {"problems": problems, "starts": starts, "ends": ends}


def why_reachability_is_not_enough():
    """Sagt, was die Prüfung noch nicht leistet.

    Erreichbarkeit sieht den Graphen, nicht die Marken. Ein Modell, in dem
    eine parallele Verzweigung auf eine exklusive Zusammenführung trifft,
    besteht die Prüfung und bleibt trotzdem stehen; dafür braucht es das
    Markenspiel.
    """
    return {"catches": ["forgotten edges", "orphan nodes",
                        "a second start event"],
            "misses": ["deadlock", "lack of synchronisation"],
            "needs": "the token game"}
