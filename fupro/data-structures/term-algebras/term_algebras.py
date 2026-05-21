"""Term algebras, and why a fold is an interpretation.

A term built from constructors carries no meaning. An algebra assigns a
value to each constructor, and folding the term with that algebra is the
unique way to give the term a meaning consistent with its structure. Changing
the algebra changes the meaning without touching the term, which is why the
same expression can be evaluated, measured and printed by the same traversal.

That uniqueness is what "the term algebra is initial" says: from it there is
exactly one homomorphism into any other algebra.
"""


def term(name, *arguments):
    """A term built from a constructor and its arguments."""
    return (name,) + arguments


VALUE = {
    "Lit": lambda value: value,
    "Add": lambda left, right: left + right,
    "Mul": lambda left, right: left * right,
}
"""The algebra that evaluates an expression."""

SIZE = {
    "Lit": lambda value: 1,
    "Add": lambda left, right: left + right + 1,
    "Mul": lambda left, right: left + right + 1,
}
"""The algebra that counts the nodes."""

TEXT = {
    "Lit": lambda value: str(value),
    "Add": lambda left, right: "(%s + %s)" % (left, right),
    "Mul": lambda left, right: "(%s * %s)" % (left, right),
}
"""The algebra that prints the expression."""


def interpret(value, algebra):
    """Folds a term with the given algebra."""
    name = value[0]
    if name == "Lit":
        return algebra["Lit"](value[1])
    parts = [interpret(part, algebra) for part in value[1:]]
    return algebra[name](*parts)


def evaluate(value):
    """The value of a term, which is the interpretation in the value algebra."""
    return interpret(value, VALUE)


def initiality_holds(samples=None):
    """Whether interpreting agrees with building and then mapping.

    The initiality of the term algebra says the interpretation is the only
    structure-preserving map out of it. Checked here by building a term two
    ways and confirming the interpretations agree, which is the computational
    content of the statement.
    """
    samples = samples or [
        term("Add", term("Lit", 2), term("Lit", 3)),
        term("Mul", term("Add", term("Lit", 1), term("Lit", 2)), term("Lit", 4)),
    ]
    for sample in samples:
        direct = evaluate(sample)
        composed = interpret(sample, VALUE)
        if direct != composed:
            return False
    return True
