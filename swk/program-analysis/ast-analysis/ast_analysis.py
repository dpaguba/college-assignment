"""Static checks on the syntax tree, the cheapest kind of program analysis.

The lecture's example is a coding standard: find assignment nodes whose first
child is a variable with too short a name. That is the whole idea of AST-based
analysis, and it is what tools like PMD do at scale, matching patterns against
the tree with XPath.

Each rule here is a function from the program to a list of findings. Some rules
need the control flow graph rather than the tree alone, which is the point
where AST analysis stops being enough.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "while-language"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "control-flow-graph"))

from control_flow_graph import ControlFlowGraph
from while_language import (Assign, BinOp, Bool, If, Num, Seq, Skip, Var, While,
                            blocks, parse)

MINIMUM_NAME_LENGTH = 3


@dataclass(frozen=True)
class Finding:
    """One rule violation: which rule, which label, and what it says."""

    rule: str
    label: int
    message: str

    def __str__(self):
        """The finding with the label it applies to."""
        return f"[{self.label}] {self.rule}: {self.message}"


def short_names(program):
    """Variables assigned under a name shorter than the minimum.

    The rule from the lecture slide, and a good example of what an AST rule
    can and cannot do: it sees the shape of the tree, so it can tell an
    assignment target from a read, but it knows nothing about execution.
    """
    found = []
    for label, block in sorted(blocks(program).items()):
        if block.kind == "assign" and len(block.variable) < MINIMUM_NAME_LENGTH:
            found.append(Finding("short-name", label,
                                 f"variable {block.variable!r} is shorter than "
                                 f"{MINIMUM_NAME_LENGTH} characters"))
    return found


def self_assignments(program):
    """Assignments of a variable to itself, which cannot change anything."""
    found = []
    for label, block in sorted(blocks(program).items()):
        if (block.kind == "assign" and isinstance(block.expression, Var)
                and block.expression.name == block.variable):
            found.append(Finding("self-assignment", label,
                                 f"{block.variable} := {block.variable} has no effect"))
    return found


def constant_conditions(program):
    """Tests whose outcome is fixed, so one branch can never run.

    ``while [true]`` is a deliberate infinite loop and is reported all the
    same: the rule states what it sees, and a suppression comment is the usual
    way a standard handles the intentional case.
    """
    found = []
    for label, block in sorted(blocks(program).items()):
        if block.kind == "test" and isinstance(block.expression, Bool):
            found.append(Finding("constant-condition", label,
                                 f"the test is always {block.expression}"))
    return found


def division_by_zero(program):
    """Divisions by a literal zero, which no execution can survive."""
    found = []
    for label, block in sorted(blocks(program).items()):
        if block.expression is None:
            continue
        for expression in _walk(block.expression):
            if (isinstance(expression, BinOp) and expression.op in ("/", "%")
                    and isinstance(expression.right, Num) and expression.right.value == 0):
                found.append(Finding("division-by-zero", label,
                                     f"{expression} divides by zero"))
    return found


def never_read(program):
    """Variables that are assigned somewhere and read nowhere.

    A whole-program rule rather than a node pattern, and still purely
    syntactic: it does not need to know which paths run, only which names
    appear on the right of something.
    """
    written = {}
    read = set()

    for label, block in sorted(blocks(program).items()):
        if block.kind == "assign":
            written.setdefault(block.variable, []).append(label)
            read |= set(block.expression.variables())
        elif block.expression is not None:
            read |= set(block.expression.variables())

    found = []
    for name, labels_written in sorted(written.items()):
        if name not in read:
            for label in labels_written:
                found.append(Finding("never-read", label,
                                     f"{name} is assigned but never read"))
    return found


def unreachable_code(program):
    """Statements no execution can reach.

    This one needs the control flow graph: reachability is a property of the
    edges, not of the tree. In a While program it can only arise from a
    constant test, which is why the two rules usually fire together.
    """
    graph = ControlFlowGraph(program)
    return [Finding("unreachable", label, f"{graph.blocks[label]} cannot be reached")
            for label in sorted(graph.unreachable())]


def nesting_depth(program):
    """The deepest nesting of conditionals and loops, with the labels at that depth.

    Not a violation in itself, and one of the oldest complexity heuristics
    there is: deeply nested code is hard to follow no matter how few decisions
    it contains.
    """
    depths = {}
    _measure(program, 0, depths)
    deepest = max(depths.values(), default=0)
    return deepest, sorted(label for label, depth in depths.items() if depth == deepest)


def _measure(statement, depth, depths):
    """Records the nesting depth of every labelled statement."""
    if isinstance(statement, (Assign, Skip)):
        depths[statement.label] = depth
    elif isinstance(statement, Seq):
        _measure(statement.first, depth, depths)
        _measure(statement.second, depth, depths)
    elif isinstance(statement, If):
        depths[statement.label] = depth
        _measure(statement.then_branch, depth + 1, depths)
        _measure(statement.else_branch, depth + 1, depths)
    elif isinstance(statement, While):
        depths[statement.label] = depth
        _measure(statement.body, depth + 1, depths)


def _walk(expression):
    """Every subexpression of the expression, including itself."""
    yield expression
    if isinstance(expression, BinOp):
        yield from _walk(expression.left)
        yield from _walk(expression.right)


RULES = (short_names, self_assignments, constant_conditions, division_by_zero,
         never_read, unreachable_code)


def check(source, rules=RULES):
    """Run every rule and return the findings, sorted by label.

    A linter is exactly this: a list of rules, a tree, and a report. The
    difference between this and a production tool is the number of rules and
    the quality of the messages, not the idea.
    """
    program = parse(source) if isinstance(source, str) else source
    found = []
    for rule in rules:
        found.extend(rule(program))
    return sorted(found, key=lambda finding: (finding.label, finding.rule))
