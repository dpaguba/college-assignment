"""Der erwartete Ertrag einer Kreuzung."""

import random

PIPS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}


def expected_yield(tokens):
    """Die erwartete Kartenzahl je Wurf für eine Siedlung.

    Aufsummiert werden die Wahrscheinlichkeiten der angrenzenden
    Zahlen. Das ist erlaubt, obwohl sich die Ereignisse ausschliessen:
    bei einem Wurf liefert höchstens ein Feld, und der Erwartungswert
    einer Summe ist die Summe der Erwartungswerte, ob abhängig oder
    nicht.

    Args:
        tokens: die Zahlen der angrenzenden Felder, None für die Wüste.

    Returns:
        Die erwartete Zahl der Karten je Wurf.

    Raises:
        ValueError: bei mehr als drei Feldern oder einer unmöglichen
            Zahl.
    """
    if len(tokens) > 3:
        raise ValueError("an einer Kreuzung liegen höchstens drei Felder")
    total = 0.0
    for token in tokens:
        if token is None:
            continue
        if token not in PIPS:
            raise ValueError("kein gültiges Zahlenplättchen: %s" % token)
        total += PIPS[token] / 36.0
    return total


def settlement_or_city(tokens):
    """Vergleicht den Ertrag einer Siedlung und einer Stadt.

    Raises:
        ValueError: wie bei ``expected_yield``.
    """
    base = expected_yield(tokens)
    return {"settlement": base, "city": 2.0 * base,
            "gain": base,
            "why upgrading is cheap": "die Stadt verdoppelt den Ertrag "
                                      "einer Kreuzung, ohne eine neue zu "
                                      "brauchen"}


def corner_report(tokens, resources):
    """Bewertet eine Kreuzung nach Ertrag und Vielfalt.

    Der Ertrag allein reicht nicht: drei Felder desselben Rohstoffs
    liefern viele Karten einer Art, und gebaut wird aus vieren. Deshalb
    steht die Zahl der verschiedenen Rohstoffe daneben.

    Raises:
        ValueError: bei unpassend vielen Angaben.
    """
    if len(tokens) != len(resources):
        raise ValueError("zu jeder Zahl gehört ein Rohstoff")
    return {"expected yield": expected_yield(tokens),
            "kinds": len({name for name in resources if name}),
            "tokens": list(tokens), "resources": list(resources)}


def best_corners(board=None, seed=0, count=5):
    """Sucht die ertragreichsten Kreuzungen eines Bretts.

    Raises:
        ValueError: bei einer nicht positiven Anzahl.
    """
    if count <= 0:
        raise ValueError("die Anzahl muss positiv sein")
    if board is None:
        board = _board(seed)
    found = []
    for point in sorted({corner for centre in board
                         for corner in _corners(centre)}):
        touching = [centre for centre in board
                    if point in _corners(centre)]
        tokens = [board[centre]["token"] for centre in touching]
        resources = [board[centre]["yields"] for centre in touching]
        found.append({"corner": point,
                      "expected yield": expected_yield(tokens),
                      "kinds": len({name for name in resources if name}),
                      "tokens": tokens})
    found.sort(key=lambda row: (-row["expected yield"], -row["kinds"],
                                row["corner"]))
    return found[:count]


def simulate(tokens, rolls=100000, seed=0):
    """Würfelt und zählt, was die Kreuzung wirklich abwirft.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Würfen.
    """
    if rolls <= 0:
        raise ValueError("es muss gewürfelt werden")
    rng = random.Random(seed)
    wanted = [token for token in tokens if token is not None]
    got = 0
    for _ in range(rolls):
        rolled = rng.randint(1, 6) + rng.randint(1, 6)
        got += wanted.count(rolled)
    return {"measured": got / rolls, "expected": expected_yield(tokens),
            "rolls": rolls}


def _corners(centre):
    """Die sechs Ecken eines Feldes."""
    column, row = centre
    return [(column, row + 2), (column + 1, row + 1),
            (column + 1, row - 1), (column, row - 2),
            (column - 1, row - 1), (column - 1, row + 1)]


def _board(seed):
    """Ein gemischtes Brett, damit das Modul für sich lauffähig ist."""
    rows = {-6: (-2, 0, 2), -3: (-3, -1, 1, 3), 0: (-4, -2, 0, 2, 4),
            3: (-3, -1, 1, 3), 6: (-2, 0, 2)}
    kinds = (("Ackerland", "Getreide", 4), ("Wald", "Holz", 4),
             ("Weide", "Wolle", 4), ("Hügel", "Lehm", 3),
             ("Gebirge", "Erz", 3), ("Wüste", None, 1))
    tokens = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    rng = random.Random(seed)
    fields = [name for name, _, count in kinds for _ in range(count)]
    rng.shuffle(fields)
    rng.shuffle(tokens)
    yields = {name: resource for name, resource, _ in kinds}
    built = {}
    centres = [(column, row) for row, columns in sorted(rows.items())
               for column in columns]
    for centre, name in zip(centres, fields):
        built[centre] = {"resource": name, "yields": yields[name],
                         "token": None if name == "Wüste"
                         else tokens.pop()}
    return built


def what_the_number_does_not_say():
    """Nennt, was der Ertrag einer Kreuzung offen lässt.

    Er sagt nichts über die Mischung, nichts über die Häfen, nichts über
    das, was die Gegner brauchen, und nichts über den Räuber, der genau
    auf die stärkste Zahl gesetzt wird. Eine Kreuzung an zwei Sechsen
    ist die beste im Erwartungswert und die erste, die blockiert wird.
    """
    return {"missing": ["die Mischung der Rohstoffe", "die Häfen",
                        "was die Gegner brauchen",
                        "der Räuber sucht die stärkste Zahl"],
            "the irony": "die beste Kreuzung wird als erste blockiert"}
