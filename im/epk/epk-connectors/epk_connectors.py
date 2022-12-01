"""Die Konnektoren und die Regel, wer entscheiden darf."""

CONNECTORS = {
    "XOR": {"branches taken": "genau einer",
            "join waits for": "den einen Zweig, der gelaufen ist"},
    "OR": {"branches taken": "mindestens einer",
           "join waits for": "die Zweige, die gelaufen sind"},
    "AND": {"branches taken": "alle",
            "join waits for": "alle Zweige"},
}

DECIDING = ("XOR", "OR")


def connectors():
    """Nennt die drei Konnektoren."""
    return sorted(CONNECTORS)


def describe(kind):
    """Beschreibt einen Konnektor.

    Raises:
        ValueError: bei einem unbekannten Konnektor.
    """
    if kind not in CONNECTORS:
        raise ValueError("unbekannter Konnektor")
    return dict(CONNECTORS[kind])


def may_follow(predecessor, kind, splitting=True):
    """Sagt, ob ein Konnektor auf einen Baustein folgen darf.

    Die Regel, die die EPK von anderen Notationen unterscheidet: nach
    einem Ereignis darf keine entscheidende Verzweigung stehen. Ein
    Ereignis ist passiv; es stellt fest, dass etwas eingetreten ist, und
    kann nicht wählen, welcher Zweig weitergeht. Wählen kann nur eine
    Funktion.

    Args:
        predecessor: ``Ereignis`` oder ``Funktion``.
        kind: der Konnektor.
        splitting: ob er verzweigt; eine Zusammenführung ist immer
            erlaubt.

    Returns:
        Abbildung mit dem Urteil und der Begründung.

    Raises:
        ValueError: bei einem unbekannten Baustein oder Konnektor.
    """
    if predecessor not in ("Ereignis", "Funktion"):
        raise ValueError("unbekannter Baustein")
    if kind not in CONNECTORS:
        raise ValueError("unbekannter Konnektor")
    if not splitting or kind not in DECIDING:
        return {"allowed": True,
                "why": "eine Zusammenführung und das UND entscheiden nicht"}
    allowed = predecessor == "Funktion"
    return {"allowed": allowed,
            "why": "nur eine Funktion kann entscheiden, ein Ereignis "
                   "stellt nur fest" if not allowed
                   else "eine Funktion darf entscheiden"}


def matching(split, join):
    """Prüft, ob Verzweigung und Zusammenführung zusammenpassen.

    Raises:
        ValueError: bei einem unbekannten Konnektor.
    """
    for kind in (split, join):
        if kind not in CONNECTORS:
            raise ValueError("unbekannter Konnektor")
    return {"matched": split == join, "split": split, "join": join,
            "risk": None if split == join else
            "eine parallele Verzweigung mit exklusiver Zusammenführung "
            "lässt den Prozess doppelt enden, umgekehrt bleibt er stehen"}


def one_direction_only(incoming, outgoing):
    """Prüft die Regel, dass ein Konnektor nur in eine Richtung wirkt.

    Ein Konnektor verzweigt oder führt zusammen, nie beides zugleich. Ein
    Knoten mit zwei Eingängen und zwei Ausgängen liesse offen, welcher
    Eingang zu welchem Ausgang gehört.

    Raises:
        ValueError: bei einer Zahl unter eins.
    """
    if incoming < 1 or outgoing < 1:
        raise ValueError("ein Konnektor braucht mindestens je eine Kante")
    both = incoming > 1 and outgoing > 1
    return {"valid": not both, "role": "Zusammenführung" if incoming > 1
            else "Verzweigung" if outgoing > 1 else "Durchgang",
            "why": "ein Konnektor tut eines von beiden, nicht beides"}


def or_join_problem():
    """Nennt, warum die inklusive Zusammenführung schwer ist.

    Sie muss wissen, welche Zweige überhaupt gelaufen sind, und das steht
    nicht an ihr, sondern an der Verzweigung weit davor. Deshalb ist sie
    in ausführbaren Notationen entweder eingeschränkt oder verboten, und
    in der EPK ist sie erlaubt, weil dort nichts ausgeführt wird.
    """
    return {"needs": "die Kenntnis der genommenen Zweige",
            "knows": "nur, was bei ihr ankommt",
            "in EPK": "erlaubt, weil das Modell nicht ausgeführt wird",
            "in executable notations": "eingeschränkt oder verboten"}
