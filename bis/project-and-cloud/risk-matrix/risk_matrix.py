"""Die Risikomatrix aus Wahrscheinlichkeit und Auswirkung."""

SCALE = 5

STRATEGIES = {
    "vermeiden": "die Ursache beseitigen, notfalls das Vorhaben ändern",
    "vermindern": "die Wahrscheinlichkeit oder die Auswirkung senken",
    "übertragen": "das Risiko an einen anderen geben, etwa an eine "
                  "Versicherung oder einen Dienstleister",
    "akzeptieren": "bewusst tragen und beobachten",
}


def strategies():
    """Nennt die vier Strategien im Umgang mit einem Risiko."""
    return dict(STRATEGIES)


def score(probability, impact):
    """Bewertet ein Risiko als Produkt aus Wahrscheinlichkeit und Wirkung.

    Args:
        probability: Wahrscheinlichkeit auf einer Skala von eins bis fünf.
        impact: Auswirkung auf derselben Skala.

    Raises:
        ValueError: bei einem Wert ausserhalb der Skala.
    """
    for value in (probability, impact):
        if not 1 <= value <= SCALE:
            raise ValueError("Wert ausserhalb der Skala von 1 bis %d"
                             % SCALE)
    return probability * impact


def classify(value):
    """Ordnet einen Risikowert einer Klasse zu.

    Raises:
        ValueError: bei einem Wert ausserhalb des möglichen Bereichs.
    """
    if not 1 <= value <= SCALE * SCALE:
        raise ValueError("Wert ausserhalb des möglichen Bereichs")
    if value <= 6:
        return "gering"
    if value <= 14:
        return "mittel"
    return "hoch"


def recommend(value):
    """Schlägt eine Strategie vor.

    Ein geringes Risiko wird getragen, weil die Massnahme mehr kostet als
    der Schaden. Ein mittleres wird vermindert. Ein hohes wird übertragen
    oder vermieden; es einfach hinzunehmen wäre keine Entscheidung,
    sondern das Fehlen einer.

    Raises:
        ValueError: bei einem Wert ausserhalb des möglichen Bereichs.
    """
    kind = classify(value)
    if kind == "gering":
        return "akzeptieren"
    if kind == "mittel":
        return "vermindern"
    return "vermeiden"


def matrix():
    """Baut die volle Matrix aus Wahrscheinlichkeit und Auswirkung.

    Returns:
        Abbildung vom Paar auf Wert, Klasse und Empfehlung.
    """
    built = {}
    for probability in range(1, SCALE + 1):
        for impact in range(1, SCALE + 1):
            value = score(probability, impact)
            built[(probability, impact)] = {"score": value,
                                            "class": classify(value),
                                            "strategy": recommend(value)}
    return built


def what_the_product_hides():
    """Nennt die Schwäche des Produktes.

    Wahrscheinlichkeit eins mal Auswirkung fünf ergibt denselben Wert wie
    fünf mal eins, und die beiden Fälle sind sehr verschieden: das eine
    ist ein seltener Totalschaden, das andere ein ständiges Ärgernis. Wer
    nur den Wert betrachtet, behandelt beide gleich.
    """
    return {"same score": [(1, 5), (5, 1)],
            "different case": ["ein seltener grosser Schaden",
                              "ein häufiger kleiner"],
            "consequence": "die Position in der Matrix mitlesen, nicht nur "
                           "das Produkt",
            "rare and severe": "gehört übertragen, nicht vermindert"}
