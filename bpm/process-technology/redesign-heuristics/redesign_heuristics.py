"""Redesign: die Heuristiken und das Teufelsquadrat."""

QUADRANGLE = ("time", "cost", "quality", "flexibility")

HEURISTICS = {
    "parallelism": {
        "idea": "Aktivitäten, die nicht voneinander abhängen, gleichzeitig "
                "ausführen",
        "time": "better", "cost": "worse", "quality": "same",
        "flexibility": "same"},
    "triage": {
        "idea": "den Fall nach seiner kind of case aufteilen und je Art "
                "einen eigenen Weg vorsehen",
        "time": "better", "cost": "same", "quality": "better",
        "flexibility": "worse"},
    "resequencing": {
        "idea": "die Reihenfolge ändern, damit Fälle früher ausscheiden",
        "time": "better", "cost": "better", "quality": "same",
        "flexibility": "same"},
    "task elimination": {
        "idea": "Aktivitäten streichen, die keinen Wert schaffen",
        "time": "better", "cost": "better", "quality": "worse",
        "flexibility": "same"},
    "task composition": {
        "idea": "kleine Aktivitäten zusammenlegen und Übergaben sparen",
        "time": "better", "cost": "better", "quality": "same",
        "flexibility": "worse"},
    "empower": {
        "idea": "Entscheidungen dorthin geben, wo die Arbeit passiert",
        "time": "better", "cost": "better", "quality": "worse",
        "flexibility": "better"},
    "integral technology": {
        "idea": "eine technische Beschränkung aufheben, statt den Ablauf "
                "um sie herum zu bauen",
        "time": "better", "cost": "worse", "quality": "better",
        "flexibility": "better"},
    "exception": {
        "idea": "den Normalfall geradeziehen und Ausnahmen ausgliedern",
        "time": "better", "cost": "same", "quality": "better",
        "flexibility": "worse"},
}


def quadrangle():
    """Nennt die vier Ecken, die gegeneinander stehen."""
    return list(QUADRANGLE)


def heuristics():
    """Nennt die Heuristiken, alphabetisch."""
    return sorted(HEURISTICS)


def apply(name):
    """Beschreibt eine Heuristik und ihre Wirkung auf die vier Ecken.

    Raises:
        ValueError: bei einer unbekannten Heuristik.
    """
    if name not in HEURISTICS:
        raise ValueError("unbekannte Heuristik")
    row = dict(HEURISTICS[name])
    row["quadrangle"] = {corner: row[corner] for corner in QUADRANGLE}
    return row


def trade_offs():
    """Zählt, wie oft jede Ecke gewinnt und verliert.

    Die Zeit gewinnt bei jeder Heuristik; das ist kein Zufall, sondern
    zeigt, wofür die Sammlung gemacht wurde. Interessant sind die Ecken,
    die dafür bezahlen.

    Returns:
        Abbildung von der Ecke auf die Zahl der Verbesserungen und
        Verschlechterungen.
    """
    counted = {corner: {"better": 0, "worse": 0, "same": 0}
               for corner in QUADRANGLE}
    for row in HEURISTICS.values():
        for corner in QUADRANGLE:
            counted[corner][row[corner]] += 1
    return counted


def the_devil():
    """Erklärt, warum das Quadrat so heisst.

    Wer an einer Ecke zieht, bewegt die anderen mit. Eine Änderung, die
    Zeit spart, kostet in der Regel Geld oder Flexibilität; eine, die
    beides schont, senkt die Qualität. Ein Vorschlag, der alle vier Ecken
    verbessert, ist deshalb zuerst ein Anlass, die Annahmen zu prüfen.
    """
    return {"corners": list(QUADRANGLE),
            "rule": "pulling one corner moves the others",
            "suspicious": "a proposal that improves all four",
            "what to do": "name the corner that pays, before deciding"}
