"""Statistische Eigenschaften eines Korpus."""

import random

CATEGORIES = ("news", "editorial", "reviews", "religion", "hobbies",
              "lore", "belles_lettres", "government", "learned",
              "fiction", "mystery", "science_fiction", "adventure",
              "romance", "humor")

DOCUMENTS = (44, 27, 17, 17, 36, 48, 75, 30, 80, 29, 24, 6, 29, 29, 9)

SHARED = ("time", "year", "people", "way", "work", "day", "man", "state",
          "life", "world", "part", "case", "place", "group", "number",
          "point", "hand", "problem", "fact", "form")

TOPICS = {
    "news": ("police", "city", "report", "election", "mayor"),
    "editorial": ("opinion", "policy", "reader", "argument", "letter"),
    "reviews": ("film", "music", "performance", "critic", "stage"),
    "religion": ("church", "faith", "god", "prayer", "spirit"),
    "hobbies": ("garden", "engine", "model", "wood", "collection"),
    "lore": ("legend", "custom", "village", "story", "tradition"),
    "belles_lettres": ("prose", "poet", "essay", "style", "author"),
    "government": ("committee", "federal", "programme", "budget", "law"),
    "learned": ("method", "analysis", "theory", "result", "measure"),
    "fiction": ("room", "voice", "window", "smile", "letter"),
    "mystery": ("murder", "gun", "detective", "clue", "body"),
    "science_fiction": ("ship", "planet", "robot", "alien", "orbit"),
    "adventure": ("horse", "river", "trail", "camp", "rifle"),
    "romance": ("love", "kiss", "heart", "wedding", "tear"),
    "humor": ("joke", "laugh", "cartoon", "gag", "pun"),
}


def _zipf_pick(rng, words):
    """Zieht ein Wort mit einer Häufigkeit nach dem Zipfschen Gesetz."""
    weights = [1.0 / (rank + 1.0) for rank in range(len(words))]
    return rng.choices(words, weights=weights, k=1)[0]


def corpus(seed=20240401):
    """Erzeugt den Beispielkorpus.

    Aufbau und Verteilung folgen dem Brown Corpus: 500 Dokumente in 15
    Kategorien, ungleich verteilt von 6 Dokumenten in science_fiction bis
    80 in learned. Die Texte selbst sind erzeugt, weil der Korpus dem
    Fachprojekt nicht beiliegt; jedes Dokument mischt allgemeine Wörter
    mit den Wörtern seiner Kategorie, beide nach dem Zipfschen Gesetz.

    Args:
        seed: der Startwert des Zufallsgenerators.

    Returns:
        Abbildung von der Kategorie auf die Liste ihrer Dokumente.
    """
    rng = random.Random(seed)
    built = {}
    index = 0
    for category, count in zip(CATEGORIES, DOCUMENTS):
        documents = []
        for _ in range(count):
            length = 220 + (index % 97)
            index += 1
            words = []
            for position in range(length):
                if position % 5 < 3:
                    words.append(_zipf_pick(rng, SHARED))
                else:
                    words.append(_zipf_pick(rng, TOPICS[category]))
            documents.append(words)
        built[category] = documents
    return built


def counts(built=None):
    """Zählt Kategorien, Dokumente, Wörter und das Vokabular.

    Returns:
        Abbildung mit den vier Zahlen.

    Raises:
        ValueError: bei einem leeren Korpus.
    """
    built = corpus() if built is None else built
    if not built:
        raise ValueError("leerer Korpus")
    documents = [document for group in built.values() for document in group]
    vocabulary = {word for document in documents for word in document}
    return {"categories": len(built), "documents": len(documents),
            "tokens": sum(len(document) for document in documents),
            "vocabulary": len(vocabulary)}


def per_category(built=None):
    """Zählt Dokumente und Wörter je Kategorie.

    Die Ungleichverteilung ist der Grund, warum die Fehlerrate eines
    Klassifikators allein wenig sagt: wer immer learned rät, liegt in
    achtzig von fünfhundert Fällen richtig, ohne etwas gelernt zu haben.

    Returns:
        Abbildung von der Kategorie auf ihre Zahlen.
    """
    built = corpus() if built is None else built
    return {category: {"documents": len(group),
                       "tokens": sum(len(document) for document in group),
                       "share": len(group) / sum(len(other) for other
                                                 in built.values())}
            for category, group in built.items()}


def most_frequent(built=None, count=10, category=None):
    """Nennt die häufigsten Wörter im Korpus oder in einer Kategorie.

    Args:
        built: der Korpus.
        count: wie viele Wörter genannt werden.
        category: die Kategorie, oder None für den ganzen Korpus.

    Returns:
        Liste aus Wort und Häufigkeit, absteigend sortiert.

    Raises:
        ValueError: bei einer unbekannten Kategorie oder einer nicht
            positiven Anzahl.
    """
    built = corpus() if built is None else built
    if count <= 0:
        raise ValueError("die Anzahl muss positiv sein")
    if category is not None and category not in built:
        raise ValueError("unbekannte Kategorie: %s" % category)
    groups = [built[category]] if category is not None else built.values()
    frequency = {}
    for group in groups:
        for document in group:
            for word in document:
                frequency[word] = frequency.get(word, 0) + 1
    ordered = sorted(frequency.items(), key=lambda row: (-row[1], row[0]))
    return ordered[:count]


def zipf(built=None, ranks=20):
    """Prüft das Zipfsche Gesetz an den häufigsten Wörtern.

    Das Gesetz sagt, dass Rang mal Häufigkeit ungefähr gleich bleibt. Es
    ist der Grund, warum wenige Wörter fast den ganzen Text ausmachen und
    warum das Entfernen der Stopwords so viel bringt.

    Returns:
        Abbildung mit den Häufigkeiten, den Produkten und ihrer Spanne.

    Raises:
        ValueError: bei einer nicht positiven Anzahl von Rängen.
    """
    built = corpus() if built is None else built
    if ranks <= 0:
        raise ValueError("die Anzahl der Ränge muss positiv sein")
    rows = most_frequent(built, ranks)
    frequencies = [frequency for _, frequency in rows]
    products = [(rank + 1) * frequency
                for rank, frequency in enumerate(frequencies)]
    return {"frequencies": frequencies,
            "rank times frequency": products,
            "spread": max(products) - min(products),
            "top share": sum(frequencies) / counts(built)["tokens"]}


def why_the_statistics_come_first():
    """Sagt, wozu die Zählerei vor jedem Verfahren steht.

    Sie legt fest, was danach überhaupt gemessen wird: die Grösse des
    Vokabulars bestimmt die Länge der Termvektoren, die Verteilung der
    Dokumente über die Kategorien die Grundrate, gegen die jede
    Fehlerrate zu halten ist, und die Häufigkeitsverteilung entscheidet,
    ob Stopwords und Gewichtung nötig sind.
    """
    return {"vocabulary size": "die Länge der Termvektoren",
            "documents per category": "die Grundrate der Klassifikation",
            "frequency curve": "ob Stopwords und Gewichtung nötig sind",
            "order": "zuerst zählen, dann rechnen"}
