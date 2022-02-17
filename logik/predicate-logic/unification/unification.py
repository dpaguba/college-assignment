"""Robinson's unification algorithm.

Two terms unify when some substitution makes them identical. The algorithm
walks them in parallel, and there are only three cases: identical symbols
recurse into the arguments, a variable binds to the other side, and anything
else fails.

The **occurs check** is the one line that is routinely left out. Unifying `x`
with `f(x)` has no finite solution, and skipping the check produces a cyclic
term that makes the prover loop or crash later. Prolog systems omit it for
speed and document that they are unsound as a result.

The unifier the algorithm returns is **most general**: every other unifier is
an instance of it. That is what makes resolution with unification complete
while resolution with arbitrary ground instances is only complete in the limit.
"""

from __future__ import annotations


def parse_term(text):
    """Parse a term written as `f(x, g(a))`."""
    state = {"text": text.replace(" ", ""), "position": 0}
    term = _term(state)
    if state["position"] != len(state["text"]):
        raise ValueError(f"unexpected character at {state['position']}")
    return term


def _term(state):
    """Parse one term."""
    start = state["position"]
    while (state["position"] < len(state["text"])
           and (state["text"][state["position"]].isalnum()
                or state["text"][state["position"]] == "_")):
        state["position"] += 1
    name = state["text"][start:state["position"]]

    if not state["text"].startswith("(", state["position"]):
        return name

    state["position"] += 1
    arguments = [_term(state)]
    while state["text"].startswith(",", state["position"]):
        state["position"] += 1
        arguments.append(_term(state))
    state["position"] += 1
    return (name, arguments)


def to_text(term):
    """Print a term."""
    if isinstance(term, tuple):
        return f"{term[0]}({','.join(to_text(argument) for argument in term[1])})"
    return term


def is_variable(term):
    """Whether a term is a variable.

    The convention here is the lecture's: a lower-case letter from the end of
    the alphabet, optionally followed by digits, is a variable, and everything
    else is a constant or a function symbol. The digits matter: resolution
    renames clauses apart by appending them, and a renamed variable that stops
    being recognised as one silently turns every unification into a failure.

    Prolog uses the opposite convention, capitals for variables, which is why
    the Prolog module states its own rule rather than reusing this one.
    """
    return (isinstance(term, str) and term[:1] in ("u", "v", "w", "x", "y", "z")
            and (len(term) == 1 or term[1:].isdigit()))


def occurs(variable, term):
    """Whether a variable occurs inside a term."""
    if isinstance(term, tuple):
        return any(occurs(variable, argument) for argument in term[1])
    return term == variable


def apply(substitution, term):
    """Apply a substitution to a term, repeatedly until it is stable."""
    if isinstance(term, str):
        term = parse_term(term) if "(" in term else term

    if isinstance(term, tuple):
        return (term[0], [apply(substitution, argument) for argument in term[1]])

    if term in substitution:
        replacement = substitution[term]
        if isinstance(replacement, str) and "(" in replacement:
            replacement = parse_term(replacement)
        return apply(substitution, replacement) if replacement != term else replacement

    return term


def unify(first, second):
    """The most general unifier of two terms, or `None`.

    Returned as a mapping from variable names to terms, printed in the same
    textual form the arguments were given in, so that a solution can be
    compared against a written one directly.
    """
    left = parse_term(first) if isinstance(first, str) else first
    right = parse_term(second) if isinstance(second, str) else second

    substitution = {}
    if not _unify(left, right, substitution):
        return None

    return {variable: to_text(term) for variable, term in substitution.items()}


def _unify(first, second, substitution):
    """The recursive step, updating the substitution in place."""
    first = _resolve(first, substitution)
    second = _resolve(second, substitution)

    if first == second:
        return True

    if is_variable(first):
        if occurs(first, second):
            return False
        substitution[first] = second
        return True

    if is_variable(second):
        return _unify(second, first, substitution)

    if isinstance(first, str) or isinstance(second, str):
        return False

    if first[0] != second[0] or len(first[1]) != len(second[1]):
        return False

    for left, right in zip(first[1], second[1]):
        if not _unify(left, right, substitution):
            return False

    return True


def _resolve(term, substitution):
    """Follow the substitution until the term is not a bound variable."""
    while is_variable(term) and term in substitution:
        term = substitution[term]
        if isinstance(term, str) and "(" in term:
            term = parse_term(term)
    return term


def compose(first, second):
    """Apply one substitution after another."""
    result = {variable: to_text(apply(second, term))
              for variable, term in first.items()}
    for variable, term in second.items():
        result.setdefault(variable, to_text(term) if not isinstance(term, str) else term)
    return result


def more_general(general, specific, term):
    """Whether one substitution is more general than another on a term.

    True when some further substitution turns the first result into the second.
    That is the property Robinson's algorithm guarantees, and it is what makes
    the unifier unique up to renaming.
    """
    left = apply(general, term)
    right = apply(specific, term)
    bridge = {}
    return _unify(left, right, bridge) and to_text(apply(bridge, left)) == to_text(right)
