"""Funktionale Abhängigkeiten, Hülle, Schlüssel und minimale Überdeckung."""

from itertools import combinations


def closure(attributes, dependencies):
    """Berechnet die Attributhülle unter den Abhängigkeiten.

    Args:
        attributes: Startmenge von Attributnamen.
        dependencies: Liste von Paaren (linke Seite, rechte Seite).

    Returns:
        Menge aller Attribute, die aus der Startmenge folgen.
    """
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for left, right in dependencies:
            if set(left) <= result and not set(right) <= result:
                result |= set(right)
                changed = True
    return result


def implies(dependencies, candidate):
    """Prüft, ob eine Abhängigkeit aus den übrigen folgt."""
    left, right = candidate
    return set(right) <= closure(left, dependencies)


def candidate_keys(attributes, dependencies):
    """Sucht alle minimalen Schlüssel eines Schemas.

    Returns:
        Liste der Schlüssel als Mengen, ohne Obermengen bereits
        gefundener Schlüssel.
    """
    attributes = set(attributes)
    found = []
    for size in range(1, len(attributes) + 1):
        for subset in combinations(sorted(attributes), size):
            subset = set(subset)
            if any(key <= subset for key in found):
                continue
            if closure(subset, dependencies) == attributes:
                found.append(subset)
    return found


def derive(attributes, dependencies):
    """Leitet alle Abhängigkeiten aus den Armstrong-Axiomen ab.

    Angewandt werden Reflexivität, Verstärkung und Transitivität bis zum
    Fixpunkt. Das Verfahren ist unabhängig von der Hüllenberechnung und
    dient ihr als Prüfstein; es läuft in der Zahl der Attributmengen
    quadratisch und taugt daher nur für kleine Schemata.

    Args:
        attributes: Attribute des Schemas.
        dependencies: gegebene Abhängigkeiten.

    Returns:
        Menge der Paare (linke Seite, rechte Seite) als frozenset.
    """
    subsets = [frozenset(subset)
               for size in range(len(attributes) + 1)
               for subset in combinations(sorted(attributes), size)]
    derived = {(frozenset(left), frozenset(right))
               for left, right in dependencies}
    for left in subsets:
        for right in subsets:
            if right <= left:
                derived.add((left, right))
    changed = True
    while changed:
        changed = False
        for left, right in list(derived):
            for extra in subsets:
                widened = (left | extra, right | extra)
                if widened not in derived:
                    derived.add(widened)
                    changed = True
            for middle, far in list(derived):
                if middle == right and (left, far) not in derived:
                    derived.add((left, far))
                    changed = True
    return derived


def armstrong_agrees(dependencies):
    """Vergleicht die Hüllenberechnung mit der Ableitung aus den Axiomen.

    Geprüft werden alle Paare von Attributmengen des Schemas: die Hülle
    muss genau die Abhängigkeiten bestätigen, die sich ableiten lassen.
    """
    attributes = set()
    for left, right in dependencies:
        attributes |= set(left) | set(right)
    derived = derive(attributes, dependencies)
    for size in range(len(attributes) + 1):
        for left in combinations(sorted(attributes), size):
            for other_size in range(len(attributes) + 1):
                for right in combinations(sorted(attributes), other_size):
                    by_axioms = (frozenset(left), frozenset(right)) in derived
                    by_closure = implies(dependencies, (set(left), set(right)))
                    if by_axioms != by_closure:
                        return False
    return True


def equivalent(first, second):
    """Prüft, ob zwei Mengen von Abhängigkeiten dieselbe Hülle erzeugen."""
    return (all(implies(second, dependency) for dependency in first)
            and all(implies(first, dependency) for dependency in second))


def minimal_cover(dependencies):
    """Berechnet eine minimale Überdeckung.

    Zuerst werden die rechten Seiten auf einzelne Attribute zerlegt, dann
    überflüssige Attribute links entfernt und zuletzt ganze
    Abhängigkeiten gestrichen, die aus den übrigen folgen.
    """
    single = []
    for left, right in dependencies:
        for attribute in sorted(right):
            entry = (set(left), {attribute})
            if entry not in single:
                single.append(entry)
    reduced = []
    for left, right in single:
        current = set(left)
        for attribute in sorted(left):
            smaller = current - {attribute}
            if smaller and set(right) <= closure(smaller, single):
                current = smaller
        reduced.append((current, set(right)))
    final = list(reduced)
    for entry in list(reduced):
        rest = [other for other in final if other is not entry]
        if rest and implies(rest, entry):
            final = rest
    return [(frozenset(left), frozenset(right)) for left, right in final]


def trivial(dependency):
    """Sagt, ob eine Abhängigkeit trivial ist, die rechte Seite also links steht."""
    left, right = dependency
    return set(right) <= set(left)
