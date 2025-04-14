"""Wie weit es sich lohnt, vorauszuschauen."""

GAME = {
    "root": {"children": ["A", "B"], "guess": 0.0},
    "A": {"children": ["A1", "A2"], "guess": 5.0},
    "B": {"children": ["B1", "B2"], "guess": 3.0},
    "A1": {"children": ["A1x"], "guess": 4.0},
    "A2": {"children": ["A2x"], "guess": 4.0},
    "B1": {"children": ["B1x"], "guess": 9.0},
    "B2": {"children": ["B2x"], "guess": 1.0},
    "A1x": {"children": [], "guess": 10.0, "value": 10.0},
    "A2x": {"children": [], "guess": 8.0, "value": 8.0},
    "B1x": {"children": [], "guess": 0.0, "value": 0.0},
    "B2x": {"children": [], "guess": 0.0, "value": 0.0},
}

BEST = 10.0


def true_value(node):
    """Nennt den wirklichen Wert eines Knotens.

    Gerechnet wird bis zu den Blättern, ohne Schätzung. Das ist der
    Massstab, gegen den jede Suche mit begrenzter Tiefe gehalten wird.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    if node not in GAME:
        raise ValueError("unbekannter Knoten: %s" % node)
    row = GAME[node]
    if not row["children"]:
        return row["value"]
    return max(true_value(child) for child in row["children"])


def perfect(node):
    """Eine Schätzfunktion, die den wirklichen Wert kennt."""
    return true_value(node)


def guess(node):
    """Die Schätzfunktion des Beispiels, die sich in der Tiefe irrt.

    Raises:
        ValueError: bei einem unbekannten Knoten.
    """
    if node not in GAME:
        raise ValueError("unbekannter Knoten: %s" % node)
    return GAME[node]["guess"]


def search(node, depth=1, heuristic=None):
    """Sucht bis zu einer festen Tiefe und schätzt dann ab.

    Args:
        node: der Wurzelknoten.
        depth: die Suchtiefe in Zügen.
        heuristic: die Schätzfunktion für die Blätter der Suche.

    Returns:
        Abbildung mit dem Wert, dem gewählten Zug und der Zahl der
        besuchten Knoten.

    Raises:
        ValueError: bei einer nicht positiven Tiefe oder einem
            unbekannten Knoten.
    """
    if depth <= 0:
        raise ValueError("die Tiefe muss positiv sein")
    if node not in GAME:
        raise ValueError("unbekannter Knoten: %s" % node)
    heuristic = perfect if heuristic is None else heuristic
    seen = [0]

    def look(current, left):
        """Sucht rekursiv und zählt die besuchten Knoten."""
        seen[0] += 1
        row = GAME[current]
        if left == 0 or not row["children"]:
            return heuristic(current), None
        best = None
        for child in row["children"]:
            value, _ = look(child, left - 1)
            if best is None or value > best[0]:
                best = (value, child)
        return best

    value, move = look(node, depth)
    return {"value": value, "move": move, "nodes": seen[0], "depth": depth}


def deeper_is_not_always_better():
    """Zeigt, dass eine tiefere Suche schlechter entscheiden kann.

    Die Schätzung an der Wurzel spricht für A, und A ist auch richtig:
    dort liegt die Zehn. Eine Stufe tiefer sieht B besser aus, weil dort
    ein Knoten mit der Schätzung neun steht, hinter dem nichts mehr
    kommt. Die tiefere Suche wählt B und verliert alles.

    Das ist keine Ausnahme, sondern der Normalfall bei einer
    Schätzfunktion, deren Fehler mit der Tiefe nicht kleiner wird. Tiefer
    zu suchen hilft nur, wenn die Schätzung näher am Blatt besser wird,
    und für eine handgeschriebene Bewertungsfunktion ist das eine
    Annahme und kein Gesetz.

    Returns:
        Abbildung mit beiden Entscheidungen und ihren wirklichen Werten.
    """
    one = search("root", depth=1, heuristic=guess)
    two = search("root", depth=2, heuristic=guess)
    best = max(GAME["root"]["children"], key=true_value)
    return {"move at depth 1": one["move"], "move at depth 2": two["move"],
            "best move": best,
            "value at depth 1": true_value(one["move"]),
            "value at depth 2": true_value(two["move"]),
            "true best value": true_value(best),
            "why": "die Schätzung wird in der Tiefe nicht besser"}


def cost_of_depth():
    """Misst, wie die Zahl der Knoten mit der Tiefe wächst.

    Returns:
        Liste mit einer Zeile je Tiefe.
    """
    return [dict(search("root", depth=depth, heuristic=guess),
                 **{"branching": 2}) for depth in (1, 2, 3, 4)]


def what_it_means_for_catan():
    """Überträgt das Ergebnis auf das Fachprojekt.

    Die Folie fragt, wie weit es sich lohnt, in die Zukunft zu schauen.
    Für Catan kommt zur Frage der Schätzung noch der Würfel: nach jedem
    Zug verzweigt der Baum in elf Möglichkeiten, und ein Zug
    Vorausschau kostet damit nicht das Doppelte, sondern das Elffache
    mal der Zahl der eigenen Züge.

    Das Ergebnis oben sagt, dass sich dieser Aufwand nur lohnt, wenn die
    Bewertungsfunktion in der Nähe des Blattes besser wird. Deshalb ist
    die Reihenfolge im Projekt richtig herum: erst eine Bewertung, die
    etwas taugt, dann die Suche darüber.
    """
    return {"the question": "wie weit lohnt es sich vorauszuschauen",
            "the extra cost in Catan": "nach jedem Zug elf Würfelfälle",
            "what saves it": "eine Bewertung, die nahe am Blatt besser "
                             "wird",
            "the order that follows": "erst die Bewertung, dann die "
                                      "Suche"}
