"""Syntax des pi-Kalküls: freie und gebundene Namen."""

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


def binders():
    """Nennt die beiden Konstrukte, die Namen binden.

    Die Eingabe bindet ihren Parameter im Rumpf, die Einschränkung
    bindet ihren Namen im ganzen Term. Die Ausgabe bindet nichts: sie
    verschickt einen Namen, den sie selbst schon kennen muss.
    """
    return {"x(y).P": "bindet y in P",
            "(new x)P": "bindet x in P",
            "'x<y>.P": "bindet nichts"}


def alpha_convert(process, old, new):
    """Benennt einen gebundenen Namen um.

    Erlaubt ist die Umbenennung nur, wenn der neue Name im Term nicht
    schon frei vorkommt; sonst würde ein bisher freies Vorkommen
    plötzlich gebunden, und der Term hiesse etwas anderes.

    Raises:
        ValueError: wenn der neue Name im Term frei vorkommt oder der
            alte nicht gebunden wird.
    """
    if new in free_names(process):
        raise ValueError("der neue Name kommt frei vor: %s" % new)
    kind = process[0]
    if kind == "in" and process[2] == old:
        return ("in", process[1], new,
                substitute(process[3], old, new))
    if kind == "res" and process[1] == old:
        return ("res", new, substitute(process[2], old, new))
    raise ValueError("der Name wird hier nicht gebunden: %s" % old)


def capture_example():
    """Zeigt, warum die Bedingung der Umbenennung nötig ist.

    In ``(new x)'y<x>.0`` ist x gebunden und y frei. Wird x in y
    umbenannt, so entsteht ``(new y)'y<y>.0``, und das vorher freie y ist
    nun gebunden: der Term redet nicht mehr mit der Aussenwelt. Deshalb
    lehnt ``alpha_convert`` die Umbenennung ab.

    Returns:
        Abbildung mit dem Term, dem Versuch und der Meldung.
    """
    term = restrict("x", send("y", "x"))
    try:
        alpha_convert(term, "x", "y")
        message = None
    except ValueError as problem:
        message = str(problem)
    fine = alpha_convert(term, "x", "z")
    return {"term": show(term), "free before": sorted(free_names(term)),
            "renaming to a free name rejected": message,
            "renaming to a fresh name": show(fine),
            "free after": sorted(free_names(fine))}


def scope(process):
    """Nennt die freien und gebundenen Namen eines Terms.

    Ein Name kann beides sein: in ``x(y).0 | 'y<z>.0`` ist y links
    gebunden und rechts frei, weil die beiden Seiten verschiedene y
    meinen. Genau daran hängt, ob zwei Prozesse überhaupt miteinander
    reden können.
    """
    return {"free": sorted(free_names(process)),
            "bound": sorted(bound_names(process)),
            "both": sorted(free_names(process) & bound_names(process))}


def structural_congruence():
    """Nennt die Gleichungen, die vor der Reaktion angewandt werden.

    Sie ordnen den Term um, ohne ihn zu ändern: Parallelität ist
    kommutativ und assoziativ, 0 ist ihr neutrales Element,
    Einschränkungen dürfen vertauscht und über Prozesse geschoben
    werden, die den Namen nicht frei enthalten, und die Replikation
    darf jederzeit eine Kopie abgeben.
    """
    return ["P | Q ≡ Q | P",
            "(P | Q) | R ≡ P | (Q | R)",
            "P | 0 ≡ P",
            "(new x)(new y)P ≡ (new y)(new x)P",
            "(new x)(P | Q) ≡ P | (new x)Q, falls x nicht frei in P",
            "!P ≡ P | !P"]


def why_the_congruence_comes_first():
    """Sagt, wozu die Umformung dient.

    Die Reaktionsregel sieht nur eine Ausgabe und eine Eingabe
    nebeneinander. Stehen sie im Term an entfernten Stellen, so muss er
    erst umgeordnet werden, damit die Regel greift. Die Kongruenz macht
    genau das und ist deshalb kein Beiwerk, sondern die Hälfte der
    Semantik.
    """
    return {"the rule sees": "eine Ausgabe neben einer Eingabe",
            "the congruence provides": "die Umordnung, bis sie nebeneinander "
                                       "stehen",
            "consequence": "ohne Kongruenz wäre die Reaktion von der "
                           "Schreibweise abhängig"}
