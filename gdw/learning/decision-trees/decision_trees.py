"""Decision trees: greedy splitting by information gain.

At each node the attribute with the largest information gain is chosen, the
data is split, and the procedure repeats. Nothing looks ahead, so the tree is
greedy and can be beaten by a different first split, and nothing stops it
before the leaves are pure, so it fits the training data exactly.

That last property is the one the module measures. An unlimited tree reaches
perfect training accuracy and lower test accuracy; limiting the depth
narrows the gap, which is the standard picture of overfitting and the reason
pruning exists.
"""

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "entropy"))
import entropy


def best_attribute(rows, attributes):
    """The attribute whose split removes the most entropy."""
    labels = [label for _features, label in rows]
    best, best_gain = None, None
    for attribute in attributes:
        parts = {}
        for features, label in rows:
            parts.setdefault(features[attribute], []).append(label)
        gain = entropy.information_gain(labels, list(parts.values()))
        if best_gain is None or gain > best_gain:
            best, best_gain = attribute, gain
    return best


def build(rows, attributes, depth=None):
    """The tree, split greedily until the labels are pure or nothing is left."""
    labels = [label for _features, label in rows]
    if len(set(labels)) == 1:
        return {"kind": "leaf", "label": labels[0]}
    if not attributes or depth == 0:
        return {"kind": "leaf", "label": max(set(labels), key=labels.count)}
    attribute = best_attribute(rows, attributes)
    parts = {}
    for features, label in rows:
        parts.setdefault(features[attribute], []).append((features, label))
    remaining = [name for name in attributes if name != attribute]
    children = {value: build(part, remaining,
                             None if depth is None else depth - 1)
                for value, part in parts.items()}
    return {"kind": "node", "attribute": attribute, "children": children,
            "fallback": max(set(labels), key=labels.count)}


def classify(tree, features):
    """The label the tree gives to a row."""
    while tree["kind"] == "node":
        value = features.get(tree["attribute"])
        if value not in tree["children"]:
            return tree["fallback"]
        tree = tree["children"][value]
    return tree["label"]


def overfitting_example(seed=0, depth=None, size=200):
    """Training and test accuracy of a tree grown on noisy data."""
    generator = random.Random(seed)
    rows = []
    for _ in range(size):
        features = {"a": generator.randint(0, 4), "b": generator.randint(0, 4),
                    "noise": generator.randint(0, 20)}
        label = 1 if features["a"] > 2 else 0
        if generator.random() < 0.1:
            label = 1 - label
        rows.append((features, label))
    split = size // 2
    train, test = rows[:split], rows[split:]
    tree = build(train, ["a", "b", "noise"], depth)
    return {"training accuracy": _accuracy(tree, train),
            "test accuracy": _accuracy(tree, test)}


def _accuracy(tree, rows):
    """The share of rows the tree labels correctly."""
    correct = sum(1 for features, label in rows
                  if classify(tree, features) == label)
    return correct / len(rows)
