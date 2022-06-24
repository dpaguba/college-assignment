"""Operatoren der Relationenalgebra auf Listen von Tupeln."""


def _distinct(rows):
    """Entfernt Duplikate und erhält die Reihenfolge des ersten Auftretens."""
    seen = []
    for row in rows:
        row = tuple(row)
        if row not in seen:
            seen.append(row)
    return seen


def select(rows, predicate):
    """Selektion: behält die Tupel, für die das Prädikat wahr ist."""
    return [tuple(row) for row in rows if predicate(row)]


def project(rows, positions):
    """Projektion auf die genannten Stellen, mit Duplikatentfernung."""
    return _distinct(tuple(row[position] for position in positions)
                     for row in rows)


def rename(attributes, old, new):
    """Umbenennung eines Attributs im Schema.

    Raises:
        ValueError: wenn der alte Name fehlt oder der neue schon vorkommt.
    """
    if old not in attributes:
        raise ValueError("Attribut nicht vorhanden")
    if new in attributes:
        raise ValueError("Name schon vergeben")
    return [new if name == old else name for name in attributes]


def union(left, right):
    """Vereinigung zweier gleich stelliger Relationen.

    Raises:
        ValueError: wenn die Stelligkeiten nicht übereinstimmen.
    """
    _check_arity(left, right)
    return _distinct(list(left) + list(right))


def difference(left, right):
    """Differenz: Tupel der linken Relation, die rechts fehlen."""
    _check_arity(left, right)
    excluded = {tuple(row) for row in right}
    return [tuple(row) for row in _distinct(left) if tuple(row) not in excluded]


def intersection(left, right):
    """Durchschnitt, ausgedrückt über zwei Differenzen."""
    return difference(left, difference(left, right))


def product(left, right):
    """Kartesisches Produkt: jedes Tupel links mit jedem Tupel rechts."""
    return [tuple(first) + tuple(second) for first in left for second in right]


def natural_join(left, right, left_positions, right_positions):
    """Verbund über die genannten Stellenpaare.

    Die Verbundattribute erscheinen im Ergebnis einmal, die restlichen
    Stellen der rechten Relation folgen danach.

    Raises:
        ValueError: wenn die beiden Stellenlisten verschieden lang sind.
    """
    if len(left_positions) != len(right_positions):
        raise ValueError("Verbundattribute passen nicht zusammen")
    rest = [position for position in range(_arity(right))
            if position not in right_positions]
    result = []
    for first in left:
        for second in right:
            if all(first[a] == second[b]
                   for a, b in zip(left_positions, right_positions)):
                result.append(tuple(first)
                              + tuple(second[position] for position in rest))
    return _distinct(result)


def theta_join(left, right, predicate):
    """Verbund über eine beliebige Bedingung auf dem Produkt."""
    return select(product(left, right), predicate)


def basic_operators():
    """Nennt die Operatoren, aus denen sich alle übrigen ableiten lassen."""
    return ["selection", "projection", "union", "difference",
            "cartesian product", "rename"]


def _arity(rows):
    """Stelligkeit der Relation, 0 bei leerer Relation."""
    for row in rows:
        return len(row)
    return 0


def _check_arity(left, right):
    """Wirft, wenn zwei Relationen nicht dieselbe Stelligkeit haben."""
    if left and right and _arity(left) != _arity(right):
        raise ValueError("Relationen sind nicht vereinigungsverträglich")
