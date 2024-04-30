"""Entscheidungsbäume nach ID3 auf der Personentabelle der Übung."""

import math

ATTRIBUTES = ["Geschlecht", "Brille", "Alter", "Haarfarbe", "Bart",
              "Accessoire"]

ROWS = [
    ("David", "m", "ja", "jung", "blond", "kein", "kein"),
    ("Albert", "m", "nein", "jung", "schwarz", "kein", "Ohrringe"),
    ("Philipp", "m", "nein", "alt", "schwarz", "Schnauzer", "kein"),
    ("Ingrid", "f", "ja", "jung", "braun", "kein", "Haarband"),
    ("Tina", "f", "nein", "jung", "blond", "kein", "Ohrringe"),
    ("Stefan", "m", "nein", "alt", "grau", "Schnauzer", "kein"),
    ("Elke", "f", "ja", "jung", "schwarz", "kein", "Ohrringe"),
    ("Tina", "f", "nein", "jung", "blond", "kein", "Haarband"),
    ("Markus", "m", "nein", "alt", "grau", "Vollbart", "kein"),
    ("Joerg", "m", "nein", "jung", "braun", "kein", "Muetze"),
    ("Patrick", "m", "nein", "jung", "braun", "kein", "Hut"),
    ("Alfred", "m", "nein", "alt", "rot", "Schnauzer", "kein"),
    ("Thomas", "m", "nein", "jung", "blond", "kein", "kein"),
    ("Oliver", "m", "nein", "jung", "blond", "kein", "Muetze"),
    ("Peter", "m", "nein", "jung", "braun", "kein", "kein"),
    ("Klaus", "m", "ja", "alt", "braun", "Schnauzer", "kein"),
    ("Hannes", "m", "nein", "alt", "schwarz", "Schnauzer", "kein"),
    ("Simone", "f", "ja", "jung", "rot", "kein", "Haarband"),
    ("Ute", "f", "nein", "jung", "blond", "kein", "Ohrringe"),
    ("Michael", "m", "ja", "alt", "grau", "Vollbart", "kein"),
    ("Doris", "f", "nein", "jung", "rot", "kein", "Haarband"),
    ("Andreas", "m", "ja", "alt", "grau", "Schnauzer", "kein"),
    ("Tobias", "m", "ja", "jung", "schwarz", "kein", "kein"),
    ("Manfred", "m", "nein", "alt", "grau", "Schnauzer", "Monokel"),
]


def people():
    """Liefert die Tabelle der Übung als Liste von Abbildungen."""
    rows = []
    for entry in ROWS:
        row = {"Name": entry[0]}
        row.update(dict(zip(ATTRIBUTES, entry[1:])))
        rows.append(row)
    return rows


def entropy(labels):
    """Berechnet die Entropie einer Werteliste in Bit.

    Raises:
        ValueError: bei einer leeren Liste.
    """
    if not labels:
        raise ValueError("leere Liste")
    total = len(labels)
    value = 0.0
    for label in set(labels):
        share = labels.count(label) / total
        value -= share * math.log2(share)
    return value


def split(rows, attribute):
    """Teilt die Zeilen nach den Werten eines Merkmals auf."""
    parts = {}
    for row in rows:
        parts.setdefault(row[attribute], []).append(row)
    return parts


def information_gain(rows, attribute, target="Name"):
    """Berechnet den Erfahrungsgewinn eines Merkmals.

    Der Gewinn ist die Entropie vor der Aufteilung abzüglich der mit den
    Gruppengrössen gewichteten Entropien danach.
    """
    before = entropy([row[target] for row in rows])
    after = 0.0
    for part in split(rows, attribute).values():
        after += (len(part) / len(rows)) * entropy([row[target]
                                                    for row in part])
    return before - after


def attribute_report(attribute, rows=None, target="Name"):
    """Stellt Teilentropien und Gewinn eines Merkmals zusammen.

    Returns:
        Abbildung mit der Gesamtentropie, den Gruppen und dem Gewinn.
    """
    if rows is None:
        rows = people()
    parts = {}
    for value, group in split(rows, attribute).items():
        parts[value] = {"count": len(group),
                        "entropy": entropy([row[target] for row in group])}
    return {"total": entropy([row[target] for row in rows]),
            "parts": parts,
            "gain": information_gain(rows, attribute, target)}


def best_attribute(rows=None, attributes=None, target="Name"):
    """Sucht das Merkmal mit dem grössten Erfahrungsgewinn.

    Returns:
        Abbildung mit dem Merkmal, seinem Gewinn und der Rangliste.
    """
    if rows is None:
        rows = people()
    if attributes is None:
        attributes = ATTRIBUTES
    ranking = sorted(((information_gain(rows, attribute, target), attribute)
                      for attribute in attributes), reverse=True)
    return {"attribute": ranking[0][1], "gain": ranking[0][0],
            "ranking": [(name, gain) for gain, name in ranking]}


def id3(rows, target="Name", attributes=None):
    """Baut einen Entscheidungsbaum nach ID3.

    In jedem Knoten wird das Merkmal mit dem grössten Erfahrungsgewinn
    gewählt; die Rekursion endet, wenn alle Zeilen dasselbe Ziel tragen
    oder kein Merkmal mehr übrig ist.

    Returns:
        Ein Blatt als Abbildung mit ``leaf`` oder ein Knoten mit
        ``attribute`` und ``children``.

    Raises:
        ValueError: bei einer leeren Zeilenmenge.
    """
    if not rows:
        raise ValueError("keine Zeilen")
    if attributes is None:
        attributes = list(ATTRIBUTES)
    labels = [row[target] for row in rows]
    if len(set(labels)) == 1:
        return {"leaf": labels[0], "rows": len(rows)}
    if not attributes:
        return {"leaf": max(set(labels), key=labels.count),
                "rows": len(rows), "impure": True}
    chosen = best_attribute(rows, attributes, target)["attribute"]
    remaining = [name for name in attributes if name != chosen]
    children = {}
    for value, part in split(rows, chosen).items():
        children[value] = id3(part, target, remaining)
    return {"attribute": chosen, "children": children, "rows": len(rows)}


def classify(tree, row):
    """Führt eine Zeile durch den Baum bis zu einem Blatt."""
    while "leaf" not in tree:
        value = row[tree["attribute"]]
        if value not in tree["children"]:
            return None
        tree = tree["children"][value]
    return tree["leaf"]


def accuracy(tree, rows, target="Name"):
    """Anteil der Zeilen, die der Baum richtig einordnet."""
    correct = sum(1 for row in rows if classify(tree, row) == row[target])
    return correct / len(rows)


def identifiable(rows=None):
    """Prüft, ob die Merkmale jede Person auseinanderhalten.

    Zwei Zeilen mit gleichen Merkmalen und verschiedenen Namen können von
    keinem Baum getrennt werden, gleich welches Merkmal er wählt.

    Returns:
        Abbildung mit der Antwort und den Namenspaaren, die zusammenfallen.
    """
    if rows is None:
        rows = people()
    seen = {}
    for row in rows:
        key = tuple(row[attribute] for attribute in ATTRIBUTES)
        seen.setdefault(key, []).append(row["Name"])
    collisions = [sorted(set(names)) for names in seen.values()
                  if len(set(names)) > 1]
    return {"all identifiable": not collisions, "collisions": collisions,
            "distinct names": len({row["Name"] for row in rows}),
            "rows": len(rows)}


def partition_kind():
    """Beschreibt, wie ein Baum den Merkmalsraum zerlegt.

    Jeder Test betrifft ein Merkmal, deshalb verlaufen die Schnitte
    parallel zu den Achsen; eine schräge Trennlinie muss ein Baum durch
    viele Stufen annähern.
    """
    return "axis parallel"
