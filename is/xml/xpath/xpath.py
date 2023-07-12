"""XPath: Pfade, Achsen und Prädikate über einem Dokumentbaum."""

import re


def select(root, path):
    """Wertet einen Pfadausdruck aus.

    Unterstützt werden absolute Pfade, die Nachfahrenachse ``//``,
    Attributprädikate der Form ``[@name='wert']``, Positionsprädikate der
    Form ``[n]`` und der Platzhalter ``*``.

    Args:
        root: Wurzel des Dokuments.
        path: Pfadausdruck.

    Returns:
        Liste der Knoten in Dokumentreihenfolge.

    Raises:
        ValueError: bei einem leeren Ausdruck.
    """
    if not path:
        raise ValueError("leerer Pfad")
    if path.startswith("//"):
        return _step(_sibling_groups(root), path[2:], grouped=True)
    steps = [step for step in path.split("/") if step]
    if path.startswith("/"):
        if not steps:
            return [root]
        first = steps.pop(0)
        if not _matches(root, first):
            return []
        current = [root]
    else:
        current = [root]
    for step in steps:
        groups = [list(node) for node in current]
        current = _step(groups, step, grouped=True)
    return current


def values(root, path):
    """Wertet einen Pfad aus, der auf ein Attribut endet.

    Returns:
        Liste der Attributwerte.

    Raises:
        ValueError: wenn der Pfad nicht auf ein Attribut zeigt.
    """
    if "/@" not in path:
        raise ValueError("Pfad endet nicht auf einem Attribut")
    node_path, attribute = path.rsplit("/@", 1)
    return [node.attrib[attribute] for node in select(root, node_path)
            if attribute in node.attrib]


def axes():
    """Nennt die Achsen, die in der Vorlesung vorkommen."""
    return ["child", "descendant", "parent", "ancestor", "attribute",
            "following-sibling", "preceding-sibling"]


def _descendants(node):
    """Sammelt den Knoten und alle Nachfahren in Dokumentreihenfolge."""
    found = [node]
    for child in node:
        found.extend(_descendants(child))
    return found


def _sibling_groups(root):
    """Zerlegt den Baum in die Geschwistergruppen der Nachfahrenachse.

    Ein Positionsprädikat zählt in XPath je Elternknoten, nicht über das
    ganze Dokument; deshalb liefert die Nachfahrenachse eine Gruppe je
    Elternknoten, in Dokumentreihenfolge.
    """
    groups = [[root]]
    for node in _descendants(root):
        children = list(node)
        if children:
            groups.append(children)
    return groups


def _step(nodes, step, grouped):
    """Wendet einen Schritt an und wertet dabei ein Positionsprädikat aus.

    Args:
        nodes: bei ``grouped`` eine Liste von Geschwisterlisten, sonst eine
            flache Knotenliste.
        step: Elementname mit optionalem Prädikat.
        grouped: sagt, ob die Position je Geschwistergruppe zählt.

    Returns:
        Liste der ausgewählten Knoten in Dokumentreihenfolge.
    """
    groups = nodes if grouped else [nodes]
    position = _position_predicate(step)
    found = []
    for group in groups:
        matching = [node for node in group if _matches(node, step)]
        if position is not None:
            matching = matching[position - 1:position]
        found.extend(matching)
    return found


def _position_predicate(step):
    """Liest die Position aus einem Prädikat der Form ``[n]``.

    Returns:
        Die Position, gezählt ab eins, oder None.

    Raises:
        ValueError: bei der Position null, die XPath nicht kennt.
    """
    match = re.search(r"\[(\d+)\]", step)
    if match is None:
        return None
    position = int(match.group(1))
    if position < 1:
        raise ValueError("XPath zaehlt Positionen ab eins")
    return position


def _step_name(step):
    """Trennt den Elementnamen vom Prädikat eines Schritts."""
    return step.split("[", 1)[0]


def _matches(node, step):
    """Prüft, ob ein Knoten Namen und Attributprädikat eines Schritts erfüllt.

    Das Positionsprädikat bleibt hier unberücksichtigt, weil es die
    ganze Geschwistergruppe braucht.

    Raises:
        ValueError: bei einem Prädikat, das dieses Modul nicht kennt.
    """
    wanted = _step_name(step)
    if wanted not in ("*", node.tag):
        return False
    predicate = step[len(wanted):]
    if not predicate:
        return True
    match = re.fullmatch(r"\[@([\w:-]+)='([^']*)'\]", predicate)
    if match:
        return node.attrib.get(match.group(1)) == match.group(2)
    if re.fullmatch(r"\[\d+\]", predicate):
        return True
    match = re.fullmatch(r"\[@([\w:-]+)\]", predicate)
    if match:
        return match.group(1) in node.attrib
    raise ValueError("unbekanntes Praedikat: %s" % predicate)
