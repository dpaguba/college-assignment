"""Propositional formulas, conjunctive normal form, and what entailment means.

Everything the verification folder does eventually becomes a question about a
propositional formula: is it satisfiable? The lecture states the three
questions in one place, and they are all the same question:

- satisfiable: some assignment makes it true
- contradictory: no assignment makes ``phi and psi`` true
- entailment, written ``phi |= psi``: no assignment makes ``phi and not psi``
  true

The last one is the one that matters. Bounded model checking, inductive
invariants and Hoare proofs are all entailment checks, and each of them is
answered by asking a satisfiability solver about the negation.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass


class Formula:
    """Base class of propositional formulas."""

    def atoms(self):
        """Every atom name occurring in the formula."""
        raise NotImplementedError

    def evaluate(self, assignment):
        """The truth value under a mapping from atom names to booleans."""
        raise NotImplementedError


@dataclass(frozen=True)
class Atom(Formula):
    """A propositional variable."""

    name: str

    def atoms(self):
        """The atom itself."""
        return frozenset({self.name})

    def evaluate(self, assignment):
        """The value bound to the name."""
        return assignment[self.name]

    def __str__(self):
        """The variable name."""
        return self.name


@dataclass(frozen=True)
class Constant(Formula):
    """The formula true or the formula false."""

    value: bool

    def atoms(self):
        """A constant contains no atoms."""
        return frozenset()

    def evaluate(self, assignment):
        """The constant itself."""
        return self.value

    def __str__(self):
        """The constant as true or false."""
        return "true" if self.value else "false"


@dataclass(frozen=True)
class Not(Formula):
    """Negation."""

    operand: Formula

    def atoms(self):
        """The atoms of the operand."""
        return self.operand.atoms()

    def evaluate(self, assignment):
        """The negated value of the operand."""
        return not self.operand.evaluate(assignment)

    def __str__(self):
        """The negation."""
        return f"!{self.operand}"


@dataclass(frozen=True)
class And(Formula):
    """Conjunction of any number of formulas."""

    parts: tuple

    def atoms(self):
        """The atoms of every part."""
        return frozenset().union(*(part.atoms() for part in self.parts)) if self.parts \
            else frozenset()

    def evaluate(self, assignment):
        """True when every part is true."""
        return all(part.evaluate(assignment) for part in self.parts)

    def __str__(self):
        """The conjunction, bracketed, or true when it is empty."""
        return "(" + " & ".join(str(part) for part in self.parts) + ")" if self.parts else "true"


@dataclass(frozen=True)
class Or(Formula):
    """Disjunction of any number of formulas."""

    parts: tuple

    def atoms(self):
        """The atoms of every part."""
        return frozenset().union(*(part.atoms() for part in self.parts)) if self.parts \
            else frozenset()

    def evaluate(self, assignment):
        """True when at least one part is true."""
        return any(part.evaluate(assignment) for part in self.parts)

    def __str__(self):
        """The disjunction, bracketed, or false when it is empty."""
        return "(" + " | ".join(str(part) for part in self.parts) + ")" if self.parts else "false"


@dataclass(frozen=True)
class Implies(Formula):
    """Material implication, kept as its own node so formulas read as they are written."""

    left: Formula
    right: Formula

    def atoms(self):
        """The atoms of both sides."""
        return self.left.atoms() | self.right.atoms()

    def evaluate(self, assignment):
        """False only when the left side holds and the right one does not."""
        return (not self.left.evaluate(assignment)) or self.right.evaluate(assignment)

    def __str__(self):
        """The implication."""
        return f"({self.left} -> {self.right})"


@dataclass(frozen=True)
class Iff(Formula):
    """Biconditional."""

    left: Formula
    right: Formula

    def atoms(self):
        """The atoms of both sides."""
        return self.left.atoms() | self.right.atoms()

    def evaluate(self, assignment):
        """True when both sides agree."""
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def __str__(self):
        """The equivalence."""
        return f"({self.left} <-> {self.right})"


@dataclass(frozen=True)
class Literal:
    """An atom or its negation, the unit a clause is built from."""

    name: str
    positive: bool = True

    def negated(self):
        """The same atom with the opposite sign."""
        return Literal(self.name, not self.positive)

    def evaluate(self, assignment):
        """The value of the literal under a partial or total assignment."""
        value = assignment[self.name]
        return value if self.positive else not value

    def __str__(self):
        """The literal, with a leading mark when it is negated."""
        return self.name if self.positive else f"!{self.name}"


def clause(*literals):
    """A clause, which is a disjunction of literals held as a frozen set."""
    return frozenset(literals)


def cnf_atoms(clauses):
    """Every atom name occurring in a set of clauses."""
    return {literal.name for one in clauses for literal in one}


def evaluate_clauses(clauses, assignment):
    """True when every clause has a literal that is true under the assignment."""
    return all(any(literal.evaluate(assignment) for literal in one) for one in clauses)


def to_nnf(formula):
    """Push negations down to the atoms, removing implications on the way.

    Negation normal form is the halfway house to CNF: after this step the only
    negations left sit directly on atoms, so the distribution below has fewer
    cases to handle.
    """
    if isinstance(formula, (Atom, Constant)):
        return formula
    if isinstance(formula, Implies):
        return to_nnf(Or((Not(formula.left), formula.right)))
    if isinstance(formula, Iff):
        return to_nnf(And((Implies(formula.left, formula.right),
                           Implies(formula.right, formula.left))))
    if isinstance(formula, And):
        return And(tuple(to_nnf(part) for part in formula.parts))
    if isinstance(formula, Or):
        return Or(tuple(to_nnf(part) for part in formula.parts))

    inner = formula.operand
    if isinstance(inner, Atom):
        return formula
    if isinstance(inner, Constant):
        return Constant(not inner.value)
    if isinstance(inner, Not):
        return to_nnf(inner.operand)
    if isinstance(inner, And):
        return Or(tuple(to_nnf(Not(part)) for part in inner.parts))
    if isinstance(inner, Or):
        return And(tuple(to_nnf(Not(part)) for part in inner.parts))
    return to_nnf(Not(to_nnf(inner)))


def to_cnf(formula):
    """Convert to a set of clauses by distributing or over and.

    Correct and exponential in the worst case: distributing an ``or`` of two
    conjunctions multiplies their clause counts. For hand-sized formulas that
    is fine, and ``to_tseitin`` is the linear alternative when it is not.
    """
    return _distribute(to_nnf(formula))


def _distribute(formula):
    """The clauses of the formula, distributing or over and."""
    if isinstance(formula, Atom):
        return {clause(Literal(formula.name))}
    if isinstance(formula, Not):
        return {clause(Literal(formula.operand.name, False))}
    if isinstance(formula, Constant):
        return set() if formula.value else {frozenset()}
    if isinstance(formula, And):
        result = set()
        for part in formula.parts:
            result |= _distribute(part)
        return result

    parts = [_distribute(part) for part in formula.parts]
    result = {frozenset()}
    for clauses in parts:
        result = {left | right for left in result for right in clauses}
    return result


def to_tseitin(formula, prefix="t"):
    """Convert to CNF in linear size by naming every subformula.

    The clauses produced are not equivalent to the original formula, they are
    **equisatisfiable**: a fresh atom stands for each subformula, and clauses
    force it to agree with what it names. Satisfiability is preserved, which is
    all a solver needs, and the size grows linearly instead of exponentially.

    This is what every real solver front end does, and it is the reason a
    million-clause instance can come from a formula that would blow up under
    naive distribution.
    """
    clauses = set()
    counter = itertools.count()

    def encode(node):
        """The literal standing for a subformula, defining it on first use."""
        if isinstance(node, Atom):
            return Literal(node.name)
        if isinstance(node, Constant):
            name = f"{prefix}{next(counter)}"
            clauses.add(clause(Literal(name, node.value)))
            return Literal(name)
        if isinstance(node, Not):
            return encode(node.operand).negated()

        if isinstance(node, Implies):
            node = Or((Not(node.left), node.right))
        elif isinstance(node, Iff):
            node = And((Implies(node.left, node.right), Implies(node.right, node.left)))

        parts = [encode(part) for part in node.parts]
        name = f"{prefix}{next(counter)}"
        gate = Literal(name)

        if isinstance(node, And):
            for part in parts:
                clauses.add(clause(gate.negated(), part))
            clauses.add(clause(gate, *(part.negated() for part in parts)))
        else:
            for part in parts:
                clauses.add(clause(gate, part.negated()))
            clauses.add(clause(gate.negated(), *parts))

        return gate

    root = encode(formula)
    clauses.add(clause(root))
    return clauses


def brute_force_satisfiable(clauses):
    """Try every assignment, for checking the real solvers against.

    2^n assignments, which is exactly what DPLL exists to avoid, and exactly
    what makes it a trustworthy reference on small inputs.
    """
    names = sorted(cnf_atoms(clauses))
    for values in itertools.product([False, True], repeat=len(names)):
        assignment = dict(zip(names, values))
        if evaluate_clauses(clauses, assignment):
            return assignment
    return None


def entails(premise, conclusion, solver=None):
    """Check ``premise |= conclusion`` by looking for a counterexample.

    The check is one line of logic and the whole basis of the verification
    folder: an entailment holds exactly when ``premise and not conclusion`` has
    no model. A model that is found is a counterexample, and printing it is
    usually more useful than the answer.
    """
    formula = And((premise, Not(conclusion)))
    clauses = to_tseitin(formula)
    solve = solver or brute_force_satisfiable
    model = solve(clauses)
    return model is None, model
