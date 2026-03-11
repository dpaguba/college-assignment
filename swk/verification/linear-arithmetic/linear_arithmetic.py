"""Deciding arithmetic constraints, the part a SAT solver cannot do alone.

Bounded model checking and Hoare proofs both end in a question about integers,
not about propositional atoms: is ``s = 20 and s' = s / 2 and not (s' mod 2 = 0)``
satisfiable? That question needs a theory solver, which is the T in SMT.

Two are here, and they are complementary:

- ``fourier_motzkin`` decides conjunctions of **linear** inequalities over the
  rationals, and it is complete: it eliminates variables one at a time until
  the truth is arithmetic on constants
- ``search`` decides **anything** the expression language can express, over
  **bounded** integer domains, by backtracking with propagation

Neither is a general decision procedure for integer arithmetic, and none can
be: Presburger arithmetic is decidable but expensive, and once multiplication
of variables is allowed the problem is undecidable outright. The bounds are
where that difficulty is parked, and the exercise instances live well inside
them.
"""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-analysis" / "while-language"))

from while_language import BinOp, Bool, Not, Num, Var


@dataclass(frozen=True)
class Domain:
    """The integers a variable may take, inclusive at both ends."""

    low: int
    high: int

    def values(self):
        """Every value in the domain, low first."""
        return range(self.low, self.high + 1)


def variables(expression):
    """Every variable name occurring in an expression."""
    return set(expression.variables())


def search(constraint, domains, all_models=False):
    """Find an integer assignment satisfying the constraint inside the domains.

    Backtracking with one useful refinement: as soon as every variable of a
    conjunct is assigned, that conjunct is evaluated, and a false one prunes
    the whole subtree. Without it this is 2^n enumeration; with it the
    exercise-sized instances finish immediately.

    Division and modulo by zero make a branch fail rather than raise, since a
    partial assignment that divides by zero simply is not a model.
    """
    conjuncts = _conjuncts(constraint)
    order = sorted(variables(constraint))
    missing = [name for name in order if name not in domains]
    if missing:
        raise KeyError(f"no domain given for {missing}")

    found = []

    def extend(index, assignment):
        """Assigns the next variable and recurses over the remaining ones."""
        if index == len(order):
            if _holds(constraint, assignment):
                found.append(dict(assignment))
                return not all_models
            return False

        name = order[index]
        for value in domains[name].values():
            assignment[name] = value
            if _consistent(conjuncts, assignment):
                if extend(index + 1, assignment):
                    del assignment[name]
                    return True
            del assignment[name]
        return False

    extend(0, {})
    if all_models:
        return found
    return found[0] if found else None


def satisfiable(constraint, domains):
    """True when the constraint has a model inside the domains."""
    return search(constraint, domains) is not None


def entails(premise, conclusion, domains):
    """Check ``premise |= conclusion`` over the bounded domains.

    Same trick as in propositional logic: look for a model of the premise that
    breaks the conclusion. Bounded, so a "holds" answer means "holds for every
    value in these domains", which is exactly the guarantee bounded model
    checking gives and no more.
    """
    counterexample = search(BinOp("&&", premise, Not(conclusion)), domains)
    return counterexample is None, counterexample


def _conjuncts(expression):
    """Split a conjunction into its parts, so each can be checked as soon as possible."""
    if isinstance(expression, BinOp) and expression.op == "&&":
        return _conjuncts(expression.left) + _conjuncts(expression.right)
    return [expression]


def _consistent(conjuncts, assignment):
    """False when some fully assigned conjunct is already violated."""
    for conjunct in conjuncts:
        if variables(conjunct) <= set(assignment) and not _holds(conjunct, assignment):
            return False
    return True


def _holds(expression, assignment):
    """Whether the constraint holds under the assignment."""
    try:
        return bool(expression.evaluate(assignment))
    except (ZeroDivisionError, KeyError):
        return False


def linear_form(expression):
    """Express a term as coefficients per variable plus a constant, or None.

    Returns a dictionary mapping variable names to Fractions with the constant
    under the empty key. Anything with a variable times a variable, a division
    by a variable, or a modulo comes back as None, which is the signal to fall
    back on the bounded search.
    """
    if isinstance(expression, Num):
        return {"": Fraction(expression.value)}
    if isinstance(expression, Var):
        return {expression.name: Fraction(1), "": Fraction(0)}

    if isinstance(expression, BinOp):
        left = linear_form(expression.left)
        right = linear_form(expression.right)
        if left is None or right is None:
            return None

        if expression.op in ("+", "-"):
            sign = 1 if expression.op == "+" else -1
            combined = dict(left)
            for name, value in right.items():
                combined[name] = combined.get(name, Fraction(0)) + sign * value
            return combined

        if expression.op == "*":
            if _is_constant(left):
                return {name: left[""] * value for name, value in right.items()}
            if _is_constant(right):
                return {name: right[""] * value for name, value in left.items()}
            return None

        if expression.op == "/" and _is_constant(right) and right[""] != 0:
            return {name: value / right[""] for name, value in left.items()}

    return None


def _is_constant(form):
    """Whether the normal form has no variable left in it."""
    return all(name == "" for name in form)


@dataclass(frozen=True)
class Inequality:
    """A constraint of the form ``sum of coefficients * variables <= constant``."""

    coefficients: tuple
    constant: Fraction

    def as_dict(self):
        """The coefficients as a dictionary keyed by variable name."""
        return dict(self.coefficients)

    def __str__(self):
        """The inequality with its terms written out."""
        terms = " + ".join(f"{value}*{name}" for name, value in self.coefficients) or "0"
        return f"{terms} <= {self.constant}"


def to_inequalities(constraint):
    """Turn a conjunction of linear comparisons into inequalities, or None.

    Equalities become two inequalities, strict comparisons over the integers
    are tightened by one, and anything non-linear makes the whole conversion
    fail so the caller knows to use the search instead.
    """
    result = []

    for conjunct in _conjuncts(constraint):
        if isinstance(conjunct, Bool) and conjunct.value:
            continue
        if not isinstance(conjunct, BinOp) or conjunct.op not in ("<", "<=", ">", ">=", "="):
            return None

        left = linear_form(conjunct.left)
        right = linear_form(conjunct.right)
        if left is None or right is None:
            return None

        difference = dict(left)
        for name, value in right.items():
            difference[name] = difference.get(name, Fraction(0)) - value

        constant = -difference.pop("", Fraction(0))
        coefficients = tuple(sorted((name, value) for name, value in difference.items() if value))

        if conjunct.op == "<=":
            result.append(Inequality(coefficients, constant))
        elif conjunct.op == "<":
            result.append(Inequality(coefficients, constant - 1))
        elif conjunct.op == ">=":
            result.append(Inequality(tuple((n, -v) for n, v in coefficients), -constant))
        elif conjunct.op == ">":
            result.append(Inequality(tuple((n, -v) for n, v in coefficients), -constant - 1))
        else:
            result.append(Inequality(coefficients, constant))
            result.append(Inequality(tuple((n, -v) for n, v in coefficients), -constant))

    return result


def fourier_motzkin(inequalities, trace=None):
    """Decide a conjunction of linear inequalities over the rationals.

    Pick a variable, split the inequalities into those that bound it from
    above and from below, and replace every pair by the combined bound with
    the variable gone. Repeat until no variables are left, then check the
    constant inequalities.

    Complete for the rationals, and that is the catch: a system can be
    satisfiable over the rationals and have no integer solution, ``2x = 1``
    being the smallest example. Over the integers this is a sound test for
    unsatisfiability only, which is why the bounded search exists alongside it.

    The elimination can square the number of inequalities per variable, so the
    cost is doubly exponential in the worst case. It is a decision procedure,
    not a practical solver, and it is here because it is the one that can be
    read.
    """
    current = list(inequalities)
    names = sorted({name for inequality in current for name, _ in inequality.coefficients})

    for name in names:
        lower, upper, unrelated = [], [], []

        for inequality in current:
            coefficient = inequality.as_dict().get(name, Fraction(0))
            if coefficient > 0:
                upper.append(inequality)
            elif coefficient < 0:
                lower.append(inequality)
            else:
                unrelated.append(inequality)

        combined = list(unrelated)
        for low in lower:
            for high in upper:
                combined.append(_combine(low, high, name))

        if trace is not None:
            trace.append((name, len(current), len(combined)))
        current = combined

    for inequality in current:
        if inequality.constant < 0:
            return False
    return True


def _combine(lower, upper, name):
    """Eliminate one variable from a pair of opposing bounds."""
    low = lower.as_dict()
    high = upper.as_dict()
    scale_low = high[name]
    scale_high = -low[name]

    merged = {}
    for key in set(low) | set(high):
        value = scale_low * low.get(key, Fraction(0)) + scale_high * high.get(key, Fraction(0))
        if value and key != name:
            merged[key] = value

    constant = scale_low * lower.constant + scale_high * upper.constant
    return Inequality(tuple(sorted(merged.items())), constant)


def rationally_satisfiable(constraint, trace=None):
    """Decide a linear constraint over the rationals, or return None if non-linear."""
    inequalities = to_inequalities(constraint)
    if inequalities is None:
        return None
    return fourier_motzkin(inequalities, trace)
