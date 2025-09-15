"""Live variable analysis on a control flow graph.

A variable is **live** at a program point when some path from there uses its
current value before overwriting it. Nothing else is a definition of liveness,
and everything else follows from it: dead code elimination, register
allocation, and the check that a variable is initialised before use.

The analysis is backwards, because liveness looks at what happens after a
point, and it takes unions at joins, because a variable live on any outgoing
path is live. In the standard framework that makes it a **may** analysis run in
reverse.

Statements sit on the edges of the graph here, as they do on the exercise
sheets, rather than inside the nodes. The transfer function of an edge is

    f(X) = (X \\ kill) union gen

and the order of the two operations is not negotiable: an assignment `y = y + b`
both uses and kills `y`, and killing first would lose the use.
"""

from __future__ import annotations


class Graph:
    """A control flow graph with statements on the edges."""

    def __init__(self, edges, entry, exit_node):
        """Store the labelled edges and the entry and exit nodes."""
        self.edges = [(source, target, statement) for source, target, statement in edges]
        self.entry = entry
        self.exit = exit_node
        self.nodes = ({source for source, _, _ in self.edges}
                      | {target for _, target, _ in self.edges}
                      | {entry, exit_node})

    def variables(self):
        """Every variable the program mentions."""
        names = set()
        for _, _, statement in self.edges:
            defined, used = parse_statement(statement)
            names |= used
            if defined:
                names.add(defined)
        return names

    def successors(self, node):
        """Edges leaving a node."""
        return [(target, statement) for source, target, statement in self.edges
                if source == node]

    def predecessors(self, node):
        """Edges entering a node."""
        return [(source, statement) for source, target, statement in self.edges
                if target == node]

    def without(self, edge):
        """The same graph with one edge's statement replaced by a no-operation.

        Removing a dead assignment must not remove the edge, or the control
        flow changes. The statement becomes a skip and the shape stays.
        """
        source, target = edge
        return Graph([(a, b, "skip" if (a, b) == (source, target) else statement)
                      for a, b, statement in self.edges], self.entry, self.exit)


def parse_statement(statement):
    """Split a statement into what it defines and what it uses.

    An assignment `x = a + b` defines `x` and uses `a` and `b`. A condition
    defines nothing and uses everything it mentions. `skip` does neither.
    """
    text = statement.strip()

    if text in ("skip", ""):
        return None, set()

    if "=" in text and not any(operator in text for operator in ("==", "!=", "<=", ">=")):
        target, expression = text.split("=", 1)
        return target.strip(), _names(expression)

    return None, _names(text)


def _names(expression):
    """The variable names in an expression."""
    names = set()
    current = ""

    for character in expression:
        if character.isalpha():
            current += character
        else:
            if current:
                names.add(current)
            current = ""

    if current:
        names.add(current)
    return names


def transfer(statement, live, wrong_order=False):
    """Apply one edge's transfer function to a set of live variables.

    The correct form removes the killed variable first and then adds the used
    ones, so a statement that both uses and kills a variable keeps it live.
    `wrong_order` implements the mistake the sheet asks about, adding first and
    removing afterwards, which loses exactly that case.
    """
    defined, used = parse_statement(statement)
    kill = {defined} if defined else set()

    if wrong_order:
        return (set(live) | used) - kill
    return (set(live) - kill) | used


def live_variables(graph, wrong_order=False, live_at_exit=None):
    """Live variables at every node, as a backwards least fixed point.

    A node's set is the union over its outgoing edges of the transfer function
    applied to the successor's set. Iterating until nothing changes gives the
    least solution.

    The boundary condition is a choice, and it changes the answer. Starting the
    exit node with the empty set means the final values of all variables are
    dead, so the last assignment to every variable is removable. Starting it
    with **every** variable means the final state is observable, which is the
    exercise sheet's convention and the safe one for a procedure whose
    variables outlive it.

    On the sheet's graph the difference is concrete: with an empty exit,
    `x = 2y-1`, `a = 0` and `b = 0` all become dead alongside `x = a+b`; with a
    full exit only `x = a+b` is, which is the published answer.
    """
    if live_at_exit is None:
        live_at_exit = graph.variables()

    live = {node: set() for node in graph.nodes}
    live[graph.exit] = set(live_at_exit)
    changed = True

    while changed:
        changed = False
        for node in sorted(graph.nodes, reverse=True):
            if node == graph.exit:
                continue
            union = set()
            for target, statement in graph.successors(node):
                union |= transfer(statement, live[target], wrong_order)
            if union != live[node]:
                live[node] = union
                changed = True

    return live


def dead_assignments(graph, live=None):
    """Assignments whose target is not live at the edge's target node.

    That is the definition of a dead assignment: the value it computes is
    never read. Conditions are never dead, since they steer the control flow
    whatever their value is used for.
    """
    live = live if live is not None else live_variables(graph)

    found = []

    for source, target, statement in graph.edges:
        defined, _ = parse_statement(statement)
        if defined is not None and defined not in live[target]:
            found.append(((source, target), statement))

    return found


def live_on_path(graph, node, variable, limit=40):
    """Whether a path from a node really uses a variable before overwriting it.

    The definition, checked by search rather than by the fixed point. It is
    what makes a claim about the analysis being wrong checkable: an analysis
    result that omits a variable this finds is unsound, not merely imprecise.
    """
    stack = [(node, 0)]
    seen = set()

    while stack:
        current, depth = stack.pop()
        if depth > limit:
            continue

        for target, statement in graph.successors(current):
            defined, used = parse_statement(statement)
            if variable in used:
                return True
            if defined == variable:
                continue
            key = (target, depth + 1)
            if key not in seen:
                seen.add(key)
                stack.append(key)

    return False


def unsound_points(graph, wrong_order=True):
    """Nodes where an analysis misses a variable that really is live.

    A live variable analysis is meant to over-approximate: reporting a variable
    live when it is not costs a register, reporting one dead when it is live
    breaks the program. This finds the second kind.
    """
    computed = live_variables(graph, wrong_order)

    found = []
    for node in sorted(graph.nodes):
        for variable in sorted(graph.variables()):
            if variable not in computed[node] and live_on_path(graph, node, variable):
                found.append((node, variable))

    return found
