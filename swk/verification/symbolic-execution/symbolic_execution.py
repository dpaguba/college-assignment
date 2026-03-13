"""Symbolic execution: run the program on symbols and collect path conditions.

The lecture gives the same seven rules as the concrete semantics, with two
changes. The state maps variables to **expressions over symbolic values**
instead of numbers, and every branch carries a **path condition**: the
conjunction of the tests taken to reach it.

    <skip, v, f> => (v, f)
    <x := a, v, f> => (v[x -> sigma(a, v)], f)
    <if b then S1 else S2, v, f> => <S1, v, f and b>   if satisfiable
    <if b then S1 else S2, v, f> => <S2, v, f and !b>  if satisfiable

Both branch rules can apply, and that is the point: execution becomes a tree
rather than a path. A branch whose path condition is unsatisfiable is dropped,
which is how the technique avoids exploring impossible code, and solving a
path condition gives concrete inputs that reach that leaf, which is how it
generates tests.

Loops are the limit. Each iteration is another unrolling, so a loop with an
unbounded trip count has infinitely many paths, and the depth bound here is
what makes the search finite.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-analysis" / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "linear-arithmetic"))

import linear_arithmetic as arithmetic
from while_language import (Assign, BinOp, Bool, If, Not, Num, Seq, Skip, Var,
                            While, blocks, parse)


def symbolic_state(names, prefix=""):
    """Give every variable a fresh symbol of its own, which is the initial state."""
    return {name: Var(f"{prefix}{name.upper()}") for name in sorted(names)}


def evaluate(expression, state):
    """Substitute the symbolic state into an expression.

    This is the lecture's ``sigma[a, v]``: replace each variable by whatever
    expression the state currently binds it to. Nothing is computed, because
    the values are symbols.
    """
    if isinstance(expression, Var):
        return state.get(expression.name, expression)
    if isinstance(expression, (Num, Bool)):
        return expression
    if isinstance(expression, Not):
        return Not(evaluate(expression.operand, state))
    if isinstance(expression, BinOp):
        return BinOp(expression.op,
                     evaluate(expression.left, state),
                     evaluate(expression.right, state))
    raise TypeError(f"cannot evaluate {expression!r} symbolically")


@dataclass
class Path:
    """One leaf of the execution tree: the final state, its condition, and the labels."""

    state: dict
    condition: object
    visited: tuple
    complete: bool = True

    def inputs(self, domains=None, low=None, high=None):
        """Concrete values for the symbols that drive execution down this path.

        This is test generation: the model of the path condition is an input
        that provably reaches this leaf. A path that no input can reach has an
        unsatisfiable condition and never becomes a leaf in the first place.

        When no domain is given, one is derived from the constants in the
        condition, so a test like ``x + 100 > 200`` is searched over a range
        that can actually contain the answer.
        """
        names = sorted(self.condition.variables())
        domains = domains or default_domains(self.condition, low, high)
        return arithmetic.search(self.condition, domains)

    def __str__(self):
        """The path, its labels and the values that reach the end of it."""
        values = ", ".join(f"{name} = {value}" for name, value in sorted(self.state.items()))
        return (f"labels {list(self.visited)}"
                f"{'' if self.complete else ' (cut off)'}\n"
                f"    condition: {self.condition}\n"
                f"    state:     {values}")


def execute(program, depth=8, low=None, high=None, prune=True):
    """Explore the execution tree and return one Path per leaf.

    ``depth`` bounds how many times a loop may be unrolled. A path that hits
    the bound is returned with ``complete`` false rather than dropped, so the
    caller can tell "no more behaviour" from "we stopped looking".

    ``prune`` decides whether unsatisfiable branches are discarded. Turning it
    off shows how much work the solver saves: the tree without pruning contains
    every syntactic path, including the ones that contradict themselves.
    """
    if isinstance(program, str):
        program = parse(program)

    names = set()
    for block in blocks(program).values():
        names |= set(block.variables())

    start = symbolic_state(names)
    paths = []
    _walk(program, start, Bool(True), (), depth, paths, low, high, prune)
    return paths


def _walk(statement, state, condition, visited, budget, paths, low, high, prune):
    """Follows both branches, recording the path condition of each."""
    if statement is None:
        paths.append(Path(dict(state), condition, visited))
        return

    if isinstance(statement, Skip):
        _walk(None, state, condition, visited + (statement.label,), budget, paths,
              low, high, prune)
        return

    if isinstance(statement, Assign):
        updated = {**state, statement.variable: evaluate(statement.expression, state)}
        _walk(None, updated, condition, visited + (statement.label,), budget, paths,
              low, high, prune)
        return

    if isinstance(statement, Seq):
        _walk_sequence(statement.first, statement.second, state, condition, visited,
                       budget, paths, low, high, prune)
        return

    if isinstance(statement, If):
        test = evaluate(statement.condition, state)
        for branch, guard in ((statement.then_branch, test),
                              (statement.else_branch, Not(test))):
            extended = BinOp("&&", condition, guard)
            if not prune or _feasible(extended, low, high):
                _walk(branch, state, extended, visited + (statement.label,), budget,
                      paths, low, high, prune)
        return

    if isinstance(statement, While):
        test = evaluate(statement.condition, state)

        exit_condition = BinOp("&&", condition, Not(test))
        if not prune or _feasible(exit_condition, low, high):
            _walk(None, state, exit_condition, visited + (statement.label,), budget,
                  paths, low, high, prune)

        enter_condition = BinOp("&&", condition, test)
        if budget <= 0:
            if not prune or _feasible(enter_condition, low, high):
                paths.append(Path(dict(state), enter_condition,
                                  visited + (statement.label,), complete=False))
            return

        if not prune or _feasible(enter_condition, low, high):
            _walk_sequence(statement.body, statement, state, enter_condition,
                           visited + (statement.label,), budget - 1, paths,
                           low, high, prune)
        return

    raise TypeError(f"not a While statement: {statement!r}")


def _walk_sequence(first, second, state, condition, visited, budget, paths,
                   low, high, prune):
    """Run the first statement, then continue with the second from each of its leaves."""
    intermediate = []
    _walk(first, state, condition, visited, budget, paths_or_collect(intermediate),
          low, high, prune)

    for path in intermediate:
        if not path.complete:
            paths.append(path)
            continue
        _walk(second, path.state, path.condition, path.visited, budget, paths,
              low, high, prune)


def paths_or_collect(target):
    """Adapter so a sub-walk collects into a list instead of the final result."""
    return target


def default_domains(condition, low=None, high=None):
    """Bounds wide enough to hold the constants the condition mentions.

    A fixed window is the wrong default: ``x + 100 > 200`` has no solution in
    [-32, 32] and plenty outside it, and a pruning step that used the narrow
    window would drop a reachable path and call it impossible.
    """
    if low is not None and high is not None:
        bounds = arithmetic.Domain(low, high)
        return {name: bounds for name in sorted(condition.variables())}

    largest = max((abs(node.value) for node in _constants(condition)), default=0)
    span = max(2 * largest + 10, 32)
    bounds = arithmetic.Domain(-span, span)
    return {name: bounds for name in sorted(condition.variables())}


def _constants(expression):
    """Every literal that occurs in the expression."""
    if isinstance(expression, Num):
        yield expression
    elif isinstance(expression, Not):
        yield from _constants(expression.operand)
    elif isinstance(expression, BinOp):
        yield from _constants(expression.left)
        yield from _constants(expression.right)


def _feasible(condition, low, high):
    """Whether a path condition can be satisfied at all.

    Linear conditions go to Fourier-Motzkin, which is exact over the rationals
    and needs no bounds. That is sound for pruning in the direction that
    matters: a condition with no rational solution has no integer solution
    either, so nothing reachable is ever discarded.

    The opposite direction can be imprecise. A condition satisfiable over the
    rationals but not over the integers, such as ``2x = 1``, survives pruning
    and shows up later as a path whose inputs cannot be generated.

    Anything non-linear falls back to the bounded integer search.
    """
    names = sorted(condition.variables())
    if not names:
        return bool(condition.evaluate({}))

    rational = arithmetic.rationally_satisfiable(condition)
    if rational is not None:
        return rational

    domains = (default_domains(condition, low, high) if low is not None
               else default_domains(condition))
    return arithmetic.search(condition, domains) is not None


def test_suite(program, depth=8, low=None, high=None):
    """Generate one concrete input per feasible path.

    The classical use of symbolic execution, and the reason tools like KLEE
    exist: the suite covers every path the search reached, by construction, and
    each input comes with the proof that it does.
    """
    suite = []
    for path in execute(program, depth, low, high):
        inputs = path.inputs(low=low, high=high)
        if inputs is not None:
            suite.append((inputs, path))
    return suite


def coverage(program, depth=8, low=None, high=None):
    """Which labels the generated suite reaches, and which it misses."""
    if isinstance(program, str):
        program = parse(program)

    reached = set()
    for _, path in test_suite(program, depth, low, high):
        reached |= set(path.visited)

    return reached, set(blocks(program)) - reached
