"""Die drei Beziehungen zwischen Prozessen und die Prüfung der Hierarchie."""

RELATIONS = ("sequence", "decomposition", "specialisation")

DIRECTION = {"sequence": "horizontal", "decomposition": "vertical",
             "specialisation": "vertical"}

EXERCISE = {
    ("Produkte herstellen", "Einzelteile montieren"): "decomposition",
    ("Produkte herstellen", "Einzelteile herstellen"): "decomposition",
    ("Produkte herstellen", "Produkte liefern"): "sequence",
    ("Material beschaffen", "Produkte herstellen"): "sequence",
    ("Produkte liefern", "Kundendienst bereitstellen"): "sequence",
    ("Produkte vermarkten", "Produkte vermarkten (DE)"): "specialisation",
    ("Produkte vermarkten", "Produkte vermarkten (US)"): "specialisation",
    ("Produkte herstellen", "Information verarbeiten"): "decomposition",
}


def relations():
    """Nennt die drei Beziehungen."""
    return list(RELATIONS)


def direction(relation):
    """Sagt, ob eine Beziehung waagerecht oder senkrecht verläuft.

    Die Sequenz ordnet Prozesse nebeneinander an, die Zerlegung
    untereinander. Die Spezialisierung ist ebenfalls senkrecht, meint aber
    Varianten desselben Prozesses und keine Teile davon.

    Raises:
        ValueError: bei einer unbekannten Beziehung.
    """
    if relation not in DIRECTION:
        raise ValueError("unbekannte Beziehung")
    return DIRECTION[relation]


def classify(first, second):
    """Bestimmt die Beziehung zwischen zwei Prozessen der Übung.

    Raises:
        ValueError: wenn das Paar nicht in der Übung steht.
    """
    if (first, second) in EXERCISE:
        return EXERCISE[(first, second)]
    if (second, first) in EXERCISE:
        return EXERCISE[(second, first)]
    raise ValueError("unbekanntes Prozesspaar")


def check_hierarchy(edges):
    """Prüft eine Zerlegung auf Kreisfreiheit und misst ihre Tiefe.

    Eine Zerlegung ist eine Halbordnung: ein Prozess kann nicht mittelbar
    sein eigener Teilprozess sein. Ein Kreis in den Kanten wäre genau das
    und macht die Architektur unbrauchbar, weil sich die Ebenen nicht mehr
    durchnummerieren liessen.

    Args:
        edges: Paare aus Oberprozess und Teilprozess.

    Returns:
        Abbildung mit ``depth``, ``roots`` und ``leaves``.

    Raises:
        ValueError: bei einer leeren Zerlegung oder wenn die Kanten einen
            Kreis enthalten.
    """
    if not edges:
        raise ValueError("leere Zerlegung")
    children = {}
    nodes = set()
    for parent, child in edges:
        children.setdefault(parent, []).append(child)
        nodes.add(parent)
        nodes.add(child)
    roots = sorted(node for node in nodes
                   if all(node != child for _, child in edges))
    if not roots:
        raise ValueError("die Zerlegung enthält einen Kreis")

    depth = {}
    visiting = set()

    def measure(node):
        """Misst die Tiefe eines Teilbaums und meldet Kreise."""
        if node in visiting:
            raise ValueError("die Zerlegung enthält einen Kreis")
        if node in depth:
            return depth[node]
        visiting.add(node)
        below = [measure(child) for child in children.get(node, ())]
        visiting.discard(node)
        depth[node] = 1 + max(below, default=0)
        return depth[node]

    for node in nodes:
        measure(node)
    return {"depth": max(depth[root] for root in roots),
            "roots": roots,
            "leaves": sorted(node for node in nodes
                             if not children.get(node))}


def why_specialisation_is_not_decomposition():
    """Trennt die beiden senkrechten Beziehungen.

    Ein Teilprozess ist ein Stück des Ganzen und läuft mit den anderen
    Stücken zusammen ab. Eine Variante ist der ganze Prozess noch einmal,
    nur anders ausgeführt; von zwei Varianten läuft in einem Fall genau
    eine.
    """
    return {"decomposition": "the parts run together and make up the whole",
            "specialisation": "the variants are the whole, and one of them "
                              "runs per case",
            "test": "ask whether the two run in the same case"}
