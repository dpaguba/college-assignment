"""Verklemmungen: Erkennung im Wartegraphen, Vermeidung, Auflösung."""


def detect(wait_graph):
    """Sucht einen Zyklus im Wartegraphen.

    Args:
        wait_graph: Abbildung von Transaktionen auf die Transaktionen, auf
            die sie warten.

    Returns:
        Wahr, wenn ein Zyklus besteht, also eine Verklemmung vorliegt.
    """
    state = {}

    def visit(node):
        """Durchsucht den Teilgraphen und meldet einen gefundenen Zyklus."""
        state[node] = "grey"
        for neighbour in wait_graph.get(node, []):
            colour = state.get(neighbour)
            if colour == "grey":
                return True
            if colour is None and visit(neighbour):
                return True
        state[node] = "black"
        return False

    return any(visit(node) for node in list(wait_graph) if node not in state)


def cycle(wait_graph):
    """Gibt die Transaktionen eines gefundenen Zyklus zurück.

    Returns:
        Liste der Transaktionen des Zyklus oder eine leere Liste.
    """
    path = []
    on_path = set()
    visited = set()

    def visit(node):
        """Verlaengert den Pfad und gibt den Zyklus zurueck, sobald er sich schliesst."""
        path.append(node)
        on_path.add(node)
        visited.add(node)
        for neighbour in wait_graph.get(node, []):
            if neighbour in on_path:
                return path[path.index(neighbour):]
            if neighbour not in visited:
                found = visit(neighbour)
                if found:
                    return found
        path.pop()
        on_path.discard(node)
        return []

    for node in wait_graph:
        if node not in visited:
            found = visit(node)
            if found:
                return found
    return []


def victim(wait_graph, costs):
    """Wählt die Transaktion, deren Abbruch am wenigsten kostet.

    Args:
        wait_graph: Wartegraph.
        costs: Abbildung von Transaktionen auf ihre bisherige Arbeit.

    Returns:
        Name der abzubrechenden Transaktion.

    Raises:
        ValueError: wenn keine Verklemmung vorliegt.
    """
    involved = cycle(wait_graph)
    if not involved:
        raise ValueError("keine Verklemmung")
    return min(involved, key=lambda name: costs.get(name, 0))


def ordering_prevents(requests):
    """Prüft, ob alle Transaktionen die Betriebsmittel gleich ordnen.

    Args:
        requests: Folge von Paaren (Transaktion, Liste der Anforderungen).

    Returns:
        Wahr, wenn keine zwei Transaktionen zwei Betriebsmittel in
        verschiedener Reihenfolge anfordern.
    """
    pairs = {}
    for _, sequence in requests:
        for first_index, first in enumerate(sequence):
            for second in sequence[first_index + 1:]:
                if (second, first) in pairs:
                    return False
                pairs[(first, second)] = True
    return True


def timeout_may_kill_a_healthy_transaction():
    """Beschreibt die Schwäche der Zeitschranke.

    Eine langsame, aber nicht verklemmte Transaktion überschreitet die
    Schranke ebenso wie eine verklemmte.
    """
    return True


def strategies():
    """Nennt die Umgangsweisen mit Verklemmungen."""
    return ["detection", "prevention", "avoidance", "timeout"]
