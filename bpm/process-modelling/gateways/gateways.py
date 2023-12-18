"""Die drei Gateways und die Prüfung, ob Verzweigung und Zusammenführung
zusammenpassen."""

KINDS = ("xor", "and", "or")

MEANING = {
    "xor": "genau ein Zweig, entschieden an einer Bedingung",
    "and": "alle Zweige, gleichzeitig",
    "or": "mindestens ein Zweig, jede nicht leere Auswahl ist möglich",
}


def kinds():
    """Nennt die drei Gateways."""
    return list(KINDS)


def meaning(kind):
    """Beschreibt ein Gateway.

    Raises:
        ValueError: bei einem unbekannten Gateway.
    """
    if kind not in MEANING:
        raise ValueError("unbekanntes Gateway")
    return MEANING[kind]


def branches_taken(kind, branches):
    """Nennt, wie viele Zweige ein Gateway nehmen kann.

    Args:
        kind: ``xor``, ``and`` oder ``or``.
        branches: Zahl der ausgehenden Zweige.

    Returns:
        Aufsteigende Liste der möglichen Zweigzahlen.

    Raises:
        ValueError: bei einem unbekannten Gateway oder bei weniger als
            einem Zweig.
    """
    if kind not in MEANING:
        raise ValueError("unbekanntes Gateway")
    if branches < 1:
        raise ValueError("mindestens ein Zweig")
    if kind == "xor":
        return [1]
    if kind == "and":
        return [branches]
    return list(range(1, branches + 1))


def example():
    """Ein Modell mit einer parallelen Verzweigung und Zusammenführung.

    Returns:
        Abbildung mit ``nodes`` und ``flows``.
    """
    return {
        "nodes": {"start": {"type": "start"},
                  "split": {"type": "gateway", "gateway": "and"},
                  "ship": {"type": "task"},
                  "invoice": {"type": "task"},
                  "join": {"type": "gateway", "gateway": "and"},
                  "end": {"type": "end"}},
        "flows": [("start", "split"), ("split", "ship"),
                  ("split", "invoice"), ("ship", "join"),
                  ("invoice", "join"), ("join", "end")],
    }


def _outgoing(model, name):
    """Nennt die Nachfolger eines Knotens."""
    return [target for source, target in model["flows"] if source == name]


def _incoming(model, name):
    """Nennt die Vorgänger eines Knotens."""
    return [source for source, target in model["flows"] if target == name]


def splits(model):
    """Nennt die Gateways mit mehr als einem Ausgang, alphabetisch."""
    return sorted(name for name in model["nodes"]
                  if len(_outgoing(model, name)) > 1)


def joins(model):
    """Nennt die Gateways mit mehr als einem Eingang, alphabetisch."""
    return sorted(name for name in model["nodes"]
                  if len(_incoming(model, name)) > 1)


def _first_join_after(model, name, stop):
    """Folgt einem Zweig bis zur ersten Zusammenführung.

    Returns:
        Der Name der Zusammenführung oder ``None``, wenn der Zweig vorher
        endet oder im Kreis läuft.
    """
    seen = set()
    while name not in stop:
        if name in seen:
            return None
        seen.add(name)
        following = _outgoing(model, name)
        if len(following) != 1:
            return None
        name = following[0]
    return name


def matching(model):
    """Prüft, ob jede Verzweigung von der gleichen Art zusammengeführt wird.

    Eine parallele Verzweigung, die exklusiv zusammengeführt wird, läuft
    fest, und eine exklusive Verzweigung mit paralleler Zusammenführung
    wartet auf eine Marke, die nie kommt. Beides fällt hier auf, ohne dass
    das Modell ausgeführt werden muss.

    Returns:
        Abbildung mit ``matched``, den gefundenen Paaren und den Paaren,
        deren Arten nicht übereinstimmen.
    """
    stop = set(joins(model))
    pairs = []
    mismatched = []
    for split in splits(model):
        reached = {_first_join_after(model, branch, stop)
                   for branch in _outgoing(model, split)}
        if len(reached) != 1:
            continue
        join = reached.pop()
        if join is None:
            continue
        pairs.append((split, join))
        if (model["nodes"][split].get("gateway")
                != model["nodes"][join].get("gateway")):
            mismatched.append((split, join))
    return {"matched": not mismatched, "pairs": pairs,
            "mismatched": mismatched}


def why_or_is_expensive():
    """Sagt, warum das inklusive Gateway die teuerste Wahl ist.

    Bei n Zweigen sind 2ⁿ − 1 Auswahlen möglich, und die Zusammenführung
    muss wissen, auf welche Zweige sie wartet; sie kann nicht einfach
    zählen. Deshalb ist das inklusive Gateway in vielen Werkzeugen
    entweder eingeschränkt oder gar nicht ausführbar.
    """
    return {"combinations": "2 to the number of branches, minus one",
            "join must know": "which branches were actually taken",
            "consequence": "many engines restrict or forbid it"}
