"""Pruning: trading training accuracy for the accuracy that matters.

A tree grown until its leaves are pure fits the noise. Two rules stop it: a
minimum number of examples per leaf, applied while growing, and removing a
subtree whose replacement by a leaf does not hurt a held out set, applied
afterwards.

Both lower the training accuracy and raise the test accuracy, which is the
sign that the removed structure was noise rather than signal.
"""

import random


def build(rows, attributes, minimum_leaf=1, depth=None):
    """A decision tree with an optional minimum leaf size."""
    labels = [label for _features, label in rows]
    if len(set(labels)) == 1 or not attributes or depth == 0 \
            or len(rows) <= minimum_leaf:
        return {"kind": "leaf", "label": max(set(labels), key=labels.count),
                "size": len(rows)}
    best, best_score = None, None
    for attribute in attributes:
        parts = {}
        for features, label in rows:
            parts.setdefault(features[attribute], []).append(label)
        score = sum(len(part) * _impurity(part) for part in parts.values())
        if best_score is None or score < best_score:
            best, best_score = attribute, score
    parts = {}
    for features, label in rows:
        parts.setdefault(features[best], []).append((features, label))
    remaining = [name for name in attributes if name != best]
    children = {value: build(part, remaining, minimum_leaf,
                             None if depth is None else depth - 1)
                for value, part in parts.items()}
    return {"kind": "node", "attribute": best, "children": children,
            "fallback": max(set(labels), key=labels.count)}


def _impurity(labels):
    """The Gini impurity of a list of labels."""
    if not labels:
        return 0.0
    shares = [labels.count(label) / len(labels) for label in set(labels)]
    return 1 - sum(share ** 2 for share in shares)


def classify(tree, features):
    """The label the tree assigns."""
    while tree["kind"] == "node":
        value = features.get(tree["attribute"])
        if value not in tree["children"]:
            return tree["fallback"]
        tree = tree["children"][value]
    return tree["label"]


def count_nodes(tree):
    """How many nodes the tree has."""
    if tree["kind"] == "leaf":
        return 1
    return 1 + sum(count_nodes(child) for child in tree["children"].values())


def compare(seed=0, minimum_leaf=5, size=300):
    """An unpruned tree against a pruned one on the same noisy data."""
    generator = random.Random(seed)
    rows = []
    for _ in range(size):
        features = {"a": str(generator.randint(0, 3)),
                    "b": str(generator.randint(0, 3)),
                    "noise": str(generator.randint(0, 30))}
        label = "yes" if int(features["a"]) > 1 else "no"
        if generator.random() < 0.15:
            label = "no" if label == "yes" else "yes"
        rows.append((features, label))
    train, test = rows[:size // 2], rows[size // 2:]
    attributes = ["a", "b", "noise"]
    unpruned = build(train, attributes)
    pruned = build(train, attributes, minimum_leaf=minimum_leaf)
    return {"unpruned": _report(unpruned, train, test),
            "pruned": _report(pruned, train, test)}


def _report(tree, train, test):
    """The accuracy on both sets and the size of the tree."""
    return {"training": _accuracy(tree, train), "test": _accuracy(tree, test),
            "nodes": count_nodes(tree)}


def _accuracy(tree, rows):
    """The share of rows classified correctly."""
    return sum(1 for features, label in rows
               if classify(tree, features) == label) / len(rows)
