"""Relationen, Schlüssel und Integritätsbedingungen des relationalen Modells."""

from itertools import combinations


class Relation:
    """Eine Relation als Menge von Tupeln über einem festen Schema.

    Duplikate verschwinden bei der Konstruktion, weil eine Relation
    mengenwertig ist. Die Reihenfolge der Tupel trägt keine Bedeutung.
    """

    def __init__(self, attributes, rows):
        """Legt eine Relation über den Attributen mit den Tupeln an.

        Args:
            attributes: Namen der Attribute in Reihenfolge des Schemas.
            rows: iterierbare Folge gleich langer Tupel.

        Raises:
            ValueError: wenn ein Tupel nicht zur Stelligkeit passt.
        """
        self.attributes = list(attributes)
        collected = []
        for row in rows:
            row = tuple(row)
            if len(row) != len(self.attributes):
                raise ValueError("Tupel passt nicht zum Schema")
            if row not in collected:
                collected.append(row)
        self.rows = collected

    def index_of(self, attribute):
        """Gibt die Position eines Attributs im Schema zurück."""
        return self.attributes.index(attribute)

    def values(self, attributes):
        """Projiziert jedes Tupel auf die genannten Attribute."""
        positions = [self.index_of(name) for name in attributes]
        return [tuple(row[position] for position in positions)
                for row in self.rows]

    def __len__(self):
        """Anzahl der Tupel."""
        return len(self.rows)


def is_key(relation, attributes):
    """Prüft, ob die Attribute die Tupel der Relation eindeutig bestimmen.

    Das ist die Superschlüssel-Eigenschaft: Minimalität wird hier nicht
    verlangt.
    """
    projected = relation.values(attributes)
    return len(set(projected)) == len(relation.rows)


def is_minimal_key(relation, attributes):
    """Prüft, ob die Attribute ein Schlüssel sind und keine Teilmenge davon."""
    if not is_key(relation, attributes):
        return False
    for dropped in attributes:
        smaller = [name for name in attributes if name != dropped]
        if smaller and is_key(relation, smaller):
            return False
    return True


def candidate_keys(relation):
    """Sucht alle minimalen Schlüssel der Ausprägung.

    Die Suche geht über alle Attributmengen aufsteigender Größe und
    verwirft jede, die eine gefundene Menge umfasst.

    Returns:
        Liste der Schlüssel, jeweils als Liste von Attributnamen in
        Schemareihenfolge.
    """
    found = []
    for size in range(1, len(relation.attributes) + 1):
        for subset in combinations(relation.attributes, size):
            subset = list(subset)
            if any(set(key) <= set(subset) for key in found):
                continue
            if is_key(relation, subset):
                found.append(subset)
    return found


def foreign_key_holds(child, child_attribute, parent, parent_attribute):
    """Prüft die referentielle Integrität zwischen zwei Relationen.

    Ein Nullwert im Fremdschlüssel verletzt die Bedingung nicht: er
    bedeutet, dass keine Referenz besteht.
    """
    targets = {row[0] for row in parent.values([parent_attribute])}
    for value, in child.values([child_attribute]):
        if value is None:
            continue
        if value not in targets:
            return False
    return True


def entity_integrity_holds(relation, key):
    """Prüft, dass kein Schlüsselattribut einen Nullwert trägt."""
    for row in relation.values(key):
        if any(value is None for value in row):
            return False
    return True
