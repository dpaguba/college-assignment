"""Teilfaktorielle Versuchspläne und ihre Vermengungen."""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "full-factorial"))

import full_factorial


def design(factors, generators):
    """Baut einen Plan, in dem einige Spalten aus anderen erzeugt werden.

    Args:
        factors: Gesamtzahl der Faktoren.
        generators: Abbildung von der erzeugten Spalte auf die Faktoren,
            deren Produkt sie ist.

    Returns:
        Liste der Versuche als Vorzeichentupel.

    Raises:
        ValueError: wenn ein Erzeuger auf eine erzeugte Spalte verweist.
    """
    base = factors - len(generators)
    for column, sources in generators.items():
        if any(source in generators for source in sources):
            raise ValueError("Erzeuger verweist auf eine erzeugte Spalte")
        if column < base:
            raise ValueError("erzeugte Spalte liegt im Grundplan")
    rows = []
    for row in full_factorial.design(base):
        full = list(row) + [0] * len(generators)
        for column, sources in generators.items():
            value = 1
            for source in sources:
                value *= row[source]
            full[column] = value
        rows.append(tuple(full))
    return rows


def defining_relation(generators):
    """Nennt die Beziehung, die den Plan festlegt.

    Wird die Spalte D als Produkt ABC erzeugt, so ist ABCD gleich der
    Einsspalte; diese Beziehung erzeugt alle Vermengungen.
    """
    words = []
    for column, sources in generators.items():
        words.append(tuple(sorted(tuple(sources) + (column,))))
    return words


def aliases(factors, generators):
    """Bestimmt, welche Effekte nicht voneinander zu trennen sind.

    Zwei Effekte sind vermengt, wenn ihre Spalten im Plan gleich sind.

    Returns:
        Sortierte Liste von Paaren vermengter Effekte.
    """
    matrix = design(factors, generators)
    columns = {}
    for size in range(1, factors + 1):
        for combination in itertools.combinations(range(factors), size):
            key = tuple(full_factorial.interaction_column(matrix, combination))
            columns.setdefault(key, []).append(combination)
    pairs = []
    for group in columns.values():
        for first, second in itertools.combinations(sorted(group), 2):
            pairs.append((first, second))
    return sorted(pairs)


def resolution(factors, generators):
    """Bestimmt die Auflösung des Plans.

    Die Auflösung ist die Länge des kürzesten Wortes der definierenden
    Beziehung: bei IV sind Haupteffekte mit Dreifachwechselwirkungen und
    Zweifachwechselwirkungen untereinander vermengt.
    """
    words = defining_relation(generators)
    return min(len(word) for word in words)


def helicopter_plan():
    """Stellt den Plan der Aufgabe 6.4 für den Papierhubschrauber auf.

    Vier Faktoren ergäben vollfaktoriell 16 Versuche; mit D = ABC bleiben
    acht, und der Plan hat die Auflösung IV.

    Returns:
        Abbildung mit beiden Umfängen, der Auflösung und dem Plan.
    """
    generators = {3: (0, 1, 2)}
    matrix = design(4, generators)
    return {"full factorial": 16, "chosen": len(matrix),
            "resolution": resolution(4, generators),
            "generator": "D = ABC", "matrix": matrix,
            "factors": ["height", "wing width", "wing length", "weight"]}


def aliased_columns_are_equal():
    """Prüft, dass vermengte Effekte im Plan wirklich dieselbe Spalte haben.

    Damit ist gezeigt, was Vermengung bedeutet: kein Versuchsergebnis
    kann die beiden Effekte auseinanderhalten.
    """
    generators = {3: (0, 1, 2)}
    matrix = design(4, generators)
    for first, second in aliases(4, generators):
        left = full_factorial.interaction_column(matrix, first)
        right = full_factorial.interaction_column(matrix, second)
        if left != right:
            return False
    return True


def solution_types():
    """Nennt die Auflösungen und was sie noch trennen können."""
    return {"III": "main effects confounded with two factor interactions",
            "IV": "main effects clear, two factor interactions confounded "
                  "with each other",
            "V": "main effects and two factor interactions clear"}
