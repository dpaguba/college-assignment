"""Konfliktserialisierbarkeit über den Konfliktgraphen."""


def _conflicting(first, second):
    """Sagt, ob zwei Operationen verschiedener Transaktionen kollidieren.

    Zwei Operationen stehen im Konflikt, wenn sie dasselbe Datum
    betreffen, zu verschiedenen Transaktionen gehören und mindestens eine
    von ihnen schreibt.
    """
    transaction, operation, item = first
    other_transaction, other_operation, other_item = second
    if transaction == other_transaction or item != other_item:
        return False
    return "w" in (operation, other_operation)


def conflict_graph(schedule):
    """Baut den Konfliktgraphen eines Schedules.

    Args:
        schedule: Folge von Tripeln (Transaktion, Operation, Datum), wobei
            die Operation ``r`` oder ``w`` ist.

    Returns:
        Abbildung von Transaktionen auf die Liste ihrer Nachfolger.
    """
    edges = {}
    for index, earlier in enumerate(schedule):
        for later in schedule[index + 1:]:
            if _conflicting(earlier, later):
                targets = edges.setdefault(earlier[0], [])
                if later[0] not in targets:
                    targets.append(later[0])
    return edges


def has_cycle(graph):
    """Sucht einen Zyklus mit einer Tiefensuche und drei Farben."""
    state = {}

    def visit(node):
        """Durchsucht den Teilgraphen und meldet eine graue Rueckwaertskante."""
        state[node] = "grey"
        for neighbour in graph.get(node, []):
            colour = state.get(neighbour)
            if colour == "grey":
                return True
            if colour is None and visit(neighbour):
                return True
        state[node] = "black"
        return False

    return any(visit(node) for node in list(graph) if node not in state)


def is_conflict_serialisable(schedule):
    """Prüft, ob ein Schedule konfliktserialisierbar ist."""
    return not has_cycle(conflict_graph(schedule))


def serial_order(schedule):
    """Gibt eine äquivalente serielle Reihenfolge an.

    Returns:
        Liste der Transaktionen in topologischer Ordnung.

    Raises:
        ValueError: wenn der Graph einen Zyklus enthält.
    """
    graph = conflict_graph(schedule)
    nodes = []
    for transaction, _, _ in schedule:
        if transaction not in nodes:
            nodes.append(transaction)
    incoming = {node: 0 for node in nodes}
    for sources in graph.values():
        for target in sources:
            incoming[target] += 1
    order = []
    ready = [node for node in nodes if incoming[node] == 0]
    while ready:
        node = ready.pop(0)
        order.append(node)
        for neighbour in graph.get(node, []):
            incoming[neighbour] -= 1
            if incoming[neighbour] == 0:
                ready.append(neighbour)
    if len(order) != len(nodes):
        raise ValueError("Schedule ist nicht serialisierbar")
    return order


def view_serialisability_is_wider():
    """Beschreibt das Verhältnis zur Sichtserialisierbarkeit.

    Konfliktserialisierbarkeit ist die strengere Bedingung; sie lässt
    sich in Polynomzeit prüfen, während die Sichtserialisierbarkeit
    NP-vollständig ist.
    """
    return {"conflict is stronger": True, "conflict test": "polynomial",
            "view test": "NP-complete"}
