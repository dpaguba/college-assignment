"""Shift-reduce parsing: the driver that runs an LR table.

Two actions and a stack of states. **Shift** pushes the next input symbol and
the state the automaton moves to. **Reduce** pops as many states as the rule
has symbols on its right side, then pushes the state reached from the exposed
one by the rule's left side. That is the whole parser; everything specific to
the grammar lives in the table.

Because it reduces innermost-leftmost handles as it scans left to right, the
sequence of reductions read backwards is a rightmost derivation. That is what
the R in LR names, and it is why a bottom-up parser handles left recursion
without difficulty while a top-down one cannot: the recursive symbol is
completed before it is ever needed.
"""

from __future__ import annotations

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "grammars"))
sys.path.insert(0, os.path.join(_here, "..", "first-follow"))
sys.path.insert(0, os.path.join(_here, "..", "lr-automata"))
import first_follow as ff
import grammars as gr
import lr_automata as lr


class ConflictError(Exception):
    """The table cannot be built because a cell would hold two actions."""

    def __init__(self, conflicts):
        """Summarise the conflicting cells in the message and keep the details."""
        kinds = ", ".join(sorted({conflict["kind"] for conflict in conflicts}))
        super().__init__(f"grammar is not LR(1): {kinds} in "
                         f"{len(conflicts)} cell(s)")
        self.conflicts = conflicts


def table(grammar, construction=lr.lr1_automaton):
    """The action and goto tables of an LR parser.

    Actions are `("shift", state)`, `("reduce", left, right)` and
    `("accept",)`. Building the table is where a grammar is accepted or
    rejected as LR: a conflict is not a parse error but a statement that no
    deterministic parser of this class exists for this grammar.
    """
    automaton = construction(grammar)
    found = lr.conflicts(automaton, grammar)
    if found:
        raise ConflictError(found)

    augmented = lr.augment(grammar)
    actions = {}
    gotos = {}

    for number in range(len(automaton.states)):
        for (state, symbol), target in automaton.transitions.items():
            if state != number:
                continue
            if symbol in augmented.nonterminals:
                gotos[(number, symbol)] = target
            else:
                actions[(number, symbol)] = ("shift", target)

        for left, dot, right, lookahead in automaton.states[number]:
            if dot < len(right):
                continue
            if left == augmented.start:
                actions[(number, lr.END)] = ("accept",)
            else:
                actions[(number, lookahead)] = ("reduce", left, list(right))

    return actions, gotos


def trace(grammar, word, construction=lr.lr1_automaton):
    """Run the parser, recording the state stack, input and action per step.

    The configuration format follows the lecture: the stack of states on the
    left, the remaining input on the right, and the action that is about to be
    taken. A reduction is recorded before it happens, which is why the stack
    shrinks in the following row rather than in this one.
    """
    actions, gotos = table(grammar, construction)
    stack = [0]
    position = 0
    steps = []

    while True:
        lookahead = word[position] if position < len(word) else lr.END
        action = actions.get((stack[-1], lookahead))

        if action is None:
            steps.append({"stack": list(stack), "input": list(word[position:]),
                          "action": f"error on {lookahead}"})
            return steps

        if action[0] == "accept":
            steps.append({"stack": list(stack), "input": list(word[position:]),
                          "action": "accept"})
            return steps

        if action[0] == "shift":
            steps.append({"stack": list(stack), "input": list(word[position:]),
                          "action": f"shift {lookahead}"})
            stack.append(action[1])
            position += 1
            continue

        _, left, right = action
        shown = " ".join(right) if right else ff.EPSILON
        steps.append({"stack": list(stack), "input": list(word[position:]),
                      "action": f"reduce {left} ::= {shown}"})
        for _ in right:
            stack.pop()
        stack.append(gotos[(stack[-1], left)])


def accepts(grammar, word, construction=lr.lr1_automaton):
    """Whether the parser reaches the accept action."""
    steps = trace(grammar, word, construction)
    return steps[-1]["action"] == "accept"


def parse(grammar, word, construction=lr.lr1_automaton):
    """Build the parse tree, keeping a stack of subtrees beside the states.

    Each reduction pops as many subtrees as the rule is long and makes them the
    children of a new node. The tree is therefore built bottom up, leaves
    first, which is the mirror image of what the predictive parser in
    [ll1-parser](../ll1-parser/) does.
    """
    actions, gotos = table(grammar, construction)
    stack = [0]
    trees = []
    position = 0

    while True:
        lookahead = word[position] if position < len(word) else lr.END
        action = actions.get((stack[-1], lookahead))

        if action is None:
            raise ValueError(f"parse error at position {position} on {lookahead}")

        if action[0] == "accept":
            return trees[-1]

        if action[0] == "shift":
            stack.append(action[1])
            trees.append(gr.Node(lookahead))
            position += 1
            continue

        _, left, right = action
        children = []
        for _ in right:
            stack.pop()
            children.insert(0, trees.pop())
        trees.append(gr.Node(left, children if children else [gr.Node(gr.EMPTY)]))
        stack.append(gotos[(stack[-1], left)])


def report(grammar, construction=lr.lr1_automaton):
    """The action and goto tables as rows, in the layout the sheets print."""
    actions, gotos = table(grammar, construction)
    terminals = sorted({symbol for _, symbol in actions})
    nonterminals = sorted({symbol for _, symbol in gotos})
    states = sorted({state for state, _ in actions} | {state for state, _ in gotos})

    rows = []
    for state in states:
        row = {"state": state}
        for symbol in terminals:
            action = actions.get((state, symbol))
            if action is None:
                continue
            if action[0] == "shift":
                row[symbol] = f"s{action[1]}"
            elif action[0] == "accept":
                row[symbol] = "acc"
            else:
                row[symbol] = f"r {action[1]} ::= {' '.join(action[2]) or ff.EPSILON}"
        for symbol in nonterminals:
            if (state, symbol) in gotos:
                row[symbol] = gotos[(state, symbol)]
        rows.append(row)

    return terminals, nonterminals, rows
