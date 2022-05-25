"""Die Reduktion im pi-Kalkül: Übungsblatt 8."""

NIL = ("nil",)


def send(channel, message, rest=NIL):
    """Baut die Ausgabe x quer <y>.P."""
    return ("out", channel, message, rest)


def receive(channel, binder, rest=NIL):
    """Baut die Eingabe x(y).P; y wird dabei gebunden."""
    return ("in", channel, binder, rest)


def parallel(*parts):
    """Baut die parallele Zusammensetzung."""
    if not parts:
        return NIL
    built = parts[0]
    for part in parts[1:]:
        built = ("par", built, part)
    return built


def restrict(name, process):
    """Baut die Einschränkung (νx)P."""
    return ("res", name, process)


def replicate(process):
    """Baut die Replikation !P."""
    return ("rep", process)


def show(process):
    """Schreibt einen Term in der Notation der Vorlesung."""
    kind = process[0]
    if kind == "nil":
        return "0"
    if kind == "out":
        return "'%s<%s>.%s" % (process[1], process[2], show(process[3]))
    if kind == "in":
        return "%s(%s).%s" % (process[1], process[2], show(process[3]))
    if kind == "par":
        return "(%s | %s)" % (show(process[1]), show(process[2]))
    if kind == "res":
        return "(new %s)%s" % (process[1], show(process[2]))
    return "!%s" % show(process[1])


def free_names(process):
    """Nennt die freien Namen eines Terms.

    Gebunden wird durch die Eingabe, die ihren Parameter bindet, und
    durch die Einschränkung. Alles andere ist frei, und nur über freie
    Namen kann ein Term mit seiner Umgebung reagieren.
    """
    kind = process[0]
    if kind == "nil":
        return set()
    if kind == "out":
        return {process[1], process[2]} | free_names(process[3])
    if kind == "in":
        return {process[1]} | (free_names(process[3]) - {process[2]})
    if kind == "par":
        return free_names(process[1]) | free_names(process[2])
    if kind == "res":
        return free_names(process[2]) - {process[1]}
    return free_names(process[1])


def bound_names(process):
    """Nennt die gebundenen Namen eines Terms."""
    kind = process[0]
    if kind == "nil":
        return set()
    if kind == "out":
        return bound_names(process[3])
    if kind == "in":
        return {process[2]} | bound_names(process[3])
    if kind == "par":
        return bound_names(process[1]) | bound_names(process[2])
    if kind == "res":
        return {process[1]} | bound_names(process[2])
    return bound_names(process[1])


def substitute(process, old, new):
    """Ersetzt einen freien Namen durch einen anderen.

    Die Ersetzung hält vor einem Binder desselben Namens an: in
    ``x(y).P`` wird ein y innerhalb von P nicht ersetzt, weil es dort ein
    anderes y ist.
    """
    kind = process[0]
    if kind == "nil":
        return process
    if kind == "out":
        return ("out", new if process[1] == old else process[1],
                new if process[2] == old else process[2],
                substitute(process[3], old, new))
    if kind == "in":
        channel = new if process[1] == old else process[1]
        if process[2] == old:
            return ("in", channel, process[2], process[3])
        return ("in", channel, process[2],
                substitute(process[3], old, new))
    if kind == "par":
        return ("par", substitute(process[1], old, new),
                substitute(process[2], old, new))
    if kind == "res":
        if process[1] == old:
            return process
        return ("res", process[1], substitute(process[2], old, new))
    return ("rep", substitute(process[1], old, new))


def _flatten(process):
    """Zerlegt eine parallele Zusammensetzung in ihre Bestandteile."""
    if process[0] == "par":
        return _flatten(process[1]) + _flatten(process[2])
    if process[0] == "nil":
        return []
    return [process]


def normalise(process):
    """Entfernt 0 aus parallelen Zusammensetzungen.

    Das ist der Teil der strukturellen Kongruenz, den die Rechnung
    braucht: P | 0 ≡ P. Ohne ihn wachsen die Terme bei jedem Schritt.
    """
    kind = process[0]
    if kind == "par":
        parts = [normalise(part) for part in _flatten(process)]
        parts = [part for part in parts if part != NIL]
        if not parts:
            return NIL
        return parallel(*parts)
    if kind == "res":
        inner = normalise(process[2])
        return NIL if inner == NIL else ("res", process[1], inner)
    if kind == "out":
        return ("out", process[1], process[2], normalise(process[3]))
    if kind == "in":
        return ("in", process[1], process[2], normalise(process[3]))
    if kind == "rep":
        return ("rep", normalise(process[1]))
    return process


def _offers(process):
    """Nennt die Ausgaben und Eingaben, die ein Term unmittelbar anbietet.

    Returns:
        Paar aus zwei Listen; jede enthält Tupel aus dem Kanal, den
        Angaben des Präfixes und dem Rest, der nach der Reaktion bleibt.
    """
    kind = process[0]
    if kind == "out":
        return [(process[1], process[2], process[3], False)], []
    if kind == "in":
        return [], [(process[1], process[2], process[3], False)]
    if kind == "rep":
        sends, receives = _offers(process[1])
        return ([(channel, value, rest, True)
                 for channel, value, rest, _ in sends],
                [(channel, value, rest, True)
                 for channel, value, rest, _ in receives])
    return [], []


def _fresh(name, used):
    """Sucht einen Namen, der noch nicht benutzt wird."""
    if name not in used:
        return name
    index = 0
    while True:
        index += 1
        candidate = "%s%d" % (name, index)
        if candidate not in used:
            return candidate


def open_scopes(process):
    """Zieht die Einschränkungen der obersten Ebene nach aussen.

    Das ist die Regel ``(new x)(P | Q) ≡ P | (new x)Q``, in der Richtung
    gelesen, in der sie gebraucht wird: eine Einschränkung, die einen
    Teil des Terms umschliesst, wird über den ganzen Term gezogen, damit
    die Reaktionsregel eine Ausgabe und eine Eingabe nebeneinander sieht.
    Die Bedingung der Regel ist, dass der eingeschränkte Name in den
    Teilen, über die er gezogen wird, nicht frei vorkommt. Sonst würde
    ein bisher freier Name gebunden, und aus zwei Prozessen, die
    zufällig denselben Namen benutzen, würden zwei, die ihn teilen.
    Trifft das zu, wird der gebundene Name vorher umbenannt; damit
    bleibt die Reaktion über die Grenze hinweg richtigerweise aus.

    Returns:
        Paar aus den herausgezogenen Namen und den flachen Bestandteilen.
    """
    outside = set(free_names(process))
    used = outside | set(bound_names(process))
    names = []
    parts = []
    stack = _flatten(normalise(process))
    while stack:
        part = stack.pop(0)
        if part[0] == "res":
            name, body = part[1], part[2]
            if name in names or name in outside:
                other = _fresh(name, used | set(names))
                body = substitute(body, name, other)
                name = other
            used.add(name)
            names.append(name)
            stack = _flatten(body) + stack
            continue
        if part[0] == "par":
            stack = _flatten(part) + stack
            continue
        parts.append(part)
    return names, parts


def reactions(process):
    """Nennt die Terme, zu denen ein Term in einem Schritt reagieren kann.

    Die einzige Regel des Kalküls: treffen in einer parallelen
    Zusammensetzung eine Ausgabe und eine Eingabe auf demselben Kanal
    zusammen, so verschwinden beide Präfixe, und der übergebene Name
    wird im Rumpf der Eingabe für den gebundenen Namen eingesetzt. Eine
    Replikation bleibt dabei stehen und stellt eine weitere Kopie.

    Vor der Regel werden die Einschränkungen der obersten Ebene nach
    aussen gezogen. Ohne diesen Schritt könnte ein Prozess hinter einer
    Einschränkung mit einem davor nie reagieren, und eine kodierte Liste
    liesse sich nicht auslesen.

    Returns:
        Liste der Folgeterme.
    """
    names, parts = open_scopes(process)
    if not parts:
        return []

    def wrap(built):
        """Legt die herausgezogenen Einschränkungen wieder um den Term."""
        for name in reversed(names):
            built = restrict(name, built)
        return normalise(built)

    found = []
    for first in range(len(parts)):
        sends, _ = _offers(parts[first])
        for second in range(len(parts)):
            if first == second:
                continue
            _, receives = _offers(parts[second])
            for channel, value, sender_rest, sender_kept in sends:
                for other, binder, reader_rest, reader_kept in receives:
                    if channel != other:
                        continue
                    changed = list(parts)
                    changed[first] = (parts[first] if sender_kept
                                      else NIL)
                    changed[second] = (parts[second] if reader_kept
                                       else NIL)
                    result = changed + [sender_rest,
                                        substitute(reader_rest, binder,
                                                   value)]
                    found.append(wrap(parallel(*result)))
    return found


def reduce_fully(process, limit=40):
    """Reduziert einen Term, so weit es geht.

    Bei mehreren möglichen Reaktionen wird die erste genommen. Erreicht
    die Rechnung die Schranke, so ist das ein Hinweis auf eine
    unendliche Rechnung und wird als solcher gemeldet, nicht als
    Ergebnis.

    Args:
        process: der Term.
        limit: obere Schranke der Schritte.

    Returns:
        Abbildung mit der Kette, dem Endterm und dem Befund.
    """
    chain = [normalise(process)]
    for _ in range(limit):
        steps = reactions(chain[-1])
        if not steps:
            return {"steps": len(chain) - 1, "chain": [show(term)
                                                       for term in chain],
                    "result": show(chain[-1]), "terminates": True}
        chain.append(steps[0])
    return {"steps": limit, "chain": [show(term) for term in chain[:6]],
            "result": None, "terminates": False,
            "note": "die Rechnung erreicht die Schranke und hat "
                    "vermutlich unendlich viele Schritte"}


def examples():
    """Terme, an denen sich die Regel zeigt.

    Returns:
        Abbildung vom Namen auf den Term.
    """
    simple = parallel(send("x", "z"), receive("x", "y", send("y", "w")))
    chained = parallel(send("x", "a", send("x", "b")),
                       receive("x", "u", receive("x", "v")))
    hidden = restrict("x", parallel(send("x", "z"),
                                    receive("x", "y", NIL)))
    endless = parallel(replicate(send("x", "z")),
                       replicate(receive("x", "y", NIL)))
    stuck = parallel(send("x", "z"), receive("w", "y", NIL))
    return {"simple": simple, "chained": chained, "hidden": hidden,
            "endless": endless, "stuck": stuck}


def solved():
    """Reduziert die Beispiele und schreibt die Befunde auf.

    Returns:
        Abbildung vom Namen auf das Ergebnis.
    """
    return {name: reduce_fully(term)
            for name, term in examples().items()}


def the_name_travels():
    """Zeigt, was den pi-Kalkül von CCS unterscheidet.

    In CCS reagieren zwei Prozesse über einen festen Kanalnamen, und was
    dabei fliesst, ist nichts weiter als die Tatsache der Reaktion. Im
    pi-Kalkül fliesst ein Name, und der Empfänger kann ihn danach als
    Kanal benutzen. Damit ändert sich die Verbindungsstruktur zur
    Laufzeit, und genau das heisst Mobilität.

    Returns:
        Abbildung mit dem Beispiel und dem, was der Empfänger danach
        kann.
    """
    term = parallel(send("x", "z"), receive("x", "y", send("y", "w")))
    after = reactions(term)
    return {"before": show(term),
            "after": [show(other) for other in after],
            "what changed": "der Empfänger sendet nun auf z, einen Kanal, "
                            "den er vorher nicht kannte",
            "in CCS": "unmöglich, weil dort keine Namen fliessen"}


def a_restricted_name_stays_inside():
    """Zeigt, dass eine Einschränkung die Reaktion nicht verhindert.

    Ein eingeschränkter Name ist nach aussen unsichtbar, aber innerhalb
    der Einschränkung reagieren die Prozesse ganz normal. Das ist der
    Unterschied zu CCS, wo die Einschränkung Aktionen ganz verbietet:
    hier verbirgt sie nur, wer mitreden darf.

    Returns:
        Abbildung mit dem Term und seinen Folgetermen.
    """
    inside = restrict("x", parallel(send("x", "z"),
                                    receive("x", "y", NIL)))
    outside = parallel(restrict("x", send("x", "z")),
                       receive("x", "y", NIL))
    return {"inside reacts": bool(reactions(inside)),
            "across the border reacts": bool(reactions(outside)),
            "why": "innerhalb der Einschränkung ist der Name geteilt, "
                   "über die Grenze hinweg nicht"}
