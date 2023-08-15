"""Abstands- und dichtebasierte Erkennung."""

import math
import random


def distance(first, second):
    """Der euklidische Abstand zweier Punkte.

    Raises:
        ValueError: bei verschiedenen Längen.
    """
    if len(first) != len(second):
        raise ValueError("die Punkte haben verschiedene Länge")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def neighbours(points, index, count):
    """Nennt die Nummern der nächsten Nachbarn eines Punktes.

    Raises:
        ValueError: bei einer unzulässigen Nummer oder Nachbarzahl.
    """
    if not 0 <= index < len(points):
        raise ValueError("unbekannter Punkt")
    if not 1 <= count < len(points):
        raise ValueError("unzulässige Zahl von Nachbarn")
    ranked = sorted((other for other in range(len(points))
                     if other != index),
                    key=lambda other: distance(points[index],
                                               points[other]))
    return ranked[:count]


def kth_distance(points, index, count):
    """Der Abstand zum k-ten Nachbarn.

    Das ist das einfachste Mass: wer weit von seinen Nachbarn entfernt
    liegt, ist verdächtig. Es funktioniert, solange alle Bereiche
    dieselbe Dichte haben, und genau daran scheitert es sonst.

    Raises:
        ValueError: bei einer unzulässigen Nummer oder Nachbarzahl.
    """
    found = neighbours(points, index, count)
    return distance(points[index], points[found[-1]])


def local_outlier_factor(points, index, count=5):
    """Rechnet den lokalen Ausreisserfaktor eines Punktes.

    Verglichen wird die Dichte um den Punkt mit der Dichte um seine
    Nachbarn. Ein Wert um eins heisst, dass er so dicht liegt wie sie;
    deutlich über eins heisst, dass er dünner liegt als seine Umgebung,
    und das ist die Aussage, die ein reiner Abstand nicht treffen kann.

    Raises:
        ValueError: bei einer unzulässigen Nummer oder Nachbarzahl.
    """
    def reach(first, second):
        """Der erreichbare Abstand, nach unten durch die Dichte begrenzt."""
        return max(kth_distance(points, second, count),
                   distance(points[first], points[second]))

    def density(other):
        """Die lokale Erreichbarkeitsdichte eines Punktes."""
        found = neighbours(points, other, count)
        average = sum(reach(other, item) for item in found) / len(found)
        return 1.0 / average if average else float("inf")

    found = neighbours(points, index, count)
    own = density(index)
    if own == 0:
        raise ValueError("die Dichte ist null")
    return sum(density(other) for other in found) / len(found) / own


def two_densities(seed=0):
    """Baut Daten mit einer dichten und einer dünnen Gruppe.

    Returns:
        Paar aus den Punkten und den Nummern der eingefügten Ausreisser.
    """
    generator = random.Random(seed)
    points = [(generator.gauss(0.0, 0.3), generator.gauss(0.0, 0.3))
              for _ in range(60)]
    points += [(generator.gauss(8.0, 2.0), generator.gauss(8.0, 2.0))
               for _ in range(30)]
    points.append((1.5, 1.5))
    points.append((20.0, 20.0))
    return points, [len(points) - 2, len(points) - 1]


def where_the_distance_fails(seed=0, count=5):
    """Vergleicht beide Masse auf Daten mit zwei Dichten.

    Der eingefügte Punkt bei (1.5, 1.5) liegt dicht neben der engen
    Gruppe und ist für sie weit weg; gemessen am absoluten Abstand fällt
    er trotzdem kaum auf, weil in der dünnen Gruppe alle Abstände viel
    grösser sind. Der lokale Faktor sieht ihn, weil er ihn mit seiner
    eigenen Umgebung vergleicht und nicht mit dem Datensatz.

    Returns:
        Abbildung mit den Rängen beider Masse für den eingefügten Punkt.
    """
    points, inserted = two_densities(seed)
    near = inserted[0]
    by_distance = sorted(range(len(points)),
                         key=lambda index: -kth_distance(points, index,
                                                         count))
    by_factor = sorted(range(len(points)),
                       key=lambda index: -local_outlier_factor(points,
                                                               index, count))
    return {"rank by distance": by_distance.index(near) + 1,
            "rank by local factor": by_factor.index(near) + 1,
            "points": len(points),
            "factor of the inserted point":
                round(local_outlier_factor(points, near, count), 3),
            "why": "der absolute Abstand misst gegen den ganzen Datensatz, "
                   "der Faktor gegen die Umgebung"}
