"""Viele Bäume statt eines."""

import math

import numpy as np


def vote(labels):
    """Nennt die häufigste Klasse, bei Gleichstand die erste genannte.

    Raises:
        ValueError: bei einer leeren Abstimmung.
    """
    if not labels:
        raise ValueError("leere Abstimmung")
    counted = {}
    for label in labels:
        counted[label] = counted.get(label, 0) + 1
    best = max(counted.values())
    for label in labels:
        if counted[label] == best:
            return label
    return None


def out_of_bag(size=1000, seed=0):
    """Misst, welcher Anteil einer Stichprobe beim Ziehen aussen bleibt.

    Beim Ziehen mit Zurücklegen bleibt ein Punkt mit der
    Wahrscheinlichkeit eins minus eins durch n hoch n aussen, und das
    strebt gegen eins durch e, also gut ein Drittel. Diese Punkte sind
    für den jeweiligen Baum ungesehene Daten und lassen sich zum Messen
    verwenden, ohne dass etwas zurückgehalten werden muss.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    if size <= 0:
        raise ValueError("die Grösse muss positiv sein")
    rng = np.random.default_rng(seed)
    drawn = rng.integers(0, size, size=size)
    left = size - len(set(drawn.tolist()))
    return {"size": size, "measured share left out": left / size,
            "expected share left out": (1.0 - 1.0 / size) ** size,
            "limit": 1.0 / math.e,
            "what it is used for": "messen ohne zurückgehaltene Daten"}


def _gini(labels):
    """Der Gini-Index."""
    counted = {}
    for label in labels:
        counted[label] = counted.get(label, 0) + 1
    total = len(labels)
    return 1.0 - sum((count / total) ** 2 for count in counted.values())


def _grow_tree(points, labels, depth, features, rng):
    """Baut einen Baum auf einer Auswahl der Merkmale."""
    counted = {}
    for label in labels:
        counted[label] = counted.get(label, 0) + 1
    majority = max(counted, key=lambda name: (counted[name], name))
    if depth == 0 or len(counted) == 1:
        return {"leaf": majority}
    chosen = rng.choice(points.shape[1],
                        size=min(features, points.shape[1]),
                        replace=False)
    before = _gini(labels)
    best = None
    for feature in chosen:
        values = np.unique(points[:, feature])
        for one, two in zip(values, values[1:]):
            threshold = (one + two) / 2.0
            mask = points[:, feature] <= threshold
            left = [label for label, keep in zip(labels, mask) if keep]
            right = [label for label, keep in zip(labels, mask)
                     if not keep]
            if not left or not right:
                continue
            after = (len(left) * _gini(left)
                     + len(right) * _gini(right)) / len(labels)
            if best is None or before - after > best[0]:
                best = (before - after, int(feature), float(threshold),
                        mask)
    if best is None:
        return {"leaf": majority}
    _, feature, threshold, mask = best
    return {"feature": feature, "threshold": threshold,
            "left": _grow_tree(points[mask],
                               [label for label, keep in zip(labels, mask)
                                if keep], depth - 1, features, rng),
            "right": _grow_tree(points[~mask],
                                [label for label, keep in zip(labels, mask)
                                 if not keep], depth - 1, features, rng)}


def _classify(tree, point):
    """Führt einen Punkt durch einen Baum."""
    while "leaf" not in tree:
        tree = (tree["left"] if point[tree["feature"]] <= tree["threshold"]
                else tree["right"])
    return tree["leaf"]


def grow_forest(points, labels, trees=20, depth=6, features=1, seed=0):
    """Baut einen Wald aus Bäumen auf gezogenen Stichproben.

    Zwei Quellen des Zufalls: jede Stichprobe wird mit Zurücklegen
    gezogen, und an jedem Knoten steht nur eine Auswahl der Merkmale zur
    Verfügung. Beides dient demselben Zweck, nämlich die Bäume
    verschieden zu machen; gleiche Bäume mitteln sich nicht heraus.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Bäumen oder
            unpassend vielen Klassen.
    """
    if trees <= 0:
        raise ValueError("es braucht mindestens einen Baum")
    field = np.asarray(points, dtype=float)
    if len(field) != len(labels):
        raise ValueError("zu jedem Punkt gehört eine Klasse")
    rng = np.random.default_rng(seed)
    forest = []
    for _ in range(trees):
        drawn = rng.integers(0, len(field), size=len(field))
        forest.append(_grow_tree(field[drawn],
                                 [labels[index] for index in drawn],
                                 depth, features, rng))
    return forest


def classify_forest(forest, point):
    """Lässt den Wald abstimmen."""
    return vote([_classify(tree, point) for tree in forest])


def _data(points=200, noise=0.15, seed=0):
    """Zwei Klassen mit einer krummen Grenze und etwas Rauschen."""
    rng = np.random.default_rng(seed)
    cloud = rng.uniform(-1.0, 1.0, size=(points, 2))
    labels = ["a" if row[1] > 0.6 * row[0] ** 2 - 0.2 else "b"
              for row in cloud]
    for index in range(len(labels)):
        if rng.random() < noise:
            labels[index] = "a" if labels[index] == "b" else "b"
    return cloud, labels


def forest_versus_tree(trees=25, depth=6, seed=0):
    """Vergleicht den Wald mit seinen eigenen Bäumen.

    Gemessen wird auf frischen Daten aus derselben Quelle. Der Wald
    schlägt den mittleren Baum, weil sich die unabhängigen Fehler
    teilweise auslöschen; wie stark, hängt daran, wie verschieden die
    Bäume sind.

    Returns:
        Abbildung mit beiden Fehlerraten und der Uneinigkeit.
    """
    points, labels = _data(seed=seed)
    fresh, fresh_labels = _data(seed=seed + 100)
    forest = grow_forest(points, labels, trees=trees, depth=depth,
                         seed=seed)
    single = [np.mean([_classify(tree, point) != label
                       for point, label in zip(fresh, fresh_labels)])
              for tree in forest]
    together = np.mean([classify_forest(forest, point) != label
                        for point, label in zip(fresh, fresh_labels)])
    disagreement = np.mean([len({_classify(tree, point)
                                 for tree in forest}) > 1
                            for point in fresh])
    return {"forest error": float(together),
            "mean tree error": float(np.mean(single)),
            "best tree error": float(np.min(single)),
            "disagreement between trees": float(disagreement),
            "trees": trees}


def over_sizes(sizes=(1, 3, 7, 15, 31, 63), seed=0):
    """Misst die Fehlerrate über die Grösse des Waldes.

    Returns:
        Liste mit einer Zeile je Grösse.
    """
    points, labels = _data(seed=seed)
    fresh, fresh_labels = _data(seed=seed + 100)
    found = []
    for size in sizes:
        forest = grow_forest(points, labels, trees=size, seed=seed)
        error = np.mean([classify_forest(forest, point) != label
                         for point, label in zip(fresh, fresh_labels)])
        found.append({"trees": size, "error": float(error)})
    return found


def why_two_sources_of_chance():
    """Sagt, wozu Stichprobe und Merkmalsauswahl beide nötig sind.

    Das Ziehen mit Zurücklegen allein reicht nicht: gibt es ein sehr
    starkes Merkmal, so wählen fast alle Bäume es an der Wurzel, und
    dann sehen sie einander sehr ähnlich. Ihre Fehler sind dann
    verbunden, und Mitteln bringt wenig. Die Auswahl der Merkmale an
    jedem Knoten zwingt einen Teil der Bäume, ohne das starke Merkmal
    auszukommen, und erst das macht sie wirklich verschieden.
    """
    return {"bagging alone": "ein starkes Merkmal steht in fast jedem "
                             "Baum an der Wurzel",
            "why that hurts": "verbundene Fehler mitteln sich nicht "
                              "heraus",
            "why two sources": "erst die Merkmalsauswahl macht die Bäume "
                               "wirklich verschieden",
            "the price": "jeder einzelne Baum wird schwächer"}
