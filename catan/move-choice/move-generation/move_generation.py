"""Die zulässigen Züge auf dem Brett."""

ROWS = {-6: (-2, 0, 2), -3: (-3, -1, 1, 3), 0: (-4, -2, 0, 2, 4),
        3: (-3, -1, 1, 3), 6: (-2, 0, 2)}


def _centres():
    """Die Mittelpunkte der Felder."""
    return [(column, row) for row, columns in sorted(ROWS.items())
            for column in columns]


def _corners(centre):
    """Die sechs Ecken eines Feldes."""
    column, row = centre
    return [(column, row + 2), (column + 1, row + 1),
            (column + 1, row - 1), (column, row - 2),
            (column - 1, row - 1), (column - 1, row + 1)]


INTERSECTIONS = sorted({point for centre in _centres()
                        for point in _corners(centre)})

ROADS = sorted({tuple(sorted((points[index], points[(index + 1) % 6])))
                for centre in _centres()
                for points in [_corners(centre)]
                for index in range(6)})

NEIGHBOURS = {point: sorted(other for road in ROADS if point in road
                            for other in road if other != point)
              for point in INTERSECTIONS}

BOX = 4 * 5

_LARGEST = {}


def neighbours(point):
    """Nennt die Nachbarkreuzungen einer Kreuzung.

    Raises:
        ValueError: bei einer Kreuzung, die nicht zum Brett gehört.
    """
    if point not in NEIGHBOURS:
        raise ValueError("keine Kreuzung dieses Bretts")
    return list(NEIGHBOURS[point])


def settlement_spots(taken):
    """Nennt die Kreuzungen, auf die gebaut werden darf.

    Die Abstandsregel verbietet nicht nur die belegte Kreuzung, sondern
    auch ihre Nachbarn. Eine Siedlung sperrt daher bis zu vier
    Kreuzungen, und deshalb ist das Brett schneller voll, als die
    vierundfünfzig Plätze vermuten lassen.

    Raises:
        ValueError: bei einer Kreuzung, die nicht zum Brett gehört.
    """
    blocked = set()
    for point in taken:
        if point not in NEIGHBOURS:
            raise ValueError("keine Kreuzung dieses Bretts")
        blocked.add(point)
        blocked.update(NEIGHBOURS[point])
    return [point for point in INTERSECTIONS if point not in blocked]


def place(taken, point):
    """Setzt eine Siedlung und gibt die neue Belegung zurück.

    Raises:
        ValueError: bei einer Kreuzung ausserhalb des Bretts oder einer
            Verletzung der Abstandsregel.
    """
    if point not in NEIGHBOURS:
        raise ValueError("keine Kreuzung dieses Bretts")
    if point not in settlement_spots(taken):
        raise ValueError("die Abstandsregel verbietet diese Kreuzung")
    return list(taken) + [point]


def road_spots(taken_roads, own_roads, own_settlements):
    """Nennt die Wege, die gebaut werden dürfen.

    Ein Weg muss an das eigene Netz anschliessen, also an eine eigene
    Siedlung oder an einen eigenen Weg. Wer nichts auf dem Brett hat,
    kann keinen Weg bauen, und das ist der Grund für die beiden
    Startsiedlungen.

    Raises:
        ValueError: bei einem Weg, den es nicht gibt.
    """
    for road in list(taken_roads) + list(own_roads):
        if tuple(sorted(road)) not in ROADS:
            raise ValueError("kein Weg dieses Bretts")
    reachable = set(own_settlements)
    for road in own_roads:
        reachable.update(road)
    blocked = {tuple(sorted(road)) for road in taken_roads}
    return [road for road in ROADS
            if road not in blocked
            and (road[0] in reachable or road[1] in reachable)]


def most_that_fit():
    """Sucht die grösste Menge von Siedlungen, die nebeneinander passt.

    Das ist die grösste unabhängige Menge des Kreuzungsgraphen, gesucht
    mit Verzweigen und Beschränken über Bitmasken. Die Antwort ist
    siebenundzwanzig, also genau die Hälfte der Kreuzungen.

    Die Schachtel enthält aber nur zwanzig Siedlungen. Nicht die
    Abstandsregel begrenzt das Brett, sondern das Material, und in einer
    wirklichen Partie noch früher die Wege, die man erst dorthin bauen
    muss.

    Returns:
        Abbildung mit dem Maximum und einer Lösung.
    """
    order = {point: index for index, point in enumerate(INTERSECTIONS)}
    masks = [0] * len(INTERSECTIONS)
    for one, two in ROADS:
        masks[order[one]] |= 1 << order[two]
        masks[order[two]] |= 1 << order[one]
    best = {"size": 0, "set": 0}

    def branch(available, chosen, size):
        """Verzweigt über die noch freien Kreuzungen."""
        if size + bin(available).count("1") <= best["size"]:
            return
        if available == 0:
            if size > best["size"]:
                best["size"] = size
                best["set"] = chosen
            return
        index = (available & -available).bit_length() - 1
        branch(available & ~((1 << index) | masks[index]),
               chosen | (1 << index), size + 1)
        branch(available & ~(1 << index), chosen, size)

    if "found" in _LARGEST:
        best = _LARGEST["found"]
    else:
        branch((1 << len(INTERSECTIONS)) - 1, 0, 0)
        _LARGEST["found"] = best
    solution = [point for point in INTERSECTIONS
                if best["set"] >> order[point] & 1]
    return {"maximum": best["size"], "one solution": solution,
            "intersections": len(INTERSECTIONS),
            "settlements in the box": BOX,
            "what really limits it": "das Material und die Wege dorthin, "
                                     "nicht die Abstandsregel"}


def why_generating_moves_is_the_easy_half():
    """Sagt, wo die eigentliche Arbeit liegt.

    Die Spielimplementierung des Fachprojekts bietet für die meisten
    Züge alle Möglichkeiten an; die Aufgabe ist, den besten zu finden.
    Die Ausnahmen sind aufschlussreich: für den Handel zwischen Spielern
    muss die Anfrage selbst gebaut werden, und beim Abwerfen muss selbst
    entschieden werden, welche Karten gehen.

    Genau dort ist der Raum zu gross zum Aufzählen: die Zahl der
    denkbaren Handelsangebote ist nicht beschränkt, und die Zahl der
    Abwurfmengen wächst mit der Hand. Deshalb liegen die Ausnahmen dort,
    wo eine Aufzählung nicht mehr trägt.
    """
    return {"given by the game": "fast alle Züge",
            "left to the player": ["das Handelsangebot",
                                   "die Auswahl beim Abwerfen"],
            "why those two": "ihr Raum lässt sich nicht aufzählen",
            "the real task": "aus den angebotenen Zügen den besten "
                             "auswählen"}
