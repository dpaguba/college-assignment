"""Ein Petrinetz als Tripel (P, T, F): Übungsblatt 10."""


def net(places, transitions, flow):
    """Baut ein Netz und prüft seine Form.

    Ein Netz ist ein Tripel aus Stellen, Transitionen und einer
    Flussrelation. Die Flussrelation darf nur von einer Stelle zu einer
    Transition oder umgekehrt führen; eine Kante zwischen zwei Stellen
    oder zwei Transitionen gibt es nicht, und das ist der Grund, warum
    das Netz zweigeteilt ist.

    Args:
        places: die Stellen.
        transitions: die Transitionen.
        flow: die Kanten als Paare.

    Returns:
        Abbildung mit den drei Bestandteilen.

    Raises:
        ValueError: bei einer leeren Menge, einem gemeinsamen Namen oder
            einer unzulässigen Kante.
    """
    places = list(places)
    transitions = list(transitions)
    if not places or not transitions:
        raise ValueError("Stellen und Transitionen dürfen nicht fehlen")
    shared = set(places) & set(transitions)
    if shared:
        raise ValueError("Name doppelt vergeben: %s" % sorted(shared))
    for source, target in flow:
        first = source in places
        second = target in places
        if first == second:
            raise ValueError("unzulässige Kante: %s nach %s"
                             % (source, target))
        for name in (source, target):
            if name not in places and name not in transitions:
                raise ValueError("unbekannter Knoten: %s" % name)
    return {"places": places, "transitions": transitions,
            "flow": [tuple(edge) for edge in flow]}


def preset(built, node):
    """Nennt den Vorbereich eines Knotens.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    if node not in built["places"] and node not in built["transitions"]:
        raise ValueError("unbekannter Knoten")
    return sorted(source for source, target in built["flow"]
                  if target == node)


def postset(built, node):
    """Nennt den Nachbereich eines Knotens.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    if node not in built["places"] and node not in built["transitions"]:
        raise ValueError("unbekannter Knoten")
    return sorted(target for source, target in built["flow"]
                  if source == node)


def is_bipartite(built):
    """Prüft die Zweiteilung; sie folgt aus der Bauvorschrift."""
    for source, target in built["flow"]:
        if (source in built["places"]) == (target in built["places"]):
            return False
    return True


def example():
    """Ein kleines Netz: eine Transition zwischen zwei Stellen."""
    return net(["P1", "P2"], ["T1"], [("P1", "T1"), ("T1", "P2")])


def sequence(length=3):
    """Baut eine Kette aus Stellen und Transitionen.

    Raises:
        ValueError: bei einer nicht positiven Länge.
    """
    if length < 1:
        raise ValueError("die Länge muss positiv sein")
    places = ["P%d" % index for index in range(1, length + 2)]
    transitions = ["T%d" % index for index in range(1, length + 1)]
    flow = []
    for index in range(length):
        flow.append((places[index], transitions[index]))
        flow.append((transitions[index], places[index + 1]))
    return net(places, transitions, flow)


def what_the_triple_leaves_out():
    """Sagt, was im Tripel noch nicht steht.

    Das Tripel beschreibt die Struktur und sagt nichts über den
    Zustand. Erst eine Markierung, also die Verteilung der Marken auf
    die Stellen, macht daraus ein System, das etwas tut. Zwei Netze mit
    demselben Tripel und verschiedenen Anfangsmarkierungen verhalten
    sich völlig verschieden.
    """
    return {"in the triple": ["Stellen", "Transitionen", "Flussrelation"],
            "not in the triple": ["die Markierung", "Kantengewichte",
                                  "Kapazitäten der Stellen"],
            "consequence": "die Struktur allein sagt nichts über das "
                           "Verhalten"}
