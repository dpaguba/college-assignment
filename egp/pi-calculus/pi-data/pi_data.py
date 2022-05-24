"""Daten im pi-Kalkül: die Listenkodierung aus Übungsblatt 9."""

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


def encode_list(values, channel, fresh="t"):
    """Kodiert eine Liste als Prozess über einem Kanal.

    Eine Zelle schickt über den Kanal zuerst ihren Wert und danach den
    Kanal, unter dem der Rest der Liste zu erreichen ist. Der Rest liegt
    hinter einer Einschränkung, damit sein Kanal frisch ist und nicht
    mit einem anderen zusammenfällt.

    Die leere Liste schickt den Namen ``nil`` und hört auf.

    Args:
        values: die Elemente.
        channel: der Kanal, unter dem die Liste erreichbar ist.
        fresh: der Stamm für die frischen Kanalnamen.

    Returns:
        Der Prozess.
    """
    if not values:
        return send(channel, "nil")
    head = values[0]
    tail_channel = "%s%d" % (fresh, len(values))
    return restrict(tail_channel,
                    parallel(send(channel, head,
                                  send(channel, tail_channel)),
                             encode_list(values[1:], tail_channel, fresh)))


def reader(channel, count, collected="got"):
    """Baut einen Prozess, der eine Liste ausliest.

    Er liest abwechselnd einen Wert und den Kanal des Restes. Der
    gelesene Wert wird über den Kanal ``got`` gemeldet, und zwar in
    einem eigenen parallelen Zweig: eine Ausgabe blockiert im
    synchronen Kalkül, bis jemand sie annimmt, und niemand nimmt ``got``
    an. Stünde die Meldung als Präfix vor dem Weiterlesen, so bliebe der
    Leser nach dem ersten Element stehen.

    Raises:
        ValueError: bei einer negativen Zahl.
    """
    if count < 0:
        raise ValueError("negative Zahl von Elementen")
    if count == 0:
        return NIL
    return receive(channel, "v",
                   parallel(send(collected, "v"),
                            receive(channel, "rest",
                                    reader("rest", count - 1,
                                           collected))))


def read_back(values, limit=60):
    """Kodiert eine Liste, liest sie wieder aus und meldet, was ankam.

    Das ist die Probe auf die Kodierung: nur wenn die Werte in der
    richtigen Reihenfolge wieder herauskommen, beschreibt der Prozess
    die Liste.

    Args:
        values: die Elemente.
        limit: obere Schranke der Reduktionsschritte.

    Returns:
        Abbildung mit den ausgelesenen Werten und dem Urteil.

    Raises:
        ValueError: bei einer nicht positiven Schranke.
    """
    if limit < 1:
        raise ValueError("die Schranke muss positiv sein")
    wanted = list(values)
    current = normalise(parallel(encode_list(wanted, "k"),
                                 reader("k", len(wanted))))
    got = []
    before = _counted(current)
    for _ in range(limit):
        steps = reactions(current)
        if not steps:
            break
        current = steps[0]
        after = _counted(current)
        for value, count in sorted(after.items()):
            got.extend([value] * (count - before.get(value, 0)))
        before = after
    return {"encoded": show(encode_list(wanted, "k")),
            "read back": got, "matches": got == wanted,
            "left in the term": sorted(_reported(current))}


def _reported(process):
    """Sammelt die Werte, die über den Kanal got ausgegeben wurden.

    Die Reihenfolge im Term sagt nichts: die parallele Zusammensetzung
    ist kommutativ, und was hier steht, ist eine Menge von Meldungen und
    keine Folge. Die Reihenfolge des Lesens wird deshalb während der
    Reduktion mitgeschrieben und nicht am Ende abgelesen.
    """
    kind = process[0]
    if kind == "out":
        head = [process[2]] if process[1] == "got" else []
        return head + _reported(process[3])
    if kind == "in":
        return _reported(process[3])
    if kind == "par":
        return _reported(process[1]) + _reported(process[2])
    if kind in ("res", "rep"):
        return _reported(process[2 if kind == "res" else 1])
    return []


def _counted(process):
    """Zählt die gemeldeten Werte."""
    counted = {}
    for value in _reported(process):
        counted[value] = counted.get(value, 0) + 1
    return counted


def why_two_messages_per_cell():
    """Erklärt, warum eine Zelle zweimal sendet.

    Der Kalkül überträgt einen Namen je Reaktion. Ein Paar aus Wert und
    Restkanal passt nicht in eine Nachricht, also wird es in zwei
    zerlegt, und die Reihenfolge ist Teil der Vereinbarung: erst der
    Wert, dann der Rest. Wer sie umdreht, bekommt einen Leser, der
    Werte für Kanäle hält.

    Der polyadische Kalkül erlaubt Tupel und ist genau diese
    Zerlegung als Abkürzung.
    """
    return {"monadic": "ein Name je Reaktion",
            "a cell needs": "Wert und Restkanal",
            "so": "zwei Reaktionen in fester Reihenfolge",
            "polyadic pi": "erlaubt Tupel und ist die Abkürzung dafür",
            "risk": "die Reihenfolge ist eine Vereinbarung, kein Typ"}


def encoding_of_booleans():
    """Zeigt die übliche Kodierung von Wahrheitswerten.

    Ein Wahrheitswert wird zu einem Prozess, der über einen Kanal zwei
    Namen entgegennimmt und auf einem von beiden antwortet. Wahr wählt
    den ersten, falsch den zweiten. Das ist dieselbe Idee wie bei der
    Liste: Daten sind Verhalten.
    """
    return {"true": "k(t).k(f).'t<>.0",
            "false": "k(t).k(f).'f<>.0",
            "idea": "ein Datum ist ein Prozess, der sich unterscheidbar "
                    "verhält",
            "same for": ["Zahlen als Church-Zahlen", "Listen", "Paare"]}
