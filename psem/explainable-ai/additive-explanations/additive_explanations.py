"""SHAP: die Erklärung als additive Zerlegung einer Vorhersage."""

import itertools
import math

BACKGROUND = ((1.0, 2.0, 0.0), (3.0, 0.0, 1.0), (2.0, 4.0, 1.0),
              (0.0, 2.0, 0.0))

WEIGHTS = (2.0, -1.0, 5.0)
BIAS = 3.0


def linear(point, weights=WEIGHTS, bias=BIAS):
    """Ein lineares Modell.

    Raises:
        ValueError: wenn Punkt und Gewichte verschieden lang sind.
    """
    if len(point) != len(weights):
        raise ValueError("Punkt und Gewichte passen nicht zusammen")
    return bias + sum(weight * value
                      for weight, value in zip(weights, point))


def value_function(model, point, background, present):
    """Der Wert einer Merkmalsmenge: die erwartete Vorhersage.

    Die Merkmale in der Menge behalten ihren Wert, die anderen werden
    aus dem Hintergrund gezogen und der Mittelwert genommen. Das ist die
    eingreifende Lesart: sie fragt, was das Modell sagen würde, wenn die
    übrigen Merkmale beliebig wären.
    """
    total = 0.0
    for other in background:
        mixed = tuple(point[index] if index in present else other[index]
                      for index in range(len(point)))
        total += model(mixed)
    return total / len(background)


def shap(model, point, background=BACKGROUND):
    """Rechnet die SHAP-Werte einer Vorhersage aus.

    Das ist der Shapley-Wert des Spiels, in dem die Spieler die Merkmale
    sind und der Wert einer Koalition die erwartete Vorhersage bei
    bekannten Merkmalen dieser Koalition.

    Returns:
        Liste der Beiträge je Merkmal.

    Raises:
        ValueError: bei einem leeren Hintergrund.
    """
    if not background:
        raise ValueError("leerer Hintergrund")
    count = len(point)
    contributions = []
    for index in range(count):
        others = [other for other in range(count) if other != index]
        total = 0.0
        for size in range(len(others) + 1):
            weight = (math.factorial(size)
                      * math.factorial(count - size - 1)
                      / math.factorial(count))
            for group in itertools.combinations(others, size):
                present = frozenset(group)
                total += weight * (
                    value_function(model, point, background,
                                   present | {index})
                    - value_function(model, point, background, present))
        contributions.append(total)
    return contributions


def local_accuracy(model, point, background=BACKGROUND):
    """Prüft, dass die Beiträge die Vorhersage genau erklären.

    Die Summe der Beiträge plus dem Grundwert, also der mittleren
    Vorhersage über den Hintergrund, muss die Vorhersage ergeben. Das
    ist die erste der drei Eigenschaften bei Lundberg und Lee, und sie
    ist die Effizienz des Shapley-Werts unter anderem Namen.
    """
    base = sum(model(other) for other in background) / len(background)
    contributions = shap(model, point, background)
    return {"base value": base, "contributions": contributions,
            "sum": base + sum(contributions),
            "prediction": model(point),
            "holds": abs(base + sum(contributions) - model(point)) < 1e-9}


def matches_the_linear_formula(point, weights=WEIGHTS,
                               background=BACKGROUND):
    """Vergleicht die Rechnung mit der Formel für lineare Modelle.

    Bei einem linearen Modell und unabhängig gezogenen Hintergrunddaten
    ist der Beitrag eines Merkmals genau sein Gewicht mal dem Abstand
    vom Mittelwert. Das ist eine geschlossene Formel und damit eine
    Probe auf die Rechnung, die nichts von der Rechnung übernimmt.

    Returns:
        Abbildung mit beiden Ergebnissen.
    """
    def model(other):
        """Das lineare Modell mit den vorgegebenen Gewichten."""
        return linear(other, weights)

    computed = shap(model, point, background)
    means = [sum(other[index] for other in background) / len(background)
             for index in range(len(point))]
    expected = [weights[index] * (point[index] - means[index])
                for index in range(len(point))]
    return {"computed": computed, "by formula": expected,
            "agree": all(abs(first - second) < 1e-9
                         for first, second in zip(computed, expected))}


def missingness(background=BACKGROUND):
    """Prüft, dass ein Merkmal ohne Einfluss den Beitrag null bekommt.

    Ein Gewicht von null heisst, dass das Merkmal die Vorhersage nicht
    ändert, und dann darf die Erklärung ihm auch nichts zuschreiben. Das
    ist der Nullbeitrag des Shapley-Werts.
    """
    weights = (2.0, 0.0, 5.0)

    def model(other):
        """Ein Modell, dessen zweites Merkmal nichts beiträgt."""
        return linear(other, weights)

    contributions = shap(model, (1.0, 9.0, 1.0), background)
    return {"contributions": contributions,
            "second is zero": abs(contributions[1]) < 1e-9}


def the_three_properties():
    """Nennt die drei Eigenschaften aus Lundberg und Lee.

    Lokale Genauigkeit: die Beiträge summieren sich zur Vorhersage.
    Fehlen: ein Merkmal, das nicht vorkommt, bekommt nichts.
    Konsistenz: wird ein Modell so geändert, dass ein Merkmal in jeder
    Koalition mehr beiträgt, so darf sein Beitrag nicht sinken.

    Der Satz der Arbeit ist, dass genau eine additive Erklärung alle
    drei erfüllt, und das ist der Shapley-Wert. Die Rechtfertigung von
    SHAP kommt also nicht aus der Erfahrung, sondern aus einem
    Eindeutigkeitssatz.
    """
    return {"local accuracy": "die Beiträge ergeben die Vorhersage",
            "missingness": "ein fehlendes Merkmal bekommt null",
            "consistency": "mehr Beitrag im Modell heisst nicht weniger "
                           "Beitrag in der Erklärung",
            "theorem": "genau eine additive Erklärung erfüllt alle drei",
            "which one": "der Shapley-Wert"}
