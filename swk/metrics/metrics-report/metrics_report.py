"""One report over a real code base, joining the four measures.

The lecture's own motivation for this topic is a question: would it not be
good if coding standards and metrics could be checked automatically? This is
that check, run over the Python in this repository.

Nothing here is new. It extracts the class models LCOM needs from real
sources, runs the size, coupling and standards modules, and prints the result
as one table, which is what turns four separate numbers into something a team
can look at once a week.
"""

from __future__ import annotations

import ast
import pathlib
import sys
from dataclasses import dataclass

_HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_HERE / "lcom"))
sys.path.insert(0, str(_HERE / "size-metrics"))
sys.path.insert(0, str(_HERE / "coupling-and-cohesion"))
sys.path.insert(0, str(_HERE / "coding-standards"))

import coding_standards
from coupling_and_cohesion import from_python_sources
from lcom import ClassModel, lcom, lcom4
from size_metrics import complexity_per_function, measure_tree, summarise


def class_models(source, path="<string>"):
    """Extract a ClassModel per class, for LCOM.

    Fields are the ``self.x`` attributes the class touches, methods are its
    functions, and an access is a method mentioning a field. Properties and
    private helpers count like any other method: the metric asks which methods
    touch which data, and it does not care what they are called.
    """
    tree = ast.parse(source)
    models = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        methods = [child for child in node.body
                   if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))]
        accesses = {}
        fields = set()

        for method in methods:
            touched = set()
            for inner in ast.walk(method):
                if (isinstance(inner, ast.Attribute) and isinstance(inner.value, ast.Name)
                        and inner.value.id == "self"):
                    touched.add(inner.attr)
            accesses[method.name] = touched
            fields |= touched

        callable_fields = {name for name in fields
                           if name not in {method.name for method in methods}}

        if callable_fields and len(methods) > 1:
            models.append(ClassModel(f"{path}:{node.name}",
                                     tuple(sorted(callable_fields)), accesses))

    return models


@dataclass
class Report:
    """Everything measured for one directory."""

    root: str
    size: dict
    classes: list
    coupling: list
    cycles: list
    violations: list

    def worst_classes(self, count=5):
        """Classes with the least cohesion, worst first."""
        scored = [(model, lcom(model), lcom4(model)) for model in self.classes]
        scored = [item for item in scored if item[1] is not None]
        return sorted(scored, key=lambda item: -item[1])[:count]

    def worst_functions(self, count=5):
        """Functions with the highest cyclomatic complexity."""
        return self.complexity[:count]

    def __str__(self):
        """The whole report, one section per metric family."""
        lines = [f"metrics for {self.root}", ""]

        lines.append("size")
        for key, value in self.size.items():
            lines.append(f"  {key}: {value}")

        lines.append("")
        lines.append("cohesion, worst classes by LCOM")
        for model, value, groups in self.worst_classes():
            lines.append(f"  {float(value):.2f}  LCOM4={groups}  {model.name}")

        lines.append("")
        lines.append("coupling, most depended upon")
        for row in sorted(self.coupling, key=lambda row: -row["Ca"])[:5]:
            lines.append(f"  Ca={row['Ca']:2} Ce={row['Ce']:2} I={row['I']:.2f}  {row['module']}")
        lines.append(f"  dependency cycles: {self.cycles or 'none'}")

        lines.append("")
        lines.append("coding standard")
        for rule, count in coding_standards.summary(self.violations):
            lines.append(f"  {count:3}  {rule}")

        return "\n".join(lines)


def analyse(root):
    """Run every measure over a directory and return one report."""
    root = pathlib.Path(root)

    models = []
    complexity = []
    for path in sorted(root.rglob("*.py")):
        source = path.read_text()
        models.extend(class_models(source, path.name))
        for name, value in complexity_per_function(source).items():
            complexity.append((value, f"{path.parent.name}/{name}"))

    graph = from_python_sources(root)
    report = Report(
        root=str(root),
        size=summarise(measure_tree(root)),
        classes=models,
        coupling=graph.report(),
        cycles=graph.cycles(),
        violations=coding_standards.check_tree(root),
    )
    report.complexity = sorted(complexity, reverse=True)
    return report


def main(argv=None):
    """Print the report for a directory given on the command line."""
    argv = argv or sys.argv[1:]
    root = argv[0] if argv else "."
    print(analyse(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
