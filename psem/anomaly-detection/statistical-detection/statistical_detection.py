"""Statistische Ausreissererkennung und ihre Grenzen."""

import math
import random


def mean(values):
    """Der Mittelwert.

    Raises:
        ValueError: bei einer leeren Folge.
    """
    if not values:
        raise ValueError("leere Folge")
    return sum(values) / len(values)


def deviation(values):
    """Die Standardabweichung.

    Raises:
        ValueError: bei weniger als zwei Werten.
    """
    if len(values) < 2:
        raise ValueError("mindestens zwei Werte")
    middle = mean(values)
    return math.sqrt(sum((value - middle) ** 2
                         for value in values) / len(values))


def z_scores(values):
    """Rechnet jeden Wert in Vielfache der Standardabweichung um.

    Raises:
        ValueError: bei weniger als zwei Werten oder einer Streuung von
            null.
    """
    spread = deviation(values)
    if spread == 0:
        raise ValueError("die Werte streuen nicht")
    middle = mean(values)
    return [(value - middle) / spread for value in values]


def by_z_score(values, limit=3.0):
    """Meldet Werte jenseits einer Zahl von Standardabweichungen.

    Raises:
        ValueError: bei einer nicht positiven Schranke oder einer
            Streuung von null.
    """
    if limit <= 0:
        raise ValueError("die Schranke muss positiv sein")
    scores = z_scores(values)
    return sorted(index for index, score in enumerate(scores)
                  if abs(score) > limit)


def quartiles(values):
    """Nennt das untere und das obere Quartil.

    Raises:
        ValueError: bei weniger als vier Werten.
    """
    if len(values) < 4:
        raise ValueError("mindestens vier Werte")
    ordered = sorted(values)
    half = len(ordered) // 2
    lower = ordered[:half]
    upper = ordered[half + len(ordered) % 2:]
    return _median(lower), _median(upper)


def _median(values):
    """Der Median einer nicht leeren Folge."""
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def by_interquartile_range(values, factor=1.5):
    """Meldet Werte ausserhalb der üblichen Whisker-Grenzen.

    Raises:
        ValueError: bei einem nicht positiven Faktor oder zu wenigen
            Werten.
    """
    if factor <= 0:
        raise ValueError("der Faktor muss positiv sein")
    low, high = quartiles(values)
    span = high - low
    return sorted(index for index, value in enumerate(values)
                  if value < low - factor * span
                  or value > high + factor * span)


def the_outlier_hides_itself(values=None):
    """Zeigt, wie ein Ausreisser die Schwelle mitverschiebt.

    Mittelwert und Standardabweichung werden aus denselben Daten
    gerechnet, in denen der Ausreisser steckt. Ein einzelner sehr grosser
    Wert hebt beide an und macht sich damit selbst unauffälliger; bei
    wenigen Werten reicht das, um ihn ganz zu verstecken. Die Quartile
    haben das Problem nicht, weil sie den Rand nicht mitrechnen.

    Returns:
        Abbildung mit den Befunden beider Verfahren.
    """
    values = [10, 11, 9, 10, 12, 11, 10, 9, 200] if values is None \
        else list(values)
    return {"values": values,
            "z score finds": by_z_score(values),
            "iqr finds": by_interquartile_range(values),
            "z of the outlier": round(z_scores(values)[-1], 3),
            "why": "der Ausreisser hebt Mittelwert und Streuung, an denen "
                   "er gemessen wird"}


def two_populations(seed=0, count=200):
    """Zeigt, dass eine Schwelle bei zwei Gruppen nichts trennt.

    Bestehen die Daten aus zwei Häufungen, so liegt der Mittelwert
    zwischen ihnen, wo kaum ein Wert ist, und die Streuung ist gross.
    Punkte in der Lücke, die zu keiner der beiden Gruppen gehören, fallen
    dann nicht auf, und Punkte am äusseren Rand einer Gruppe fallen auf,
    obwohl sie normal sind.

    Returns:
        Abbildung mit dem Befund.

    Raises:
        ValueError: bei einer zu kleinen Zahl.
    """
    if count < 10:
        raise ValueError("zu wenige Werte")
    generator = random.Random(seed)
    values = [generator.gauss(0.0, 1.0) for _ in range(count // 2)]
    values += [generator.gauss(20.0, 1.0) for _ in range(count // 2)]
    inserted = 10.0
    values.append(inserted)
    found = by_z_score(values)
    return {"middle point": inserted,
            "reported": len(found),
            "middle point reported": (len(values) - 1) in found,
            "mean": round(mean(values), 3),
            "deviation": round(deviation(values), 3),
            "why": "der Mittelwert liegt in der Lücke, und dort ist der "
                   "eingefügte Punkt zu Hause"}
