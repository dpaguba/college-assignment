"""Die Geometrie des Spielbretts von Catan."""

import random

ROWS = {-6: (-2, 0, 2), -3: (-3, -1, 1, 3), 0: (-4, -2, 0, 2, 4),
        3: (-3, -1, 1, 3), 6: (-2, 0, 2)}

RESOURCES = (("Ackerland", "Getreide", 4), ("Wald", "Holz", 4),
             ("Weide", "Wolle", 4), ("Hügel", "Lehm", 3),
             ("Gebirge", "Erz", 3), ("Wüste", None, 1))

TOKENS = (2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12)


def centres():
    """Nennt die Mittelpunkte der neunzehn Felder.

    Gerechnet wird in ganzen Zahlen: eine Spalte weiter sind zwei
    Einheiten, eine Reihe weiter drei. Damit fallen gemeinsame Ecken
    zweier Felder exakt zusammen, ohne dass gerundet werden muss.

    Returns:
        Liste der Mittelpunkte als Paare.
    """
    return [(column, row) for row, columns in sorted(ROWS.items())
            for column in columns]


def corners(centre):
    """Nennt die sechs Ecken eines Feldes.

    Returns:
        Liste der Ecken, im Uhrzeigersinn ab oben.
    """
    column, row = centre
    return [(column, row + 2), (column + 1, row + 1),
            (column + 1, row - 1), (column, row - 2),
            (column - 1, row - 1), (column - 1, row + 1)]


def intersections():
    """Nennt alle Kreuzungen des Bretts.

    Sie ergeben sich aus der Geometrie und werden nicht gezählt: die
    Ecken der neunzehn Felder, doppelte zusammengefasst.
    """
    return sorted({point for centre in centres()
                   for point in corners(centre)})


def roads():
    """Nennt alle Wege des Bretts.

    Ein Weg ist eine Seite eines Feldes, also ein ungeordnetes Paar
    benachbarter Kreuzungen.
    """
    found = set()
    for centre in centres():
        points = corners(centre)
        for index in range(6):
            found.add(frozenset((points[index], points[(index + 1) % 6])))
    return sorted(tuple(sorted(edge)) for edge in found)


def euler():
    """Prüft die Geometrie mit der eulerschen Polyederformel.

    Für einen zusammenhängenden ebenen Graphen gilt V minus E plus F
    gleich zwei, wobei die Flächen die neunzehn Felder und das Äussere
    sind. Die Formel prüft die Konstruktion gegen etwas, das nichts mit
    Catan zu tun hat: stimmen die Ecken oder die Kanten nicht, kommt
    nicht zwei heraus.

    Returns:
        Abbildung mit den drei Zahlen und ihrer Verrechnung.
    """
    points = len(intersections())
    edges = len(roads())
    faces = len(centres()) + 1
    return {"vertices": points, "edges": edges, "faces": faces,
            "V - E + F": points - edges + faces}


def degrees():
    """Zählt, an wie vielen Wegen die Kreuzungen liegen.

    Returns:
        Abbildung vom Grad auf die Anzahl der Kreuzungen.
    """
    counted = {}
    for one, two in roads():
        for point in (one, two):
            counted[point] = counted.get(point, 0) + 1
    found = {}
    for value in counted.values():
        found[value] = found.get(value, 0) + 1
    return found


def hexes_at(point):
    """Nennt die Felder, die an einer Kreuzung liegen.

    Raises:
        ValueError: wenn der Punkt keine Kreuzung des Bretts ist.
    """
    found = [centre for centre in centres() if point in corners(centre)]
    if not found:
        raise ValueError("keine Kreuzung dieses Bretts")
    return found


def resource_counts():
    """Nennt die Verteilung der Landschaften aus der Schachtel."""
    return {name: count for name, _, count in RESOURCES}


def yields():
    """Nennt, welche Landschaft welchen Rohstoff liefert."""
    return {name: resource for name, resource, _ in RESOURCES}


def board(seed=0):
    """Mischt ein Brett aus Landschaften und Zahlen.

    Die Wüste bekommt keine Zahl; auf ihr steht zu Beginn der Räuber.
    Deshalb sind es achtzehn Zahlen auf neunzehn Feldern, und deshalb
    geht die Rechnung mit den Augen der Zahlen nur über achtzehn Felder.

    Args:
        seed: der Startwert des Mischens.

    Returns:
        Abbildung vom Mittelpunkt auf Landschaft, Rohstoff und Zahl.
    """
    rng = random.Random(seed)
    fields = [name for name, _, count in RESOURCES for _ in range(count)]
    rng.shuffle(fields)
    numbers = list(TOKENS)
    rng.shuffle(numbers)
    built = {}
    resource = yields()
    for centre, name in zip(centres(), fields):
        token = None if name == "Wüste" else numbers.pop()
        built[centre] = {"resource": name, "yields": resource[name],
                         "token": token}
    return built


def what_the_geometry_settles():
    """Sagt, was aus der Zählung folgt.

    Vierundfünfzig Kreuzungen bei zweiundsiebzig Wegen und vier
    Spielern mit je fünf Siedlungen: höchstens zwanzig Kreuzungen
    werden je bebaut, und wegen der Abstandsregel sperrt jede davon
    ihre Nachbarn. Der Platz ist also knapp, und das ist der Grund,
    warum die ersten beiden Setzungen über das ganze Spiel entscheiden.
    """
    return {"intersections": 54, "roads": 72,
            "settlements in the box": 20,
            "what follows": "der Platz ist knapp, und die ersten beiden "
                            "Setzungen entscheiden",
            "why": "die Abstandsregel sperrt zu jeder Siedlung ihre "
                   "Nachbarkreuzungen"}
