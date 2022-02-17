"""Equivalence transformations: rewriting a formula without changing its models.

The exercise sheets ask for the transformation to NNF or CNF **step by step,
naming the law used at each step**, and that requirement is the reason this
module exists in the form it does. A function returning only the final formula
would answer the question and teach nothing about why the answer is right.

Every law is an equivalence, so every step preserves the set of models exactly.
That is checkable rather than assumed, and it is what the tests check: the
models of every intermediate formula are the models of the original.
"""

from __future__ import annotations

LAWS = {
    "implication": "A -> B is !A | B",
    "equivalence": "A <-> B is (A -> B) & (B -> A)",
    "de morgan": "!(A & B) is !A | !B, and dually",
    "double negation": "!!A is A",
    "distributivity": "A | (B & C) is (A | B) & (A | C), and dually",
    "commutativity": "A & B is B & A, and dually",
    "associativity": "(A & B) & C is A & (B & C), and dually",
}
"""The named laws the sheets expect, with the shape each one rewrites."""


def parse(text):
    """Parse a propositional formula.

    Precedence from loosest to tightest: `<->`, `->`, `|`, `&`, `!`. Implication
    is right associative, which is why `A -> B -> C` is `A -> (B -> C)` and not
    the other grouping: the other grouping is not even equivalent.
    """
    state = {"text": text.replace(" ", ""), "position": 0}
    formula = _equivalence(state)
    if state["position"] != len(state["text"]):
        raise ValueError(f"unexpected character at {state['position']}")
    return formula


def _equivalence(state):
    """Parse the loosest level, `<->`."""
    left = _implication(state)
    while _looking_at(state, "<->"):
        _consume(state, "<->")
        left = ("<->", left, _implication(state))
    return left


def _implication(state):
    """Parse `->`, right associative."""
    left = _disjunction(state)
    if _looking_at(state, "->"):
        _consume(state, "->")
        return ("->", left, _implication(state))
    return left


def _disjunction(state):
    """Parse `|`."""
    left = _conjunction(state)
    while _looking_at(state, "|"):
        _consume(state, "|")
        left = ("|", left, _conjunction(state))
    return left


def _conjunction(state):
    """Parse `&`."""
    left = _negation(state)
    while _looking_at(state, "&"):
        _consume(state, "&")
        left = ("&", left, _negation(state))
    return left


def _negation(state):
    """Parse `!` and the atoms."""
    if _looking_at(state, "!"):
        _consume(state, "!")
        return ("!", _negation(state))

    if _looking_at(state, "("):
        _consume(state, "(")
        inner = _equivalence(state)
        _consume(state, ")")
        return inner

    start = state["position"]
    while (state["position"] < len(state["text"])
           and state["text"][state["position"]].isalnum()):
        state["position"] += 1

    if start == state["position"]:
        raise ValueError(f"expected a variable at {start}")

    return ("var", state["text"][start:state["position"]])


def _looking_at(state, token):
    """Whether the input continues with a token."""
    return state["text"].startswith(token, state["position"])


def _consume(state, token):
    """Consume a token, or fail."""
    if not _looking_at(state, token):
        raise ValueError(f"expected {token} at {state['position']}")
    state["position"] += len(token)


def to_text(formula):
    """Print a formula, bracketing every binary operator."""
    kind = formula[0]
    if kind == "var":
        return formula[1]
    if kind == "!":
        return "!" + to_text(formula[1])
    return f"({to_text(formula[1])} {kind} {to_text(formula[2])})"


def variables_of(formula):
    """The variables a formula mentions."""
    kind = formula[0]
    if kind == "var":
        return {formula[1]}
    if kind == "!":
        return variables_of(formula[1])
    return variables_of(formula[1]) | variables_of(formula[2])


def evaluate(formula, assignment):
    """The truth value of a formula under an assignment."""
    kind = formula[0]

    if kind == "var":
        return assignment[formula[1]]
    if kind == "!":
        return not evaluate(formula[1], assignment)

    left = evaluate(formula[1], assignment)
    right = evaluate(formula[2], assignment)

    if kind == "&":
        return left and right
    if kind == "|":
        return left or right
    if kind == "->":
        return (not left) or right
    return left == right


def is_nnf(formula):
    """Whether negation appears only directly in front of variables."""
    kind = formula[0]
    if kind == "var":
        return True
    if kind == "!":
        return formula[1][0] == "var"
    if kind in ("->", "<->"):
        return False
    return is_nnf(formula[1]) and is_nnf(formula[2])


def is_cnf(formula):
    """Whether the formula is a conjunction of disjunctions of literals."""
    if not is_nnf(formula):
        return False

    def clause(current):
        """Whether a subformula is a disjunction of literals."""
        if current[0] in ("var", "!"):
            return True
        if current[0] == "|":
            return clause(current[1]) and clause(current[2])
        return False

    def conjunction(current):
        """Whether a subformula is a conjunction of clauses."""
        if current[0] == "&":
            return conjunction(current[1]) and conjunction(current[2])
        return clause(current)

    return conjunction(formula)


def to_nnf_steps(formula):
    """Every rewriting step on the way to negation normal form.

    Each entry is a formula and the name of the law that produced it, with the
    original carrying no law. The first applicable law is used at the outermost
    applicable position, which makes the sequence deterministic and therefore
    comparable against a written solution.
    """
    steps = [(formula, None)]
    current = formula

    while True:
        result = _one_nnf_step(current)
        if result is None:
            return steps
        current, law = result
        steps.append((current, law))


def _one_nnf_step(formula):
    """One rewriting step towards NNF, or `None` when none applies."""
    kind = formula[0]

    if kind == "<->":
        left, right = formula[1], formula[2]
        return ("&", ("->", left, right), ("->", right, left)), "equivalence"

    if kind == "->":
        return ("|", ("!", formula[1]), formula[2]), "implication"

    if kind == "!":
        inner = formula[1]
        if inner[0] == "!":
            return inner[1], "double negation"
        if inner[0] == "&":
            return ("|", ("!", inner[1]), ("!", inner[2])), "de morgan"
        if inner[0] == "|":
            return ("&", ("!", inner[1]), ("!", inner[2])), "de morgan"
        if inner[0] in ("->", "<->"):
            rewritten = _one_nnf_step(inner)
            return ("!", rewritten[0]), rewritten[1]
        return None

    if kind in ("&", "|"):
        for index in (1, 2):
            rewritten = _one_nnf_step(formula[index])
            if rewritten is not None:
                parts = list(formula)
                parts[index] = rewritten[0]
                return tuple(parts), rewritten[1]

    return None


def to_nnf(formula):
    """The negation normal form."""
    return to_nnf_steps(formula)[-1][0]


def to_cnf(formula):
    """The conjunctive normal form, by NNF and then distribution.

    Distributing disjunction over conjunction can square the size of the
    formula, and repeating it can make the growth exponential. That is the
    reason Tseitin's transformation exists, and it is in
    [swk/verification/propositional-logic](../../../swk/verification/propositional-logic/):
    it gives up equivalence for equisatisfiability and stays linear.
    """
    current = to_nnf(formula)

    while True:
        result = _distribute(current, over="&")
        if result is None:
            return current
        current = result


def to_dnf(formula):
    """The disjunctive normal form, by distributing the other way."""
    current = to_nnf(formula)

    while True:
        result = _distribute(current, over="|")
        if result is None:
            return current
        current = result


def _distribute(formula, over):
    """One distribution step, or `None` when the formula is already normal."""
    outer = "|" if over == "&" else "&"
    kind = formula[0]

    if kind == outer:
        for index, other in ((1, 2), (2, 1)):
            if formula[index][0] == over:
                inner = formula[index]
                rest = formula[other]
                return (over, (outer, inner[1], rest), (outer, inner[2], rest))

    if kind in ("&", "|"):
        for index in (1, 2):
            rewritten = _distribute(formula[index], over)
            if rewritten is not None:
                parts = list(formula)
                parts[index] = rewritten
                return tuple(parts)

    return None


def clauses_of(formula):
    """The clauses of a CNF formula, as sets of literal strings."""
    def literals(current):
        """Collect the literals of one clause."""
        if current[0] == "|":
            return literals(current[1]) | literals(current[2])
        if current[0] == "!":
            return {"!" + current[1][1]}
        return {current[1]}

    def conjuncts(current):
        """Split a conjunction into its clauses."""
        if current[0] == "&":
            return conjuncts(current[1]) + conjuncts(current[2])
        return [literals(current)]

    return conjuncts(formula)
