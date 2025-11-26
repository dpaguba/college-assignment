"""Wordspotting mit einem Wortabbild als Anfrage."""

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _name in (("..", "word-segmentation"),
              ("..", "retrieval-evaluation"),
              ("..", "..", "image-features", "sift-descriptors"),
              ("..", "..", "image-features", "lloyd-clustering"),
              ("..", "..", "image-features", "dense-grid"),
              ("..", "..", "image-features", "bag-of-features")):
    sys.path.insert(0, os.path.join(_HERE, *_name))

import bag_of_features as bof
import dense_grid
import lloyd_clustering
import retrieval_evaluation as ev
import sift_descriptors as sift
import word_segmentation as ws

MEASURES = ("cosine", "euclidean", "cityblock")


def word_images(field=None, boxes=None):
    """Schneidet die Wortabbilder aus der Seite.

    Wie im Projekt vorgesehen wird dafür die Ground Truth genommen und
    nicht die eigene Segmentierung, damit ein Fehler der Segmentierung
    das Ergebnis der Suche nicht verdeckt.

    Returns:
        Liste der Ausschnitte.
    """
    if field is None:
        field, boxes, _ = ws.page()
    return [field[top:bottom, left:right]
            for top, left, bottom, right in boxes]


def features(image, step=5, size=12, cells=2, bins=8):
    """Beschreibt ein Wortabbild an den Punkten eines dichten Gitters.

    Returns:
        Ein Paar aus Deskriptoren und ihren Mittelpunkten.

    Raises:
        ValueError: bei einem Ausschnitt, der kleiner ist als das
            Fenster.
    """
    field = np.asarray(image, dtype=float)
    if min(field.shape) < size:
        raise ValueError("das Wortabbild ist kleiner als das Fenster")
    positions = dense_grid.points(field.shape, step=step, size=size)
    half = size // 2
    described = [sift.describe(field[row - half:row - half + size,
                                     column - half:column - half + size],
                               cells=cells, bins=bins)
                 for row, column in positions]
    return np.vstack(described), positions


def vocabulary(images, size=32, seed=0, step=5, window=12):
    """Lernt das visuelle Vokabular aus allen Wortabbildern.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    if size <= 0:
        raise ValueError("die Grösse des Vokabulars muss positiv sein")
    collected = [features(image, step=step, size=window)[0]
                 for image in images]
    stacked = np.vstack(collected)
    return lloyd_clustering.cluster(stacked, k=size, seed=seed)["centroids"]


def represent(image, centroids, levels=2, step=5, window=12):
    """Bildet ein Wortabbild auf seine räumliche Pyramide ab.

    Normiert wird auf die Summe eins, damit ein langes Wort mit vielen
    Fenstern nicht allein wegen seiner Länge weit von einem kurzen
    entfernt liegt.

    Raises:
        ValueError: bei einem zu kleinen Ausschnitt.
    """
    described, positions = features(image, step=step, size=window)
    built = bof.spatial_pyramid(described, positions, centroids,
                                np.asarray(image).shape, levels=levels)
    total = built.sum()
    return built / total if total > 0 else built


def _distance(first, second, measure):
    """Rechnet den Abstand zweier Darstellungen aus.

    Raises:
        ValueError: bei einem unbekannten Mass.
    """
    if measure == "euclidean":
        return float(np.sqrt(np.sum((first - second) ** 2)))
    if measure == "cityblock":
        return float(np.sum(np.abs(first - second)))
    if measure == "cosine":
        lengths = np.linalg.norm(first) * np.linalg.norm(second)
        if lengths == 0.0:
            return 1.0
        return float(1.0 - np.dot(first, second) / lengths)
    raise ValueError("unbekanntes Mass: %s" % measure)


def ranking(query, others, measure="cosine"):
    """Sortiert die Darstellungen nach ihrem Abstand zur Anfrage.

    Raises:
        ValueError: bei einem unbekannten Mass.
    """
    measured = [(_distance(query, other, measure), index)
                for index, other in enumerate(others)]
    return [index for _, index in sorted(measured)]


def evaluate(vocabulary_size=32, levels=2, measure="cosine", seed=0,
             step=5, window=12, vocabulary=None):
    """Nutzt jedes Wort einmal als Anfrage und misst die mittlere AP.

    Args:
        vocabulary_size: die Grösse des visuellen Vokabulars.
        levels: die Stufen der räumlichen Pyramide.
        measure: das Abstandsmass.
        seed: der Startwert der Clusteranalyse.
        step: der Abstand im Gitter.
        window: die Kantenlänge eines Fensters.
        vocabulary: eine feste Grösse des Vokabulars, wenn gesetzt.

    Returns:
        Abbildung mit der mittleren Average Precision und dem Zufall.

    Raises:
        ValueError: bei einem unbekannten Mass oder einer nicht
            positiven Vokabulargrösse.
    """
    if measure not in MEASURES:
        raise ValueError("unbekanntes Mass: %s" % measure)
    size = vocabulary_size if vocabulary is None else vocabulary
    if size <= 0:
        raise ValueError("die Grösse des Vokabulars muss positiv sein")
    field, boxes, labels = ws.page()
    images = word_images(field, boxes)
    centroids = globals()["vocabulary"](images, size=size, seed=seed,
                                        step=step, window=window)
    built = [represent(image, centroids, levels, step, window)
             for image in images]
    runs = []
    shares = []
    for index, query in enumerate(built):
        others = [position for position in range(len(built))
                  if position != index]
        order = ranking(query, [built[position] for position in others],
                        measure)
        results = [1 if labels[others[position]] == labels[index] else 0
                   for position in order]
        relevant = sum(results)
        if relevant == 0:
            continue
        runs.append((results, relevant))
        shares.append(relevant / len(results))
    return {"mAP": ev.mean_average_precision(runs),
            "mean recall": ev.mean_recall(runs),
            "queries": len(runs), "words": len(built),
            "list length": len(built) - 1,
            "chance": float(np.mean(shares)),
            "vocabulary": size, "levels": levels, "measure": measure}


def pyramid_helps():
    """Vergleicht das reine Histogramm mit der räumlichen Pyramide.

    Returns:
        Abbildung mit beiden Werten.
    """
    plain = evaluate(levels=1)["mAP"]
    pyramid = evaluate(levels=2)["mAP"]
    return {"plain histogram": plain, "with pyramid": pyramid,
            "difference": pyramid - plain,
            "why": "die Pyramide behält, wo im Wort ein Merkmal stand"}


def what_the_measure_changes():
    """Vergleicht die drei Abstandsmasse an derselben Aufgabe.

    Returns:
        Abbildung mit der mittleren AP je Mass.
    """
    return {measure: evaluate(measure=measure)["mAP"]
            for measure in MEASURES}
