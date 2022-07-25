"""A coding standard as executable rules, each tied to a quality attribute.

The exercise asks for a definition of a coding standard and three concrete,
checkable rules, each linked to a quality attribute. A rule that cannot be
checked mechanically is a preference; a rule that can be is a standard, and
the difference is whether a build can fail on it.

Every rule here names the attribute it serves, because a rule without one is
a habit nobody can argue with or against.
"""

from __future__ import annotations

import ast
import pathlib
from dataclasses import dataclass

MINIMUM_NAME_LENGTH = 3
MAXIMUM_FUNCTION_LINES = 60
MAXIMUM_PARAMETERS = 5
MAXIMUM_NESTING = 4
MAXIMUM_COMPLEXITY = 15


@dataclass(frozen=True)
class Violation:
    """One breach of the standard: where, which rule, and which attribute suffers."""

    path: str
    line: int
    rule: str
    attribute: str
    message: str

    def __str__(self):
        """The violation in the usual file, line, rule form."""
        return f"{self.path}:{self.line} [{self.rule}/{self.attribute}] {self.message}"


def short_names(tree, path):
    """Names shorter than the minimum, serving **readability**.

    Loop counters are exempt: ``i`` in a three-line loop is clearer than
    ``index_of_current_element``, and a rule that cannot make that distinction
    gets switched off wholesale, which is worse than not having it.
    """
    found = []
    exempt = {"i", "j", "k", "n", "x", "y", "z", "_"}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if len(node.name) < MINIMUM_NAME_LENGTH and node.name not in exempt:
                found.append(Violation(path, node.lineno, "short-name", "readability",
                                       f"{node.name!r} is shorter than {MINIMUM_NAME_LENGTH}"))
    return found


def long_functions(tree, path):
    """Functions over the line limit, serving **maintainability**.

    Length is a proxy for how much has to be held in mind at once. It is a
    crude one, and it is the rule most likely to be gamed by splitting a
    function in the middle rather than at a seam.
    """
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1
            if length > MAXIMUM_FUNCTION_LINES:
                found.append(Violation(path, node.lineno, "long-function", "maintainability",
                                       f"{node.name} is {length} lines, limit {MAXIMUM_FUNCTION_LINES}"))
    return found


def many_parameters(tree, path):
    """Functions with too many parameters, serving **testability**.

    Each parameter multiplies the combinations a test has to cover, so the
    count is a direct measure of how hard the function is to exercise.
    """
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            count = len(node.args.args) + len(node.args.kwonlyargs)
            if node.args.args and node.args.args[0].arg in ("self", "cls"):
                count -= 1
            if count > MAXIMUM_PARAMETERS:
                found.append(Violation(path, node.lineno, "many-parameters", "testability",
                                       f"{node.name} takes {count}, limit {MAXIMUM_PARAMETERS}"))
    return found


def deep_nesting(tree, path):
    """Control structures nested too deeply, serving **readability**."""
    found = []
    kinds = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith)

    def walk(node, depth, owner):
        """Reports nesting deeper than the limit, per function."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            owner = node
            depth = 0
        for child in ast.iter_child_nodes(node):
            step = depth + (1 if isinstance(child, kinds) else 0)
            if step > MAXIMUM_NESTING and isinstance(child, kinds):
                name = owner.name if owner else "<module>"
                found.append(Violation(path, child.lineno, "deep-nesting", "readability",
                                       f"{name} nests {step} deep, limit {MAXIMUM_NESTING}"))
                return
            walk(child, step, owner)

    walk(tree, 0, None)
    return found


def missing_docstrings(tree, path):
    """Public definitions without documentation, serving **understandability**.

    Private names are exempt: the standard asks for an interface to be
    described, not for every helper to be narrated.
    """
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_") and not ast.get_docstring(node):
                found.append(Violation(path, node.lineno, "missing-docstring",
                                       "understandability",
                                       f"{node.name} has no docstring"))
    return found


def bare_excepts(tree, path):
    """Exception handlers that catch everything, serving **reliability**.

    A bare ``except`` swallows the errors the author never thought about,
    including the ones that mean the program is already broken. It is the
    single most reliable way to turn a crash into silent wrong behaviour.
    """
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            found.append(Violation(path, node.lineno, "bare-except", "reliability",
                                   "catches everything, including bugs"))
    return found


def high_complexity(tree, path):
    """Functions over the complexity limit, serving **testability**.

    Cyclomatic complexity is a lower bound on the tests needed for branch
    coverage, so the limit is a statement about how much testing the team is
    prepared to write for one function.
    """
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "size-metrics"))
    from size_metrics import cyclomatic_complexity

    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            value = cyclomatic_complexity(node)
            if value > MAXIMUM_COMPLEXITY:
                found.append(Violation(path, node.lineno, "high-complexity", "testability",
                                       f"{node.name} scores {value}, limit {MAXIMUM_COMPLEXITY}"))
    return found


RULES = (short_names, long_functions, many_parameters, deep_nesting,
         missing_docstrings, bare_excepts, high_complexity)


def check_source(source, path="<string>", rules=RULES):
    """Run every rule over one source string."""
    tree = ast.parse(source)
    found = []
    for rule in rules:
        found.extend(rule(tree, str(path)))
    return sorted(found, key=lambda violation: (violation.path, violation.line))


def check_tree(root, rules=RULES, pattern="*.py"):
    """Run every rule over every matching file under a directory."""
    found = []
    for path in sorted(pathlib.Path(root).rglob(pattern)):
        found.extend(check_source(path.read_text(), path, rules))
    return found


def summary(violations):
    """How many violations per rule, worst first."""
    counts = {}
    for violation in violations:
        counts[violation.rule] = counts.get(violation.rule, 0) + 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))
