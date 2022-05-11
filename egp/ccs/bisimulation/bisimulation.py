"""Starke Bisimulation und der Unterschied zur Sprachgleichheit."""

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


def _states(process, definitions, limit=400):
    """Sammelt die erreichbaren Prozesse mit ihren Übergängen.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    start = simplify(process)
    known = {start}
    steps = {}
    stack = [start]
    while stack:
        current = stack.pop()
        found = []
        for action, other in transitions(current, definitions):
            following = simplify(other)
            found.append((action, following))
            if following not in known:
                if len(known) >= limit:
                    raise ValueError("die Suche erreicht die Schranke")
                known.add(following)
                stack.append(following)
        steps[current] = found
    return start, steps


def bisimilar(first, second, definitions=None, limit=400):
    """Prüft, ob zwei Prozesse stark bisimular sind.

    Gerechnet wird durch Verfeinerung: alle Zustände beginnen in einer
    Klasse, und solange zwei Zustände derselben Klasse verschiedene
    Klassen erreichen können, werden sie getrennt. Am Ende sind zwei
    Prozesse bisimular, wenn sie in derselben Klasse liegen.

    Args:
        first: der erste Prozess.
        second: der zweite.
        definitions: die Prozessdefinitionen.
        limit: obere Schranke der Zustandszahl.

    Returns:
        Abbildung mit dem Urteil und der Zahl der Klassen.

    Raises:
        ValueError: wenn die Schranke erreicht wird.
    """
    start_first, steps_first = _states(first, definitions, limit)
    start_second, steps_second = _states(second, definitions, limit)
    steps = dict(steps_first)
    steps.update(steps_second)
    classes = {state: 0 for state in steps}
    while True:
        signature = {}
        for state, found in steps.items():
            key = (frozenset((action, classes[other])
                             for action, other in found),)
            signature[state] = key
        fresh = {}
        changed = {}
        for state in steps:
            key = (classes[state], signature[state])
            if key not in fresh:
                fresh[key] = len(fresh)
            changed[state] = fresh[key]
        if changed == classes:
            break
        classes = changed
    return {"bisimilar": classes[start_first] == classes[start_second],
            "classes": len(set(classes.values())),
            "states": len(steps)}


def traces(process, definitions=None, depth=6):
    """Sammelt die Folgen von Aktionen bis zu einer Tiefe.

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
            walk(simplify(other), trace + (action,))

    walk(simplify(process), ())
    return found


def the_classic_counterexample():
    """Zeigt zwei Prozesse mit derselben Sprache und anderem Verhalten.

    ``a.(b.0 + c.0)`` und ``a.b.0 + a.c.0`` führen dieselben Folgen aus:
    a, dann b oder c. Sie sind trotzdem verschieden. Der erste
    entscheidet sich nach dem a, der zweite vorher; wer mit dem zweiten
    a gemacht hat und dann b will, kann Pech gehabt haben.

    Das ist der Grund, warum die Sprache als Gleichheitsbegriff nicht
    ausreicht, und der ganze Anlass für die Bisimulation.

    Returns:
        Abbildung mit beiden Urteilen.
    """
    a, b, c = (action_in(name) for name in ("a", "b", "c"))
    first = prefix(a, choice(prefix(b, NIL), prefix(c, NIL)))
    second = choice(prefix(a, prefix(b, NIL)), prefix(a, prefix(c, NIL)))
    return {"same traces": traces(first) == traces(second),
            "bisimilar": bisimilar(first, second)["bisimilar"],
            "why": "der zweite entscheidet sich vor dem a, der erste "
                   "danach"}


def expand(actions):
    """Baut die sequentielle Entsprechung einer parallelen Zusammensetzung.

    Der Expansionssatz: eine parallele Zusammensetzung von Präfixen ist
    gleich der Summe über die möglichen ersten Aktionen, wobei hinter
    jeder Aktion wieder die Expansion des Restes steht. Die Verzweigung
    ist also geschachtelt und nicht flach.

    Args:
        actions: die Aktionen der parallel laufenden Präfixe.

    Returns:
        Der sequentielle Prozess.
    """
    if not actions:
        return NIL
    parts = []
    for index, action in enumerate(actions):
        rest = actions[:index] + actions[index + 1:]
        parts.append(prefix(action, expand(rest)))
    return choice(*parts)


def flat_orders(actions):
    """Baut die flache Summe über alle Reihenfolgen.

    Das ist die Antwort, die sich zuerst anbietet: jede Reihenfolge als
    eine Kette, alle Ketten mit + verbunden. Sie hat dieselbe Sprache
    wie die parallele Zusammensetzung und ist trotzdem ein anderer
    Prozess.
    """
    if not actions:
        return NIL
    chains = []

    def build(rest, chain):
        """Sammelt eine Reihenfolge als Kette von Präfixen."""
        if not rest:
            process = NIL
            for action in reversed(chain):
                process = prefix(action, process)
            chains.append(process)
            return
        for index, action in enumerate(rest):
            build(rest[:index] + rest[index + 1:], chain + [action])

    build(list(actions), [])
    return choice(*chains)


def expansion_law():
    """Prüft Aufgabe 1b des sechsten Blattes durch Bisimulation.

    Gesucht war ein Prozess ohne Parallelität mit demselben Verhalten wie
    ``a.0 | b.0 | c.0``. Die naheliegende Antwort ist die Summe über die
    sechs Reihenfolgen, und sie ist falsch. Nach dem ersten a bietet die
    parallele Zusammensetzung b und c an; die flache Summe hat sich zu
    diesem Zeitpunkt schon entschieden und bietet nur noch eines von
    beiden. Es ist derselbe Fehler wie bei ``a.b.0 + a.c.0`` gegen
    ``a.(b.0 + c.0)``, nur grösser.

    Richtig ist die geschachtelte Form: hinter jeder Aktion steht wieder
    die Auswahl über den Rest, also

    a.(b.c.0 + c.b.0) + b.(a.c.0 + c.a.0) + c.(a.b.0 + b.a.0).

    Returns:
        Abbildung mit beiden Urteilen und den Sprachen.
    """
    actions = [action_in(name) for name in ("a", "b", "c")]
    concurrent = parallel(*[prefix(action, NIL) for action in actions])
    nested = expand(actions)
    flat = flat_orders(actions)
    return {"nested is bisimilar": bisimilar(concurrent,
                                             nested)["bisimilar"],
            "flat is bisimilar": bisimilar(concurrent, flat)["bisimilar"],
            "flat has the same traces": traces(concurrent) == traces(flat),
            "nested": show(nested),
            "why the flat sum fails": "sie entscheidet sich vor der "
                                      "ersten Aktion, die parallele "
                                      "Zusammensetzung danach"}


def a_process_is_bisimilar_to_itself():
    """Prüft die Grundeigenschaften an Beispielen.

    Returns:
        Abbildung mit Reflexivität und einem Gegenbeispiel.
    """
    a, b = action_in("a"), action_in("b")
    same = prefix(a, prefix(b, NIL))
    other = prefix(a, NIL)
    return {"reflexive": bisimilar(same, same)["bisimilar"],
            "different": bisimilar(same, other)["bisimilar"],
            "nil against nil": bisimilar(NIL, NIL)["bisimilar"]}
