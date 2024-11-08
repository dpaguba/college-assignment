"""Die Wahrscheinlichkeiten zweier Würfel."""

from itertools import product

PIPS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}


def ways():
    """Zählt für jede Summe die Zahl der Würfelpaare.

    Gezählt wird durch vollständiges Aufzählen aller sechsunddreissig
    Paare, nicht mit einer Formel. Die Formel kommt danach und wird
    dagegen geprüft.

    Returns:
        Abbildung von der Summe auf die Anzahl der Paare.
    """
    counted = {}
    for first, second in product(range(1, 7), repeat=2):
        counted[first + second] = counted.get(first + second, 0) + 1
    return counted


def probability(number):
    """Die Wahrscheinlichkeit einer Summe.

    Raises:
        ValueError: bei einer Summe ausserhalb von zwei bis zwölf.
    """
    if not 2 <= number <= 12:
        raise ValueError("zwei Würfel geben zwei bis zwölf")
    return ways()[number] / 36.0


def expected_sum():
    """Der Erwartungswert der Augensumme."""
    return sum(number * probability(number) for number in range(2, 13))


def total_pips():
    """Die Summe der Augen auf allen achtzehn Zahlenplättchen.

    Jede Zahl trägt so viele Punkte, wie es Würfelpaare für sie gibt,
    und jede Zahl ausser zwei und zwölf liegt zweimal auf dem Brett.

    Returns:
        Die Summe.
    """
    return sum(PIPS[number] * (1 if number in (2, 12) else 2)
               for number in PIPS)


def seven_in_a_round(players):
    """Die Wahrscheinlichkeit, dass in einer Runde eine Sieben fällt.

    Args:
        players: die Anzahl der Spieler und damit der Würfe.

    Returns:
        Abbildung mit beiden Wahrscheinlichkeiten.

    Raises:
        ValueError: bei einer nicht positiven Spielerzahl.
    """
    if players <= 0:
        raise ValueError("es braucht mindestens einen Spieler")
    without = (1.0 - probability(7)) ** players
    return {"players": players, "no seven": without,
            "at least one seven": 1.0 - without,
            "expected sevens": players * probability(7)}


def why_the_pips_are_printed():
    """Sagt, wozu die Punkte unter der Zahl gut sind.

    Sie sind die Wahrscheinlichkeit in einer Form, die sich addieren
    lässt, ohne zu rechnen: eine Kreuzung an drei Feldern mit zusammen
    zwölf Punkten liefert im Schnitt zwölf Sechsunddreissigstel Karten
    je Wurf. Wer nur auf die Zahlen sieht, vergleicht sechs mit acht und
    hält sie für verschieden; über die Punkte sind sie gleich.
    """
    return {"what a pip is": "ein Würfelpaar für diese Zahl",
            "why it helps": "Punkte lassen sich addieren, "
                            "Wahrscheinlichkeiten nicht so bequem",
            "the pair to remember": "sechs und acht sind gleich stark, "
                                    "ebenso fünf und neun",
            "sum on the board": total_pips()}
