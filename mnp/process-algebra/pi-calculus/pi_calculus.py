"""The pi-calculus: name passing, restriction, scope extrusion, encodings.

CCS fixes the communication topology at the time the process is written. The
pi-calculus sends names over channels, so a received name becomes a channel
the receiver can use, and the topology changes as the system runs. That single
change is what lets the calculus model mobility, and it is why the encodings
of booleans and lists below need no data types at all.

A process is ``("nil",)``, ``("send", channel, name, P)``, ``("receive",
channel, variable, P)``, ``("par", P, Q)`` or ``("new", name, P)``.
"""

NIL = ("nil",)


def parse(text):
    """Parse the subset of pi-calculus syntax used here."""
    return _parse_parallel(text.strip())


def _split_top(text, separator):
    """Split on a separator that appears at bracket depth zero."""
    depth, parts, current = 0, [], ""
    for symbol in text:
        if symbol == "(":
            depth += 1
        elif symbol == ")":
            depth -= 1
        if symbol == separator and depth == 0:
            parts.append(current)
            current = ""
            continue
        current += symbol
    parts.append(current)
    return parts


def _parse_parallel(text):
    """Parse parallel composition."""
    parts = _split_top(text, "|")
    if len(parts) > 1:
        result = _parse_atom(parts[-1])
        for piece in reversed(parts[:-1]):
            result = ("par", _parse_atom(piece), result)
        return result
    return _parse_atom(text)


def _parse_atom(text):
    """Parse a restriction, a send, a receive, or the inert process."""
    text = text.strip()
    if text.startswith("(new "):
        closing = text.index(")")
        name = text[len("(new "):closing].strip()
        return ("new", name, _parse_parallel(text[closing + 1:]))
    if text.startswith("(") and text.endswith(")") and _balanced(text[1:-1]):
        return _parse_parallel(text[1:-1])
    if text in ("0", ""):
        return NIL
    opening = text.find("(")
    opening = len(text) if opening < 0 else opening
    if "<" in text and text.index("<") < opening:
        channel = text[:text.index("<")].strip()
        payload = text[text.index("<") + 1:text.index(">")].strip()
        rest = text[text.index(">") + 1:].lstrip(".")
        return ("send", channel, payload, _parse_atom(rest))
    if "(" in text:
        channel = text[:text.index("(")].strip()
        variable = text[text.index("(") + 1:text.index(")")].strip()
        rest = text[text.index(")") + 1:].lstrip(".")
        return ("receive", channel, variable, _parse_atom(rest))
    return NIL


def _balanced(text):
    """Whether the brackets in the text are balanced."""
    depth = 0
    for symbol in text:
        if symbol == "(":
            depth += 1
        elif symbol == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def to_text(process):
    """Print a process back as text."""
    kind = process[0]
    if kind == "nil":
        return "0"
    if kind == "send":
        return "%s<%s>.%s" % (process[1], process[2], to_text(process[3]))
    if kind == "receive":
        return "%s(%s).%s" % (process[1], process[2], to_text(process[3]))
    if kind == "par":
        return "%s | %s" % (to_text(process[1]), to_text(process[2]))
    return "(new %s) %s" % (process[1], to_text(process[2]))


def substitute(process, variable, name):
    """Substitute a name for the free occurrences of a variable."""
    kind = process[0]
    if kind == "nil":
        return process
    if kind == "send":
        channel = name if process[1] == variable else process[1]
        payload = name if process[2] == variable else process[2]
        return ("send", channel, payload, substitute(process[3], variable, name))
    if kind == "receive":
        channel = name if process[1] == variable else process[1]
        if process[2] == variable:
            return ("receive", channel, process[2], process[3])
        return ("receive", channel, process[2],
                substitute(process[3], variable, name))
    if kind == "par":
        return ("par", substitute(process[1], variable, name),
                substitute(process[2], variable, name))
    if process[1] == variable:
        return process
    return ("new", process[1], substitute(process[2], variable, name))


def _components(process):
    """Flatten a parallel composition into its components."""
    if process[0] == "par":
        return _components(process[1]) + _components(process[2])
    return [process]


def _rebuild(parts):
    """Rebuild a composition from components, dropping inert ones."""
    parts = [part for part in parts if part[0] != "nil"] or [NIL]
    result = parts[-1]
    for part in reversed(parts[:-1]):
        result = ("par", part, result)
    return result


def step(process):
    """Perform one communication by the COMM rule, or return ``None``."""
    if process[0] == "new":
        inner = step(process[2])
        return ("new", process[1], inner) if inner else None
    parts = _components(process)
    for sender in range(len(parts)):
        if parts[sender][0] != "send":
            continue
        for receiver in range(len(parts)):
            if receiver == sender or parts[receiver][0] != "receive":
                continue
            if parts[sender][1] != parts[receiver][1]:
                continue
            payload = parts[sender][2]
            rest = list(parts)
            rest[sender] = parts[sender][3]
            rest[receiver] = substitute(parts[receiver][3],
                                        parts[receiver][2], payload)
            return _rebuild(rest)
    return None


def channels(process):
    """The names that occur in channel position."""
    kind = process[0]
    if kind == "nil":
        return set()
    if kind in ("send", "receive"):
        return {process[1]} | channels(process[3])
    if kind == "par":
        return channels(process[1]) | channels(process[2])
    return channels(process[2])


def is_bound(process, name):
    """Whether a name is bound by a ``new`` restriction."""
    kind = process[0]
    if kind == "new":
        return process[1] == name or is_bound(process[2], name)
    if kind == "par":
        return is_bound(process[1], name) or is_bound(process[2], name)
    if kind in ("send", "receive"):
        return is_bound(process[3], name)
    return False


def extrude(process):
    """Whether a private name escapes the scope that restricts it.

    Sending a restricted name widens its scope to cover the receiver, which
    keeps the name private to the two parties rather than public. Scope
    extrusion is how a fresh channel is handed to a partner without any third
    process gaining access to it.
    """
    private = []

    def collect(node):
        """Gather the names bound by restrictions anywhere in the term."""
        if node[0] == "new":
            private.append(node[1])
            collect(node[2])
        elif node[0] == "par":
            collect(node[1])
            collect(node[2])
        elif node[0] in ("send", "receive"):
            collect(node[3])

    collect(process)
    sent = set()

    def outputs(node):
        """Gather the names that appear as the payload of a send."""
        if node[0] == "send":
            sent.add(node[2])
            outputs(node[3])
        elif node[0] == "receive":
            outputs(node[3])
        elif node[0] == "par":
            outputs(node[1])
            outputs(node[2])
        elif node[0] == "new":
            outputs(node[2])

    outputs(process)
    escaping = sorted(set(private) & sent)
    return {"extruded": bool(escaping), "names": escaping}


TRUE = "(new t) (new f) r<t>.0"
FALSE = "(new t) (new f) r<f>.0"


def encode_boolean(value):
    """Encode a boolean as a process that signals on one of two channels."""
    return TRUE if value else FALSE


def evaluate_and(left, right):
    """Conjunction under that encoding: consult the second only if the first holds."""
    return right if left else False


def evaluate_not(value):
    """Negation, which swaps the two channels in the continuation."""
    return not value


def encode_list(items, result_channel):
    """Encode a list as nested outputs ending in an empty-list signal."""
    encoded = "nil<%s>.0" % result_channel
    for item in reversed(items):
        encoded = "cons<%s>.(%s)" % (item, encoded)
    return encoded


def decode_list(encoded):
    """Read the elements back out of the encoding."""
    items, rest = [], encoded
    while rest.startswith("cons<"):
        closing = rest.index(">")
        items.append(rest[len("cons<"):closing])
        rest = rest[closing + 1:].lstrip(".").lstrip("(")
    return items
