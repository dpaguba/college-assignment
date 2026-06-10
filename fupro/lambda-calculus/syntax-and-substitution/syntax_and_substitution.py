"""Lambda terms, free variables, and capture-avoiding substitution.

Three forms and nothing else: a variable, an abstraction, an application. All
the difficulty is in substitution, where replacing a free variable by a term
must not let a free variable of that term fall under a binder that happens to
carry the same name. Renaming the binder is the fix, and it is why terms that
differ only in the names of bound variables have to count as equal.
"""

import itertools

_COUNTER = itertools.count()


def variable(name):
    """A variable term."""
    return ("var", name)


def abstraction(name, body):
    """A lambda abstraction binding the name in the body."""
    return ("lam", name, body)


def application(function, argument):
    """An application of one term to another."""
    return ("app", function, argument)


def parse(text):
    """Parses a term written with a backslash for the lambda."""
    position = [0]
    term = _parse_term(text, position)
    _skip(text, position)
    if position[0] != len(text):
        raise ValueError("unexpected text at %d: %r" % (position[0], text))
    return term


def _skip(text, position):
    """Advances past whitespace."""
    while position[0] < len(text) and text[position[0]].isspace():
        position[0] += 1


def _parse_term(text, position):
    """Parses an abstraction, an application chain, or an atom."""
    _skip(text, position)
    if position[0] < len(text) and text[position[0]] == "\\":
        position[0] += 1
        _skip(text, position)
        start = position[0]
        while position[0] < len(text) and (text[position[0]].isalnum()
                                           or text[position[0]] == "_"):
            position[0] += 1
        name = text[start:position[0]]
        _skip(text, position)
        if position[0] >= len(text) or text[position[0]] != ".":
            raise ValueError("expected a dot after the binder")
        position[0] += 1
        return abstraction(name, _parse_term(text, position))
    result = _parse_atom(text, position)
    while True:
        save = position[0]
        _skip(text, position)
        if position[0] >= len(text) or text[position[0]] in ").":
            position[0] = save
            return result
        try:
            argument = _parse_atom(text, position)
        except ValueError:
            position[0] = save
            return result
        result = application(result, argument)


def _parse_atom(text, position):
    """Parses a variable or a bracketed term."""
    _skip(text, position)
    if position[0] >= len(text):
        raise ValueError("unexpected end of term")
    if text[position[0]] == "(":
        position[0] += 1
        inner = _parse_term(text, position)
        _skip(text, position)
        if position[0] >= len(text) or text[position[0]] != ")":
            raise ValueError("unclosed bracket")
        position[0] += 1
        return inner
    if text[position[0]] == "\\":
        return _parse_term(text, position)
    start = position[0]
    while position[0] < len(text) and (text[position[0]].isalnum()
                                       or text[position[0]] in "_'"):
        position[0] += 1
    if start == position[0]:
        raise ValueError("expected a variable at %d" % position[0])
    return variable(text[start:position[0]])


def to_text(term):
    """Prints a term so that parsing it again gives the same tree.

    An abstraction inside an application has to be bracketed, since the body
    of a lambda otherwise extends as far to the right as it can and would
    swallow the argument.
    """
    kind = term[0]
    if kind == "var":
        return term[1]
    if kind == "lam":
        return "\\%s.%s" % (term[1], to_text(term[2]))
    return "(%s %s)" % (_bracketed(term[1]), _bracketed(term[2]))


def _bracketed(term):
    """The text of a term, bracketed when it is an abstraction."""
    text = to_text(term)
    return "(%s)" % text if term[0] == "lam" else text


def free_variables(term):
    """The variables that are not bound by any enclosing abstraction."""
    kind = term[0]
    if kind == "var":
        return {term[1]}
    if kind == "lam":
        return free_variables(term[2]) - {term[1]}
    return free_variables(term[1]) | free_variables(term[2])


def bound_variables(term):
    """The names that occur as binders."""
    kind = term[0]
    if kind == "var":
        return set()
    if kind == "lam":
        return {term[1]} | bound_variables(term[2])
    return bound_variables(term[1]) | bound_variables(term[2])


def fresh(name):
    """A variable name that has not been used before."""
    return "%s%d" % (name.rstrip("0123456789"), next(_COUNTER))


def substitute(term, name, replacement):
    """Replaces the free occurrences of a variable, renaming binders as needed.

    The renaming is the whole point. Substituting ``y`` for ``x`` in
    ``\\y.(x y)`` without renaming would produce ``\\y.(y y)``, in which the
    substituted variable has become bound and means something else.
    """
    kind = term[0]
    if kind == "var":
        return replacement if term[1] == name else term
    if kind == "app":
        return application(substitute(term[1], name, replacement),
                           substitute(term[2], name, replacement))
    if term[1] == name:
        return term
    if term[1] in free_variables(replacement):
        renamed = fresh(term[1])
        body = substitute(term[2], term[1], variable(renamed))
        return abstraction(renamed, substitute(body, name, replacement))
    return abstraction(term[1], substitute(term[2], name, replacement))


def alpha_equal(first, second, mapping=None):
    """Whether two terms differ only in the names of their bound variables."""
    mapping = mapping or {}
    if first[0] != second[0]:
        return False
    if first[0] == "var":
        return mapping.get(first[1], first[1]) == second[1]
    if first[0] == "lam":
        return alpha_equal(first[2], second[2],
                           dict(mapping, **{first[1]: second[1]}))
    return (alpha_equal(first[1], second[1], mapping)
            and alpha_equal(first[2], second[2], mapping))


def size(term):
    """How many nodes the term has."""
    if term[0] == "var":
        return 1
    if term[0] == "lam":
        return 1 + size(term[2])
    return 1 + size(term[1]) + size(term[2])
