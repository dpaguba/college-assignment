"""Bewertung von Rückgabelisten."""

import numpy as np

READINGS = ("union", "ground truth")


def _results(results):
    """Prüft eine Ergebnisliste aus Nullen und Einsen.

    Raises:
        ValueError: bei einer leeren Liste oder anderen Werten.
    """
    field = np.asarray(results, dtype=float)
    if field.size == 0 or field.ndim != 1:
        raise ValueError("leere oder falsch geformte Liste")
    if not np.all((field == 0.0) | (field == 1.0)):
        raise ValueError("die Liste besteht aus Nullen und Einsen")
    return field


def precision(results):
    """Der Anteil der relevanten Ergebnisse an der Rückgabeliste.

    Raises:
        ValueError: bei einer leeren Liste.
    """
    field = _results(results)
    return float(field.sum() / len(field))


def recall(results, relevant):
    """Der Anteil der gefundenen an allen relevanten Ergebnissen.

    Raises:
        ValueError: bei einer leeren Liste oder einer nicht positiven
            Anzahl relevanter Ergebnisse.
    """
    field = _results(results)
    if relevant <= 0:
        raise ValueError("es muss relevante Ergebnisse geben")
    return float(field.sum() / relevant)


def average_precision(results, relevant):
    """Misst, wie gut die Rückgabeliste sortiert ist.

    Gemittelt wird die Precision an genau den Stellen, an denen ein
    relevantes Ergebnis steht, geteilt durch die Anzahl der relevanten
    Ergebnisse im Datensatz. Precision und Recall allein sehen die
    Reihenfolge nicht; zwei Listen mit denselben Treffern an anderen
    Stellen haben dieselbe Precision und verschiedene Average Precision.

    Raises:
        ValueError: bei einer leeren Liste oder wenn die Liste mehr
            Treffer enthält, als es relevante Ergebnisse gibt.
    """
    field = _results(results)
    if relevant <= 0:
        raise ValueError("es muss relevante Ergebnisse geben")
    if field.sum() > relevant:
        raise ValueError("mehr Treffer als relevante Ergebnisse")
    found = 0
    total = 0.0
    for position, value in enumerate(field, start=1):
        if value:
            found += 1
            total += found / position
    return float(total / relevant)


def precision_recall_curve(results, relevant):
    """Nennt die Punkte der Precision-Recall-Kurve.

    Aufgenommen wird ein Punkt an jeder Stelle, an der sich der Recall
    ändert, also bei jedem Treffer. Die Fläche unter dieser Kurve ist
    die Average Precision.

    Raises:
        ValueError: wie bei ``average_precision``.
    """
    field = _results(results)
    if relevant <= 0:
        raise ValueError("es muss relevante Ergebnisse geben")
    points = {"recall": [], "precision": []}
    found = 0
    for position, value in enumerate(field, start=1):
        if value:
            found += 1
            points["recall"].append(found / relevant)
            points["precision"].append(found / position)
    return points


def mean_average_precision(runs):
    """Mittelt die Average Precision über die Anfragen.

    Raises:
        ValueError: bei einer leeren Menge von Anfragen.
    """
    if not runs:
        raise ValueError("keine Anfragen")
    return float(np.mean([average_precision(results, relevant)
                          for results, relevant in runs]))


def mean_recall(runs):
    """Mittelt den Recall über die Anfragen.

    Raises:
        ValueError: bei einer leeren Menge von Anfragen.
    """
    if not runs:
        raise ValueError("keine Anfragen")
    return float(np.mean([recall(results, relevant)
                          for results, relevant in runs]))


def overlap(box, other, reading="union"):
    """Misst, wie stark sich zwei Rahmen decken.

    Args:
        box: der gefundene Rahmen als oben, links, unten, rechts.
        other: der Rahmen der Ground Truth.
        reading: ``union`` teilt durch die Vereinigung, ``ground truth``
            durch die Fläche der Ground Truth.

    Raises:
        ValueError: bei einem Rahmen ohne Fläche oder einer unbekannten
            Lesart.
    """
    if reading not in READINGS:
        raise ValueError("unbekannte Lesart: %s" % reading)
    for one in (box, other):
        if one[2] <= one[0] or one[3] <= one[1]:
            raise ValueError("ein Rahmen ohne Fläche")
    top = max(box[0], other[0])
    left = max(box[1], other[1])
    bottom = min(box[2], other[2])
    right = min(box[3], other[3])
    if bottom <= top or right <= left:
        return 0.0
    inside = (bottom - top) * (right - left)
    first = (box[2] - box[0]) * (box[3] - box[1])
    second = (other[2] - other[0]) * (other[3] - other[1])
    if reading == "union":
        return float(inside / (first + second - inside))
    return float(inside / second)


def what_fifty_percent_overlap_means():
    """Zeigt, dass die Angabe auf der Folie zwei Lesarten hat.

    Die Folie nennt fünfzig Prozent Überlapp mit der Ground Truth als
    Schwelle für die Relevanz eines Patches und lässt offen, wovon
    fünfzig Prozent. Ein Patch, der das Wort ganz enthält und dreimal so
    gross ist, deckt die Ground Truth vollständig ab und erreicht doch
    nur ein Drittel der Vereinigung.

    Nach der einen Lesart ist er relevant, nach der anderen nicht, und
    die gemessene mAP unterscheidet sich entsprechend. Wer Zahlen
    zwischen zwei Arbeiten vergleicht, muss die Lesart kennen.

    Returns:
        Abbildung mit beiden Werten für denselben Fall.
    """
    truth = (0, 0, 10, 10)
    found = (0, 0, 10, 30)
    first = overlap(found, truth, "union")
    second = overlap(found, truth, "ground truth")
    return {"ground truth": truth, "found": found,
            "intersection over union": first,
            "intersection over ground truth": second,
            "the two disagree here": (first < 0.5) != (second < 0.5),
            "why it matters": "die gemessene mAP hängt an der Lesart"}


def the_denominator_is_the_dataset():
    """Zeigt, was der Nenner der Average Precision bedeutet.

    Geteilt wird durch die Anzahl der relevanten Ergebnisse im
    Datensatz, nicht durch die Länge der Liste. Eine Liste, die acht von
    zehn relevanten Ergebnissen fehlerfrei an den Anfang stellt, erreicht
    deshalb 0.8 und nicht 1.0. Das ist gewollt: eine kurze Liste soll
    nicht dadurch gut aussehen, dass sie das meiste weglässt.

    Returns:
        Abbildung mit beiden Fällen.
    """
    return {"perfect but truncated": average_precision([1] * 8, 10),
            "complete": average_precision([1] * 10, 10),
            "what it prevents": "eine kurze Liste sieht nicht dadurch "
                                "gut aus, dass sie das meiste weglässt"}
