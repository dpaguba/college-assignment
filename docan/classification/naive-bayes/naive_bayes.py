"""Der naive Bayes Klassifikator über Bag-of-Words."""

import math

import numpy as np


def train(matrix, labels):
    """Schätzt die Verteilungen aus der Stichprobe.

    Die a-priori-Wahrscheinlichkeit einer Klasse ist ihr Anteil an den
    Dokumenten. Die klassenbedingte Wahrscheinlichkeit eines Terms ist
    sein Anteil an allen Termvorkommen der Klasse, geglättet nach
    Laplace: ein Zähler von eins auf jeden Term und die Vokabulargrösse
    im Nenner.

    Ohne die Glättung bekäme ein Term, der in einer Klasse nie vorkommt,
    die Wahrscheinlichkeit null, und ein einziges solches Wort im
    Dokument würde die ganze Klasse ausschliessen, gleich wie gut alles
    andere passt.

    Args:
        matrix: die Term-Dokument-Matrix mit absoluten Häufigkeiten.
        labels: die Kategorie je Zeile.

    Returns:
        Abbildung mit ``prior``, ``conditional`` und ``terms``.

    Raises:
        ValueError: bei einer leeren Stichprobe oder unpassend vielen
            Kategorien.
    """
    field = np.asarray(matrix, dtype=float)
    if field.size == 0 or field.ndim != 2:
        raise ValueError("leere Stichprobe")
    if field.shape[0] != len(labels):
        raise ValueError("zu jeder Zeile gehört genau eine Kategorie")
    terms = field.shape[1]
    prior = {}
    conditional = {}
    for label in sorted(set(labels)):
        rows = field[[index for index, name in enumerate(labels)
                      if name == label]]
        prior[label] = len(rows) / len(labels)
        counted = rows.sum(axis=0)
        conditional[label] = (1.0 + counted) / (terms + counted.sum())
    return {"prior": prior, "conditional": conditional, "terms": terms}


def score(model, vector, label):
    """Rechnet den Logarithmus von P(K) mal P(f|K) aus.

    Gerechnet wird durchweg im Logarithmus. Ein Produkt über tausende
    Terme, jeder kleiner als eins, unterschreitet sonst die kleinste
    darstellbare Zahl, und aus dem Vergleich zweier Klassen wird der
    Vergleich zweier Nullen.

    Raises:
        ValueError: bei einer unbekannten Klasse oder einem Vektor der
            falschen Länge.
    """
    if label not in model["prior"]:
        raise ValueError("unbekannte Klasse: %s" % label)
    counts = np.asarray(vector, dtype=float)
    if counts.shape != (model["terms"],):
        raise ValueError("der Vektor hat die falsche Länge")
    return float(math.log(model["prior"][label])
                 + np.sum(counts * np.log(model["conditional"][label])))


def classify(model, vector):
    """Nennt die Klasse mit der höchsten a-posteriori-Wahrscheinlichkeit.

    Raises:
        ValueError: bei einem Vektor der falschen Länge.
    """
    scored = {label: score(model, vector, label)
              for label in model["prior"]}
    return max(scored, key=lambda label: scored[label])


def classify_all(model, matrix):
    """Klassifiziert eine ganze Menge von Dokumenten.

    Raises:
        ValueError: bei einem Vektor der falschen Länge.
    """
    return [classify(model, row) for row in matrix]


def why_the_log_domain(terms=2000, probability=0.001):
    """Zeigt, dass das direkte Produkt unterläuft.

    Zweitausend Faktoren von je einem Tausendstel ergeben zehn hoch minus
    sechstausend. Das ist weit unterhalb der kleinsten Fliesskommazahl,
    also kommt genau null heraus; im Logarithmus ist es eine gewöhnliche
    Zahl.

    Returns:
        Abbildung mit beiden Rechnungen.

    Raises:
        ValueError: bei einer Wahrscheinlichkeit ausserhalb von null bis
            eins.
    """
    if not 0.0 < probability < 1.0:
        raise ValueError("die Wahrscheinlichkeit liegt zwischen null und "
                         "eins")
    direct = 1.0
    for _ in range(terms):
        direct *= probability
    return {"terms": terms, "each": probability, "direct product": direct,
            "in the log domain": terms * math.log(probability),
            "smallest positive float": 5e-324}


def what_naive_means():
    """Sagt, welche Annahme dem Verfahren den Namen gibt.

    Die Terme werden als unabhängig behandelt, gegeben die Klasse. Für
    Sprache ist das falsch: nach «New» steht überdurchschnittlich oft
    «York». Das Verfahren rechnet die gemeinsame Information deshalb
    mehrfach und liefert übertrieben sichere Wahrscheinlichkeiten. Für
    die Entscheidung selbst genügt es meist trotzdem, weil es nur auf die
    Reihenfolge der Klassen ankommt und nicht auf die Höhe der Werte.
    """
    return {"assumption": "die Terme sind unabhängig, gegeben die Klasse",
            "why it is false": "nach «New» folgt überdurchschnittlich "
                               "oft «York»",
            "what it costs": "übertrieben sichere Wahrscheinlichkeiten",
            "why it still decides well": "es zählt die Reihenfolge der "
                                         "Klassen, nicht die Höhe"}
