"""Die operationale Semantik von CCS und die tau-Ketten der Übung."""

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


def tau_transitions(process, definitions=None):
    """Nennt nur die tau-Übergänge eines Prozesses."""
    return [(action, other)
            for action, other in transitions(process, definitions)
            if action[0] == "tau"]


def tau_chain(process, definitions=None, limit=20):
    """Führt tau-Übergänge aus, bis keiner mehr möglich ist.

    Bei mehreren möglichen Übergängen wird der erste genommen; die
    Aufgabe verlangt eine Kette, nicht alle Ketten. Der Endzustand kann
    von der Wahl abhängen, und genau das ist bei Aufgabe 1c der Fall.

    Args:
        process: der Anfangsprozess.
        definitions: die Prozessdefinitionen.
        limit: obere Schranke gegen eine unendliche Kette.

    Returns:
        Liste der Prozesse, beginnend beim Anfang.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    chain = [simplify(process)]
    for _ in range(limit):
        steps = tau_transitions(chain[-1], definitions)
        if not steps:
            return chain
        chain.append(simplify(steps[0][1]))
    raise ValueError("die Kette erreicht die Schranke")


def all_tau_endpoints(process, definitions=None, limit=200):
    """Sammelt alle Prozesse, bei denen keine tau-Reaktion mehr geht.

    Anders als ``tau_chain`` verfolgt diese Funktion jede Wahl. Damit
    lässt sich zeigen, dass der Endzustand bei einer Auswahl nicht
    eindeutig ist.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    seen = set()
    ends = set()
    stack = [simplify(process)]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        if len(seen) > limit:
            raise ValueError("die Suche erreicht die Schranke")
        steps = tau_transitions(current, definitions)
        if not steps:
            ends.add(current)
            continue
        for _, other in steps:
            stack.append(simplify(other))
    return sorted(ends, key=show)


def exercise_terms():
    """Die fünf Terme aus Aufgabe 1a des vierten Übungsblattes.

    Die Überstriche des Blattes gehen beim Auslesen des PDF verloren;
    aus der Lösungsskizze geht hervor, welche Aktionen gestrichen sind,
    und so stehen sie hier.

    Returns:
        Abbildung vom Buchstaben der Aufgabe auf Prozess und
        Definitionen.
    """
    a_in, b_in, c_in = (action_in(name) for name in ("a", "b", "c"))
    a_out, b_out, c_out = (action_out(name) for name in ("a", "b", "c"))
    recursive = {"A": (("a1",), prefix(action_in("a1"),
                                       call("A", "a1")))}
    return {
        "a": {"process": parallel(prefix(a_in, prefix(b_in, NIL)),
                                  prefix(a_out, NIL)),
              "definitions": {}},
        "b": {"process": parallel(prefix(a_in, NIL), prefix(b_out, NIL),
                                  prefix(b_in, prefix(a_out, NIL))),
              "definitions": {}},
        "c": {"process": parallel(
            choice(prefix(a_in, prefix(b_in, NIL)),
                   prefix(b_in, prefix(a_out, NIL))),
            prefix(a_out, prefix(a_in, NIL))),
              "definitions": {}},
        "d": {"process": parallel(
            call("A", "a"), call("A", "b"),
            prefix(a_out, prefix(b_out, prefix(b_out,
                                               prefix(a_out, NIL))))),
              "definitions": recursive},
        "e": {"process": parallel(
            choice(restrict("a", prefix(a_in, prefix(b_in, NIL))),
                   prefix(c_in, NIL)),
            choice(prefix(a_out, NIL), prefix(b_out, NIL),
                   prefix(c_out, NIL))),
              "definitions": {}},
    }


def solved_exercise():
    """Rechnet die fünf Terme durch und schreibt die Ketten auf.

    Returns:
        Abbildung vom Buchstaben auf die Kette als Text.
    """
    solved = {}
    for letter, row in exercise_terms().items():
        chain = tau_chain(row["process"], row["definitions"])
        solved[letter] = [show(step) for step in chain]
    return solved


def why_the_restriction_blocks_the_reaction():
    """Erklärt den fünften Term.

    Der ν-Operator bindet den Namen a im linken Summanden. Eine Aktion
    mit diesem Namen ist damit nach aussen nicht sichtbar und kann mit
    dem a der rechten Seite nicht reagieren; sie könnte nur mit einer
    Aktion innerhalb der Einschränkung reagieren, und dort steht keine.
    Es bleibt die Reaktion von c mit c quer, und danach sind beide
    Seiten der 0-Prozess.
    """
    return {"binds": "a im linken Summanden",
            "consequence": "a links und a quer rechts reagieren nicht",
            "what remains": "c mit c quer",
            "result": "0",
            "general point": "die Einschränkung modelliert einen Namen, "
                             "den zwei Prozesse gleich nennen und "
                             "trotzdem nicht teilen"}
