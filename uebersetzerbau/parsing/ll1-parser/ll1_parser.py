"""LL(1) parsing: one lookahead symbol, one stack, one table.

The parser reads left to right, produces a **L**eftmost derivation, and decides
each step from **1** symbol of lookahead. That is the whole of the name, and it
is also the whole of the algorithm: a stack of grammar symbols, and a table
saying which rule to apply for a nonterminal on top and a terminal ahead.

Everything interesting is in building the table. A rule `A ::= alpha` is
entered under every terminal that can begin `alpha`, and if `alpha` can vanish,
under every terminal that can follow `A`, since choosing a vanishing rule means
the decision is really about what comes after.

Two entries in one cell means the grammar is not LL(1). That is not a defect of
the parser; it says one lookahead symbol genuinely does not determine the rule.
"""

from __future__ import annotations

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "grammars"))
sys.path.insert(0, os.path.join(_here, "..", "first-follow"))
import first_follow as ff
import grammars as gr


def parse_table(grammar):
    """The LL(1) table, mapping a nonterminal and a lookahead to a right side.

    Conflicting cells are resolved by keeping the first rule, so that the table
    is still usable for tracing. `conflicts` reports what was dropped, and
    should be consulted before trusting a parse.
    """
    table = {}
    for nonterminal, lookahead, right in _entries(grammar):
        table.setdefault((nonterminal, lookahead), right)
    return table


def _entries(grammar):
    """Every table entry the construction produces, conflicts included."""
    first = ff.first_sets(grammar)
    follow = ff.follow_sets(grammar)

    for left, right in grammar.rules:
        starters = ff._first_of_sequence(grammar, right, first)
        for symbol in starters - {ff.EPSILON}:
            yield left, symbol, right
        if ff.EPSILON in starters:
            for symbol in follow[left]:
                yield left, symbol, right


def conflicts(grammar):
    """Cells that would hold more than one rule, as triples.

    An LL(1) grammar is exactly one with no such cell. The two classic causes
    are left recursion, where a rule's First set contains what the recursive
    call would also predict, and a common prefix, where two rules start alike
    and one symbol cannot tell them apart.
    """
    seen = {}
    found = []

    for nonterminal, lookahead, right in _entries(grammar):
        key = (nonterminal, lookahead)
        if key in seen and seen[key] != right:
            found.append((nonterminal, lookahead, [seen[key], right]))
        else:
            seen[key] = right

    return found


def trace(grammar, word):
    """Run the parser, recording stack, remaining input and action per step.

    The stack holds grammar symbols with the top on the left, which is the
    layout the lecture's tables use. Each step is either a rule application,
    which replaces the top nonterminal by its right side, or a match, which
    consumes one terminal from both stack and input.
    """
    table = parse_table(grammar)
    stack = [grammar.start]
    position = 0
    steps = []

    while stack:
        lookahead = word[position] if position < len(word) else ff.EPSILON
        top = stack[0]

        if top not in grammar.nonterminals:
            if top != lookahead:
                steps.append({"stack": list(stack), "input": list(word[position:]),
                              "action": f"error: expected {top}, found {lookahead}"})
                return steps
            steps.append({"stack": list(stack), "input": list(word[position:]),
                          "action": f"term({top})"})
            stack.pop(0)
            position += 1
            continue

        right = table.get((top, lookahead))
        if right is None:
            steps.append({"stack": list(stack), "input": list(word[position:]),
                          "action": f"error: no rule for {top} on {lookahead}"})
            return steps

        shown = " ".join(right) if right else ff.EPSILON
        steps.append({"stack": list(stack), "input": list(word[position:]),
                      "action": f"{top} ::= {shown}"})
        stack = list(right) + stack[1:]

    return steps


def accepts(grammar, word):
    """Whether the parser consumes the whole input and empties the stack."""
    steps = trace(grammar, word)
    if any(step["action"].startswith("error") for step in steps):
        return False

    consumed = sum(1 for step in steps if step["action"].startswith("term("))
    return consumed == len(word)


def parse(grammar, word):
    """Build the parse tree the run corresponds to.

    A predictive parser produces a leftmost derivation, and a leftmost
    derivation is a tree built top down and left to right. Keeping a parallel
    stack of tree nodes turns the recogniser into a parser at no extra cost,
    which is why LL parsers are written this way rather than reconstructing the
    tree afterwards.
    """
    table = parse_table(grammar)
    root = gr.Node(grammar.start)
    stack = [root]
    position = 0

    while stack:
        node = stack[0]
        lookahead = word[position] if position < len(word) else ff.EPSILON

        if node.symbol not in grammar.nonterminals:
            if node.symbol != lookahead:
                raise ValueError(f"expected {node.symbol}, found {lookahead}")
            stack.pop(0)
            position += 1
            continue

        right = table.get((node.symbol, lookahead))
        if right is None:
            raise ValueError(f"no rule for {node.symbol} on {lookahead}")

        children = [gr.Node(symbol) for symbol in right]
        node.children = children if children else [gr.Node(gr.EMPTY)]
        stack = children + stack[1:]

    if position != len(word):
        raise ValueError("input not fully consumed")

    return root


def report(grammar):
    """The table as rows, in the layout the exercise sheets print."""
    table = parse_table(grammar)
    columns = sorted({lookahead for _, lookahead in table})
    rows = []

    for nonterminal in sorted(grammar.nonterminals):
        row = {"nonterminal": nonterminal}
        for column in columns:
            right = table.get((nonterminal, column))
            if right is not None:
                row[column] = " ".join(right) if right else ff.EPSILON
        rows.append(row)

    return columns, rows
