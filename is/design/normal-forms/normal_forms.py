"""Normalformen: erste bis Boyce-Codd."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "functional-dependencies"))

import functional_dependencies as fds


def is_first(rows):
    """Prüft die erste Normalform: jeder Wert ist atomar.

    Args:
        rows: Tupel der Relation.

    Returns:
        Falsch, sobald ein Wert eine Liste, Menge oder ein Tupel ist.
    """
    for row in rows:
        for value in row:
            if isinstance(value, (list, set, tuple, dict)):
                return False
    return True


def _key_attributes(attributes, dependencies):
    """Sammelt alle Attribute, die in irgendeinem Schlüssel vorkommen."""
    keys = fds.candidate_keys(attributes, dependencies)
    primes = set()
    for key in keys:
        primes |= key
    return keys, primes


def is_second(attributes, dependencies):
    """Prüft die zweite Normalform.

    Verletzt ist sie, wenn ein Nichtschlüsselattribut schon von einem
    echten Teil eines Schlüssels abhängt.
    """
    attributes = set(attributes)
    keys, primes = _key_attributes(attributes, dependencies)
    for key in keys:
        for size in range(1, len(key)):
            for subset in _subsets(key, size):
                for attribute in fds.closure(subset, dependencies) - subset:
                    if attribute not in primes:
                        return False
    return True


def is_third(attributes, dependencies):
    """Prüft die dritte Normalform.

    Erlaubt ist eine nichttriviale Abhängigkeit nur, wenn ihre linke
    Seite Superschlüssel ist oder ihre rechte Seite aus
    Schlüsselattributen besteht.
    """
    attributes = set(attributes)
    _, primes = _key_attributes(attributes, dependencies)
    for left, right in dependencies:
        for attribute in set(right) - set(left):
            if fds.closure(left, dependencies) == attributes:
                continue
            if attribute in primes:
                continue
            return False
    return True


def is_bcnf(attributes, dependencies):
    """Prüft die Boyce-Codd-Normalform.

    Hier muss jede nichttriviale linke Seite Superschlüssel sein; die
    Ausnahme für Schlüsselattribute entfällt.
    """
    attributes = set(attributes)
    for left, right in dependencies:
        if set(right) <= set(left):
            continue
        if fds.closure(left, dependencies) != attributes:
            return False
    return True


def hierarchy():
    """Nennt die Normalformen in aufsteigender Strenge."""
    return ["1NF", "2NF", "3NF", "BCNF"]


def anomalies():
    """Nennt die drei Anomalien, gegen die die Normalisierung wirkt."""
    return ["insert", "update", "delete"]


def _subsets(values, size):
    """Erzeugt alle Teilmengen gegebener Größe als Mengen."""
    from itertools import combinations
    return [set(subset) for subset in combinations(sorted(values), size)]
