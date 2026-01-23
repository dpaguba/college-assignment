"""Auffälligkeit über die Tiefe, in der ein Punkt allein steht."""

import numpy as np


def average_path_length(size):
    """Die mittlere Pfadlänge eines zufälligen binären Suchbaums.

    Sie ist der Massstab, gegen den die gemessene Tiefe normiert wird:
    zwei mal die harmonische Zahl bis n minus eins, minus zwei mal
    (n − 1) durch n. Ohne diese Normierung liesse sich die Tiefe
    zwischen Bäumen verschiedener Stichprobengrösse nicht vergleichen.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    if size <= 0:
        raise ValueError("die Grösse muss positiv sein")
    if size == 1:
        return 0.0
    harmonic = sum(1.0 / index for index in range(1, size))
    return 2.0 * harmonic - 2.0 * (size - 1) / size


def score(data, trees=100, sample=256, seed=0):
    """Bewertet jeden Punkt nach seiner mittleren Trennungstiefe.

    Ein Punkt, der weit aussen liegt, wird von einer zufälligen Trennung
    früher abgeschnitten als einer mitten in der Menge. Gemittelt über
    viele Bäume ist die Tiefe damit ein Mass für Auffälligkeit, und das
    Verfahren braucht dafür keinen Abstand und keine Dichte.

    Der Wert zwei hoch minus mittlere Tiefe durch Massstab liegt
    zwischen null und eins; ein Wert nahe eins heisst früh getrennt.

    Args:
        data: die Punkte.
        trees: die Anzahl der Bäume.
        sample: die Grösse der Stichprobe je Baum.
        seed: der Startwert.

    Returns:
        Die Bewertungen.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Bäumen oder einer
            leeren Menge.
    """
    field = np.asarray(data, dtype=float)
    if field.ndim != 2 or field.shape[0] == 0:
        raise ValueError("leere oder falsch geformte Punktmenge")
    if trees <= 0:
        raise ValueError("es braucht mindestens einen Baum")
    rng = np.random.default_rng(seed)
    size = min(sample, len(field))
    limit = int(np.ceil(np.log2(max(2, size))))
    total = np.zeros(len(field))
    for _ in range(trees):
        chosen = rng.choice(len(field), size=size, replace=False)
        for point in range(len(field)):
            total[point] += _walk(field[chosen], field[point], rng, limit)
    mean = total / trees
    return 2.0 ** (-mean / average_path_length(size))


def _walk(sample, point, rng, limit):
    """Misst die Tiefe eines Punktes in einem zufälligen Baum."""
    indices = np.arange(len(sample))
    depth = 0
    while len(indices) > 1 and depth < limit:
        feature = int(rng.integers(0, sample.shape[1]))
        values = sample[indices, feature]
        low, high = float(values.min()), float(values.max())
        if low == high:
            break
        threshold = rng.uniform(low, high)
        mask = values < threshold
        indices = indices[mask] if point[feature] < threshold \
            else indices[~mask]
        depth += 1
    return depth + average_path_length(max(1, len(indices)))


def trace_one_tree():
    """Rechnet die Tiefe eines Punktes in einem Baum von Hand nach.

    Fünf Punkte auf einer Geraden, vier davon eng beieinander und einer
    weit draussen. Wird immer in der Mitte des Wertebereichs getrennt,
    so fällt der weit entfernte Punkt bei der ersten Trennung ab, und
    die vier übrigen brauchen weitere Trennungen. Die Tiefe des weit
    entfernten ist also eins plus dem Massstab für eine Menge aus einem
    Punkt, und der ist null.

    Returns:
        Abbildung mit der gemessenen und der von Hand bestimmten Tiefe.
    """
    field = np.array([[0.0], [0.1], [0.2], [0.3], [10.0]])
    depth = 0
    indices = np.arange(5)
    threshold = 5.0
    values = field[indices, 0]
    indices = indices[values >= threshold]
    depth += 1
    measured = depth + average_path_length(max(1, len(indices)))
    return {"points": field.reshape(-1).tolist(),
            "threshold": threshold,
            "depth of the far point": measured, "by hand": 1.0,
            "why": "eine Trennung in der Mitte schneidet ihn sofort ab"}


def more_trees_steady_it(seed=0):
    """Misst, wie die Streuung der Bewertung mit der Zahl der Bäume fällt.

    Returns:
        Abbildung mit beiden Streuungen.
    """
    rng = np.random.default_rng(seed)
    cloud = np.vstack([rng.normal(size=(150, 2)),
                       np.array([[7.0, 7.0]])])
    few = [float(score(cloud, trees=3, seed=index)[-1])
           for index in range(12)]
    many = [float(score(cloud, trees=60, seed=index)[-1])
            for index in range(12)]
    return {"spread with few": float(np.std(few)),
            "spread with many": float(np.std(many)),
            "trees": (3, 60),
            "why": "jeder Baum trennt zufällig, erst der Durchschnitt "
                   "ist stabil"}


def why_it_scales(size=256):
    """Sagt, warum die Stichprobe je Baum klein bleibt.

    Ein Baum sieht nur wenige hundert Punkte, und mehr würde das
    Ergebnis sogar verschlechtern: in einer grossen Stichprobe stehen
    genügend Punkte in der Nähe eines Ausreissers, um ihn mitten in die
    Menge zu ziehen. Der Aufwand hängt damit nicht an der Grösse des
    Datensatzes, sondern an der Zahl der Bäume.
    """
    return {"sample per tree": size,
            "why not more": "in einer grossen Stichprobe verschwindet "
                            "der Ausreisser in der Menge",
            "cost": "die Zahl der Bäume, nicht die Grösse der Daten",
            "reference length": average_path_length(size)}
