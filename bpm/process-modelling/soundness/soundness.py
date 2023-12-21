"""Soundness: die drei Bedingungen, die ein ausführbares Modell erfüllt."""

CRITERIA = ("option to complete", "proper completion", "no dead activities")

MARKING_LIMIT = 10000


def criteria():
    """Nennt die drei Bedingungen."""
    return list(CRITERIA)


def sound_example():
    """Ein korrektes Modell: parallele Verzweigung, parallel geschlossen."""
    return {
        "nodes": {"start": {"type": "start"},
                  "split": {"type": "gateway", "gateway": "and"},
                  "ship": {"type": "task"}, "invoice": {"type": "task"},
                  "join": {"type": "gateway", "gateway": "and"},
                  "end": {"type": "end"}},
        "flows": [("start", "split"), ("split", "ship"),
                  ("split", "invoice"), ("ship", "join"),
                  ("invoice", "join"), ("join", "end")],
    }


def deadlock_example():
    """Exklusiv verzweigt, parallel zusammengeführt: der Klassiker.

    Die Verzweigung schickt eine Marke auf einen der beiden Zweige, die
    Zusammenführung wartet auf beide. Sie bekommt nie beide und feuert
    nie.
    """
    model = sound_example()
    model["nodes"]["split"]["gateway"] = "xor"
    return model


def lack_of_synchronisation_example():
    """Parallel verzweigt, exklusiv zusammengeführt: die Marke verdoppelt sich.

    Die Verzweigung legt zwei Marken, die Zusammenführung lässt jede
    einzeln durch. Am Ende liegen zwei Marken auf dem Endereignis: der
    Prozess läuft zweimal zu Ende.
    """
    model = sound_example()
    model["nodes"]["join"]["gateway"] = "xor"
    return model


def dead_activity_example():
    """Eine Aufgabe, die nie an die Reihe kommt.

    Hinter der exklusiven Verzweigung steht eine parallele
    Zusammenführung; sie feuert nie, und alles dahinter ist tot.
    """
    return {
        "nodes": {"start": {"type": "start"},
                  "split": {"type": "gateway", "gateway": "xor"},
                  "a": {"type": "task"}, "b": {"type": "task"},
                  "join": {"type": "gateway", "gateway": "and"},
                  "never": {"type": "task"},
                  "end": {"type": "end"}},
        "flows": [("start", "split"), ("split", "a"), ("split", "b"),
                  ("a", "join"), ("b", "join"), ("join", "never"),
                  ("never", "end")],
    }


def _incoming(model, name):
    """Nennt die Nummern der eingehenden Flüsse."""
    return [index for index, (_, target) in enumerate(model["flows"])
            if target == name]


def _outgoing(model, name):
    """Nennt die Nummern der ausgehenden Flüsse."""
    return [index for index, (source, _) in enumerate(model["flows"])
            if source == name]


def _steps(model, marking):
    """Nennt die möglichen Schritte aus einer Markierung.

    Betrachtet werden die exklusive und die parallele Verzweigung; das
    inklusive Gateway bleibt aussen vor, weil seine Zusammenführung eine
    Vorausschau braucht, die für die drei Bedingungen nichts beiträgt.

    Returns:
        Liste von Tupeln aus Knoten und neuer Markierung.
    """
    counts = dict(marking)
    steps = []
    for name, node in sorted(model["nodes"].items()):
        if node["type"] in ("start", "end"):
            continue
        incoming = _incoming(model, name)
        outgoing = _outgoing(model, name)
        if node["type"] == "gateway":
            kind = node.get("gateway", "xor")
        else:
            kind = "seq"
        marked = [flow for flow in incoming if counts.get(flow, 0) > 0]
        if not marked:
            continue
        if kind == "and" and len(marked) < len(incoming):
            continue
        taken = tuple(incoming) if kind == "and" else None
        givens = ([(flow,) for flow in outgoing] if kind == "xor" and
                  len(outgoing) > 1 else [tuple(outgoing)])
        for one in ([taken] if taken else [(flow,) for flow in marked]):
            for given in givens:
                changed = dict(counts)
                for flow in one:
                    changed[flow] = changed.get(flow, 0) - 1
                for flow in given:
                    changed[flow] = changed.get(flow, 0) + 1
                steps.append((name, frozenset(
                    (flow, count) for flow, count in changed.items()
                    if count > 0)))
    return steps


def _initial(model):
    """Die Anfangsmarkierung hinter dem Startereignis.

    Raises:
        ValueError: wenn es nicht genau ein Startereignis mit einem
            Ausgang gibt.
    """
    starts = [name for name, node in model["nodes"].items()
              if node["type"] == "start"]
    if len(starts) != 1 or len(_outgoing(model, starts[0])) != 1:
        raise ValueError("genau ein Startereignis mit einem Ausgang erwartet")
    return frozenset({(_outgoing(model, starts[0])[0], 1)})


def _final(model):
    """Die Menge der Markierungen, die einen fertigen Ablauf beschreiben."""
    ends = [name for name, node in model["nodes"].items()
            if node["type"] == "end"]
    return {frozenset({(flow, 1)})
            for name in ends for flow in _incoming(model, name)}


def _all_can_finish(seen, goals, backward):
    """Prüft, ob von jeder erreichbaren Markierung ein Ende erreichbar ist.

    Das ist die eigentliche Bedingung: nicht, dass die Endmarkierung
    irgendwie vorkommt, sondern dass sie von überall aus noch zu erreichen
    ist. Gesucht wird sie rückwärts, von den Endmarkierungen aus über die
    umgekehrten Kanten des Erreichbarkeitsgraphen.
    """
    good = {marking for marking in goals if marking in seen}
    stack = list(good)
    while stack:
        marking = stack.pop()
        for before in backward.get(marking, ()):
            if before not in good:
                good.add(before)
                stack.append(before)
    return good >= seen


def check(model):
    """Prüft ein Modell gegen die drei Bedingungen.

    Erzeugt wird der Erreichbarkeitsgraph über den Markierungen. Daraus
    folgt alles Weitere: eine Markierung ohne Schritte und ohne Marke auf
    dem Ende ist eine Verklemmung, der Fall bleibt stehen; eine Markierung
    mit einer Marke auf dem Ende und noch etwas daneben verletzt den
    sauberen Abschluss, der Fall läuft mehrfach zu Ende; eine Aufgabe, die
    in keinem Schritt vorkommt, ist tot. Die beiden Fehler werden
    getrennt gemeldet, weil sie sich verschieden anfühlen: das eine
    bleibt liegen, das andere kommt doppelt an.

    Returns:
        Abbildung mit den drei Bedingungen, ``sound``, ``deadlocks`` und
        ``dead activities``.

    Raises:
        ValueError: bei einem Modell ohne eindeutigen Start oder wenn der
            Erreichbarkeitsgraph über die Schranke wächst.
    """
    goals = _final(model)
    start = _initial(model)
    seen = {start}
    stack = [start]
    fired = set()
    deadlocks = []
    improper = []
    backward = {}
    end_flows = {flow for goal in goals for flow, _ in goal}
    while stack:
        marking = stack.pop()
        steps = _steps(model, marking)
        on_end = sum(count for flow, count in marking if flow in end_flows)
        if on_end and marking not in goals:
            improper.append(sorted(marking))
        if not steps and marking not in goals and not on_end:
            deadlocks.append(sorted(marking))
        for name, following in steps:
            fired.add(name)
            backward.setdefault(following, set()).add(marking)
            if following not in seen:
                if len(seen) >= MARKING_LIMIT:
                    raise ValueError("der Erreichbarkeitsgraph wächst "
                                     "über die Schranke")
                seen.add(following)
                stack.append(following)
    completes = _all_can_finish(seen, goals, backward)
    dead = sorted(name for name, node in model["nodes"].items()
                  if node["type"] == "task" and name not in fired)
    return {"option to complete": completes,
            "proper completion": not improper,
            "no dead activities": not dead,
            "sound": completes and not improper and not dead,
            "deadlocks": deadlocks,
            "finished more than once": improper,
            "dead activities": dead,
            "markings": len(seen)}


def why_it_matters():
    """Sagt, wozu die Prüfung gut ist.

    Ein unsoundes Modell lässt sich zeichnen, besprechen und abnehmen; es
    fällt erst auf, wenn eine Maschine es ausführt und ein Fall
    steckenbleibt. Der Erreichbarkeitsgraph findet das vorher, ohne einen
    einzigen echten Fall.
    """
    return {"deadlock": "a case stops and never finishes",
            "lack of synchronisation": "a case finishes twice",
            "dead activity": "work that was modelled and never happens",
            "found by": "the reachability graph, before any execution"}
