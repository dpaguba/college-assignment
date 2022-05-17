"""Der Transitionsgraph eines Prozesses und seine Sprache."""

NIL = ("nil",)


def prefix(action, process):
    """Baut den Präfix α.P."""
    return ("prefix", action, process)


def choice(*parts):
    """Baut die Auswahl P + Q + ..."""
    if not parts:
        return NIL
    built = parts[0]
    for part in parts[1:]:
        built = ("sum", built, part)
    return built


def parallel(*parts):
    """Baut die parallele Zusammensetzung P | Q | ..."""
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
    """Baut den Aufruf A⟨args⟩."""
    return ("call", name, tuple(arguments))


def action_in(name):
    """Die Eingabeaktion a."""
    return ("in", name)


def action_out(name):
    """Die Ausgabeaktion a quer."""
    return ("out", name)


TAU = ("tau", None)


def complement(action):
    """Vertauscht Ein- und Ausgabe einer Aktion.

    Raises:
        ValueError: bei tau, das kein Gegenstück hat.
    """
    kind, name = action
    if kind == "tau":
        raise ValueError("tau hat kein Gegenstück")
    return ("out", name) if kind == "in" else ("in", name)


def action_name(action):
    """Nennt den Namen einer Aktion, oder None bei tau."""
    return action[1]


def show(process):
    """Schreibt einen Prozess in der Notation der Vorlesung."""
    kind = process[0]
    if kind == "nil":
        return "0"
    if kind == "prefix":
        head, action, rest = process
        mark = "" if action[0] == "in" else "'" if action[0] == "out" else ""
        text = "tau" if action[0] == "tau" else mark + action[1]
        return "%s.%s" % (text, show(rest))
    if kind == "sum":
        return "(%s + %s)" % (show(process[1]), show(process[2]))
    if kind == "par":
        return "(%s | %s)" % (show(process[1]), show(process[2]))
    if kind == "res":
        return "(new %s)%s" % (process[1], show(process[2]))
    return "%s<%s>" % (process[1], ",".join(process[2]))


def _substitute(process, mapping):
    """Ersetzt Namen in einem Prozess."""
    kind = process[0]
    if kind == "nil":
        return process
    if kind == "prefix":
        _, action, rest = process
        if action[0] == "tau":
            changed = action
        else:
            changed = (action[0], mapping.get(action[1], action[1]))
        return ("prefix", changed, _substitute(rest, mapping))
    if kind in ("sum", "par"):
        return (kind, _substitute(process[1], mapping),
                _substitute(process[2], mapping))
    if kind == "res":
        inner = {key: value for key, value in mapping.items()
                 if key != process[1]}
        return ("res", process[1], _substitute(process[2], inner))
    return ("call", process[1],
            tuple(mapping.get(name, name) for name in process[2]))


def simplify(process):
    """Entfernt den 0-Prozess aus parallelen Zusammensetzungen.

    Es gilt P | 0 ≡ P, und die Lösungsskizze der Übung nutzt das
    durchgehend. Ohne die Vereinfachung wachsen die Terme bei jedem
    Schritt um ein 0, und die Ketten werden unlesbar.
    """
    kind = process[0]
    if kind == "par":
        left = simplify(process[1])
        right = simplify(process[2])
        if left == NIL:
            return right
        if right == NIL:
            return left
        return ("par", left, right)
    if kind == "sum":
        return ("sum", simplify(process[1]), simplify(process[2]))
    if kind == "res":
        return ("res", process[1], simplify(process[2]))
    if kind == "prefix":
        return ("prefix", process[1], simplify(process[2]))
    return process


def transitions(process, definitions=None):
    """Nennt die Übergänge eines Prozesses nach den Regeln der Vorlesung.

    Die Regeln: ein Präfix bietet seine Aktion an; eine Auswahl bietet
    die Übergänge beider Seiten und verwirft dabei die nicht genommene;
    eine parallele Zusammensetzung bietet die Übergänge beider Seiten
    und zusätzlich die Reaktion zweier zueinander passender Aktionen als
    tau; eine Einschränkung lässt alles durch ausser dem eingeschränkten
    Namen; ein Aufruf wird durch seinen Rumpf mit eingesetzten
    Argumenten ersetzt.

    Args:
        process: der Prozess.
        definitions: Abbildung vom Namen auf Parameter und Rumpf.

    Returns:
        Liste von Paaren aus Aktion und Folgeprozess.

    Raises:
        ValueError: bei einem unbekannten Aufruf oder einer falschen
            Zahl von Argumenten.
    """
    definitions = definitions or {}
    kind = process[0]
    if kind == "nil":
        return []
    if kind == "prefix":
        return [(process[1], process[2])]
    if kind == "sum":
        return (transitions(process[1], definitions)
                + transitions(process[2], definitions))
    if kind == "par":
        left, right = process[1], process[2]
        found = [(action, ("par", other, right))
                 for action, other in transitions(left, definitions)]
        found += [(action, ("par", left, other))
                  for action, other in transitions(right, definitions)]
        for action, other in transitions(left, definitions):
            if action[0] == "tau":
                continue
            for second, rest in transitions(right, definitions):
                if second[0] == "tau":
                    continue
                if second == complement(action):
                    found.append((TAU, ("par", other, rest)))
        return found
    if kind == "res":
        name = process[1]
        return [(action, ("res", name, other))
                for action, other in transitions(process[2], definitions)
                if action_name(action) != name]
    if kind == "call":
        _, name, arguments = process
        if name not in definitions:
            raise ValueError("unbekannte Definition: %s" % name)
        parameters, body = definitions[name]
        if len(parameters) != len(arguments):
            raise ValueError("falsche Zahl von Argumenten für %s" % name)
        mapping = dict(zip(parameters, arguments))
        return transitions(_substitute(body, mapping), definitions)
    raise ValueError("unbekannter Prozess: %s" % kind)


def graph(process, definitions=None, limit=200):
    """Baut den Transitionsgraphen eines Prozesses.

    Die Knoten sind die erreichbaren Prozesse, die Kanten die Übergänge.
    Vereinfacht wird nach jedem Schritt, sonst wachsen die Terme durch
    stehenbleibende 0-Prozesse und derselbe Zustand erscheint mehrfach.

    Args:
        process: der Anfangsprozess.
        definitions: die Prozessdefinitionen.
        limit: obere Schranke der Knotenzahl.

    Returns:
        Abbildung mit ``states``, ``edges`` und dem Anfangszustand.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    start = simplify(process)
    seen = [start]
    known = {start}
    edges = []
    stack = [start]
    while stack:
        current = stack.pop()
        for action, other in transitions(current, definitions):
            following = simplify(other)
            edges.append((current, action, following))
            if following not in known:
                if len(known) >= limit:
                    raise ValueError("der Graph erreicht die Schranke")
                known.add(following)
                seen.append(following)
                stack.append(following)
    return {"states": seen, "edges": edges, "start": start,
            "state count": len(seen), "edge count": len(edges)}


def language(process, definitions=None, depth=6):
    """Sammelt die Folgen sichtbarer Aktionen bis zu einer Tiefe.

    Die Sprache eines Prozesses ist die Menge der Aktionsfolgen, die er
    ausführen kann. Sie ist gröber als der Transitionsgraph: zwei
    Prozesse mit derselben Sprache können sich verschieden verhalten,
    und genau daran hängt der Unterschied zwischen Sprachgleichheit und
    Bisimulation.

    Raises:
        ValueError: bei einer negativen Tiefe.
    """
    if depth < 0:
        raise ValueError("negative Tiefe")
    found = set()

    def walk(current, trace):
        """Verfolgt einen Pfad bis zur Tiefe."""
        found.add(trace)
        if len(trace) >= depth:
            return
        for action, other in transitions(current, definitions):
            mark = "tau" if action[0] == "tau" else (
                ("'" if action[0] == "out" else "") + action[1])
            walk(simplify(other), trace + (mark,))

    walk(simplify(process), ())
    return sorted(found)


def exercise_processes():
    """Die beiden Prozesse aus Aufgabe 1a des sechsten Übungsblattes.

    Der erste ist endlich, der zweite ruft sich selbst auf und hat
    deshalb einen Graphen mit Zyklen, aber immer noch endlich vielen
    Knoten.

    Returns:
        Abbildung mit beiden Prozessen und ihren Definitionen.
    """
    a, b, c = (action_in(name) for name in ("a", "b", "c"))
    d, e = action_in("d"), action_in("e")
    first = choice(prefix(a, prefix(b, NIL)),
                   prefix(c, parallel(prefix(d, NIL), prefix(e, NIL))))
    second = {"P": ((), choice(prefix(a, prefix(b, call("P"))),
                               prefix(c, choice(prefix(d, call("P")),
                                                prefix(e, call("P"))))))}
    return {"finite": {"process": first, "definitions": {}},
            "recursive": {"process": call("P"), "definitions": second}}


def infinite_example(depth=8):
    """Aufgabe 1c: ein Prozess mit unendlich vielen Knoten.

    ``P ≜ a.(P | b.0)`` legt bei jedem Schritt ein weiteres ``b.0``
    daneben. Der Graph wächst mit jedem a um einen Knoten und hört nie
    auf; hier wird er bis zu einer Tiefe aufgezählt, um das Wachstum zu
    zeigen.

    Returns:
        Abbildung mit der Knotenzahl je Tiefe.

    Raises:
        ValueError: bei einer nicht positiven Tiefe.
    """
    if depth < 1:
        raise ValueError("die Tiefe muss positiv sein")
    definitions = {"P": ((), prefix(action_in("a"),
                                    parallel(call("P"),
                                             prefix(action_in("b"),
                                                    NIL))))}
    counted = {}
    for bound in range(1, depth + 1):
        try:
            counted[bound] = graph(call("P"), definitions,
                                   limit=bound)["state count"]
        except ValueError:
            counted[bound] = bound
    return {"process": "P = a.(P | b.0)", "states up to a bound": counted,
            "grows": "mit jedem a kommt ein b.0 dazu",
            "finite": False}


def without_parallelism():
    """Aufgabe 1b: derselbe Graph ohne Parallelität.

    Gesucht ist ein Prozess ohne ``|``, der sich wie ``a.0 | b.0 | c.0``
    verhält. Die Summe über die sechs Reihenfolgen hat zwar dieselbe
    Sprache, aber nicht dasselbe Verhalten: sie legt die Reihenfolge
    schon vor der ersten Aktion fest. Richtig ist die geschachtelte
    Form, in der hinter jeder Aktion wieder die Auswahl über den Rest
    steht. Ob die beiden übereinstimmen, entscheidet die Bisimulation
    und nicht der Vergleich der Knotenzahlen.

    Returns:
        Abbildung mit beiden Prozessen und ihren Graphen.
    """
    actions = [action_in(name) for name in ("a", "b", "c")]
    concurrent = parallel(*[prefix(action, NIL) for action in actions])

    def build(rest):
        """Baut die geschachtelte Auswahl über die restlichen Aktionen."""
        if not rest:
            return NIL
        return choice(*[prefix(action, build(rest[:index]
                                             + rest[index + 1:]))
                        for index, action in enumerate(rest)])

    nested = build(actions)
    return {"concurrent": concurrent, "nested": nested,
            "concurrent states": graph(concurrent)["state count"],
            "nested states": graph(nested)["state count"],
            "note": "gleiche Knotenzahl ist weder nötig noch hinreichend; "
                    "das Urteil fällt in der Bisimulation"}
