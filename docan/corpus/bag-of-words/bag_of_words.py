"""Bag-of-Words: Vokabular und Termvektoren."""

import numpy as np


def _frequency(built):
    """Zählt jedes Wort im ganzen Korpus."""
    frequency = {}
    for group in built.values():
        for document in group:
            for word in document:
                frequency[word] = frequency.get(word, 0) + 1
    return frequency


def vocabulary(built, size):
    """Wählt die häufigsten Wörter als Terme aus.

    Die Auswahl über die Häufigkeit ist eine Entscheidung mit Folgen: sie
    behält, was oft vorkommt, und wirft weg, was selten ist, obwohl
    gerade seltene Wörter eine Kategorie verraten können. Das Verfahren
    verlässt sich darauf, dass die Gewichtung die häufigen Wörter später
    wieder abwertet.

    Args:
        built: der Korpus.
        size: die Anzahl der Terme.

    Returns:
        Liste der Terme, nach Häufigkeit absteigend.

    Raises:
        ValueError: bei einer nicht positiven Grösse oder wenn der Korpus
            weniger verschiedene Wörter enthält.
    """
    if size <= 0:
        raise ValueError("die Grösse muss positiv sein")
    frequency = _frequency(built)
    if size > len(frequency):
        raise ValueError("der Korpus hat nur %d verschiedene Wörter"
                         % len(frequency))
    ordered = sorted(frequency.items(), key=lambda row: (-row[1], row[0]))
    return [word for word, _ in ordered[:size]]


def term_vector(document, terms):
    """Bildet ein Dokument auf ein Histogramm über die Terme ab.

    Wörter ausserhalb des Vokabulars fallen weg. Damit hat jedes Dokument
    dieselbe Länge, und Dokumente werden vergleichbar; verloren geht
    alles, was in der Reihenfolge steckt.

    Raises:
        ValueError: bei einem leeren Vokabular.
    """
    if not terms:
        raise ValueError("leeres Vokabular")
    position = {term: index for index, term in enumerate(terms)}
    vector = np.zeros(len(terms))
    for word in document:
        index = position.get(word)
        if index is not None:
            vector[index] += 1.0
    return vector


def term_document_matrix(built, terms):
    """Baut die Term-Dokument-Matrix und die Liste der Kategorien.

    Returns:
        Ein Paar aus Matrix und den Kategorien der Zeilen.

    Raises:
        ValueError: bei einem leeren Korpus oder Vokabular.
    """
    if not built:
        raise ValueError("leerer Korpus")
    if not terms:
        raise ValueError("leeres Vokabular")
    rows = []
    labels = []
    for category, group in built.items():
        for document in group:
            rows.append(term_vector(document, terms))
            labels.append(category)
    return np.vstack(rows), labels


def what_the_representation_loses():
    """Nennt, was die Darstellung wegwirft.

    Die Reihenfolge der Wörter, damit jede Verneinung, jede Zuordnung
    eines Adjektivs und jeder Satzbau. «Der Hund beisst den Mann» und
    «Der Mann beisst den Hund» haben dasselbe Histogramm. Für die
    Kategorisierung genügt es meistens, weil die Kategorie an den
    verwendeten Wörtern hängt und nicht an ihrer Anordnung.
    """
    return {"order": "die Reihenfolge und damit der Satzbau",
            "example": "«der Hund beisst den Mann» und «der Mann beisst "
                       "den Hund» sind dasselbe Histogramm",
            "negation": "eine Verneinung verschwindet mit der Stellung",
            "why it still works": "die Kategorie hängt an den Wörtern, "
                                  "nicht an ihrer Anordnung"}
