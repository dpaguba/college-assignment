"""Zerlegung in Boyce-Codd-Normalform und ihre Eigenschaften."""

import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "functional-dependencies"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "normal-forms"))

import functional_dependencies as fds
import normal_forms


def projected(dependencies, attributes):
    """Projiziert die Abhängigkeiten auf eine Teilmenge der Attribute.

    Für jede Teilmenge der Attribute wird ihre Hülle gebildet und auf die
    Teilmenge eingeschränkt; nichttriviale Ergebnisse bleiben stehen.
    """
    attributes = set(attributes)
    result = []
    for size in range(1, len(attributes)):
        for subset in combinations(sorted(attributes), size):
            subset = set(subset)
            right = (fds.closure(subset, dependencies) & attributes) - subset
            if right:
                result.append((frozenset(subset), frozenset(right)))
    return result


def violation(attributes, dependencies):
    """Sucht eine Abhängigkeit, die die Boyce-Codd-Normalform verletzt.

    Returns:
        Das Paar (linke Seite, rechte Seite) oder None.
    """
    attributes = set(attributes)
    for left, right in dependencies:
        if set(right) <= set(left):
            continue
        if fds.closure(left, dependencies) != attributes:
            return set(left), set(right)
    return None


def decompose(attributes, dependencies):
    """Zerlegt ein Schema rekursiv, bis jedes Teilschema in BCNF ist.

    Bei einer Verletzung X → Y entstehen die Teilschemata X⁺ und
    X ∪ (R − X⁺).

    Returns:
        Liste der Teilschemata als Mengen von Attributnamen.
    """
    attributes = set(attributes)
    local = projected(dependencies, attributes)
    broken = violation(attributes, local)
    if broken is None:
        return [attributes]
    left, _ = broken
    hull = fds.closure(left, local) & attributes
    rest = left | (attributes - hull)
    return decompose(hull, dependencies) + decompose(rest, dependencies)


def lossless(attributes, dependencies, parts):
    """Prüft die Verbundtreue mit dem Tableau-Verfahren von Aho.

    Das Tableau hat eine Zeile je Teilschema; wiederholtes Anwenden der
    Abhängigkeiten gleicht Symbole an. Enthält am Ende eine Zeile nur
    ausgezeichnete Symbole, ist die Zerlegung verbundtreu.
    """
    attributes = sorted(attributes)
    tableau = []
    for index, part in enumerate(parts):
        tableau.append([attribute if attribute in part
                        else "%s%d" % (attribute, index)
                        for attribute in attributes])
    position = {attribute: index for index, attribute in enumerate(attributes)}
    changed = True
    while changed:
        changed = False
        for left, right in dependencies:
            groups = {}
            for row in tableau:
                key = tuple(row[position[name]] for name in sorted(left))
                groups.setdefault(key, []).append(row)
            for rows in groups.values():
                if len(rows) < 2:
                    continue
                for name in right:
                    column = position[name]
                    values = [row[column] for row in rows]
                    marked = [value for value in values if value == name]
                    target = marked[0] if marked else values[0]
                    for row in rows:
                        if row[column] != target:
                            row[column] = target
                            changed = True
    return any(all(row[index] == attribute
                   for index, attribute in enumerate(attributes))
               for row in tableau)


def preserves_dependencies(dependencies, parts):
    """Prüft, ob die Vereinigung der projizierten Abhängigkeiten reicht.

    Jede ursprüngliche Abhängigkeit muss aus den Abhängigkeiten folgen,
    die innerhalb der Teilschemata sichtbar bleiben.
    """
    kept = []
    for part in parts:
        kept.extend(projected(dependencies, part))
    return all(fds.implies(kept, dependency) for dependency in dependencies)


def trade_off():
    """Fasst zusammen, was die Zerlegung garantiert und was nicht."""
    return {"lossless": True, "dependency preserving": False,
            "normal form": "BCNF"}
