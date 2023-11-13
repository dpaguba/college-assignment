"""Random forests: bagging plus a second source of randomness.

Bagging alone leaves the trees correlated, because a dominant feature is
chosen first by nearly every tree. Restricting each split to a random subset
of the features breaks that, and the average of less correlated trees has
lower variance than the average of similar ones.

The out-of-bag estimate is the third ingredient. Each tree is tested on the
third of the data it never saw, so the forest evaluates itself without a
separate test set, and the module checks that the estimate lands near the
test accuracy.
"""

import random


def ingredients():
    """What the method combines."""
    return ["bootstrap samples", "random feature subsets", "majority vote"]


def correlation_effect(seed=0, trees=20, size=200):
    """How correlated the trees are with and without feature subsets."""
    generator = random.Random(seed)
    data = []
    for _ in range(size):
        strong = generator.randint(0, 1)
        weak = generator.randint(0, 1)
        label = strong if generator.random() < 0.9 else 1 - strong
        data.append(({"strong": strong, "weak": weak, "noise":
                      generator.randint(0, 5)}, label))
    chosen_without = []
    chosen_with = []
    for index in range(trees):
        sample = [generator.choice(data) for _ in data]
        chosen_without.append(_first_split(sample, ["strong", "weak", "noise"]))
        subset = generator.sample(["strong", "weak", "noise"], 2)
        chosen_with.append(_first_split(sample, subset))
    return {"without subsets": _agreement(chosen_without),
            "with subsets": _agreement(chosen_with)}


def _first_split(rows, attributes):
    """The attribute a tree would split on first."""
    best, best_score = None, None
    for attribute in attributes:
        parts = {}
        for features, label in rows:
            parts.setdefault(features[attribute], []).append(label)
        score = sum(len(part) * _impurity(part) for part in parts.values())
        if best_score is None or score < best_score:
            best, best_score = attribute, score
    return best


def _impurity(labels):
    """The Gini impurity."""
    if not labels:
        return 0.0
    shares = [labels.count(label) / len(labels) for label in set(labels)]
    return 1 - sum(share ** 2 for share in shares)


def _agreement(choices):
    """The share of trees that made the most common choice."""
    return max(choices.count(choice) for choice in set(choices)) / len(choices)


def out_of_bag(seed=0, trees=15, size=200):
    """The out-of-bag accuracy against a held out test set."""
    generator = random.Random(seed)
    data = []
    for _ in range(size):
        value = generator.randint(0, 9)
        label = 1 if value > 4 else 0
        if generator.random() < 0.1:
            label = 1 - label
        data.append(((value,), label))
    train, test = data[:size // 2], data[size // 2:]
    votes = {index: [] for index in range(len(train))}
    models = []
    for _ in range(trees):
        indices = [generator.randrange(len(train)) for _ in train]
        sample = [train[index] for index in indices]
        threshold = sum(point[0][0] for point in sample) / len(sample)
        models.append(threshold)
        for index in range(len(train)):
            if index not in indices:
                votes[index].append(1 if train[index][0][0] > threshold else 0)
    correct = 0
    counted = 0
    for index, cast in votes.items():
        if not cast:
            continue
        counted += 1
        prediction = 1 if sum(cast) * 2 >= len(cast) else 0
        correct += int(prediction == train[index][1])
    test_correct = 0
    for point, label in test:
        cast = [1 if point[0] > threshold else 0 for threshold in models]
        prediction = 1 if sum(cast) * 2 >= len(cast) else 0
        test_correct += int(prediction == label)
    return {"out of bag accuracy": correct / counted if counted else 0.0,
            "test accuracy": test_correct / len(test)}
