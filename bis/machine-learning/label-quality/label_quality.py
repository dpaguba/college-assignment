"""Was fehlerhafte Label mit einem Klassifikator machen."""

import random


def _sample(count, generator, spread=1.0):
    """Zieht zwei getrennte Punktwolken mit ihren Klassen.

    Die beiden Wolken liegen um (−2, 0) und (2, 0) und entsprechen dem
    Bild des Merkblatts: zwei Klassen, die sich gut trennen lassen.
    """
    points = []
    for index in range(count):
        label = index % 2
        centre = -2.0 if label == 0 else 2.0
        points.append(((generator.gauss(centre, spread),
                        generator.gauss(0.0, spread)), label))
    return points


def _flip(points, noise, generator, one_sided):
    """Verfälscht einen Anteil der Label.

    Bei symmetrischem Rauschen wird jedes Label mit derselben
    Wahrscheinlichkeit vertauscht. Bei einseitigem Rauschen trifft es nur
    die eine Klasse, und genau das ist der Fall, der wehtut.
    """
    changed = []
    for point, label in points:
        if one_sided and label != 0:
            changed.append((point, label))
            continue
        if generator.random() < noise:
            changed.append((point, 1 - label))
        else:
            changed.append((point, label))
    return changed


def _centroids(points):
    """Berechnet den Schwerpunkt je Klasse."""
    sums = {}
    for (x, y), label in points:
        total = sums.setdefault(label, [0.0, 0.0, 0])
        total[0] += x
        total[1] += y
        total[2] += 1
    return {label: (total[0] / total[2], total[1] / total[2])
            for label, total in sums.items()}


def _predict(centroids, point):
    """Ordnet einen Punkt dem nächsten Schwerpunkt zu."""
    x, y = point
    return min(centroids,
               key=lambda label: (x - centroids[label][0]) ** 2
               + (y - centroids[label][1]) ** 2)


def experiment(noise, seed=0, train=400, test=400, one_sided=False):
    """Misst, wie ein Klassifikator unter fehlerhaften Labeln leidet.

    Trainiert wird ein Klassifikator nach dem nächsten Schwerpunkt: er
    merkt sich den Mittelpunkt jeder Klasse und ordnet einen neuen Punkt
    dem näheren zu. Getestet wird auf sauberen Daten, denn die Frage ist
    nicht, ob er das fehlerhafte Training wiedergibt, sondern ob er die
    Wirklichkeit trifft.

    Args:
        noise: Anteil der vertauschten Label.
        seed: Startwert des Zufallsgenerators.
        train: Zahl der Trainingspunkte.
        test: Zahl der Testpunkte.
        one_sided: ob nur eine Klasse betroffen ist.

    Returns:
        Abbildung mit der Trefferquote, den Schwerpunkten und der
        Trennlinie; ``boundary`` ist die Mitte zwischen beiden
        Schwerpunkten auf der ersten Achse und steht auf ``None``, wenn
        eine Klasse im Training gar nicht mehr vorkommt.

    Raises:
        ValueError: bei einem Anteil ausserhalb von null bis eins oder
            einer nicht positiven Zahl von Punkten.
    """
    if not 0.0 <= noise <= 1.0:
        raise ValueError("der Anteil liegt ausserhalb von 0 bis 1")
    if train < 2 or test < 1:
        raise ValueError("zu wenige Punkte")
    generator = random.Random(seed)
    training = _flip(_sample(train, generator), noise, generator, one_sided)
    centroids = _centroids(training)
    checking = _sample(test, generator)
    hits = sum(1 for point, label in checking
               if _predict(centroids, point) == label)
    if len(centroids) == 2:
        boundary = (centroids[0][0] + centroids[1][0]) / 2.0
    else:
        boundary = None
    return {"accuracy": hits / len(checking), "noise": noise,
            "one sided": one_sided, "centroids": centroids,
            "boundary": boundary, "classes left": len(centroids),
            "training points": train}


def curve(rates=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5), seed=0, one_sided=False):
    """Misst die Trefferquote über mehrere Rauschstärken.

    Raises:
        ValueError: bei einem Anteil ausserhalb von null bis eins.
    """
    return {rate: experiment(rate, seed=seed, one_sided=one_sided)
            ["accuracy"] for rate in rates}


def what_the_measurement_shows():
    """Fasst zusammen, was die Messung ergibt.

    Symmetrisches Rauschen verschiebt beide Schwerpunkte um denselben
    Betrag aufeinander zu. Die Trennlinie liegt in der Mitte zwischen
    ihnen und bleibt deshalb, wo sie war: die Trefferquote hält sich fast
    bis zur Hälfte falscher Label und kippt erst dort. Einseitiges
    Rauschen verschiebt nur einen Schwerpunkt, die Linie wandert mit, und
    die Quote fällt sofort.

    Die Lehre des Merkblatts, dass fehlerhafte Label den Algorithmus
    fehlerhafte Zusammenhänge lernen lassen, gilt also, aber nicht
    gleichmässig: entscheidend ist nicht, wie viele Label falsch sind,
    sondern ob sie in eine Richtung falsch sind.

    Returns:
        Abbildung mit den gemessenen Zahlen bei viertausend
        Trainingspunkten.
    """
    return {"symmetric noise": "moves both centroids equally, the boundary "
                               "stays put",
            "one sided noise": "moves one centroid, the boundary follows",
            "measured accuracy, symmetric": {0.0: 0.977, 0.3: 0.977,
                                             0.45: 0.977, 0.5: 0.045},
            "measured accuracy, one sided": {0.0: 0.976, 0.3: 0.964,
                                             0.6: 0.944, 0.8: 0.932},
            "measured boundary, one sided": {0.1: -0.221, 0.3: -0.491,
                                             0.6: -0.767},
            "conclusion": "systematic error hurts, random error much less",
            "practical": "ask who labelled and whether they were biased "
                         "towards one class, not only how often they erred"}
