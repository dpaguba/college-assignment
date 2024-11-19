"""Rekursive Teilung der Daten."""

import math

import numpy as np

MEASURES = ("gini", "entropy")


def _counts(labels):
    """Zählt die Klassen.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    if len(labels) == 0:
        raise ValueError("leere Menge")
    counted = {}
    for label in labels:
        counted[label] = counted.get(label, 0) + 1
    return counted


def gini(labels):
    """Der Gini-Index einer Menge von Klassen.

    Er misst, wie oft ein zufällig gezogenes Element falsch benannt
    würde, wenn man es nach der Klassenverteilung rät. Null heisst rein.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    counted = _counts(labels)
    total = len(labels)
    return 1.0 - sum((count / total) ** 2 for count in counted.values())


def entropy(labels):
    """Die Entropie einer Menge von Klassen, in Bit.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    counted = _counts(labels)
    total = len(labels)
    return -sum((count / total) * math.log2(count / total)
                for count in counted.values())


def _impurity(labels, measure):
    """Wählt das Mass.

    Raises:
        ValueError: bei einem unbekannten Mass.
    """
    if measure == "gini":
        return gini(labels)
    if measure == "entropy":
        return entropy(labels)
    raise ValueError("unbekanntes Mass: %s" % measure)


def best_split(points, labels, measure="gini"):
    """Sucht die beste Teilung über die Mitten zwischen den Werten.

    Für jedes Merkmal werden die vorkommenden Werte sortiert und die
    Mitten zwischen benachbarten als Schwelle geprüft. Andere Schwellen
    ändern die Teilung nicht, also genügt diese Liste.

    Returns:
        Abbildung mit Merkmal, Schwelle und Gewinn.

    Raises:
        ValueError: bei einem unbekannten Mass oder unpassend vielen
            Klassen.
    """
    field = np.asarray(points, dtype=float)
    if len(field) != len(labels):
        raise ValueError("zu jedem Punkt gehört eine Klasse")
    before = _impurity(labels, measure)
    best = {"feature": None, "threshold": None, "gain": 0.0}
    for feature in range(field.shape[1]):
        values = np.unique(field[:, feature])
        for one, two in zip(values, values[1:]):
            threshold = (one + two) / 2.0
            left = [label for value, label in zip(field[:, feature],
                                                  labels)
                    if value <= threshold]
            right = [label for value, label in zip(field[:, feature],
                                                   labels)
                     if value > threshold]
            if not left or not right:
                continue
            after = (len(left) * _impurity(left, measure)
                     + len(right) * _impurity(right, measure)) / len(labels)
            if before - after > best["gain"] + 1e-12:
                best = {"feature": feature, "threshold": float(threshold),
                        "gain": before - after}
    return best


def best_split_by_search(points, labels, measure="gini", steps=400):
    """Sucht dieselbe Teilung über ein feines Gitter von Schwellen.

    Diese Rechnung weiss nichts von Mitten zwischen Werten; sie probiert
    Schwellen gleichmässig über den Wertebereich. Verglichen werden
    Merkmal, Gewinn und die erzeugte Teilung, nicht die Zahl der
    Schwelle: zwei Schwellen zwischen denselben Nachbarwerten trennen
    dieselben Punkte.

    Raises:
        ValueError: bei einem unbekannten Mass.
    """
    field = np.asarray(points, dtype=float)
    before = _impurity(labels, measure)
    best = {"feature": None, "threshold": None, "gain": 0.0}
    for feature in range(field.shape[1]):
        low = float(field[:, feature].min())
        high = float(field[:, feature].max())
        for step in range(steps + 1):
            threshold = low + (high - low) * step / steps
            left = [label for value, label in zip(field[:, feature],
                                                  labels)
                    if value <= threshold]
            right = [label for value, label in zip(field[:, feature],
                                                   labels)
                     if value > threshold]
            if not left or not right:
                continue
            after = (len(left) * _impurity(left, measure)
                     + len(right) * _impurity(right, measure)) / len(labels)
            if before - after > best["gain"] + 1e-12:
                best = {"feature": feature, "threshold": float(threshold),
                        "gain": before - after}
    return best


def same_partition(points, labels, first, second):
    """Sagt, ob zwei Teilungen dieselben Punkte trennen.

    Zwei Schwellen zwischen denselben Nachbarwerten erzeugen dieselbe
    Teilung, obwohl die Zahlen verschieden sind. Verglichen werden
    deshalb die Mengen und nicht die Schwellen.

    Raises:
        ValueError: bei einer Teilung ohne Merkmal.
    """
    if first["feature"] is None or second["feature"] is None:
        raise ValueError("eine der Teilungen hat kein Merkmal")
    field = np.asarray(points, dtype=float)
    left = field[:, first["feature"]] <= first["threshold"]
    right = field[:, second["feature"]] <= second["threshold"]
    return bool(np.array_equal(left, right))


def grow(points, labels, depth=3, measure="gini"):
    """Baut einen Baum bis zu einer festen Tiefe.

    Raises:
        ValueError: bei einer negativen Tiefe oder unpassend vielen
            Klassen.
    """
    if depth < 0:
        raise ValueError("die Tiefe darf nicht negativ sein")
    if len(points) != len(labels):
        raise ValueError("zu jedem Punkt gehört eine Klasse")
    counted = _counts(labels)
    majority = max(counted, key=lambda name: (counted[name], name))
    if depth == 0 or len(counted) == 1:
        return {"leaf": majority, "size": len(labels)}
    split = best_split(points, labels, measure)
    if split["feature"] is None:
        return {"leaf": majority, "size": len(labels)}
    field = np.asarray(points, dtype=float)
    mask = field[:, split["feature"]] <= split["threshold"]
    return {"feature": split["feature"], "threshold": split["threshold"],
            "gain": split["gain"], "size": len(labels),
            "left": grow(field[mask], [label for label, keep
                                       in zip(labels, mask) if keep],
                         depth - 1, measure),
            "right": grow(field[~mask], [label for label, keep
                                         in zip(labels, mask) if not keep],
                          depth - 1, measure)}


def classify(tree, point):
    """Führt einen Punkt durch den Baum bis zu einem Blatt."""
    while "leaf" not in tree:
        tree = (tree["left"] if point[tree["feature"]] <= tree["threshold"]
                else tree["right"])
    return tree["leaf"]


def classify_all(tree, points):
    """Klassifiziert eine ganze Menge."""
    return [classify(tree, point) for point in points]


def leaves(tree):
    """Zählt die Blätter eines Baums."""
    if "leaf" in tree:
        return 1
    return leaves(tree["left"]) + leaves(tree["right"])


def example(points=60, seed=0):
    """Zwei Klassen, getrennt durch eine schräge Grenze mit Überlapp."""
    rng = np.random.default_rng(seed)
    cloud = rng.uniform(-1.0, 1.0, size=(points, 2))
    labels = ["a" if row[0] + row[1] > 0.15 else "b" for row in cloud]
    return cloud, labels


def one_noise_point():
    """Zeigt, was ein einzelner falsch benannter Punkt anrichtet.

    Ein Baum, der bis zur Reinheit wächst, muss auch diesen Punkt
    trennen. Dafür legt er zusätzliche Schnitte an, die mit der
    eigentlichen Grenze nichts zu tun haben, und die verzerren die
    Entscheidung für alle Punkte in der Umgebung. Deshalb wird ein Baum
    beschnitten und nicht bis zum Ende gebaut.

    Returns:
        Abbildung mit der Zahl der Blätter mit und ohne den Punkt.
    """
    points, labels = example()
    clean = grow(points, labels, depth=20)
    spoiled = list(labels)
    spoiled[0] = "a" if spoiled[0] == "b" else "b"
    dirty = grow(points, spoiled, depth=20)
    return {"leaves without it": leaves(clean),
            "leaves with the noise point": leaves(dirty),
            "extra cuts": leaves(dirty) - leaves(clean),
            "why pruning exists": "ein Baum bis zur Reinheit trennt auch "
                                  "das Rauschen"}


def what_a_tree_gives_that_a_number_does_not():
    """Nennt, warum Bäume trotz schwächerer Güte genommen werden.

    Ein Pfad von der Wurzel zu einem Blatt ist eine Regel in Worten, und
    die lässt sich vorlesen und bestreiten. Für Catan heisst das: eine
    Bewertungsfunktion aus einem Baum sagt, warum ein Zug gut ist, und
    ein Netz sagt nur, dass er gut ist. Wer die erste KI von Hand baut,
    hat ohnehin einen Baum geschrieben, nur ohne ihn zu lernen.
    """
    return {"what a tree gives": "eine Regel in Worten je Pfad",
            "what a net gives": "eine Zahl",
            "the connection to the project": "die regelbasierte KI ist "
                                             "ein von Hand geschriebener "
                                             "Baum",
            "the cost": "einzelne Bäume sind schwächer als ein Wald"}
