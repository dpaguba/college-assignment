"""Das Markenspiel: welche Abläufe ein Modell zulässt."""

import itertools

DEFAULT_LIMIT = 20


def sequence_example():
    """Drei Aufgaben hintereinander."""
    return {
        "nodes": {"start": {"type": "start"}, "a": {"type": "task"},
                  "b": {"type": "task"}, "c": {"type": "task"},
                  "end": {"type": "end"}},
        "flows": [("start", "a"), ("a", "b"), ("b", "c"), ("c", "end")],
    }


def parallel_example():
    """Zwei Aufgaben zwischen einer parallelen Verzweigung."""
    return {
        "nodes": {"start": {"type": "start"},
                  "split": {"type": "gateway", "gateway": "and"},
                  "a": {"type": "task"}, "b": {"type": "task"},
                  "join": {"type": "gateway", "gateway": "and"},
                  "end": {"type": "end"}},
        "flows": [("start", "split"), ("split", "a"), ("split", "b"),
                  ("a", "join"), ("b", "join"), ("join", "end")],
    }


def choice_example():
    """Zwei Aufgaben zwischen einer exklusiven Verzweigung."""
    model = parallel_example()
    model["nodes"]["split"]["gateway"] = "xor"
    model["nodes"]["join"]["gateway"] = "xor"
    return model


def inclusive_example():
    """Zwei Aufgaben zwischen einer inklusiven Verzweigung."""
    model = parallel_example()
    model["nodes"]["split"]["gateway"] = "or"
    model["nodes"]["join"]["gateway"] = "or"
    return model


def loop_example():
    """Eine Aufgabe, die sich wiederholen kann."""
    return {
        "nodes": {"start": {"type": "start"},
                  "join": {"type": "gateway", "gateway": "xor"},
                  "a": {"type": "task"},
                  "split": {"type": "gateway", "gateway": "xor"},
                  "end": {"type": "end"}},
        "flows": [("start", "join"), ("join", "a"), ("a", "split"),
                  ("split", "end"), ("split", "join")],
    }


def _incoming(model, name):
    """Nennt die Nummern der eingehenden Flüsse eines Knotens."""
    return [index for index, (_, target) in enumerate(model["flows"])
            if target == name]


def _outgoing(model, name):
    """Nennt die Nummern der ausgehenden Flüsse eines Knotens."""
    return [index for index, (source, _) in enumerate(model["flows"])
            if source == name]


def _kind(model, name):
    """Nennt die Art eines Knotens für das Markenspiel."""
    node = model["nodes"][name]
    if node["type"] == "gateway":
        return node.get("gateway", "xor")
    return node["type"]


def initial(model):
    """Legt die Anfangsmarkierung: eine Marke hinter dem Startereignis.

    Raises:
        ValueError: wenn es nicht genau ein Startereignis mit genau einem
            Ausgang gibt.
    """
    starts = [name for name, node in model["nodes"].items()
              if node["type"] == "start"]
    if len(starts) != 1:
        raise ValueError("genau ein Startereignis erwartet")
    out = _outgoing(model, starts[0])
    if len(out) != 1:
        raise ValueError("das Startereignis braucht genau einen Ausgang")
    return frozenset({(out[0], 1)})


def _as_counts(marking):
    """Wandelt eine Markierung in eine änderbare Abbildung um."""
    return {flow: count for flow, count in marking}


def _as_marking(counts):
    """Wandelt eine Abbildung zurück in eine Markierung."""
    return frozenset((flow, count) for flow, count in counts.items()
                     if count > 0)


def _can_still_arrive(model, counts, target):
    """Sagt, ob eine Marke die Zusammenführung noch erreichen kann.

    Gefragt wird das für die inklusive Zusammenführung: sie darf erst
    feuern, wenn von den Zweigen, die sie noch beliefern könnten, keiner
    mehr eine Marke trägt. Gesucht wird deshalb ein Weg von einer Marke
    ausserhalb der eigenen Eingänge zu dem Knoten, ohne ihn zu
    durchlaufen.
    """
    incoming = set(_incoming(model, target))
    stack = [model["flows"][flow][1] for flow, count in counts.items()
             if count > 0 and flow not in incoming]
    seen = set()
    while stack:
        name = stack.pop()
        if name == target:
            return True
        if name in seen:
            continue
        seen.add(name)
        for flow in _outgoing(model, name):
            stack.append(model["flows"][flow][1])
    return False


def _consume_options(model, name, counts):
    """Nennt die Mengen von Flüssen, aus denen ein Knoten nehmen kann."""
    incoming = _incoming(model, name)
    marked = [flow for flow in incoming if counts.get(flow, 0) > 0]
    kind = _kind(model, name)
    if not marked:
        return []
    if kind == "and":
        if len(marked) == len(incoming):
            return [tuple(incoming)]
        return []
    if kind == "or" and len(incoming) > 1:
        if len(marked) < len(incoming) and _can_still_arrive(model, counts,
                                                            name):
            return []
        return [tuple(marked)]
    return [(flow,) for flow in marked]


def _produce_options(model, name):
    """Nennt die Mengen von Flüssen, auf die ein Knoten legen kann."""
    outgoing = _outgoing(model, name)
    if not outgoing:
        return [()]
    kind = _kind(model, name)
    if kind == "xor":
        return [(flow,) for flow in outgoing]
    if kind == "or" and len(outgoing) > 1:
        chosen = []
        for size in range(1, len(outgoing) + 1):
            chosen.extend(itertools.combinations(outgoing, size))
        return chosen
    return [tuple(outgoing)]


def enabled(model, marking):
    """Nennt die Knoten, die feuern können, mit ihren Möglichkeiten.

    Start- und Endereignisse feuern nicht: die Anfangsmarke liegt hinter
    dem Start, und eine Marke vor einem Ende bleibt dort liegen. Das ist
    die übliche Sicht des Workflow-Netzes und macht die Endmarkierung
    ablesbar.

    Returns:
        Liste von Tupeln aus Knoten, genommenen und gelegten Flüssen.
    """
    counts = _as_counts(marking)
    steps = []
    for name, node in sorted(model["nodes"].items()):
        if node["type"] in ("start", "end"):
            continue
        for taken in _consume_options(model, name, counts):
            for given in _produce_options(model, name):
                steps.append((name, taken, given))
    return steps


def fire(marking, taken, given):
    """Führt einen Schritt aus und liefert die neue Markierung."""
    counts = _as_counts(marking)
    for flow in taken:
        counts[flow] = counts.get(flow, 0) - 1
    for flow in given:
        counts[flow] = counts.get(flow, 0) + 1
    return _as_marking(counts)


def final(model):
    """Die Markierung, die einen fertigen Ablauf beschreibt.

    Raises:
        ValueError: wenn es kein Endereignis gibt.
    """
    ends = [name for name, node in model["nodes"].items()
            if node["type"] == "end"]
    if not ends:
        raise ValueError("kein Endereignis")
    flows = [flow for name in ends for flow in _incoming(model, name)]
    return {frozenset({(flow, 1)}) for flow in flows}


def markings(model):
    """Sammelt alle erreichbaren Markierungen.

    Returns:
        Menge der Markierungen, die Anfangsmarkierung eingeschlossen.
    """
    start = initial(model)
    seen = {start}
    stack = [start]
    while stack:
        marking = stack.pop()
        for _, taken, given in enabled(model, marking):
            following = fire(marking, taken, given)
            if following not in seen:
                seen.add(following)
                stack.append(following)
    return seen


def traces(model, limit=DEFAULT_LIMIT):
    """Sammelt die Abläufe, die im Endzustand ankommen.

    Ein Ablauf ist die Folge der ausgeführten Aufgaben; Gateways stehen
    nicht darin, weil sie keine Arbeit sind. Schleifen machen die Zahl der
    Abläufe unendlich, deshalb die Schranke.

    Args:
        model: das Prozessmodell.
        limit: höchste Zahl von Aufgaben in einem Ablauf.

    Returns:
        Liste der Abläufe als Tupel von Aufgabennamen.
    """
    goals = final(model)
    found = set()
    stack = [(initial(model), ())]
    seen = set()
    while stack:
        marking, done = stack.pop()
        if marking in goals:
            found.add(done)
            continue
        if (marking, done) in seen:
            continue
        seen.add((marking, done))
        for name, taken, given in enabled(model, marking):
            work = model["nodes"][name]["type"] == "task"
            if work and len(done) >= limit:
                continue
            following = done + (name,) if work else done
            stack.append((fire(marking, taken, given), following))
    return sorted(found)
