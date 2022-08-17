"""Auflösung transitiver Abhängigkeiten nach der Regel der kürzesten Strecke."""


def reachable(graph, root):
    """Sammelt alle über den Graphen erreichbaren Abhängigkeiten.

    Args:
        graph: Abbildung von (Name, Version) auf die Liste der direkten
            Abhängigkeiten.
        root: das eigene Projekt als (Name, Version).

    Returns:
        Menge aller erreichbaren Paare, den Wurzelknoten eingeschlossen.
    """
    seen = set()
    queue = [root]
    while queue:
        node = queue.pop()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(graph.get(node, []))
    return seen


def candidates(graph, root, name):
    """Nennt alle Versionen eines Artefakts samt ihrer kürzesten Entfernung.

    Returns:
        Liste von Paaren (Tiefe, Version), aufsteigend sortiert.
    """
    depths = {}
    queue = [(root, 0)]
    visited = {}
    while queue:
        node, depth = queue.pop(0)
        if node in visited and visited[node] <= depth:
            continue
        visited[node] = depth
        if node[0] == name and node != root:
            if node[1] not in depths or depth < depths[node[1]]:
                depths[node[1]] = depth
        for child in graph.get(node, []):
            queue.append((child, depth + 1))
    return sorted((depth, version) for version, depth in depths.items())


def resolve(graph, root):
    """Wählt je Artefakt eine Version nach der Regel des nächsten Vorkommens.

    Gewinnt die Version, die im Baum am wenigsten Schritte von der Wurzel
    entfernt steht; bei gleicher Entfernung die zuerst deklarierte. Eine
    eigene direkte Abhängigkeit steht immer auf Tiefe eins und schlägt
    daher jede transitive.

    Returns:
        Abbildung von Artefaktnamen auf die gewählte Version.

    Raises:
        KeyError: wenn eine genannte Abhängigkeit im Graphen fehlt.
    """
    chosen = {}
    order = 0
    queue = [(root, 0)]
    best = {}
    while queue:
        node, depth = queue.pop(0)
        if node not in graph:
            raise KeyError("unbekannte Abhaengigkeit: %s" % (node,))
        for child in graph[node]:
            if child not in graph:
                raise KeyError("unbekannte Abhaengigkeit: %s" % (child,))
            name, version = child
            key = (depth + 1, order)
            order += 1
            if name not in best or key[0] < best[name][0]:
                best[name] = key
                chosen[name] = version
            if depth + 1 <= _limit(graph):
                queue.append((child, depth + 1))
    return chosen


def _limit(graph):
    """Obere Schranke der Tiefe, damit ein Kreis die Suche nicht aufhält."""
    return len(graph) + 1


def conflict_report(graph, root):
    """Nennt die Artefakte, für die mehrere Versionen im Baum stehen.

    Returns:
        Abbildung von Artefaktnamen auf die Liste der gefundenen Versionen.
    """
    versions = {}
    for name, version in reachable(graph, root):
        versions.setdefault(name, set()).add(version)
    return {name: sorted(found) for name, found in versions.items()
            if len(found) > 1}


def exclusion(graph, root, excluded):
    """Entfernt eine Abhängigkeit samt ihrem Teilbaum aus der Auflösung."""
    trimmed = {node: [child for child in children if child[0] != excluded]
               for node, children in graph.items()}
    return resolve(trimmed, root)
