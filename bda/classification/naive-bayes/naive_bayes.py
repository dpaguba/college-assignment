"""Naive Bayes: an assumption known to be false that works anyway.

The classifier multiplies the class prior by the likelihood of each feature
given the class, as though the features were independent. They usually are
not, and the classifier is usually still accurate, because the decision needs
only the ranking of the classes and not the correctness of the probabilities.

Smoothing is the part that cannot be skipped. Without it, one unseen feature
value makes the whole product zero and the class impossible, whatever the
other features say.
"""

import random


def fit(rows, smoothing=1.0):
    """The priors and the conditional counts of a training set."""
    classes = {}
    counts = {}
    values = {}
    for features, label in rows:
        classes[label] = classes.get(label, 0) + 1
        for name, value in features.items():
            counts.setdefault((label, name, value), 0)
            counts[(label, name, value)] += 1
            values.setdefault(name, set()).add(value)
    total = len(rows)
    return {"priors": {label: count / total for label, count in classes.items()},
            "counts": counts, "class counts": classes, "values": values,
            "smoothing": smoothing}


def probability(model, features, label):
    """The unnormalised probability of a class given the features."""
    result = model["priors"].get(label, 0.0)
    smoothing = model["smoothing"]
    for name, value in features.items():
        seen = len(model["values"].get(name, ())) or 1
        numerator = model["counts"].get((label, name, value), 0) + smoothing
        denominator = model["class counts"].get(label, 0) + smoothing * seen
        result *= numerator / denominator if denominator else 0.0
    return result


def classify(model, features):
    """The class with the largest probability."""
    return max(model["priors"], key=lambda label: probability(model, features,
                                                              label))


def correlated_features_example(seed=0, size=400):
    """A data set whose features are strongly correlated.

    The independence assumption is badly violated and the classifier is still
    accurate, which is the observation the lecture makes: the assumption
    affects the probabilities and rarely the ranking.
    """
    generator = random.Random(seed)
    rows = []
    firsts, seconds = [], []
    for _ in range(size):
        label = generator.choice(["a", "b"])
        base = 1 if label == "a" else 0
        first = base if generator.random() < 0.9 else 1 - base
        second = first if generator.random() < 0.95 else 1 - first
        rows.append(({"x": str(first), "y": str(second)}, label))
        firsts.append(first)
        seconds.append(second)
    model = fit(rows[:size // 2])
    correct = sum(1 for features, label in rows[size // 2:]
                  if classify(model, features) == label)
    mean_first = sum(firsts) / size
    mean_second = sum(seconds) / size
    numerator = sum((a - mean_first) * (b - mean_second)
                    for a, b in zip(firsts, seconds))
    left = sum((a - mean_first) ** 2 for a in firsts) ** 0.5
    right = sum((b - mean_second) ** 2 for b in seconds) ** 0.5
    return {"accuracy": correct / (size - size // 2),
            "correlation": numerator / (left * right)}
