"""Hoare logic: proving what a program computes, not just running it.

A Hoare triple ``{P} S {Q}`` claims that if P holds before S runs and S
terminates, then Q holds afterwards. Partial correctness only: termination is
a separate obligation, and the while rule below says nothing about it.

The rules are syntax-directed, so a proof follows the shape of the program:

    {Q} skip {Q}                                        skip
    {Q[a/x]} x := a {Q}                                 assignment
    {P} S1 {R}, {R} S2 {Q}  =>  {P} S1;S2 {Q}           sequence
    {P and b} S1 {Q}, {P and !b} S2 {Q}                 conditional
    {I and b} S {I}  =>  {I} while b do S {I and !b}    loop
    P -> P', {P'} S {Q'}, Q' -> Q                       consequence

Everything except the loop is mechanical. The loop needs an invariant, and
finding it is the part no rule provides.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-analysis" / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "linear-arithmetic"))

import linear_arithmetic as arithmetic
from while_language import (Assign, BinOp, Bool, If, Not, Num, Seq, Skip, Var,
                            While, parse)


def substitute(expression, name, replacement):
    """Replace every occurrence of a variable by an expression.

    The assignment rule is nothing but this, applied backwards: to know what
    must hold before ``x := a`` so that Q holds after, replace x by a in Q.
    Working backwards is what makes the rule an equality rather than a guess.
    """
    if isinstance(expression, Var):
        return replacement if expression.name == name else expression
    if isinstance(expression, (Num, Bool)):
        return expression
    if isinstance(expression, Not):
        return Not(substitute(expression.operand, name, replacement))
    if isinstance(expression, BinOp):
        return BinOp(expression.op,
                     substitute(expression.left, name, replacement),
                     substitute(expression.right, name, replacement))
    raise TypeError(f"cannot substitute inside {expression!r}")


def implies(left, right):
    """The formula ``left -> right``, written with the operators available."""
    return BinOp("||", Not(left), right)


@dataclass
class Obligation:
    """One side condition a proof leaves behind, with where it came from."""

    origin: str
    formula: object
    label: int = None

    def __str__(self):
        """The obligation with the place it came from."""
        where = f" at {self.label}" if self.label is not None else ""
        return f"{self.origin}{where}: {self.formula}"


@dataclass
class Proof:
    """The weakest precondition of a statement plus the obligations collected."""

    precondition: object
    obligations: list = field(default_factory=list)


def weakest_precondition(statement, postcondition, invariants=None):
    """Compute wp(S, Q) and the obligations the loops leave behind.

    ``wp(S, Q)`` is the weakest condition that guarantees Q after S. Every rule
    but the loop computes it exactly; a loop returns its invariant and adds two
    obligations, because no rule can derive an invariant from the program.

    ``invariants`` maps a loop's label to its invariant.
    """
    invariants = invariants or {}
    proof = Proof(None, [])
    proof.precondition = _wp(statement, postcondition, invariants, proof.obligations)
    return proof


def _wp(statement, postcondition, invariants, obligations):
    """The weakest precondition of the statement for this postcondition."""
    if isinstance(statement, Skip):
        return postcondition

    if isinstance(statement, Assign):
        return substitute(postcondition, statement.variable, statement.expression)

    if isinstance(statement, Seq):
        after = _wp(statement.second, postcondition, invariants, obligations)
        return _wp(statement.first, after, invariants, obligations)

    if isinstance(statement, If):
        then_part = _wp(statement.then_branch, postcondition, invariants, obligations)
        else_part = _wp(statement.else_branch, postcondition, invariants, obligations)
        return BinOp("&&",
                     implies(statement.condition, then_part),
                     implies(Not(statement.condition), else_part))

    if isinstance(statement, While):
        if statement.label not in invariants:
            raise KeyError(f"no invariant given for the loop at label {statement.label}")

        invariant = invariants[statement.label]
        body_precondition = _wp(statement.body, invariant, invariants, obligations)

        obligations.append(Obligation(
            "loop preserves the invariant",
            implies(BinOp("&&", invariant, statement.condition), body_precondition),
            statement.label))
        obligations.append(Obligation(
            "invariant and exit test give the postcondition",
            implies(BinOp("&&", invariant, Not(statement.condition)), postcondition),
            statement.label))

        return invariant

    raise TypeError(f"not a While statement: {statement!r}")


def verification_conditions(precondition, statement, postcondition, invariants=None):
    """Every formula that must be valid for the triple to hold.

    The first is always ``P -> wp(S, Q)``, the entry condition. The rest come
    from the loops. Discharging them is a separate job, and handing them to a
    solver is exactly what a modern verifier does.
    """
    proof = weakest_precondition(statement, postcondition, invariants)
    conditions = [Obligation("precondition implies wp",
                             implies(precondition, proof.precondition))]
    conditions.extend(proof.obligations)
    return conditions


def verify(precondition, statement, postcondition, invariants=None, domains=None,
           low=-16, high=16):
    """Check every verification condition over bounded integer domains.

    Returns whether all conditions hold and the list of results per condition.
    The bounds make this a check rather than a proof: a condition that holds
    for every value in the range may still fail outside it. For the exercises
    the range covers the interesting cases, and the failures it does report are
    real.
    """
    if isinstance(statement, str):
        statement = parse(statement)

    conditions = verification_conditions(precondition, statement, postcondition, invariants)

    names = set()
    for condition in conditions:
        names |= set(condition.formula.variables())
    domains = domains or {name: arithmetic.Domain(low, high) for name in sorted(names)}

    results = []
    for condition in conditions:
        counterexample = arithmetic.search(Not(condition.formula), domains)
        results.append((condition, counterexample is None, counterexample))

    return all(ok for _, ok, _ in results), results


def proof_tree(statement, postcondition, invariants=None, depth=0):
    """A readable derivation, annotating each statement with the condition before it.

    Read from the bottom up it is the proof: each line shows what has to hold
    before that statement so that the line below it can assume its own
    precondition.
    """
    invariants = invariants or {}
    lines = []
    _annotate(statement, postcondition, invariants, depth, lines)
    return "\n".join(lines)


def _annotate(statement, postcondition, invariants, depth, lines):
    """The proof outline, with the condition that holds before each statement."""
    indent = "  " * depth
    before = _wp(statement, postcondition, invariants, [])

    if isinstance(statement, Seq):
        after_first = _wp(statement.second, postcondition, invariants, [])
        _annotate(statement.first, after_first, invariants, depth, lines)
        _annotate(statement.second, postcondition, invariants, depth, lines)
        return

    lines.append(f"{indent}{{{before}}}")
    if isinstance(statement, If):
        lines.append(f"{indent}if [{statement.condition}]{statement.label} then")
        _annotate(statement.then_branch, postcondition, invariants, depth + 1, lines)
        lines.append(f"{indent}else")
        _annotate(statement.else_branch, postcondition, invariants, depth + 1, lines)
    elif isinstance(statement, While):
        lines.append(f"{indent}while [{statement.condition}]{statement.label} do")
        _annotate(statement.body, invariants[statement.label], invariants, depth + 1, lines)
    else:
        lines.append(f"{indent}{statement}")
    lines.append(f"{indent}{{{postcondition}}}")
