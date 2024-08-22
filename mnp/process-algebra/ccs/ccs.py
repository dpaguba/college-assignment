"""CCS: syntax, operational semantics, and the three classical containers.

A process is a tree of nodes ``("nil",)``, ``("prefix", action, P)``,
``("choice", P, Q)``, ``("par", P, Q)``, ``("restrict", P, names)`` and
``("const", name)``. The action ``'a`` is the co-action of ``a``, and ``tau``
is the internal step that synchronisation produces.

The point of the operational semantics is that behaviour is derived, not
described: the transitions of a parallel composition follow from the
transitions of its parts by three rules, and everything else in this block
reads those transitions rather than the syntax.
"""

NIL = ("nil",)
TAU = "tau"


def complement(action):
    """The co-action: ``a`` becomes ``'a`` and back. ``tau`` is its own."""
    if action == TAU:
        return TAU
    return action[1:] if action.startswith("'") else "'" + action


def base_name(action):
    """The channel name with the co-action mark removed."""
    return action[1:] if action.startswith("'") else action


def parse(text):
    """Parse a CCS expression into a process tree."""
    return _parse_restriction(text.strip())


def _split_top(text, separator):
    """Split on a separator that appears at bracket depth zero."""
    depth, parts, current = 0, [], ""
    index = 0
    while index < len(text):
        symbol = text[index]
        if symbol == "(":
            depth += 1
        elif symbol == ")":
            depth -= 1
        if depth == 0 and text.startswith(separator, index):
            parts.append(current)
            current = ""
            index += len(separator)
            continue
        current += symbol
        index += 1
    parts.append(current)
    return parts


def _parse_restriction(text):
    """Parse the outermost level, where restriction binds loosest."""
    text = text.strip()
    parts = _split_top(text, "\\")
    if len(parts) > 1:
        process = _parse_parallel(parts[0])
        names = set()
        for piece in parts[1:]:
            names.update(name.strip() for name in
                         piece.strip().strip("{}").split(",") if name.strip())
        return ("restrict", process, frozenset(names))
    return _parse_parallel(text)


def _parse_parallel(text):
    """Parse parallel composition, which is right-associative here."""
    parts = _split_top(text, "|")
    if len(parts) > 1:
        result = _parse_choice(parts[-1])
        for piece in reversed(parts[:-1]):
            result = ("par", _parse_choice(piece), result)
        return result
    return _parse_choice(text)


def _parse_choice(text):
    """Parse choice, which binds tighter than composition."""
    parts = _split_top(text, "+")
    if len(parts) > 1:
        result = _parse_prefix(parts[-1])
        for piece in reversed(parts[:-1]):
            result = ("choice", _parse_prefix(piece), result)
        return result
    return _parse_prefix(text)


def _parse_prefix(text):
    """Parse action prefixes, constants, and bracketed subterms."""
    text = text.strip()
    if text.startswith("(") and _split_top(text, " ")[0].endswith(")") and \
            _matching(text) == len(text) - 1:
        return _parse_restriction(text[1:-1])
    parts = _split_top(text, ".")
    if len(parts) > 1:
        action = parts[0].strip()
        rest = ".".join(parts[1:])
        return ("prefix", action, _parse_prefix(rest))
    if text in ("0", "nil", ""):
        return NIL
    if text.startswith("(") and _matching(text) == len(text) - 1:
        return _parse_restriction(text[1:-1])
    return ("const", text)


def _matching(text):
    """The index of the bracket closing the one at position zero."""
    depth = 0
    for index, symbol in enumerate(text):
        if symbol == "(":
            depth += 1
        elif symbol == ")":
            depth -= 1
            if depth == 0:
                return index
    return -1


def to_text(process):
    """Print a process back as CCS syntax."""
    kind = process[0]
    if kind == "nil":
        return "0"
    if kind == "const":
        return process[1]
    if kind == "prefix":
        return "%s.%s" % (process[1], to_text(process[2]))
    if kind == "choice":
        return "%s + %s" % (to_text(process[1]), to_text(process[2]))
    if kind == "par":
        return "%s | %s" % (to_text(process[1]), to_text(process[2]))
    return "(%s) \\ %s" % (to_text(process[1]), ",".join(sorted(process[2])))


def transitions(process, environment=None):
    """The (action, successor) pairs derivable by the SOS rules.

    Parallel composition contributes three kinds of move: the left side acting
    alone, the right side acting alone, and a synchronisation on complementary
    actions that appears as ``tau``. Restriction then filters out whatever is
    left unsynchronised, which is how ``(a.0 | 'a.0) \\ a`` is forced to
    communicate instead of merely being able to.
    """
    environment = environment or {}
    kind = process[0]
    if kind in ("nil",):
        return []
    if kind == "const":
        body = environment.get(process[1])
        return transitions(body, environment) if body is not None else []
    if kind == "prefix":
        return [(process[1], process[2])]
    if kind == "choice":
        return (transitions(process[1], environment) +
                transitions(process[2], environment))
    if kind == "par":
        left, right = process[1], process[2]
        moves = [(action, ("par", following, right))
                 for action, following in transitions(left, environment)]
        moves += [(action, ("par", left, following))
                  for action, following in transitions(right, environment)]
        for action, after_left in transitions(left, environment):
            for other, after_right in transitions(right, environment):
                if other == complement(action) and action != TAU:
                    moves.append((TAU, ("par", after_left, after_right)))
        return moves
    names = process[2]
    return [(action, ("restrict", following, names))
            for action, following in transitions(process[1], environment)
            if action == TAU or base_name(action) not in names]


def actions(process, environment=None):
    """The actions available in the current state, without repetition."""
    seen, result = set(), []
    for action, _ in transitions(process, environment):
        if action not in seen:
            seen.add(action)
            result.append(action)
    return result


def step(process, action, environment=None):
    """Take one transition labelled by the action, or return ``None``."""
    for label, following in transitions(process, environment):
        if label == action:
            return following
    return None


def buffer(capacity):
    """A buffer of the given capacity, as constants ``B0`` to ``Bn``.

    Each state offers ``in`` while there is room and ``out`` while there is
    content, so capacity is visible in the behaviour rather than stored in a
    variable: the buffer of capacity three accepts exactly three ``in`` before
    it must emit.
    """
    environment = {}
    for level in range(capacity + 1):
        options = []
        if level < capacity:
            options.append(("prefix", "in", ("const", "B%d" % (level + 1))))
        if level > 0:
            options.append(("prefix", "out", ("const", "B%d" % (level - 1))))
        if len(options) == 2:
            body = ("choice", options[0], options[1])
        elif options:
            body = options[0]
        else:
            body = NIL
        environment["B%d" % level] = body
    return {"start": ("const", "B0"), "environment": environment}


def longest_trace(definition, limit):
    """Walk the definition greedily, preferring ``in`` over ``out``."""
    process = definition["start"]
    environment = definition["environment"]
    trace = []
    for _ in range(limit):
        available = actions(process, environment)
        if not available:
            break
        chosen = "in" if "in" in available else available[0]
        trace.append(chosen)
        process = step(process, chosen, environment)
    return trace


def max_consecutive(definition, action):
    """How often the action can be repeated from the initial state."""
    process = definition["start"]
    environment = definition["environment"]
    count = 0
    while action in actions(process, environment):
        process = step(process, action, environment)
        count += 1
    return count


def stack_behaviour(commands):
    """Run a sequence of ``pushN`` and ``pop`` under LIFO discipline."""
    return _container(commands, take_last=True)


def queue_behaviour(commands):
    """The same sequence under FIFO discipline.

    Stack and queue have the same alphabet and the same traces of actions.
    They differ only in which value comes back, which is why the course
    defines them in CCS by their observable outputs and not by their storage.
    """
    return _container(commands, take_last=False)


def _container(commands, take_last):
    """Run push and pop commands, taking from either end."""
    content, output = [], []
    for command in commands:
        if command.startswith("push"):
            content.append(command[len("push"):])
        elif command == "pop":
            if not content:
                raise ValueError("порожній контейнер")
            output.append(content.pop() if take_last else content.pop(0))
        else:
            raise ValueError("невідома команда: %s" % command)
    return output
