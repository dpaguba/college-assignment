"""Coupling and cohesion, measured on a dependency graph.

The lecture defines both in words: coupling is how much a module has to know
about others, cohesion is how strongly its own responsibilities belong
together. The design rule that follows is to minimise the first and maximise
the second, and the lecture says plainly that the two often pull against each
other.

This module turns the words into numbers, using Robert Martin's package
metrics, because they are the ones that can be computed from imports alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DependencyGraph:
    """Modules and the modules each one depends on."""

    dependencies: dict = field(default_factory=dict)

    def modules(self):
        """Every module mentioned, as a dependant or as a dependency."""
        names = set(self.dependencies)
        for targets in self.dependencies.values():
            names |= set(targets)
        return sorted(names)

    def efferent(self, module):
        """Ce: how many modules this one depends on, outgoing coupling.

        The number of reasons this module can break when something else
        changes.
        """
        return len(self.dependencies.get(module, set()))

    def afferent(self, module):
        """Ca: how many modules depend on this one, incoming coupling.

        The number of modules that break when this one changes, which is what
        makes a widely used module expensive to modify.
        """
        return sum(1 for other, targets in self.dependencies.items()
                   if module in targets and other != module)

    def instability(self, module):
        """I = Ce / (Ca + Ce), between 0 and 1.

        Zero means nothing depends on this module's own dependencies: it is
        stable, hard to change, and everyone relies on it. One means it depends
        on everything and nobody depends on it, so it can be rewritten freely.

        Neither end is wrong. The rule is that dependencies should point from
        unstable modules towards stable ones, and a stable module that depends
        on an unstable one is the shape that hurts.
        """
        incoming = self.afferent(module)
        outgoing = self.efferent(module)
        total = incoming + outgoing
        return outgoing / total if total else 0.0

    def violations(self):
        """Dependencies that point from a stable module to a less stable one.

        Martin's stable dependencies principle, checked directly. Each pair
        returned is a place where a module that many others rely on has tied
        itself to something more likely to change.
        """
        found = []
        for module, targets in sorted(self.dependencies.items()):
            for target in sorted(targets):
                if self.instability(module) < self.instability(target):
                    found.append((module, target,
                                  round(self.instability(module), 2),
                                  round(self.instability(target), 2)))
        return found

    def cycles(self):
        """Dependency cycles, which make the modules in them one unit in practice.

        Two modules that depend on each other cannot be understood, tested or
        released separately, whatever the folder structure says. Found here by
        Tarjan's strongly connected components.
        """
        index_of = {}
        low = {}
        stack = []
        on_stack = set()
        found = []
        counter = [0]

        def walk(module):
            """Tarjan's search, collecting the strongly connected components."""
            index_of[module] = low[module] = counter[0]
            counter[0] += 1
            stack.append(module)
            on_stack.add(module)

            for target in sorted(self.dependencies.get(module, set())):
                if target not in index_of:
                    walk(target)
                    low[module] = min(low[module], low[target])
                elif target in on_stack:
                    low[module] = min(low[module], index_of[target])

            if low[module] == index_of[module]:
                component = []
                while True:
                    other = stack.pop()
                    on_stack.discard(other)
                    component.append(other)
                    if other == module:
                        break
                if len(component) > 1:
                    found.append(sorted(component))

        for module in self.modules():
            if module not in index_of:
                walk(module)

        return sorted(found)

    def report(self):
        """Ca, Ce and instability for every module."""
        rows = []
        for module in self.modules():
            rows.append({
                "module": module,
                "Ca": self.afferent(module),
                "Ce": self.efferent(module),
                "I": round(self.instability(module), 2),
            })
        return rows


def from_python_sources(root, package_prefixes=None):
    """Build a dependency graph from the imports in a directory of Python files.

    Only imports that resolve to another module in the same directory tree are
    counted, since a dependency on the standard library says nothing about the
    coupling of the code being measured.
    """
    import ast
    import pathlib

    root = pathlib.Path(root)
    files = sorted(root.rglob("*.py"))
    names = {path.stem for path in files}

    dependencies = {}
    for path in files:
        tree = ast.parse(path.read_text())
        targets = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    head = alias.name.split(".")[0]
                    if head in names and head != path.stem:
                        targets.add(head)
            elif isinstance(node, ast.ImportFrom) and node.module:
                head = node.module.split(".")[0]
                if head in names and head != path.stem:
                    targets.add(head)

        dependencies[path.stem] = targets

    return DependencyGraph(dependencies)
