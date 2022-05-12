"""Puffer, Stapel und Schlange als CCS-Prozesse: Übungsblatt 5."""

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


def buffer_definitions(capacity):
    """Baut die Definitionen eines Puffers mit fester Kapazität.

    Aufgabe 1a: ein Puffer der Kapazität drei. Der Zustand ist die Zahl
    der gespeicherten Werte; bei jedem Zustand bietet der Prozess ``in``
    an, solange noch Platz ist, und ``out``, solange etwas darin liegt.

    Args:
        capacity: die Kapazität.

    Returns:
        Abbildung von ``Buff0``, ``Buff1`` und so fort auf ihre
        Definitionen.

    Raises:
        ValueError: bei einer nicht positiven Kapazität.
    """
    if capacity < 1:
        raise ValueError("die Kapazität muss positiv sein")
    definitions = {}
    for level in range(capacity + 1):
        parts = []
        if level < capacity:
            parts.append(prefix(action_in("in"),
                                call("Buff%d" % (level + 1))))
        if level > 0:
            parts.append(prefix(action_out("out"),
                                call("Buff%d" % (level - 1))))
        definitions["Buff%d" % level] = ((), choice(*parts) if parts
                                         else NIL)
    return definitions


def buffer_states(capacity):
    """Zählt die Zustände eines Puffers.

    Ein Puffer der Kapazität n hat n plus einen Zustand: leer, ein Wert,
    bis voll. Das ist der Grund, warum ein Puffer sich in CCS ohne
    Datentypen beschreiben lässt: gespeichert wird nur, wie viel darin
    ist, nicht was.

    Raises:
        ValueError: bei einer nicht positiven Kapazität.
    """
    return len(buffer_definitions(capacity))


def unordered_buffer_definitions():
    """Aufgabe 1b: ein Puffer der Kapazität zwei ohne feste Reihenfolge.

    Der geordnete Puffer gibt die Werte in der Reihenfolge heraus, in der
    sie hineinkamen. Soll die Reihenfolge beliebig sein, muss der
    Prozess unterscheiden, welche Werte er hält, und nicht nur wie
    viele. Mit zwei unterscheidbaren Werten sind das die Zustände leer,
    nur der erste, nur der zweite, und beide, und im letzten Zustand
    bietet er beide Ausgaben an.

    Returns:
        Die Definitionen.
    """
    return {
        "U": ((), choice(prefix(action_in("in1"), call("U1")),
                         prefix(action_in("in2"), call("U2")))),
        "U1": ((), choice(prefix(action_in("in2"), call("U12")),
                          prefix(action_out("out1"), call("U")))),
        "U2": ((), choice(prefix(action_in("in1"), call("U12")),
                          prefix(action_out("out2"), call("U")))),
        "U12": ((), choice(prefix(action_out("out1"), call("U2")),
                           prefix(action_out("out2"), call("U1")))),
    }


def stack_definitions(depth=3):
    """Aufgabe 2a: ein Stapel über den Werten null und eins.

    Der Zustand ist der Inhalt als Zeichenkette, das oberste Element
    vorn. Der Prozess bietet ``push0`` und ``push1`` an, solange die
    Schranke nicht erreicht ist, ``pop`` für das oberste Element, und im
    leeren Zustand die Aktion ``empty``.

    Args:
        depth: die betrachtete Tiefe; ein echter Stapel ist unbegrenzt
            und hätte unendlich viele Zustände.

    Returns:
        Abbildung von den Zuständen auf ihre Definitionen.

    Raises:
        ValueError: bei einer negativen Tiefe.
    """
    if depth < 0:
        raise ValueError("negative Tiefe")
    definitions = {}
    contents = [""]
    for _ in range(depth):
        contents += [value + digit for value in contents
                     for digit in "01" if len(value) + 1 <= depth]
    for content in sorted(set(contents)):
        parts = []
        if len(content) < depth:
            for digit in "01":
                parts.append(prefix(action_in("push" + digit),
                                    call("S_" + digit + content)))
        if content:
            parts.append(prefix(action_out("pop" + content[0]),
                                call("S_" + content[1:])))
        else:
            parts.append(prefix(action_out("empty"), call("S_")))
        definitions["S_" + content] = ((), choice(*parts))
    return definitions


def queue_definitions(depth=3):
    """Aufgabe 2b: dieselben Aktionen, aber als Schlange.

    Der einzige Unterschied steht in einer Zeile: der Stapel gibt das
    vorderste Element heraus, die Schlange das hinterste. Alles andere
    bleibt gleich, und genau daran lässt sich zeigen, dass die beiden
    Prozesse verschieden sind, obwohl sie dieselben Aktionen anbieten.

    Raises:
        ValueError: bei einer negativen Tiefe.
    """
    if depth < 0:
        raise ValueError("negative Tiefe")
    definitions = stack_definitions(depth)
    changed = {}
    for name, (parameters, body) in definitions.items():
        content = name[2:]
        parts = []
        if len(content) < depth:
            for digit in "01":
                parts.append(prefix(action_in("push" + digit),
                                    call("Q_" + digit + content)))
        if content:
            parts.append(prefix(action_out("pop" + content[-1]),
                                call("Q_" + content[:-1])))
        else:
            parts.append(prefix(action_out("empty"), call("Q_")))
        changed["Q_" + content] = (parameters, choice(*parts))
    return changed


def what_comes_out_first(order="01", depth=3):
    """Vergleicht Stapel und Schlange an derselben Eingabefolge.

    Nach ``push0`` und dann ``push1`` gibt der Stapel die Eins heraus und
    die Schlange die Null. Das ist der ganze Unterschied, und er ist an
    den angebotenen Aktionen abzulesen.

    Args:
        order: die Folge der eingefügten Werte.
        depth: die betrachtete Tiefe.

    Returns:
        Abbildung mit den beiden Ausgaben.

    Raises:
        ValueError: bei einer zu langen Folge.
    """
    if len(order) > depth:
        raise ValueError("die Folge passt nicht in die Tiefe")
    stack = stack_definitions(depth)
    queue = queue_definitions(depth)
    content = ""
    for digit in order:
        content = digit + content
    stack_pops = [action_name(action) for action, _
                  in transitions(call("S_" + content), stack)
                  if action[0] == "out"]
    queue_pops = [action_name(action) for action, _
                  in transitions(call("Q_" + content), queue)
                  if action[0] == "out"]
    return {"pushed": order, "stack offers": stack_pops,
            "queue offers": queue_pops,
            "differ": stack_pops != queue_pops}


def why_the_value_has_to_be_in_the_state():
    """Sagt, warum der ungeordnete Puffer mehr Zustände braucht.

    CCS kennt keine Daten. Ein Prozess merkt sich nur, welcher Prozess er
    geworden ist, und deshalb muss alles, woran er sich erinnern soll, in
    den Zustandsnamen. Beim geordneten Puffer genügt die Zahl der Werte,
    beim ungeordneten braucht es die Menge, und beim Stapel die ganze
    Folge. Die Zustandszahl wächst entsprechend: n plus eins, zwei hoch
    n, und zwei hoch n plus eins minus eins.
    """
    return {"ordered buffer": "die Anzahl genügt",
            "unordered buffer": "die Menge der gehaltenen Werte",
            "stack": "die ganze Folge",
            "states": {"buffer of 3": buffer_states(3),
                       "unordered of 2": len(unordered_buffer_definitions()),
                       "stack of depth 3": len(stack_definitions(3))},
            "reason": "CCS kennt keine Daten, alles Gemerkte steckt im "
                      "Zustand"}
