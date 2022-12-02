"""Die Prüfung einer EPK gegen die Regeln der Notation."""

KINDS = ("Ereignis", "Funktion", "Konnektor")
DECIDING = ("XOR", "OR")


def example():
    """Eine kleine, korrekte Kette.

    Returns:
        Abbildung mit ``nodes`` und ``flows``.
    """
    return {
        "nodes": {
            "bestellung eingegangen": {"kind": "Ereignis"},
            "bestellung pruefen": {"kind": "Funktion"},
            "ergebnis": {"kind": "Konnektor", "connector": "XOR"},
            "unterlagen in ordnung": {"kind": "Ereignis"},
            "unterlagen nicht in ordnung": {"kind": "Ereignis"},
            "bestellung bearbeiten": {"kind": "Funktion"},
            "bestellung stornieren": {"kind": "Funktion"},
            "bestellung bearbeitet": {"kind": "Ereignis"},
            "bestellung storniert": {"kind": "Ereignis"},
        },
        "flows": [("bestellung eingegangen", "bestellung pruefen"),
                  ("bestellung pruefen", "ergebnis"),
                  ("ergebnis", "unterlagen in ordnung"),
                  ("ergebnis", "unterlagen nicht in ordnung"),
                  ("unterlagen in ordnung", "bestellung bearbeiten"),
                  ("unterlagen nicht in ordnung", "bestellung stornieren"),
                  ("bestellung bearbeiten", "bestellung bearbeitet"),
                  ("bestellung stornieren", "bestellung storniert")],
    }


def _successors(model, name):
    """Nennt die Nachfolger eines Knotens."""
    return [target for source, target in model["flows"] if source == name]


def _predecessors(model, name):
    """Nennt die Vorgänger eines Knotens."""
    return [source for source, target in model["flows"] if target == name]


def _kind(model, name):
    """Nennt die Art eines Knotens.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    node = model["nodes"].get(name)
    if node is None:
        raise ValueError("unbekannter Knoten: %s" % name)
    return node["kind"]


def check(model):
    """Prüft eine Kette gegen die Regeln der Notation.

    Geprüft wird: die Kette beginnt und endet mit Ereignissen; Ereignisse
    und Funktionen wechseln sich ab, wobei Konnektoren übersprungen
    werden; nach einem Ereignis steht keine entscheidende Verzweigung;
    und kein Konnektor verzweigt und führt zugleich zusammen.

    Returns:
        Abbildung mit den Verstössen und den Rand-Ereignissen.

    Raises:
        ValueError: bei einem Fluss auf einen unbekannten Knoten.
    """
    for source, target in model["flows"]:
        _kind(model, source)
        _kind(model, target)
    problems = []
    starts = [name for name in sorted(model["nodes"])
              if not _predecessors(model, name)]
    ends = [name for name in sorted(model["nodes"])
            if not _successors(model, name)]
    for name in starts:
        if _kind(model, name) != "Ereignis":
            problems.append("beginnt nicht mit einem Ereignis: %s" % name)
    for name in ends:
        if _kind(model, name) != "Ereignis":
            problems.append("endet nicht mit einem Ereignis: %s" % name)
    for name in sorted(model["nodes"]):
        kind = _kind(model, name)
        following = _successors(model, name)
        if kind == "Konnektor":
            if len(_predecessors(model, name)) > 1 and len(following) > 1:
                problems.append("verzweigt und führt zusammen: %s" % name)
            connector = model["nodes"][name].get("connector")
            if (connector in DECIDING and len(following) > 1
                    and all(_kind(model, other) == "Ereignis"
                            for other in _predecessors(model, name))):
                problems.append("entscheidende Verzweigung nach einem "
                                "Ereignis: %s" % name)
            continue
        for other in following:
            if _kind(model, other) == kind:
                problems.append("%s folgt auf %s, beide sind %s"
                                % (other, name, kind))
    return {"problems": problems, "starts": starts, "ends": ends,
            "nodes": len(model["nodes"])}


def paths(model, limit=50):
    """Sammelt die Pfade vom Anfang bis zum Ende.

    Returns:
        Liste der Pfade als Tupel von Knotennamen.
    """
    starts = [name for name in sorted(model["nodes"])
              if not _predecessors(model, name)]
    found = []
    stack = [(name, (name,)) for name in starts]
    while stack:
        name, walked = stack.pop()
        following = _successors(model, name)
        if not following:
            found.append(walked)
            continue
        if len(walked) >= limit:
            continue
        for other in following:
            stack.append((other, walked + (other,)))
    return sorted(found)


def alternation_holds(model):
    """Prüft die Abwechslung entlang jedes Pfades.

    Das ist dieselbe Regel wie in ``check``, nur von der anderen Seite
    geprüft: statt über die Kanten zu laufen, werden die Pfade
    aufgezählt, die Konnektoren gestrichen und die Reste angesehen. Zwei
    unabhängige Wege zu derselben Aussage.
    """
    for walked in paths(model):
        kinds = [_kind(model, name) for name in walked
                 if _kind(model, name) != "Konnektor"]
        for first, second in zip(kinds, kinds[1:]):
            if first == second:
                return False
    return True
