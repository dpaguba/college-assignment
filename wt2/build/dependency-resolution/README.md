# Dependency resolution

The graph of transitive dependencies usually contains the same artefact at
several versions. The rule that decides is nearest wins: the version fewest
steps from the root, and on a tie the one declared first.

That second half surprises people. With `app → a → c:2.0` and `app → b →
c:1.0`, both candidates sit at depth 2, and `a` is declared before `b`, so
**2.0** is chosen. Swapping the order of `a` and `b` in the project file
changes which version is built, without any other edit.

Declaring `c` directly puts it at depth 1 and settles the matter. That is the
usual fix for a version conflict, and the reason a project file often names
an artefact it never mentions in its own code.

The resolution is checked against an independently written breadth-first
search on 30 random graphs. A cycle in the graph does not hang the search.
