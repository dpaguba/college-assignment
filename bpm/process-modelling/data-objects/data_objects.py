"""Datenobjekte, Datenspeicher und die Prüfung der Datenflüsse."""

KINDS = {"data object": False, "data store": True}


def survives_the_instance(kind):
    """Sagt, ob die Daten den einzelnen Fall überdauern.

    Ein Datenobjekt gehört zu einer Prozessinstanz und verschwindet mit
    ihr. Ein Datenspeicher liegt daneben und wird von allen Instanzen
    gelesen und geschrieben.

    Raises:
        ValueError: bei einer unbekannten Art.
    """
    if kind not in KINDS:
        raise ValueError("unbekannte Datenart")
    return KINDS[kind]


def example():
    """Ein Modell mit Datenobjekten und ihren Verknüpfungen.

    Returns:
        Abbildung mit ``order``, ``reads`` und ``writes``.
    """
    return {
        "order": ["annehmen", "prüfen", "entscheiden"],
        "writes": [("annehmen", "Antrag"), ("prüfen", "Bewertung")],
        "reads": [("prüfen", "Antrag"), ("entscheiden", "Bewertung")],
    }


def check(model):
    """Prüft die Datenverknüpfungen gegen die Reihenfolge der Aktivitäten.

    Gesucht wird zweierlei: ein Objekt, das gelesen wird, bevor es je
    geschrieben wurde (dann fehlt im Modell, woher es kommt), und ein
    Objekt, das geschrieben und nie gelesen wird (dann ist unklar, wozu
    die Aktivität es erzeugt).

    Args:
        model: Abbildung mit ``order``, ``reads`` und ``writes``.

    Returns:
        Abbildung mit beiden Befunden.

    Raises:
        ValueError: wenn eine Verknüpfung eine Aktivität nennt, die nicht
            in der Reihenfolge steht.
    """
    order = list(model["order"])
    position = {name: index for index, name in enumerate(order)}
    for activity, _ in list(model["reads"]) + list(model["writes"]):
        if activity not in position:
            raise ValueError("unbekannte Aktivität: %s" % activity)
    first_write = {}
    for activity, name in model["writes"]:
        index = position[activity]
        if name not in first_write or index < first_write[name]:
            first_write[name] = index
    read_before = []
    for activity, name in model["reads"]:
        if position[activity] <= first_write.get(name, len(order)):
            read_before.append(name)
    read_names = {name for _, name in model["reads"]}
    never_read = sorted({name for _, name in model["writes"]}
                        - read_names)
    return {"read before written": sorted(set(read_before)),
            "written but never read": never_read,
            "objects": sorted(set(first_write) | read_names)}


def association_kinds():
    """Nennt die Richtungen einer Datenverknüpfung."""
    return {"input": "von den Daten zur Aktivität, gestrichelter Pfeil",
            "output": "von der Aktivität zu den Daten",
            "note": "die Verknüpfung ist kein Kontrollfluss und ordnet "
                    "nichts an"}


def why_data_is_missing_in_conceptual_models():
    """Sagt, warum Datenaspekte im fachlichen Modell oft fehlen.

    Wer den Ablauf zeichnet, denkt in Tätigkeiten und Entscheidungen; die
    Daten sind für die Beteiligten selbstverständlich und werden nicht
    genannt. Für die Ausführung fehlen sie dann: eine Maschine kann eine
    Bedingung nicht auswerten, deren Datenquelle nirgends steht.
    """
    return {"reason": "the participants take the data for granted",
            "consequence": "a gateway condition with no source for its value",
            "fix": "add the objects that every condition reads"}
