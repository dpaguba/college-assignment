"""Parsing modal formulas, and deciding satisfiability by search.

Modal logic has the **finite model property**: a satisfiable formula has a
model with at most exponentially many worlds in its size. That is what makes
satisfiability decidable at all, and it is why searching over small structures
is a decision procedure rather than a heuristic, as long as the bound is
respected.

The search here enumerates structures up to a few worlds. That is enough for
the formulas an exercise sheet contains and is not how a real prover works: the
standard method is a tableau calculus, which builds only the worlds a formula
forces to exist.
"""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "kripke-structures"))
import kripke_structures as ks


def parse(text):
    """Parse a modal formula.

    `[]` is the box and `<>` the diamond, both prefix and binding as tightly as
    negation. The rest is propositional, with the same precedence as everywhere
    else.
    """
    state = {"text": text.replace(" ", ""), "position": 0}
    formula = _equivalence(state)
    if state["position"] != len(state["text"]):
        raise ValueError(f"unexpected character at {state['position']}")
    return formula


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
    """Parse the prefix operators and the atoms."""
    if _at(state, "[]"):
        _eat(state, "[]")
        return ("[]", _unary(state))
    if _at(state, "<>"):
        _eat(state, "<>")
        return ("<>", _unary(state))
    if _at(state, "!"):
        _eat(state, "!")
        return ("!", _unary(state))
    if _at(state, "("):
        _eat(state, "(")
        inner = _equivalence(state)
        _eat(state, ")")
        return inner

    start = state["position"]
    while (state["position"] < len(state["text"])
           and state["text"][state["position"]].isalnum()):
        state["position"] += 1
    if start == state["position"]:
        raise ValueError(f"expected an atom at {start}")
    return ("var", state["text"][start:state["position"]])


def _at(state, token):
    """Whether the input continues with a token."""
    return state["text"].startswith(token, state["position"])


def _eat(state, token):
    """Consume a token, or fail."""
    if not _at(state, token):
        raise ValueError(f"expected {token} at {state['position']}")
    state["position"] += len(token)


def variables_of(formula):
    """The atoms a formula mentions."""
    kind = formula[0]
    if kind == "var":
        return {formula[1]}
    if kind in ("!", "[]", "<>"):
        return variables_of(formula[1])
    if kind in ("true", "false"):
        return set()
    return variables_of(formula[1]) | variables_of(formula[2])


def structures(variables, size):
    """Every Kripke structure with a given number of worlds over given atoms.

    Exponential in both arguments, which is exactly why this is a teaching
    procedure and not a prover: two worlds and two atoms already give 4096
    structures, and each extra world squares the number of relations.
    """
    worlds = list(range(size))
    pairs = [(source, target) for source in worlds for target in worlds]

    for relation_bits in itertools.product([False, True], repeat=len(pairs)):
        accessible = {world: [] for world in worlds}
        for (source, target), present in zip(pairs, relation_bits):
            if present:
                accessible[source].append(target)

        for label_bits in itertools.product([False, True],
                                            repeat=size * len(variables)):
            labels = {}
            index = 0
            for world in worlds:
                labels[world] = set()
                for name in variables:
                    if label_bits[index]:
                        labels[world].add(name)
                    index += 1
            yield ks.Kripke(worlds, accessible, labels)


def satisfiable(text, limit=3):
    """A structure and world satisfying the formula, or `None`.

    Searches structures with one world, then two, and so on. Small models are
    tried first because most satisfiable formulas have one, and because a
    smaller witness is a better explanation.
    """
    formula = parse(text) if isinstance(text, str) else text
    variables = sorted(variables_of(formula)) or ["p"]

    for size in range(1, limit + 1):
        for structure in structures(variables, size):
            for world in structure.worlds:
                if structure.holds(formula, world):
                    return structure, world

    return None


def valid(text, limit=3):
    """Whether a formula holds in every world of every structure.

    Valid exactly when its negation is unsatisfiable, which is how it is
    decided here. The bound makes this a search for a counterexample rather
    than a proof, and the two axioms it is tested on show the difference: the
    K axiom has no counterexample because it is valid, and `[]A -> A` has one
    with a single world.
    """
    formula = parse(text) if isinstance(text, str) else text
    return satisfiable(("!", formula), limit) is None
