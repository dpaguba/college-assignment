"""The Herbrand universe, the Herbrand expansion, and ground resolution.

A first-order formula in Skolem form is unsatisfiable exactly when some finite
set of **ground instances** of its matrix is unsatisfiable as a propositional
formula. That is Herbrand's theorem, and it is what makes first-order
refutation possible at all: an infinite question about all structures becomes a
sequence of finite propositional questions.

The instances are taken over the **Herbrand universe**: all ground terms
buildable from the signature's constants and function symbols. With any
function symbol that universe is infinite, so the sequence of propositional
questions never ends, which is exactly the sense in which first-order validity
is semi-decidable.
"""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "propositional-logic", "resolution"))
import resolution as prop


class Signature:
    """The constants and function symbols a formula uses."""

    def __init__(self, constants, functions):
        """Store the constants and the arities of the function symbols."""
        self.constants = list(constants) or ["a"]
        self.functions = dict(functions)
        self.invented = not constants

    def universe(self, max_depth):
        """Ground terms with at most the given nesting of function symbols.

        Depth 0 is the constants. Each further level applies every function
        symbol to every combination of the terms already built, which is why
        the universe grows so fast: with two constants, one unary and one
        binary function, depth 1 already has 8 terms and depth 2 has 74.

        A signature with no constant symbol gets one invented, since otherwise
        the universe would be empty and the theorem would say nothing.
        """
        terms = list(self.constants)

        for _ in range(max_depth):
            new = list(terms)
            for name, arity in sorted(self.functions.items()):
                for arguments in itertools.product(terms, repeat=arity):
                    candidate = f"{name}({','.join(arguments)})"
                    if candidate not in new:
                        new.append(candidate)
            terms = new

        return terms


def instantiate(formula, substitution):
    """Replace variables by ground terms throughout a formula."""
    kind = formula[0]

    if kind == "atom":
        return ("atom", formula[1],
                [_instantiate_term(argument, substitution) for argument in formula[2]])
    if kind == "!":
        return ("!", instantiate(formula[1], substitution))
    return (kind, instantiate(formula[1], substitution),
            instantiate(formula[2], substitution))


def _instantiate_term(term, substitution):
    """Replace variables inside a term, textually."""
    if isinstance(term, tuple):
        return (term[0], [_instantiate_term(a, substitution) for a in term[1]])

    if term in substitution:
        return substitution[term]

    for variable, replacement in substitution.items():
        if variable in term and not term.replace(variable, "").isalnum():
            pass

    return _replace_in_text(term, substitution)


def _replace_in_text(term, substitution):
    """Replace whole-word variable occurrences inside a textual term."""
    result = ""
    current = ""

    for character in term:
        if character.isalnum() or character == "_":
            current += character
        else:
            result += substitution.get(current, current) + character
            current = ""

    return result + substitution.get(current, current)


def to_text(formula):
    """Print a formula."""
    kind = formula[0]

    if kind == "atom":
        if not formula[2]:
            return formula[1]
        return f"{formula[1]}({','.join(_term_text(a) for a in formula[2])})"
    if kind == "!":
        return "!" + to_text(formula[1])
    return f"({to_text(formula[1])} {kind} {to_text(formula[2])})"


def _term_text(term):
    """Print a term."""
    if isinstance(term, tuple):
        return f"{term[0]}({','.join(_term_text(a) for a in term[1])})"
    return term


def expansion(matrix, variables, signature, depth):
    """Every ground instance of a matrix over the Herbrand universe.

    The size is the universe raised to the number of variables, which is why
    an implementation searches depth by depth rather than generating the whole
    expansion: at depth 1 with two variables over the sheet's signature that is
    64 instances, at depth 2 it is 5476.
    """
    terms = signature.universe(depth)
    instances = []

    for values in itertools.product(terms, repeat=len(variables)):
        substitution = dict(zip(variables, values))
        instances.append(instantiate(matrix, substitution))

    return instances


def ground_refute(clauses):
    """Refute a set of ground clauses by propositional resolution.

    Once the instances are ground there is no unification left to do, and the
    problem is exactly the propositional one solved in
    [propositional-logic/resolution](../../propositional-logic/resolution/).
    """
    return prop.refute([set(clause) for clause in clauses])


def refute_with_expansion(clauses, signature, depth):
    """Instantiate clauses over the universe and refute them propositionally.

    This is Herbrand's theorem used as an algorithm, and it terminates on
    unsatisfiable input only. On satisfiable input it runs forever, deepening
    the universe, which is the semi-decidability of first-order logic in
    executable form.
    """
    variables = sorted({name for clause in clauses for _, arguments in clause
                        for argument in arguments
                        for name in _variables_in(argument)})

    terms = signature.universe(depth)
    ground = []

    for values in itertools.product(terms, repeat=len(variables)):
        substitution = dict(zip(variables, values))
        for clause in clauses:
            instance = set()
            for name, arguments in clause:
                grounded = [_replace_in_text(argument, substitution)
                            for argument in arguments]
                instance.add(f"{name}({','.join(grounded)})")
            ground.append(instance)

    return prop.refute(ground)


def _variables_in(term):
    """The variables of a textual term, by the lecture's naming convention."""
    names = set()
    current = ""

    for character in term + " ":
        if character.isalnum() or character == "_":
            current += character
        else:
            if len(current) == 1 and current in "uvwxyz":
                names.add(current)
            current = ""

    return names
