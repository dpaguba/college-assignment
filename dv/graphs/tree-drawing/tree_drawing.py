"""Zeichnen von Bäumen: das einfache Verfahren und das von Reingold/Tilford."""


def _depths(tree, root):
    """Bestimmt die Tiefe jedes Knotens."""
    found = {root: 0}
    queue = [root]
    while queue:
        node = queue.pop(0)
        for child in tree.get(node, []):
            found[child] = found[node] + 1
            queue.append(child)
    return found


def simple_levels(tree, root, spacing=1.0):
    """Zeichnet stufenweise: jede Ebene bekommt ihre Knoten nebeneinander.

    Das Verfahren ist einfach und breit: die Breite wächst mit der Zahl
    der Knoten einer Ebene, unabhängig davon, wie der Baum aussieht.

    Returns:
        Abbildung von Knoten auf ihre Koordinaten.
    """
    depths = _depths(tree, root)
    by_level = {}
    for node, depth in sorted(depths.items(), key=lambda entry: entry[1]):
        by_level.setdefault(depth, []).append(node)
    positions = {}
    for depth, nodes in by_level.items():
        for index, node in enumerate(nodes):
            positions[node] = (index * spacing, depth)
    return positions


def reingold_tilford(tree, root, spacing=1.0):
    """Zeichnet einen Baum nach Reingold und Tilford.

    Die Teilbäume werden getrennt gezeichnet und dann so weit
    zusammengeschoben, wie es die Konturen erlauben; ein Elternknoten
    steht mittig über seinen Kindern.

    Args:
        tree: Abbildung von Knoten auf ihre Kinder.
        root: Wurzel.
        spacing: kleinster Abstand zweier Knoten einer Ebene.

    Returns:
        Abbildung von Knoten auf Koordinatenpaare.

    Raises:
        ValueError: wenn die Wurzel im Baum fehlt.
    """
    if root not in tree:
        raise ValueError("Wurzel fehlt im Baum")

    def build(node):
        """Zeichnet den Teilbaum und gibt Positionen samt Konturen zurück."""
        children = tree.get(node, [])
        if not children:
            return {node: (0.0, 0)}, [0.0], [0.0]
        blocks = [build(child) for child in children]
        positions = {}
        left_contour = []
        right_contour = []
        offset = 0.0
        for index, (block, left, right) in enumerate(blocks):
            if index > 0:
                needed = 0.0
                overlap = min(len(right_contour), len(left))
                for level in range(overlap):
                    needed = max(needed,
                                 right_contour[level] - left[level] + spacing)
                offset = needed
            for name, (x, y) in block.items():
                positions[name] = (x + offset, y + 1)
            shifted_left = [value + offset for value in left]
            shifted_right = [value + offset for value in right]
            if not left_contour:
                left_contour = list(shifted_left)
                right_contour = list(shifted_right)
            else:
                for level in range(len(shifted_left)):
                    if level < len(left_contour):
                        left_contour[level] = min(left_contour[level],
                                                  shifted_left[level])
                    else:
                        left_contour.append(shifted_left[level])
                for level in range(len(shifted_right)):
                    if level < len(right_contour):
                        right_contour[level] = max(right_contour[level],
                                                   shifted_right[level])
                    else:
                        right_contour.append(shifted_right[level])
        middle = (positions[children[0]][0] + positions[children[-1]][0]) / 2
        positions[node] = (middle, 0)
        return (positions, [middle] + left_contour,
                [middle] + right_contour)

    positions, _, _ = build(root)
    smallest = min(x for x, _ in positions.values())
    return {node: (x - smallest, y) for node, (x, y) in positions.items()}


def no_overlap(positions, spacing=1.0):
    """Prüft, dass zwei Knoten einer Ebene mindestens ``spacing`` trennen."""
    by_level = {}
    for node, (x, y) in positions.items():
        by_level.setdefault(y, []).append(x)
    for values in by_level.values():
        values.sort()
        for earlier, later in zip(values, values[1:]):
            if later - earlier < spacing - 1e-9:
                return False
    return True


def width(positions):
    """Breite der Zeichnung, der Abstand des linken zum rechten Rand."""
    values = [x for x, _ in positions.values()]
    return max(values) - min(values)


def isomorphic_subtrees_congruent():
    """Prüft, dass gleich gebaute Teilbäume gleich gezeichnet werden.

    Zwei Teilbäume derselben Form müssen bis auf eine Verschiebung
    dieselben Koordinaten bekommen; das ist eine der Forderungen, die
    Reingold und Tilford an ein ordentliches Bild stellen.
    """
    tree = {"r": ["a", "b"], "a": ["a1", "a2"], "b": ["b1", "b2"],
            "a1": [], "a2": [], "b1": [], "b2": []}
    positions = reingold_tilford(tree, "r")
    first = [positions["a1"][0] - positions["a"][0],
             positions["a2"][0] - positions["a"][0]]
    second = [positions["b1"][0] - positions["b"][0],
              positions["b2"][0] - positions["b"][0]]
    return all(abs(a - b) < 1e-9 for a, b in zip(first, second))


def width_comparison():
    """Vergleicht die Breite beider Verfahren an einem schmalen Baum.

    Returns:
        Abbildung mit den Breiten beider Zeichnungen.
    """
    tree = {"r": ["a", "b"], "a": ["c"], "b": ["d"], "c": ["e"], "d": [],
            "e": []}
    return {"simple": width(simple_levels(tree, "r")),
            "reingold tilford": width(reingold_tilford(tree, "r"))}


def conventions():
    """Nennt die Zeichenkonventionen für Bäume aus der Vorlesung."""
    return ["children below the parent", "no edge crossings",
            "parent centred over its children",
            "same depth on the same line",
            "isomorphic subtrees drawn identically"]
