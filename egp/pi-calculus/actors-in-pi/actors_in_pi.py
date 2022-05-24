"""Das Actor-Modell im pi-Kalkül: Foliensatz 10."""

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


def actor(mail, behaviour):
    """Kodiert einen Aktor als replizierte Eingabe auf seinem Postkanal.

    Ein Aktor ist ein Prozess, der immer wieder eine Nachricht auf
    seiner Adresse annimmt und darauf reagiert. Die Replikation ist
    genau das: sie stellt nach jeder angenommenen Nachricht eine neue
    Kopie bereit, so dass der Aktor empfangsbereit bleibt.

    Args:
        mail: der Kanal, der die Adresse des Aktors ist.
        behaviour: eine Funktion vom gebundenen Namen der Nachricht auf
            den Rumpf.

    Returns:
        Der Prozess.
    """
    return replicate(receive(mail, "msg", behaviour("msg")))


def create(name, body):
    """Kodiert das Erzeugen eines Aktors als Einschränkung.

    ``create`` liefert eine Adresse, die vorher niemand kannte. Im
    Kalkül ist das die Einschränkung: ein frischer Name, der nur den
    Prozessen bekannt ist, die innerhalb stehen, und der weitergegeben
    werden kann.
    """
    return restrict(name, body)


def tell(address, message, rest=NIL):
    """Kodiert das Senden als Ausgabe."""
    return send(address, message, rest)


def correspondence():
    """Ordnet die drei Grundoperationen ihren Entsprechungen zu.

    Die Übereinstimmung ist die Aussage des Foliensatzes: das
    Aktormodell braucht keine eigene Theorie, es ist ein Fragment des
    pi-Kalküls. Was im Aktormodell eine Adresse ist, ist im Kalkül ein
    Name; was dort eine Nachricht ist, ist hier eine Ausgabe; und der
    Wechsel des Verhaltens ist die Wahl des Rumpfes nach der Eingabe.
    """
    return {"create": "(new a)P, eine Einschränkung",
            "send": "'a<v>.P, eine Ausgabe",
            "become": "die Wahl des Rumpfes hinter der Eingabe",
            "address": "ein Name",
            "mailbox": "die replizierte Eingabe auf dem Namen",
            "conclusion": "das Aktormodell ist ein Ausschnitt des "
                          "pi-Kalküls"}


def what_the_encoding_does_not_capture():
    """Nennt, was bei der Kodierung verlorengeht.

    Die replizierte Eingabe nimmt beliebig viele Nachrichten zugleich
    an: jede Kopie bearbeitet eine, und die Kopien laufen parallel. Ein
    Aktor bearbeitet dagegen eine Nachricht zur Zeit. Wer das braucht,
    muss es im Kalkül nachbauen, etwa indem der Rumpf am Ende einen
    Marker zurücklegt, den die nächste Kopie erst holen muss.

    Ebenso fehlt der Posteingang als Warteschlange. Im Kalkül liegen die
    Nachrichten ungeordnet nebeneinander, was zur Theorie von Agha
    passt und nicht zu den üblichen Umsetzungen.
    """
    return {"one message at a time": False,
            "how to get it": "einen Marker, den der Rumpf zurücklegt",
            "mailbox order": "keine, die Nachrichten liegen nebeneinander",
            "matches": "Aghas Theorie, nicht die üblichen Umsetzungen"}


def echo_example():
    """Ein Aktor, der jede Nachricht an eine feste Adresse weiterreicht.

    Returns:
        Abbildung mit dem Term und dem Ergebnis einer Reduktion.
    """
    forwarder = actor("a", lambda name: send("out", name))
    system = parallel(forwarder, tell("a", "x"), tell("a", "y"))
    steps = reactions(system)
    return {"actor": show(forwarder),
            "system": show(system),
            "reactions available": len(steps),
            "stays ready": "die Replikation bleibt nach der Reaktion "
                           "stehen"}


def one_at_a_time_example():
    """Zeigt den Marker, der einen Aktor auf eine Nachricht beschränkt.

    Der Rumpf holt sich zuerst den Marker vom Kanal ``lock`` und legt
    ihn am Ende zurück. Solange er ihn hält, kann keine zweite Kopie
    beginnen. Das ist eine Sperre, und dass sie hier nötig wird, zeigt,
    wo die Kodierung vom Modell abweicht.

    Returns:
        Abbildung mit dem Term.
    """
    guarded = replicate(receive("lock", "token",
                                receive("a", "msg",
                                        send("out", "msg",
                                             send("lock", "token")))))
    return {"term": show(guarded),
            "idea": "der Marker macht aus der Replikation eine Reihe",
            "cost": "eine Nachricht mehr je Bearbeitung"}
