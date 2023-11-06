"""Why a model decided, and the shortcut it might have taken.

Permutation importance shuffles one feature and measures how much the score
falls: a feature the model relies on costs accuracy when destroyed, and an
irrelevant one costs nothing. A local surrogate fits a simple model near one
point, which explains that prediction and not the model as a whole.

The case that matters is the shortcut: a model can be accurate for the wrong
reason. The module builds a data set where a spurious feature predicts the
label perfectly in training, and the importance measure names it, which is
what an interpretability method is for.
"""

import random


def permutation_importance(seed=0, size=400):
    """How much shuffling each feature costs the accuracy."""
    generator = random.Random(seed)
    data = []
    for _ in range(size):
        important = generator.randint(0, 1)
        irrelevant = generator.randint(0, 1)
        label = important if generator.random() < 0.95 else 1 - important
        data.append(({"important": important, "irrelevant": irrelevant}, label))
    base = _accuracy(data, lambda row: row["important"])
    shuffled_important = _accuracy(_shuffle(data, "important", generator),
                                   lambda row: row["important"])
    shuffled_irrelevant = _accuracy(_shuffle(data, "irrelevant", generator),
                                    lambda row: row["important"])
    return {"base": base, "important": base - shuffled_important,
            "irrelevant": base - shuffled_irrelevant}


def _shuffle(data, column, generator):
    """The data with one column permuted."""
    values = [row[column] for row, _label in data]
    generator.shuffle(values)
    return [(dict(row, **{column: value}), label)
            for (row, label), value in zip(data, values)]


def _accuracy(data, model):
    """The share the model gets right."""
    return sum(1 for row, label in data if model(row) == label) / len(data)


def local_surrogate(seed=0, size=400):
    """A linear surrogate fitted near one point against one fitted globally.

    The black box here is a threshold on a product, which no line describes
    globally and a line describes well in a neighbourhood. That gap is the
    reason local explanations exist.
    """
    generator = random.Random(seed)
    black_box = lambda x, y: 1 if x * y > 0.25 else 0
    points = [(generator.random(), generator.random()) for _ in range(size)]
    globally = _fit_line(points, black_box)
    near = [(x, y) for x, y in points if abs(x - 0.5) < 0.1]
    locally = _fit_line(near, black_box)
    return {"global agreement": _agreement(points, black_box, globally),
            "local agreement": _agreement(near, black_box, locally)}


def _fit_line(points, model):
    """A threshold on the sum of the coordinates, fitted by search."""
    best, best_score = 0.0, -1
    for step in range(101):
        threshold = step / 50
        score = sum(1 for x, y in points
                    if (x + y > threshold) == bool(model(x, y)))
        if score > best_score:
            best, best_score = threshold, score
    return best


def _agreement(points, model, threshold):
    """How often the surrogate and the black box agree."""
    if not points:
        return 0.0
    return sum(1 for x, y in points
               if (x + y > threshold) == bool(model(x, y))) / len(points)


def shortcut_example(seed=0, size=400):
    """A model that is accurate and uses a feature it should not.

    The spurious feature is perfectly correlated with the label in the
    training data and would not be in the world. The accuracy says nothing
    about that; the importance measure names the feature the model actually
    used.
    """
    generator = random.Random(seed)
    data = []
    for _ in range(size):
        real = generator.randint(0, 1)
        shortcut = real
        data.append(({"real": real, "shortcut": shortcut}, real))
    model = lambda row: row["shortcut"]
    base = _accuracy(data, model)
    without_shortcut = _accuracy(_shuffle(data, "shortcut", generator), model)
    without_real = _accuracy(_shuffle(data, "real", generator), model)
    return {"accuracy": base, "shortcut importance": base - without_shortcut,
            "real importance": base - without_real}
