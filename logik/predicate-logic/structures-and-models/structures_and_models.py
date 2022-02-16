"""First-order structures, and what it means for a formula to hold in one.

A propositional formula is evaluated against an assignment of truth values. A
first-order formula is evaluated against a **structure**: a domain, a relation
for each relation symbol, a function for each function symbol, and an element
for each constant. Free variables additionally need an assignment.

The definition is compositional and short, and every subtlety is in the
quantifier cases: `forall x phi` holds when `phi` holds for every element of
the domain substituted for `x`. The domain is therefore part of the question,
not part of the logic, which is why the same formula can hold in one structure
and fail in another of the same signature.
"""

from __future__ import annotations


class Structure:
    """A domain, relations, functions and constants over it."""

    def __init__(self, domain, relations, functions=None, constants=None):
        """Store the interpretation of every symbol of the signature."""
        self.domain = list(domain)
        self.relations = {name: set(tuples) for name, tuples in relations.items()}
        self.functions = dict(functions or {})
        self.constants = dict(constants or {})

    def value(self, term, assignment):
        """The element a term denotes.

        A name is a constant if the structure interprets it, otherwise it is a
        variable and must be in the assignment. Getting a `KeyError` here is the
        right behaviour for a free variable with no assignment: the formula does
        not have a truth value, and pretending otherwise hides the mistake.
        """
        if isinstance(term, tuple):
            name, arguments = term
            values = [self.value(argument, assignment) for argument in arguments]
            return self.functions[name](*values)

        if term in self.constants:
            return self.constants[term]
        return assignment[term]

    def holds(self, formula, assignment):
        """Whether a formula holds in this structure under an assignment."""
        kind = formula[0]

        if kind == "atom":
            name, arguments = formula[1], formula[2]
            values = tuple(self.value(argument, assignment) for argument in arguments)
            if name == "Eq":
                return values[0] == values[1]
            return values in self.relations.get(name, set())

        if kind == "!":
            return not self.holds(formula[1], assignment)

        if kind == "forall":
            variable, body = formula[1], formula[2]
            return all(self.holds(body, dict(assignment, **{variable: element}))
                       for element in self.domain)

        if kind == "exists":
            variable, body = formula[1], formula[2]
            return any(self.holds(body, dict(assignment, **{variable: element}))
                       for element in self.domain)

        left = self.holds(formula[1], assignment)
        right = self.holds(formula[2], assignment)

        if kind == "&":
            return left and right
        if kind == "|":
            return left or right
        if kind == "->":
            return (not left) or right
        return left == right

    def models(self, formula):
        """Whether a sentence holds with the empty assignment."""
        return self.holds(formula, {})


def parse(text):
    """Parse a first-order formula.

    Quantifiers are written `forall x` and `exists x` and extend as far to the
    right as possible, which is the usual convention and the reason
    `forall x P(x) & Q(x)` means `forall x (P(x) & Q(x))` here.
    """
    state = {"text": text, "position": 0}
    _skip(state)
    formula = _equivalence(state)
    _skip(state)
    if state["position"] != len(state["text"]):
        raise ValueError(f"unexpected character at {state['position']}")
    return formula


def _skip(state):
    """Skip spaces."""
    while state["position"] < len(state["text"]) and state["text"][state["position"]] == " ":
        state["position"] += 1


def _at(state, token):
    """Whether the input continues with a token."""
    _skip(state)
    return state["text"].startswith(token, state["position"])


def _eat(state, token):
    """Consume a token, or fail."""
    if not _at(state, token):
        raise ValueError(f"expected {token} at {state['position']}")
    state["position"] += len(token)


def _equivalence(state):
    """Parse `<->`."""
    left = _implication(state)
    while _at(state, "<->"):
        _eat(state, "<->")
        left = ("<->", left, _implication(state))
    return left


def _implication(state):
    """Parse `->`, right associative."""
    left = _disjunction(state)
    if _at(state, "->"):
        _eat(state, "->")
        return ("->", left, _implication(state))
    return left


def _disjunction(state):
    """Parse `|`."""
    left = _conjunction(state)
    while _at(state, "|"):
        _eat(state, "|")
        left = ("|", left, _conjunction(state))
    return left


def _conjunction(state):
    """Parse `&`."""
    left = _unary(state)
    while _at(state, "&"):
        _eat(state, "&")
        left = ("&", left, _unary(state))
    return left


def _unary(state):
    """Parse quantifiers, negation and the atoms."""
    if _at(state, "forall"):
        _eat(state, "forall")
        variable = _name(state)
        return ("forall", variable, _unary(state))

    if _at(state, "exists"):
        _eat(state, "exists")
        variable = _name(state)
        return ("exists", variable, _unary(state))

    if _at(state, "!"):
        _eat(state, "!")
        return ("!", _unary(state))

    if _at(state, "("):
        _eat(state, "(")
        inner = _equivalence(state)
        _eat(state, ")")
        return inner

    return _atom(state)


def _atom(state):
    """Parse a relation applied to terms."""
    name = _name(state)
    if not _at(state, "("):
        return ("atom", name, [])

    _eat(state, "(")
    arguments = [_term(state)]
    while _at(state, ","):
        _eat(state, ",")
        arguments.append(_term(state))
    _eat(state, ")")
    return ("atom", name, arguments)


def _term(state):
    """Parse a term, which is a name or a function applied to terms."""
    name = _name(state)
    if not _at(state, "("):
        return name

    _eat(state, "(")
    arguments = [_term(state)]
    while _at(state, ","):
        _eat(state, ",")
        arguments.append(_term(state))
    _eat(state, ")")
    return (name, arguments)


def _name(state):
    """Parse an identifier."""
    _skip(state)
    start = state["position"]
    while (state["position"] < len(state["text"])
           and (state["text"][state["position"]].isalnum()
                or state["text"][state["position"]] == "_")):
        state["position"] += 1
    if start == state["position"]:
        raise ValueError(f"expected a name at {start}")
    return state["text"][start:state["position"]]


def free_variables(formula, bound=None):
    """The variables a formula uses without binding them."""
    bound = bound or set()
    kind = formula[0]

    if kind == "atom":
        names = set()
        for argument in formula[2]:
            names |= _term_names(argument)
        return names - bound

    if kind == "!":
        return free_variables(formula[1], bound)

    if kind in ("forall", "exists"):
        return free_variables(formula[2], bound | {formula[1]})

    return free_variables(formula[1], bound) | free_variables(formula[2], bound)


def _term_names(term):
    """Every name occurring in a term."""
    if isinstance(term, tuple):
        names = set()
        for argument in term[1]:
            names |= _term_names(argument)
        return names
    return {term}
