"""Die Syntax von CCS und ihre strukturellen Gleichungen."""

NIL = ("nil",)


def prefix(action, process):
    """Baut den Präfix α.P."""
    return ("prefix", action, process)


def choice(*parts):
    """Baut die Auswahl über beliebig viele Teile."""
    if not parts:
        return NIL
    built = parts[0]
    for part in parts[1:]:
        built = ("sum", built, part)
    return built


def parallel(*parts):
    """Baut die parallele Zusammensetzung."""
    if not parts:
        return NIL
    built = parts[0]
    for part in parts[1:]:
        built = ("par", built, part)
    return built


def restrict(name, process):
    """Baut die Einschränkung (νa)P."""
    return ("res", name, process)


def call(name, *arguments):
    """Baut den Aufruf einer Definition."""
    return ("call", name, tuple(arguments))


def action_in(name):
    """Die Eingabeaktion a."""
    return ("in", name)


def action_out(name):
    """Die Ausgabeaktion a quer."""
    return ("out", name)


TAU = ("tau", None)


def operators():
    """Nennt die Konstrukte des Kalküls mit ihrer Bedeutung."""
    return {"0": "der Prozess, der nichts tut",
            "α.P": "bietet die Aktion α an und wird danach zu P",
            "P + Q": "verhält sich wie P oder wie Q, und die nicht "
                     "genommene Seite verschwindet",
            "P | Q": "beide laufen nebeneinander und können miteinander "
                     "reagieren",
            "(νa)P": "der Name a ist innerhalb von P privat",
            "A⟨a⟩": "der Aufruf einer Definition, das Mittel für "
                    "Wiederholung"}


def show(process):
    """Schreibt einen Prozess in der Notation der Vorlesung."""
    kind = process[0]
    if kind == "nil":
        return "0"
    if kind == "prefix":
        action = process[1]
        if action[0] == "tau":
            text = "tau"
        else:
            text = ("'" if action[0] == "out" else "") + action[1]
        return "%s.%s" % (text, show(process[2]))
    if kind == "sum":
        return "(%s + %s)" % (show(process[1]), show(process[2]))
    if kind == "par":
        return "(%s | %s)" % (show(process[1]), show(process[2]))
    if kind == "res":
        return "(new %s)%s" % (process[1], show(process[2]))
    return "%s<%s>" % (process[1], ",".join(process[2]))


def names(process):
    """Nennt die Aktionsnamen, die in einem Prozess vorkommen."""
    kind = process[0]
    if kind == "nil":
        return set()
    if kind == "prefix":
        action = process[1]
        head = set() if action[0] == "tau" else {action[1]}
        return head | names(process[2])
    if kind in ("sum", "par"):
        return names(process[1]) | names(process[2])
    if kind == "res":
        return names(process[2])
    return set(process[2])


def restricted_names(process):
    """Nennt die Namen, die irgendwo im Term eingeschränkt werden.

    Die Menge sagt nur, welche Namen als gebunden vorkommen, nicht wo.
    Für die Frage, ob ein Prozess über einen Namen nach aussen reagieren
    kann, ist ``visible_names`` zuständig.
    """
    kind = process[0]
    if kind == "nil":
        return set()
    if kind == "prefix":
        return restricted_names(process[2])
    if kind in ("sum", "par"):
        return restricted_names(process[1]) | restricted_names(process[2])
    if kind == "res":
        return {process[1]} | restricted_names(process[2])
    return set()


def visible_names(process):
    """Nennt die Namen, über die ein Prozess mit aussen reagieren kann.

    Die Einschränkung wirkt nur in ihrem eigenen Geltungsbereich, und
    deshalb genügt es nicht, alle eingeschränkten Namen von allen
    vorkommenden abzuziehen. In ``((νa)a.b.0 + c.0) | ā.0`` ist a links
    gebunden und rechts frei; der Name ist also sichtbar, und die
    Einschränkung verhindert nur, dass die beiden Seiten über ihn
    miteinander reagieren.

    Gerechnet wird deshalb rekursiv: an jeder Einschränkung fällt ihr
    Name aus den Namen des Teilterms heraus, und nur aus diesen.
    """
    kind = process[0]
    if kind == "nil":
        return set()
    if kind == "prefix":
        action = process[1]
        head = set() if action[0] == "tau" else {action[1]}
        return head | visible_names(process[2])
    if kind in ("sum", "par"):
        return visible_names(process[1]) | visible_names(process[2])
    if kind == "res":
        return visible_names(process[2]) - {process[1]}
    return set(process[2])


def free_names(process):
    """Nennt die sichtbaren Namen als sortierte Liste."""
    return sorted(visible_names(process))


def structural_laws():
    """Nennt die Gleichungen, die Terme umformen, ohne sie zu ändern."""
    return ["P | 0 ≡ P",
            "P | Q ≡ Q | P",
            "(P | Q) | R ≡ P | (Q | R)",
            "P + 0 ≡ P",
            "P + Q ≡ Q + P",
            "(P + Q) + R ≡ P + (Q + R)",
            "(νa)0 ≡ 0",
            "(νa)(νb)P ≡ (νb)(νa)P",
            "(νa)(P | Q) ≡ P | (νa)Q, falls a nicht in P vorkommt"]


def why_sum_is_not_parallel():
    """Trennt die beiden Operatoren, die am leichtesten verwechselt werden.

    ``a.0 + b.0`` bietet a oder b an, und wer eines nimmt, hat das
    andere verloren. ``a.0 | b.0`` bietet beide an und behält nach der
    ersten Aktion die zweite. Der Unterschied zeigt sich erst im zweiten
    Schritt, weshalb er sich an der Sprache nicht ablesen lässt.
    """
    a, b = action_in("a"), action_in("b")
    return {"sum": show(choice(prefix(a, NIL), prefix(b, NIL))),
            "parallel": show(parallel(prefix(a, NIL), prefix(b, NIL))),
            "after a, the sum offers": "nichts",
            "after a, the parallel offers": "b",
            "visible in the language": False,
            "visible in the transition graph": True}
