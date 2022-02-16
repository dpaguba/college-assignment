"""First-order resolution and SLD resolution, which is Prolog.

Ground resolution works by instantiating everything first. Robinson's insight
was that instantiating can be **postponed**: resolve two clauses whenever their
literals can be unified, and let the most general unifier decide how much to
instantiate. The result is complete and enormously more efficient, because it
never builds instances that no proof needs.

SLD resolution is that rule restricted to Horn clauses with a fixed selection
strategy, and it is a programming language: a set of definite clauses is a
program, a negative clause is a query, and the substitution accumulated along a
refutation is the answer.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "unification"))
import unification as uni


def rename(clause, index):
    """Rename a clause's variables apart from every other clause.

    Two clauses that happen to use the same variable name are not talking about
    the same thing, and resolving them without renaming derives nonsense. The
    step is invisible in a written proof, which is why it is the most common
    mistake in one.
    """
    mapping = {}
    renamed = []

    for name, arguments in clause:
        new_arguments = []
        for argument in arguments:
            new_arguments.append(_rename_term(argument, mapping, index))
        renamed.append((name, new_arguments))

    return renamed


def _rename_term(term, mapping, index):
    """Append an index to every variable in a textual term."""
    result = ""
    current = ""

    for character in term + " ":
        if character.isalnum() or character == "_":
            current += character
        else:
            if len(current) == 1 and current in "uvwxyz":
                mapping.setdefault(current, f"{current}{index}")
                result += mapping[current]
            else:
                result += current
            result += character
            current = ""

    return result[:-1]


def _negate(name):
    """The complement of a predicate name."""
    return name[1:] if name.startswith("!") else "!" + name


def refute(clauses, limit=200):
    """Derive the empty clause by resolution with unification, or `None`.

    Each step picks two clauses, renames them apart, finds a pair of
    complementary literals whose arguments unify, and adds the resolvent with
    the unifier applied. The search is breadth first over pairs, which is
    complete but not efficient; real provers add ordering and subsumption.
    """
    known = [rename(clause, index) for index, clause in enumerate(clauses)]
    seen = {_key(clause) for clause in known}

    for _ in range(limit):
        added = False

        for i in range(len(known)):
            for j in range(len(known)):
                if i == j:
                    continue

                left = rename(known[i], 1000 + i)
                right = rename(known[j], 2000 + j)

                for name, arguments in left:
                    for other_name, other_arguments in right:
                        if other_name != _negate(name):
                            continue
                        if len(arguments) != len(other_arguments):
                            continue

                        substitution = _unify_all(arguments, other_arguments)
                        if substitution is None:
                            continue

                        resolvent = _apply_clause(
                            [literal for literal in left
                             if literal != (name, arguments)]
                            + [literal for literal in right
                               if literal != (other_name, other_arguments)],
                            substitution)

                        if not resolvent:
                            return known + [resolvent]

                        key = _key(resolvent)
                        if key not in seen:
                            seen.add(key)
                            known.append(resolvent)
                            added = True

        if not added:
            return None

    return None


def _unify_all(first, second):
    """Unify two argument lists, or `None`."""
    substitution = {}

    for left, right in zip(first, second):
        step = uni.unify(uni.to_text(uni.apply(substitution, left)),
                         uni.to_text(uni.apply(substitution, right)))
        if step is None:
            return None
        substitution = uni.compose(substitution, step)

    return substitution


def _apply_clause(clause, substitution):
    """Apply a substitution to every literal of a clause."""
    return [(name, [uni.to_text(uni.apply(substitution, argument))
                    for argument in arguments])
            for name, arguments in clause]


def _key(clause):
    """A hashable form of a clause, for the seen set."""
    return frozenset((name, tuple(arguments)) for name, arguments in clause)


class Program:
    """A Prolog program: definite clauses with a head and a body.

    Variables are written with a leading capital, as Prolog does, and constants
    in lower case. That convention is the opposite of the lecture's for
    first-order terms, and keeping both makes the difference visible rather
    than hiding it behind a shared helper.
    """

    def __init__(self, clauses):
        """Store the clauses in the order they were written.

        The order matters: SLD resolution tries them top to bottom, so a
        program is not a set of logical statements but a sequence of them, and
        swapping two clauses can turn a terminating program into a
        non-terminating one.
        """
        self.clauses = list(clauses)

    def solve(self, query, depth=10):
        """Every answer substitution for a query, by SLD resolution."""
        answers = []
        variables = _query_variables(query)

        for substitution in self._solve([query], {}, depth, [0]):
            answer = {name: _apply_prolog(substitution, name) for name in variables}
            if answer not in answers:
                answers.append(answer)

        return answers

    def _solve(self, goals, substitution, depth, counter):
        """Resolve the goal list against the program, depth first."""
        if not goals:
            yield substitution
            return

        if depth <= 0:
            return

        goal, rest = goals[0], goals[1:]
        goal = (goal[0], [_apply_prolog(substitution, argument) for argument in goal[1]])

        for head_name, head_arguments, body in self.clauses:
            if head_name != goal[0] or len(head_arguments) != len(goal[1]):
                continue

            counter[0] += 1
            index = counter[0]
            renamed_head = [_rename_prolog(argument, index) for argument in head_arguments]
            renamed_body = [(name, [_rename_prolog(argument, index)
                                    for argument in arguments])
                            for name, arguments in body]

            unifier = _unify_prolog(goal[1], renamed_head)
            if unifier is None:
                continue

            merged = dict(substitution)
            merged.update(unifier)
            yield from self._solve(renamed_body + rest, merged, depth - 1, counter)


def _query_variables(query):
    """The variables of a query, by the Prolog convention."""
    return [argument for argument in query[1]
            if argument and argument[0].isupper()]


def _rename_prolog(term, index):
    """Give a clause's variables a fresh suffix."""
    if term and term[0].isupper():
        return f"{term}_{index}"
    return term


def _unify_prolog(first, second):
    """Unify two argument lists under the Prolog naming convention."""
    substitution = {}

    for left, right in zip(first, second):
        left = _apply_prolog(substitution, left)
        right = _apply_prolog(substitution, right)

        if left == right:
            continue
        if left and left[0].isupper():
            substitution[left] = right
        elif right and right[0].isupper():
            substitution[right] = left
        else:
            return None

    return substitution


def _apply_prolog(substitution, term):
    """Follow the substitution until the term is not a bound variable."""
    seen = set()
    while term in substitution and term not in seen:
        seen.add(term)
        term = substitution[term]
    return term
