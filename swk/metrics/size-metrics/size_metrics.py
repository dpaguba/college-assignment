"""Size metrics: the simplest indicators, and what they are worth.

The lecture starts the metrics section with lines of code, calls it the
simplest indicator of complexity, and immediately lists its relatives: number
of classes, number of methods, number of anything.

They are worth having because they are free and comparable over time. They are
worth distrusting because they measure typing, not difficulty: the same
function written in two styles differs by a factor of two in lines and not at
all in what it does.
"""

from __future__ import annotations

import ast
import pathlib
from dataclasses import dataclass


@dataclass
class FileMetrics:
    """Counts for one source file."""

    path: str
    lines: int
    code: int
    blank: int
    comment: int
    docstring: int
    functions: int
    classes: int
    longest_function: int
    max_nesting: int

    @property
    def comment_ratio(self):
        """Share of documentation among the non-blank lines.

        A ratio, not a count, because the count grows with the file and says
        nothing on its own. Very low means undocumented; very high often means
        the code is explaining itself badly and the prose is compensating.
        """
        meaningful = self.code + self.comment + self.docstring
        return (self.comment + self.docstring) / meaningful if meaningful else 0.0

    def __str__(self):
        """The row this file contributes to the report."""
        return (f"{self.path}: {self.lines} lines, {self.code} code, "
                f"{self.functions} functions, longest {self.longest_function}, "
                f"nesting {self.max_nesting}, documented {self.comment_ratio:.0%}")


def measure_source(source, path="<string>"):
    """Count lines, definitions and nesting in one Python source string."""
    lines = source.split("\n")
    tree = ast.parse(source)

    docstring_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                docstring_lines.update(range(node.body[0].lineno, node.body[0].end_lineno + 1))

    blank = comment = code = 0
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if number in docstring_lines:
            continue
        if not stripped:
            blank += 1
        elif stripped.startswith("#"):
            comment += 1
        else:
            code += 1

    functions = [node for node in ast.walk(tree)
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    longest = max((node.end_lineno - node.lineno + 1 for node in functions), default=0)

    return FileMetrics(
        path=str(path),
        lines=len(lines),
        code=code,
        blank=blank,
        comment=comment,
        docstring=len(docstring_lines),
        functions=len(functions),
        classes=len(classes),
        longest_function=longest,
        max_nesting=nesting_depth(tree),
    )


def measure_file(path):
    """Count everything in one file on disk."""
    path = pathlib.Path(path)
    return measure_source(path.read_text(), path)


def measure_tree(root, pattern="*.py"):
    """Count every matching file under a directory."""
    return [measure_file(path) for path in sorted(pathlib.Path(root).rglob(pattern))]


def nesting_depth(tree):
    """The deepest nesting of control structures in a syntax tree.

    Counted over conditionals, loops, exception handlers and context managers.
    It is a better complexity signal than length, and it is the one that
    matches how code actually feels to read: three levels are followable, six
    are not.
    """
    nesting_kinds = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With,
                     ast.AsyncWith)

    def depth(node, current):
        """The deepest nesting inside this node."""
        deepest = current
        for child in ast.iter_child_nodes(node):
            step = 1 if isinstance(child, nesting_kinds) else 0
            deepest = max(deepest, depth(child, current + step))
        return deepest

    return depth(tree, 0)


def cyclomatic_complexity(node):
    """McCabe's measure for a Python function, counted from decision points.

    One plus the number of branch points: conditionals, loops, exception
    handlers, boolean operators and comprehension filters. On a control flow
    graph this equals ``e - n + 2p``, which is how the
    [program analysis](../../program-analysis/cyclomatic-complexity/) folder
    computes it for the While language. Counting decisions is the same number
    reached without building the graph.
    """
    decisions = 0

    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While,
                              ast.ExceptHandler, ast.Assert)):
            decisions += 1
        elif isinstance(child, ast.BoolOp):
            decisions += len(child.values) - 1
        elif isinstance(child, ast.IfExp):
            decisions += 1
        elif isinstance(child, comprehension_types):
            decisions += len(child.generators) + sum(len(gen.ifs) for gen in child.generators)

    return decisions + 1


comprehension_types = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def complexity_per_function(source):
    """The cyclomatic complexity of every function in a source string."""
    tree = ast.parse(source)
    return {node.name: cyclomatic_complexity(node)
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def summarise(measurements):
    """Totals and averages across a set of files."""
    if not measurements:
        return {}

    return {
        "files": len(measurements),
        "lines": sum(item.lines for item in measurements),
        "code": sum(item.code for item in measurements),
        "documentation": sum(item.comment + item.docstring for item in measurements),
        "functions": sum(item.functions for item in measurements),
        "classes": sum(item.classes for item in measurements),
        "longest function": max(item.longest_function for item in measurements),
        "deepest nesting": max(item.max_nesting for item in measurements),
        "documented share": round(
            sum(item.comment + item.docstring for item in measurements)
            / max(1, sum(item.code + item.comment + item.docstring for item in measurements)), 3),
    }
